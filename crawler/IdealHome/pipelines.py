# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class IdealhomePipeline:
    required_fields = ("create_at", "apartment_name", "url")
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        for field in self.required_fields:
            if not adapter.get(field):
                raise DropItem(f"Missing required field: {field}")
            return item
