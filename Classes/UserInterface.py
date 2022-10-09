from tkinter.constants import *
from os import path
import tkinter as tk
from turtle import onclick
from PIL import Image,ImageTk
import tkinter.messagebox
from tkinter import filedialog
import os

file_path="a"
def OnopenFile():
    # msg = "Hello, {}.".format(entry.get())
    global file_path
    file_path = filedialog.askopenfilename()
    tkinter.messagebox.showinfo(title = 'Hello',message = file_path)

class ui():
    def __init__(self) -> None:
        self.win = tk.Tk()
        self.basepath = path.dirname(path.realpath(__file__))
        self.align_mode = 'nsew'
        self.pad = 8
        pass

    def open_window(self):
        #視窗介面
        self.win.title('OmniImaginer.exe')
        self.win.geometry('1000x563')
        self.win.resizable(False, False)
        self.win.iconbitmap('Bernie.ico')
        #本地檔案導入方式(LII)
        self.promptL = tk.Label(text="選取本地檔案", bg="grey", fg="white", height=2, width=15)
        self.btnL = tk.Button(text="...", height=1, width=4,command=OnopenFile)
        self.btnL.pack()
        self.labelL = tk.Label( text = file_path)
        self.labelL.pack()
        # self.entryL = tk.Text(height=2, width=45)
        # self.entryL['state'] = DISABLED
        self.promptL.place(x=25,y=27)
        self.labelL.place(x=150,y=30)#entry into label
        self.btnL.place(x=485,y=32)
        #網路檔案導入方式(IUI)
        self.promptU = tk.Label(text="導入網路檔案", bg="grey", fg="white", height=2, width=15)
        self.entryU = tk.Text(height=2, width=45)
        self.entryU['state'] = DISABLED
        self.btnU = tk.Button(text="...", height=1, width=4)
        self.promptU.place(x=25,y=77)
        self.entryU.place(x=150,y=80)
        self.btnU.place(x=485,y=82)
        #雲端導入方式(CI)
        self.GDicon = ImageTk.PhotoImage(Image.open('Drive.png').resize((50,50)))
        self.DBicon = ImageTk.PhotoImage(Image.open('Dropbox.png').resize((50,50)))
        self.promptC = tk.Label(text="或者...從雲端導入", bg="grey", fg="white", height=2, width=20)
        self.btnGD = tk.Button(text="Google Drive", image=self.GDicon)
        self.btnDB = tk.Button(text="Dropbox", image = self.DBicon)
        self.promptC.place(x=600, y=15)
        self.btnGD.place(x=610, y=60)
        self.btnDB.place(x=680, y=60)
        #浮水印(L)
        #self.img= ImageTk.PhotoImage(Image.open("uep.png").resize((100,120)))
        self.label = tk.Label(text="浮水印預定放置區塊",bg="grey", fg="white", height=5, width=20)
        self.label.place(x=800,y=25)
        #效果處理器(EP)
        #方位處理器(PP)
        #尺寸動態顯示(SD)
        #圖片資訊顯示(ID)
        #圖片預覽(PoI)
        #輸出(ExP)

        #菜單
        self.menu = tk.Menu(self.win, background='red')

        self.win.config(menu=self.menu)
        self.file = tk.Menu(self.menu, tearoff=0)
        self.file.add_command(label='顯示範例') #程式中顯示範例圖片檔的預覽
        self.file.add_command(label='重置') #跳出視窗顯示警告，並詢問是否真的要重置

        self.window = tk.Menu(self.menu, tearoff=0)
        self.window.add_command(label='步驟紀錄') #跳出新視窗，顯示步驟紀錄
        self.window.add_command(label='開發者資訊') #跳出新視窗，顯示開發者資訊

        self.view = tk.Menu(self.menu, tearoff=0)
        self.view_options = tk.Menu(self.view, tearoff=0)
        self.view_options.add_command(label='小') #變更為小視窗
        self.view_options.add_command(label='中等') #變更為中等視窗
        self.view_options.add_command(label='大') #變更為大視窗
        self.view.add_cascade(label='更改視窗大小', menu=self.view_options) #給予更改視窗比例的選項

        self.help = tk.Menu(self.menu, tearoff=0)
        self.window.add_command(label='功能介紹') #跳出新視窗，顯示一個功能介紹的畫面(Help)
        self.help.add_command(label='聯絡開發者') #跳出新視窗，內嵌開發者聯絡資訊(直接寄信?)

        self.menu.add_cascade(label='檔案', menu=self.file)
        self.menu.add_cascade(label='視窗', menu=self.window)
        self.menu.add_cascade(label='顯示', menu=self.view)
        self.menu.add_cascade(label='幫助', menu=self.help)

        #運行程式
        self.win.mainloop()



