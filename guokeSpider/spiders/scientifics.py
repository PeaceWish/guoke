# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import guokeSpider.items as Item
import re

class ScientificsSpider(CrawlSpider):
    name = "scientific"
    allowed_domains = ["www.guokr.com"]
    start_urls = ['http://www.guokr.com/scientific/all/archive/201612/',
                  'http://www.guokr.com/scientific/all/archive/201611/',
                  'http://www.guokr.com/scientific/all/archive/201610/',]
    rules = (
        Rule(LinkExtractor(allow=(r'http:\/\/www\.guokr\.com\/article\/(\d+)\/')), callback='parse_article_detail',),
    )

    def parse_start_url(self, response):
        next_page = response.xpath('//ul[@class="gpages"]/li/a').re(r'href="(.*)">下一页')
        if next_page :
            next_page = response.urljoin(next_page[0])
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_article_detail(self, response):
        articleItem = Item.ScientificItem()
        articleItem['publishDate'] = response.xpath('//div[@class="content-th-info"]/meta/@content').extract()[0].split('T')[0]
        articleItem['label'] = response.xpath('//div[@class="content-th"]/a/text()').extract()[0]
        labels = response.xpath('//div[@class="content-th"]/a/text()').extract()
        articleItem['subLabel'] = labels[1] if (len(labels) == 2) else ""
        articleItem['title'] = response.xpath('//h1[@id="articleTitle"]/text()').extract()[0]
        articleItem['summary'] = response.xpath('//script/text()').re(r'(summary) : "(.*)"')[1].encode('utf-8').decode('unicode_escape')
        articleItem['articleUrl'] = response.xpath('//a[@id="basketBtn"]/@data-url').extract()[0]
        articleItem['articleId'] = re.match(r'.*/(\d+)/', articleItem['articleUrl'])[1]
        yield articleItem
