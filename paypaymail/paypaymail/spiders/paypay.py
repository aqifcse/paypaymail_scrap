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

        top_rankings = []
        famous_stores = []

        scrap_output = { 
            'top_rankings': top_rankings, 
            'famous_stores': famous_stores 
        }

        # --------------------------------------------Top Ranking-------------------------------------------------------------------------------------------------
        
        top_rankings = response.xpath('//body/div/main/div[@class = "Partition top_ranking Partition-separate"]/div[@class = "RankingCarousel"]/amp-list/div[@class="i-amphtml-fill-content i-amphtml-replaced-content"]/amp-carousel/div[@class="i-amphtml-scrollable-carousel-container"]').extract()

        ranking_categories = response.xpath('.//div[@class="RankingItem amp-carousel-slide amp-scrollable-carousel-slide"]/div')

        for category in ranking_categories:
            category_name = category.xpath('./p/a/text()').extract_first().replace(' ', '').replace('\n', '')
            items = category.xpath('.//div[@class="TinyShelfItem_info"]')

            ranking_item_list = []

            ranking_output = {
                'category_name' : category_name,
                'items' : ranking_item_list
            }
        
            for item in items:
                brand = item.xpath('./p[@class="TinyShelfItem_brand"]/text()').extract_first()
                name = item.xpath('./p[@class="TinyShelfItem_name"]/text()').extract_first()
                price = item.xpath('./p[@class="TinyShelfItem_price"]/text()').extract_first()
                # yield {
                #     'category_name': category_name,
                #     'item_brand' : brand,
                #     'item_name' : name,
                #     'item_price' : price,
                # }

                ranking_items_out = {
                    'item_brand' : brand,
                    'item_name' : name,
                    'item_price' : price,
                }

                ranking_output['items'].append(ranking_items_out)
            scrap_output['top_rankings'].append(ranking_output) 

        #------------------------------------------Famous Store ----------------------------------------------------------------------------------------------------------
        famous_stores = response.xpath('//body/div/main/div[@class = "Partition top_famousStore Partition-separate"]/div[@class = "RecommendStoreCarousel"]/amp-list/div[@class="i-amphtml-fill-content i-amphtml-replaced-content"]/amp-carousel/div[@class="i-amphtml-scrollable-carousel-container"]').extract()

        stores = response.xpath('.//div[@class="RecommendStoreItem amp-carousel-slide amp-scrollable-carousel-slide"]/div')

        for store in stores:
            store_name = store.xpath('./p/a/text()').extract_first().replace(' ', '').replace('\n', '')
            items = store.xpath('.//div[@class="RecommendStoreItem_unit"]/div/a/div')

            store_item_list = []

            store_output = {
                'store_name' : store_name,
                'items' : store_item_list
            }
        
            for item in items:
                item_title = item.xpath('./p[@class="TinyItem_title"]/text()').extract_first()
                price = item.xpath('./p[@class="TinyItem_price"]/text()').extract_first()

                # yield {
                #     'store_name': store_name,
                #     'item_title' : item_title,
                #     'item_price' : price,
                # }

                store_items_out = {
                    'item_title' : item_title,
                    'item_price' : price,
                }

                store_output['items'].append(store_items_out)
            scrap_output['famous_stores'].append(store_output)

        yield scrap_output
