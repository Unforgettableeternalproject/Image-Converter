from tkinter.constants import *
from os import path, remove
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter.font as tkFont
from idlelib.tooltip import Hovertip
from tkinter.messagebox import showinfo, showerror, showwarning, askyesno, askokcancel
import requests
import subprocess
import Classes.FileManager as FM
import Classes.EffectProcessor as EP
import Classes.PositionProcessor as PP
import Classes.Language as L
import numpy as np
import cv2




class ui():

    def __init__(self) -> None:
        self.f = FM.fm()
        self.e = EP.ep()
        self.p = PP.pp()
        self.original = None
        self.vaild = False
        self.win = tk.Tk()
        self.defaultFont = tkFont.Font(root=self.win, name="TkDefaultFont", exists=True)
        self.defaultFont.configure(family="Microsoft YaHei",
                                   size=9,
                                   weight=tkFont.NORMAL)
        self.basepath = path.dirname(path.realpath(__file__))
        self.align_mode = 'nsew'
        self.pad = 8
        self.textvariable = 0
        self.dimension = (0,0)
        self.createPreview()
        self.status = self.chknet()
        self.lanMode = 'CH'

        def hsv(event):
            self.color_block['bg'] = self.e.changeHSV(self.H_slider.get(), self.S_slider.get(), self.V_slider.get())
        def update():
            if(self.vaild):
                self.state = not self.state
                self.e.updateHSV(self.state)
                if(self.state):
                    self.color_block_btn['state'] = 'disabled'
                    self.color_block_btn2['state'] = 'normal'
                    self.H_slider['state'] = 'disabled'
                    self.S_slider['state'] = 'disabled'
                    self.V_slider['state'] = 'disabled'
                else:
                    self.color_block_btn2['state'] = 'disabled'
                    self.color_block_btn['state'] = 'normal'
                    self.H_slider['state'] = 'normal'
                    self.S_slider['state'] = 'normal'
                    self.V_slider['state'] = 'normal'
                self.createFilteredImage()
                self.createFlipedImage()
            self.updatePic()
        def erode():
            if(self.vaild):
                self.e.erode()
                self.createFilteredImage()
                self.createFlipedImage()
                self.edv.set(str(int(self.edv.get())+1))
            self.updatePic()
        def dilate():
            if(self.vaild):
                self.e.dilate()
                self.createFilteredImage()
                self.createFlipedImage()
                self.edv.set(str(int(self.edv.get())-1))
            self.updatePic()
        def opening():
            if(self.vaild):
                if(b1.get()):
                    self.accessOriginal('Set')
                    self.e.opening()
                    self.gradientck['state'] = 'disabled'
                    self.closingck['state'] = 'disabled'
                else:
                    cv2.imwrite("Preview.png", self.accessOriginal('Get'))
                    self.gradientck['state'] = 'normal'
                    self.closingck['state'] = 'normal'
                self.createFilteredImage()
                self.createFlipedImage()
            self.updatePic()
        def closing():
            if(self.vaild):
                if(b2.get()):
                    self.accessOriginal('Set')
                    self.e.closing()
                    self.gradientck['state'] = 'disabled'
                    self.openingck['state'] = 'disabled'
                else:
                    cv2.imwrite("Preview.png", self.accessOriginal('Get'))
                    self.gradientck['state'] = 'normal'
                    self.openingck['state'] = 'normal'
                self.createFilteredImage()
                self.createFlipedImage()
            self.updatePic()
        def gradient():
            if(self.vaild):
                if(b3.get()):
                    self.accessOriginal('Set')
                    self.e.gradient()
                    self.openingck['state'] = 'disabled'
                    self.closingck['state'] = 'disabled'
                else:
                    cv2.imwrite("Preview.png", self.accessOriginal('Get'))
                    self.openingck['state'] = 'normal'
                    self.closingck['state'] = 'normal'
                self.createFilteredImage()
                self.createFlipedImage()
            self.updatePic()
        def filter():
            if(self.vaild):
                self.e.filter(self.clist.get())
                self.createFlipedImage()
            self.updatePic()
        def flip(mode):
            if(self.vaild): 
                self.p.flip(mode)
                self.createFilteredImage()
            self.updatePic()
        def rotate():
            if(self.vaild):
                value = self.croinput.get('1.0', 'end-1c').strip()
                f = True if(value != '') else False
                for i in value:
                    if(not i.isdigit()): f = False
                if(f): 
                    if(self.dlist.get() == "順時針"): self.p.rotate(-(int(value) % 360))
                    else: self.p.rotate(int(value) % 360)
                else:
                    showwarning("不合理的輸入角度!", "旋轉角度必須要為整數，請再試一次!")
                self.croinput.delete(1.0, "end")
                self.createFilteredImage()
                self.createFlipedImage()
            self.updatePic()
        def zoom(event):
            if(self.vaild and self.chkscale.get()):
                if(self.zoom.get() > 0): percent = 1+(self.zoom.get() * 0.01)
                else: percent = 1+(self.zoom.get() * 0.005)
                new_w, new_h = self.p.zoom(percent)
                self.dimension = (new_w, new_h)
                self.width['state'] = 'normal'; self.height['state'] = 'normal'
                self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
                self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                self.width['state'] = 'disabled'; self.height['state'] = 'disabled'
        def resize():
            if(self.vaild):
                f = True if(self.width.get("1.0",'end-1c').strip() != '' and self.height.get("1.0",'end-1c').strip() != '') else False
                for i in self.width.get("1.0",'end-1c').strip():
                    if(not i.isdigit()): f = False
                for i in self.height.get("1.0",'end-1c').strip():
                    if(not i.isdigit()): f = False
                if(not f):
                    showwarning("不合理的輸入尺寸!", "寬度或高度可能有其一並未被填寫或是輸入的值並非整數，請重新再試一次!")
                    self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
                    self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                elif(int(self.width.get("1.0",'end-1c')) > 5000 or int(self.height.get("1.0",'end-1c')) > 5000):
                    showwarning("輸入尺寸超出限制!", "寬度或高度可能有其一超出了此應用程式的限制(Max:5000x5000 px)，請重新再試一次!")
                    self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
                    self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                else:
                    self.dimension = (self.width.get("1.0",'end-1c'), self.height.get("1.0",'end-1c'))
                    self.p.resize(tuple(map(int,self.dimension)))
                    self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
                    self.createFilteredImage()
                    self.createFlipedImage()
                    self.getImageSize()
            self.updatePic()
        def check():
            if(self.vaild):
                if(self.chkscale.get()):
                    self.width['state'] = 'disabled'; self.height['state'] = 'disabled'
                    self.zoom['state'] = 'normal'
                else:
                    self.width['state'] = 'normal'; self.height['state'] = 'normal'
                    self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
                    self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                    self.zoom['state'] = 'disabled'
        def getEnglish(self):
            promptL["text"] = "test"
             

        #視窗介面
        self.win.title('OmniImaginer.exe')
        self.win.geometry('1000x563')
        self.win.resizable(0,0)
        self.win.iconbitmap('Image-Converter/Bernie.ico')

        #本地檔案導入方式(LII)
        self.promptL = tk.Label(text="選取本地檔案", bg="grey", fg="white", height=2, width=15)
        self.entryL = tk.Text(height=2, width=45, state="disabled")
        self.btnL = tk.Button(text="...", height=1, width=4, command=self.openFileL)
        self.entryL.place(x=150, y=30)
        self.promptL.place(x=25, y=27)
        self.btnL.place(x=485, y=32)
        #網路檔案導入方式(IUI)
        self.promptU = tk.Label(text="導入網路檔案", bg="grey", fg="white", height=2, width=15)
        self.entryU = tk.Text(height=2, width=45, state="disabled")
        self.btnU = tk.Button(text="...", height=1, width=4, command=self.openFIleU)
        self.entryU.place(x=150, y=80)
        self.promptU.place(x=25, y=77)
        self.btnU.place(x=485, y=82)
        #雲端導入方式(CI)
        self.GDicon = ImageTk.PhotoImage(Image.open('Image-Converter/Drive.png').resize((50,50)))
        self.promptC = tk.Label(text="或者...從雲端導入", bg="grey", fg="white", height=2, width=20)
        self.btnGD = tk.Button(text="Google Drive", image=self.GDicon, command=self.openFileGD)
        self.sva = tk.StringVar()
        self.sva.set('網路狀態: {}'.format("線上" if self.status else "離線"))
        self.dstatus = tk.Label(textvariable = self.sva, fg="green")
        if(not self.status): self.dstatus['fg'] = "red"
        self.updateNetStatus()
        self.promptC.place(x=600, y=15)
        self.dstatus.place(x=810, y=3)
        self.btnGD.place(x=645, y=60)
        #浮水印(L)
        #self.img= ImageTk.PhotoImage(Image.open("uep.png").resize((100,120)))
        self.label = tk.Label(text="浮水印預定放置區塊",bg="grey", fg="white", height=5, width=25)
        self.label.place(x=810, y=25)
        #效果處理器(EP)
            #顯示要疊加上去的顏色的方塊
        self.color_block_label = tk.Label(width=10, text="遮罩顏色預覽:", justify="left")
        self.color_block = tk.Label(width=4, bg="black")
        self.color_block.place(x=110, y=250)
            #疊加按鈕
        self.state = False
        self.color_block_btn = tk.Button(width=5, text="疊加", state='disabled', justify="left", command=update)
        self.color_block_btn2 = tk.Button(width=5, text="撤銷", state='disabled', justify="left", command=update)
        self.color_block_btn.place(x=155, y=247)    
        self.color_block_btn2.place(x=205, y=247)     
            #HSV滑桿的部分
        self.H_label = tk.Label(text="色相:")
        self.S_label = tk.Label(text="飽和度:")
        self.V_label = tk.Label(text="明度:")
        self.H_label.place(x=15, y=139)
        self.S_label.place(x=4, y=179)
        self.V_label.place(x=15, y=219)
        self.H_slider = tk.Scale(from_=0, to=179, length=200, orient=tk.HORIZONTAL, command=hsv)
        self.H_slider.place(x=50, y=120)
        self.S_slider = tk.Scale(from_=0, to=255, length=200, orient=tk.HORIZONTAL, command=hsv)
        self.S_slider.place(x=50, y=160)
        self.V_slider = tk.Scale(from_=0, to=255, length=200, orient=tk.HORIZONTAL, command=hsv)
        self.V_slider.place(x=50, y=200)
            #侵蝕、膨脹的部分
        self.erodebtn = tk.Button(text="侵蝕++", height=2, width=7, command=erode)
        self.erodebtn.place(x=50, y=280)
        self.dilatebtn = tk.Button(text="膨脹++", height=2, width=7, command=dilate)
        self.dilatebtn.place(x=50, y=330)
        self.eddisplay = tk.Label(text="平衡落差:")
        self.eddisplay.place(x=140, y=342)
        self.edv = tk.StringVar()
        self.edv.set('0')
        self.edvalue = tk.Entry(width=4, state=DISABLED, textvariable=self.edv)
        self.edvalue.place(x=200, y=344)
        self.b1 = tk.BooleanVar(); self.b2 = tk.BooleanVar(); self.b3 = tk.BooleanVar()
        self.openingck = tk.Checkbutton(text="去白點", state='disabled', variable=self.b1, command=opening)
        self.openingck.place(x=125, y=285)
        self.closingck = tk.Checkbutton(text="去黑點", state='disabled', variable=self.b2, command=closing)
        self.closingck.place(x=195, y=285)
        self.gradientck = tk.Checkbutton(text="只顯示輪廓", state='disabled', variable=self.b3, command=gradient)
        self.gradientck.place(x=148, y=310)
            #濾波器的部分
        self.clabel = tk.Label(text="其他效果:")
        self.clabel.place(x=25, y=385)
        self.clist = ttk.Combobox(width=12, value=["無", "中值降噪", "高斯模糊", "銳利化", "自適應二值化", "灰階"])
        self.clist.current(0)
        self.clist.place(x=92, y=385)
        self.c_confirm = tk.Button(width=6, text="應用", command=filter)
        self.c_confirm.place(x=213, y=381)
        #尺寸動態顯示(SD)
        self.distext = tk.Label(text="原始圖片尺寸:")
        self.distext.place(x=320, y=130)
        self.display = tk.Label(text="尚未導入!!", height=1, width=20)
        self.display.place(x=321, y=150)
        #方位處理器(PP)
            #縮放的部分
        self.chkscale = tk.BooleanVar()
        self.fixedscale = tk.Checkbutton(text="固定圖片比例", state='disabled', variable=self.chkscale, command=check)
        self.fixedscale.select()
        self.zlabel = tk.Label(text="縮放(?):")
        self.zoom = tk.Scale(from_=-100, to=100, length=200, orient=tk.HORIZONTAL, command=zoom)
        self.zoom.set(0)
        self.tp = Hovertip(self.zlabel,'當固定比例被開啟時才可用')
        self.relabel = tk.Label(text="自訂尺寸:")
        self.relabel.place(x=320, y=252)
        self.width = tk.Text(height=1, width=7, state='disabled')
        self.x = tk.Label(text="x").place(x=385, y=280)
        self.height = tk.Text(height=1, width=7, state='disabled')
        self.s_confirm = tk.Button(text="設定尺寸", command=resize)
        self.s_confirm.place(x=469, y=276)
        self.fixedscale.place(x=423, y=184)
        self.zlabel.place(x=320, y=185)
        self.width.place(x=325, y=282)
        self.zoom.place(x=320, y=203)
        self.height.place(x=403, y=282)
            #旋轉與翻轉的部分
        self.rolabel = tk.Label(text="翻轉:")
        self.rolabel.place(x=320, y=308)
        self.n_flipbtn =tk.Radiobutton(text="不翻轉", value=1, command= lambda x = None: flip(0))
        self.h_flipbtn = tk.Radiobutton(text="水平翻轉", value=2, command= lambda x = None: flip(1))
        self.v_flipbtn = tk.Radiobutton(text="垂直翻轉", value=3, command= lambda x = None: flip(2))
        self.b_flipbtn = tk.Radiobutton(text="水平+垂直", value=4, command= lambda x = None: flip(3))
        self.crolabel = tk.Label(text="旋轉:")
        self.crolabel.place(x=320, y=385)
        self.croinput = tk.Text(height=1, width=4, state='disabled')
        self.degree = tk.Label(text="度")
        self.degree.place(x=385, y=385)
        self.dlist = ttk.Combobox(width=5, state="readonly", value=["順時針", "逆時針"])
        self.d_confirm = tk.Button(text="設定旋轉", command=rotate)
        self.d_confirm.place(x=469, y=382)
        self.dlist.current(0)
        self.n_flipbtn.select()
        self.n_flipbtn.place(x=320, y=330)
        self.h_flipbtn.place(x=420, y=330)
        self.v_flipbtn.place(x=320, y=355)
        self.b_flipbtn.place(x=420, y=355)
        self.croinput.place(x=355, y=388)
        self.dlist.place(x=405, y=386)
        #圖片資訊顯示(ID)
        self.idlabel = tk.Label(text="圖片資訊:")
        self.imgnamedis = tk.Label(text="檔案名稱:")
        self.imgname = tk.Label(text="尚未導入!!")
        self.impwaydis = tk.Label(text="導入方式:")
        self.impway = tk.Label(text="尚未導入!!")
        self.idlabel.place(x=600, y=130)
        self.imgnamedis.place(x=630, y=150)
        self.impwaydis.place(x=630, y=170)
        self.imgname.place(x=688, y=150)
        self.impway.place(x=688, y=170)
        #還原、重作(Un/Redo)
        self.undo = tk.Button(text="還原上一動作")
        self.redo = tk.Button(text="重作上一動作")
        self.undo.place(x=865, y=145)
        self.redo.place(x=865, y=185)
        #圖片預覽(PoI)
        self.plabel = tk.Label(text="預覽圖片:")
        self.plabel.place(x=570, y=200)
        self.img = Image.open('Image-Converter/Preview.png')
        self.tk_img = ImageTk.PhotoImage(self.img.resize((420,300), Image.ANTIALIAS))
        self.preframe = tk.Frame(self.win, width = 440, height = 320).place(x=560, y=220)
        self.preview = tk.Label(image=self.tk_img, width=420, height=300)
        self.preview.place(x=570, y=230)
        #輸出(ExP)
        self.promptE = tk.Label(text="導出檔案", bg="grey", fg="white", height=2, width=71)
        self.promptE.place(x=25, y=430)
        self.localS = tk.Button(text="儲存至電腦", height=2, width=20, command=self.saveL)
        self.localS.place(x=30, y=480)
        self.cloudS = tk.Button(text="上傳至雲端(?)", height=2, width=20, command = self.saveC)
        self.tp2 = Hovertip(self.cloudS, "目前只支援Google雲端硬碟")
        self.cloudS.place(x=200, y=480)
        self.mails = tk.Button(text="寄送給他人", height=2, width=20, command=self.sendM)
        self.mails.place(x=370, y=480)

        #菜單
        self.menu = tk.Menu()

        self.win.config(menu=self.menu)
        self.file = tk.Menu(self.menu, tearoff=0)
        self.file.add_command(label='顯示範例', command=self.example) #程式中顯示範例圖片檔的預覽
        self.file.add_command(label='完全重置', foreground='red', command=self.resetall) #跳出視窗顯示警告，並詢問是否真的要重置

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

        self.lan = tk.Menu(self.menu, tearoff=0)
        self.lan.add_command(label='English', command=self.ENmode)
        self.lan.add_command(label='中文', command=self.CHmode)
        
        self.menu.add_cascade(label='檔案', menu=self.file)
        self.menu.add_cascade(label='視窗', menu=self.window)
        self.menu.add_cascade(label='顯示', menu=self.view)
        self.menu.add_cascade(label='幫助', menu=self.help)
        self.menu.add_cascade(label='語言', menu=self.lan)

    def updateNetStatus(self):
        self.status = self.chknet()
        if(self.lanMode == 'CH'):
            self.sva.set('網路狀態: {}'.format("線上" if self.status else "離線"))
            self.dstatus = tk.Label(textvariable = self.sva, fg="green")
            if(not self.status): self.dstatus['fg'] = "red"
        else:
            self.sva.set('network status: {}'.format("online" if self.status else "offline"))
            self.dstatus = tk.Label(textvariable = self.sva, fg="green")
            if(not self.status): self.dstatus['fg'] = "red"
        
        self.win.after(5000, self.updateNetStatus)
    def chknet(self):
        try:
            requests.get('https://www.google.com',timeout=10)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    def quit(self):
        if(self.lanMode == 'CH'):
            ans = askyesno("結束程式", "你確定要離開了嗎? (Bernie會想你的)")
        else:
            ans = askyesno("Quit", "Are you sure about leaving? (Bernie will miss you!)")
        if(ans): 
            self.win.destroy()
            remove('Image-Converter/Preview.png')
        else: pass

    def sendM(self):
        if(self.vaild):
            if(not self.status):
                showerror('沒有連線!', '你尚未連線到網際網路!')
                return None
            try:
                flag = self.f.sendFileViaMail()
                if(flag): showinfo('寄送成功!!', '您修改過的圖檔已經成功寄送給目標信箱!')
                else: pass
            except Exception as e:
                print(e)
                showerror('寄送失敗!', '發生未知的錯誤導致寄送失敗，我們深感抱歉!')
        else:
            showerror('沒有可用的匯出圖片!', '您尚未匯入任何圖片，請再試一次。')

    def saveL(self):
        if(self.vaild):
            try:
                flag = self.f.saveFileLocal()
                if(flag): showinfo('匯出成功!!', '您修改過的圖檔已經成功儲存至本機!')
                else: pass
            except Exception as e:
                print(e)
                showerror('匯出失敗!', '發生未知的錯誤導致匯出失敗，我們深感抱歉!')
        else:
            showerror('沒有可用的匯出圖片!', '您尚未匯入任何圖片，請再試一次。')

    def saveC(self):
        if(self.vaild):
            if(not self.status):
                showerror('沒有連線!', '你尚未連線到網際網路!')
                return None
            try:
                flag = self.f.saveFileCloud()
                if(flag): showinfo('匯出成功!!', '您修改過的圖檔已經成功儲存至雲端!')
                else: pass
            except Exception as e:
                print(e)
                showerror('匯出失敗!', '發生未知的錯誤導致匯出失敗，我們深感抱歉!')
        else:
            showerror('沒有可用的匯出圖片!', '您尚未匯入任何圖片，請再試一次。')

    def resetall(self):
        ans = askokcancel('你確定嗎?!', '您將要重置Omniimaginer的所有動作，此動作無法返回!', icon = 'error')
        if(ans):
            self.createPreview()
            self.updatePic()
            self.entryL['state'] = NORMAL
            self.entryU['state'] = NORMAL
            self.reset()
            self.entryL['state'] = DISABLED
            self.entryU['state'] = DISABLED
            self.status = self.chknet()
            self.sva.set('網路狀態: {}'.format("線上" if self.status else "離線"))
            if(not self.status): self.dstatus['fg'] = "red"
            else: self.dstatus['fg'] = 'green'
            self.display["text"] = "尚未導入!!"
        else: pass #Not Yet Done

    def example(self):
        image = cv2.imread('Image-Converter/Default Image.png')
        cv2.imwrite("Image-Converter/Preview.png", image)
        file_name = '範例圖片.png'
        importtype = "範例圖片檔案"
        self.entryL['state'] = NORMAL; self.entryU['state'] = NORMAL
        self.vaild = True
        self.reset()
        self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
        self.getImageSize()
        self.updateID(file_name, importtype)
        self.updatePic()
        self.createFlipedImage()

    def reset(self):
        self.entryL.delete(1.0, "end"); self.entryU.delete(1.0, "end")
        self.btnGD['relief'] = RAISED; self.btnGD['state'] = NORMAL
        self.updateID('尚未導入!!', '尚未導入!!')
        self.display['text'] = '尚未導入!!'
        self.color_block['bg'] = 'black'
        self.state = False
        self.H_slider['state'] = 'normal'; self.S_slider['state'] = 'normal'; self.V_slider['state'] = 'normal'
        self.H_slider.set(0); self.S_slider.set(0); self.V_slider.set(0)
        self.openingck.deselect(); self.closingck.deselect(); self.gradientck.deselect()
        self.width['state'] = 'normal'; self.height['state'] = 'normal'
        self.width.delete(1.0, "end"); self.height.delete(1.0, "end")
        self.fixedscale['state'] = 'normal'; self.fixedscale.select(); self.zoom['state'] = 'normal'; self.zoom.set(0);
        self.edv.set('0')
        self.n_flipbtn.select()
        self.dlist.current(0)
        self.clist.current(0)
        if(self.vaild):
            self.openingck['state'] = 'normal'; self.closingck['state'] = 'normal'; self.gradientck['state'] = 'normal'
            self.color_block_btn['state'] = 'normal'; self.color_block_btn2['state'] = 'disabled'
            self.croinput['state'] = 'normal'; self.croinput.delete(1.0, "end")
            self.getImageSize()
            self.width['state'] = 'disabled'; self.height['state'] = 'disabled'
            self.createFlipedImage()
            self.createFilteredImage()
        else:
            self.openingck['state'] = 'disabled'; self.closingck['state'] = 'disabled'; self.gradientck['state'] = 'disabled'
            self.color_block_btn['state'] = 'disabled'; self.color_block_btn2['state'] = 'disabled'
            self.croinput['state'] = 'disabled'
            self.fixedscale.select(); self.fixedscale['state'] = 'disabled'
            self.width['state'] = 'disabled'; self.height['state'] = 'disabled'
        
    def createPreview(self):
        self.vaild = False
        og = cv2.imread("Image-Converter/Default Preview.png")
        cv2.imwrite("Image-Converter/Preview.png", og)    
        
    def accessOriginal(self, mode):
        if(mode == 'Set'):
            self.original = cv2.imread("Image-Converter/Preview.png")
            return None
        if(mode == 'Get'):
            return self.original

    def openFileGD(self):
        if(not self.status):
            showerror('沒有連線!', '你尚未連線到網際網路!')
            return None
        self.tvaild = self.f.loadFileViaDrive()
        if(self.tvaild):
            showinfo('成功!', '雲端檔案已經成功匯入!')
            file_name = 'cloud_img.png'
            importtype = "從雲端硬碟導入"
            self.vaild = True
            self.entryL['state'] = NORMAL; self.entryU['state'] = NORMAL
            self.reset()
            self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
            self.btnGD['relief'] = SUNKEN; self.btnGD['state'] = DISABLED
            self.updateID(file_name, importtype)
        else:
            pass
            #showerror('匯入失敗!', '檔案可能有問題或者伺服器出錯，請再試一次。')
        self.updatePic()
            
    def openFileL(self):
        # msg = "Hello, {}.".format(entry.get())
        cpath = self.f.loadFileLocal()
        importtype = "從本地端導入"
        file_name = path.basename(cpath)
        if(cpath == "" or file_name == "Image-Converter/Preview.png"):
            pass
        else: 
            image = cv2.imdecode(np.fromfile(cpath, dtype=np.uint8), -1);
            cv2.imwrite("Preview.png", image)
            self.vaild = True
            self.entryL['state'] = NORMAL; self.entryU['state'] = NORMAL
            self.reset()
            self.entryL.insert("insert", cpath)
            self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
            self.updateID(file_name, importtype)
        self.updatePic()
        
    def openFIleU(self):
        if(not self.status):
            showerror('沒有連線!', '你尚未連線到網際網路!')
            return None
        self.tvaild, url = self.f.loadFileURL()
        if(self.tvaild): 
            file_name = 'url_image.png'
            importtype = "從URL導入" 
            self.vaild = True
            self.entryL['state'] = NORMAL; self.entryU['state'] = NORMAL
            self.reset()
            self.entryU.insert("insert", url)
            self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
            self.updateID(file_name, importtype)
        else: 
            if(not url): pass 
            else: showerror('匯入失敗!', '檔案可能有問題或者伺服器出錯，請再試一次。')
        self.updatePic()

    def updateID(self, filename, way):
        if(len(filename) > 15): filename = filename[:15] + '...'
        self.imgname['text'] = filename
        self.impway['text'] = way
        pass

    def updatePic(self):
        def cv_imread(file_path):
            cv_pic = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
            return cv_pic
        
        try:
            openpic = cv_imread("Image-Converter/Preview.png")
            realpic = Image.open("Image-Converter/Preview.png")
            lside = 'h' if (max(openpic.shape[0], openpic.shape[1]) == openpic.shape[0]) else 'w'
            ratio = openpic.shape[0]/openpic.shape[1]
            if(lside == 'h'):
                dispic = ImageTk.PhotoImage(realpic.resize((round(300/ratio), 300), Image.ANTIALIAS))
            else:
                dispic = ImageTk.PhotoImage(realpic.resize((420, round(420*ratio)), Image.ANTIALIAS))
        except Exception as e:
            print(e)
            img = Image.open('Image-Converter/Preview.png')
            dispic = ImageTk.PhotoImage(img.resize((420,300), Image.ANTIALIAS))
            self.reset()
            showerror('檔案預覽失敗', '出現未知的問題導致檔案無法顯示，我們深感抱歉。')
        self.preview.imgtk=dispic #換圖片
        self.preview.config(image=dispic)
        #Get picture size and scale it with the preview window (420, 300)

    def createFlipedImage(self):
        self.p.filps[0] = cv2.imread("Image-Converter/Preview.png")
        self.p.filps[1] = cv2.flip(self.p.filps[0], 1)
        self.p.filps[2] = cv2.flip(self.p.filps[0], 0)
        self.p.filps[3] = cv2.flip(self.p.filps[0], -1)
        self.n_flipbtn.select()

    def createFilteredImage(self):
        kernel_1d = cv2.getGaussianKernel(5, 0)
        self.e.filters[0] = cv2.imread("Image-Converter/Preview.png")
        self.e.filters[1] = cv2.medianBlur(self.e.filters[0], 5)
        self.e.filters[2] = cv2.sepFilter2D(self.e.filters[0], -1, kernel_1d, kernel_1d)
        blur_img = cv2.GaussianBlur(self.e.filters[0], (0, 0), 50)
        self.e.filters[3] = cv2.addWeighted(self.e.filters[0], 1.5, blur_img, -0.5, 0)
        self.e.filters[5] = cv2.cvtColor(self.e.filters[0], cv2.COLOR_BGR2GRAY)
        self.e.filters[4] = cv2.adaptiveThreshold(self.e.filters[5], 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        self.clist.current(0)

    def getImageSize(self):
        img = cv2.imread("Image-Converter/Preview.png")
        self.dimension = (img.shape[1], img.shape[0])
        output = "%d x %d" % (self.dimension[0], self.dimension[1])
        self.display["text"] = output + ' (px)'
        self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
        if(self.chkscale.get()): self.zoom.set(0)
        else: 
            self.zoom['state'] = 'normal'
            self.zoom.set(0)
            self.zoom['state'] = 'disabled'

    def ENmode(self):
        self.lanMode = 'EN'
        self.promptL["text"] = "import from \nlocal"
        self.promptU["text"] = "import from \ninternet"
        self.btnU["text"] = "..."
        self.promptC["text"] = "import from \n Google Drive"
        self.sva.set('network status: {}'.format("online" if self.status else "offline"))
        self.label["text"] = "Water Mark"
        self.color_block_label["text"] = "Color filter preview:"
        self.color_block_btn["text"] = "Use"
        self.color_block_btn2["text"] = "Redo"
        self.H_label["text"] = "Hue:"
        self.S_label["text"] = "Saturation:"
        self.V_label["text"] = "Lightness:"
        self.erodebtn["text"] = "Erode(+)"
        self.dilatebtn["text"] = "Dilate(-)"
        self.eddisplay["text"] = "+-:"
        self.openingck["text"] = "Opening"
        self.closingck["text"] = "Closing"
        self.gradientck["text"] = "Gradient"
        self.clabel["text"] = "Other filters:"
        self.clist["value"] = ["None", "Median filter", "Gaussian Blur", "Sharpen", "Binarization", "Grayscale"]
        self.c_confirm["text"] = "Confirm" 
        self.distext["text"] = "Original image size:"
        self.display["text"] = "Image not imported yet"
        self.fixedscale["text"] = "Fixed Scale"
        self.zlabel["text"] = "Enlarge/ Shrink:"
        self.tp = Hovertip(self.zlabel,'Can be used only when "Fixed Scale" is on')
        self.relabel["text"] = "Resize:"
        self.s_confirm["text"] = "Confirm"
        self.rolabel["text"] = "Rotate:"
        self.n_flipbtn["text"] ="None"
        self.h_flipbtn["text"] = "Horizontal"
        self.v_flipbtn["text"] = "Vertical"
        self.b_flipbtn["text"] = "Horizontal + vertical"
        self.crolabel["text"] = ""
        self.degree["text"] = "°"
        self.dlist["value"] = ["clockwise", "anticlockwise"]
        self.d_confirm["text"] = "Confirm"
        self.idlabel["text"] = "Image Info:"
        self.imgnamedis["text"] = "Name:"
        self.imgname["text"] = "Not imported yet"
        self.impwaydis["text"] = "Way:"
        self.impway["text"] = "Not imported yet"
        self.undo["text"] = "Undo"
        self.redo["text"] = "Redo"
        self.plabel["text"] = "Image Preview:"
        self.promptE["text"] = "Export"
        self.localS["text"] = "Save to local"
        self.cloudS["text"] = "Upload to Cloud"
        self.tp2 = Hovertip(self.cloudS, "Only support Google Drive for now")
        self.mails["text"] = "Email to others"

        #菜單


        self.win.config(menu=self.menu)
        self.file.delete('顯示範例')
        self.file.delete('完全重置')
        self.file.add_command(label='Show example', command=self.example) #程式中顯示範例圖片檔的預覽
        self.file.add_command(label='RESET ALL', foreground='red', command=self.resetall) #跳出視窗顯示警告，並詢問是否真的要重置

        self.window.delete('步驟紀錄')
        self.window.delete('開發者資訊')
        self.window.add_command(label='Step record') #跳出新視窗，顯示步驟紀錄
        self.window.add_command(label ='Developer info') #跳出新視窗，顯示開發者資訊

        self.view_options.delete('小')
        self.view_options.delete('中等')
        self.view_options.delete('大')
        self.view.delete('更改視窗大小')
        self.view_options.add_command(label='Small') #變更為小視窗
        self.view_options.add_command(label='Medium') #變更為中等視窗
        self.view_options.add_command(label='Large') #變更為大視窗
        self.view.add_cascade(label='Change window size', menu=self.view_options) #給予更改視窗比例的選項

        self.window.delete('功能介紹')
        self.help.delete('聯絡開發者')
        self.window.add_command(label='Help') #跳出新視窗，顯示一個功能介紹的畫面(Help)
        self.help.add_command(label='Contact') #跳出新視窗，內嵌開發者聯絡資訊(直接寄信?)

        self.menu.delete('檔案')
        self.menu.delete('視窗')
        self.menu.delete('顯示')
        self.menu.delete('幫助')
        self.menu.delete('語言')
        self.menu.add_cascade(label='File', menu=self.file)
        self.menu.add_cascade(label='Window', menu=self.window)
        self.menu.add_cascade(label='View', menu=self.view)
        self.menu.add_cascade(label='Help', menu=self.help)
        self.menu.add_cascade(label='Lan', menu=self.lan)

    def CHmode(self):
        self.lanMode = 'CH'
        self.promptL["text"] = "選取本地檔案"
        self.promptU["text"] = "導入網路檔案"
        self.btnU["text"] = "..."
        self.promptC["text"] = "或者...從雲端導入"
        self.sva.set('network status: {}'.format("線上" if self.status else "離線"))
        self.label["text"] = "浮水印預定放置區塊"
        self.color_block_label["text"] = "遮罩顏色預覽:"
        self.color_block_btn["text"] = "疊加"
        self.color_block_btn2["text"] = "撤銷"
        self.H_label["text"] = "色相:"
        self.S_label["text"] = "飽和度:"
        self.V_label["text"] = "明度:"
        self.erodebtn["text"] = "侵蝕++"
        self.dilatebtn["text"] = "膨脹++"
        self.eddisplay["text"] = "平衡落差:"
        self.openingck["text"] = "去白點"
        self.closingck["text"] = "去黑點"
        self.gradientck["text"] = "只顯示輪廓"
        self.clabel["text"] = "其他效果:"
        self.clist["value"] = ["無", "中值降噪", "高斯模糊", "銳利化", "自適應二值化", "灰階"]
        self.c_confirm["text"] = "應用" 
        self.distext["text"] = "原始圖片尺寸:"
        self.display["text"] = "尚未導入!!"
        self.fixedscale["text"] = "固定圖片比例"
        self.zlabel["text"] = "縮放(?):"
        self.tp = Hovertip(self.zlabel,'當固定比例被開啟時才可用')
        self.relabel["text"] = "自訂尺寸:"
        self.s_confirm["text"] = "設定尺寸"
        self.rolabel["text"] = "翻轉:"
        self.n_flipbtn["text"] ="不翻轉"
        self.h_flipbtn["text"] = "水平翻轉"
        self.v_flipbtn["text"] = "垂直翻轉"
        self.b_flipbtn["text"] = "水平+垂直"
        self.crolabel["text"] = "旋轉:"
        self.degree["text"] = "度"
        self.dlist["value"] = ["順時針", "逆時針"]
        self.d_confirm["text"] = "設定旋轉"
        self.idlabel["text"] = "圖片資訊:"
        self.imgnamedis["text"] = "檔案名稱:"
        self.imgname["text"] = "尚未導入!!"
        self.impwaydis["text"] = "導入方式:"
        self.impway["text"] = "尚未導入!!"
        self.undo["text"] = "還原上一動作"
        self.redo["text"] = "重作上一動作"
        self.plabel["text"] = "預覽圖片:"
        self.promptE["text"] = "導出檔案"
        self.localS["text"] = "儲存至電腦"
        self.cloudS["text"] = "上傳至雲端(?)"
        self.tp2 = Hovertip(self.cloudS, "目前只支援Google雲端硬碟")
        self.mails["text"] = "寄送給他人"

        self.win.config(menu=self.menu)
        self.file.delete('Show example')
        self.file.delete('RESET ALL')
        self.file.add_command(label='顯示範例', command=self.example) #程式中顯示範例圖片檔的預覽
        self.file.add_command(label='完全重置', foreground='red', command=self.resetall) #跳出視窗顯示警告，並詢問是否真的要重置

        self.window.delete('Step record')
        self.window.delete('Developer info')
        self.window.add_command(label='步驟紀錄') #跳出新視窗，顯示步驟紀錄
        self.window.add_command(label ='開發者資訊') #跳出新視窗，顯示開發者資訊

        self.view_options.delete('Small')
        self.view_options.delete('Medium')
        self.view_options.delete('Large')
        self.view.delete('Change window size')
        self.view_options.add_command(label='小') #變更為小視窗
        self.view_options.add_command(label='中等') #變更為中等視窗
        self.view_options.add_command(label='大') #變更為大視窗
        self.view.add_cascade(label='更改視窗大小', menu=self.view_options) #給予更改視窗比例的選項

        self.window.delete('Help')
        self.help.delete('Contact')
        self.window.add_command(label='功能介紹') #跳出新視窗，顯示一個功能介紹的畫面(Help)
        self.help.add_command(label='聯絡開發者') #跳出新視窗，內嵌開發者聯絡資訊(直接寄信?)

        self.menu.delete('File')
        self.menu.delete('Window')
        self.menu.delete('View')
        self.menu.delete('Help')
        self.menu.delete('Lan')
        
        self.menu.add_cascade(label='檔案', menu=self.file)
        self.menu.add_cascade(label='視窗', menu=self.window)
        self.menu.add_cascade(label='顯示', menu=self.view)
        self.menu.add_cascade(label='幫助', menu=self.help)
        self.menu.add_cascade(label='語言', menu=self.lan)
    def open_window(self):
        
        #運行程式
        
        self.win.protocol("WM_DELETE_WINDOW", self.quit)
        self.win.mainloop()

