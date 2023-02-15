from tkinter.constants import *
from os import path, remove
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter.font as tkFont
from idlelib.tooltip import Hovertip
from tkinter.messagebox import showinfo, showerror, showwarning, askyesno, askokcancel
import requests
import Classes.FileManager as FM
import Classes.EffectProcessor as EP
import Classes.PositionProcessor as PP
import Classes.StepRecord as SR
import numpy as np
import cv2

f = FM.fm()
e = EP.ep()
p = PP.pp()
s = SR.sr()

class ui():

    def __init__(self) -> None:
        self.original = None
        self.valid = False
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

    def chknet(self):
        try:
            requests.get('https://www.google.com',timeout=10)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    def quit(self):
        ans = askyesno("結束程式", "你確定要離開了嗎? (Bernie會想你的)")
        if(ans): 
            self.win.destroy()
            remove('Preview.png')
        else: pass

    def sendM(self):
        if(self.valid):
            if(not self.status):
                showerror('沒有連線!', '你尚未連線到網際網路!')
                return None
            try:
                flag = f.sendFileViaMail()
                if(flag): showinfo('寄送成功!!', '您修改過的圖檔已經成功寄送給目標信箱!')
                else: pass
            except Exception as e:
                print(e)
                showerror('寄送失敗!', '發生未知的錯誤導致寄送失敗，我們深感抱歉!')
        else:
            showerror('沒有可用的匯出圖片!', '您尚未匯入任何圖片，請再試一次。')

    def saveL(self):
        if(self.valid):
            try:
                flag = f.saveFileLocal()
                if(flag): showinfo('匯出成功!!', '您修改過的圖檔已經成功儲存至本機!')
                else: pass
            except Exception as e:
                print(e)
                showerror('匯出失敗!', '發生未知的錯誤導致匯出失敗，我們深感抱歉!')
        else:
            showerror('沒有可用的匯出圖片!', '您尚未匯入任何圖片，請再試一次。')

    def saveC(self):
        if(self.valid):
            if(not self.status):
                showerror('沒有連線!', '你尚未連線到網際網路!')
                return None
            try:
                flag = f.saveFileCloud()
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
        else: pass

    def example(self):
        image = cv2.imread('Default Image.png')
        cv2.imwrite("Preview.png", image)
        file_name = '範例圖片.png'
        importtype = "範例圖片檔案"
        self.entryL['state'] = NORMAL; self.entryU['state'] = NORMAL
        self.valid = True
        self.reset()
        self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
        self.updateID(file_name, importtype)
        self.updatePic()
        self.createFlipedImage()

    def reset(self):
        s.reset()
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
        self.effects = 0
        if(self.valid):
            f = self.getImageSize()
            if(f):
                self.openingck['state'] = 'normal'; self.closingck['state'] = 'normal'; self.gradientck['state'] = 'normal'
                self.color_block_btn['state'] = 'normal'; self.color_block_btn2['state'] = 'disabled'
                self.croinput['state'] = 'normal'; self.croinput.delete(1.0, "end")
                self.width['state'] = 'disabled'; self.height['state'] = 'disabled'
                self.undo['state'] = 'normal'; self.redo['state'] = 'disabled'
                self.createFlipedImage()
                self.createFilteredImage()
                return True
            else: 
                self.vaild = False
                self.createPreview()
                self.updatePic()
                return False
        else:
            self.openingck['state'] = 'disabled'; self.closingck['state'] = 'disabled'; self.gradientck['state'] = 'disabled'
            self.color_block_btn['state'] = 'disabled'; self.color_block_btn2['state'] = 'disabled'
            self.croinput['state'] = 'disabled'
            self.fixedscale.select(); self.fixedscale['state'] = 'disabled'
            self.undo['state'] = 'disabled'; self.redo['state'] = 'disabled'
            self.width['state'] = 'disabled'; self.height['state'] = 'disabled'
            return False
        
    def createPreview(self):
        self.valid = False
        og = cv2.imread("Default Preview.png")
        cv2.imwrite("Preview.png", og)    
        
    def accessOriginal(self, mode):
        if(mode == 'Set'):
            self.original = cv2.imread("Preview.png")
            return None
        if(mode == 'Get'):
            return self.original

    def openFileGD(self):
        if(not self.status):
            showerror('沒有連線!', '你尚未連線到網際網路!')
            return None
        self.tvalid = f.loadFileViaDrive()
        if(self.tvalid):
            showinfo('成功!', '雲端檔案已經成功匯入!')
            file_name = 'cloud_img.png'
            importtype = "從雲端硬碟導入"
            self.valid = True
            self.entryL['state'] = NORMAL; self.entryU['state'] = NORMAL
            if(not self.reset()):
                self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
                return None
            self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
            self.btnGD['relief'] = SUNKEN; self.btnGD['state'] = DISABLED
            self.updateID(file_name, importtype)
            self.updatePic()
            
    def openFileL(self):
        # msg = "Hello, {}.".format(entry.get())
        cpath = f.loadFileLocal()
        importtype = "從本地端導入"
        file_name = path.basename(cpath)
        if(cpath == "" or file_name == "Preview.png"):
            pass
        else: 
            image = cv2.imdecode(np.fromfile(cpath, dtype=np.uint8), -1);
            cv2.imwrite("Preview.png", image)
            self.valid = True
            self.entryL['state'] = NORMAL; self.entryU['state'] = NORMAL
            if(not self.reset()):
                self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
                return None
            self.entryL.insert("insert", cpath)
            self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
            self.updateID(file_name, importtype)
            self.updatePic()
        
    def openFIleU(self):
        if(not self.status):
            showerror('沒有連線!', '你尚未連線到網際網路!')
            return None
        self.tvalid, url = f.loadFileURL()
        if(self.tvalid): 
            file_name = 'url_image.png'
            importtype = "從URL導入" 
            self.valid = True
            self.entryL['state'] = NORMAL; self.entryU['state'] = NORMAL
            if(not self.reset()):
                self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
                return None
            self.entryU.insert("insert", url)
            self.entryL['state'] = DISABLED; self.entryU['state'] = DISABLED
            self.updateID(file_name, importtype)
            self.updatePic()
        else: 
            if(not url): pass 
            else: showerror('匯入失敗!', '檔案可能有問題或者伺服器出錯，請再試一次。')

    def updateID(self, filename, way):
        if(len(filename) > 15): filename = filename[:15] + '...'
        self.imgname['text'] = filename
        self.impway['text'] = way
        pass

    def updatePic(self, skip=False):
        def cv_imread(file_path):
            cv_pic = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
            return cv_pic
        try:
            openpic = cv_imread("Preview.png")
            realpic = Image.open("Preview.png")
            lside = 'h' if (max(openpic.shape[0], openpic.shape[1]) == openpic.shape[0]) else 'w'
            ratio = openpic.shape[0]/openpic.shape[1]
            if(lside == 'h'):
                dispic = ImageTk.PhotoImage(realpic.resize((round(300/ratio), 300), Image.ANTIALIAS))
            else:
                dispic = ImageTk.PhotoImage(realpic.resize((420, round(420*ratio)), Image.ANTIALIAS))
        except Exception as err:
            print(err)
            img = Image.open('Preview.png')
            dispic = ImageTk.PhotoImage(img.resize((420,300), Image.ANTIALIAS))
            self.reset()
            showerror('檔案預覽失敗', '出現未知的問題導致檔案無法顯示，我們深感抱歉。')
        self.preview.imgtk=dispic #換圖片
        self.preview.config(image=dispic)
        if(not skip and self.valid): 
            c = s.add_act((self.valid, self.H_slider.get(), self.S_slider.get(), self.V_slider.get(), self.state, self.edv.get(), self.effects, self.clist.current(), self.chkscale.get(), self.zoom.get(), self.width.get("1.0",'end-1c').strip(), self.height.get("1.0",'end-1c').strip(), self.radio.get(), self.dlist.current()), e.filters, p.flips)
            if(c): self.redo['state'] = 'disabled'
        #Get picture size and scale it with the preview window (420, 300)
        
    def createFlipedImage(self):
        p.flips[0] = cv2.imread("Preview.png")
        p.flips[1] = cv2.flip(p.flips[0], 1)
        p.flips[2] = cv2.flip(p.flips[0], 0)
        p.flips[3] = cv2.flip(p.flips[0], -1)
        self.n_flipbtn.select()

    def createFilteredImage(self):
        kernel_1d = cv2.getGaussianKernel(5, 0)
        e.filters[0] = cv2.imread("Preview.png")
        e.filters[1] = cv2.medianBlur(e.filters[0], 5)
        e.filters[2] = cv2.sepFilter2D(e.filters[0], -1, kernel_1d, kernel_1d)
        blur_img = cv2.GaussianBlur(e.filters[0], (0, 0), 50)
        e.filters[3] = cv2.addWeighted(e.filters[0], 1.5, blur_img, -0.5, 0)
        e.filters[5] = cv2.cvtColor(e.filters[0], cv2.COLOR_BGR2GRAY)
        e.filters[4] = cv2.adaptiveThreshold(e.filters[5], 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        self.clist.current(0)

    def getImageSize(self):
        img = cv2.imread("Preview.png")
        self.dimension = (img.shape[1], img.shape[0])
        if(self.dimension[0] >= 5000 or self.dimension[1] >= 5000 or (self.dimension[0]**2 + self.dimension[1]**2)**0.5 >= 5000):
            showerror("檔案大小超出限制!", "您選擇的圖片檔案的大小可能超出了範圍限制，請選取其他圖片。")
            return False
        output = "%d x %d" % (self.dimension[0], self.dimension[1])
        self.display["text"] = output + ' (px)'
        self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
        if(self.chkscale.get()): self.zoom.set(0)
        else: 
            self.zoom['state'] = 'normal'
            self.zoom.set(0)
            self.zoom['state'] = 'disabled'
        return True

    def open_window(self):
        def hsv(event):
            self.color_block['bg'] = e.changeHSV(self.H_slider.get(), self.S_slider.get(), self.V_slider.get())
        def update():
            if(self.valid):
                self.state = not self.state
                e.updateHSV(self.state)
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
            if(self.valid):
                e.erode()
                self.createFilteredImage()
                self.createFlipedImage()
                self.edv.set(str(int(self.edv.get())+1))
            self.updatePic()
        def dilate():
            if(self.valid):
                e.dilate()
                self.createFilteredImage()
                self.createFlipedImage()
                self.edv.set(str(int(self.edv.get())-1))
            self.updatePic()
        def opening():
            if(self.valid):
                if(b1.get()): #被選取時
                    self.effects = 1
                    self.accessOriginal('Set')
                    e.opening()
                    self.gradientck['state'] = 'disabled'
                    self.closingck['state'] = 'disabled'
                else: #被取消選取時
                    self.effects = 0
                    cv2.imwrite("Preview.png", self.accessOriginal('Get'))
                    self.gradientck['state'] = 'normal'
                    self.closingck['state'] = 'normal'
                self.createFilteredImage()
                self.createFlipedImage()
            self.updatePic()
        def closing():
            if(self.valid):
                if(b2.get()):
                    self.effects = 2
                    self.accessOriginal('Set')
                    e.closing()
                    self.gradientck['state'] = 'disabled'
                    self.openingck['state'] = 'disabled'
                else:
                    self.effects = 0
                    cv2.imwrite("Preview.png", self.accessOriginal('Get'))
                    self.gradientck['state'] = 'normal'
                    self.openingck['state'] = 'normal'
                self.createFilteredImage()
                self.createFlipedImage()
            self.updatePic()
        def gradient():
            if(self.valid):
                if(b3.get()):
                    self.effects = 3
                    self.accessOriginal('Set')
                    e.gradient()
                    self.openingck['state'] = 'disabled'
                    self.closingck['state'] = 'disabled'
                else:
                    self.effects = 0
                    cv2.imwrite("Preview.png", self.accessOriginal('Get'))
                    self.openingck['state'] = 'normal'
                    self.closingck['state'] = 'normal'
                self.createFilteredImage()
                self.createFlipedImage()
            self.updatePic()
        def filter():
            if(self.valid):
                e.filter(self.clist.get())
                self.createFlipedImage()
            self.updatePic()
        def flip():
            if(self.valid): 
                p.flip(self.radio.get())
                self.createFilteredImage()
            self.updatePic()
        def rotate():
            if(self.valid):
                value = self.croinput.get('1.0', 'end-1c').strip()
                f = True if(value != '') else False
                for i in value:
                    if(not i.isdigit()): f = False
                if(f): 
                    if(self.dlist.get() == "順時針"): p.rotate(-(int(value) % 360))
                    else: p.rotate(int(value) % 360)
                else:
                    showwarning("不合理的輸入角度!", "旋轉角度必須要為整數，請再試一次!")
                self.croinput.delete(1.0, "end")
                self.createFilteredImage()
                self.createFlipedImage()
            self.updatePic()
        def zoom(event):
            if(self.valid and self.chkscale.get()):
                if(self.zoom.get() > 0): percent = 1+(self.zoom.get() * 0.01)
                else: percent = 1+(self.zoom.get() * 0.005)
                new_w, new_h = p.zoom(percent)
                self.dimension = (new_w, new_h)
                self.width['state'] = 'normal'; self.height['state'] = 'normal'
                self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
                self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                self.width['state'] = 'disabled'; self.height['state'] = 'disabled'
        def resize():
            if(self.valid):
                f = True if(self.width.get("1.0",'end-1c').strip() != '' and self.height.get("1.0",'end-1c').strip() != '') else False
                for i in self.width.get("1.0",'end-1c').strip():
                    if(not i.isdigit()): f = False
                for i in self.height.get("1.0",'end-1c').strip():
                    if(not i.isdigit()): f = False
                if(not f):
                    showwarning("不合理的輸入尺寸!", "寬度或高度可能有其一並未被填寫或是輸入的值並非整數，請重新再試一次!")
                    self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
                    self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                elif(int(self.width.get("1.0",'end-1c')) > 5000 or int(self.height.get("1.0",'end-1c')) > 5000 or (int(self.height.get("1.0",'end-1c'))**2 + int(self.width.get("1.0",'end-1c'))**2)**0.5 >= 5000):
                    showwarning("輸入尺寸超出限制!", "寬度或高度可能有其一超出了此應用程式的限制(Max:25000000 px square)，請重新再試一次!")
                    self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
                    self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                else:
                    self.dimension = (self.width.get("1.0",'end-1c'), self.height.get("1.0",'end-1c'))
                    p.resize(tuple(map(int,self.dimension)))
                    self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
                    self.createFilteredImage()
                    self.createFlipedImage()
                    self.getImageSize()
            self.updatePic()
        def check():
            if(self.valid):
                if(self.chkscale.get()):
                    self.width['state'] = 'disabled'; self.height['state'] = 'disabled'
                    self.zoom['state'] = 'normal'
                else:
                    self.width['state'] = 'normal'; self.height['state'] = 'normal'
                    self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
                    self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                    self.zoom['state'] = 'disabled'
        def undo():
            #變數紀錄: 已導入?, H值, S值, V值, 是否應用遮罩, 平衡落差, 三種效果的應用狀況, 其他效果的應用狀況, 固定比例, 縮放值, 長, 寬, 翻轉模式, 旋轉模式
            self.redo['state'] = 'normal'
            state, argu, filt, flip = s.undo()
            if(not state): self.undo['state'] = 'disabled'
            if(not argu[0]):#已導入?
                self.valid = 0
                self.entryL['state'] = 'normal'; self.entryU['state'] = 'normal'
                self.reset()
                self.entryL['state'] = 'disabled'; self.entryU['state'] = 'disabled'
                self.createPreview()
                self.updatePic(True)
                return None
            self.H_slider['state'] = 'normal'; self.S_slider['state'] = 'normal'; self.V_slider['state'] = 'normal'
            self.H_slider.set(argu[1]); self.S_slider.set(argu[2]); self.V_slider.set(argu[3])
            if(argu[4]):
                self.H_slider['state'] = 'disabled'; self.S_slider['state'] = 'disabled'; self.V_slider['state'] = 'disabled'
                if(self.color_block_btn['state'] == 'normal'): self.state = not self.state
                self.color_block_btn['state'] = 'disabled'; self.color_block_btn2['state'] = 'normal'
            else:
                if(self.color_block_btn2['state'] == 'normal'): self.state = not self.state
                self.color_block_btn['state'] = 'normal'; self.color_block_btn2['state'] = 'disabled'
            self.edv.set(argu[5])
            self.openingck.deselect(); self.closingck.deselect(); self.gradientck.deselect()
            if(argu[6] == 0):
                self.openingck['state'] = 'normal'; self.closingck['state'] = 'normal'; self.gradientck['state'] = 'normal'
            elif(argu[6] == 1):
                self.openingck['state'] = 'normal'; self.closingck['state'] = 'disabled'; self.gradientck['state'] = 'disabled'
                self.openingck.select()           
            elif(argu[6] == 2):
                self.openingck['state'] = 'disabled'; self.closingck['state'] = 'normal'; self.gradientck['state'] = 'disabled'
                self.closingck.select()
            else:
                self.openingck['state'] = 'disabled'; self.closingck['state'] = 'disabled'; self.gradientck['state'] = 'normal'
                self.gradientck.select()
            self.clist.current(argu[7])
            self.zoom['state'] = 'normal'; self.height['state'] = 'normal'; self.width['state'] = 'normal'
            self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
            if(argu[8]):
                self.fixedscale.select()
                self.zoom.set(argu[9])
                self.dimension = (int(argu[10]), int(argu[11]))
                self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                self.height['state'] = 'disabled'; self.width['state'] = 'disabled'
            else:
                self.fixedscale.deselect()
                self.zoom.set(argu[9])
                self.dimension = (int(argu[10]), int(argu[11]))
                self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                self.zoom['state'] = 'disabled'
            self.display["text"] = "%d x %d (px)" % (self.dimension[0], self.dimension[1])
            self.radio.set(argu[12])
            self.dlist.current(argu[13])
            e.filters = filt; p.flips = flip
            self.updatePic(True)
        def redo():
            self.undo['state'] = 'normal'
            state, argu, filt, flip = s.redo()
            if(not state): self.redo['state'] = 'disabled'
            self.H_slider['state'] = 'normal'; self.S_slider['state'] = 'normal'; self.V_slider['state'] = 'normal'
            self.H_slider.set(argu[1]); self.S_slider.set(argu[2]); self.V_slider.set(argu[3])
            if(argu[4]):
                self.H_slider['state'] = 'disabled'; self.S_slider['state'] = 'disabled'; self.V_slider['state'] = 'disabled'
                if(self.color_block_btn['state'] == 'normal'): self.state = not self.state
                self.color_block_btn['state'] = 'disabled'; self.color_block_btn2['state'] = 'normal'
            else:
                if(self.color_block_btn2['state'] == 'normal'): self.state = not self.state
                self.color_block_btn['state'] = 'normal'; self.color_block_btn2['state'] = 'disabled'
            self.edv.set(argu[5])
            self.openingck.deselect(); self.closingck.deselect(); self.gradientck.deselect()
            if(argu[6] == 0):
                self.openingck['state'] = 'normal'; self.closingck['state'] = 'normal'; self.gradientck['state'] = 'normal'
            elif(argu[6] == 1):
                self.openingck['state'] = 'normal'; self.closingck['state'] = 'disabled'; self.gradientck['state'] = 'disabled'
                self.openingck.select()           
            elif(argu[6] == 2):
                self.openingck['state'] = 'disabled'; self.closingck['state'] = 'normal'; self.gradientck['state'] = 'disabled'
                self.closingck.select()
            else:
                self.openingck['state'] = 'disabled'; self.closingck['state'] = 'disabled'; self.gradientck['state'] = 'normal'
                self.gradientck.select()
            self.clist.current(argu[7])
            self.zoom['state'] = 'normal'; self.height['state'] = 'normal'; self.width['state'] = 'normal'
            self.width.delete('1.0', 'end-1c'); self.height.delete('1.0', 'end-1c')
            if(argu[8]):
                self.fixedscale.select()
                self.zoom.set(argu[9])
                self.dimension = (int(argu[10]), int(argu[11]))
                self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                self.height['state'] = 'disabled'; self.width['state'] = 'disabled'
            else:
                self.fixedscale.deselect()
                self.zoom.set(argu[9])
                self.dimension = (int(argu[10]), int(argu[11]))
                self.width.insert("insert", self.dimension[0]); self.height.insert("insert", self.dimension[1])
                self.zoom['state'] = 'disabled'
            self.display["text"] = "%d x %d" % (self.dimension[0], self.dimension[1]) + ' (px)'
            self.radio.set(argu[12])
            self.dlist.current(argu[13])
            e.filters = filt; p.flips = flip
            self.updatePic(True)

        #視窗介面
        self.win.title('OmniImaginer.exe')
        self.win.geometry('1000x563')
        self.win.resizable(0,0)
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
        self.sva.set('網路狀態: {}'.format("線上" if self.status else "離線"))
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
            #顯示要疊加上去的顏色的方塊
        self.color_block_label = tk.Label(width=10, text="遮罩顏色預覽:", justify="left").place(x=29, y=250)    
        self.color_block = tk.Label(width=4, bg="black")
        self.color_block.place(x=110, y=250)
            #疊加按鈕
        self.state = False
        self.color_block_btn = tk.Button(width=5, text="疊加", state='disabled', justify="left", command=update)
        self.color_block_btn2 = tk.Button(width=5, text="撤銷", state='disabled', justify="left", command=update)
        self.color_block_btn.place(x=155, y=247)    
        self.color_block_btn2.place(x=205, y=247)     
            #HSV滑桿的部分
        self.H_label = tk.Label(text="色相:").place(x=15, y=139)
        self.S_label = tk.Label(text="飽和度:").place(x=4, y=179)
        self.V_label = tk.Label(text="明度:").place(x=15, y=219)
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
        self.eddisplay = tk.Label(text="平衡落差:").place(x=140, y=342)
        self.edv = tk.StringVar()
        self.edv.set('0')
        self.edvalue = tk.Entry(width=4, state=DISABLED, textvariable=self.edv)
        self.edvalue.place(x=200, y=344)
        b1 = tk.BooleanVar(); b2 = tk.BooleanVar(); b3 = tk.BooleanVar()
        self.openingck = tk.Checkbutton(text="去白點", state='disabled', variable=b1, command=opening)
        self.openingck.place(x=125, y=285)
        self.closingck = tk.Checkbutton(text="去黑點", state='disabled', variable=b2, command=closing)
        self.closingck.place(x=195, y=285)
        self.gradientck = tk.Checkbutton(text="只顯示輪廓", state='disabled', variable=b3, command=gradient)
        self.gradientck.place(x=148, y=310)
            #濾波器的部分
        self.clabel = tk.Label(text="其他效果:").place(x=25, y=385)
        self.clist = ttk.Combobox(width=14, state="readonly", value=["無", "中值降噪", "高斯模糊", "銳利化", "自適應二值化", "灰階"])
        self.clist.current(0)
        self.clist.place(x=85, y=385)
        self.c_confirm = tk.Button(width=5, text="應用", command=filter).place(x=213, y=381)
        #尺寸動態顯示(SD)
        self.distext = tk.Label(text="原始圖片尺寸:").place(x=320, y=130)
        self.display = tk.Label(text="尚未導入!!", height=1, width=15)
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
        self.relabel = tk.Label(text="自訂尺寸:").place(x=320, y=252)
        self.width = tk.Text(height=1, width=7, state='disabled')
        self.x = tk.Label(text="x").place(x=385, y=280)
        self.height = tk.Text(height=1, width=7, state='disabled')
        self.s_confirm = tk.Button(text="設定尺寸", command=resize).place(x=469, y=276)
        self.fixedscale.place(x=423, y=184)
        self.zlabel.place(x=320, y=185)
        self.width.place(x=325, y=282)
        self.zoom.place(x=320, y=203)
        self.height.place(x=403, y=282)
            #旋轉與翻轉的部分
        self.rolabel = tk.Label(text="翻轉:").place(x=320, y=308)
        self.radio = tk.IntVar()
        self.n_flipbtn =tk.Radiobutton(text="不翻轉", variable=self.radio, value=0, command=flip)
        self.h_flipbtn = tk.Radiobutton(text="水平翻轉", variable=self.radio, value=1, command=flip)
        self.v_flipbtn = tk.Radiobutton(text="垂直翻轉", variable=self.radio, value=2, command=flip)
        self.b_flipbtn = tk.Radiobutton(text="水平+垂直", variable=self.radio, value=3, command=flip)
        self.crolabel = tk.Label(text="旋轉:").place(x=320, y=385)
        self.croinput = tk.Text(height=1, width=4, state='disabled')
        self.degree = tk.Label(text="度").place(x=385, y=385)
        self.dlist = ttk.Combobox(width=5, state="readonly", value=["順時針", "逆時針"])
        self.d_confirm = tk.Button(text="設定旋轉", command=rotate).place(x=469, y=382)
        self.dlist.current(0)
        self.n_flipbtn.select()
        self.n_flipbtn.place(x=320, y=330); self.h_flipbtn.place(x=420, y=330); self.v_flipbtn.place(x=320, y=355); self.b_flipbtn.place(x=420, y=355)
        self.croinput.place(x=355, y=388)
        self.dlist.place(x=405, y=386)
        #圖片資訊顯示(ID)
        self.idlabel = tk.Label(text="圖片資訊:").place(x=600, y=130)
        self.imgnamedis = tk.Label(text="檔案名稱:").place(x=630, y=150)
        self.imgname = tk.Label(text="尚未導入!!")
        self.impwaydis = tk.Label(text="導入方式:").place(x=630, y=170)
        self.impway = tk.Label(text="尚未導入!!")
        self.imgname.place(x=688, y=150)
        self.impway.place(x=688, y=170)
        #還原、重作(Un/Redo)
        self.undo = tk.Button(text="還原上一動作", state='disabled', command=undo)
        self.redo = tk.Button(text="重作上一動作", state='disabled', command=redo)
        self.undo.place(x=865, y=145)
        self.redo.place(x=865, y=185)
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

