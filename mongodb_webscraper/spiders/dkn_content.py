import scrapy
from scrapy.selector import Selector
import json
class DknContentSpider(scrapy.Spider):
    name = 'dkn_content'
    with open('links.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    names = [obj["link"] for obj in data]
    start_urls = [name for name in names if name.startswith("https://")]
    # start_urls = ['https://www.dkn.tv/thoi-su/4-tiep-vien-vietnam-airlines-xach-hon-11kg-ma-tuy-duoc-tra-tu-do.html']
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_page)
    
    def parse_page(self, response):
        title = Selector(response).xpath('//*[@class="post-title"]/text()').extract()
        content = response.xpath('//div[@class="post-content"]//text()')
        author = response.css('div.p-meta span.p-meta-author span::text').get()
        date = response.css('div.p-meta span.tie-date span.p-time::text').get()
        txt_contents = ""
        for text in content:
            txt_contents = txt_contents + text.extract().strip()
        if (len(title)>0 and txt_contents!= ""):
            result = {
                'title': title,
                'content': txt_contents,
                'author': author,
                'date': date,
                "class": 1           
            }
            
            with open('article.json', 'a', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False)
            yield result
        