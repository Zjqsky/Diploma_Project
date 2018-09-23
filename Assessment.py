#!/usr/bin/python
# -*- coding: utf-8 -*-

from KNearestNeighbor import KNearestNeighbor
from MyData import MyData
import numpy as np
import os
import time
from ImageDao import ImageDao
from utils import saveCsv,readCsv

class Assessment(object):
    def __init__(self):
        self.trainNum = 5000
        self.testNum = 1000
        self.dataBaseUrl = "DataSet/"
        self.resultBasePath = "Assessment/"
        self.totalNum = self.trainNum + self.testNum
        self.knn = KNearestNeighbor()
        self.k = 12

        pass



    def assess(self,k = None):
        if not k:
            k = self.k
        print "reading data..."
        pictures = readCsv(self.dataBaseUrl + "data", self.totalNum)

        dao = ImageDao()
        imgs = dao.getAll()
        typeDict = {}
        for img in imgs:
            typeDict[img.imgId] = img.imgType

        print "training..."
        trainSet = pictures[:self.trainNum]
        self.knn.train(trainSet)

        testSet = pictures[self.trainNum : self.totalNum]

        zerNp = np.zeros([k, self.testNum])
        testLabel = np.arange(self.trainNum,self.totalNum)
        for i in range(len(testLabel)):
            testLabel[i] = typeDict[str(testLabel[i]).zfill(5)]
        testLabel = (zerNp + testLabel).astype('int').T

        print "predicting..."
        accuracy,avgCriDist = self.knn.predictForManyWithK(testSet,testLabel,k,typeDict)

        print "accuracy:%f%%       averageCriticalDist:%f" % (accuracy * 100,avgCriDist)


    def assessWithoutK(self):
        print "reading data..."
        pictures = readCsv(self.dataBaseUrl + "data", self.totalNum)

        dao = ImageDao()
        imgs = dao.getAll()
        typeDict = {}
        for img in imgs:
            typeDict[img.imgId] = img.imgType

        print "training..."
        trainSet = pictures[:self.trainNum]
        self.knn.train(trainSet)

        testSet = pictures[self.trainNum: self.totalNum]

        accuracyList = []
        heads = ['k','accuracy','averageCriticalDist']

        print "predicting..."
        for k in range(1,101):
            zerNp = np.zeros([k, self.testNum])
            testLabel = np.arange(self.trainNum, self.totalNum)
            for i in range(len(testLabel)):
                testLabel[i] = typeDict[str(testLabel[i]).zfill(5)]
            testLabel = (zerNp + testLabel).astype('int').T

            accuracy,avgCriDist = self.knn.predictForManyWithK(testSet, testLabel, k, typeDict)

            item = [k,accuracy,avgCriDist]
            accuracyList.append(item)

            print "k:%d     accuracy:%f%%       averageCriticalDist:%f" % (k,accuracy * 100,avgCriDist)

        saveCsv(self.resultBasePath + 'assessKWithoutBlur.csv',heads,accuracyList)

    def assessWithoutDist(self):
        print "reading data..."
        pictures = readCsv(self.dataBaseUrl + "data", self.totalNum)

        dao = ImageDao()
        imgs = dao.getAll()
        typeDict = {}
        for img in imgs:
            typeDict[img.imgId] = img.imgType

        print "training..."
        trainSet = pictures[:self.trainNum]
        self.knn.train(trainSet)

        testSet = pictures[self.trainNum: self.totalNum]

        accuracyList = []
        heads = ['distance', 'accuracy', 'averageK']

        print "predicting..."
        for d in range(2000, 4000, 20):
            accuracy, avgK = self.knn.predictForManyWithDist(testSet, self.trainNum, d, typeDict)

            item = [d, accuracy, avgK]
            accuracyList.append(item)

            print "distance:%d     accuracy:%f%%       averageK:%f" % (d, accuracy * 100, avgK)

        saveCsv(self.resultBasePath + 'assessDist_Radius10_5000-1000.csv', heads, accuracyList)

    def assessWithoutRadius(self,k = None):
        if not k:
            k = self.k
        accuracyList = []
        heads = ['radius', 'accuracy', 'averageCriticalDist']

        for radius in range(5,15):
            print radius,':'
            print "blurring ..."
            data=MyData()
            data.saveCsvWithGaussianBlur(radius=radius)

            dao = ImageDao()
            imgs = dao.getAll()
            typeDict = {}
            for img in imgs:
                typeDict[img.imgId] = img.imgType

            zerNp = np.zeros([k, self.testNum])
            testLabel = np.arange(self.trainNum, self.totalNum)
            for i in range(len(testLabel)):
                testLabel[i] = typeDict[str(testLabel[i]).zfill(5)]
            testLabel = (zerNp + testLabel).astype('int').T

            pictures = readCsv(self.dataBaseUrl + "data", self.totalNum)

            print "training..."
            trainSet = pictures[:self.trainNum]
            self.knn.train(trainSet)

            testSet = pictures[self.trainNum: self.totalNum]

            print "predicting..."
            accuracy, avgCriDist = self.knn.predictForManyWithK(testSet, testLabel, k, typeDict)

            item = [radius,accuracy,avgCriDist]
            accuracyList.append(item)

            print "k:%d     radius:%f    accuracy:%f%%   averageCriticalDist:%f" % (k,radius,accuracy * 100, avgCriDist)

        saveCsv(self.resultBasePath + 'assessRadiusK' + str(k) + '.csv', heads, accuracyList)

    def assessWithoutRadiusAndK(self):
        accuracyList = []
        heads = ['radius', 'k', 'accuracy', 'averageCriticalDist']

        for radius in range(15,25):
            print radius,':'
            print "blurring ..."
            data=MyData()
            data.saveCsvWithGaussianBlur(radius=radius)

            dao = ImageDao()
            imgs = dao.getAll()
            typeDict = {}
            for img in imgs:
                typeDict[img.imgId] = img.imgType

            pictures = readCsv(self.dataBaseUrl + "data", self.totalNum)

            print "training..."
            trainSet = pictures[:self.trainNum]
            self.knn.train(trainSet)

            testSet = pictures[self.trainNum: self.totalNum]

            for k in range(5,20):
                zerNp = np.zeros([k, self.testNum])
                testLabel = np.arange(self.trainNum, self.totalNum)
                for i in range(len(testLabel)):
                    testLabel[i] = typeDict[str(testLabel[i]).zfill(5)]
                testLabel = (zerNp + testLabel).astype('int').T

                print "predicting..."
                accuracy, avgCriDist = self.knn.predictForManyWithK(testSet, testLabel, k, typeDict)

                item = [radius, k, accuracy, avgCriDist]
                accuracyList.append(item)

                print "radius:%f    k:%d     accuracy:%f%%   averageCriticalDist:%f" % \
                      (radius, k, accuracy * 100, avgCriDist)

        saveCsv(self.resultBasePath + 'assessRadius15-25AndK.csv', heads, accuracyList)

    def assessFeaWithoutK(self):
        print "reading data..."
        pictures = readCsv(self.dataBaseUrl + "netFea", self.totalNum)*256*40

        dao = ImageDao()
        imgs = dao.getAll()
        typeDict = {}
        for img in imgs:
            typeDict[img.imgId] = img.imgType

        print "training..."
        trainSet = pictures[:self.trainNum]
        self.knn.train(trainSet)

        testSet = pictures[self.trainNum: self.totalNum]

        accuracyList = []
        heads = ['k','accuracy','averageCriticalDist']

        print "predicting..."
        for k in range(1,101):
            zerNp = np.zeros([k, self.testNum])
            testLabel = np.arange(self.trainNum, self.totalNum)
            for i in range(len(testLabel)):
                testLabel[i] = typeDict[str(testLabel[i]).zfill(5)]
            testLabel = (zerNp + testLabel).astype('int').T

            accuracy,avgCriDist = self.knn.predictForManyWithK(testSet, testLabel, k, typeDict)

            item = [k,accuracy,avgCriDist]
            accuracyList.append(item)

            print "k:%d     accuracy:%f%%       averageCriticalDist:%f" % (k,accuracy * 100,avgCriDist)

        saveCsv(self.resultBasePath + 'assessFeaWithoutK.csv',heads,accuracyList)

    def assessFeaWithBlurWithoutK(self):
        print "reading neaFeaData..."
        netFea = readCsv(self.dataBaseUrl + "netFea", self.totalNum)*256*40
        print "reading data..."
        pictures = readCsv(self.dataBaseUrl + "data", self.totalNum)
        pictures = np.append(pictures,netFea,axis=1)
        print pictures.shape
        dao = ImageDao()
        imgs = dao.getAll()
        typeDict = {}
        for img in imgs:
            typeDict[img.imgId] = img.imgType

        print "training..."
        trainSet = pictures[:self.trainNum]
        self.knn.train(trainSet)

        testSet = pictures[self.trainNum: self.totalNum]

        accuracyList = []
        heads = ['k','accuracy','averageCriticalDist']

        print "predicting..."
        for k in range(1,101):
            zerNp = np.zeros([k, self.testNum])
            testLabel = np.arange(self.trainNum, self.totalNum)
            for i in range(len(testLabel)):
                testLabel[i] = typeDict[str(testLabel[i]).zfill(5)]
            testLabel = (zerNp + testLabel).astype('int').T

            accuracy,avgCriDist = self.knn.predictForManyWithK(testSet, testLabel, k, typeDict)

            item = [k,accuracy,avgCriDist]
            accuracyList.append(item)

            print "k:%d     accuracy:%f%%       averageCriticalDist:%f" % (k,accuracy * 100,avgCriDist)

        saveCsv(self.resultBasePath + 'assessFeaWithBlurWithoutK.csv',heads,accuracyList)

if __name__ == '__main__':
    # k=12
    # Assessment().assess(k)

    # Assessment().assessWithoutK()

    # Assessment().assessWithoutDist()

    # for k in range(5,20):
    #     Assessment().assessWithoutRadius(k)

    # assess = Assessment()
    # assess.assessWithoutRadiusAndK()
    Assessment().assessFeaWithoutK()
