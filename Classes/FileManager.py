import os.path, io, smtplib, re
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from tkinter.constants import *
from tkinter.messagebox import *    
import tkinter as tk
from tkinter import filedialog, ttk
from urllib.parse import urlparse
import requests
from PIL import Image

SCOPES = ['https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.readonly']
DROPBOX_ACCESS_TOKEN = 'sl.BRdTAQzfjPVBPItFvornCS0d5rYOXsUq8kpviwEk91Y4nmCfphAtNIFB06BN8YNLJG8RDiJtv_CwtX-s4U_W0mRcpgcmXPK1dvurAXGYcY8r_71oouFdnRIyD1kklEGzk2yVl-DO'
DEFAULT_MAIL_ADRESS = 'ptyc4076@gmail.com'
DEFAULT__MAIL_TOKEN = 'yvjzdurxghiehhbv'

class file_man():
    def __init__(self) -> None:
        self.creds = None
        pass

    def sendFileViaMail(self):
        self.vaild = False
        def quit():
            if(not mail_to.get() and not subject.get('1.0', 'end-1c') and not content.get('1.0', 'end-1c')):
                promptM.destroy()
            else:
                ans = askyesno("結束寄送程序?", "您的郵件尚未寄送，如果結束則不會儲存你的變更，是否要結束?", icon='warning')
                if(ans): promptM.destroy()
                else: pass
        def send():
            try:
                msg = MIMEMultipart()
                info = MIMEText(content.get('1.0', 'end-1c').strip(), 'plain', 'utf-8')
                msg.attach(info)
                with open('Preview.png', 'rb') as fp:
                    img = MIMEImage(fp.read())
                msg.attach(img)
                msg['Subject'] = subject.get('1.0', 'end-1c').strip()
                msg['From'] = DEFAULT_MAIL_ADRESS
                msg['To'] = mail_to.get()

                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(DEFAULT_MAIL_ADRESS, DEFAULT__MAIL_TOKEN)
                server.send_message(msg)
                server.quit()
                self.vaild = True
            except Exception as e:
                print(e)
                showerror("發生錯誤!", "寄送時發生錯誤，可能是電子郵件地址並不存在，請稍後再試.")
            promptM.update()
            promptM.destroy()
        def verify():
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if(not re.fullmatch(regex, mail_to.get())):
                alertmsg.set("Please enter a valid email adress!")
            else:
                if(not subject.get('1.0', 'end-1c') or not content.get('1.0', 'end-1c')):
                    ans = askyesno('您有資料沒有填寫!', '您有主旨或內容並沒有填寫，要繼續寄送嗎?', icon = 'warning')
                    if(ans): send()
                    else: pass
                else: send()
            pass
        mail_to = tk.StringVar()
        alertmsg = tk.StringVar()
        promptM = tk.Toplevel()
        promptM.iconbitmap('Bernie.ico')
        promptM.title("Image Sender")
        promptM.geometry('500x500')
        promptM.resizable(0,0)
        Cs = tk.Frame(promptM, width=200, height=200)
        Cs.pack()
        t = 50
        display = tk.Label(promptM, text="Mail To:").place(x=60, y=48+t)
        sub_display = tk.Label(promptM, text="Subject:").place(x=60, y=83+t)
        con_display = tk.Label(promptM, text='Content:\n(Image\nincluded!)').place(x=56, y=160+t)
        mail = tk.Entry(promptM, textvariable=mail_to, width=40).place(x=130, y=50+t)
        subject = tk.Text(promptM, width=40, height=2)
        content = tk.Text(promptM, width=40, height=10)
        button = tk.Button(promptM, text="Confirm and Send", width=40, bg='lightslategrey', fg='gainsboro', command=verify).place(x=100, y=280+t)
        msglabel = tk.Label(promptM, textvariable=alertmsg, fg='maroon').place(x=130, y=20+t)
        subject.place(x=130, y=80+t)
        content.place(x=130, y=120+t)
        promptM.protocol("WM_DELETE_WINDOW", quit)
        promptM.wait_window()
        return self.vaild

    def saveFileLocal(self):
        im = Image.open('Preview.png')
        file = filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=(("png 檔案", "*.png"),("jpeg 檔案","*.jpeg"),("bmp 檔案", '*.bmp'),("所有檔案", "*.*")))
        if file:
            tpe = 'png'
            if('.jpeg' in file.name): tpe = 'jpeg'
            if('.bmp' in file.name): tpe = 'bmp'
            abs_path = os.path.abspath(file.name)
            im.save(abs_path, tpe) # saves the image to the input file name. 
            return True
        else: return False

    def saveFileCloud(self):
        mimty = 'image/png'
        self.vaild = False
        def uploadFile(mimty):
            file_metadata = {
            'name': name.get(),
            'mimeType': mimty
            }
            media = MediaFileUpload('Preview.png',
                                    mimetype=mimty,
                                    resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            self.vaild = True
       
        def setvariables():
            if not name.get():
                alertmsg.set("Please enter a file name!!")
                print('no')
            else:
                if(typsel.get() == 'png 檔案'): mimty = 'image/png'
                if(typsel.get() == 'jpeg 檔案'): mimty = 'image/jpeg'
                if(typsel.get() == 'bmp 檔案'): mimty = 'image/bmp'
                try:
                    uploadFile(mimty)
                    promptD2.update()
                    promptD2.destroy()
                except Exception as e:
                    print(e)
            pass

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

        service = build('drive', 'v3', credentials=self.creds)
        
        name = tk.StringVar()
        alertmsg = tk.StringVar()
        promptD2 = tk.Toplevel()
        promptD2.iconbitmap('Bernie.ico')
        promptD2.title("Google Drive File Uploader")
        promptD2.geometry('350x150')
        promptD2.resizable(0,0)
        Cs = tk.Frame(promptD2, width=200, height=200)
        Cs.pack()
        inputlabel = tk.Label(Cs, text="Enter your file name and type:")
        entry = tk.Entry(Cs, textvariable=name)
        typsel = ttk.Combobox(Cs, width=17, state="readonly", value=['png 檔案', 'jpeg 檔案', 'bmp 檔案'])
        typsel.current(0)
        button = tk.Button(Cs, text="Submit", width=20, bg='lightslategrey', fg='gainsboro', command=setvariables)
        msglabel = tk.Label(Cs, textvariable=alertmsg, fg='maroon')
        inputlabel.pack()
        entry.pack()
        typsel.pack()
        button.pack()
        msglabel.pack()
        promptD2.wait_window()
        return self.vaild

    def loadFileViaDrive(self):
        self.vaild = False
        def chkpath():
            try:
                fid = file_id[display.index(file_name.get())]
            except:
                fid = ''
            if (file_name.get() == "" or not self.is_ImageFile(fid)):
                alertmsg.set("The file was not an image.")
            else:
                msglabel['fg'] = 'forestgreen'
                alertmsg.set("Trying to download...")
                promptD.update()
                try:
                    msg = self.driveDownload(fid)
                    alertmsg.set(msg)
                    promptD.update()
                    promptD.destroy()
                    self.vaild = True
                except Exception:
                    msglabel['fg'] = 'maroon'
                    alertmsg.set("Unknown error occured, please try another file.")

        promptD = tk.Toplevel()
        promptD.iconbitmap('Bernie.ico')
        promptD.title("Google Drive File Selector")
        promptD.geometry('350x150')
        promptD.resizable(0,0)
        global item_list
        try:       
            item_list = self.driveFetch() #如果沒有資料就跳出錯誤視窗 
            if (len(item_list) == 0): 
                showerror('檔案錯誤', '沒有使用者最近存取的檔案!')
                promptD.destroy()
        except:
            showerror('檔案錯誤', '存取雲端硬碟時出現錯誤!')
            promptD.destroy()
        display = [x['name'] for x in item_list]
        file_id = [x['id'] for x in item_list]
        Cs = tk.Frame(promptD, width=200, height=200)
        Cs.pack()
        file_name = tk.StringVar()
        alertmsg = tk.StringVar()
        inputlabel = tk.Label(Cs, text="Choose a file from below (Must be an image):")
        userchoosefrom = ttk.Combobox(Cs, textvariable=file_name, width=17, state="readonly", value=display)
        yrbtn = tk.Button(Cs, text="Confirm", width=20, bg='lightslategrey', fg='gainsboro', command=chkpath)
        msglabel = tk.Label(Cs, textvariable=alertmsg, fg='maroon')
        inputlabel.pack()
        userchoosefrom.pack()
        yrbtn.pack()
        msglabel.pack()
        promptD.wait_window()
        return self.vaild

    def loadFileURL(self):
        supported_files = ['.jpg', '.png', '.jpeg', '.bmp', '.webp', '.heic']
        self.vaild = False
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
                    ftype = ''
                    for i in supported_files:
                        if(i in path.get()):
                            ftype = i
                            break
                    if ftype != '':
                        try:
                            img_data = requests.get(path.get()).content
                            with open("Preview.png", "wb") as handler:
                                handler.write(img_data) 
                            self.vaild = True
                        except:
                            pass
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
        #print(ftype)
        ##filename = "url_img" + ftype if ftype != '' else "Invalid Input!!!"
        #ret = os.path.realpath(filename) if filename != 'Invalid Input!!!' else ''
        return self.vaild, path.get()

    def loadFileLocal(self):
        file_path = filedialog.askopenfilename(filetypes = (("png 檔案","*.png*"),("jpg 檔案","*.jpg"),("jpeg 檔案","*.jpeg"),("bmp 檔案", '*.bmp'),("所有檔案", "*.*")))
        return file_path

    def driveDownload(self, id):
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
        service = build('drive', 'v3', credentials=self.creds)
        request = service.files().get_media(
            fileId=id,
            supportsAllDrives=True,
        )
        file_metadata = service.files().get(
            fileId = id,
            fields="id, name, mimeType, size, parents",
            supportsAllDrives=True,
        ).execute()
        mp = {'image/jpg':'.jpg', 'image/png':'.png', 'image/jpeg':'.jpeg', 'image/bmp':'.bmp', 'image/webp':'.webp', 'image/heic':'.heic'}
        #final_filename = 'cloud_img' + mp[file_metadata['mimeType']]
        final_filename = 'Preview.png'
        with io.FileIO(final_filename, "wb") as fh:
            #self.alertmsg = "Start downloading..."
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
        return "Download completed!"

    def is_ImageFile(self, id):
        supported_files = ['image/jpg', 'image/png', 'image/jpeg', 'image/bmp', 'image/webp', 'image/heic']
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
        service = build('drive', 'v3', credentials=self.creds)
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
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
        service = build('drive', 'v3', credentials=self.creds)

        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            return "沒有找到任何資料"
        else:
            return items