import numpy
from PIL import Image,ImageFilter
import os
import re

def open_img(giffile):
    img = Image.open(giffile)
    img = img.convert('RGB')
    pixdata = img.load()
    return img,pixdata

def remove_line(giffile,savepath):
    (img,pixdata) = open_img(giffile)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pixdata[x,y][0]<8 or pixdata[x,y][1]<6 or pixdata[x,y][2]<8 or (pixdata[x,y][0]+pixdata[x,y][1]+pixdata[x,y][2])<=30:
                if y==0:
                    pixdata[x, y] = (255, 255, 255)
                if y>0:
                    if pixdata[x, y-1][0] > 120 or pixdata[x, y-1][1] > 136 or pixdata[x, y-1][2] > 120:
                        pixdata[x,y] = (255,255,255)

    #二值化处理
    for y in range(img.size[1]):  # 二值化处理，这个阈值为R=95，G=95，B=95
        for x in range(img.size[0]):
            if pixdata[x, y][0] < 160 and pixdata[x, y][1] < 160 and pixdata[x, y][2] < 160:
                pixdata[x, y] = (0, 0, 0)
            else:
                pixdata[x, y] = (255, 255, 255)
    img.filter(ImageFilter.EDGE_ENHANCE_MORE)#边界加强(阀值更大)
    img.resize(((img.size[0])*2,(img.size[1])*2),Image.BILINEAR)#Image.BILINEAR指定采用双线性法对像素点插值
    img.save(savepath)


def getcoldocnum(giffile, openpath):
    (img, pixdata) = open_img(openpath + giffile)
    dot_num = numpy.zeros(img.size[0])  # 创建0矩阵
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pixdata[x, y][0] == 0:
                black_dot = 1
            else:
                black_dot = 0
            dot_num[x] = dot_num[x] + black_dot
    return dot_num

def pic_cut(giffile,openpath,savepath):
    (img, pixdata) = open_img(openpath+giffile)
    doc_num = getcoldocnum(giffile,openpath)
    #print(doc_num)
    i = 4
    k = 0
    flag=0
    picname=giffile.split('.')
    while(i):
        #print(i)
        if k+1>=100:
            break
        if (doc_num[k+1])**2-(doc_num[k])**2>=5:
            x1 = k
            for j in range(8,26):
                if x1+j+1>=100:
                    break
                t=doc_num[x1+j]
                if (doc_num[x1+j])==0 :
                    cut=x1+j
                    if (doc_num[x1 + j + 1]) ==0 and (doc_num[x1 + j + 2]) ==0:
                        x2 = x1+j

                        img.crop((x1, 0, x2, 20)).save(savepath+picname[0]+"_%d.gif" %(5-i))  # 适当的修改  crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
                        k = x2
                        break
                    elif (doc_num[x1+j+1]>0):
                        for back in range(1,9):
                            if doc_num[x1+j+back+1]==0:
                                x2 = x1 + j+back
                                img.crop((x1, 0, x2, 20)).save(savepath + picname[0] + "_%d.gif" % (5 - i))  # 适当的修改  crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
                                k = x2
                                flag=1
                                break

                        if flag==0:
                            x2 = x1 + j
                            img.crop((x1, 0, x2, 20)).save(savepath + picname[0] + "_%d.gif" % (5 - i))  # 适当的修改  crop函数带的参数为(起始点的横坐标，起始点的纵坐标，宽度，高度）
                            k = x2
                            break

            i = i-1
        else:
            k = k+1



if __name__=="__main__":
    '''
    #create removeline pic
    dirs='/Users/wc/Downloads/captcha_master/captchas/'
    file=[]
    for fr in os.listdir(dirs):
        f = dirs + fr
        if f.rfind(u'.DS_Store') == -1:
            file.append(f)
    #file=open("")
    for cap in file:
        oldname=re.compile("captchas")
        new=oldname.sub('removeline',cap)
        remove_line(cap,new)
    '''
    #create cut pic
    dirs = '/Users/wc/Downloads/captcha_master/removeline/'
    newdirs = '/Users/wc/Downloads/captcha_master/single/'
    file2 = []
    file3=[]
    for fr in os.listdir(dirs):
        f = dirs + fr
        if f.rfind(u'.DS_Store') == -1: #？
            p = re.compile(r'\d+')
            capname = p.findall(f)
            file2.append(capname[0]+'.gif')

    for cap in file2:
        pic_cut(cap,dirs,newdirs)

'''

   #测试
    dirs = '/Users/wc/Downloads/captcha_master/removeline/'
    testnewdirs = '/Users/wc/Downloads/captcha_master/test/'
    pic_cut('8.gif',dirs,testnewdirs)


'''