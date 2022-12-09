class Request:
	def __init__(self,url,callback,method = None,headers=None, params=None, data=None, timeout=3,meta = {}):
		self.url = url
		self.method = method or "GET"
		self.headers = headers
		self.params = params
		self.data = data
		self.timeout = timeout
		self.callback = callback
		self.meta = meta
