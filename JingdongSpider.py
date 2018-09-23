#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
from scipy.misc import imread, imsave, imresize
import os
import shutil

# 抓取京东商品图片
class JingdongSpider:
    def __init__(self):
        self.dataAddr = []
        self.numPerPage = 30
        self.pageNum = 40
        self.basePath = 'static/raw/'
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' + \
                          ' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}



    # 从dataAddress中获取网址
    def getAddresses(self):
        self.dataAddr = []
        # with open('JD_dataAddress.txt', 'r') as f:
        #     while f.readline():
        #         self.dataAddr.append(f.readline())
        print "getting addresses!!!"

        addr = "https://search.jd.com/Search?keyword=%E7%8C%AA%E5%82%A8%E8%93%84%E7%BD%90&enc=utf-8&wq=%E7%8C%AA%E5%82%A8%E8%93%84%E7%BD%90&pvid=f285ea4a1fa249bb9d8a8ddde67b75a0"
        self.dataAddr.append(addr)
        addr = "https://search.jd.com/Search?keyword=%E7%91%9E%E5%A3%AB%E6%89%8B%E8%A1%A8&enc=utf-8&wq=%E7%91%9E%E5%A3%AB%E6%89%8B%E8%A1%A8&pvid=58a815cb324d4ad196d17c4d85e81eeb"
        self.dataAddr.append(addr)
        addr = "https://search.jd.com/Search?keyword=%E6%A3%89%E8%A2%84&enc=utf-8&wq=%E8%93%9D%E6%9C%88%E4%BA%AE&pvid=4587aaae0a7a4e2a9863b10268fbe3f1"
        self.dataAddr.append(addr)
        addr = "https://search.jd.com/Search?keyword=%E6%A8%A1%E5%9E%8B%E9%A3%9E%E6%9C%BA&enc=utf-8&wq=%E6%A8%A1%E5%9E%8B%E9%A3%9E%E6%9C%BA&pvid=98a98b7bbfcf46418e7122ddb6e99b6f"
        self.dataAddr.append(addr)
        addr = "https://search.jd.com/Search?keyword=%E5%B0%8F%E7%B1%B3%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E5%B0%8F%E7%B1%B3%E6%89%8B%E6%9C%BA&pvid=b12185a6c1d34471ac5eb9a1ae9580a5"
        self.dataAddr.append(addr)
        addr = "https://search.jd.com/Search?keyword=%E4%B9%A6%E5%8C%85%E9%98%BF%E8%BF%AA%E8%BE%BE%E6%96%AF&enc=utf-8&wq=%E5%B0%8F%E7%B1%B36&pvid=8de86c29eb3c46bb9d13aa349d55c24d"
        self.dataAddr.append(addr)
        addr = "https://search.jd.com/Search?keyword=%E4%B9%A6%E6%9E%B6&enc=utf-8&wq=%E4%B9%A6%E6%9E%B6&pvid=92c27af2de2d40b4bf7c1f368f5ed2dc"
        self.dataAddr.append(addr)
        addr = "https://search.jd.com/Search?keyword=%E7%BE%BD%E6%AF%9B%E7%90%83%E6%8B%8D&enc=utf-8&wq=%E7%BE%BD%E6%AF%9B%E7%90%83%E6%8B%8D&pvid=68d1d14499314af1b0d5dc01c4f74e40"
        self.dataAddr.append(addr)
        addr = "https://search.jd.com/Search?keyword=%E8%BF%90%E5%8A%A8%E8%A3%A4&enc=utf-8&wq=%E8%BF%90%E5%8A%A8%E8%A3%A4&pvid=59e8aba3b1654c34acf2b961f04f3880"
        self.dataAddr.append(addr)
        addr = "https://search.jd.com/Search?keyword=%E8%BF%90%E5%8A%A8%E9%9E%8B&enc=utf-8&wq=%E8%BF%90%E5%8A%A8%E9%9E%8B&pvid=fe25b3f12f4e499a92b79274a722fa2a"
        self.dataAddr.append(addr)

        for addr in self.dataAddr:
            print addr



    def getPage(self,address,pageIndex):
        print "getting pages no." + str(pageIndex) + "!!!"

        addr = address + "&page=" + str(2 * pageIndex + 1) + "&s=" +\
              str(self.numPerPage * pageIndex + 1) + "&click=0"

        request = urllib2.Request(addr,headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read()

    def getPictures(self,page):
        print "getting pictures!!!"

        pattern = re.compile('class="gl-item.*?<div class="gl-i-wrap.*?<div class="p-img.*?' +
                             '<a target="_blank.*?<img width=.*?(src|data-lazy-img)="(.*?)"', re.S)
        datas = re.findall(pattern, page)

        urls = []
        for data in datas:
            urls.append(data[1])

        return urls

    def savePictures(self,imageURL,imgName):
        u = urllib.urlopen("https:" + imageURL)
        data = u.read()
        fileName = self.basePath + imgName + '.jpg'
        f = open(fileName, 'wb')
        f.write(data)
        print u"正在保存图片", fileName
        f.close()

        data = imread(fileName)
        if len(data.shape) == 3 and data.shape[2] == 3:
            return True
        else:
            os.remove(fileName)
            return False



    def spider(self):
        shutil.rmtree(self.basePath[:-1])
        os.mkdir(self.basePath[:-1])
        self.getAddresses()

        for type,address in enumerate(self.dataAddr):
            num = 0
            for pageIndex in range(40):
                page = self.getPage(address,pageIndex)
                urls = self.getPictures(page)
                if len(urls) == 0:
                    break
                else:
                    for url in urls:
                        no = num * 10 + type
                        if self.savePictures(url,str(no).zfill(5)):
                            num = num + 1


spider = JingdongSpider()
spider.spider()