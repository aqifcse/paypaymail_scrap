# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urljoin

LUA_SCRIPT = """
function main(splash)
    splash.private_mode_enabled = false
    splash:go(splash.args.url)
    splash:wait(2)
    html = splash:html()
    splash.private_mode_enabled = true
    return html
end
"""

class PaypaySpider(scrapy.Spider):
    name = 'paypay'
    allowed_domains = ['paypaymall.yahoo.co.jp']
    start_urls = ['https://paypaymall.yahoo.co.jp/?sc_e=ytc/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='execute',
                args={
                    'wait': 1,
                    "lua_source":LUA_SCRIPT
                }
            )

    def parse(self, response):
        
        top_rankings = response.xpath('//body/div/main/div[@class = "Partition top_ranking Partition-separate"]/div[@class = "RankingCarousel"]/amp-list/div[@class="i-amphtml-fill-content i-amphtml-replaced-content"]/amp-carousel/div').extract()
        print(top_rankings)
        # for item in items:
        #     brand = item.xpath('.//div[@class="TinyShelfItem_info"]/p[@class="TinyShelfItem_brand"]/text()').extract_first()
        #     name = item.xpath('.//div[@class="TinyShelfItem_info"]/p[@class="TinyShelfItem_name"]/text()').extract_first()
        #     price = item.xpath('.//div[@class="TinyShelfItem_info"]/p[@class="TinyShelfItem_price"]/text()').extract_first()

        #     yield {
        #         "brand": brand,
        #         "name": name,
        #         "price": price,
        #     }
            

