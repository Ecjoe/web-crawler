import sys
from urllib.parse import urlparse

import scrapy

from ..items import IfbItem


class IfbspiderSpider(scrapy.Spider):
    name = 'ifb'
    # allowed_domains = ['ifb.com']
    capacity = int(input("Enter capacity of washing machine: "))
    p= 1
    url = 'https://www.ifbappliances.com/products/laundry/washing-machine/top-loader?washing_capacity=' + str(capacity) + '&p=' + str(p)
    start_urls = [
        url
    ]

    def parse(self, response):
        product_links = response.css(".product-item-link::attr(href)").extract()
        if product_links is None:
            sys.exit(0)
        
        for _product in product_links:
            yield scrapy.Request(_product, callback=self.parse_product_page)

        next_page = 'https://www.ifbappliances.com/products/laundry/washing-machine/top-loader?washing_capacity=' + str(IfbspiderSpider.capacity) + '&p=' +  str(IfbspiderSpider.p)
        
        if IfbspiderSpider.p<=3:
            print(f"nextpage: {next_page}")
            IfbspiderSpider.p+=1
            yield response.follow(next_page, self.parse)

    def parse_product_page(self, response):
        items = IfbItem()

        product_link=urlparse(response.url)._replace(fragment="").geturl()
        
        product_name = response.css(".base::text").extract()
        product_price= response.css(".exc-span+ .exchange-price .admin__field-label::text").extract()
        key_features = response.css(".key::text").extract()
        value_features = response.css("#additional .value::text").extract()

        features=dict(zip(key_features, value_features))        

        items['product_name']=product_name
        items['product_price']=product_price
        items['features'] = features
        items['product_link']=product_link

        yield items
