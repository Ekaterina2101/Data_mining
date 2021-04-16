
AVITO_PAGE_XPATH = {
    "pagination": '//div[@data-market="pagination-button"]//span[@data-market="pagination-button/next"]/@href',
    "flat": '//div[contains(@data-qa, "vacancy-serp__vacancy")]//'
    'a[@data-qa="vacancy-serp__vacancy-title"]/@href',
}

AVITO_FLAT_XPATH = {
    "url": '//a[@itemprop="url"]/@href',
    "title": '//a[@title]/text()',
    "price": '//div[@data-market="item-price"]/span/text()',
    "address": '//span[@class="geo-address-9QndR text-text-1PdBw text-size-s-1PUdo"]/span/text()' + '//div[@class="geo-georeferences-3or5Q text-text-1PdBw text-size-s-1PUdo"]/span/text()',
    "parameters": '//p/text()',
    "author": '//a/@href',
}
