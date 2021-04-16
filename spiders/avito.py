import scrapy

from gb_parse.loaders import AvitoLoader
from gb_parse.spiders.xpaths import AVITO_PAGE_XPATH, AVITO_FLAT_XPATH


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ru"]
    start_urls = [
        "https://www.avito.ru/krasnodar/kvartiry/prodam"
    ]

    def _get_follow_xpath(self, response, xpath, callback):
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback)

    def parse(self, response):
        callbacks = {"pagination": self.parse, "flat": self.flat_parse}

        for key, xpath in AVITO_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])

    def flat_parse(self, response):
        loader = AvitoLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in AVITO_FLAT_XPATH.items():
            loader.add_xpath(key, xpath)

        yield loader.load_item()