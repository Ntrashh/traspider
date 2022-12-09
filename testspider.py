import time

from loguru import logger

from traspider import spider
from traspider.core.request import Request


class TestSpider(spider.Spider):
	def __init__(self):
		self.urls = ["https://www.imau.edu.cn/zhxw/ndxw.htm"]



	def parser(self,response,request):
		if response is None:
			return
		urls = response.xpath('//li[contains(@id,"line_u4_")]/a/@href').extract()

		for url in urls:
			yield Request(url="https://www.imau.edu.cn"+url.split("..")[-1],callback=self.parse_detail)

		next_url = response.xpath('//a[contains(text(),"下页")]/@href').extract()

		if len(next_url) == 0:
			return
		yield Request(url="https://www.imau.edu.cn/zhxw/"+next_url[0],callback=self.parser)


	def parse_detail(self,response,request):
		if response is None:
			return
		logger.info(f"{response.status_code} 请求链接:{request.url}")

if __name__ == '__main__':
	start = time.time()
	t = TestSpider()
	t.start()
	logger.info(f"end:{start - time.time()}")