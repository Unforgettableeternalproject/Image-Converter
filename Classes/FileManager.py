from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from tkinter.constants import *
from tkinter.messagebox import *    
import tkinter as tk
from tkinter import filedialog
import tkinter.colorchooser as cc
from urllib.parse import urlparse

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

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
#        self.prompt.protocol("WM_DELETE_WINDOW", disable_event)
        self.prompt.wait_window()
        ret = path.get() if path.get() != "" and self.is_url(path.get()) else "Invalid Input!!!"
        return ret

    def loadFileLocal(self):
        file_path = filedialog.askopenfilename()
        return file_path

    def driveFetch(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)

        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            return "沒有找到任何資料"
        else:
            return items


