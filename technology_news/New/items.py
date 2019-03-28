# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy import Field
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose



class NewItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def get_text(value):
    return value.strip()


def get_source(value):
    return value.strip()


def get_date_time(value):
    date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return date


class NewItem(scrapy.Item):
    title = Field()
    time = Field(input_processor=MapCompose(get_date_time))
    url = Field()
    text = Field(
        input_processor=MapCompose(get_text),
        output_processor = Join()
    )
    source = Field(input_processor=MapCompose(get_source))



