import scrapy
from ..items import AtlaItem

class RatingsSpider(scrapy.Spider):
    name = "atla"

    start_urls = [
        "https://www.imdb.com/title/tt0417299/episodes?season=1&ref_=tt_eps_sn_1"
    ]

    def parse(self, response):
        items = AtlaItem()

        season = response.css("#episode_top::text").get()
        for info in response.css(".info"):
            items['season'] = season
            items['title'] = info.css("strong a::text").get()
            items['rating'] = info.css(".ipl-rating-star.small .ipl-rating-star__rating::text").get()
            yield items
        
        next_page = response.css('#load_next_episodes::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)