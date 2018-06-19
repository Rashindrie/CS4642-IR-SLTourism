# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YamuItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    address = scrapy.Field()
    contact = scrapy.Field()
    description = scrapy.Field()
    cuisine = scrapy.Field()
    price_range = scrapy.Field()
    dish_types = scrapy.Field()
    facilities = scrapy.Field()
    user_rating = scrapy.Field()
    overall_rating = scrapy.Field()
    quality_rating = scrapy.Field()
    service_rating = scrapy.Field()
    ambiance_rating = scrapy.Field()
    opening_hours = scrapy.Field()
    same_as = scrapy.Field()
    similar_places = scrapy.Field()
    nearby_places = scrapy.Field()
