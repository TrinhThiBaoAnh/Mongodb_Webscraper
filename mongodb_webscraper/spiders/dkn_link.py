import scrapy


class DknLinkSpider(scrapy.Spider):
    name = 'dkn_links'
    start_urls = ['https://www.dkn.tv/']

    def parse(self, response):
        for link in response.css('a::attr(href)').getall():
            yield {'link': link}
