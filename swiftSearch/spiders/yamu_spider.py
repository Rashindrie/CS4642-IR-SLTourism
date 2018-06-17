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
        restaurant.add_xpath(field_name='contact', xpath='//a[@class="emph"]/text()')
        restaurant.add_xpath(field_name='address', xpath='//p[@class="addressLine"]/text()')
        restaurant.add_xpath(field_name='description', xpath='//p[@class="excerpt"]/text()')
        restaurant.add_xpath(field_name='cuisine', xpath='//a[contains(@href,"/cuisine/")]/text()')
        restaurant.add_xpath(field_name='price_range', xpath='//a[contains(text(),"Rs.")]/text()')
        restaurant.add_xpath(field_name='dish_types', xpath='//a[contains(@href,"/dishtype/")]/text()')
        restaurant.add_value('overall_rating',
                             response.xpath('//a[contains(@href,"/rating/rating")]/@href')[0].extract().split('-')[-1])
        restaurant.add_value('quality_rating',
                             response.xpath('//a[contains(@href,"/rating/quality")]/@href')[0].extract().split('-')[-1])
        restaurant.add_value('service_rating',
                             response.xpath('//a[contains(@href,"/rating/service")]/@href')[0].extract().split('-')[-1])
        restaurant.add_value('ambiance_rating',
                             response.xpath('//a[contains(@href,"/rating/ambiance")]/@href')[0].extract().split('-')[
                                 -1])

        yield restaurant.load_item()
