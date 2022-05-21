import scrapy
from ..items import BoardgamesItem


class GamesSpider(scrapy.Spider):
    name = 'games'
    start_urls = ['https://boardgamegeek.com/browse/boardgame/page/1']

    def parse(self, response):
        items = BoardgamesItem()
        base_url = 'https://boardgamegeek.com'
        for game in response.css('#row_'):
            items['id'] = int(game.css("#row_ a::attr(href)").re("\d+")[0])
            items['rank'] = game.css(".collection_rank a::attr(name)").get()
            items['name'] = game.css(".primary ::text").get()
            items['url'] = base_url + game.css("#row_ a::attr(href)").get()
            items['rating'] = game.css(
                "#row_ .collection_bggrating:nth-child(5)::text").get().split()[0]
            items['num_voters'] = response.css(
                "td.collection_bggrating ::text")[2].get()
            items['year'] = int(response.css(
                "span.smallerfont.dull ::text").get()[1:-1])
            items['description'] = response.css(
                "p.smallefont.dull ::text").get().replace("\n", "").replace("\t", "")
            yield items

        next_page = response.css('a[title="next page"] ::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
