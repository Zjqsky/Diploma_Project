#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division, absolute_import

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from utils import readCsv,saveCsv


class AutoEnc_Tensor(object):
    def __init__(self,dataSet):
        # 参数
        self.learning_rate = 0.0000001  # 学习率
        self.training_epochs = 10  # 训练的周期100
        self.batch_size = 64  # 每一批次训练的大小32
        self.display_step = 1
        self.examples_to_show = 10

        # 神经网络的参数
        self.n_hidden_1 = 250  # 隐层1的神经元个数
        self.n_hidden_2 = 10  # 隐层2神经元个数
        self.n_input = 7500  # 数据集图像的输出(img shape: 50*50*3)
        self.dataSet = dataSet

        # tf Graph input (only pictures)
        self.X = tf.placeholder("float", [None, self.n_input])

        self.weights = {
            'encoder_h1': tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1])),
            'encoder_h2': tf.Variable(tf.random_normal([self.n_hidden_1, self.n_hidden_2])),
            'decoder_h1': tf.Variable(tf.random_normal([self.n_hidden_2, self.n_hidden_1])),
            'decoder_h2': tf.Variable(tf.random_normal([self.n_hidden_1, self.n_input])),
        }
        self.biases = {
            'encoder_b1': tf.Variable(tf.random_normal([self.n_hidden_1])),
            'encoder_b2': tf.Variable(tf.random_normal([self.n_hidden_2])),
            'decoder_b1': tf.Variable(tf.random_normal([self.n_hidden_1])),
            'decoder_b2': tf.Variable(tf.random_normal([self.n_input])),
        }

        self.sess = tf.InteractiveSession()
        # Construct model
        self.encoder_op = self.encoder(self.X)
        self.decoder_op = self.decoder(self.encoder_op)

    # Building the encoder
    def encoder(self,x):
        # Encoder Hidden layer with sigmoid activation #1
        layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, self.weights['encoder_h1']),
                                       self.biases['encoder_b1']))
        # layer_1 = tf.nn.relu(tf.add(tf.matmul(x, self.weights['encoder_h1']),
        #                                 self.biases['encoder_b1']))
        # layer_2 = tf.nn.relu(tf.add(tf.matmul(layer_1, self.weights['encoder_h2']),
        #                                 self.biases['encoder_b2']))
        # layer_1 = tf.nn.tanh(tf.add(tf.matmul(x, self.weights['encoder_h1']),
        #                                 self.biases['encoder_b1']))
        # layer_2 = tf.nn.tanh(tf.add(tf.matmul(layer_1, self.weights['encoder_h2']),
        #                                 self.biases['encoder_b2']))
        return layer_1

    # Building the decoder
    def decoder(self,x):
        # Decoder Hidden layer with sigmoid activation #2
        layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(x, self.weights['decoder_h2']),
                                       self.biases['decoder_b2']))
        # layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, self.weights['decoder_h1']),
        #                                self.biases['decoder_b1']))
        # # Decoder Hidden layer with sigmoid activation #2
        # layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, self.weights['decoder_h2']),
        #                                self.biases['decoder_b2']))
        # layer_1 = tf.nn.relu(tf.add(tf.matmul(x, self.weights['decoder_h1']),
        #                                 self.biases['decoder_b1']))
        # layer_2 = tf.nn.relu(tf.add(tf.matmul(layer_1, self.weights['decoder_h2']),
        #                                 self.biases['decoder_b2']))
        # layer_1 = tf.nn.tanh(tf.add(tf.matmul(x, self.weights['decoder_h1']),
        #                                 self.biases['decoder_b1']))
        # layer_2 = tf.nn.tanh(tf.add(tf.matmul(layer_1, self.weights['decoder_h2']),
        #                                 self.biases['decoder_b2']))
        return layer_2

    def train(self):
        # Prediction
        self.y_pred = self.decoder_op
        # Targets (Labels) are the input data.
        y_true = self.X

        # Define loss and optimizer, minimize the squared error
        epsilon = 10e-6
        cost = tf.reduce_mean(tf.pow(y_true - self.y_pred + epsilon, 2)**(1/2))
        """

        predictions=self.y_pred
        float_labels = tf.cast(y_true, tf.float32)
        cross_entropy_loss = float_labels * tf.log(predictions + epsilon) + (
                                                                                1 - float_labels) * tf.log(
            1 - predictions + epsilon)
        cross_entropy_loss = tf.negative(cross_entropy_loss)
        cost=tf.reduce_mean(tf.reduce_sum(cross_entropy_loss, 1))
        """
        optimizer = tf.train.RMSPropOptimizer(self.learning_rate).minimize(cost)

        # Initializing the variables
        init = tf.global_variables_initializer()

        # saver = tf.train.Saver()
        self.sess.run(init)

        costs = []
        total_batch = int(self.dataSet.shape[0] / self.batch_size)
        # Training cycle
        for epoch in range(self.training_epochs):
            # Loop over all batches
            for i in range(total_batch):
                batch_xs = self.dataSet[i*self.batch_size:(i+1)*self.batch_size]
                # Run optimization op (backprop) and cost op (to get loss value)
                _, c,p= self.sess.run([optimizer, cost,self.y_pred], feed_dict={self.X: batch_xs})
                # Display logs per epoch step
                if epoch % self.display_step == 0:
                    print "Epoch:%04d" % (epoch + 1), "batch:%04d" % (i +1),"cost=","{:.9f}".format(c)
                    val=[(epoch + 1),i,c]
                    costs.append(val)
        # saver.save(self.sess,'network/model/model.ckpt')
        heads = ['epoch', 'cost']
        # saveCsv(fileName="network/netCost.csv", heads=heads, datas=costs)

        print("Optimization Finished!")

    def test(self):
        saver = tf.train.Saver()
        saver.restore(self.sess, "network/model/model.ckpt")
        # Applying encode and decode over test set
        encode_decode = self.sess.run(
            self.decoder_op, feed_dict={self.X: self.dataSet[:self.examples_to_show]})
        # Compare original images with their reconstructions
        f, a = plt.subplots(2, 10, figsize=(10, 2))
        for i in range(self.examples_to_show):
            a[2][i].imshow(np.reshape(encode_decode[i], (50, 50,3)))
            a[3][i].imshow(np.reshape(encode_decode[i]-a[i], (50, 50, 3)))
        f.show()
        plt.draw()
        plt.show()

if __name__ == '__main__':
    print "reading data..."
    dataSet = readCsv("DataSetRawNoDb/data", 1000)
    model = AutoEnc_Tensor(dataSet=dataSet)
    a=model.train()
    # model.test()