#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import os


# 抓取淘宝商品图片
class TaobaoSpider:
    def __init__(self):
        self.dataAddr = []
        self.pages = []
        self.pictures = []
        self.numPerPage = 44
        self.pictureNum = 100
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' + \
                          ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}



    # 从dataAddress中获取网址
    def getAddresses(self):
        self.dataAddr = []
        # with open('dataAddress.txt', 'r') as f:
        #     while f.readline():
        #         self.dataAddr.append(f.readline())
        addr = "https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%A3%89%E8%A2%84&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest"
        self.dataAddr.append(addr)
        addr = "https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20180402&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E4%B9%A6%E6%9E%B6&suggest=history_3&_input_charset=utf-8&wq=&suggest_query=&source=suggest"
        self.dataAddr.append(addr)
        addr = "https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20180402&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E7%BE%BD%E6%AF%9B%E7%90%83%E6%8B%8D&suggest=history_4&_input_charset=utf-8&wq=&suggest_query=&source=suggest"
        self.dataAddr.append(addr)
        addr = "https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20180402&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E8%BF%90%E5%8A%A8%E8%A3%A4&suggest=history_5&_input_charset=utf-8&wq=&suggest_query=&source=suggest"
        self.dataAddr.append(addr)
        addr = "https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20180402&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E6%B4%97%E8%A1%A3%E6%B6%B2&suggest=history_6&_input_charset=utf-8&wq=&suggest_query=&source=suggest"
        self.dataAddr.append(addr)
        addr = "https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20180402&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E8%BF%90%E5%8A%A8%E9%9E%8B&suggest=history_7&_input_charset=utf-8&wq=&suggest_query=&source=suggest"
        self.dataAddr.append(addr)
        addr = "https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20180402&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E4%B9%A6%E5%8C%85&suggest=history_8&_input_charset=utf-8&wq=&suggest_query=&source=suggest"
        self.dataAddr.append(addr)
        addr = "https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20180402&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E6%89%8B%E6%9C%BA&suggest=history_10&_input_charset=utf-8&wq=&suggest_query=&source=suggest"
        self.dataAddr.append(addr)
        addr = "https://s.taobao.com/search?q=%E5%82%A8%E8%93%84%E7%BD%90&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180402&ie=utf8"
        self.dataAddr.append(addr)
        addr = "https://s.taobao.com/search?q=%E6%A8%A1%E5%9E%8B%E9%A3%9E%E6%9C%BA&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180402&ie=utf8"
        self.dataAddr.append(addr)



    def getPage(self,pageIndex):
        urls = []
        self.pages = []
        # 后缀为：&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s=44
        for address in self.dataAddr:
            urls.append(address + "&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s="
                       + str(pageIndex * self.numPerPage))
        for url in urls:
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            self.pages.append(response.read())

    def getPictures(self):
        datas = []
        self.pictures = []
        pattern = re.compile('<div class="item J_MouserOnver.*?<div class="pic-box J_Mouse.*?' +
                             'EnterLeave.*?<div class="pic-box-inner.*?<div class="pic.*?' +
                             '<img id=.*?src="(.*?)"', re.S)
        for page in self.pages:
            items = re.findall(pattern, page)
            datas.append((x for x in items))

        for i in range(self.numPerPage):
            for data in datas:
                self.pictures.append(data.next())

    def savePictures(self,imageURL,no):
        u = urllib.urlopen("https:" + imageURL)
        data = u.read()
        fileName = 'TB_picture/' + str(no) + '.jpg'
        f = open(fileName, 'wb')
        f.write(data)
        print u"正在保存图片", fileName
        f.close()

    def spider(self):
        pageIndex = -1
        self.getAddresses()
        for i in range(self.pictureNum):
            if i % self.numPerPage == 0:
                pageIndex = pageIndex + 1
                self.getPage(pageIndex)
                self.getPictures()

            for j in range(10):
                no = 10 * (i % self.numPerPage) + j
                self.savePictures(self.pictures[no],no)



# spider = TaobaoSpider()
# spider.getAddresses()
# for item in spider.dataAddr:
#     print item
# spider.getPage(0)
# for item in spider.pages:
#     print item
# spider.getPictures()
# for item in spider.pictures:
#     print item
