from traspider.core.engine import Engine
from traspider.core.request import Request
from traspider.core.response import Response


class Spider:

	def __init__(self):
		self.urls = []


	def start_request(self):

		for url in self.urls:
			yield Request(url, callback=self.parser)

	def parser(self,response:Response,request:Request):
		pass




	def start(self):

		engine = Engine(spider=self)
		engine.start()




