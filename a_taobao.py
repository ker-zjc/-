import requests#引入request库
import re#正则
import time
import tkinter as tk#引入tk库
from tkinter.messagebox import *

def getHTMLText(url):
    kv = {
         'authority': 's.taobao.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh,ja;q=0.9,zh-CN;q=0.8',
    'cookie': 'cna=K5wPF7CguQQCATwe5Q1dHs/k; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; _fbp=fb.1.1586946094270.1002744736; tracknick=tb16442152; _cc_=UIHiLt3xSw%3D%3D; enc=3bej%2BMmtAEIl47Xm0I69vadtsUabBUkf25JVyzJjw8b7pmxQrtUgxqpyM93DU4ryRTWFc3sgMF%2BZ6rXT0vEcbA%3D%3D; miid=1792419291247203692; t=f85ccbb3a881336013731f6d98030535; sgcookie=EdPhQgjxwfrjh%2F4RyQWOW; uc3=lg2=Vq8l%2BKCLz3%2F65A%3D%3D&nk2=F5REODd5SLVpMg%3D%3D&vt3=F8dBxGZpZ1oh0egoQ9E%3D&id2=UUkO1b5x86rpIw%3D%3D; lgc=tb16442152; uc4=nk4=0%40FY4PammI5gU9RX%2BWfAt1OVTOpaei&id4=0%40U2uCuvDuFKOSKank8g66kwoBKJNW; tfstk=cSDdBesqUFYnCoZt0XdgNOVYoi8cZ9SLrMaRe3PQ7lSGhk6RirHmHYVkOu7LBhC..; mt=ci=-1_0; cookie2=13d02341c725d810ab8668e4725ea2a1; v=0; _tb_token_=e33be9f5b1ea; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=7180563A7AC7EE9BCA24B20B3513224F; uc1=cookie14=UoTV7X4AhUQBHA%3D%3D; isg=BPT0I8qrFvxEXoLgyt1Y8uAJxbJmzRi3oDJ_7I5VgH8C-ZRDtt3oR6q7fTkhGlAP; l=eBglraAVQmV985C9BOfanurza77OSIRYYuPzaNbMiOCP_p1B5ZC5WZvGFq86C3GNh6XkR35uw339BeYBqQAonxv92j-la_kmn',}
    try:
        r = requests.get(url, headers=kv, timeout=30)
        r = requests.get(url, headers=kv, timeout=30)#get获取网页内容
        r.raise_for_status()#HTTP请求的返回状态，200成功，其余表示失败
        r.encoding = r.apparent_encoding#从HTTP header中猜测编码方式=从内容中分析出响应内容的编码方式
        return r.text
    except:
        return ""

def parsePage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)#正则过滤价格
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)#过滤标题
        for i in range(len(plt)):#遍历
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])#切片
            ilt.append([price, title])
    except:
        print("")

def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"#字符串，添加关键词
    print(tplt.format("序号", "价格", "商品名称"))
    # 写入文件
    f = open('淘宝价格清单.txt', 'w', encoding='utf-8')#utf-8写中文
    f.write('价格         商品名称\n')
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))#format写法填充
        f.write(g[0])
        f.write(g[1])
        f.write('\r\n')
    showinfo('提示', '数据文件已成功导出到根目录！')

def taobao():
    depth = 1#爬取页数（此程序通过cookie绕过网站防爬检测，页数尽量不要设太高）
    start_url = 'https://s.taobao.com/search?q=' + goods.get()
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHTMLText(url)
            parsePage(infoList, html)
            time.sleep(2)
        except:
            continue
    printGoodsList(infoList)#形式参数

#此处开始是GUI函数
def getgoods():
    taobao()

root = tk.Toplevel()#如果独立访问该文件，需将Toplevel()换为Tk(),否则会出现两个窗口
root.title("淘宝商品查询")
frmlt_1 = tk.Frame(root,width=250, height=160)
frmlt_2 = tk.Frame(root,width=250, height=160)
laber_1 = tk.Label(root,text = "欢迎使用淘宝商品查询系统")
laber_2 = tk.Label(root,text = "请在此输入所需要的商品名")
goods = tk.StringVar()
entryGoods = tk.Entry(root, textvariable = goods)
GetGoods = tk.Button(root,text = "提交",command = getgoods)
frmlt_1.grid(row=0, column=1,padx=1,pady=3)
frmlt_2.grid(row=4, column=4,padx=1,pady=3)
laber_1.grid(row = 1, column = 2)
laber_2.grid(row = 3, column = 2)
entryGoods.grid(row = 2,column = 2)
GetGoods.grid(row = 2,column = 3)
img = tk.Frame(root,width=200, height=500)#建立图片所使用的标签
img.grid(row=0, column=1, rowspan=3,padx=2,pady=3)
imgInfo = tk.PhotoImage(file = "Logo_taobao.png")#图片插入
lblImage = tk.Label(img, image = imgInfo)
lblImage.image = imgInfo
lblImage.grid()

root.mainloop()
