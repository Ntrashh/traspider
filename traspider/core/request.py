import json
from urllib import parse

import aiohttp


class Request:
	def __init__(self, url, callback=None, method=None, headers=None, params=None, data=None, proxy=None, timeout=3,
				 meta={}):
		self.__proxy = proxy
		self.url = url
		self.method = method or "GET"
		self.headers = headers
		self.params = params
		self.__data = data
		self.timeout = timeout
		self.callback = callback
		self.meta = meta

	def parse_url(self, url=None):
		if url is None:
			url = self.url
		query = {i.split("=")[0]: i.split("=")[1] for i in parse.unquote(parse.urlsplit(url).query).split("&") if i}
		url = parse.urlparse(url)
		return {
			"url": url.scheme + "://" + url.netloc + url.path,
			"query": query
		}

	@property
	def data(self):
		return self.__data

	@data.setter
	def data(self, value):
		if value == "null":
			self.__data = None
		else:
			self.__data = value

	@property
	def retry_(self):
		if hasattr(self, "_Request__retry_"):
			return self.__retry_
		return False

	@retry_.setter
	def retry_(self, value):
		if isinstance(value, bool):
			self.__retry_ = value
		else:
			raise ValueError('<retry_ must be a bool type>')


	@property
	def proxy(self):
		if hasattr(self,"_Request__proxy"):
			return self.__proxy
		return None

	@proxy.setter
	def proxy(self,value):
		if isinstance(value,dict):
			if set(value.keys()) == set(["username","password","tunnel"]):
				self.proxy_auth = {
					"username":value["username"],
					"password":value["password"]
				}
				self.__proxy = value["tunnel"]
			else:
				raise ValueError('<Tunnel proxy must contain "username", "password", "tunnel">')
		elif isinstance(value,str):
			self.__proxy = value
		else:
			raise ValueError('<Proxy only supports dict and str>')

	@property
	def proxy_auth(self):
		if hasattr(self,"_Request__proxy_auth"):
			return self.__proxy_auth
		return None


	@proxy_auth.setter
	def proxy_auth(self,value):
		self.__proxy_auth = aiohttp.BasicAuth(value["username"], value["password"])

	def __iter__(self):
		return (i for i in
				(
					self.method, self.url, self.params, self.data, self.proxy, self.meta,
					getattr(self.callback, "__name__")
					if callable(self.callback)
					else self.callback))

	def __repr__(self):
		class_name = type(self).__name__
		return "{}(method:{!r}, url:{!r}, params:{!r}, data:{!r}, proxy:{!r}, meta:{!r}, callback:{!r})".format(
			class_name,
			*self
		)
