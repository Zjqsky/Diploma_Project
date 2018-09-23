#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import timeit

import numpy

import theano
import theano.tensor as T

from utils import tile_raster_images,saveCsv,readCsv


try:
    import PIL.Image as Image
except ImportError:
    import Image

'''代码编写参考文献：Contractive Auto-Encoder class
这篇文献主要是提出一个约束正则项
整个总计算过程，参考文献的公式：7'''


class AutoEnc_Theano(object):
    def __init__(self, numpy_rng, input=None, n_visible=None, n_hidden=None,
                 n_batchsize=None, W=None, bhid=None, bvis=None):
        """
        input:输入训练数据数据， input与n_batchsize是对应的，input中有n_batchsize个样本
        input每一行代表一个样本，共有n_batchsize个样本

        n_visible:可见层神经元的个数

        n_hidden: 隐藏层神经元个数

        n_batchsize:批量训练，每批数据的个数

        W:输入当隐藏层的全连接权值矩阵，因为使用了tied weight 所以从隐藏到输入的权值
        矩阵为:W.transpose()

        bhid:从输入到隐藏层的偏置单元

        bvis:从隐藏层的偏置单元
        """
        self.n_visible = n_visible
        self.n_hidden = n_hidden
        self.n_batchsize = n_batchsize
        # 如果没有输入W，则在类里面进行初始化
        if not W:
            '''W 采用[-a,a]的均匀采样方法进行初始化，因为后面采用s函数，所以
           a=4*sqrt(6./(n_visible+n_hidden)) ,矩阵类型theano.config.floatX
           这样才能保证在GPU上运行'''
            initial_W = numpy.asarray(
                numpy_rng.uniform(
                    low=-4 * numpy.sqrt(6. / (n_hidden + n_visible)),
                    high=4 * numpy.sqrt(6. / (n_hidden + n_visible)),
                    size=(n_visible, n_hidden)
                ),
                dtype=theano.config.floatX
            )
            W = theano.shared(value=initial_W, name='W', borrow=True)

        if not bvis:
            bvis = theano.shared(value=numpy.zeros(n_visible,
                                                   dtype=theano.config.floatX),
                                 borrow=True)

        if not bhid:
            bhid = theano.shared(value=numpy.zeros(n_hidden,
                                                   dtype=theano.config.floatX),
                                 name='b',
                                 borrow=True)

        self.W = W
        # 输入到隐藏的偏置单元
        self.b = bhid
        # 隐藏到输出的偏置单元
        self.b_prime = bvis
        # 使用了tied weights, 所以 W_prime 是 W 的转置
        self.W_prime = self.W.T

        # 如果没有给定input，那么创建一个
        if input is None:
            self.x = T.dmatrix(name='input')
        else:
            self.x = input

        self.params = [self.W, self.b, self.b_prime]

    # 1、输入层到隐藏层
    def get_hidden_values(self, input):
        return T.nnet.sigmoid(T.dot(input, self.W) + self.b)

    # 2、隐藏层到输出层。重建结果 x' = s(W' h  + b') ，因为文献使用了tied weigth，所以
    # W'等于W的转置，这个可以百度搜索：自编码，tied weight等关键词
    def get_reconstructed_input(self, hidden):
        return T.nnet.sigmoid(T.dot(hidden, self.W_prime) + self.b_prime)

    # 计算 J_i = h_i (1 - h_i) * W_i
    def get_jacobian(self, hidden, W):
        return T.reshape(hidden * (1 - hidden), (self.n_batchsize, 1, self.n_hidden)) * T.reshape(W, (
        1, self.n_visible, self.n_hidden))

    # 权值更新函数
    def get_cost_updates(self, contraction_level, learning_rate):
        y = self.get_hidden_values(self.x)  # 输入-》隐藏
        z = self.get_reconstructed_input(y)  # 隐藏-》输出
        J = self.get_jacobian(y, self.W)  # y*(1-y)*W
        # 文献Contractive Auto-Encoders:公式4损失函数计算公式
        self.L_rec = - T.sum(self.x * T.log(z) + (1 - self.x) * T.log(1 - z), axis=1)

        # 因为J是由n_batchsize*n_hidden计算而来，有n_batchsize个样本，所以要求取样本平均值
        self.L_jacob = T.sum(J ** 2) / self.n_batchsize

        # 整个惩罚函数
        cost = T.mean(self.L_rec) + contraction_level * T.mean(self.L_jacob)

        # 对参数求导
        gparams = T.grad(cost, self.params)
        # 梯度下降法更新参数
        updates = []
        for param, gparam in zip(self.params, gparams):
            updates.append((param, param - learning_rate * gparam))

        return (cost, updates)


# 测试验证上面的类是否正确
def test_cA(train_set_x, n_hidden=None,
        learning_rate=0.01, training_epochs=20,
        batch_size=10, output_folder='network', contraction_level=.1):
    """
    learning_rate:梯度下降法的学习率

    training_epochs: 最大迭代次数

    contraction_level：为正则项的权重

    """


    # 批量下降法，训练的批数
    n_train_batches = train_set_x.shape[0] / batch_size

    # allocate symbolic variables for the data
    index = T.lscalar()  # 每一批训练数据的索引
    x = T.matrix('x')  # 每一批训练数据

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
    os.chdir(output_folder)

    rng = numpy.random.RandomState(123)

    ca = AutoEnc_Theano(numpy_rng=rng, input=x,
            n_visible=50* 50 * 3, n_hidden=n_hidden, n_batchsize=batch_size)

    cost, updates = ca.get_cost_updates(contraction_level=contraction_level,
                                        learning_rate=learning_rate)
    # 每一批，训练更新函数，输入参数index
    train_ca = theano.function(
        [index],
        [T.mean(ca.L_rec), ca.L_jacob],
        updates=updates,
        givens={
            x: train_set_x[index * batch_size: (index + 1) * batch_size]
        }
    )

    start_time = timeit.default_timer()

    ############
    # TRAINING #
    ############

    costs = []
    # go through training epochs
    for epoch in xrange(training_epochs):
        # go through trainng set
        c = []
        for batch_index in xrange(n_train_batches):
            print 'epoch:%d    batch_index:%d'%(epoch,batch_index)
            c.append(train_ca(batch_index))

        c_array = numpy.vstack(c)
        cost = [epoch,numpy.mean(c_array[0]),numpy.mean(numpy.sqrt(c_array[1]))]
        costs.append(cost)
        print 'Training epoch %d, reconstruction cost ' % cost[0], numpy.mean(
            cost[1]), ' jacobian norm ', cost[2]

    heads=['epoch','cost','jacobian']
    saveCsv(fileName="layer_1Cost.csv",heads=heads,datas=costs)

    end_time = timeit.default_timer()

    training_time = (end_time - start_time)

    print >> sys.stderr, ('The code for file ' + os.path.split(__file__)[1] +
                          ' ran for %.2fm' % ((training_time) / 60.))

    image = Image.fromarray(tile_raster_images(
        X=ca.W.get_value(borrow=True).T,
        img_shape=(50, 50 * 3), tile_shape=(10, 10),
        tile_spacing=(1, 1)))

    image.save('cae_filters.png')
    numpy.savetxt('layer_1W.csv', ca.W.get_value(borrow=True), delimiter=',')
    os.chdir('../')


if __name__ == '__main__':
    print "reading data..."
    train_set_x = readCsv("DataSetRaw/data", 1000)
    test_cA(train_set_x=train_set_x,n_hidden=100)