import scrapy
from scrapy.loader import ItemLoader
from soYAMU.items import YamuItem
import json

class YamuPageSpider(scrapy.Spider):
    name = "yamu_pages"

    # The URLs to start with
    start_urls = [
        'https://www.yamu.lk/place?page=1'
    ]

    allowed_domains = ["yamu.lk"]

    def parse(self, response):

        links = response.xpath('//a[contains(@href,"/review")]/@href').extract()

        for place in links:
            yield scrapy.Request(place, self.parse_item)

        for i in range(2, 131):
            yield scrapy.Request('https://www.yamu.lk/place?page=%s' % str(i))

    def parse_item(self, response):
        page = response.url.split("/")[-2]
        filename = 'data/pages/%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
