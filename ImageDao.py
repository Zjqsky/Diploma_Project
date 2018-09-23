#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
from ImageInfo import ImageInfo

class ImageDao:
    def __init__(self):
        print "connect mysql"
        self.conn = mysql.connector.connect(user='root', password='Zjqsky929',
                                            database='imgRetriDB')

    def __del__(self):
        self.conn.close()
        print "stop connect mysql"

    def insertImg(self,imgList):
        cursor = self.conn.cursor()

        sql = 'delete from image'
        cursor.execute(sql)
        self.conn.commit()

        sql = 'insert into image(imgId,imgName,imgUrl,imgType) values'
        for index, img in enumerate(imgList):
            sql += '("' + img.imgId + '","' + img.imgName + '","' + img.imgUrl + \
                   '",' + str(img.imgType) +')'
            if not index == (len(imgList) - 1):
                sql += ','
        cursor.execute(sql)
        count = cursor.rowcount
        self.conn.commit()

        cursor.close()
        return count

    def getImgCount(self):
        sql = 'select count(*) from image'
        cursor = self.conn.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def getTypeCount(self,type):
        sql = 'select count(*) from image where imgType = ' + str(type)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def getImageById(self,id):
        sql = 'select * from image where imgId = "' + id +'"'
        cursor = self.conn.cursor()
        cursor.execute(sql)
        img = cursor.fetchone()
        img = ImageInfo(img[0], img[1], img[2], img[3])
        cursor.close()
        return img

    def getImagesByIds(self,ids):
        sql = 'select * from image where imgId in ('
        for index, id in enumerate(ids):
            sql += '"'+ id +'"'
            if not index == (len(ids) - 1):
                sql += ","
        sql += ')'

        cursor = self.conn.cursor()
        cursor.execute(sql)
        imgDb = cursor.fetchall()

        imgs=[]
        for img in imgDb:
            imgs.append(ImageInfo(img[0], img[1], img[2], img[3]))

        cursor.close()
        return imgs

    def getAll(self):
        sql = 'select * from image'
        cursor = self.conn.cursor()
        cursor.execute(sql)
        imgDb = cursor.fetchall()

        imgs = []
        for img in imgDb:
            imgs.append(ImageInfo(img[0], img[1], img[2], img[3]))

        cursor.close()
        return imgs

    def insertImgTest(self):
        imgList = []
        img = ImageInfo("00001", "00001", "00001.jpg", 1)
        imgList.append(img)
        img = ImageInfo("00002", "00002", "00002.jpg", 2)
        imgList.append(img)
        self.insertImg(imgList)

    def getImagesByIdsTest(self):
        ids = []
        id = "00001"
        ids.append(id)
        id = "00002"
        ids.append(id)
        self.getImagesByIds(ids)


if __name__ == '__main__':
    dao = ImageDao()
    # dao.insertImgTest()
    dao.getImagesByIdsTest()

