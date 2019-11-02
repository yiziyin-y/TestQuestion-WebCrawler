# -*- coding: UTF-8 -*-

from Tkinter import *
import sys
from BS import glo
from scrapy import cmdline
import threading
from PIL import Image, ImageTk

reload(sys)
sys.setdefaultencoding('utf-8')
inputUrl = ""
inputType = ""


def StartCallback(inputUrl, inputType):
    print(inputUrl)
    print(inputType)
    glo.setInputType(inputType)
    glo.setInputUrl(inputUrl)
    # os.system("start.py")
    # print("UI:%s"%glo.inputType)
    cmdline.execute("scrapy crawl BS ".split())


def ExportTOGO(inputType):
    thread1 = threading.Thread(target=UIexport(inputType))
    thread1.setDaemon(True)
    thread1.start()


def StartTOGO(inputUrl, inputType):
    thread2 = threading.Thread(target=StartCallback(inputUrl, inputType))
    thread2.setDaemon(True)
    thread2.start()


def UIexport(inputType):

    from BS.export import replaceQ, replaceA, export
    glo.setInputType(inputType)
    export()
    replaceQ()
    replaceA()


# 防止跳出奇怪新窗口
if __name__ == '__main__':
    # 创建空白窗口,作为主载体

    root = Tk()
    root.resizable(False, False)
    root.title('试题抓取程序')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

# 窗口的大小，后面的加号是窗口在整个屏幕的位置
    root.geometry('600x200+400+200')
    root.iconbitmap('1.ico')

    photo=ImageTk.PhotoImage(file="11.jpg")
    label=Label(root,image=photo)  # 图片
    label.grid(columnspan=3,rowspan=8)
# 标签控件，窗口中放置文本组件
    L1 = Label(root, text='请输入下载的url:', font=("微软雅黑", 15), fg='brown')
    L1.grid(row=0, column=0, sticky=W+N)
# Entry是可输入文本框
    url_input = Entry(root, font=("微软雅黑", 15), width=35)
    url_input.grid(row=0, column=1, columnspan=2, sticky=N)
# 定位 pack包 place位置 grid是网格式的布局
    L2 = Label(root, text='请输入题目类型:', font=("微软雅黑", 15), fg='brown')
    L2.grid(row=1, column=0, sticky=W)
    type_input = Entry(root, font=("微软雅黑", 15), width=35)
    type_input.grid(row=1, column=1, columnspan=2)


# 列表控件
    L3 = Label(root)
    L3.grid(row=3, sticky=W)
    L4 = Label(root)
    L4.grid(row=4, sticky=W)
    global inputUrl
    global inputType

# 设置按钮 sticky对齐方式，N S W E
    buttonStart = Button(
        root,
        text='开始下载',
        bg='#228B22',
        font=("微软雅黑", 15), command=lambda: StartTOGO(url_input.get(), type_input.get()))\
        .grid(row=5, column=0, sticky=W+S)
    buttonExport = Button(
        root,
        text='导出',
        bg='#6495ED',
        font=("微软雅黑", 15), command=lambda: ExportTOGO(type_input.get())) .grid(row=5, column=1, sticky=S)
    buttonExit = Button(
        root,
        text='退出',
        bg='#F08080',
        font=("微软雅黑", 15), command=root.quit)\
        .grid(row=5, column=2, sticky=E+S)
# 使得窗口一直存在
#
    root.mainloop()
