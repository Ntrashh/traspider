import asyncio

from loguru import logger

from traspider import Logging
from traspider.core.download import Download
from traspider.core.request import Request
from traspider.core.scheduler import Scheduler


class Engine:
	def __init__(self, spider):
		self.logging = Logging()
		self.spider = spider
		self.scheduler = Scheduler()
		self.download = Download()
		self.task_num = 5
		self.loop = asyncio.get_event_loop()
		self.task_list = []
		self.loop_flag = True

	def next_request(self):
		pass

	async def process_request(self, request):
		"""
		使用下载器下载请求
		:param request:
		:return:
		"""
		response = await self.download.download(request)
		if response is None:
			return
		if isinstance(response,Request):
			await self.scheduler.add_scheduler(response)
			return
		await self.process_response(response, request)

	async def process_response(self, response, request):
		"""
		处理获取到的response并使用request的回调方法进行解析
		:param response:获取到的response
		:param request:发起请求的request
		:return:
		"""
		results = request.callback(response, request)
		if results is None:
			return
		for result in results:
			if isinstance(result, Request):
				await self.scheduler.add_scheduler(result)

	async def process_task(self, task):
		self.task_list.append(task)
		if len(self.task_list) == 100 or not await self.scheduler.scheduler_qsize():
			# 获取所有完成任务和未完成任务
			dones, pending = await asyncio.wait(self.task_list)
			# 如果有未完成任务在此等待
			while pending:
				pass
			self.loop_flag = False
			self.task_list.clear()

	async def engine(self, start_requests):
		for request in start_requests:
			await self.scheduler.add_scheduler(request)
		while self.loop_flag or await self.scheduler.scheduler_qsize():
			request = await self.scheduler.next_request()
			logger.info(request)
			task = asyncio.ensure_future(self.process_request(request))
			await self.process_task(task)

	def start(self):
		start_requests = iter(self.spider.start_request())
		self.loop.run_until_complete(self.loop.create_task(self.engine(start_requests)))
		logger.info(f""
					f"总请求:{self.download.count} \n"
					f"错误请求:{self.download.error_count}")
