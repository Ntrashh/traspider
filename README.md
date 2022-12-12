# traspider:一个开箱即用的爬虫框架 




**generate_total_Request** 功能

`generate_total_Request`是生成后续所有Request请求的一个方法，一共有5个参数
- request:`parser`方法中的request参数
- data: 需要修改的request中的属性，params或data
- total: 总量数据,如果没有总量数据也可以传入总页数
- size:每页的size，如果taotal传入的参数是总页数，那size传入1
- key: data中需要修改的key

```python
def parser(self, response, request):
    for i in range(1,101):
        yield Request(url=f"https://www.gongbiaoku.com/search?pageNo={i}&query=&status=&itemCatIds=1190&orderField=top&asc=0&style=", callback=self.parser)
```
```python
def parser(self, response, request):
    for req in self.generate_total_Request(request=request,data=request.url,total=100,size=1,key="pageNo"):
        yield req
```

```python

```