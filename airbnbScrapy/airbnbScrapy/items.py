# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AirbnbItem(scrapy.Item):
    nombreVenue = scrapy.Field()
    city = scrapy.Field()
    coordenadas = scrapy.Field()
    #last_visited = scrapy.Field()
    total_visitas = scrapy.Field()
    #review = scrapy.Field()
    score_prom = scrapy.Field()
    nums_evaluacion = scrapy.Field()
    categoria = scrapy.Field()
    precios = scrapy.Field()
    #neighborhood = scrapy.Field()
