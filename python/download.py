import requests
from bs4 import BeautifulSoup
import time
from urllib.request import urlretrieve



i=101
kai=time.time()
print(time.ctime())
while i<=600:
    start=time.time()
    url_login = 'http://login.weibo.cn/login/'
    html = requests.get(url_login).content  # 解析网页
    soup = BeautifulSoup(html, 'lxml')
    code_img = str(soup.find('img'))[24:-3]  # 获取验证码图片地址
    mid=time.time()
    print(code_img,mid-start)
    urlretrieve(code_img, '//Users/wc/Downloads/captcha_master/captchas/%s.gif'%i)
    end=time.time()
    print(end-mid)
    i +=1
jieshu=time.time()
print(jieshu-kai,time.ctime())
