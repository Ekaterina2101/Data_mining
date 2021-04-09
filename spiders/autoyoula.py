import scrapy
import pymongo



class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = client["youla"]


    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            url = a.attrib.get("href")
            yield response.follow(url, callback=callback, **kwargs)

    def parse(self, response):
        yield from self._get_follow(
            response, "div.TransportMainFilters_brandsList__2tIkv a.blackLink", self.brand_parse
        )

    def brand_parse(self, response):
        yield from self._get_follow(
            response, "div.Paginator_block__2XAPy a.Paginator_button__u1e7D", self.brand_parse
        )
        yield from self._get_follow(
            response,
            "article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu",
            self.car_parse,
        )

    def car_parse(self, response):
        data = {
            "url": response.url,
            "title": response.css("div.AdvertCard_advertTitle__1S1Ak::text").extract_first(),
            "price": float(
                response.css("div.AdvertCard_price__3dDCr::text")
                .extract_first()
                .replace("\u2009", "")
            ),
            "photos": response.css("figure.PhotoGallery_photo__36e_r img"),
            "characteristics": {'Год выпуска': response.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX.AdvertSpecs_data__xK2Qx::text").extract_first(),
                                'Пробег': response.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcXAdvertSpecs_data__xK2Qx::text").extract_first()},
            "descriptions": response.css(".AdvertCard_descriptionInner__KnuRi::text").extract_first(),

        }
        return self.save(data)


    def save(self, data):
        collection = self.db["autoyoula"]
        collection.insert_one(data)