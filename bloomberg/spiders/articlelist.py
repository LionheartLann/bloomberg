# -*- coding: utf-8 -*-
import scrapy
import re
from bloomberg.items import BloombergItem


class ArticlelistSpider(scrapy.Spider):
    name = "articlelist"
    #allowed_domains = ["http://content.cdn.bb.bbwc.cn"]
    start_urls = ['http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/iphone6/tag/cat_18/articlelist/']

    def parse(self, response):
        r_text = r'http://content.cdn.bb.bbwc.cn/.+?\.html'
        regex = re.compile(r_text)
        result = regex.findall(response.text)
        try:
            for url in result:
                self.logger.info("Parsing:%s", url)
                yield scrapy.Request(url=url, callback=self.parse_article)
        except Exception as e:
            self.logger.info("ERROR:%s",e)

    def parse_article(self, response):
        #if response.status == 200:
        try:
            wrapper = response.xpath('//div[@class="wrapper"]')
            title = wrapper.xpath('//title/text()').extract() 
            time = wrapper.xpath('//p[@class="time"]/text()').extract()
            r_text = r'articles/\d+'
            id_regex = re.compile(r_text)
            article_id = id_regex.search(response.url).group(0)
            aid = article_id.replace('articles/','')

            item = BloombergItem()
            item['article_id'] = aid
            item['title'] = title
            item['date'] = time
            item['link'] = response.url
            item['content'] = wrapper.extract()

            self.logger.info("Aid:%s", aid)
            self.logger.info("Item:%s",item['title'])
            #return item
            yield item
        except Exception as e:
            self.logger.info("ERROR:%s",e)
    
    def get_article_id(self, response):
        pass
