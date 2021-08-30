import requests
import re
import jieba
import time
import sys
from bs4 import BeautifulSoup


class Bilibili:
    def __init__(self, videourl, page, img_path):
        
        self.page = str(page)
        self.img_path = img_path
        self.baseurl = videourl.split('?')[0]

    # 爬取弹幕和评论

    def getAidAndCid(self):
        cidurl = self.baseurl + "?p=" + self.page
        cidRegx = '{"cid":([\d]+),"page":%s,' % (self.page)
        aidRegx = '"aid":([\d]+),'
        r = requests.get(cidurl)
        r.encoding = 'utf-8'
        try:

            self.cid = re.findall(cidRegx, r.text)[0]
            self.aid = re.findall(aidRegx, r.text)[int(self.page) - 1]
        except:
            print('视频序号输入有误，请保证序号在1到最大值之间！')
            time.sleep(3)
            sys.exit()

    def getBarrage(self):
        print('正在获取弹幕......')

        commentUrl = 'https://comment.bilibili.com/' + self.cid + '.xml'

        # 获取并提取弹幕 #
        r = requests.get(commentUrl)
        r.encoding = 'utf-8'
        content = r.text
        # 正则表达式匹配字幕文本(前两行是无用的)
        comment_list = re.findall('>(.*?)</d><d ', content)[2:]

        # jieba分词
        self.barrage = "\n".join(comment_list)

    def getComment(self, x, y):
        for i in range(x, y + 1):
            r = requests.get(
                'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&sort=2'
                .format(i, self.aid)).json()
            replies = r['data']['replies']
            print('------评论列表------')
            for repliy in replies:
                print(repliy['content']['message'] + '\n')

        pass


def checkUrl(url):
    try:
        r = requests.get(url)
    except:
        return 0
    r.encoding = 'utf-8'
    # 视频名称正则表达式
    regx = '"part":"(.*?)"'
    r.encoding = 'utf-8'
    result = re.findall(regx, r.text)
    count = 0
    if len(result) > 0:
        print('------视频列表------')
        for i in result:
            count += 1
            print("视频" + str(count) + " : " + i)
        return 1
    return 0
