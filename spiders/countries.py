import scrapy

class countriesSpider(scrapy.Spider):
    name = "countries"

    def start_requests(self):
        urls = ["https://www.cia.gov/library/publications/resources/the-world-factbook/"]

        for url in urls:
            yield scrapy.Request(url= url, callback=self.parse)

    def parse(self, response):
        for country  in response.css('#search-place > option'):
            yield {
                'text': country.css('option::attr(data-place-code)').get()
            }

