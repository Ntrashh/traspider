from traspider.core.engine import Engine
from traspider.core.request import Request
from traspider.core.response import Response


class Spider:

	def __init__(self):
		self.urls = []
		self.save_path = None


	def start_request(self):

		for url in self.urls:
			yield Request(url, callback=self.parser)

	def parser(self,response:Response,request:Request):
		pass


	def download_middleware(self,request):
		"""爬虫下载器中间件"""
		return request

	def start(self):

		engine = Engine(spider=self)
		engine.start()




