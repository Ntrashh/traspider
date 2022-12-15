from loguru import logger

from traspider import Engine

from traspider.core.request import Request
from traspider.core.response import Response
from traspider.util.exception import WrongParameter

from traspider.util.node_vm.node import Node


class Spider:
	def __init__(self):
		self.urls = []  # 起始url
		self.node = Node()  # 运行js的node

	def start_request(self):
		for url in self.urls:
			if isinstance(url,str):
				yield Request(url, callback=self.parser)
			elif isinstance(url,dict):
				if url.get("url") is None:
					raise ValueError(f"The url attribute in urls cannot be empty:{url}")
				yield Request(url=url.get("url"),params=url.get("params"),data=url.get("data"),callback=self.parser)
			else:
				raise ValueError("<Only dictionaries and strings can be stored in urls>")


	def parser(self, response: Response, request: Request):
		pass

	def download_middleware(self, request):
		"""爬虫下载器中间件"""
		return request

	def call_node(self, func, *args, **kwargs):
		return self.node.call_node(func, *args, **kwargs)

	def generate_total_Request(self, request=None, data=None, total=None, size=None, key=None):
		if not self.paging:
			return
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
					request.data = data
					yield request
				elif request.params == data:
					request.params = page
					yield request
				else:
					raise WrongParameter('<Wrong parameter type, data can only be an attribute in the request>')

	@property
	def retry(self):
		if hasattr(self, "_Spider__retry"):
			return self.__retry
		return 100

	@retry.setter
	def retry(self, value):
		if value < 0 and not isinstance(value, int):
			raise ValueError('<The retry attribute must be an integer and greater than 0>')
		self.__retry = value

	@property
	def paging(self):
		if hasattr(self, "_Spider__paging"):
			return self.__paging
		return True

	@paging.setter
	def paging(self, value):
		self.__paging = value

	@property
	def mysql_setting(self):
		if hasattr(self, "_Spider__mysql_setting"):
			return self.__mysql_setting
		return {
			"host": "",
			"port": "",
			"user": "",
			"password": "",
			"db": "",
			"table": "",
		}

	@mysql_setting.setter
	def mysql_setting(self, value):
		if not isinstance(value, dict):
			raise ValueError('<mysql_setting must be a dictionary type>')
		if self.__check_mysql_setting_key(value):
			missing_keys = self.__check_mysql_setting_key(value)
			raise ValueError(f'<mysql_setting is missing the following fields:{missing_keys}>')
		self.__mysql_setting = value

	def __check_mysql_setting_key(self, mysql_setting: dict):
		"""
		检测mysql_setting中所需要的属性是否存在
		:param mysql_setting:
		:return:
		"""
		template = {
			"host": "",
			"port": "",
			"user": "",
			"password": "",
			"db": "",
			"table": "",
		}
		missing_keys = []
		for key in template.keys():
			if mysql_setting.get(key) is None:
				missing_keys.append(key)
		return missing_keys

	@property
	def save_path(self):
		if hasattr(self, "_Spider__save_path"):
			return self.__save_path
		return ""

	@save_path.setter
	def save_path(self, value: str):
		# 判断赋值路径是不是字符串
		if not isinstance(value, str):
			raise ValueError("<The save_path attribute only supports strings>")
		if value == "":
			self.__save_type = ""
			self.__save_path = value
			return
		if '.' not in value or len(value.split(".")) < 2:
			raise ValueError("<save_path is not a filename>")
		file_type = value.split(".")[-1]
		# 判断赋值的路径是不是csv或txt
		if file_type not in ["csv", "txt"]:
			raise ValueError(f'<{file_type} is an unsupported file type>')
		self.__save_type = file_type
		self.__save_path = value

	@property
	def save_type(self):
		if hasattr(self, "_Spider__save_type"):
			return self.__save_type
		return ""

	@property
	def node(self):
		if hasattr(self,"_Spider__node"):
			return self.__node
		return None

	@node.setter
	def node(self,value):
		if not isinstance(value,Node):
			raise ValueError('<The node attribute must be of Node class>')
		self.__node = value

	@property
	def task_num(self):
		if hasattr(self, "_Spider__task_num"):
			return self.__task_num
		return 100

	@task_num.setter
	def task_num(self,value):
		if value < 1 or value > 100:
			raise ValueError("task_num can only be between 1-100")
		self.__task_num = value

	@property
	def time_out(self):
		if hasattr(self, "_Spider__time_out"):
			return self.__time_out
		return 5

	@time_out.setter
	def time_out(self, value):
		if value < 1 or value > 20:
			raise ValueError("time_out can only be between 1-20")
		self.__time_out = value


	def start(self):
		engine = Engine(spider=self)
		engine.start()
