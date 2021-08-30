# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from bili.items import DanmusItem, BiliItem


class BiliPipeline:
    def process_item(self, item, spider):
        if isinstance(item, BiliItem):
            urls = item["urls"]
            f = open("./data.txt", 'a', encoding="utf-8")
            for url in urls:
                if url[:5] == '//www':
                    f.writelines(str(url))
                    f.writelines("\n")
                
            f.close()
        if isinstance(item, DanmusItem):
            danmus = item['danmus']
            # print("type:", type(danmus))
            # print("content:", danmus)
            f = open("./danmu.txt", 'a', encoding='utf-8')
            if((danmus[0] != '<') & (danmus[0] != 'p')):
                f.writelines(str(danmus))
                f.writelines("\n")
            
            f.close()
        return item

