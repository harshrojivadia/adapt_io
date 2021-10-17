import scrapy
import json
from scrapy.utils.response import open_in_browser
from scrapy.cmdline import execute
import pymongo

from adaptio.items import AdaptioDataItem


class DataSpider(scrapy.Spider):

    name = 'dataspider'

    handle_httpstatus_list = [503, 502, 501, 204, 429, 204]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        conn = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = conn.adaptio

    def start_requests(self):

        urls = self.db['LinkData'].find()

        for surl in urls:
            headers = {
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
            }
            # url = 'https://www.adapt.io/company/igroup-pte-ltd'
            yield scrapy.Request(url=surl['source_url'], headers=headers, callback=self.infoparser, meta={'url': surl['source_url']})
            # break

    def infoparser(self, respones):

        if respones.status in self.handle_httpstatus_list:
            url = respones.meta['url']
            headers = {
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
            }
            # url = 'https://www.adapt.io/company/igroup-pte-ltd'
            yield scrapy.Request(url=url, headers=headers, callback=self.infoparser,
                                 meta={'url': url})
        else:
            Company_name = respones.xpath('//h1[@itemprop="name"]/text()').get('')
            Company_website = respones.xpath('//div[@itemprop="url"]/text()').get('')
            Company_industry = respones.xpath('//span[contains(text(), "Industry")]/following-sibling::span/text()').get('')
            Company_revenue = respones.xpath('//span[contains(text(), "Revenue")]/following-sibling::span/text()').get('')
            Company_location = "".join(respones.xpath('//span[@itemprop="address"]//text()').getall())
            Company_employee_size = respones.xpath('//span[contains(text(), "Head Count")]/following-sibling::span/text()').get('')

            contact = list()
            allcontact = respones.xpath('//div[@itemprop="employee"]')

            for scontact in allcontact:
                contactdict = dict()
                contactdict['Contact_name'] = scontact.xpath('.//a[@itemprop="url"]/text()').get('')
                contactdict['Contact_jobtitle'] = scontact.xpath('.//p[@itemprop="jobTitle"]/text()').get('')
                Contact_email_domain = scontact.xpath('.//button[@itemprop="email"]/text()').get('')
                try:
                    Contact_email_domain = Contact_email_domain.split('@')[-1]
                except:
                    Contact_email_domain = ''
                contactdict['Contact_email_domain'] = Contact_email_domain

                contact.append(contactdict)

            item = AdaptioDataItem()

            item['Company_name'] = Company_name
            item['Company_website'] = Company_website
            item['Company_industry'] = Company_industry
            item['Company_revenue'] = Company_revenue
            item['Company_location'] = Company_location
            item['Company_employee_size'] = Company_employee_size
            item["contact_details"] = contact

            yield item


if __name__ == '__main__':
    execute('scrapy crawl dataspider'.split())