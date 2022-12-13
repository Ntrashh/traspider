import asyncio

from loguru import logger
import csv
from traspider import Logging
from traspider.core.download import Download
from traspider.core.request import Request
from traspider.core.scheduler import Scheduler
from traspider.util.myexception import FileTypeUnsupported


class Engine:
	def __init__(self, spider):
		self.logging = Logging()
		self.spider  = spider
		self.scheduler = Scheduler()
		self.download = Download()
		self.task_num = 5
		self.loop = asyncio.get_event_loop()
		self.task_list = []
		self.loop_flag = True
		self.save_type = None

	def next_request(self):
		pass

	async def process_request(self, request):
		"""
		使用下载器下载请求
		:param request:
		:return:
		"""
		response = await self.download.download(self.spider,request)
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
			else:
				await self.process_item(result)

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

	async def process_item(self,item):
		if self.save_type == "csv":
			await self.write_csv(item)
		elif self.save_type == "txt":
			await self.write_txt(item)

	async def write_csv(self,item):
		with open(self.spider.save_path,"a+",newline="",encoding="utf-8")as f:
			csv_obj = csv.writer(f)
			csv_obj.writerow(item.values())

	async def write_txt(self,item):
		with open(self.spider.save_path,"a+",newline="",encoding="utf-8")as f:
			f.write(await self.__dict_to_str(item))

	async def __dict_to_str(self,item):
		return " ".join(item.values())+"\n"

	async def engine(self, start_requests):
		for request in start_requests:
			await self.scheduler.add_scheduler(request)
		while self.loop_flag or await self.scheduler.scheduler_qsize():
			request = await self.scheduler.next_request()
			task = asyncio.ensure_future(self.process_request(request))
			await self.process_task(task)

	def __init_save(self,save_path):
		if save_path is None or save_path == "":
			return
		suffisso = save_path.split(".")[-1]
		if suffisso in ['csv', "txt"]:
			self.save_type = suffisso
		else:
			raise FileTypeUnsupported(f'<{suffisso} is an unsupported file type>')


	def start(self):
		logger.info(f"{'*'*20}爬虫启动{'*'*20}")
		self.__init_save(self.spider.save_path)
		start_requests = iter(self.spider.start_request())
		self.loop.run_until_complete(self.loop.create_task(self.engine(start_requests)))
		logger.info(f"""
									总请求:{self.download.count}
									错误请求:{self.download.error_count}
					""")
