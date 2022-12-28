import requests
import re
import os
import time
import urllib
import tkinter as tk
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400QQBrowser/10.5.3863.400',

}  # 请求头



def spider(img_name, img_num):
    n=1
    dir_name = 'img'  # 生成文件夹
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    time.sleep(2)
    while n <= img_num:
        url = 'https://pic.sogou.com/pics?query='+img_name
        response = requests.get(url, headers=headers)
        plt = re.findall(r'\"pic_url\"\:\".*?\"', response.text)#response.text是以unicode返回响应的内容
        print(plt)
        for i in plt:
            pic_url = i.split(':')[2][0:-1]
            pic_name = dir_name+'/'+str(n)+'.jpg'

            result_pic = requests.get('http:'+pic_url, headers=headers)
            # 存入文件，注意使用二进制存储(wb+),b是二进制存储，所有多媒体(图片、音乐、视频)文件都是二进制
            with open(pic_name, 'wb+') as f:
                f.write(result_pic.content)
            print(pic_name + "正在下载........")#可在gui显示
            n += 1
    text.insert('end',"下载完成")

def keywords():
    spider(kw.get(), 1)#关键词在这里修改



root = tk.Toplevel()
root.title("搜狗图片批量下载")
root.geometry('410x150')
laber_0 = tk.Label(root,text = "请输入图片关键词：")
laber_1 = tk.Label(root,text = "由于技术限制，下载过程中界面未响应属正常现象，请耐心等待图片下载完毕")
laber_0.grid(row = 1, column = 0)
laber_1.grid(row = 2, column = 0,columnspan = 3)
Getkw = tk.Button(root, text='开始下载', width=10,height=2, command=keywords)
kw = tk.StringVar()
entrykw = tk.Entry(root, textvariable = kw)
entrykw.grid(row = 1,column = 1)
Getkw.grid(row = 1,column = 2)


text = tk.Text(root, height=5,width=50)
text.grid(row=4, column=0,columnspan = 4)
root.mainloop()
