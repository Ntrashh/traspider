from traspider import Engine

from traspider.core.request import Request
from traspider.core.response import Response
from traspider.util.exception import WrongParameter

from traspider.util.node_vm.node import Node


class Spider:
	def __init__(self):
		self.mysql_setting = {
			"host": "",
			"port": "",
			"user": "",
			"password": "",
			"db": "",
			"charset": "utf-8"
		}
		self.urls = []
		self.save_path = None
		self.paging = True
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

	def generate_total_Request(self, request=None, data=None, total=None, size=None, key=None):
		if not self.paging:
			return []
		self.paging = False
		if isinstance(data, str) and request.url == data:
			for page in range(2, total):
				url_obj = request.parse_url(data)
				url_obj["query"][key] = page
				request.url = url_obj["url"]
				request.params = url_obj["query"]
				yield request
		else:
			if data is None:
				raise WrongParameter('<data cannot be None>')
			all_page = total // size if total % size == 0 else total // size + 1
			for page in range(1, all_page + 1):
				data[key] = page
				if request.data == data:
					request.data[key] = page
					yield request
				elif request.params == data:
					request.params[key] = page
					yield request
				else:
					raise WrongParameter('<Wrong parameter type, data can only be an attribute in the request>')

	def start(self):
		engine = Engine(spider=self)
		engine.start()
