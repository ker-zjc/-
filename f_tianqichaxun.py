import tkinter as tk
import requests
from bs4 import BeautifulSoup
import re

def get_page(url):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url,headers = kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '错误'

def parse_page(html, return_list):
    soup = BeautifulSoup(html, 'html.parser')
    day_list = soup.find('ul', 't clearfix').find_all('li')
    for day in day_list:
        date = day.find('h1').get_text()
        wea = day.find('p',  'wea').get_text()
        if day.find('p', 'tem').find('span'):
                hightem = day.find('p', 'tem').find('span').get_text()
        else:
                hightem = ''
        lowtem = day.find('p', 'tem').find('i').get_text() 
        #win = re.search('(?<= title=").*?(?=")', str(day.find('p','win').find('em'))).group()
        win = re.findall('(?<= title=").*?(?=")', str(day.find('p','win').find('em')))
        wind = '-'.join(win)
        level = day.find('p', 'win').find('i').get_text()
        return_list.append([date, wea, lowtem, hightem, wind, level])
    #return return_list

def print_res(return_list):
    tplt = '{0:<10}\t{1:^10}\t{2:^10}\t{3:{6}^10}\t{4:{6}^10}\t{5:{6}^5}'
    text.insert('end',tplt.format('日期', '天气', '最低温', '最高温', '风向', '风力',chr(12288)))
    text.insert('end',"\n")
    for i in return_list:
        text.insert('end',tplt.format(i[0], i[1],i[2],i[3],i[4],i[5],chr(12288)))
        text.insert('end',"\n")

def main():
    url = 'http://www.weather.com.cn/weather/'+ID.get()+'.shtml'
    html = get_page(url)
    wea_list = []
    parse_page(html, wea_list)
    print_res(wea_list)
def set():
    if __name__ == '__main__':
        main()

root = tk.Toplevel()
root.title("天气查询")
root.geometry('665x500')

GetID = tk.Button(root, text='获取一周天气', width=10,height=2, command=main)
laber_0 = tk.Label(root,text = "请输入城市ID：")
laber_1 = tk.Label(root,text = "城市ID可在中国天气网城市链接的尾部获得")
laber_2 = tk.Label(root,text = "示例天津的ID为：101030100")
laber_0.grid(row = 1, column = 0)
laber_1.grid(row = 2, column = 1)
laber_2.grid(row = 3, column = 1)

GetID = tk.Button(root, text='获取七日天气', width=10,height=2, command=main)
ID = tk.StringVar()
entryID = tk.Entry(root, textvariable = ID)
entryID.grid(row = 1,column = 1)
GetID.grid(row = 1,column = 2)

text = tk.Text(root, height=30,width=94)
text.grid(row=4, column=0,columnspan = 4)
root.mainloop()
