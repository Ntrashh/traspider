import asyncio
import json
from asyncio import Queue
import aiohttp

from traspider.util import Encrypt

from loguru import logger
from traspider.core.response import Response


class Download:
	def __init__(self):
		self.encrypt = Encrypt()
		self.queue = Queue()
		self.count = 0
		self.dedup = set()  # url去重
		self.error = dict()  # 重试链接
		self.error_count = 0

	async def download(self, request):
		"""
		在这里可以处理下载前和下载后的处理
		:return:
		"""

		response = await self.crawl(request)
		# TODO 在这里做下载中间件之后的处理
		return response

	@logger.catch
	async def crawl(self, request):
		try:
			fingerprint_md5 = self.__encrypt_request(request)
			if self.__verify_request(fingerprint_md5):
				return
			async with aiohttp.ClientSession(
					headers=request.headers, connector=aiohttp.TCPConnector(ssl=False)
			) as session:
				if not self.error.get(fingerprint_md5):
					self.count += 1
				response = await session.request(method=request.method.upper(), url=request.url, params=request.params,
												 data = request.data)
				self.dedup.add(self.__encrypt_request(request))
				return Response(content=await response.read(), request=request, meta=request.meta, response=response)
		except aiohttp.client_exceptions.ClientOSError as e:
			logger.error(e)
		except aiohttp.client_exceptions.ClientConnectorError as e:
			logger.error(e)
		if not self.__error_retry(fingerprint_md5):
			logger.info("重试请求")
			return request

	def __error_retry(self, key):
		if self.error.get(key) == 3:
			self.error_count += 1
			return True
		if self.error.get(key) is None:
			self.error[key] = 1
		else:
			self.error[key] += 1

	def __encrypt_request(self, request):
		"""
		对所有的请求进行md5放入到set中
		:param request:
		:return:
		"""
		data = request.data
		params = request.params
		if isinstance(data, dict):
			data = json.dumps(request.data)
		if data is None:
			data = ""
		if isinstance(params, dict):
			params = json.dumps(request.params)
		if params is None:
			params = ""
		return self.encrypt.md5(request.url + data + params)

	def __verify_request(self, fingerprint_md5):
		"""

		:param request:
		:return:
		"""
		return fingerprint_md5 in self.dedup
