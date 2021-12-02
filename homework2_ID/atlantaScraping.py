import scrapy

# Atlanta Top Doctors 2021

class QuotesSpider(scrapy.Spider):
    name = 'atlantaDocSpider'
    start_urls = [
        'https://www.atlantamagazine.com/top-doctors/',
    ]

    def parse(self, response):

        #Scorrimento link per primary care
        for link_pc in response.xpath('//*/div[@class="wpb_wrapper td_block_wrap vc_raw_html tdi_19_112 "]/div/div/a'):
            
            primary_care_page = link_pc.xpath('@href').get()
            print(primary_care_page)

            #Selezione link
            if primary_care_page is not None:
                yield response.follow(primary_care_page, self.parse_doctors)

        
        #Scorrimento link per specialists

        #Prima colonna di specialists
        for link_sp1 in response.xpath('//*/div[@class="wpb_wrapper td_block_wrap vc_raw_html tdi_27_291 "]/div/div/a'):
            
            specialists_page = link_sp1.xpath('@href').get()     #pagina web dell'avvocato
            
            #Selezione link
            if specialists_page is not None:
                yield response.follow(specialists_page, self.parse_doctors)
        
        #Seconda colonna di specialists
        for link_sp2 in response.xpath('//*/div[@class="wpb_wrapper td_block_wrap vc_raw_html tdi_31_6ae "]/div/div/a'):
            
            specialists_page = link_sp2.xpath('@href').get()     #pagina web dell'avvocato
            
            #Selezione link
            if specialists_page is not None:
                yield response.follow(specialists_page, self.parse_doctors)
        
        #Terza colonna di specialists
        for link_sp3 in response.xpath('//*/div[@class="wpb_wrapper td_block_wrap vc_raw_html tdi_35_e66 "]/div/div/a'):
            
            specialists_page = link_sp3.xpath('@href').get()     #pagina web dell'avvocato
            
            #Selezione link
            if specialists_page is not None:
                yield response.follow(specialists_page, self.parse_doctors)
        

    #Scraping pagina del dottore
    def parse_doctors(self, response):

        medical_specialty = response.xpath('//*/h2[@class="specialtyHeaders"]/text()').get().replace("\n", " ")
        
        #selezione del blocco dove prendere i dottori (saltando il blocco pubblicitario)
        for doc_block in response.xpath('//*/div[@class="wpb_wrapper"]/div'):
            for doctor in doc_block.xpath('div/div[@class="docListing"]'):

                #Salvataggio
                yield {
                    'medical_specialty': medical_specialty,
                    'doc_name': doctor.xpath('p[@class="docName"]/text()').get(),
                    'hospital': doctor.xpath('p[@class="docHospital"]/text()').get(),
                    'hospital_affiliations': doctor.xpath('p[@class="hospitalAffiliation"][1]/text()').get(),
                    'doc_special_expertise': doctor.xpath('p[@class="hospitalAffiliation"][2]/text()').get(),
                    'hospital_address': doctor.xpath('p[@class="contactInfo"]/text()[1]').get(),
                    'hospital_telephone': doctor.xpath('p[@class="contactInfo"]/text()[2]').get(),
                }
