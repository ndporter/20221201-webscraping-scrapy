#2022-12-01
#Webscraping in Python with Scrapy
#Nathaniel Porter (ndporter@vt.edu)
#Based on https://librarycarpentry.org/lc-webscraping/04-scrapy/index.html

#to use:
#scrapy crawl mppaddresses -o output.csv #-o and filename save output to file rather than screen

import scrapy
from ontariompps.items import OntariomppsItem # We need this so that Python knows about the item object


class MppaddressesSpider(scrapy.Spider):
    name = 'mppaddresses' # The name of this spider
    
    # The allowed domain and the URLs where the spider should start crawling:
    allowed_domains = ['ola.org']
    start_urls = ['http://ola.org/en/members/current']

    def parse(self, response):
        # The main method of the spider. It scrapes the URL(s) specified in the
        # 'start_url' argument above. The content of the scraped URL is passed on
        # as the 'response' object.
        for url in response.xpath("//td/a/@href").extract():
            # This loops through all the URLs found inside an element of class 'mppcell'

            # Constructs an absolute URL by combining the response’s URL with a possible relative URL:
            full_url = response.urljoin(url)
            
            # The following tells Scrapy to scrape the URL in the 'full_url' variable
            # and calls the 'get_details() method below with the content of this URL:
            yield scrapy.Request(full_url, callback=self.get_details)
        
    def get_details(self, response):
        # This method is called on by the 'parse' method above. It scrapes the URLs
        # that have been extracted in the previous step.

        item = OntariomppsItem() # Creating a new Item object
        
        # Store scraped data into that item:
        item['name'] = response.xpath('//*[(@id = "block-views-block-member-block-4-2")]//h1/text()').extract_first() #extracts name and district name
        item['email'] = response.xpath('//*[(@id = "block-views-block-member-contact-group-mpp-contact-group-profile")]//a/text()').extract_first() #extracts email
        
        # Return that item to the main spider method:
        yield item
