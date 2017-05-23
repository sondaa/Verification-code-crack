# Verification-code-crack
### 基于Python对新浪登录验证码的自动识别
- 系统功能:

	抓取网页上的验证码，对验证码图片进行去噪，二值化，分割，再利用神经网络的技术实现对验证码的识别。
- 主要技术:

	Python编程，利用PIL，numpy，pybrain
- 主要步骤:

  1.  抓取微博验证码，并保存在captchas文件夹中（600张样本）:<br>
  图片地址：
  ![](https://github.com/weixianglin/Verification-code-crack/blob/master/picdoc/1.png)<br>
  主要代码：
  ![](https://github.com/weixianglin/Verification-code-crack/blob/master/picdoc/2.png)
  
  2.  预处理（去背景，降噪，二值化）:
        - 去除噪点：图片为RGB图，通过取色器观察，发现字符与噪点RGB值差别较大，选取大概阈值，遍历图片将噪点（干扰线）赋值为255。
        - 二值化：同样选取阈值，遍历图片将背景赋值为255，字符赋值为0。
        - 处理结果：![](https://github.com/weixianglin/Verification-code-crack/blob/master/picdoc/4.gif)    ![](https://github.com/weixianglin/Verification-code-crack/blob/master/picdoc/3.gif)                                                                   
        - 主要代码:![](https://github.com/weixianglin/Verification-code-crack/blob/master/picdoc/5.png)
  3. 图片分割，分类组成字模库:
      - 观察知字符之间几乎无粘黏，可将图片像素垂直投射成一维列表，记录每一列黑色像素总和。
      - 一维列表波峰可表示为字符，波谷为字符间隙。通过不断尝试选取最合适的波峰波谷值来分割图片。
      - 将分割好的字符分类，分别存放在文件夹中，组成字模库。
  4. 建立训练集和测试集进行神经网络训练，使误差达到理想值:
      - 构建三层神经网络：1个输入层、1个隐含层和1个输出层。
      - 设置网络参数，选取适当数量的字符样本训练网络。当网络误差收敛到所设定的目标值时结束训练，保存相关数据留待后用。
      - 主要代码：
      ![](https://github.com/weixianglin/Verification-code-crack/blob/master/picdoc/6.png)![](https://github.com/weixianglin/Verification-code-crack/blob/master/picdoc/7.png)
  5. 运行识别程序，验证识别准确性：
        - 抓取的图片：![](https://github.com/weixianglin/Verification-code-crack/blob/master/picdoc/8.png)
        - 识别结果：![](https://github.com/weixianglin/Verification-code-crack/blob/master/picdoc/9.png)
        
       
       
*第一次提交代码到GitHub，望大佬们轻喷 :stuck_out_tongue_closed_eyes:* 
