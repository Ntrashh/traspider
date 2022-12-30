# traspider

## 简介

traspider是一个开箱即用的轻量爬虫框架

如果你需要写一个小的爬虫,使用traspider会让你事半功倍

github地址:https://github.com/Ntrashh/traspider

### 环境要求
 - Python 3.7.0+
 - Works on Linux, Windows, macOS

### 安装
```cmd
pip3 install traspider
```

### 使用
创建爬虫
```cmd
traspider create -s demo_spider
```

生成代码
添加需要爬取的网址 `http://httpbin.org/`
```python

from loguru import logger
from traspider import Spider

class DemoSpider(Spider):

    def __init__(self):
        self.urls  = ["http://httpbin.org/"]


    def parser(self, response, request):
        logger.info(response)

    async def download_middleware(self, request):
        request.headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
        return request

if __name__ == "__main__":
    demo_spider = DemoSpider()
    demo_spider.start()
```



> traspider这个项目开始之初就是为了爬虫在开发一些简单的项目能够更轻更快,所以对大型项目支持还是不够好。如果开发的是大型爬虫项目,推荐你使用[feapder](https://github.com/Boris-code/feapder)和[scrapy](https://github.com/scrapy/scrapy)



如果你在使用过程中对traspider有任何问题或建议可以联系我

微信:


![wechat](https://user-images.githubusercontent.com/109586486/210029580-4bb2f7bb-ed19-4971-ad0a-788aa659e2ff.jpg)

邮箱:
yinghui0214@163.com


### 鸣谢

[hoopa](https://github.com/fishtn/hoopa)

[feapder](https://github.com/Boris-code/feapder)

[scrapy](https://github.com/scrapy/scrapy)

[huangjin](https://github.com/xianyucoder)
