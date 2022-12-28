import tkinter as tk
from urllib import parse
from lxml import etree
from urllib3 import disable_warnings
import requests
def main():
    class Wangyiyun(object):

        def __init__(self, **kwargs):
            # 歌单的歌曲风格
            self.types = kwargs['types']
            # 歌单的发布类型
            self.years = kwargs['years']
            # 这是当前爬取的页数
            self.pages = pages
            # 这是请求的url参数（页数）
            self.limit = 35
            self.offset = 35 * self.pages - self.limit
            # 这是请求的url
            self.url = "https://music.163.com/discover/playlist/?"


        # 设置请求头部信息(可扩展：不同的User - Agent)
        def set_header(self):
            self.header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
                "Referer": "https://music.163.com/",
                "Upgrade-Insecure-Requests": '1',
            }
            return self.header

        # 设置请求表格信息
        def set_froms(self):
            self.key = parse.quote(self.types)
            self.froms = {
                "cat": self.key,
                "order": self.years,
                "limit": self.limit,
                "offset": self.offset,
            }
            return self.froms

        # 解析代码，获取有用的数据
        def parsing_codes(self):
            page = etree.HTML(self.code)
            # 标题
            self.title = page.xpath('//div[@class="u-cover u-cover-1"]/a[@title]/@title')
            # 作者
            self.author = page.xpath('//p/a[@class="nm nm-icn f-thide s-fc3"]/text()')
            # 阅读量
            self.listen = page.xpath('//span[@class="nb"]/text()')
            # 歌单链接
            self.link = page.xpath('//div[@class="u-cover u-cover-1"]/a[@href]/@href')

            # 打印
            for i in zip(self.title, self.link, self.author, self.listen):
                text.insert('end',"[歌单名称]：{}\n[发布作者]：{}\n[总播放量]：{}\n[歌单链接]：{}\n".format(i[0],i[2],i[3],"https://music.163.com/"+i[1]))
            text.insert('end','第{}页'.format(self.pages).center(50,'='))
            print("x")
        #gui显示
        # 获取网页源代码
        def get_code(self):
            disable_warnings()
            self.froms['cat']=self.types
            disable_warnings()
            self.new_url = self.url+parse.urlencode(self.froms)
            self.code = requests.get(
                url = self.new_url,
                headers = self.header,
                data = self.froms,
                verify = False,
            ).text

        # 爬取多页时刷新offset
        def multi(self ,page):
            self.offset = self.limit * page - self.limit




    if __name__ == '__main__':
        #=======================================
        # 指定一些参数
        # 歌单的歌曲风格
        types = "说唱"
        # 歌单的发布类型:最热=hot，最新=new
        years = "hot"
        # 指定爬取的页数
        pages = 1
        #=======================================

        # =======================================
        # 例子：通过pages变量爬取指定页面（多页）
        music = Wangyiyun(
            types = types,
            years = years,
        )

        for i in range(pages):
            page = i+1              # 因为没有第0页
            music.multi(page)       # 爬取多页时指定，传入当前页数，刷新offset
            music.set_header()      # 调用头部方法，构造请求头信息
            music.set_froms()       # 调用froms方法，构造froms信息
            music.get_code()        # 获取当前页面的源码
            music.parsing_codes()   # 处理源码，获取指定数据
        # =======================================

root = tk.Toplevel()
root.title("网易云音乐推荐歌单")
root.geometry('567x710')
button_1 = tk.Button(root, text='点此获取推荐', width=10,height=2, command=main)
button_1.grid(row=1, column=1)
text = tk.Text(root, height=50)
text.grid(row=2, column=1)
root.mainloop()
