from PIL import Image
import os
import random


def getbp(im):
    img = Image.open(im)
    img = img.convert('RGB')
    pixdata = img.load()
    binpx=[]
    if img.size[0]>26:#防止截取的字符过长
        img.size[0]=25
    for x in range(img.size[0]):
        for y in range(img.size[1]):

            if pixdata[x,y]==(255,255,255):
                binpx.append(1)
            else:binpx.append(0)
    return binpx,img.size[0]





def getf(dirs):
    fs = []
    for fr in os.listdir(dirs):
        f = dirs + fr
        if f.rfind(u'.DS_Store')==-1 and f.rfind(u'Thumbs.db')==-1: #?
            fs.append(f)
    return fs

def writef(content):
    with open('E:/大三文件/数字图像处理/1 大作业/captcha_master1/captcha_master/traindata/train_data.txt','a+') as f:
        f.write(content)
        f.write('\n')
        f.close()




def GetSingleData():
    dirs='E:/大三文件/数字图像处理/1 大作业/captcha_master1/captcha_master/word/'
    num=1
    for f in getf(dirs):
        pixs, col = getbp(f)
        for row in range(20):
            for j in range(1, 26 - col):
                pixs.append(1)
        pixs = [str(i) for i in pixs]
        # print(len(pixs))
        content = ','.join(pixs)
        with open('E:/大三文件/数字图像处理/1 大作业/captcha_master1/captcha_master/worddata/word_%s_data.txt'%num, 'a+') as f:
            f.write(content)
            f.write('\n')
            f.close()
        num += 1

if __name__=='__main__':
    dirs='E:/大三文件/数字图像处理/1 大作业/captcha_master1/captcha_master/singlecap/%s/'
    iconset = ['3','c','d','e','f','h','j','k','l','m','n','w','x','y']
    for num,i in enumerate(iconset):
        for f in getf(dirs%(i)):
            pixs,col=getbp(f)
            for row in range(20):
                for j in range(1,26-col):
                    pixs.append(1)
            #pixs.append('a')
            pixs.append(num)

            pixs=[str(i) for i in pixs ]
            print(len(pixs))
            #random.shuffle(pixs)
            content = ','.join(pixs)
            writef(content)