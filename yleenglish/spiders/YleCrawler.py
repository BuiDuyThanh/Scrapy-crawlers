#from scrapy.spiders import BaseSpider
#from scrapy.selector import HtmlXPathSelector
#from yleenglish.items import YleEnglishItem
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor 
from yleenglish.items import YleEnglishItem

class MySpider(scrapy.Spider):
    name = "news"
    #declare the domain name of targeted website
    allowed_domains = ["yle.fi"]
    #declare list of url we want to crawl
    start_urls = ["http://www.yle.fi/uutiset/news/"]
    #in case we want to open and read a list of URL in a txt file
    #f = open("urls.txt")
    #start_urls = [url.strip() for url in f.readlines()]
    #f.close()
    
    #parse() : is a spider's method. The response from start URLs will be taken into the method as an argument. The response data will be parsed, extracted and returned as Item's objects.  
    
    def parse(self, response):
        
        #for href in response.css("section.recommends > article > a::attr('href')"):
         #   url = response.urljoin(href.extract())
          #  yield scrapy.Request(url, callback=self.parse_dir_contents)
        url = response.url

      
        yield scrapy.Request(url, callback=self.parse_dir_contents)
#        yield items.append(new_item)
        
    def parse_dir_contents(self, response):
        #hxs = HtmlXPathSelector(response)
        #topics = hxs.xpath('//div[@class="custom"]')
        #items = []

        #for sel in response.xpath('//*[@id="container"]/article/header/div/h1'): #topics:
        
        for sel in response.xpath('//section[@class="recommends"]/article/a/@href'): #topics:
            
      #      item['topic'] = sel.xpath('article/a/h1/text()').extract()
     #       item['link'] = sel.xpath('article/a/@href').extract()
            #items.append(item)
            url = response.urljoin(sel.extract())
            yield scrapy.Request(url, callback=self.parse_in_details)

    def parse_in_details(self, response):
        item = YleEnglishItem()
        item['link'] = response.url
        item['title'] = response.xpath('//*[@id="container"]/article/header/div/h1/text()').extract()
        yield item
        

