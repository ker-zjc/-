import requests
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
#本来想制作直接搜索电影名就出评分结果的，可是豆瓣电影搜索的API接口最近不能用，只能做成这样了
def getHTMLText(url):
       kv = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',}     
       try:  
              r = requests.get(url, headers=kv , timeout=30)#get获取网页内容
              r.raise_for_status()#HTTP请求的返回状态，200成功，其余表示失败
              r.encoding = r.apparent_encoding#从HTTP header中猜测编码方式=从内容中分析出响应内容的编码方式
              return r.text
       except:
              return ""

def searchStar(html,star_list):
       bs = BeautifulSoup(html, 'html.parser')#将网页源代码用bs4展示
       star = bs.find_all('span', class_="rating_per")#查找每个星级评价的占比所在的代码
       for i in range(5):        
              star_list.append(star[i].text[0:5])#将星级信息存入star_list列表
       
def main():
       url = 'https://movie.douban.com/subject/'+ ID.get()
       html = getHTMLText(url)
       star_list=[]
       searchStar(html,star_list)
       print(star_list)
       #将百分数转为小数
       df=pd.DataFrame({'%':star_list})
       p_float=df['%'].str.strip('%').astype(float) / 100
       p_float2=p_float.round(3)
       #建立柱状图
       sns.barplot(x=['five star','four star','three star','two star','one star'],y=p_float2)
       plt.show()

def getID():
       main()

root = tk.Toplevel()#如果独立访问该文件，需将Toplevel()换为Tk(),否则会出现两个窗口
root.title("豆瓣电影评分图表生成器")
root.geometry('250x200')
laber_1 = tk.Label(root,text = "请在此输入希望查询电影的豆瓣ID")
ID = tk.StringVar()
entryID = tk.Entry(root, textvariable = ID)
GetID = tk.Button(root,text = "提交",command = getID)
laber_1.grid(row = 1, column = 3)
entryID.grid(row = 2,column = 3)
GetID.grid(row = 2,column = 4) 
text = tk.Text(root,width=34,height=5)
text.grid(row = 3,column = 2,columnspan = 3)
text.insert('end',"例：天气之子的页面链接为：https://movie.douban.com/subject/30402296/\nID即为：30402296\nID可以在豆瓣相应电影页面的链接尾部查询")

root.mainloop()
