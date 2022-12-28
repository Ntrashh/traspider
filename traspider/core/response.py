import json
from lxml import etree
import chardet

from traspider.util import TraJson
from traspider.util.element.element import Element, ElementIter


class Response:
	def __init__(self, content, request, meta, response):
		self.content = content
		self.request = request
		self.meta = meta
		self.__response = response
	
	@property
	def status_code(self):
		return self.__response.status

	def json(self):
		json_data =  json.loads(self.content.decode())
		return TraJson(json_data)

	def text(self, encoding=None):
		"""自动解析html编码"""
		if encoding is None:
			char_code = chardet.detect(self.content)
			encoding = char_code.get('encoding', 'utf-8')
			if encoding is None:
				# 如果编码获取不到则抛出错误
				raise TypeError('<Unsupported encoding type, please specify encoding type.>')
		return self.content.decode(encoding, errors='ignore')

	def xpath(self, query):
		root = etree.HTML(self.text())
		xpath_result = root.xpath(query)
		if isinstance(xpath_result,list):
			return ElementIter(xpath_result)
		else:
			return Element(xpath_result)


	def __iter__(self):
		return (i for i in (self.status_code,self.request))

	def __repr__(self):
		class_name = type(self).__name__
		return "{}(method:{!r}, request:{!r})".format(
			class_name,
			*self
		)