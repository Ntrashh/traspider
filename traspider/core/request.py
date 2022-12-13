from urllib import parse


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

	def parse_url(self,url=None):
		if url is None:
			url = self.url
		query = {i.split("=")[0]: i.split("=")[1]for i in parse.unquote(parse.urlsplit(url).query).split("&") if i}
		url = parse.urlparse(url)
		return {
			"url":url.scheme+"://"+url.netloc+url.path,
			"query":query
		}

	#使用 urlencode() 函数可以将一个 dict 转换成合法的查询参数：
