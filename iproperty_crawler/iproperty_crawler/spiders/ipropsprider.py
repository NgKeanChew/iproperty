# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from iproperty_crawler.items import IpropertyCrawlerItem
from scrapy.spiders import CrawlSpider, Rule

class IpropSpider(CrawlSpider):
    name = 'ipropspider'
    allowed_domains = ['www.iproperty.com.my']
    start_urls = ['http://www.iproperty.com.my/buy/kuala-lumpur/']
    rules = (
            Rule(LinkExtractor(allow=(), restrict_xpaths=("//ul[contains(@class,'listing')]/li//h3/a")), callback='parse_item',follow=True),
            Rule(LinkExtractor(allow=(), restrict_xpaths=("//ul[contains(@class,'pagination')]/li/a")), follow=True)
            )
    def parse_item(self, response):
        item = IpropertyCrawlerItem()
        item["website_url"] = response.url
        item["property_name"] = response.xpath("//h2[contains(@class,'description')]/text()").extract()
        item["asking_price"] = response.xpath("/div[contains(@class,'property-price')]/text()").extract_first()
        item["address"] = response.xpath("//strong[contains(@class,'property-address')]/text()").extract_first()
        item["area"] = response.xpath("///div[contains(@class,'property-areas-info')]/ul/li/text()").extract()
        return item

class IpropSpider2(scrapy.spiders.Spider):
	name = 'ipropspider2'
	allowed_domains = ['www.iproperty.com.my']
	start_urls = ['http://www.iproperty.com.my/buy/kuala-lumpur/']
	
	def parse(self,response):
		max_page = response.xpath("//ul[contains(@class,'pagination')]/li/a/text()").extract()[-1]
		for i in range(1,int(max_page)+1):
			yield scrapy.Request('{}?page={}'.format(response.url,i), callback=self.extract_links)

	def extract_links(self,response):
		links = response.xpath("//ul[contains(@class,'listing')]/li[contains(@class,'sale-')]//a/@href").extract()
		links = [i for i in set(links) if '/property/'in i]
		for i in links:
			url = 'https://www.iproperty.com.my{}'.format(i)
			yield scrapy.Request(url,callback=self.extract_info)

	def extract_info(self, response):
		item = IpropertyCrawlerItem()
		
		item["website_url"] = response.url
		item["property_name"] = response.xpath("//h2[contains(@class,'description')]/text()").extract()
		item["asking_price"] = response.xpath("//div[contains(@class,'property-price')]/text()").extract_first()
		item["address"] = response.xpath("//strong[contains(@class,'property-address')]/text()").extract_first()
		item["area"] = response.xpath("///div[contains(@class,'property-areas-info')]/ul/li/text()").extract()
		
		item["property_type"] = response.xpath("//div[contains(@class,'propertyType')]//text()").extract()
		item["tenure"] = response.xpath("//div[contains(@class,'tenure')]//text()").extract()
		item["posted_date"] = response.xpath("//div[contains(@class,'updatedAt')]//text()").extract()
		item["land_title_type"] = response.xpath("//div[contains(@class,'landTitleType')]//text()").extract()
		return item


