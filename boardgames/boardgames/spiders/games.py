import scrapy
from ..items import BoardgamesItem
import pandas as pd
import sqlite3


class GamesSpider(scrapy.Spider):
    name = 'games'
    start_urls = ['https://boardgamegeek.com/browse/boardgame/page/1']

    def parse(self, response):
        items = BoardgamesItem()
        base_url = 'https://boardgamegeek.com'
        con = sqlite3.connect(
            'C:/Users/u10054206/OneDrive - NOS SGPS, S.A/Carreira/Portfolio/Python Projects/Scrapy/boardgames/boardgames.db')
        df = pd.read_sql_query('SELECT * FROM games;', con)
        print(df['id'].values)
        for game in response.css('#row_'):
            if int(game.css("#row_ a::attr(href)").re("\d+")[0]) not in df['id'].values:
                items['id'] = int(game.css("#row_ a::attr(href)").re("\d+")[0])
                items['rank'] = game.css(
                    ".collection_rank a::attr(name)").get()
                items['name'] = game.css(".primary ::text").get()
                items['url'] = base_url + game.css("#row_ a::attr(href)").get()
                items['rating'] = game.css(
                    "#row_ .collection_bggrating:nth-child(5)::text").get().split()[0]
                try:
                    items['num_voters'] = int(game.css(
                        "td.collection_bggrating ::text")[2].get().replace("\n", "").replace("\t", ""))
                except:
                    items['num_voters'] = 'N/A'
                try:
                    items['year'] = int(game.css(
                        "span.smallerfont.dull ::text").get()[1:-1])
                except:
                    items['year'] = 'N/A'
                try:
                    items['details'] = game.css(
                        "p.smallefont.dull ::text").get().replace("\n", "").replace("\t", "")
                except:
                    items['details'] = 'N/A'
                yield items

        next_page = response.css('a[title="next page"] ::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
