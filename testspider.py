import time

from loguru import logger

from traspider.core import spider



from traspider.core.request import Request


class TestSpider(spider.Spider):
	def __init__(self):
		self.save_path = "demo.txt"
		self.urls = [f"https://www.gongbiaoku.com/search?pageNo={i}&query=&status=&itemCatIds=1190&orderField=top&asc=0&style=" for i in range(100)]


	def start_request(self):
		headers = {
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"Accept-Language": "zh-CN,zh;q=0.9",
			"Cache-Control": "no-cache",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"Origin": "http://ggzyjy.sc.gov.cn",
			"Pragma": "no-cache",
			"Proxy-Connection": "keep-alive",
			"Referer": "http://ggzyjy.sc.gov.cn/cxgl/sincerity-creditinfo.html",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
			"X-Requested-With": "XMLHttpRequest"
		}
		url = "http://ggzyjy.sc.gov.cn/WebBuilder/rest/credit/getList"
		for i in range(1,100):
			data = {
				"name": "",
				"code": "",
				"type": "00",
				"sttime": "",
				"endtime": "",
				"pageSize": "15",
				"index": i
			}
			yield Request(method="POST",url=url,data=data,headers=headers,callback=self.parser)

	def parser(self,response,request):
		item  = {}
		legal_name = response.json().xpath("creditinfo[*]/legal_name")
		for name in legal_name:
			item["name"] = name
			yield item
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


	def parse_detail(self,response,request):
		if response is None:
			return
		logger.info(f"{response.status_code} 请求链接:{request.url}")


if __name__ == '__main__':
	start = time.time()
	t = TestSpider()
	t.start()
	logger.info(f"end:{start - time.time()}")
