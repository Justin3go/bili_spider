import scrapy
from bili.items import DanmusItem, BiliItem
import sys
from comment import Bilibili


class BiliSearchSpider(scrapy.Spider):
    keyword = 'matepad11'
    name = 'bili_search'
    # allowed_domains = ['bilibili.com']
    start_urls = ['https://search.bilibili.com/all?keyword=' + keyword + '&page=1']
    url = 'https://search.bilibili.com/all?keyword=' + keyword + '&page=%d'
    page = 1
    p = 1

    def parse(self, response):
        if response.status == 200:

            videos = response.xpath('//ul[@class="video-list clearfix"]//a/@href').extract()
            # 限制最多爬取50页
            if((videos == []) | self.page >= 50):
                print("无更多界面，终止爬取")
                sys.exit()

            # 使用这些url进行下一步（视频弹幕）的爬取
            for video in videos:
                if video[:5] != '//www':  # 过滤
                    continue
                video = 'http:' + video
                # 使用刚刚下载的爬取弹幕的类
                b = Bilibili(video, self.p, './demo.jpg')
                b.getAidAndCid()
                b.getBarrage()
                item_b = DanmusItem()
                item_b["danmus"] = b.barrage
                yield item_b

            # 创建item对象，将解析的数据保存
            item = BiliItem()
            item["urls"] = videos

            yield item

            # 如果能爬，就回调自己进行循环爬取后面的界面，每次page+=1
            self.page += 1
            new_url = format(self.url % self.page)
            print("正在爬取第%d页界面" % self.page)

            yield scrapy.Request(url=new_url, callback=self.parse, dont_filter=True)


