import scrapy

# AMERICA'S TOP LEGAL FIRMS

class QuotesSpider(scrapy.Spider):
    name = 'lowCrossSpider'
    
    start_urls = [
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=A',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=B',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=C',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=D',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=E',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=F',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=G',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=H',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=I',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=J',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=K',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=L',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=M',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=N',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=O',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=P',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=Q',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=R',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=S',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=T',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=U',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=V',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=W',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=X',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=Y',
        'https://www.lawcrossing.com/lclawfirmprofile_listing.php?rtitle=Z',
    ]

    def parse(self, response):

        #Scorrimento blocchi del sito web
        for row in response.xpath('//*/form[@id="formmain"]/div'):
            
            lawyer_firm =  row.xpath('div/h3/a/text()').get()   #nome dell'avvocato
            lawyer_page = row.xpath('div/h3/a/@href').get()     #pagina web dell'avvocato
            
            #Selezione informazioni per ogni avvocato
            if lawyer_page is not None:
                yield response.follow(lawyer_page, self.parse_law_firm, meta={'lawyer_firm': lawyer_firm})
        

        #Scorrimento pagine del sito web
        next_page = response.xpath('/html/body/div[1]/section/div/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/ul/li[last()]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


    #Scraping della pagina per ogni studio legale
    def parse_law_firm(self, response):

        #Selezione informazioni dal sito web di ogni studio legale

        lawyer_firm = response.meta['lawyer_firm']

        company_link = response.xpath('//*/p[@style="margin-bottom: 0px;"]/a/text()').get()

        street_address = response.xpath('//*/span[@itemprop="streetAddress"]/text()').get()
        if street_address is not None:
            street_address = street_address.strip('\n\t |')     #pulizia del testo
        
        address_locality = response.xpath('//*/span[@itemprop="addressLocality"]/text()').get()
        if address_locality is not None:
            address_locality = address_locality.strip('\n\t |')[-2:]        #pulizia del testo

        postal_code = response.xpath('//*/span[@itemprop="postalCode"]/text()').get()
        if postal_code is not None:
            postal_code = postal_code.strip('\n\t |')       #pulizia del testo

        telephone = response.xpath('//*/span[@itemprop="telephone"]/text()').get()
        if telephone is not None:
            telephone = telephone.strip('\n\t |')       #pulizia del testo
        
        #Salvataggio
        yield {
            'lawyer_firm': lawyer_firm,
            'company_link': company_link,
            'street_address': street_address,
            'address_locality': address_locality,
            'postal_code': postal_code,
            'telephone': telephone,
        }

