# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名，不能和项目名相同
    name = 'douban_spider'
    # 允许请求的域名
    allowed_domains = ['movie.douban.com']
    # 请求入口url
    start_urls = ['https://movie.douban.com/top250']

    base_url = 'https://movie.douban.com/top250';

    def parse(self, response):

        movie_list = response.xpath(
            "//div[@class='article']//ol[@class='grid_view']/li")

        hd_xpath = ".//div[@class='item']/div[@class='info']/div[@class='hd']"
        bd_xpath = ".//div[@class='item']/div[@class='info']/div[@class='bd']"

        for item in movie_list:
            douban_item = DoubanItem()

            douban_item['serial_number'] = item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = item.xpath(
                "%s/a/span[1]/text()" % hd_xpath).extract_first()

            intro = item.xpath("%s/p[1]/text()" % bd_xpath).extract()
            douban_item['introduce'] = "".join(intro[-1].split())
            douban_item['star'] = item.xpath(
                "%s/div[@class='star']/span[@class='rating_num']/text()" % bd_xpath).extract_first()
            douban_item['evaluate'] = item.xpath("%s/div[@class='star']/span[4]/text()" % bd_xpath).extract_first()
            douban_item['describe'] = item.xpath(
                "%s/p[@class='quote']/span[@class='inq']/text()" % bd_xpath).extract_first()

            # 将数据yield到pipeline里，可以进行数据的清洗，存储
            yield douban_item

        next_link = response.xpath("//span[@class='next']/link/@href").extract_first()

        if next_link:
            next_link = '%s%s' % (self.base_url, next_link)
            yield scrapy.Request(next_link, callback=self.parse)


