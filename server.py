#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for, send_from_directory
from scipy.misc import imread, imsave, imresize
from KNearestNeighbor import KNearestNeighbor
from MyData import MyData
import numpy as np
import os
import time
from ImageDao import ImageDao
from PIL import Image
from MyGaussianBlur import MyGaussianBlur
from utils import readCsv

server = Flask(__name__)

print "initializing..."
imgBaseURL = "img/"
dataBaseUrl = "DataSet/"

upperK = 50
select = -1
k = 0

optimalDist = 2200
optimalLeastK = 12
dataNum = -1
radius = 10

print "reading data..."
data = MyData()
pictures = readCsv(dataBaseUrl + "data",dataNum)


print "training..."
knn = KNearestNeighbor()
knn.train(pictures)

dao = ImageDao()
imgs = dao.getAll()
typeDict = {}
for img in imgs:
    typeDict[img.imgId] = img.imgUrl

# server.config['UPLOAD_FOLDER'] = os.getcwd()

@server.route('/', methods=['GET', 'POST'])
def home():
    print "start..."
    pictureURL = url_for('static', filename = imgBaseURL + "empty.jpg")
    return render_template('main.html', picture = pictureURL, select = select,
                           k = k, upperK = upperK)

@server.route('/searchAction', methods=['GET','POST'])
def search_form():
    print "saving image..."
    picture = request.files['picture']
    select = int(request.form['select'])

    if not picture:
        pictureURL = url_for('static', filename=imgBaseURL + "empty.jpg")
        return render_template('main.html', picture=pictureURL, select=select,
                               k=0, upperK=upperK)
    rawFileName = time.strftime('%Y%m%d%H%M%S0', time.localtime(time.time())) + ".jpg"
    filePath = "static/" + imgBaseURL + rawFileName
    print picture.filename
    picture.save(filePath)

    image = Image.open(filePath)
    image = image.filter(MyGaussianBlur(radius=radius))
    newFileName = time.strftime('%Y%m%d%H%M%S1', time.localtime(time.time())) + ".jpg"
    filePath = "static/" + imgBaseURL + newFileName
    image.save(filePath)

    pictureURL = url_for('static', filename = imgBaseURL + rawFileName)

    print "loading image..."
    picArr = data.loadImage(filePath)

    print "predicting..."
    if select == -1:
        predict, k = knn.predictForOneWithDist(picArr, optimalDist,optimalLeastK)
    else:
        k = select
        predict = knn.predictForOneWithK(picArr,k)
    print predict

    ansList = []
    for id in predict:
        url = typeDict[str(id).zfill(5)]
        ansList.append(url)

    print "ok..."
    return render_template('main.html',picture = pictureURL, select = select,
                           ansList = ansList, k = k, upperK = upperK)


if __name__ == '__main__':
    server.run()