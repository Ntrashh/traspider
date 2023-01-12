# Response

- response.text: 获取response的文本.如果自动解码失败,也可以response.text(encoding="xxxx")来设置网页的编码
- response.json: 获取response的json数据



## xpath选择器 

取a标签的的全部文本
```python
response.xpath("//div[@class='list-item']/h4/a/text()").extract()
```

取a标签的第一个文本
```python
response.xpath("//div[@class='list-item']/h4/a").extract_first()
```

## json选择器
返回的json数据例如
```python
{
"data":
    "list":[
        {
        "id":1,
        "title":标题1"
        },
        {
        "id":2,
        "title":标题2"
        },
        {
            "id":3,
            "title":标题3"
        }
    ],
    "total":1000
}
```
获取total
```python
json_data = response.json
json_data.xpath("data/total")
```

获取id
```python
json_data.xpath("data/list[*]/id")
```
在json中list的值是列表,可以使用[*]来表示

