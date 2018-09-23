#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for, send_from_directory
from scipy.misc import imread, imsave, imresize
from KNearestNeighbor import KNearestNeighbor
from MyData import MyData
import numpy as np
import os
import time

server = Flask(__name__)

print "initializing..."
imgBaseURL = "static/img/"
pictureBaseURL = "JD_picture/"
k = 12

# print "reading data..."
# data = MyData()
# pictures = data.readCsv("data.csv")

# print "training..."
# knn = KNearestNeighbor()
# knn.train(pictures)

# server.config['UPLOAD_FOLDER'] = os.getcwd()

@server.route('/', methods=['GET', 'POST'])
def home():
    print "start..."
    pictureURL = url_for('static', filename="img/empty.jpg", _external=True)
    return render_template('main.html', picture=pictureURL, k=0)

@server.route('/searchAction', methods=['GET','POST'])
def search_form():
    print "saving image..."
    picture = request.files['picture']
    filePath = os.path.join(imgBaseURL, "search.jpg")
    print picture.filename
    picture.save(filePath)
    time.sleep(3)

    pictureURL = url_for('static', filename="img/search.jpg", _external=True)

    # print "loading image..."
    # picArr = data.loadImage(filePath)

    # print "predicting..."
    # predict = knn.predict(picArr,k)
    # print predict

    ansList = []
    # for pos in predict:
    #     url = pictureBaseURL + str(pos) + ".jpg"
    #     ansURL = url_for('static', filename=url)
    #     ansList.append(ansURL)

    print "ok..."
    print pictureURL
    return render_template('main.html',picture = pictureURL, ansList = ansList, k=0)


if __name__ == '__main__':
    server.run()