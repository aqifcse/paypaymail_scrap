# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urljoin

# script = """
# function main(splash)
#     local scroll_delay = 2 # i have tried to vary this number with some success
#     local is_down = splash:jsfunc(
#         "function() { return((window.innerHeight + window.scrollY) >= document.body.offsetHeight);}"
#         )

#     local scroll_to = splash:jsfunc("window.scrollTo")
#     local get_body_height = splash:jsfunc(
#         "function() {return document.body.scrollHeight;}"
#     )
#     assert(splash:go(splash.args.url))

#     while not is_down() do
#         scroll_to(0, get_body_height())
#         splash:wait(scroll_delay)
#     end        
#     return splash:html()
# end
# """

class PaypaySpider(scrapy.Spider):
    name = 'paypay'
    allowed_domains = ['https://paypaymall.yahoo.co.jp']
    start_urls = ['https://paypaymall.yahoo.co.jp/?sc_e=ytc/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        splash_args = {
            'html': 1,
            'png': 1,
            'width': 600,
            'render_all': 1,
        }
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_result, endpoint='render.json', args=splash_args)

    def parse_result(self, response):
        html = response.body

        top_rankings = response.xpath('//body/div/main/div[@class = "Partition top_ranking Partition-separate"]/div[@class = "RankingCarousel"]/amp-list/div[@class="i-amphtml-fill-content i-amphtml-replaced-content"]').extract()
        print(top_rankings)
        # for item in top_rankings:
        #     brand = item.xpath('.//div[@class="TinyShelfItem_info"]/p[@class="TinyShelfItem_brand"]/text()').extract_first()
        #     name = item.xpath('.//div[@class="TinyShelfItem_info"]/p[@class="TinyShelfItem_name"]/text()').extract_first()
        #     price = item.xpath('.//div[@class="TinyShelfItem_info"]/p[@class="TinyShelfItem_price"]/text()').extract_first()

        #     yield {
        #         "brand": brand,
        #         "name": name,
        #         "price": price,
        #     }
            

