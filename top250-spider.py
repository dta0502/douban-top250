import requests
from lxml import etree
import csv

top250_url = 'https://movie.douban.com/top250?start={}&filter='
movie_name = '名称'
movie_year = '年份'
movie_country = '国家'
movie_type = '类型'
movie_director = '导演'
movie_assess = '评价人数'
movie_score = '评分'
movie_num = 0


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
