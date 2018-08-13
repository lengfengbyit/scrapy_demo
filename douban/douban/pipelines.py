# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
from douban.settings import MYSQL_CONFIG
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request

class DoubanPipeline(object):

    def open_spider(self, spider):
        """ 链接数据库 """
        self.conn = pymysql.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            passwd=MYSQL_CONFIG['passwd'],
            db=MYSQL_CONFIG['db'],
            charset=MYSQL_CONFIG['charset']
        )
        # 获取游标
        self.cursor = self.conn.cursor()

        self.piplines = {
            'douban_spider': self.douban_movie,
            'douban_book': self.douban_book
        }

    def close_spider(self, spider):
        # 关闭数据库连接
        self.conn.close()

    def process_item(self, item, spider):
        """ 数据存储 """

        if spider.name in self.piplines:
            return self.piplines[spider.name](item)

    def douban_movie(self, item):
        """ 豆瓣电影数据存储函数 """

        sql = 'insert into douban_movie(serial_number, movie_name, introduce, star, evaluate, `describe`) values(%s, "%s", "%s", %s, "%s", "%s")'
        data = (
            item['serial_number'],
            item['movie_name'],
            item['introduce'],
            item['star'],
            item['evaluate'],
            item['describe']
        )

        self.cursor.execute(sql % data)
        self.conn.commit()

        return item

    def douban_book(self, item):
        """ 豆瓣书籍数据存储函数 """

        sql = 'insert into douban_book(book_name, price, subtitle, author, category, `average`, evaluate, `desc`, cover) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'

        data = (
            item['book_name'],
            item['price'],
            item['subtitle'],
            item['author'],
            item['category'],
            item['average'],
            item['evaluate'],
            item['desc'],
            item['cover']
        )

        self.cursor.execute(sql % data)
        self.conn.commit()

        return item


class SaveImgPipeline(ImagesPipeline):
    """ 保存图片 """

    def get_media_requests(self, item, info):
        """ 返回有图片url构造的request对象 """

        if 'cover' in item:
            yield Request(item['cover'])

    def item_completed(self, results, item, info):
        # results会返回一个列表，第一个值是一个元组，里面第一个值是一个bool值
        # 代表数据是否现在成功
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('下载失败')
        print(results)
        item['cover'] = image_path[0]
        return item
