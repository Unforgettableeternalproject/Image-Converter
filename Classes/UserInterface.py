from tkinter.constants import *
from os import path
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import filedialog
from tkinter import ttk
import os

file_path="a"

    #tkinter.messagebox.showinfo(title = 'Hello',message = file_path)

class ui():
    def OnopenFile(self):
        # msg = "Hello, {}.".format(entry.get())
        file_path = filedialog.askopenfilename()
        self.entryL['state'] = NORMAL
        self.entryL.delete(1.0, "end")
        self.entryL.insert("insert", file_path)
        self.entryL['state'] = DISABLED
        return file_path

    def Update(self, scale, text):
        pass

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
        self.entryL = tk.Text(height=2, width=45)
        self.entryL['state'] = DISABLED
        self.btnL = tk.Button(text="...", height=1, width=4,command=self.OnopenFile)
        self.btnL.pack()
        #self.labelL = tk.Label( text = file_path)
        #self.labelL.pack()
        self.promptL.place(x=25, y=27)
        self.entryL.place(x=150, y=30)
        self.btnL.place(x=485, y=32)
        #網路檔案導入方式(IUI)
        self.promptU = tk.Label(text="導入網路檔案", bg="grey", fg="white", height=2, width=15)
        self.entryU = tk.Text(height=2, width=45)
        self.entryU['state'] = DISABLED
        self.btnU = tk.Button(text="...", height=1, width=4)
        self.promptU.place(x=25, y=77)
        self.entryU.place(x=150, y=80)
        self.btnU.place(x=485, y=82)
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
        self.label.place(x=800, y=25)
        #效果處理器(EP)
            #HSV滑桿的部分
        self.H_label = tk.Label(text="色相:").place(x=15, y=169)
        self.S_label = tk.Label(text="飽和度:").place(x=4, y=209)
        self.V_label = tk.Label(text="明度:").place(x=15, y=249)
        self.H_slider = tk.Scale(from_=0, to=360, length=200, orient=tk.HORIZONTAL)
        self.S_slider = tk.Scale(from_=0, to=100, length=200, orient=tk.HORIZONTAL)
        self.V_slider = tk.Scale(from_=0, to=100, length=200, orient=tk.HORIZONTAL)
        self.H_entry = tk.Entry(width=4, state=DISABLED).place(x=260, y=170) #Entry部分之後會做數值同步
        self.S_entry = tk.Entry(width=4, state=DISABLED).place(x=260, y=210)
        self.V_entry = tk.Entry(width=4, state=DISABLED).place(x=260, y=250)
        self.H_slider.place(x=50, y=150)
        self.S_slider.place(x=50, y=190)
        self.V_slider.place(x=50, y=230)
            #侵蝕、膨脹的部分
        self.erodebtn = tk.Button(text="侵蝕++", height=2, width=7).place(x=50, y=280)
        self.dilatebtn = tk.Button(text="膨脹++", height=2, width=7).place(x=50, y=330)
        self.eddisplay = tk.Label(text="平衡落差:").place(x=140, y=342)
        self.edvalue = tk.Entry(width=4, state=DISABLED).place(x=200, y=344)
        self.openingck = tk.Checkbutton(text="去白點").place(x=125, y=285)
        self.closingck = tk.Checkbutton(text="去黑點").place(x=195, y=285)
        self.gradientck = tk.Checkbutton(text="只顯示輪廓").place(x=148, y=310)
            #濾波器的部分
        self.clabel = tk.Label(text="其他效果:").place(x=25, y=385)
        self.clist = ttk.Combobox(width=17, state="readonly", value=["無", "Boxblur", "Blur", "Medianblur", "Bilateral", "Gaussian"]).place(x=85, y=385)
            #灰階的部分
        self.gsck = tk.Checkbutton(text="灰階").place(x=235, y=383)
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



