# -*- coding: utf-8 -*-
import scrapy
import re
from bloomberg.items import BloombergItem


class IncrbyIdSpider(scrapy.Spider):
    name = "incrby_id"
    #allowed_domains = ["content.cdn.bb.bbwc.cn/v5/app1/issue_1216/articles/10077969/show-1-6-1216-28-10070000-1_1470459942.html"]
    start_urls = ['http://content.cdn.bb.bbwc.cn/v5/app1/issue_1216/articles/10077969/show-1-6-1216-28-10070000-1_1470459942.html']

    def parse(self, response):
        r_text = r'show-1-6-1216-28-\d*'
        regex = re.compile(r_text)
        article_id = regex.search(response.url).group(0)[-8:]
        self.logger.info("article_id:%s", article_id)
        for id in range(int(article_id), 10077000):
            new_id = int(id)+1
            url = re.sub(r'show-1-6-1216-28-\d*', 'show-1-6-1216-28-'+str(new_id), response.url)
            self.logger.info("URL:%s",url)
            self.logger.info("id:%s",id)
            yield scrapy.Request(url=url, callback=self.parse_article)

    def parse_article(self, response):
        if response.status == 200:
            try:
                wrapper = response.xpath('//div[@class="wrapper"]')
                title = wrapper.xpath('//title/text()').extract() 
                time = wrapper.xpath('//p[@class="time"]/text()').extract()
                tags = wrapper.xpath('//a[@class="tagBtn"]/text()').extract()
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


                vip_text = r'付费专享文章'
                vip_regex = re.compile(vip_text)
                flag = vip_regex.search(response.text)
                if flag is None:
                    item['vip'] = 0
                elif flag.group(0) == "付费专享文章":
                    item['vip'] = 1

                self.logger.info("Aid:%s", aid)
                self.logger.info("Item:%s",item['title'])
                #return item
                yield item
            except Exception as e:
                self.logger.info("ERROR:%s",e)
        else:
            self.logger.info("============Status============%s",response.status)
