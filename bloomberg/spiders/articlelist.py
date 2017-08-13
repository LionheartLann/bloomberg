# -*- coding: utf-8 -*-
import scrapy
import re


class ArticlelistSpider(scrapy.Spider):
    name = "articlelist"
    allowed_domains = ["http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/iphone6/tag/cat_18/articlelist"]
    start_urls = ['http://http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/iphone6/tag/cat_18/articlelist/']

    def parse(self, response):
        r_text = r'http://content.cdn.bb.bbwc.cn/.+?\.html'
        regex = re.compile(r_text)
        result = regex.findall(response.text)
        try:
            for url in result:
                print("=====================Parse======================", url)
                yield scrapy.Request(url=url, callback=self.parse_article)
        except Exception as e:
            print(e)

    def parse_article(self, response):
        #if response.status == 200:
        try:
            wrapper = response.xpath('//div[@class="wrapper"]')
            title = wrapper.xpath('//title/text()').extract() 
            time = wrapper.xpath('//p[@class="time"]/text()').extract()
            print("=====================ParseArticle======================", title)
        except Exception as e:
            print(e)

