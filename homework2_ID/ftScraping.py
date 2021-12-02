import scrapy

#FinancialTimes 1000 – Europe’s Fastest Growing Companies 2018 (with 2016 revenue)

class QuotesSpider(scrapy.Spider):
    name = 'ftSpider'
    start_urls = [
        'https://www.ft.com/content/cf0c5fce-3112-11e8-b5bf-23cb17fd1498',
    ]

    def parse(self, response):

        #Selezione informazioni dal sito web
        for row in response.xpath('//*/table/tbody/tr'):

            #Salvataggio
            yield {
                'company_name': row.xpath('td[2]/a/text()').get(),
                'website': row.xpath('td[2]/a/@href').get(),
                'sector': row.xpath('td[4]/a/text()').get(),
                'country': row.xpath('td[3]/a/text()').get(),
                'revenue_euros': row.xpath('td[7]/text()').get()[:-3] + 'M',  #conversione in milioni
                'employees': row.xpath('td[9]/text()').get(),
                'founded': row.xpath('td[10]/text()').get(),
            }