import scrapy

# Doctors of Grady Memorial Hospital in Atlanta

class QuotesSpider(scrapy.Spider):

    name = 'gradyDocSpider'

    def create_start_urls():
    
        urls = []
        for i in range(1,115):
            next_page = 'https://www.gradyhealth.org/find-a-doctor/?keyword=&loc=&care_and_treatment=&specialty=&language=&gender=&action=filter_find_a_doctor&alpha=&page=%s' %i
            urls.append(next_page)
        
        return urls

    start_urls = create_start_urls()

    def parse(self, response):

        #Scorrimento link per primary care
        for quote in response.xpath('//*/div[@id="doctors_results"]/div'):
            
            doctor_page = quote.xpath('div/h2/a/@href').get()
            hospital = quote.xpath('div/p[2]/text()').get()

            #Selezione link
            if doctor_page is not None:
                yield response.follow(doctor_page, self.parse_doctors, meta={'hospital': hospital})
        

    def parse_doctors(self, response):

        medical_specialty = None
        board_certifications = None
        hospital = response.meta['hospital']
        hospital_affiliations = None
        fellowships = None
        education_and_training_medical_school = None
        education_and_training_internship = None
        education_and_training_residency = None


        for section in response.xpath('//*/div[@class="col-xs-12 col-sm-8"]/section'):

            title = section.xpath('div/div/div[@class="certificate-header"]/h2/text()').get()
            
            if(title == 'Specialties'):
                medical_specialty = section.xpath('div/div/div[@class="content"]/ul/li/text()').get()

            if(title == 'Board Certifications'):
                board_certifications = section.xpath('div/div/div[@class="content"]/ul/li/text()').get()
            

        
        for section in response.xpath('//*/div[@class="col-xs-12 col-sm-8"]/section'):

            title = section.xpath('div[@class="certificate-header"]/h2/text()').get()

            if(title == 'Affiliations'):
                hospital_affiliations = section.xpath('div[@class="content"]/ul/li/text()').get()

            if(title == 'Fellowships'):
                fellowships = section.xpath('div[@class="content"]/ul/li/text()').get()

            if(title == 'Education & Training'):
                for row in section.xpath('div[@class="content"]/ul/li'):
                    medschool = row.xpath('text()').get()[:14]
                    print('--------------------medschool----------------')
                    print(medschool)
                    internship = row.xpath('text()').get()[:10]
                    residency = row.xpath('text()').get()[:9]

                    if(medschool == 'Medical School'):
                        education_and_training_medical_school = row.xpath('text()').get()[16:]
                    if(internship == 'Internship'):
                        education_and_training_internship = row.xpath('text()').get()[12:]
                    if(residency == 'Residency'):
                        education_and_training_residency = row.xpath('text()').get()[11:]
        

        yield {
            'medical_specialty': medical_specialty,
            'board_certifications': board_certifications,
            'doc_name': response.xpath('//*/div[@class="doctor-header"]/h1/text()').get(), 
            'doc_gender': response.xpath('//*/p[@class="title"][contains(text(), "Gender")]/following::p/text()').get(),
            'doc_languages' : response.xpath('//*/p[@class="title"][contains(text(), "Speaks other Languages")]/following::p/text()').get(),            
            'hospital': hospital,
            'hospital_affiliations': hospital_affiliations,
            #'hospital_address': response.xpath('//*[@class="address sidebar-list"]/a/text()[1]').get() + ', ' + response.xpath('//*/div[@class="address sidebar-list"]/a/text()[2]').get(),
            'hospital_telephone': response.xpath('//*/div[@class="col-xs-12 col-sm-6 col-md-2 footer-col"]/p[3]/strong/a/text()').get(),
            'fellowships': fellowships,
            'education_and_training_medical_school': education_and_training_medical_school,
            'education_and_training_internship': education_and_training_internship,
            'education_and_training_residency': education_and_training_residency,
            }
