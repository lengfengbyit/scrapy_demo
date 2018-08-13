# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    serial_number = scrapy.Field() # 序号
    movie_name = scrapy.Field()    # 电影名称
    introduce = scrapy.Field()     # 简介
    star = scrapy.Field()          # 星级
    evaluate = scrapy.Field()      # 评价
    describe = scrapy.Field()      # 描述

class DoubanBookItem(scrapy.Item):
    book_name = scrapy.Field()     # 书名
    price = scrapy.Field()         # 价格
    subtitle = scrapy.Field()      # 副标题
    author = scrapy.Field()        # 作者
    category = scrapy.Field()      # 分类
    average = scrapy.Field()       # 评分
    evaluate = scrapy.Field()      # 评价
    desc = scrapy.Field()          # 描述
    cover = scrapy.Field()         # 封面