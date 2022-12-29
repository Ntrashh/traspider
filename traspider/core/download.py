import asyncio
import json
import aiohttp
from traspider.util import Encrypt
from loguru import logger
from traspider.core.response import Response


class Download:
    def __init__(self, retry, time_out):

        self.retry = retry
        self.time_out = time_out
        self.encrypt = Encrypt()
        self.count = 0
        self.dedup = set()  # url去重
        self.error = dict()  # 重试链接
        self.error_count = 0

    async def download(self, spider, request):
        """
		在这里可以处理下载前和下载后的处理
		:return:
		"""
        # 如果不是重试的request就放入到下载中间件中
        if not request.retry_:
            request = await spider.download_middleware(request)
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
                response = await session.request(
                    method=request.method.upper(),
                    url=request.url,
                    params=request.params,
                    data=request.data,
                    proxy=request.proxy,
                    proxy_auth=request.proxy_auth,
                    timeout=self.time_out
                )
                logger.info(f"""<response: <Response {response.status}>> url:{request.url}
								请求次数:{self.error.get(fingerprint_md5, 0) + 1}""")
                self.dedup.add(self.__encrypt_request(request))
                return Response(content=await response.read(), request=request, meta=request.meta, response=response)
        except aiohttp.client_exceptions.ClientOSError as e:
            pass
        except aiohttp.client_exceptions.ClientConnectorError as e:
            pass
        except aiohttp.client_exceptions.ServerDisconnectedError as e:
            pass
        except asyncio.exceptions.TimeoutError as e:
            logger.error("请求超时!")
        except aiohttp.client_exceptions.ClientHttpProxyError as e:
            logger.error(f"代理链接失败:{e}")
        if not self.__error_retry(fingerprint_md5):
            logger.info(
                f"<重试请求次数:{self.error.get(fingerprint_md5, 0)}  url={request.url} params={request.params} data={request.data}>")
            request.retry_ = True
            return request

    def __error_retry(self, key):
        # 如果重试的request指纹次数等于重试次数
        if self.error.get(key) == self.retry:
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
