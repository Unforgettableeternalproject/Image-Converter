from tkinter.constants import *
from os import path, remove
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from idlelib.tooltip import Hovertip
from tkinter.messagebox import * 
import requests
import FileManager as FM
import numpy as np
import cv2
import EffectProcessor as EP
#tkinter.messagebox.showinfo(title = 'Hello',message = file_path)

class ui():

    def __init__(self) -> None:
        self.vaild = False
        self.win = tk.Tk()
        self.basepath = path.dirname(path.realpath(__file__))
        self.align_mode = 'nsew'
        self.pad = 8
        self.textvariable = 0
        self.createPreview()
        self.status = self.chknet()
        pass

    def chknet(self):
        try:
            requests.get('https://www.google.com',timeout=10)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    def quit(self):
        ans = askyesno("結束程式", "你確定要離開了嗎? (Bernie會想你的)")
        if(ans): self.win.destroy()
        else: pass

    def sendM(self):
        if(self.vaild):
            if(not self.status):
                showerror('沒有連線!', '你尚未連線到網際網路!')
                return None
            try:
                flag = FM.fm.sendFileViaMail()
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
                flag = FM.fm.saveFileLocal()
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
                flag = FM.fm.saveFileCloud()
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
            self.entryL['state'] = NORMAL
            self.entryU['state'] = NORMAL
            self.clear()
            self.entryL['state'] = DISABLED
            self.entryU['state'] = DISABLED
            self.createPreview()
            self.updatePic()
            self.vaild = False
            self.status = self.chknet()
            self.sva.set('Network Status: {}'.format("Online" if self.status else "Offline"))
            if(not self.status): self.dstatus['fg'] = "red"
            else: self.dstatus['fg'] = 'green'
        else: pass #Not Yet Done

    def example(self):
        image = cv2.imread('Default Image.png')
        cv2.imwrite("Preview.png", image)
        file_name = '範例圖片.png'
        importtype = "範例圖片檔案"
        self.entryL['state'] = NORMAL
        self.entryU['state'] = NORMAL
        self.clear()
        self.entryL['state'] = DISABLED
        self.entryU['state'] = DISABLED
        self.vaild = True
        self.updateID(file_name, importtype)
        self.updatePic()

    def clear(self):
        self.entryL.delete(1.0, "end")
        self.entryU.delete(1.0, "end")
        self.btnGD['relief'] = RAISED
        self.btnGD['state'] = NORMAL
        self.updateID('尚未導入!!', '尚未導入!!')
        
    def createPreview(self):
        self.vaild = False
        original = cv2.imread("Default Preview.png")
        cv2.imwrite("Preview.png", original)       

    def openFileGD(self):
        if(not self.status):
            showerror('沒有連線!', '你尚未連線到網際網路!')
            return None
        self.tvaild = FM.fm.loadFileViaDrive()
        if(self.tvaild):
            showinfo('成功!', '雲端檔案已經成功匯入!')
            file_name = 'cloud_img.png'
            importtype = "從雲端硬碟導入"
            self.vaild = True
            self.entryL['state'] = NORMAL
            self.entryU['state'] = NORMAL
            self.clear()
            self.entryL['state'] = DISABLED
            self.entryU['state'] = DISABLED
            self.btnGD['relief'] = SUNKEN
            self.btnGD['state'] = DISABLED
            self.updateID(file_name, importtype)
        else:
            pass
            showerror('匯入失敗!', '檔案可能有問題或者伺服器出錯，請再試一次。')
        self.updatePic()
            
    def openFileL(self):
        file_path = FM.fm.loadFileLocal()
        file_name = path.basename(file_path)
        if(file_path == ""):
            pass
        else: 
            try:
                image = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imwrite("Preview.png", image)
                importtype = "從本地端導入"
                self.vaild = True
                self.entryL['state'] = NORMAL
                self.entryU['state'] = NORMAL
                self.clear()
                self.entryL.insert("insert", file_path)
                self.entryL['state'] = DISABLED
                self.entryU['state'] = DISABLED
                self.updateID(file_name, importtype)
            except:
                self.createPreview()
                self.clear()
                showerror('匯入失敗!', '檔案可能有問題，請再試一次。')
        self.updatePic()
        
    def openFIleU(self):
        if(not self.status):
            showerror('沒有連線!', '你尚未連線到網際網路!')
            return None
        self.tvaild, url = FM.fm.loadFileURL()
        if(self.tvaild): 
            file_name = 'url_image.png'
            importtype = "從URL導入" 
            self.vaild = True
            self.entryL['state'] = NORMAL
            self.entryU['state'] = NORMAL
            self.clear()
            self.entryU.insert("insert", url)
            self.entryL['state'] = DISABLED
            self.entryU['state'] = DISABLED
            self.updateID(file_name, importtype)
        else: 
            if(not url): pass 
            else: showerror('匯入失敗!', '檔案可能有問題或者伺服器出錯，請再試一次。')
        self.updatePic()

    def updateID(self, filename, way):
        if(len(filename) > 13): filename = filename[:13] + '...'
        self.imgname['text'] = filename
        self.impway['text'] = way
        pass

    def updatePic(self):
        def cv_imread(file_path):
            cv_pic = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
            return cv_pic
        try:
            openpic = cv_imread('Preview.png')
            realpic = Image.open('Preview.png')
            lside = 'h' if (max(openpic.shape[0], openpic.shape[1]) == openpic.shape[0]) else 'w'
            ratio = openpic.shape[0]/openpic.shape[1]
            if(lside == 'h'):
                dispic = ImageTk.PhotoImage(realpic.resize((round(300/ratio), 300), Image.ANTIALIAS))
            else:
                dispic = ImageTk.PhotoImage(realpic.resize((420, round(420*ratio)), Image.ANTIALIAS))
        except Exception as e:
            print(e)
            img = Image.open('Default Preview.png')
            dispic = ImageTk.PhotoImage(img.resize((420,300), Image.ANTIALIAS))
            self.clear()
            showerror('檔案預覽失敗', '出現未知的問題導致檔案無法顯示，我們深感抱歉。')
        self.preview.imgtk=dispic #換圖片
        self.preview.config(image=dispic)
        #Get picture size and scale it with the preview window (420, 300)

    def open_window(self):
        #視窗介面
        self.win.title('OmniImaginer.exe')
        self.win.geometry('1000x563')
        self.win.resizable(False, False)
        self.win.iconbitmap('Bernie.ico')

        #本地檔案導入方式(LII)
        promptL = tk.Label(text="選取本地檔案", bg="grey", fg="white", height=2, width=15)
        self.entryL = tk.Text(height=2, width=45, state="disabled")
        btnL = tk.Button(text="...", height=1, width=4, command=self.openFileL)
        self.entryL.place(x=150, y=30)
        promptL.place(x=25, y=27)
        btnL.place(x=485, y=32)
        #網路檔案導入方式(IUI)
        promptU = tk.Label(text="導入網路檔案", bg="grey", fg="white", height=2, width=15)
        self.entryU = tk.Text(height=2, width=45, state="disabled")
        btnU = tk.Button(text="...", height=1, width=4, command=self.openFIleU)
        self.entryU.place(x=150, y=80)
        promptU.place(x=25, y=77)
        btnU.place(x=485, y=82)
        #雲端導入方式(CI)
        GDicon = ImageTk.PhotoImage(Image.open('Drive.png').resize((50,50)))
        promptC = tk.Label(text="或者...從雲端導入", bg="grey", fg="white", height=2, width=20)
        self.btnGD = tk.Button(text="Google Drive", image=GDicon, command=self.openFileGD)
        self.sva = tk.StringVar()
        self.sva.set('Network Status: {}'.format("Online" if self.status else "Offline"))
        self.dstatus = tk.Label(textvariable = self.sva, fg="green")
        if(not self.status): self.dstatus['fg'] = "red"
        promptC.place(x=600, y=15)
        self.dstatus.place(x=810, y=3)
        self.btnGD.place(x=645, y=60)
        #浮水印(L)
        #self.img= ImageTk.PhotoImage(Image.open("uep.png").resize((100,120)))
        label = tk.Label(text="浮水印預定放置區塊",bg="grey", fg="white", height=5, width=25)
        label.place(x=810, y=25)
        #效果處理器(EP)
            #HSV滑桿的部分
        self.H_label = tk.Label(text="色相:").place(x=15, y=169)
        self.S_label = tk.Label(text="飽和度:").place(x=4, y=209)
        self.V_label = tk.Label(text="明度:").place(x=15, y=249)
        self.H_slider = tk.Scale(from_=0, to=179, length=200, orient=tk.HORIZONTAL, command=EP.ep.changeHSV)
        self.H_slider.place(x=50, y=150)
        self.S_slider = tk.Scale(from_=0, to=255, length=200, orient=tk.HORIZONTAL, command=EP.ep.changeHSV)
        self.S_slider.place(x=50, y=190)
        self.V_slider = tk.Scale(from_=0, to=255, length=200, orient=tk.HORIZONTAL, command=EP.ep.changeHSV)
        self.V_slider.place(x=50, y=230)
        self.H_entry = tk.Entry(width=4, state=DISABLED).place(x=260, y=170) #Entry部分之後會做數值同步
        self.S_entry = tk.Entry(width=4, state=DISABLED).place(x=260, y=210)
        self.V_entry = tk.Entry(width=4, state=DISABLED).place(x=260, y=250)
            #侵蝕、膨脹的部分
        self.erodebtn = tk.Button(text="侵蝕++", height=2, width=7, command=EP.ep.erode)
        self.erodebtn.place(x=50, y=280)
        self.dilatebtn = tk.Button(text="膨脹++", height=2, width=7, command=EP.ep.dilate)
        self.dilatebtn.place(x=50, y=330)
        self.eddisplay = tk.Label(text="平衡落差:").place(x=140, y=342)
        self.edvalue = tk.Entry(width=4, state=DISABLED)
        self.edvalue.place(x=200, y=344)
        self.openingck = tk.Checkbutton(text="去白點", command=EP.ep.opening)
        self.openingck.place(x=125, y=285)
        self.closingck = tk.Checkbutton(text="去黑點", command=EP.ep.closing)
        self.closingck.place(x=195, y=285)
        self.gradientck = tk.Checkbutton(text="只顯示輪廓").place(x=148, y=310)
            #濾波器的部分
        self.clabel = tk.Label(text="其他效果:").place(x=25, y=385)
        self.clist = ttk.Combobox(width=17, state="readonly", value=["無", "Boxblur", "Blur", "Medianblur", "Bilateral", "Gaussian"]).place(x=85, y=385)
            #灰階的部分
        self.gsck = tk.Checkbutton(text="灰階").place(x=235, y=383)
        #尺寸動態顯示(SD)
        self.distext = tk.Label(text="原始圖片尺寸:").place(x=320, y=150)
        self.display = tk.Text(height=1, width=15, state="disabled").place(x=325, y=173)
        #方位處理器(PP)
            #縮放的部分
        self.fixedscale = tk.Checkbutton(text="固定比例")
        self.fixedscale.select()
        self.zlabel = tk.Label(text="縮放:").place(x=320, y=195)
        self.zoom = tk.Scale(from_=1, to=100, length=160, orient=tk.HORIZONTAL).place(x=320, y=215)
        self.Z_entry = tk.Entry(width=4, state=DISABLED).place(x=490, y=235)
        self.ztt = tk.Button(text="?", relief=tk.SUNKEN, height=1)
        self.tp = Hovertip(self.ztt,'當固定比例被開啟時才可用')
        self.relabel = tk.Label(text="自訂尺寸縮放:").place(x=320, y=260)
        self.height = tk.Text(height=1, width=7).place(x=325, y=285)
        self.x = tk.Label(text="x").place(x=385, y=283)
        self.width = tk.Text(height=1, width=7).place(x=403, y=285)
        self.reset = tk.Button(text="重置尺寸").place(x=463, y=280)
        self.fixedscale.place(x=450, y=169)
        self.ztt.place(x=360, y=194)
            #旋轉的部分
        self.rolabel = tk.Label(text="預設旋轉:").place(x=320, y=308)
        self.zero =tk.Radiobutton(text="不旋轉", value=1)
        self.nighty = tk.Radiobutton(text="旋轉90度", value=2).place(x=420, y=330)
        self.horiflip = tk.Radiobutton(text="旋轉180度", value=3).place(x=320, y=355)
        self.twoseventy = tk.Radiobutton(text="旋轉270度", value=4).place(x=420, y=355)
        self.crolabel = tk.Label(text="自訂旋轉角度:").place(x=320, y=385)
        self.croinput = tk.Text(height=1, width=4).place(x=405, y=387)
        self.degree = tk.Label(text="度").place(x=435, y=385)
        self.dlist = ttk.Combobox(width=7, state="readonly", value=["順時針", "逆時針"])
        self.dlist.current(0)
        self.zero.select()
        self.zero.place(x=320, y=330)
        self.dlist.place(x=455, y=385)
        #圖片資訊顯示(ID)
        self.idlabel = tk.Label(text="圖片資訊:").place(x=600, y=150)
        self.imgnamedis = tk.Label(text="檔案名稱:").place(x=630, y=170)
        self.imgname = tk.Label(text="尚未導入!!")
        self.impwaydis = tk.Label(text="導入方式:").place(x=630, y=190)
        self.impway = tk.Label(text="尚未導入!!")
        self.imgname.place(x=688, y=170)
        self.impway.place(x=688, y=190)
        #還原、重作(Un/Redo)
        self.undo = tk.Button(text="還原上一動作").place(x=865, y=145)
        self.redo = tk.Button(text="重作上一動作").place(x=865, y=185)
        #圖片預覽(PoI)
        self.plabel = tk.Label(text="預覽圖片:").place(x=570, y=200)
        img = Image.open('Preview.png')
        tk_img = ImageTk.PhotoImage(img.resize((420,300), Image.ANTIALIAS))
        self.preframe = tk.Frame(self.win, width = 440, height = 320).place(x=560, y=220)
        self.preview = tk.Label(image=tk_img, width=420, height=300)
        self.preview.place(x=570, y=230)
        #輸出(ExP)
        self.promptE = tk.Label(text="導出檔案", bg="grey", fg="white", height=2, width=71).place(x=25, y=430)
        self.localS = tk.Button(text="儲存至電腦", height=2, width=20, command=self.saveL).place(x=30, y=480)
        self.cloudS = tk.Button(text="上傳至雲端(?)", height=2, width=20, command = self.saveC)
        self.tp2 = Hovertip(self.cloudS, "目前只支援Google雲端硬碟")
        self.cloudS.place(x=200, y=480)
        self.mails = tk.Button(text="寄送給他人", height=2, width=20, command=self.sendM).place(x=370, y=480)

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

        self.menu.add_cascade(label='檔案', menu=self.file)
        self.menu.add_cascade(label='視窗', menu=self.window)
        self.menu.add_cascade(label='顯示', menu=self.view)
        self.menu.add_cascade(label='幫助', menu=self.help)
        #運行程式
        self.win.protocol("WM_DELETE_WINDOW", self.quit)
        self.win.mainloop()

ui = ui()

