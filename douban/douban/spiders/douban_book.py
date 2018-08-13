# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanBookItem

class DoubanBookSpider(scrapy.Spider):
    name = 'douban_book'
    allowed_domains = ['read.douban.com']
    start_urls = ['http://read.douban.com/kind/100']

    def parse(self, response):
        """ 创建解析规则 """

        book_item = DoubanBookItem()

        ul_xpath = "//div[@class='bd']/ul/li"
        info_xpath = "./div[@class='info']"

        book_list = response.xpath(ul_xpath)
        for item in book_list:

            book_item['book_name'] = item.xpath("%s/div[@class='title']/a/text()" % info_xpath).extract_first()
            book_item['subtitle'] = item.xpath(
                "%s/div[@class='title']/p/text()" % info_xpath).extract_first()
            book_item['price'] = item.xpath(
                "%s//div[@class='action-buttons']/span/text()" % info_xpath).extract_first()
            book_item['author'] = item.xpath(
                "%s//a[@class='author-item']/text()" % info_xpath).extract_first()
            book_item['category'] = item.xpath(
                "%s//span[@class='category']/span[@class='labeled-text']/span/text()" % info_xpath).extract_first()
            book_item['average'] = item.xpath(
                "%s//span[@class='rating-average']/text()" % info_xpath).extract_first()
            book_item['evaluate'] = item.xpath(
                "%s//span[@class='rating-amount']/a/span/text()" % info_xpath).extract_first()
            book_item['desc'] = item.xpath(
                "%s/div[@class='article-desc-brief']/text()" % info_xpath).extract_first()
            book_item['cover'] = item.xpath(
                "./div[1]/a/img/@src").extract_first()
            yield book_item

        next_link = response.xpath(".//li[@class='next']/a/@href").extract_first()
        if next_link:
            next_link = "%s%s" % (self.start_urls[0], next_link)
            # yield scrapy.Request(next_link, callback=self.parse)
