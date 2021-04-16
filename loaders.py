import re
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose

def flat_text(items):
    return "\n".join(items)


def avito_user_url(user_id):
    return urljoin("https://avito.ru/", user_id)

class AvitoLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_out = flat_text
    address_out = TakeFirst()
    parameters_out = TakeFirst()
    author_in = MapCompose(avito_user_url)
    author_out = TakeFirst()