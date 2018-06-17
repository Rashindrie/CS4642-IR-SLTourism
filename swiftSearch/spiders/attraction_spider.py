import scrapy
from scrapy.loader import ItemLoader
from swiftSearch.items import YamuItem


class YamuSpider(scrapy.Spider):
    name = "yamu_attraction"

    # The URLs to start with
    start_urls = [
        'https://www.yamu.lk/place/attractions/page=1'
    ]

    allowed_domains = ["yamu.lk"]

    def parse(self, response):

        for href in response.xpath('//a[@class="front-group-item item"]/@href').extract():
            print href
            yield scrapy.Request(href, self.parse_attraction)

        for i in range(1, 10):
            yield scrapy.Request('https://www.yamu.lk/place/attractions?page=%s' % str(i))

    def parse_attraction(self, response):

        def get_facilities():
            facilities = []
            extract_facilities = response.xpath('//div[@class="col-md-12 text-center icon-row"]//div[@class="label-yamu"]/div[@class="inner"]/text()').extract()

            for f in extract_facilities:
                facilities.append(f.strip())
            return facilities

        attraction = ItemLoader(item=YamuItem(), response=response)
        attraction.add_value(field_name='category', value='attraction')
        attraction.add_xpath(field_name='name', xpath='//div[@class="place-title-box"]/h2/text()')
        attraction.add_xpath(field_name='description', xpath='//p[@class="excerpt"]/text()')
        attraction.add_xpath(field_name='cuisine', xpath='//a[contains(@href,"/cuisine/")]/text()')
        attraction.add_xpath(field_name='price_range', xpath='//a[contains(text(),"Rs.")]/text()')
        attraction.add_xpath(field_name='dish_types', xpath='//a[contains(@href,"/dishtype/")]/text()')
        attraction.add_value(field_name='overall_rating',
                             value=response.xpath('//a[contains(@href,"/rating/rating")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/rating")]/@href').extract_first() is not None else 'N/A')
        attraction.add_value(field_name='quality_rating',
                             value=response.xpath('//a[contains(@href,"/rating/quality")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/quality")]/@href').extract_first() is not None else 'N/A')
        attraction.add_value(field_name='service_rating',
                             value=response.xpath('//a[contains(@href,"/rating/service")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/service")]/@href').extract_first() is not None else 'N/A')
        attraction.add_value(field_name='ambiance_rating',
                             value=response.xpath('//a[contains(@href,"/rating/ambiance")]/@href').extract_first().split('-')[-1] if response.xpath('//a[contains(@href,"/rating/ambiance")]/@href').extract_first() is not None else 'N/A')
        attraction.add_xpath(field_name='address', xpath='//p[@class="addressLine"]/text()')
        attraction.add_value(field_name='contact',
                             value=(" ".join((response.xpath('//a[@class="emph"]/text()').extract_first()).split())).split(' ', 1)[1] if response.xpath('//a[@class="emph"]/text()').extract_first() is not None else 'N/A')
        attraction.add_value(field_name='facilities', value=get_facilities())

        yield attraction.load_item()
