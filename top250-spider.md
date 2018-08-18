# 豆瓣电影TOP250抓取

**详细分析见个人博客：[豆瓣电影TOP250抓取](https://blog.csdn.net/dta0502/article/details/81811931)**

本文是Python爬取豆瓣的top250电影的分析和实现，具体是将电影的标题、电影描述、电影的评分、电影的评论数以及电影的一句影评抓取下来，然后输出csv文件。

- 第一步：打开豆瓣电影top250这个页面。
- 第二步：分析网页源代码，找到我们需要爬取的信息的标签，例如电影title的标签等等是什么。
- 第三步：写代码了，将整个html请求下来，然后解析网页，获取我们需要的信息，利用lxml进行解析。

-------------------

## 网页分析
首先打开豆瓣电影top250，我们可以看到电影是按照一个列表呈现出来的，页面是通过最底部的12345...来进行翻页查看的。

###  定位页面元素
我通过chrome的开发者工具来分析页面元素。下面是chrome的检查的页面：
![chrome页面元素选择.png](https://github.com/dta0502/douban-top250/blob/master/images/chrome%E9%A1%B5%E9%9D%A2%E5%85%83%E7%B4%A0%E9%80%89%E6%8B%A9.png)

点击上图中画圆圈的图标，然后自己鼠标在页面上选中一部分，就会直接定位到具体的地方了。

###  电影信息的位置
通过上面所说的方法，我们可以观察得到所有列表是放在一个class = 'grid_view'的ol标签中的，这个标签下的每一个li标签就是每一部电影信息的Item。

####  ol标签的XPath路径
```XML
//*[@id="content"]/div/div[1]/ol
```
####  电影标题的XPath路径
```XML
//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a/span[1]
```
####  电影的描述
```XML
//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[1]
```
####  电影评分的XPath路径
```XML
//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/div/span[2]
```
####  电影评论数的XPath路径
```XML
//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/div/span[4]
```
####  电影的一句经典影评
```XML
//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[2]/span
```
 
### 翻页
每一页网址的变化规律，一页可以显示25部电影，就是说这250部电影一共有10页。观察前几页的网址很容易发现规律：就是start后面跟的参数变化，等于（页数-1）*25，而且发现后面的filter去掉也不影响。
```
https://movie.douban.com/top250?start=0
https://movie.douban.com/top250?start=25
...
https://movie.douban.com/top250?start=225
```

**现在完成了整个网页的分析，下面开始实现爬取**

-------------------

##  Python实现爬取(baseline model)
###  导入第三方库
####  [requests](http://docs.python-requests.org/en/latest/#)
requests模块取代内建的urllib2模块，因为其速度更快而且可读性更好。

####  [lxml](http://lxml.de/)
lxml是一个优美的扩展库，用来快速解析XML以及HTML文档即使所处理的标签非常混乱。

```python
import requests
from lxml import etree
import csv
```

### requests获取页面
这里我们将使用 requests.get 来从页面中取得我们的数据， 通过使用 html 模块解析它，并将结果保存到 tree 中。
```python
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
data = requests.get(url,headers = headers).text
```
```python
selector = etree.HTML(data)
```

etree现在包含了整个HTML文件到一个优雅的树结构中，我们可以使用两种方法访问：

- XPath：XPath是一种在结构化文档（如HTML或XML）中定位信息的方式。
- CSS选择器。  

下面我采用XPath方法来定位信息。

### 电影信息的XPath路径获取
Chrome可以右键元素，选择‘Inspect element'，高亮这段代码，再次右击，并选择‘Copy XPath'。   
下面是根据XPath路径获取想要的电影信息，把它们保存到变量中。
```python
film=selector.xpath('//*[@id="content"]/div/div[1]/ol/li')
```
```python
for div in film:
    title = div.xpath('div/div[2]/div[1]/a/span[1]/text()')[0]
    describe = div.xpath('div/div[2]/div[2]/p[1]/text()') #这里我爬取了年份、国家、类型这三个参数，忽略了导演等参数
    rating = div.xpath('div/div[2]/div[2]/div/span[2]/text()')[0]
    comments_nums = div.xpath('div/div[2]/div[2]/div/span[4]/text()')[0]
    comments = div.xpath('div/div[2]/div[2]/p[2]/span/text()')[0]
```

下面看下获取到的电影信息：
```python
>>> title
'怦然心动'
```
```python
>>> describe[0]
'\n                            导演: 罗伯·莱纳 Rob Reiner\xa0\xa0\xa0主演: 玛德琳·卡罗尔 Madeline Carroll / 卡...'
>>> describe[0].lstrip()
'导演: 罗伯·莱纳 Rob Reiner\xa0\xa0\xa0主演: 玛德琳·卡罗尔 Madeline Carroll / 卡...'
>>> describe[0].lstrip().split('\xa0\xa0\xa0')
['导演: 罗伯·莱纳 Rob Reiner', '主演: 玛德琳·卡罗尔 Madeline Carroll / 卡...']
```
```python
>>> describe[1]
'\n                            2010\xa0/\xa0美国\xa0/\xa0剧情 喜剧 爱情\n                        '
>>> describe[1].lstrip() #lstrip = left strip =去除（字符串）左边的
'2010\xa0/\xa0美国\xa0/\xa0剧情 喜剧 爱情\n                        '
>>> describe[1].lstrip().rstrip() #rstrip = right strip =去除（字符串）右边的
'2010\xa0/\xa0美国\xa0/\xa0剧情 喜剧 爱情'
>>> describe[1].lstrip().rstrip().split('\xa0/\xa0')
['2010', '美国', '剧情 喜剧 爱情']
```
```python
>>> rating
'8.9'
```
```python
>>> comments_nums
'691709人评价'
>>> comments_nums[:-3]
'691709'
```
```python
>>> comments
'真正的幸福是来自内心深处。'
```

-------------------

## 完整实现
```python
import requests
from lxml import etree
import csv
```
```python
top250_url = 'https://movie.douban.com/top250?start={}&filter='
movie_name = '名称'
movie_year = '年份'
movie_country = '国家'
movie_type = '类型'
movie_director = '导演'
movie_assess = '评价人数'
movie_score = '评分'
movie_num = 0
```
```python
with open('top250_movie.csv','w',newline = '',encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([movie_num,movie_name,movie_year,movie_country,movie_type,movie_director,movie_assess,movie_score])
    for lists in range(10):
        movie_content = requests.get(top250_url.format(lists*25)).text
        selector = etree.HTML(movie_content)
        all_list = selector.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for item in all_list:
            movie_name = item.xpath('div/div[2]/div[1]/a/span[1]/text()')[0]
            movie_assess = item.xpath('div/div[2]/div[2]/div/span[4]/text()')[0][:-3]
            movie_score = item.xpath('div/div[2]/div[2]/div/span[2]/text()')[0]
            movie_num += 1
            # 下面将电影的介绍信息进行整理
            movie_intro = item.xpath('div/div[2]/div[2]/p[1]/text()')
            movie_actor_infos = movie_intro[0].lstrip().split('\xa0\xa0\xa0')
            movie_other_infos = movie_intro[1].lstrip().rstrip().split('\xa0/\xa0')
            # 下面是导演信息
            movie_director = movie_actor_infos[0][3:]
            # 下面是电影上映的年份
            movie_year = movie_other_infos[0]
            # 下面是电影的国家
            movie_country = movie_other_infos[1]
            # 下面是电影的类型
            movie_type = movie_other_infos[2]
            
            writer.writerow([movie_num,movie_name,movie_year,movie_country,movie_type,movie_director,movie_assess,movie_score])
```

-------------------

## 结果
```python
import pandas as pd
import csv
```
```python
df = pd.read_csv("top250_movie.csv",encoding = 'utf-8')
df
```
```python
>>> df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 250 entries, 0 to 249
Data columns (total 8 columns):
0       250 non-null int64
名称      250 non-null object
年份      250 non-null object
国家      250 non-null object
类型      250 non-null object
导演      250 non-null object
评价人数    250 non-null int64
评分      250 non-null float64
dtypes: float64(1), int64(2), object(5)
memory usage: 15.7+ KB
```

-------------------

## 遇到的问题
- csv文件产生空行的问题
- Excel打开csv出现乱码怎么解决

-------------------

## 参考
- [使用python抓取豆瓣top250电影数据进行分析](https://www.jianshu.com/p/720b193a5c2b)  
- [Python爬虫一：抓取豆瓣电影Top250](https://blog.csdn.net/xing851483876/article/details/80578998)

-------------------

**详细分析见个人博客：[豆瓣电影TOP250抓取](https://blog.csdn.net/dta0502/article/details/81811931)**
