import json
from urllib import parse


class Request:
    def __init__(self, url, callback=None, method=None, headers=None, params=None, data=None, proxy=None, timeout=3,
                 meta={}):
        self.url = url
        self.method = method or "GET"
        self.headers = headers
        self.params = params
        self.__data = data
        self.proxy = proxy
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
    def data(self,value):
        if value == "null":
            self.__data = None
        else:
            self.__data = value

    def __iter__(self):
        return (i for i in
                (self.method, self.url, self.params, self.data, self.proxy, self.meta, getattr(self.callback, "__name__")
            if callable(self.callback)
            else self.callback))

    def __repr__(self):
        class_name = type(self).__name__
        return "{}(method:{!r}, url:{!r}, params:{!r}, data:{!r}, proxy:{!r}, meta:{!r}, callback:{!r})".format(
            class_name,
            *self
        )
