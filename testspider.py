import time
from loguru import logger
from traspider import Node
from traspider.core import spider
from traspider.core.request import Request


class TestSpider(spider.Spider):
	def __init__(self):
		self.mysql_setting = {
			"host": "",
			"port": "",
			"user": "",
			"password": "",
			"db": "",
			"table":"",
		}
		# {
		# 	"host": "127.0.0.1",
		# 	"port": 3306,
		# 	"user": "root",
		# 	"password": "root",
		# 	"db": "tengxun",
		# 	"table":"danmu",
		# }
		self.urls = [
			"https://www.gongbiaoku.com/search?pageNo=1&query=&status=&itemCatIds=1190&orderField=top&asc=0&style="]  # ["https://dm.video.qq.com/barrage/base/z0044divzwu"]

		self.save_path = "danmu.csv"
		self.paging = True
		self.node = Node()

	def parser(self, response, request):
		clearfixs = response.xpath("//li[@class='clearfix']").extract_first()
		print(clearfixs)
		# for clearfix in clearfixs:
		# 	print(clearfix.xpath(".//a[@class='line fl']/text()").extract_first())

	async def download_middleware(self, request):
		request.headers = {
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Accept-Language": "zh-CN,zh;q=0.9",
			"Cache-Control": "no-cache",
			"Connection": "keep-alive",
			"Pragma": "no-cache",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "none",
			"Sec-Fetch-User": "?1",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
			"sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
			"sec-ch-ua-mobile": "?0",
			"sec-ch-ua-platform": "\"Windows\""
		}
		return request

	def parse_detail(self, response, request):
		if response is None:
			return

		contents = response.json().xpath("barrage_list[*]/content")
		ids = response.json().xpath("barrage_list[*]/id")
		for id, content in zip(ids, contents):
			item = {
				"id": id,
				"content": content
			}
			yield item


if __name__ == '__main__':
	t = TestSpider()
	t.start()
