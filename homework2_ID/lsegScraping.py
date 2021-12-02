import scrapy

#Some (1000) of the fastest-growing and most dynamic small and medium-sized enterprises (SMEs) across Europe in 2018

class QuotesSpider(scrapy.Spider):
    name = 'lsegSpider'
    start_urls = [
        'https://www.lseg.com/resources/1000-companies-inspire/2018-report-1000-companies-europe/search-1000-companies-europe-2018',
    ]

    def parse(self, response):

        #Selezione informazioni dal sito web
        for quote in response.css('div.tabular-data-panel'):
            yield {
                'company_name': quote.xpath('ul/li/span[2]/text()').get(),
                'website': quote.xpath('ul/li/span[2]/a/text()').get(),
                'sector': quote.xpath('ul/li[3]/span[2]/text()').get(),
                'country': quote.xpath('ul/li[4]/span[2]/text()').get(),
                'revenue_euros': quote.xpath('ul/li[5]/span[2]/text()').get(),
            }
      
        
        #Scorrimento pagine del sito web
        next_page = response.xpath('//*/ul[@class = "pagination pager"]/li[last()-1]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


