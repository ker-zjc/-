import requests
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk

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
       url = 'http://www.tianqihoubao.com/lishi/langfang/month/202006.html'
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

