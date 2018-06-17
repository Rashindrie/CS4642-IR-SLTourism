import scrapy
from scrapy.loader import ItemLoader
from swiftSearch.items import YamuItem


class YamuSpider(scrapy.Spider):
    name = "yamu"

    # The URLs to start with
    start_urls = [
        'https://www.yamu.lk/place?page=1'
    ]

    allowed_domains = ["yamu.lk"]

    def parse(self, response):

        links = response.xpath('//a[contains(@href,"/review")]/@href').extract()

        for place in links:
            yield scrapy.Request(place, self.parse_restaurant)

        for i in range(2, 131):
            yield scrapy.Request('https://www.yamu.lk/place?page=%s' % str(i))

    def parse_restaurant(self, response):
        restaurant = ItemLoader(item=YamuItem(), response=response)
        restaurant.add_xpath(field_name='name', xpath='//div[@class="place-title-box"]/h2/text()')
        restaurant.add_xpath(field_name='description', xpath='//p[@class="excerpt"]/text()')
        restaurant.add_xpath(field_name='cuisine', xpath='//a[contains(@href,"/cuisine/")]/text()')
        restaurant.add_xpath(field_name='price_range', xpath='//a[contains(text(),"Rs.")]/text()')
        restaurant.add_xpath(field_name='dish_types', xpath='//a[contains(@href,"/dishtype/")]/text()')
        restaurant.add_value(field_name='overall_rating',
                             value=response.xpath('//a[contains(@href,"/rating/rating")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/rating")]/@href').extract_first() is not None else 'N/A')
        restaurant.add_value(field_name='quality_rating',
                             value=response.xpath('//a[contains(@href,"/rating/quality")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/quality")]/@href').extract_first() is not None else 'N/A')
        restaurant.add_value(field_name='service_rating',
                             value=response.xpath('//a[contains(@href,"/rating/service")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/service")]/@href').extract_first() is not None else 'N/A')
        restaurant.add_value(field_name='ambiance_rating',
                             value=response.xpath('//a[contains(@href,"/rating/ambiance")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/ambiance")]/@href').extract_first() is not None else 'N/A')
        restaurant.add_xpath(field_name='address', xpath='//p[@class="addressLine"]/text()')
        restaurant.add_value(field_name='contact',
                             value=(" ".join((response.xpath('//a[@class="emph"]/text()').extract_first()).split())).split(' ', 1)[1] if response.xpath('//a[@class="emph"]/text()').extract_first() is not None else 'N/A')
        yield restaurant.load_item()
