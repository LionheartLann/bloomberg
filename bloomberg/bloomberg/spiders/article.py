# -*- coding: utf-8 -*-
import scrapy


class ArticleSpider(scrapy.Spider):
    name = "article"
    allowed_domains = ["http://content.cdn.bb.bbwc.cn/v5/app1/issue_1292/articles/10076824/show-1-6-1292-1718-10076824-1_1502265373.html"]
    start_urls = ['http://http://content.cdn.bb.bbwc.cn/v5/app1/issue_1292/articles/10076824/show-1-6-1292-1718-10076824-1_1502265373.html/']

    def parse(self, response):
        #if response.status == 200:
        #try:
        wrapper = response.xpath('//div[@class="wrapper"]')
        title = wrapper.xpath('//title/text()').extract() 
        time = wrapper.xpath('//p[@class="time"]/text()').extract()
        #except:
        pass
