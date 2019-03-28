# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from New.items import NewItem, NewItemLoader


class TechSpider(CrawlSpider):
    name = 'tech'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow='http://tech.china.com/article/.*\.html', restrict_xpaths='//div[@id="left_side"]'),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(text(),"下一页")]'))
    )

    def parse_item(self, response):
        item_loader = NewItemLoader(NewItem(), response)
        item_loader.add_xpath('title', '//div[@id="chan_newsBlk"]/h1/text()')
        item_loader.add_xpath('time', '//div[@id="chan_newsInfo"]/text()', re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
        item_loader.add_value('url', response.url)
        item_loader.add_xpath('text', '//div[@id="chan_newsDetail"]//text()')
        item_loader.add_xpath('source', '//div[@id="chan_newsInfo"]/text()', re='来源：(.*)')

        new_item = item_loader.load_item()
        yield new_item



