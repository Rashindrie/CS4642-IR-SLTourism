import scrapy
from scrapy.loader import ItemLoader
from soYAMU.items import YamuItem
import json

class YamuSpider(scrapy.Spider):
    name = "yamu_spider"

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

        def get_facilities():
            facilities = []
            extract_facilities = response.xpath('//div[@class="col-md-12 text-center icon-row"]//div[@class="label-yamu"]/div[@class="inner"]/text()').extract()

            for f in extract_facilities:
                facilities.append(f.strip())
            return facilities

        item = ItemLoader(item=YamuItem(), response=response)
        item.add_xpath(field_name='name', xpath='//div[@class="place-title-box"]/h2/text()')
        item.add_xpath(field_name='description', xpath='//p[@class="excerpt"]/text()')
        item.add_xpath(field_name='cuisine', xpath='//a[contains(@href,"/cuisine/")]/text()')
        item.add_xpath(field_name='price_range', xpath='//a[contains(text(),"Rs.")]/text()')
        item.add_xpath(field_name='dish_types', xpath='//a[contains(@href,"/dishtype/")]/text()')
        item.add_value(field_name='overall_rating',
                             value=response.xpath('//a[contains(@href,"/rating/rating")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/rating")]/@href').extract_first() is not None else 'N/A')
        item.add_value(field_name='quality_rating',
                             value=response.xpath('//a[contains(@href,"/rating/quality")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/quality")]/@href').extract_first() is not None else 'N/A')
        item.add_value(field_name='service_rating',
                             value=response.xpath('//a[contains(@href,"/rating/service")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/service")]/@href').extract_first() is not None else 'N/A')
        item.add_value(field_name='ambiance_rating',
                             value=response.xpath('//a[contains(@href,"/rating/ambiance")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/ambiance")]/@href').extract_first() is not None else 'N/A')
        item.add_xpath(field_name='address', xpath='//p[@class="addressLine"]/text()')
        item.add_value(field_name='contact', value=json.loads(response.xpath('//script[contains(text(),"servesCuisine")]/text()').extract_first())['telephone'] if 'telephone' in json.loads(response.xpath('//script[contains(text(),"servesCuisine")]/text()').extract_first()) else 'N/A')
        item.add_value(field_name='facilities', value=get_facilities())
        item.add_value(field_name='category', value=json.loads(response.xpath('//script[contains(text(),"itemListElement")]/text()').extract_first())['itemListElement'][0]['item']['name'].rsplit(' ', 1)[0])
        item.add_value(field_name='url', value=response.request.url)
        item.add_value(field_name='opening_hours', value=json.loads(response.xpath('//script[contains(text(),"servesCuisine")]/text()').extract_first())['openingHours'])
        item.add_value(field_name='same_as', value=json.loads(response.xpath('//script[contains(text(),"servesCuisine")]/text()').extract_first())['sameAs'])

        yield item.load_item()
