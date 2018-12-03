#! scrapy runspider doviz.py -o doviz.json

import scrapy

# AJAXCRAWL_ENABLED = True

class BlogSpider(scrapy.Spider):
    name = 'prix'
    start_urls = [
        'https://euro.tlkur.com/refresh/header/viewHeader.php?_=1543361773220',
        # 'https://www.kuveytturk.com.tr'
    ]
    
    def parse(self, response):
        name = response.text.split(":")[3]
        # name = response.css('div.owl-carousel tr:nth-child(2) td:last-child em ::text').extract_first()
        link = 'https://www.kuveytturk.com.tr'
        request = scrapy.Request(url=link, callback = self.parse_check)
        request.meta['name'] = name
        yield request

    def parse_check(self, response):
        name = response.meta['name']
        prixkuveyt = response.css('div.owl-carousel tr:nth-child(2) td:last-child em ::text').extract_first()
        return {"prixdoviz":name, "prixkuveyt": prixkuveyt}

