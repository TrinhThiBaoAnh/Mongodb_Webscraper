import scrapy
from scrapy.selector import Selector


# scrapy runspider scheduled.py -o items.json -t json
# scrapy runspider scheduled.py
class ScheduledSpider(scrapy.Spider):
    name = 'scheduled'
    allowed_domains = ['xscores.com']
    start_urls = ["https://www.xscores.com/soccer/scheduled-games"]

    def parse(self, response):
        table_contents = Selector(response).xpath('//*[@id="scoretable"]/a')
        for n in table_contents:

            link = n.xpath('@href').extract()
            country_name = n.xpath('@data-country-name').extract()
            competition_name = n.xpath('@data-competition-name').extract()
            data_parent_competition = n.xpath(
                '@data-parent-competition').extract()
            data_league_type = n.xpath('@data-league-type').extract()
            data_league_round = n.xpath('@data-league-round').extract()
            # ft_home = n.xpath('div[@class="score_score score_cell centerTXT "]/div[@class="scoreh_ft score_cell centerTXT"]/text()').extract()
            # ft_away = n.xpath('div[@class="score_score score_cell centerTXT "]/div[@class="scorea_ft score_cell centerTXT"]/text()').extract()
            home_team = n.xpath(
                'div[@class="score_teams  score_cell"]/div[@class="score_home score_cell"]/div[@class="score_home_txt score_cell wrap"]/text()').extract()
            away_team = n.xpath(
                'div[@class="score_teams  score_cell"]/div[@class="score_away score_cell"]/div[@class="score_away_txt score_cell wrap"]/text()').extract()

            zipped = zip(link, 
                         country_name,
                         competition_name,
                         data_league_type,
                         data_league_round,
                         data_parent_competition,
                         home_team,
                         away_team)

            for item in zipped:
                result = {
                    'link': item[0],
                    'country_name': item[1],
                    'competition_name': item[2],
                    'data_league_type': item[3],
                    'data_league_round': item[4],
                    'data_parent_competition': item[5],
                    'home_team': item[6],
                    'away_team': item[7]                    
                }
            yield result
