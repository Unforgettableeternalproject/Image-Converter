import os.path, io, time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from tkinter.constants import *
from tkinter.messagebox import *    
import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.colorchooser as cc
from urllib.parse import urlparse
import requests
from PIL import Image

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
DROPBOX_ACCESS_TOKEN = 'sl.BRdTAQzfjPVBPItFvornCS0d5rYOXsUq8kpviwEk91Y4nmCfphAtNIFB06BN8YNLJG8RDiJtv_CwtX-s4U_W0mRcpgcmXPK1dvurAXGYcY8r_71oouFdnRIyD1kklEGzk2yVl-DO'

class file_man():
    def __init__(self) -> None:
        pass

    def saveFileLocal(self):
        im = Image.open('Preview.png')
        if im.mode != "RGBA":
            im = im.convert("RGBA")
        txt = Image.new('RGBA', im.size, (255,255,255,0))
        file = filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=(("png 檔案", "*.png"),("jpg 檔案","*.jpg"),("jpeg 檔案","*.jpeg"),("bmp 檔案", '*.bmp'),("所有檔案", "*.*")))
        if file:
            tpe = 'png'
            if('.jpg' in file.name): tpe = 'jpg'
            if('.jpeg' in file.name): tpe = 'jpeg'
            if('.bmp' in file.name): tpe = 'bmp'
            abs_path = os.path.abspath(file.name)
            out = Image.alpha_composite(im, txt)
            out.save(abs_path, tpe) # saves the image to the input file name. 

    def loadFileViaDropbox(self):
        pass

    def loadFileViaDrive(self):
        def chkpath():
            
            try:
                fid = file_id[display.index(file_name.get())]
            except:
                fid = ''
            if (file_name.get() == "" or not self.is_ImageFile(fid)):
                self.alertmsg.set("The file was not an image.")
            else:
                self.msglabel['fg'] = 'forestgreen'
                self.alertmsg.set("Trying to download...")
                self.promptD.update()
                try:
                    self.path = self.driveDownload(fid)
                    self.promptD.update()
                    self.promptD.destroy()
                except Exception:
                    self.msglabel['fg'] = 'maroon'
                    self.alertmsg.set("Unknown error occured, please try another file.")

        self.path = tk.StringVar()
        self.promptD = tk.Toplevel()
        self.promptD.iconbitmap('Bernie.ico')
        self.promptD.title("Google Drive File Selector")
        self.promptD.geometry('350x150')
        self.promptD.resizable(0,0)
        global item_list
        try:       
            item_list = self.driveFetch() #如果沒有資料就跳出錯誤視窗 
            if (len(item_list) == 0): 
                showerror('檔案錯誤', '沒有使用者最近存取的檔案!')
                self.promptD.destroy()
        except:
            showerror('檔案錯誤', '存取雲端硬碟時出現錯誤!')
            self.promptD.destroy()
        display = [x['name'] for x in item_list]
        file_id = [x['id'] for x in item_list]
        Cs = tk.Frame(self.promptD, width=200, height=200)
        Cs.pack()
        file_name = tk.StringVar()
        self.alertmsg = tk.StringVar()
        inputlabel = tk.Label(Cs, text="Choose a file from below (Must be an image):")
        userchoosefrom = ttk.Combobox(Cs, textvariable=file_name, width=17, state="readonly", value=display)
        yrbtn = tk.Button(Cs, text="Confirm", width=20, bg='lightslategrey', fg='gainsboro', command=chkpath)
        self.msglabel = tk.Label(Cs, textvariable=self.alertmsg, fg='maroon')
        self.progress = ttk.Progressbar(Cs, length=200, mode='determinate')
        inputlabel.pack()
        userchoosefrom.pack()
        yrbtn.pack()
        self.msglabel.pack()
        self.progress.pack()
        self.promptD.wait_window()
        ret = self.path if self.path != "" else "None"
        return str(ret), file_name.get()

    def loadFileURL(self):
        supported_files = ['.jpg', '.png', '.jpeg', '.bmp', '.webp', '.heic']
        self.mimetype = ''
        filename = ''
        def is_url(url):
            try:
                result = urlparse(url)
                return all([result.scheme, result.netloc])
            except ValueError:
                return False

        def chkpath():
            if(path.get() == ""):
                alertmsg.set("Please enter a image URL.")
            else:
                if(not is_url(path.get())):
                    alertmsg.set("Please enter a VALID image URL.")
                else:
                    for i in supported_files:
                        if(i in path.get()):
                            self.mimetype = i
                            break
                    if self.mimetype != '':
                        img_data = requests.get(path.get()).content
                        with open("url_image" + self.mimetype, "wb") as handler:
                            handler.write(img_data)
                        prompt.destroy()
                        prompt.update()
                    else: alertmsg.set("Please enter a VALID image URL.")

        prompt = tk.Toplevel()
        prompt.iconbitmap('Bernie.ico')
        prompt.title("Image URL Fetcher")
        prompt.geometry('350x150')
        prompt.resizable(0,0)
        Cs = tk.Frame(prompt, width=200, height=200)
        Cs.pack()
        path = tk.StringVar()
        alertmsg = tk.StringVar()
        inputlabel = tk.Label(Cs, text="Enter Image URL:")
        userkeyin = tk.Entry(Cs, textvariable=path)
        yrbtn = tk.Button(Cs, text="Confirm", width=20, bg='lightslategrey', fg='gainsboro', command=chkpath)
        msglabel = tk.Label(Cs, textvariable=alertmsg, fg='maroon')
        inputlabel.pack()
        userkeyin.pack()
        yrbtn.pack()
        msglabel.pack()
        prompt.wait_window()
        filename = "url_image" + self.mimetype if self.mimetype != '' else "Invalid Input!!!"
        ret = os.path.realpath(filename) if filename != 'Invalid Input!!!' else ''
        return ret, filename

    def loadFileLocal(self):
        file_path = filedialog.askopenfilename(filetypes = (("png 檔案","*.png*"),("jpg 檔案","*.jpg"),("jpeg 檔案","*.jpeg"),("bmp 檔案", '*.bmp'),("所有檔案", "*.*")))
        return file_path

    def driveDownload(self, id):
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
                token.write(creds.to_json()) #這裡之後會改，但為了測試我先用我的就好

        service = build('drive', 'v3', credentials=creds)
        request = service.files().get_media(
            fileId=id,
            supportsAllDrives=True,
        )
        file_metadata = service.files().get(
            fileId = id,
            fields="id, name, mimeType, size, parents",
            supportsAllDrives=True,
        ).execute()
        final_filename = file_metadata["name"]
        with io.FileIO(final_filename, "wb") as fh:
            #self.alertmsg = "Start downloading..."
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                #self.alertmsg = f"{final_filename} Downloading {status.progress()*100:7.2f}%."
                #self.progress['value'] = status.progress()*100
                #self.promptD.update()
        #self.alertmsg = "Download completed!"
        return final_filename

    def is_ImageFile(self, id):
        supported_files = ['image/jpg', 'image/png', 'image/jpeg', 'image/bmp', 'image/webp', 'image/heic']
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
                token.write(creds.to_json()) #這裡之後會改，但為了測試我先用我的就好

        service = build('drive', 'v3', credentials=creds)
        try:
            file_metadata = service.files().get(
            fileId = id,
            fields="id, name, mimeType, size, parents",
            supportsAllDrives=True,
            ).execute()
    
            file_mimeType = file_metadata.get("mimeType")
            return file_mimeType in supported_files
        except:
            return False

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
                token.write(creds.to_json()) #這裡之後會改，但為了測試我先用我的就好

        service = build('drive', 'v3', credentials=creds)

        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            return "沒有找到任何資料"
        else:
            return items