import scrapy
import json
from scrapy.utils.response import open_in_browser
from scrapy.cmdline import execute

from adaptio.items import AdaptioItem


class LinkExtract(scrapy.Spider):

    name = 'LinkExtract'

    def start_requests(self):

        url = 'https://www.adapt.io/directory/industry/telecommunications/A-1'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        allpages = response.xpath('//div[contains(@class, "DirectoryTopInfo_linkItemWrapper__2MyQQ ")]/a/@href').getall()

        for spage in allpages:
            yield scrapy.Request(url=spage, callback=self.Company)

    def Company(self, response):

        alllinks = response.xpath('//div[contains(@class, "DirectoryList_linkItemWrapper__3F2UE ")]/a')

        for slink in alllinks:

            name = slink.xpath('./text()').get('')
            link = slink.xpath('./@href').get('')

            item = AdaptioItem()

            item['company_name'] = name
            item['source_url'] = link

            yield item


if __name__ == '__main__':
    execute('scrapy crawl LinkExtract'.split())