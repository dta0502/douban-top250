# Pandas DataFrame数据写入文件和数据库

Pandas是Python下一个开源数据分析的库，它提供的数据结构DataFrame极大的简化了数据分析过程中一些繁琐操作,DataFrame是一张多维的表，大家可以把它想象成一张Excel表单或者Sql表。之前这篇文章已经介绍了从各种数据源将原始数据载入到dataframe中，这篇文件介绍怎么将处理好的dataframe中的数据写入到文件和数据库中。

## 创建DataFrame对象
首先我们通过二维ndarray创建一个简单的DataFrame：
```python
import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(3, 4))
df
```
```python
    0   1   2   3
0   1.0492286140081302  -0.7922606407983686 0.020418054868760225    -1.6649819403741724
1   0.3485250628814134  -2.117606544377745  1.466822878437205   -0.9249205656243358
2   1.3073567907490637  -0.7350348086218035 0.2856083175408006  -0.9053483976251634
```

## 1. Dataframe写入到csv文件
```python
df.to_csv('D:\\a.csv', sep=',', header=True, index=True)
```
第一个参数是说把dataframe写入到D盘下的a.csv文件中，参数sep表示字段之间用’,’分隔，header表示是否需要头部，index表示是否需要行号。

## 2. Dataframe写入到json文件
```python
df.to_json('D:\\a.json')
```
把dataframe写入到D盘下的a.json文件中,文件的内容为
```python
{"0":{"0":1.049228614,"1":0.3485250629,"2":1.3073567907},"1":{"0":-0.7922606408,"1":-2.1176065444,"2":-0.7350348086},"2":{"0":0.0204180549,"1":1.4668228784,"2":0.2856083175},"3":{"0":-1.6649819404,"1":-0.9249205656,"2":-0.9053483976}}
```
## 3.Dataframe写入到html文件
```python
df.to_html('D:\\a.html')
```
把dataframe写入到D盘下的a.html文件中,文件的内容为
```html
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-0.677090</td>
      <td>0.990133</td>
      <td>-1.775863</td>
      <td>0.654884</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-1.825927</td>
      <td>-2.262985</td>
      <td>-0.849212</td>
      <td>-0.154182</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.252012</td>
      <td>0.464503</td>
      <td>0.771977</td>
      <td>0.329159</td>
    </tr>
  </tbody>
</table>
```
在浏览器中打开a.html的样式为


## 4.Dataframe写入到剪贴板中
这个是我认为最为贴心的功能, 一行代码可以将dataframe的内容导入到剪切板中，然后可以复制到任意地方
```python
df.to_clipboard()
```

## 5.Dataframe写入到数据库中
```python
df.to_sql('tableName', con=dbcon, flavor='mysql')
```
第一个参数是要写入表的名字，第二参数是sqlarchmy的数据库链接对象，第三个参数表示数据库的类型，“mysql”表示数据库的类型为mysql。