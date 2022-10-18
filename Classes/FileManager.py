from tkinter.constants import *
from tkinter.messagebox import *
import tkinter as tk
from tkinter import filedialog
import tkinter.colorchooser as cc
from urllib.parse import urlparse

class file_man():
    def __init__(self) -> None:
        pass

    def is_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def loadFileURL(self):
        def disable_event():
            pass
        
        def chkpath():
            if(path.get() == ""):
                alertmsg.set("Please enter a image URL.")
            else:
                if(not self.is_url(path.get())):
                    alertmsg.set("Please enter a VALID image URL.")
                else:
                    self.prompt.destroy()
                    self.prompt.update()

        self.prompt = tk.Toplevel()
        self.prompt.iconbitmap('Bernie.ico')
        self.prompt.title("Image URL Fetcher")
        self.prompt.geometry('350x150')
        self.prompt.resizable(0,0)
        Cs = tk.Frame(self.prompt, width=200, height=200)
        Cs.pack()
        path = tk.StringVar()
        alertmsg = tk.StringVar()
        inputlabel = tk.Label(Cs, text="Enter Image URL:")
        userkeyin = tk.Entry(Cs, textvariable=path)
        yrbtn = tk.Button(Cs, text="Confirm", width=20, bg='lightslategrey', fg='gainsboro')
        msglabel = tk.Label(Cs, textvariable=alertmsg, fg ='maroon')
        inputlabel.pack()
        userkeyin.pack()
        yrbtn.pack()
        msglabel.pack()
        
        yrbtn['command'] = chkpath
        self.prompt.protocol("WM_DELETE_WINDOW", disable_event)
        self.prompt.wait_window()
        return path.get()

    def loadFileLocal(self):
        file_path = filedialog.askopenfilename()
        return file_path



