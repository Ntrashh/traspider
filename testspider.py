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
		self.urls = ["https://dm.video.qq.com/barrage/base/z0044divzwu"]
		self.save_path = "danmu.csv"
		self.paging = True
		self.node = Node()

	def parser(self, response, request):
		segment_index = response.json().xpath("segment_index")
		for val in segment_index.values():
			yield Request(url="https://dm.video.qq.com/barrage/segment/z0044divzwu/" + val["segment_name"],
						  callback=self.parse_detail)

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
		items = []
		for id, content in zip(ids, contents):
			item = {}
			item["id"] = id
			item["content"] = content
			items.append(item)
		yield items


if __name__ == '__main__':
	t = TestSpider()
	t.start()
