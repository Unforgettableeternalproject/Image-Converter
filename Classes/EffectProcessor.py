from PIL import Image,ImageDraw,ImageFont
import cv2
import Classes.UserInterface as UI

u = UI.ui()
class eff_pro():
    def __init__(self) -> None:
        pass
    #依照滑桿的值改H
    def changeH(event):
        image = cv2.imread("Preview.png")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        newH = u.H_slider.get()

        image[:, :, 0] = newH

        out = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        cv2.imwrite("Preview.png", out)
        u.updatePic()

    #依照滑桿的值改S
    def changeS(event):
        image = cv2.imread("Preview.png")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        newS = uS_slider.get()
            
        UI.ui.S_slider.set(image[:, :, 1])
            
        image[:, :, 1] = newS

        out = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        cv2.imwrite("Preview.png", out)
        UI.ui.updatePic()

    #依照滑桿的值改V            
    def changeV(event):
        image = cv2.imread("Preview.png")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        newV = UI.ui.V_slider.get()

        UI.ui.V_slider.set(image[:, :, 2])

        image[:, :, 2] = newV

        out = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        cv2.imwrite("Preview.png", out)
        UI.ui.updatePic()