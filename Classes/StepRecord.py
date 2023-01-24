import cv2

class sr():
    #�ܼƬ���: �w�ɤJ?, H��, S��, V��, �O�_���ξB�n, ���Ÿ��t, �T�خĪG�����Ϊ��p, ��L�ĪG�����Ϊ��p, �T�w���, �Y���, ��, �e, ½��Ҧ�, ����Ҧ�
    def __init__(self) -> None:
        self.preview_rec = [cv2.imread("Default Preview.png")]
        self.argument_rec = [(False, 0, 0, 0, False, '0', 0, 0, True, 0, None, None, 0, 0)]
        self.pointer = 0

    def add_act(self, arguments):
        image = cv2.imread("Preview.png")
        if(self.pointer+1 != len(self.preview_rec)):
            self.preview_rec = self.preview_rec[:self.pointer+1]
            self.argument_rec = self.argument_rec[:self.pointer+1]
        self.preview_rec.append(image)
        self.argument_rec.append(arguments)
        self.pointer+=1

    def undo(self):
        print(self.argument_rec[self.pointer])
        self.pointer-=1
        cv2.imwrite("Preview.png", self.preview_rec[self.pointer])
        if(self.pointer == 0): return False, self.argument_rec[self.pointer] #�̫�
        else: return True, self.argument_rec[self.pointer]

    def redo(self):
        self.pointer+=1
        cv2.imwrite("Preview.png", self.preview_rec[self.pointer])
        if(self.pointer+1 >= len(self.preview_rec)): return False, self.argument_rec[self.pointer] #�̫�
        else: return True, self.argument_rec[self.pointer]

    def reset(self):
        self.preview_rec = [cv2.imread("Default Preview.png")]
        self.argument_rec = [("", "", 0, 0, 0, False, 0, 0, 0, "", True, 0, None, None, 0, 0)]
        self.pointer = 0





