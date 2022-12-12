from loguru import logger


from traspider.core.engine import Engine
from traspider.core.request import Request
from traspider.core.response import Response


class Spider:
	def __init__(self):
		self.urls = []


	def start_request(self):
		logger.info("爬虫启动")

		for url in self.urls:
			yield Request(url, callback=self.parser,meta={"index":1})

	def parser(self,response:Response,request:Request):
		pass




	def start(self):

		engine = Engine(spider=self)
		engine.start()



