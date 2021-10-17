# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

from adaptio.items import AdaptioItem, AdaptioDataItem


class AdaptioPipeline:
    def __init__(self):
        conn = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = conn.adaptio
        unique = self.db['LinkData'].create_index("source_url", unique=True)
        unique_1 = self.db['DataTable'].create_index("Company_website", unique=True)
        print(unique)

    def process_item(self, item, spider):
        if isinstance(item, AdaptioItem):
            try:
                self.db['LinkData'].insert(dict(item))
            except Exception as e:
                print(e)
            return item
        if isinstance(item, AdaptioDataItem):
            try:
                self.db['DataTable'].insert(dict(item))
            except Exception as e:
                print(e)
            return item
