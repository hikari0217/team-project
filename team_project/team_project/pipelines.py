import json


class TeamProjectPipeline:

    def __init__(self):
        self.fp = open("duanzi.json", "w", encoding="utf-8")

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item_json = json.dumps(dict(item), ensure_ascii=False)
        self.fp.write(item_json + '\n', )
        return item

    def close_spider(self, spider):
        self.fp.close()
