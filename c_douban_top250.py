import requests
# 引用requests模块
from bs4 import BeautifulSoup
import tkinter as tk

def run():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    for x in range(10):
        url = 'https://movie.douban.com/top250?start=' + str(x*25) + '&filter='
        res = requests.get(url, headers=headers)
        bs = BeautifulSoup(res.text, 'html.parser')
        tag_num = bs.find_all('div', class_="item")
        # 查找包含序号，电影名，链接的<div>标签
        tag_comment = bs.find_all('div', class_='star')
        # 查找包含评分的<div>标签
        tag_word = bs.find_all('span', class_='inq')
        # 查找推荐语

        list_all = []
        for x in range(len(tag_num)):
            if tag_num[x].text[2:5] == '' or tag_num[x].text[2:5] =='' or x >= len(tag_word):
            # 此处引号内，填写没有推荐语的电影序号
                list_movie = [
                tag_num[x].find('img')['alt'], tag_comment[x].text[2:5],
                tag_num[x].find('a')['href'],['\n']
                    ]
                 
            else:
                list_movie = [
                   tag_num[x].find('img')['alt'], tag_comment[x].text[2:5], 
                     tag_word[x].text, tag_num[x].find('a')['href'],['\n']
                         ]
                
            list_all.append(list_movie)#将爬到的信息放到一个空的列表里
        count=1
        for x in list_all:
            #将列表进行遍历循环，打印每个元素
            text.insert('end',(count, x))
            count+=1

root = tk.Toplevel()
root.title("豆瓣电影排行榜")
root.geometry('567x710')
button_1 = tk.Button(root, text='点此获取排名', width=10,height=2, command=run)
button_1.grid(row=1, column=1)
text = tk.Text(root, height=50)
text.grid(row=2, column=1)
root.mainloop()

