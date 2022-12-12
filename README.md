# traspider:一个开箱即用的轻量爬虫框架 



**self.save_path属性**
save_path属性是用来设置爬虫文件的保存格式的,目前只支持`csv`和`txt`两种格式的文件,如果设置了save_path属性,则爬虫文件就会保存,否则就不会保存数据

**spider.node属性**

在我们爬取数据中经常会遇到加密参数,self.node就是加载需要运行的js文件来获取加密参数

在spider中可以这样实例化一个node对象,node对象是可以帮助我们运行我们需要调用的js文件,在下载件中间件`download_middleware`中来添加加密参数
```python
class MySpider(Spider):
    def __init__(self):
        self.paging = True
        self.node = Node("需要加载的js文件")
       
        
    async def download_middleware(self, request):
        request.params["sign"] = self.node.call_node(func_name,"arg1","arg2")
        return request
```




**spider.generate_total_Request方法**

`generate_total_Request`是生成后续所有Request请求的一个方法，一共有5个参数
- request:`parser`方法中的request参数
- data: 需要修改的request中的属性，params或data
- total: 总量数据,如果没有总量数据也可以传入总页数
- size:每页的size，如果taotal传入的参数是总页数，那size传入1
- key: 参数data中需要修改的key


```python
# 生成所有请求url
def parser(self, response, request):
    for i in range(1,101):
        yield Request(url=f"https://www.gongbiaoku.com/search?pageNo={i}&query=&status=&itemCatIds=1190&orderField=top&asc=0&style=", callback=self.parser)
```
```python
# traspider生成所有请求url 
def parser(self, response, request):
    for req in self.generate_total_Request(request=request,data=request.url,total=100,size=1,key="pageNo"):
        yield req
```

```python
# 生成所有请求params
def parser(self, response, request):
    total = response.json().xpath("total")
    all_page = total // 10 if total % 10 == 0 else total // 10 + 1
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
```

```python
#traspider生成所有请求params
def parser(self, response, request):
    total = response.json().xpath("total")
    for req in self.generate_total_Request(request=request,data=request.params,total=total,size=10,key="pageNo"):
        yield req
```


```python
# 生成所有请求data
def parser(self, response, request):
    total = response.json().xpath("total")
    all_page = total // 10 if total % 10 == 0 else total // 10 + 1
    for i in range(1,all_page+1):
        data  = {
            "pageNo": i,
            "pageSize": 10,
            "area": "",
            "publishTimeStart": "",
            "publishTimeEnd": "",
            "title": ""
        }
        yield Request(method="POST",url="https://www.xxxxxx.com/search",data=data,callback=self.parser)
```

```python
#traspider生成所有请求data
def parser(self, response, request):
    total = response.json().xpath("total")
    for req in self.generate_total_Request(request=request,data=request.data,total=total,size=10,key="pageNo"):
        yield req
```


### 鸣谢

[hoopa](https://github.com/fishtn/hoopa)

[feapder](https://github.com/Boris-code/feapder)

[aioScrapy](https://github.com/ScrapingBoot/aioScrapy)

[scrapy](https://github.com/scrapy/scrapy)

[huangjin](https://github.com/xianyucoder)