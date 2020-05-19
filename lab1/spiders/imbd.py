# -*- coding: utf-8 -*-
import scrapy
from imdb.items import ImdbItem


class ImbdSpider(scrapy.Spider):
    name = 'imbd'
    start_urls = ['http://www.imdb.com/title/tt4630562/']  # The Fate of the Furious

    def parse(self, response):
        for tr in response.xpath("//tr[@class='odd'] | //tr[@class='even']"):
            imdb_item = ImdbItem()
            imdb_item['actor'] = tr.xpath("./td[@itemprop='actor']//span/text()").extract()
            imdb_item['character'] = tr.xpath("./td[@class='character']/div/a/text()").extract()
            actor_url = tr.xpath("./td[@itemprop='actor']/a/@href").extract_first()
            request = scrapy.Request(response.urljoin(actor_url), callback=self.parse_actor_page)
            request.meta['imdb_item'] = imdb_item
            yield request

    def parse_actor_page(self, response):
        imdb_item = response.meta['imdb_item']
        imdb_item['actor_films'] = []
        for film in response.xpath("//div[contains(@class, 'filmo-row')]/b/a/text()").extract():
            imdb_item['actor_films'].append(film)
        yield imdb_item
