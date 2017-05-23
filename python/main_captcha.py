from urllib.request import urlretrieve
import numpy
from lxml import etree
from PIL import Image,ImageFilter
import requests
from bs4 import BeautifulSoup
import train
import os
import re
import pybrain_captcha
#import test2

def open_img(giffile):
    img = Image.open(giffile)   #打开图片
    img = img.convert('RGB')    #转换为RGB图
    pixdata = img.load()        #转换为像素点图
    return img, pixdata


def remove_line(giffile, savepath):
    (img, pixdata) = open_img(giffile)
    for x in range(img.size[0]):    #x坐标
        for y in range(img.size[1]):    #y坐标
            if pixdata[x, y][0] < 8 or pixdata[x, y][1] < 6 or pixdata[x, y][2] < 8 or (
                    pixdata[x, y][0] + pixdata[x, y][1] + pixdata[x, y][2]) <= 30:  #确定颜色阈值
                if y == 0:
                    pixdata[x, y] = (255, 255, 255)
                if y > 0:
                    if pixdata[x, y - 1][0] > 120 or pixdata[x, y - 1][1] > 136 or pixdata[x, y - 1][2] > 120:
                        pixdata[x, y] = (255, 255, 255) #?

    # 二值化处理
    for y in range(img.size[1]):  # 二值化处理，这个阈值为R=95，G=95，B=95
        for x in range(img.size[0]):
            if pixdata[x, y][0] < 160 and pixdata[x, y][1] < 160 and pixdata[x, y][2] < 160:
                pixdata[x, y] = (0, 0, 0)
            else:
                pixdata[x, y] = (255, 255, 255)
    img.filter(ImageFilter.EDGE_ENHANCE_MORE)  #深度边缘增强滤波，会使得图像中边缘部分更加明显（阈值更大），相当于锐化滤波
    img.resize(((img.size[0]) * 2, (img.size[1]) * 2), Image.BILINEAR)  # Image.BILINEAR指定采用双线性法对像素点插值#?
    img.save(savepath+'captcha_removeline.gif')

#计算每一列的黑色像素总数，并且将总数记录在dot_num中
def get_coldocnum(giffile, openpath):
    (img, pixdata) = open_img(openpath + giffile)
    dot_num = numpy.zeros(img.size[0])  # 创建0矩阵（一维）
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pixdata[x, y][0] == 0:
                black_dot = 1
            else:
                black_dot = 0
            dot_num[x] = dot_num[x] + black_dot
    return dot_num

#图像切割(纵向)
def pic_cut(giffile, openpath, savepath):
    (img, pixdata) = open_img(openpath + giffile)
    doc_num = get_coldocnum(giffile, openpath)
    # print(doc_num)
    i = 4
    k = 0
    flag = 0
    picname = giffile.split('.')#遇到'.'便分割
    while (i):
        # print(i)
        if k + 1 >= 100:
            break
        if (doc_num[k + 1]) ** 2 - (doc_num[k]) ** 2 >= 5:  #用后一列像素和的平方建当前列像素和的平方，初步判断每个单词开头
            x1 = k  #x1为单词开头坐标
            for j in range(8, 26):  #大概的单词像素宽度范围
                if x1 + j + 1 >= 100:
                    break
                t = doc_num[x1 + j]
                if (doc_num[x1 + j]) == 0:
                    cut = x1 + j
                    if (doc_num[x1 + j + 1]) == 0 and (doc_num[x1 + j + 2]) == 0:   #若cut后两列都没像素
                        x2 = x1 + j #x2为单词末尾坐标

                        img.crop((x1, 0, x2, 20)).save(
                            savepath + picname[0] + "_%d.gif" % (5 - i))  # 剪裁  crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
                        k = x2
                        break
                    elif (doc_num[x1 + j + 1] > 0): #切割两个几乎相黏的单词或者一个单词中有断点
                        for back in range(1, 9):
                            if doc_num[x1 + j + back + 1] == 0:    #若有断点
                                x2 = x1 + j + back
                                img.crop((x1, 0, x2, 20)).save(savepath + picname[0] + "_%d.gif" % (
                                5 - i))  # 剪裁  crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
                                k = x2
                                flag = 1
                                break

                        if flag == 0:   #几乎相黏的单词
                            x2 = x1 + j
                            img.crop((x1, 0, x2, 20)).save(savepath + picname[0] + "_%d.gif" % (
                            5 - i))  # 剪裁  crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
                            k = x2
                            break

            i = i - 1
        else:
            k = k + 1

def show_img(giffile):
    img=Image.open(giffile)
    img = img.convert('RGB')
    img.show()

def read_captcha():
    header={
        'User-Agent':'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Host':'login.weibo.cn'
    }
    url_login = 'http://login.weibo.cn/login/'
    html = requests.get(url_login,headers=header).content  # 解析网页
    soup = BeautifulSoup(html, 'lxml')
    code_img = str(soup.find('img'))[24:-3]  # 获取验证码图片地址
    print(code_img)
    urlretrieve(code_img, r'E:\大三文件\数字图像处理\1 大作业\captcha_master1\captcha_master\main_captcha\captcha.gif')
    show_img(r'E:\大三文件\数字图像处理\1 大作业\captcha_master1\captcha_master\main_captcha\captcha.gif')
    remove_line(r'E:\大三文件\数字图像处理\1 大作业\captcha_master1\captcha_master\main_captcha\captcha.gif',
                r'E:\大三文件\数字图像处理\1 大作业\captcha_master1\captcha_master\main_captcha/')
    pic_cut('captcha_removeline.gif', 'E:/大三文件/数字图像处理/1 大作业/captcha_master1/captcha_master/main_captcha/',
            'E:/大三文件/数字图像处理/1 大作业/captcha_master1/captcha_master/word/')

def delete_txt():
    filename = r'E:/大三文件/数字图像处理/1 大作业/captcha_master1/captcha_master/worddata/word_%s_data.txt'
    for i in range(1,5):
        if os.path.exists(filename%(i)):

            #print('a')
            os.remove(filename%(i))
if __name__=='__main__':
    delete_txt()
    read_captcha()
    train.GetSingleData()
    pybrain_captcha.predict()
    pybrain_captcha.test()
