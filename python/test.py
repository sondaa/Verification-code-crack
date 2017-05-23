from PIL import Image,ImageFilter
img = Image.open(r'E:\大三文件\数字图像处理\1 大作业\captcha_master1\captcha_master\captchas\1.gif')  # 打开图片
img = img.convert('RGB')  # 转换为RGB图
pixdata = img.load()
img.show('pixdata')
img.show(pixdata)
