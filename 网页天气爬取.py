import requests#pip install requests
from bs4 import BeautifulSoup#pip install BeautifulSoup
import pandas as pd#pip install pandas

def get_data(url):#用一个形参url输入网址
    resp = requests.get(url)
    #网页源代码
    html = resp.content.decode('gbk')
    #二进制返回网页内容
    soup = BeautifulSoup(html,'html.parser')
    tr_list = soup.find_all('tr')
    #以列表形式去收集
    dates,conditions,temp = [],[],[]
    for data in tr_list[1:]:#以逗号形式分隔两个字符串，列表
        sub_data = data.text.split()
        print(sub_data)
        dates.append(sub_data[0])
        conditions.append(''.join(sub_data[1:3]))#用join切割出部分天气
        print(conditions)
        temp.append(''.join(sub_data[3:6]))#用join分割出部分温度
        print(temp)
    _data = pd.DataFrame()#表格二维数据类型
    _data['日期'] = dates
    _data['天气状况'] = conditions
    _data['气温'] = temp

    return _data
    
#网页源摘自‘天气后报’廊坊2020前三个月        
data_1_month = get_data('http://www.tianqihoubao.com/lishi/langfang/month/202001.html')
data_2_month = get_data('http://www.tianqihoubao.com/lishi/langfang/month/202002.html')
data_3_month = get_data('http://www.tianqihoubao.com/lishi/langfang/month/202003.html')

data = pd.concat([data_1_month,data_2_month,data_3_month]).reset_index(drop=True)
#用一个行索引拼接成一个，并设置一个参数True
data.to_csv('langfang.csv',index=False,encoding='utf-8')
#保存在一个文件叫langfang的csv文件，为了防止出现乱码encoding命名为utf-8,同时获取数据并保存。
#基本网页爬虫写完了，下面进行可视化

import pandas as pd#pip install pandas
from matplotlib import pyplot as plt#pip install matplotlib
#解决中文问题
plt.rcParams['font.sans-serif'] = ['SimHei']
#解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False
data = pd.read_csv('langfang.csv')#读取文件langfdang.csv
print((data.isnull()).sum())
print(data.head(5))

data['最高气温'] = data['气温'].str.split('/',expand=True)[0]#用切割出来的数据放成一列
data['最低气温'] = data['气温'].str.split('/',expand=True)[1]#同上，索引改为1，即两列，最高气温，最低气温

data['最高气温']= data['最高气温'].map(lambda x:int(x.replace('℃','')))#把字符串℃数据去除，转换成整型数据，

data['最低气温']= data['最低气温'].map(lambda x:int(x.replace('℃','')))#另一列，效果同上
dates = data['日期']
highs = data['最高气温']
lows = data['最低气温']
#根据数据绘制图形
fig = plt.figure(dpi=128,figsize=(10,6))
plt.plot(dates,highs,c='red',alpha=0.5)
plt.plot(dates,lows,c='blue',alpha=0.5)
#给图表区域着色
plt.fill_between(dates,highs,lows,facecolor='blue',alpha=0.2)
#其中alpha值指定颜色的透明度（0为完全透明，1为完全不透明）

#设置图形的格式
plt.title('2020第一季度天气',fontsize=24)
plt.xlabel('',fontsize=6)
fig.autofmt_xdate()#绘制斜向的日期标签，以免重叠
plt.ylabel('气温',fontsize=12)
#参数刻度线样式设置
plt.tick_params(axis='both',which='major',labelsize=10)

#修改刻度
plt.xticks(dates[::20])
#显示最高气温折线图
plt.show()
