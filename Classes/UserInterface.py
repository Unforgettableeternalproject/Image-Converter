from tkinter.constants import *
from os import path
import tkinter as tk

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
        #分格-1
        self.upper = tk.Frame(self.win, width=1000, height=171)
        self.lower = tk.Frame(self.win, width=1000, height=392)
        self.upper.grid(column=0, row=0, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        self.lower.grid(column=0, row=1, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        #分格-2
        self.upl = tk.Frame(self.upper, width=561)
        self.upr = tk.Frame(self.upper, width=423)
        self.lol = tk.Frame(self.lower, width=561)
        self.POI = tk.Frame(self.lower, width=423)
        self.upl.grid(column=0, row=0, padx=self.pad/2, pady=self.pad/2, sticky=self.align_mode)
        self.upr.grid(column=1, row=0, padx=self.pad/2, pady=self.pad/2, sticky=self.align_mode)
        self.lol.grid(column=0, row=0, padx=self.pad/2, pady=self.pad/2, sticky=self.align_mode)
        self.POI.grid(column=1, row=0, padx=self.pad/2, pady=self.pad/2, sticky=self.align_mode)
        #分格-3
        self.LII = tk.Frame(self.upl, height=74)
        self.IUI = tk.Frame(self.upl, height=75)
        self.CI = tk.Frame(self.upr, width=99)
        self.L = tk.Frame(self.upr, width=99)
        self.EP = tk.Frame(self.lol, width=258, height=266)
        self.SD = tk.Frame(self.lol, width=295, height=62)
        self.PP = tk.Frame(self.lol, width=295, height=204)
        self.ExP = tk.Frame(self.lol, height=102)
        self.LII.grid(column=0, row=0, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        self.IUI.grid(column=0, row=1, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        self.CI.grid(column=0, row=0, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        self.L.grid(column=1, row=0, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        self.EP.grid(column=0, row=0, rowspan=2, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        self.SD.grid(column=1, row=0, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        self.PP.grid(column=1, row=1, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)
        self.ExP.grid(column=0, row=2, columnspan=2, padx=self.pad/4, pady=self.pad/4, sticky=self.align_mode)

        self.win.mainloop()



