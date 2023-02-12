import sys, os
from ctypes import windll
import Classes.Language as Language
#windll.shcore.SetProcessDpiAwareness(1)

def checkReqPackages():
    with open("requirements.txt", mode = "r", encoding = "utf-8") as file:
        for i in file.readlines():
            temp = i.split(" == ")
            packageName = temp[0]
            if(packageName not in sys.modules):
                os.system('python -m pip install {}'.format(packageName))
            else:
                print("{} is already installed".format(packageName))

if __name__ == "__main__":
    import Classes.UserInterface as UI
    import Classes.FileManager as FM
    UI = UI.ui()
    UI.open_window()
    
    

#meow
#f = fm.file_man()
#f.sendFileViaMail()

