import asyncio
import sys
import time

from loguru import logger
import csv

from traspider.util.log import Logging
from traspider.core.download import Download
from traspider.core.request import Request
from traspider.core.scheduler import Scheduler
from traspider.util.exception import FileTypeUnsupported
from traspider.util.tramysql.tramysql import AioMysql


class Engine:
	def __init__(self, spider):
		self.logging = Logging()
		self.spider = spider
		self.scheduler = Scheduler()
		self.download = Download(spider.retry,spider.time_out)
		self.item_count = 0
		self.loop = asyncio.get_event_loop()
		self.__task_list = []
		self.__loop_flag = True
		self.save_type = None
		self.aiomysql = AioMysql(self.spider.mysql_setting)
		self.__mysql_switch = False

	async def process_request(self, request):
		"""
		使用下载器下载请求
		:param request:
		:return:
		"""
		if request is None:
			return
		response = await self.download.download(self.spider, request)
		# 如果下载器下载失败response为空
		if response is None:
			return
		# 如果返回的是request类型则是重试的request  加入到队列中
		if isinstance(response, Request):
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
		item_list = []
		# 如果callback为空的情况下,回调方法为默认的parse
		if request.callback is None:
			request.callback = self.spider.parse
		callback_results = request.callback(response, request)
		# 如果callback的结果为空再次不会
		if callback_results is None:
			return
		for result in callback_results:
			if isinstance(result, Request):
				await self.scheduler.add_scheduler(result)
			elif isinstance(result, dict):
				self.item_count += 1
				item_list.append(result)
			else:
				raise TypeError("item only supports dicts and lists")
		await self.process_item(item_list)

	async def process_future(self, future):
		self.__task_list.append(future)
		if len(self.__task_list) == self.spider.task_num or not await self.scheduler.scheduler_qsize():
			# 获取所有完成任务和未完成任务
			dones, pending = await asyncio.wait(self.__task_list)
			# 如果有未完成任务在此等待
			while pending:
				pass
			self.__loop_flag = False
			self.__task_list.clear()

	async def process_item(self, item):
		if len(item) == 0:
			return
		
		# 判断是否开启mysql
		if self.__mysql_switch:
			await self.aiomysql.batchInsert(item)
		if self.spider.save_type == "csv":
			asyncio.ensure_future(self.write_csv(item))
		elif self.spider.save_type == "txt":
			asyncio.ensure_future(self.write_txt(item))

	async def write_csv(self, item):
		with open(self.spider.save_path, "a+", newline="", encoding="utf-8") as f:
			csv_obj = csv.writer(f)
			csv_obj.writerows([i.values() for i in item])

	async def write_txt(self, items):
		with open(self.spider.save_path, "a+", newline="", encoding="utf-8") as f:
			write_data = [await self.__dict_to_str(item) for item in items]
			f.writelines(write_data)

	async def __dict_to_str(self, item):
		return " ".join(item.values()) + "\n"

	async def __init_mysql(self):
		# 如果mysql的配置不正确不运行
		conn_result = await self.aiomysql.inspection_conn()
		if conn_result is False:
			sys.exit()
		elif conn_result is None:
			self.__mysql_switch = False
		else:
			self.__mysql_switch = True

	async def _init_db(self):
		"""
		初始化数据库配置,进行链接检测
		:return:
		"""
		await self.__init_mysql()


	async def engine(self, start_requests):
		await self._init_db()
		for request in start_requests:
			await self.scheduler.add_scheduler(request)
		while self.__loop_flag or await self.scheduler.scheduler_qsize():
			request = await self.scheduler.next_request()
			future = asyncio.ensure_future(self.process_request(request))
			await self.process_future(future)

	def __print_log(self):
		print(
			"""

								   __                           _     __         
								  / /___  ________ __________  (_)___/ /__  _____
								 / __/  / ___/ __ `/ ___/ __ \/ / __  / _ \/ ___/
								/ /_/  / /  / /_/ (__  ) /_/ / / /_/ /  __/ /    
								\__/  /_/   \__,_/____/ .___/_/\__,_/\___/_/     
												  /_/                         
		"""
		)

	def start(self):
		self.__print_log()
		start = time.time()
		logger.info(f"{'*' * 20}爬虫启动{'*' * 20}")
		start_requests = iter(self.spider.start_request())
		self.loop.run_until_complete(self.loop.create_task(self.engine(start_requests)))
		logger.info(f"""spider end ...
								request_count:{self.download.count}
								error_request_count:{self.download.error_count}
								storage_item:{self.item_count}
								time_consuming:{time.time() - start}
								""")
