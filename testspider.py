import time
from loguru import logger
from traspider import Node
from traspider.core import spider
from traspider.core.request import Request



class TestSpider(spider.Spider):
	def __init__(self):
		self.urls = []
		self.save_path = ""
		self.paging = True
		self.node = Node("aa.js")

	def start_request(self):

		url = "https://www.gongbiaoku.com/search?pageNo=1&query=&status=&itemCatIds=1190&orderField=top&asc=0&style="

		yield Request(method="GET", url=url, callback=self.parser)

	def parser(self, response, request):
		for req in self.generate_total_Request(request=request,data=request.params,total=100,size=10,key="pageNo"):
			yield req

		total = response.json().xpath("total")
		for req in self.generate_total_Request(request=request,data=request.params,total=total,size=10,key="pageNo"):
			yield req


		for i in range(1,all_page+1):
			params  = {
				"pageNo": i,
				"pageSize": 10,
				"area": "",
				"publishTimeStart": "",
				"publishTimeEnd": "",
				"title": ""
			}
			yield Request(url="https://www.xxxxxx.com/search",params=params,callback=self.parser)
		# legal_name = response.json().xpath("creditinfo[*]/legal_name")
		# for name in legal_name:
		# 	item["name"] = name
		# 	logger.info(item)
		# # 	yield item
		# for i in range(1,101):
		# 	yield Request(url=f"https://www.gongbiaoku.com/search?pageNo={i}&query=&status=&itemCatIds=1190&orderField=top&asc=0&style=", callback=self.parser)

	# pass
	# if response is None:
	# 	return
	# urls = response.xpath('//li[contains(@id,"line_u4_")]/a/@href').extract()
	# for url in urls:
	# 	yield Request(url="https://www.imau.edu.cn"+url.split("..")[-1],callback=self.parse_detail)
	# next_url = response.xpath('//a[contains(text(),"下页")]/@href').extract()
	# if len(next_url) == 0:
	# 	return
	# yield Request(url="https://www.imau.edu.cn/zhxw/"+next_url[0],callback=self.parser)

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
		logger.info(f"{response.status_code} 请求链接:{request.url}")


if __name__ == '__main__':
	start = time.time()
	t = TestSpider()
	t.start()
	logger.info(f"end:{start - time.time()}")
