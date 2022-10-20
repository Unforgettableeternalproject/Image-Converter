import Classes.UserInterface as ui
import Classes.FileManager as fm

#u = ui.ui()
#u.open_window()
f = fm.file_man()
file = f.dropboxFetch()
for i in file: print(i)

