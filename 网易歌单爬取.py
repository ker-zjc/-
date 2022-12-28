import requests#pip install requests
from bs4 import BeautifulSoup#pip install BeatuifulSoup
import urllib.request
from lxml import html#pip install lxml
import os#通过操作系统创建文件
import tkinter as tk
def main():
    etree = html.etree#lxml.etree提供了ElementTree API定义接口，以及简单的enhancements
    now = os.getcwd()#定位当前目录
    path = now + "\下载歌单"
    if not os.path.exists(path):
        os.mkdir(path)
    #这里是设置请求头，其实就是在访问的时候表现的像用户一样访问，而不是以一个python的形式，否则容易被拦截，表示之前爬别的时候被远程主机关了好几次，不让你爬
    headers = {
        'Referer': 'http://music.163.com/',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    #歌单都有ID号，歌曲也有，写下url的地址也可以改ID，方便爬歌
    play_url = 'https://music.163.com/playlist?id=' + ID.get()
    s = requests.session()  #这里两行用requests获取网页内容
    response = s.get(play_url, headers=headers).content
    
    s = BeautifulSoup(response, 'lxml')#现在就可以用bs4匹配出对应歌曲名称和地址啦~
    main = s.find('ul', {'class': 'f-hide'})
    print(main.find_all('a'))#这里用了bs4筛选a标签
    lists = []
    for music in main.find_all('a'):
        list = []
        #（尝试）print('{}:{}'.format(music.text,music['href']))
        musicUrl = 'http://music.163.com/song/media/outer/url' + music['href'][5:] + '.mp3'
        musicName = music.text#上面是网址，这得把歌名打印出来不是
        list.append(musicName)#单首歌曲的名字放入列表
        list.append(musicUrl)#单首歌曲的地址也放入list列表中
        #全部歌曲信息放在lists列表中
        lists.append(list)
    #下载列表中的全部歌曲，并以歌曲名命名后下载后文件，储存文件
    for i in lists:
        url = i[1]
        name = i[0]
        try:
            print('正在下载', name)
            #这两行指定下载路径，随便指定盘符都行。本来打算弄D盘的，但防止有些人电脑是没有D盘的，所以定位到了当前目录
            text.insert('end',("正在下载", name,"\n"))
            urllib.request.urlretrieve(url, now + '/下载歌单/%s.mp3' % name)
            print('下载成功')
            text.insert('end',"下载成功\n")#看到的这些text都是为了GUI，同学为了打印出来弄的
        except:
            text.insert('end',"下载失败，请查看网络哦！")#别天真了，下歌也是得连网的
    text.insert('end',"歌曲全部下载成功，请在根目录下的下载歌单中查找歌曲！\n")            
#做一个界面
root = tk.Toplevel()
root.title("网易云歌单歌曲批量下载")#界面主题
root.geometry('720x500')#大小面积
GetID = tk.Button(root, text='获取歌曲', width=10,height=2, command=main)#设置一个小按钮，写着‘获取歌曲’，后面是宽还有高的设置
laber_0 = tk.Label(root,text = "请输入歌单ID：")#第一行输入歌单ID，因为我的程序呢，是可以根据不同歌单下载不同歌曲的，简直就像是爬了网易云的所有歌（嘚瑟一下）
laber_1 = tk.Label(root,text = "歌单ID可在歌单链接的尾部获得，示例ID：4944138426，由于网站限制本程序只能抓取歌单前10首歌")#第二行
laber_2 = tk.Label(root,text = "由于技术限制，下载过程中界面未响应属正常现象，请耐心等待歌曲下载完毕")#第三行
laber_0.grid(row = 1, column = 0)#row,column就是行，列设置距离
laber_1.grid(row = 2, column = 1)
laber_2.grid(row = 3, column = 1)
ID = tk.StringVar()
entryID = tk.Entry(root, textvariable = ID)#这些就是用户输入ID框的设置了，效果和上面一样
entryID.grid(row = 1,column = 1)
GetID.grid(row = 1,column = 2) 

text = tk.Text(root, height=30)#打印
text.grid(row=4, column=0,columnspan = 4)
root.mainloop()
