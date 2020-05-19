# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    actor = scrapy.Field()
    character = scrapy.Field()
    actor_films = scrapy.Field()  # extra info about the actor

