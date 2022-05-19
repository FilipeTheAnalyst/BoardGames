import scrapy


class GamesSpider(scrapy.Spider):
    name = 'games'
    start_urls = ['https://boardgamegeek.com/browse/boardgame/page/1']

    def parse(self, response):
        base_url = 'https://boardgamegeek.com'
        for game in response.css('#row_'):
            yield{
                'rank': game.css(".collection_rank a::attr(name)").get(),
                'name': game.css(".primary ::text").get(),
                'url': base_url + game.css("#row_ a::attr(href)").get(),
                'rating': game.css(
                    "#row_ .collection_bggrating:nth-child(5)::text").get().split()[0]
            }

        next_page = response.xpath(
            '//*[@id="maincontent"]/form/div/div[1]/a[5]').attrib["href"]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
