#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from ImageDao import ImageDao

class KNearestNeighbor(object):
    def __init__(self):
        pass


    def train(self,trainSet):
        self.trainSet = trainSet


    def predictForOneWithK(self,input,k = 12):
        dists = np.sqrt(np.sum((input - self.trainSet) ** 2, axis=1))
        pred = np.argsort(dists)[:k]
        return pred

    def predictForOneWithDist(self,input,dist,minK=0):
        dists = np.sqrt(np.sum((input - self.trainSet) ** 2, axis=1))
        k = len(np.argwhere(dists < dist))
        if k < minK:
            k = minK
        pred = np.argsort(dists)[:k]
        return pred, k

    def predictForManyWithK(self,testSet,testLabel,k,typeDict):
        testNum = testSet.shape[0]

        dists = np.sqrt((testSet ** 2).sum(axis=1, keepdims=True)
                        + (self.trainSet ** 2).sum(axis=1)
                        - 2 * testSet.dot(self.trainSet.T))
        pred = np.argsort(dists,axis=1)[:,:k]

        typePred = np.empty_like(pred)
        for i in range(pred.shape[0]):
            for j in range(pred.shape[1]):
                typePred[i,j] = typeDict[str(pred[i,j]).zfill(5)]

        accuracy = np.mean(typePred == testLabel)
        avgCriDist = np.mean(dists[np.arange(testNum),pred[:,k-1]])

        return accuracy, avgCriDist

    def predictForManyWithDist(self,testSet,testBeginLabel,d,typeDict):
        dists = np.sqrt((testSet ** 2).sum(axis=1, keepdims=True)
                        + (self.trainSet ** 2).sum(axis=1)
                        - 2 * testSet.dot(self.trainSet.T))
        pred = np.where(dists < d)
        typePred = (np.empty_like(pred[0]),np.empty_like(pred[1]))
        for i,label in enumerate(pred[0]):
            typePred[0][i] = typeDict[str(label + testBeginLabel).zfill(5)]
        for i,label in enumerate(pred[1]):
            typePred[1][i] = typeDict[str(label).zfill(5)]


        avgK = float(len(pred[0])) / len(testSet)

        accuracy = np.mean(typePred[0] == typePred[1])

        return accuracy, avgK




