from tkinter.constants import *
from os import path
import tkinter as tk
from PIL import Image,ImageTk

class ui():
    def __init__(self) -> None:
        self.win = tk.Tk()
        self.basepath = path.dirname(path.realpath(__file__))
        self.align_mode = 'nsew'
        self.pad = 8
        pass

    def open_window(self):
        #Tkinter的部分
        self.win.title('OmniImaginer.exe')
        self.win.geometry('1000x563')
        self.win.resizable(False, False)
        self.win.iconbitmap('Bernie.ico')
        ##分格-1
        #self.upper = tk.Frame(self.win, width=1000, height=171)
        #self.lower = tk.Frame(self.win, width=1000, height=392)
        #self.upper.grid(column=0, row=0, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        #self.lower.grid(column=0, row=1, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        ##分格-2
        #self.upl = tk.Frame(self.upper, width=561)
        #self.upr = tk.Frame(self.upper, width=423)
        #self.lol = tk.Frame(self.lower, width=561)
        #self.PoI = tk.Frame(self.lower, width=423)
        #self.upl.grid(column=0, row=0, padx=self.pad/2, pady=self.pad, sticky=self.align_mode)
        #self.upr.grid(column=1, row=0, padx=self.pad/2, pady=self.pad/2, sticky=self.align_mode)
        #self.lol.grid(column=0, row=0, padx=self.pad/2, pady=self.pad/2, sticky=self.align_mode)
        #self.PoI.grid(column=1, row=0, padx=self.pad/2, pady=self.pad/2, sticky=self.align_mode)
        ##分格-3
        #self.LII = tk.Frame(self.upl, height=74)
        #self.IUI = tk.Frame(self.upl, height=75)
        #self.CI = tk.Frame(self.upr, width=99)
        #self.L = tk.Frame(self.upr, width=99)
        #self.EP = tk.Frame(self.lol, width=258, height=266)
        #self.SD = tk.Frame(self.lol, width=295, height=62)
        #self.PP = tk.Frame(self.lol, width=295, height=204)
        #self.ExP = tk.Frame(self.lol, height=102)
        #self.LII.grid(column=0, row=0, padx=self.pad/4, pady=self.pad/2, sticky=self.align_mode)
        #self.IUI.grid(column=0, row=1, padx=self.pad/4, pady=self.pad/2, sticky=self.align_mode)
        #self.CI.grid(column=0, row=0, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        #self.L.grid(column=1, row=0, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        #self.EP.grid(column=0, row=0, rowspan=2, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        #self.SD.grid(column=1, row=0, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        #self.PP.grid(column=1, row=1, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        #self.ExP.grid(column=0, row=2, columnspan=2, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        #本地檔案導入方式(LII)
        self.promptL = tk.Label(text="選取本地檔案", bg="grey", fg="white", height=2, width=15)
        self.entryL = tk.Text(height=2, width=45)
        self.entryL['state'] = DISABLED
        self.btnL = tk.Button(text="...", height=1, width=4)
        self.promptL.place(x=25,y=27)
        self.entryL.place(x=150,y=30)
        self.btnL.place(x=485,y=32)
        #網路檔案導入方式(IUI)
        self.promptU = tk.Label(text="導入網路檔案", bg="grey", fg="white", height=2, width=15)
        self.entryU = tk.Text(height=2, width=45)
        self.entryU['state'] = DISABLED
        self.btnU = tk.Button(text="...", height=1, width=4)
        self.promptU.place(x=25,y=77)
        self.entryU.place(x=150,y=80)
        self.btnU.place(x=485,y=82)
        #self.promptU.grid(column=0, row=1)
        #self.entryU.grid(column=1, row=1, padx=8)
        #self.btnU.grid(column=2, row=1)
        #雲端導入方式(CI)
        self.promptC = tk.Label(text="或者...從雲端導入")
        self.btnGD = tk.Button(text="Google Drive", height=2, width=20)
        self.btnDB = tk.Button(text="Dropbox", height=2, width=20)
        #self.promptC.grid(column=0, row=0, columnspan=2, padx=40)
        #self.btnGD.grid(column=0, row=1, columnspan=2, padx=40)
        #self.btnDB.grid(column=0, row=2, columnspan=2, padx=40)
        #浮水印(L)
        self.oimg= (Image.open("uep.png"))
        self.img = ImageTk.PhotoImage(self.oimg.resize((100,120), Image.ANTIALIAS))
        self.label = tk.Label(image=self.img)
        #self.label.grid(column=0, row=0, columnspan=2)
        #效果處理器(EP)
        #方位處理器(PP)
        #尺寸動態顯示(SD)
        #圖片預覽(PoI)
        #輸出(ExP)
        self.win.mainloop()



