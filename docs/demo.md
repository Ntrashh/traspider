# 案例

## 豆瓣TOP250

```python
from loguru import logger
from traspider import Spider, Request


class DoubanSpider(Spider):

	def __init__(self):
		self.urls = [f"https://movie.douban.com/top250?start={i}&filter=" for i in range(0, 250, 25)]

	def parse(self, response, request):
		urls = response.xpath("//div[@class='hd']/a/@href")
		for url in urls:
			yield Request(url=url, callback=self.parse_detail)

	def parse_detail(self, response, request):
		logger.info(response)

	async def download_middleware(self, request):
		request.headers = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
		}
		return request


if __name__ == "__main__":
	douban_spider = DoubanSpider()
	douban_spider.start()

```
