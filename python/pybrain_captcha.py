import numpy as np
import os
from pybrain.structure import *
from pybrain.structure.modules import SoftmaxLayer
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.validation import Validator
from pybrain.datasets import classification
from sklearn.externals import joblib
import time
import random

PKL='E:/大三文件/数字图像处理/1 大作业/captcha_master1/captcha_master/captcha_tanh.pkl'

def load_data():
    dataset=np.loadtxt('E:/大三文件/数字图像处理/1 大作业/captcha_master1/captcha_master/traindata/train_data.txt',delimiter=',')
    random.shuffle(dataset)
    return dataset

def loadPybrainData():
    dataset=load_data()
    row,col=dataset.shape
    global dimensions
    dimensions = col-1
    DS=classification.ClassificationDataSet(dimensions,nb_classes=14)
    X=dataset[:,:col-1]
    Y = dataset[:, col - 1:]
    for i in range(row):
        DS.addSample(X[i],Y[i])
    DS._convertToOneOfMany()
    return  DS

def buildNet():
    fnn = FeedForwardNetwork()
    inputLayer= LinearLayer(dimensions)
    firstHidden=TanhLayer(90)
    secondHidden=TanhLayer(80)
    outputLayer = SoftmaxLayer(14)

    fnn.addModule(BiasUnit(name='bias'))
    fnn.addInputModule(inputLayer)
    fnn.addModule(firstHidden)
    fnn.addModule(secondHidden)
    fnn.addOutputModule(outputLayer)

    in_to_hidden=FullConnection(inputLayer,firstHidden)
    first_to_second=FullConnection(firstHidden,secondHidden)
    hidden_to_out=FullConnection(secondHidden,outputLayer)

    fnn.addConnection(in_to_hidden)
    fnn.addConnection(first_to_second)
    fnn.addConnection(hidden_to_out)

    fnn.addConnection(FullConnection(fnn['bias'], inputLayer))
    fnn.addConnection(FullConnection(fnn['bias'], firstHidden))
    fnn.addConnection(FullConnection(fnn['bias'], secondHidden))
    fnn.addConnection(FullConnection(fnn['bias'], outputLayer))

    fnn.sortModules()
    return fnn

def train():
    DataTrain=loadPybrainData()
    fnn=buildNet()
    trainer=BackpropTrainer(fnn,dataset=DataTrain,momentum=0.05,verbose=True,weightdecay=0.005)
    trainer.trainUntilConvergence(maxEpochs=500)
    joblib.dump(fnn,PKL)
    return fnn

def dealoutput(out):
    output = 0
    for i, value in enumerate(out):
        if value == '1':
            output += 2 ** (5 - i)
    print(output)
    if output > 10:
        output = chr(output - 10 + ord('a'))
    else:output=str(output)
    return output

def predict():
    fnn=joblib.load(PKL)
    dir='E:/大三文件/数字图像处理/1 大作业/captcha_master1/captcha_master/worddata/'
    predictValue = []
    for fr in os.listdir(dir):
        dataset=[]
        f = dir + fr
        if f.rfind(u'.DS_Store') == -1 and f.rfind(u'Thumbs.db') == -1:
            data = np.loadtxt(f, delimiter=',')
            #data.reshape((1,2500))
            for item in data:
                dataset.append(int(item))

            #print(len(dataset))
            out = fnn.activate(dataset)
            out = out.argmax()
            iconset = ['3', 'c', 'd', 'e', 'f', 'h', 'j', 'k', 'l', 'm', 'n', 'w', 'x', 'y']
            for y, word in enumerate(iconset):
                if out == y:
                    print(word)
                    predictValue.append(word)

    print(u'验证码为%s' % (''.join(predictValue)))



def test():
    DS=loadPybrainData()
    train,test=DS.splitWithProportion(0.1)
    fnn=joblib.load(PKL)
    # 预测test情况
    output = fnn.activateOnDataset(test)
    # ann.activate(onedata)可以只对一个数据进行预测
    outputs=[]
    target=[]
    count=0
    for out in output:
        outs=out.argmax()
        outputs.append(outs)
    for tar in test['target']:
        ta=tar.argmax()
        target.append(ta)
    for i in range(0,len(target)):
        if outputs[i]==target[i]:
            count+=1

    right=count/len(target)#单个字符正确率
    rate=(right**4)
    print("分类正确率是：%.4f%%" % (rate * 100))
    v = Validator()
    print(u'均方和差为：',v.MSE(output, test['target']))#计算test的原始值和预测值的均方差和,两者格式必须相等

if __name__=='__main__':
    print(time.ctime())
    #fnn=train()
    #fnn = joblib.load(PKL)
    predict()

    test()
    print(time.ctime())
