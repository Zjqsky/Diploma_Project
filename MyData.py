#!/usr/bin/python
# -*- coding: utf-8 -*-

from scipy.misc import imread, imsave, imresize
import csv
import numpy as np
from MyGaussianBlur import MyGaussianBlur
from PIL import Image, ImageFilter
import os
from ImageInfo import ImageInfo
from ImageDao import ImageDao
import shutil


class MyData:
    def __init__(self):
        self.rawPath = 'static/raw/'
        self.newPath = 'static/GaussianImg/'
        self.picWid = 50
        self.picLen = 50
        self.picturePerFile = 1000
        self.radius = 10

        pass

    def saveCsvWithGaussianBlur(self,srcBase = None, tarBase = None, radius = None):
        if not srcBase:
            srcBase = self.rawPath
        if not tarBase:
            tarBase = self.newPath
        if not radius:
            radius = self.radius

        files = os.listdir(srcBase)
        images = []
        gauImgPaths = []
        dao = ImageDao()

        shutil.rmtree(tarBase[:-1])
        os.mkdir(tarBase[:-1])
        for index,file in enumerate(files):
            fileName = os.path.splitext(file)[0]
            src = srcBase + file

            print "blur", index, "picture", src
            image = Image.open(src)
            image = image.filter(MyGaussianBlur(radius=radius))
            tar = tarBase + file
            image.save(tar)

            type = int(fileName) % 10
            image = ImageInfo(str(index).zfill(5),file,src,type)
            images.append(image)
            gauImgPaths.append(tar)

        dao.insertImg(images)

        images = []
        shutil.rmtree('DataSet')
        os.mkdir('DataSet')
        for index, newPath in enumerate(gauImgPaths):
            print "add", str(index), "picture", newPath
            img = self.loadImage(newPath)
            images.append(img)

            if len(images) == self.picturePerFile or index == (len(gauImgPaths) - 1):
                dataFileName = 'DataSet/data' + str(index / self.picturePerFile) + '.csv'
                np.savetxt(dataFileName, images, delimiter=',')
                images = []



    def loadImage(self, fileName):
        img = imread(fileName)
        img = imresize(img, (self.picWid, self.picLen))
        img = img.reshape(self.picWid * self.picLen * 3)
        img = img.astype("float")
        return img

    #不带高斯模糊保存csv
    def saveCsvBySrc(self,srcBase = None):
        if not srcBase:
            srcBase = self.rawPath

        files = os.listdir(srcBase)
        images = []
        imgPaths = []
        dao = ImageDao()

        for index,file in enumerate(files):
            fileName = os.path.splitext(file)
            src = srcBase + file
            type = int(fileName) % 10
            image = ImageInfo(str(index).zfill(5),file,src,type)
            images.append(image)
            imgPaths.append(src)

        dao.insertImg(images)

        images = []
        shutil.rmtree('DataSetRaw')
        os.mkdir('DataSetRaw')
        for index, newPath in enumerate(imgPaths):
            print "add " + str(index) + " picture " + newPath
            img = self.loadImage(newPath)
            images.append(img)

            if len(images) == self.picturePerFile or index == (len(imgPaths) - 1):
                dataFileName = 'DataSetRaw/data' + str(index / self.picturePerFile) + '.csv'
                np.savetxt(dataFileName, images, delimiter=',')
                images = []
    #不带高斯模糊不保存数据库
    def saveCsvBySrcNoDb(self,srcBase=None):
        if not srcBase:
            srcBase = self.rawPath

        files = os.listdir(srcBase)
        images = []
        shutil.rmtree('DataSetRawNoDb')
        os.mkdir('DataSetRawNoDb')
        for index, path in enumerate(files):
            path = srcBase + path
            print "add " + str(index) + " picture " + path
            img = self.loadImage(path)
            images.append(img)

            if len(images) == self.picturePerFile or index == (len(files) - 1):
                dataFileName = 'DataSetRawNoDb/data' + str(index / self.picturePerFile) + '.csv'
                np.savetxt(dataFileName, images, delimiter=',')
                images = []

    def saveCsvWithBlueAndSrc(self,srcBase = None, tarBase = None, radius = None):
        if not srcBase:
            srcBase = self.rawPath
        if not tarBase:
            tarBase = self.newPath
        if not radius:
            radius = self.radius

        files = os.listdir(srcBase)
        images = []
        gauImgPaths = []
        rawImagePaths = []
        dao = ImageDao()

        shutil.rmtree(tarBase[:-1])
        os.mkdir(tarBase[:-1])
        for index,file in enumerate(files):
            fileName = os.path.splitext(file)[0]
            src = srcBase + file
            rawImagePaths.append(src)

            print "blur", index, "picture", src
            image = Image.open(src)
            image = image.filter(MyGaussianBlur(radius=radius))
            tar = tarBase + file
            image.save(tar)

            type = int(fileName) % 10
            image = ImageInfo(str(index).zfill(5),file,src,type)
            images.append(image)
            gauImgPaths.append(tar)

        dao.insertImg(images)

        images = []
        shutil.rmtree('DataSet')
        os.mkdir('DataSet')
        for index, newPath in enumerate(gauImgPaths):
            print "add", str(index), "picture", newPath
            img = self.loadImage(newPath)
            images.append(img)

            if len(images) == self.picturePerFile or index == (len(gauImgPaths) - 1):
                dataFileName = 'DataSet/data' + str(index / self.picturePerFile) + '.csv'
                np.savetxt(dataFileName, images, delimiter=',')
                images = []

        images = []
        shutil.rmtree('DataSetRaw')
        os.mkdir('DataSetRaw')
        for index, path in enumerate(rawImagePaths):
            print "add " + str(index) + " picture " + path
            img = self.loadImage(path)
            images.append(img)

            if len(images) == self.picturePerFile or index == (len(files) - 1):
                dataFileName = 'DataSetRaw/data' + str(index / self.picturePerFile) + '.csv'
                np.savetxt(dataFileName, images, delimiter=',')
                images = []

if __name__ == '__main__':
    data = MyData()
    # data.saveCsvBySrc()

    # data.saveCsvWithGaussianBlur(radius=10)
    data.saveCsvBySrcNoDb()
    # data.saveCsvWithBlueAndSrc()