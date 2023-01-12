# Spider

## 设置初始化爬虫种子
urls是爬虫初始的种子,讲需要爬取的链接放入到urls中
```python
urls = ["www.spider.com/?page=1"]

# 生成1-10页的url
urls = [f"www.spider.com/?page={i}" for i in range(1,10)]

# 初始化爬虫种子为post请求
urls = [{
    "method":"post",
    "url":"www.spider.com",
    "data":{
            "data":"info",
            "page":i
            }
} for i in range(1,10)]
```


## 设置爬取速度
task_num是控制爬虫同时处理任务数,范围是`0-100`,如果不设置task_num默认为100

## 设置响应超时时间
time_out: 控制爬虫的响应时间,范围是`0-20`,如果不设置time_out默认为20

## 设置请求重试次数
retry: 设置每个请求的重试次数,必须要大于0,如果不设置默认为100次

## 设置保存文件路径
save_path:设置数据保存的路径,只支持csv文件和txt文件,设置save_path后,yield后的数据自动被保存到save_path的文件中
```python
def __init__(self):
    self.urls = ["https://xxx.xxxxx.cn/main/index-list.json?page=1&order=1"]
    self.save_path = "data.csv"

def parse(self, response, request):
    datas = response.xpath("//div[@class='list-item']/h4/a/text()").extract()
    for data in datas:
        item = {
            "title":data
        }
        yield item


async def download_middleware(self, request):
    request.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
    return request
```



## 设置保存数据库
mysql数据库设置，如果mysql数据库正确，yield的item将保存到mysql中,注意mysql表中的字段顺序要和item数据保持一致
```python
mysql_setting = {
            "host": "127.0.0.1",
            "port": "3306",
            "user": "root",
            "password": "root",
            "db": "traspider",
            "table": "traspider",
        }
```



## 设置需要加载的js文件: 
node自动加载你所需的js文件,在spider中使用`call_node`就可以调用js中的方法
```python
from traspider import Node
def __init__(self):
    self.urls = ["https://xxx.xxxx.cn/main/index-list.json?page=1&order=1"]
    self.node = Node("md5.js")

async def download_middleware(self, request):
    request.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            "token": self.call_node("md5_func","166143141234")    
    }
    return request
```


## 设置下载中间件
在`download_middleware`中设置在发起请求之前需要做的事情


- 设置请求头

```python
async def download_middleware(self, request):
    request.headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    return request
```

- 将json转为str

```python
async def download_middleware(self, request):
    request.data = json.dumps(request.data)
    return request
```
  
- 设置代理 (目前支持隧道代理)
```python
async def download_middleware(self, request):
    request.proxy = {
            "username":"username",
            "password":"password",
            "tunnel": "http://xxx.xxx.com:88888"
    }     
    return request
```
  
## 生成request
在请求数据的时候,不知道结束的页码但是返回值会有一个数据总量,可以使用`generate_total_request`方法直接生成后续请求,`generate_total_request`有5个参数

- request:方法参数中request

- data : 需要改变的值

- total : 数据总量

- size : 每页请求的数据数 (如果total为总页数,size为1)

- key : data中需要改变的key

```python
#https://xxx.xxxx.cn/main/index-list.json?pagenumber=1&order=1

for req in self.generate_total_Request(request, data=request.url, total=30, size=1,key="pagenumber"):
    yield req
```

```python
total = json_data.xpath("data/total")
for req in self.generate_total_Request(request, data=request.data, total=total, size=20,key="page"):
    yield req
```