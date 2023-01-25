import cv2

class sr():
    #變數紀錄: 已導入?, H值, S值, V值, 是否應用遮罩, 平衡落差, 三種效果的應用狀況, 其他效果的應用狀況, 固定比例, 縮放值, 長, 寬, 翻轉模式, 旋轉模式
    def __init__(self) -> None:
        self.preview_rec = [cv2.imread("Default Preview.png")]
        self.argument_rec = [(False, 0, 0, 0, False, '0', 0, 0, True, 0, None, None, 0, 0, None, None)]
        self.filter_rec = [None]
        self.flip_rec = [None]
        self.pointer = 0
        print('Pointer #{} lead to: {}'.format(self.pointer,self.argument_rec[self.pointer]))

    def add_act(self, arguments, filters, flips):
        cut = False
        image = cv2.imread("Preview.png")
        if(self.pointer+1 != len(self.preview_rec)):
            self.preview_rec = self.preview_rec[:self.pointer+1]
            self.argument_rec = self.argument_rec[:self.pointer+1]
            self.filter_rec = self.filter_rec[:self.pointer+1]
            self.flip_rec = self.flip_rec[:self.pointer+1]
            cut = True
        if(len(self.preview_rec) == 15):
            self.preview_rec = self.preview_rec[1:]
            self.argument_rec = self.argument_rec[1:]
            self.filter_rec = self.filter_rec[1:]
            self.flip_rec = self.flip_rec[1:]
        self.preview_rec.append(image)
        self.argument_rec.append(arguments)
        self.filter_rec.append(filters.copy())
        self.flip_rec.append(flips.copy())
        self.pointer+=1
        print('Pointer #{} lead to: {}'.format(self.pointer, self.argument_rec[self.pointer]))
        return cut

    def undo(self):
        print('Undo action #{}'.format(self.pointer))
        self.pointer-=1
        cv2.imwrite("Preview.png", self.preview_rec[self.pointer])
        if(self.pointer == 0): 
            print('Reached the begining of the list.')
            return False, self.argument_rec[self.pointer], self.filter_rec[self.pointer], self.flip_rec[self.pointer] #最後
        else: return True, self.argument_rec[self.pointer], self.filter_rec[self.pointer], self.flip_rec[self.pointer]

    def redo(self):
        print('Redo action #{}'.format(self.pointer+1))
        self.pointer+=1
        cv2.imwrite("Preview.png", self.preview_rec[self.pointer])
        if(self.pointer+1 >= len(self.preview_rec)): 
            print('Reached the end of the list.')
            return False, self.argument_rec[self.pointer], self.filter_rec[self.pointer], self.flip_rec[self.pointer] #最後
        else: return True, self.argument_rec[self.pointer], self.filter_rec[self.pointer], self.flip_rec[self.pointer]

    def reset(self):
        self.preview_rec = [cv2.imread("Default Preview.png")]
        self.argument_rec = [(False, 0, 0, 0, False, '0', 0, 0, True, 0, None, None, 0, 0, None, None)]
        self.filter_rec = [None]
        self.flip_rec = [None]
        self.pointer = 0





