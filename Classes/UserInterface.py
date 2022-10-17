from tkinter.constants import *
from os import path
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import PhotoImage, filedialog
from tkinter import ttk
from idlelib.tooltip import Hovertip

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
        self.promptL = tk.Label(text="選取本地檔案", bg="grey", fg="white", height=2, width=15).place(x=25, y=27)
        self.entryL = tk.Text(height=2, width=45)
        self.entryL['state'] = DISABLED
        self.btnL = tk.Button(text="...", height=1, width=4,command=self.OnopenFile).place(x=485, y=32)
        self.entryL.place(x=150, y=30)
        #網路檔案導入方式(IUI)
        self.promptU = tk.Label(text="導入網路檔案", bg="grey", fg="white", height=2, width=15).place(x=25, y=77)
        self.entryU = tk.Text(height=2, width=45)
        self.entryU['state'] = DISABLED
        self.btnU = tk.Button(text="...", height=1, width=4).place(x=485, y=82)
        self.entryU.place(x=150, y=80)
        #雲端導入方式(CI)
        self.GDicon = ImageTk.PhotoImage(Image.open('Drive.png').resize((50,50)))
        self.DBicon = ImageTk.PhotoImage(Image.open('Dropbox.png').resize((50,50)))
        self.promptC = tk.Label(text="或者...從雲端導入", bg="grey", fg="white", height=2, width=20).place(x=600, y=15)
        self.btnGD = tk.Button(text="Google Drive", image=self.GDicon).place(x=610, y=60)
        self.btnDB = tk.Button(text="Dropbox", image = self.DBicon).place(x=680, y=60)
        #浮水印(L)
        #self.img= ImageTk.PhotoImage(Image.open("uep.png").resize((100,120)))
        self.label = tk.Label(text="浮水印預定放置區塊",bg="grey", fg="white", height=5, width=20).place(x=800, y=25)
        #效果處理器(EP)
            #HSV滑桿的部分
        self.H_label = tk.Label(text="色相:").place(x=15, y=169)
        self.S_label = tk.Label(text="飽和度:").place(x=4, y=209)
        self.V_label = tk.Label(text="明度:").place(x=15, y=249)
        self.H_slider = tk.Scale(from_=0, to=360, length=200, orient=tk.HORIZONTAL).place(x=50, y=150)
        self.S_slider = tk.Scale(from_=0, to=100, length=200, orient=tk.HORIZONTAL).place(x=50, y=190)
        self.V_slider = tk.Scale(from_=0, to=100, length=200, orient=tk.HORIZONTAL).place(x=50, y=230)
        self.H_entry = tk.Entry(width=4, state=DISABLED).place(x=260, y=170) #Entry部分之後會做數值同步
        self.S_entry = tk.Entry(width=4, state=DISABLED).place(x=260, y=210)
        self.V_entry = tk.Entry(width=4, state=DISABLED).place(x=260, y=250)
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
        self.imgname = tk.Label(text="尚未導入!!").place(x=688, y=170)
        self.impwaydis = tk.Label(text="導入方式:").place(x=630, y=190)
        self.impway = tk.Label(text="尚未導入!!").place(x=688, y=190)
        #還原、重作(Un/Redo)
        self.undo = tk.Button(text="還原上一動作").place(x=865, y=145)
        self.redo = tk.Button(text="重作上一動作").place(x=865, y=185)
        #圖片預覽(PoI)
        img = Image.open('Preview.png')
        tk_img = ImageTk.PhotoImage(img.resize((420,300), Image.ANTIALIAS))
        self.preview = tk.Label(image=tk_img, width=420, height=300)
        self.preview.place(x=570, y=230)
        #輸出(ExP)
        self.promptE = tk.Label(text="導出檔案", bg="grey", fg="white", height=2, width=71).place(x=25, y=430)
        self.locals = tk.Button(text="下載至電腦", height=2, width=20).place(x=30, y=480)
        self.clouds = tk.Button(text="上傳至雲端", height=2, width=20)
        self.tp2 = Hovertip(self.clouds, "目前只支援Google雲端硬碟")
        self.clouds.place(x=200, y=480)
        self.mails = tk.Button(text="寄送給他人", height=2, width=20).place(x=370, y=480)

        #菜單
        self.menu = tk.Menu()

        self.win.config(menu=self.menu)
        self.file = tk.Menu(self.menu, tearoff=0)
        self.file.add_command(label='顯示範例') #程式中顯示範例圖片檔的預覽
        self.file.add_command(label='完全重置', foreground='red') #跳出視窗顯示警告，並詢問是否真的要重置

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



