# coding=utf-8
import configparser

import pymongo
import redis
import requests
from jieba.analyse import extract_tags
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Referer': 'http://www.people.com.cn/'
}


class PeoplePaser:
    links = []

    # driver = webdriver.PhantomJS()

    def __init__(self, url):
        self.url = url

    def switch_methods(self, argument):
        method_name = getattr(self, argument, lambda: "NoPaser")
        return method_name(self.url)

    # 获取主页上所有新闻相关url
    def home_paser(self, url):
        r = requests.get(url, headers=headers)
        html = r.text
        html.encode('utf-8')
        selector = etree.HTML(html)
        # 暴力获取所有新闻相关url 在各个section模块中
        self.links.append(selector.xpath(
            '//section[position()>1 and position()<12]//a/@href'
        ))

        db = self.get_redisDb()
        self.redis_insert(db, self.links)
        return "success"

    # 获取分类或专题上所有相关url
    def any_url_paser(self, url):
        r = requests.get(url, headers=headers)
        html = r.text
        html.encode('utf-8')
        selector = etree.HTML(html)
        self.links.append(selector.xpath(
            '//a/@href'
        ))
        parent = url.split('/')[0]
        self.links = filter(lambda x: '/n1' not in x and '/GB' not in x and 'index' not in x, self.links)
        for i in range(0, len(self.links)):
            if self.links[i].startswith('/n1') or self.links[i].startswith('index'):
                self.links[i] = parent + '/' + self.links[i]
        db = self.get_redisDb()
        self.redis_insert(db, self.links)
        return "success"

    # 获取具体某个新闻的正文
    def body_paser(self, url):
        r = requests.get(url, headers=headers)
        r.encoding = 'gbk'
        html = r.text
        # html.encode('utf-8')
        selector = etree.HTML(html)
        title = "".join(selector.xpath('//h1/text()'))
        text = "".join(selector.xpath(
            '//*[@id="rwb_zw"]/p/text()'
        ))
        # print(title, text)
        keywords = extract_tags(text, topK=5)
        db = self.get_mogodb()
        self.mogo_insert(db, title, keywords, text)
        return "success"

    def get_mogodb(self):
        cf = configparser.ConfigParser()
        cf.read('util/config.ini')
        db_host = cf.get('MongoDB', 'host')
        db_port = cf.get('MongoDB', 'port')
        # print(db_host,db_port)
        client = pymongo.MongoClient(db_host, int(db_port))
        db = client['people']
        return db

    def mogo_insert(self, db, title, keywords, text):
        coll = db['text']
        info = {'Title': title, 'Keywords': keywords, "text": text}
        coll.insert(info)

    def get_redisDb(self):
        cf = configparser.ConfigParser()
        cf.read('util/config.ini')
        db_host = cf.get('Redis', 'host')
        db_port = cf.get('Redis', 'port')
        r = redis.Redis(db_host, db_port)
        return r

    def redis_insert(self, db, datas):
        for item in datas:
            db.lpush('url', item)
        print(db.llen('url'))

        # def __del__(self):
        #     self.driver.close()
