#!/usr/bin/env python
#coding:utf-8
import sys
from imp import reload
reload(sys)
#sys.setdefaultencoding('utf-8')
from numpy import *
import struct
from numpy import *
from covnet import *
import time


def net_train(train_covnet, cycle, case_num, learn_rate) :
    trainim_filepath = '../mnist/train-images-idx3-ubyte'
    trainlabel_filepath = '../mnist/train-labels-idx1-ubyte'
    trainimfile = open(trainim_filepath, 'rb')
    trainlabelfile = open(trainlabel_filepath, 'rb')
    train_im = trainimfile.read()
    train_label = trainlabelfile.read()
    im_index = 0
    label_index = 0
    magic, numImages , numRows , numColumns = struct.unpack_from('>IIII' , train_im , im_index)
    magic, numLabels = struct.unpack_from('>II', train_label, label_index)
    print ('train_set:'), numImages
    
    for c in range(cycle) :
        im_index = struct.calcsize('>IIII')
        label_index = struct.calcsize('>II')   
        for case in range(case_num) :
            im = struct.unpack_from('>784B', train_im, im_index)
            label = struct.unpack_from('>1B', train_label, label_index)
            im_index += struct.calcsize('>784B')
            label_index += struct.calcsize('>1B')
            im = array(im)
            im = im.reshape(28,28)
            bigim = [[-0.1] * 32] * 32
            for i in range(28) :
                for j in range(28) :
                    if im[i][j] > 0 :
                        bigim[i+2][j+2] = 1.175
            im = array([bigim])
            label = label[0]
            print (c, case, label)
            train_covnet.fw_prop(im, label)
            train_covnet.bw_prop(im, label, learn_rate[c])


def net_test(train_covnet, case_num) :
    trainim_filepath = '../mnist/train-images-idx3-ubyte'
    trainlabel_filepath = '../mnist/train-labels-idx1-ubyte'
    trainimfile = open(trainim_filepath, 'rb')
    trainlabelfile = open(trainlabel_filepath, 'rb')
    train_im = trainimfile.read()
    train_label = trainlabelfile.read()
    im_index = 0
    label_index = 0
    magic, numImages , numRows , numColumns = struct.unpack_from('>IIII' , train_im , im_index)
    magic, numLabels = struct.unpack_from('>II', train_label, label_index)

    im_index = struct.calcsize('>IIII')
    label_index = struct.calcsize('>II')

    correct_num = 0
    for case in range(case_num) :
        im = struct.unpack_from('>784B', train_im, im_index)
        label = struct.unpack_from('>1B', train_label, label_index)
        im_index += struct.calcsize('>784B')
        label_index += struct.calcsize('>1B')
        im = array(im)
        im = im.reshape(28,28)
        bigim = [[-0.1] * 32] * 32
        for i in range(28) :
            for j in range(28) :
                if im[i][j] > 0 :
                    bigim[i+2][j+2] = 1.175
        im = array([bigim])
        label = label[0]
        print (case, label)
        train_covnet.fw_prop(im)
        
        if argmax(train_covnet.outputlay7.maps[0][0]) == label :
            correct_num += 1
    correct_rate = correct_num / float(case_num)
    print ('test_correct_rate:', correct_rate)





