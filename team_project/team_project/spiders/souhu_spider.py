# _*_ coding: utf-8 _*_
"""实现定量爬取搜狐网站新闻
Author:   Fuyuxia
Version:  V 0.2
"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
from pyquery import PyQuery as pq
import pymongo
from bs4 import BeautifulSoup
import pandas as pd

'新闻url列表'
url_list = []
'新闻url总数'
num = 0
'新闻标题数量'
name_n = 0

MONGO_URL = 'localhost'
'新闻标题列表'
title_list = []
'阅读量列表'
reading_list = []
'存储阅读量切割后的字符'
list_cut = []
list_num =[]
'标题与阅读量'
rank = {}

"打开搜狐新闻网站后，获取所有板块下的url,在新窗口中爬取其中的标题和正文信息以及阅读量，并实现存储"

'存储到mongodb'
def save_mongo(article):
    MONGO_DB = 'souhu_news'
    MONGO_COLLECTION = 'news'
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    try:
        if db[MONGO_COLLECTION].insert_one(article):
            print("存储成功")
    except Exception:
        print("存储失败")



'根据阅读量排名输出新闻标题'
def reading_rank(max):
    global rank
    global reading_list
    global title_list
    global list_cut
    for i in range(max):
        lenth = len(reading_list[i])
        list_cut.append(reading_list[i][4:lenth-1])

    for i in range(max):
        lenth = len(list_cut[i])
        n = lenth - 1
        if (list_cut[i][n] == "万"):
            count = list_cut[i][0:n]
            list_cut[i] = float(count) * 10000
        else:
            list_cut[i] = float(list_cut[i])

    for i in range(max):
        rank[title_list[i]] = list_cut[i]

    rank = dict(rank)
    dataframe = pd.DataFrame({'标题': title_list, '阅读量': list_cut})
    print(dataframe)
    '排序'
    rank = sorted(rank.items(), key=lambda rank: rank[1], reverse=True)
    print("根据阅读量排序后为")
    "创建排名索引"
    rank_list = []
    for i in range(1, len(reading_list)+1):
        rank_list.append(i)

    rank = pd.DataFrame(rank, index=rank_list, columns=['标题', '阅读量'])
    rank.to_csv("data.csv")
    print(rank)


class spider_sh():

    def __init__(self):
        self.url = 'https://news.sohu.com/'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)

    "打开网页"
    def open(self):
        self.browser.get(self.url)

    "获取新的url"

    def get_new_url(self):
        print('开始获取新闻url')
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        newslist = soup.find_all(class_='list16')
        global num
        global url_list
        for url in newslist:
            for k in url.find_all('a'):
                new_url = k['href']
                num = num+1
                url_list.append(new_url)
        print('完成获取url')

    "关闭网页"

    def close(self):
        self.browser.close()

    "开始爬取"

    def start(self):
        print('开始爬取')
        self.open()
        self.get_new_url()

"打开新网页来获取新页面"

class new_window():

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)

    " 获取标题和正文和阅读量"

    def get_title_article(self):
        html = self.browser.page_source
        doc = pq(html)
        global title_list
        global reading_list
        title_list.append(doc('.text-title > h1').text())
        reading_list.append(doc('.read-wrap .read-num').text())
        article = {
                'title': doc('.article-page .text .text-title > h1').text(),
                'article': doc('.article ').text(),
                'reading': doc('.read-wrap .read-num').text()
        }
        save_mongo(article)

    "关闭网页"

    def close(self):
        self.browser.close()

    "打开网页，开始爬取"

    def open(self):
        global url_list
        '测试，只获取前十个并排名(实际数量为num)'
        #test = 10
        global num
        print('开始爬取文章信息')
        for n in range(0, num):
            url = url_list[n]
            self.browser.get(url)
            self.get_title_article()
            self.close
        print('文章信息爬取完毕')
        reading_rank(num)



if __name__ == '__main__':
    souhu = spider_sh()
    souhu.start()
    souhu2 = new_window()
    souhu2.open()