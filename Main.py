import sys, os

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
    UI.ui().open_window()

#f = fm.file_man()
#f.sendFileViaMail()

