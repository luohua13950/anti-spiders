# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.request import request_fingerprint


class DyttSpider(CrawlSpider):
    name = 'dytt'
    allowed_domains = ['www.dytt8.net']
    #start_urls = ['http://www.dytt8.net/']
    start_urls = ['https://www.dytt8.net/html/gndy/china/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.dytt8.net/html/gndy/china/list_.*?.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        print(response)
        print(response.text)
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        scrapy.Request()
        return item
