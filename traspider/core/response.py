import json
from lxml import etree
import chardet

from traspider.util.element import Element


class Response:
	def __init__(self, content, request, meta, response):
		self.content = content
		self.request = request
		self.meta = meta
		self.response = response
	
	@property
	def status_code(self):
		return self.response.status

	def json(self):
		return json.loads(self.content.decode())

	def text(self, encoding=None):
		"""自动解析html编码"""
		if encoding is None:
			char_code = chardet.detect(self.content)
			encoding = char_code.get('encoding', 'utf-8')
			if encoding is None:
				# 如果编码获取不到则抛出错误
				raise TypeError
		return self.content.decode(encoding, errors='ignore')

	def xpath(self, xpath_str):
		root = etree.HTML(self.text())
		return Element(root.xpath(xpath_str))
