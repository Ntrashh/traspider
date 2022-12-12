from traspider.core.engine import Engine
from traspider.core.request import Request
from traspider.core.response import Response
from node_vm2 import NodeVM

from traspider.util.node_vm.node import Node


class Spider:
	def __init__(self):
		self.urls = []
		self.save_path = None
		self.node = Node()

	def start_request(self):
		for url in self.urls:
			yield Request(url, callback=self.parser)

	def parser(self, response: Response, request: Request):
		pass

	def download_middleware(self, request):
		"""爬虫下载器中间件"""
		return request

	def call_node(self, func, *args, **kwargs):
		return self.node.call_node(func, *args, **kwargs)

	def start(self):
		engine = Engine(spider=self)
		engine.start()
