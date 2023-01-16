from PIL import Image,ImageDraw,ImageFont
import cv2
import UserInterface as UI
import numpy as np

class ep():
    
    def changeHSV(self, event):
        def _from_rgb(r, g, b):
            return "#%02x%02x%02x" % (r, g, b)   
        image = cv2.imread("Image-Converter/Preview.png")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


        image[:, :, 0] = UI.ui.H_slider.get()
        image[:, :, 1] = UI.ui.S_slider.get()
        image[:, :, 2] = UI.ui.V_slider.get()

        out = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

        B = out[:, :, 0][0][0]
        G = out[:, :, 1][0][0]
        R = out[:, :, 2][0][0]
        print("%s %s %s" % (R, G, B))
        print(_from_rgb(r=R, g=G, b=B))
        UI.ui.color_block["bg"] = "%s" % _from_rgb(r=R, g=G, b=B)

    def erode(self):
        image = cv2.imread("Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.erode(image, kernel, iterations=1)  
        cv2.imwrite("Image-Converter/Preview.png", out)

        UI.ui.updatePic()

    def dilate(self):
        image = cv2.imread("Image-Converter/Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.dilate(image, kernel, iterations=1)  
        cv2.imwrite("Image-Converter/Preview.png", out)

        UI.ui.updatePic()

    def opening(self):
        image = cv2.imread("Image-Converter/Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
        cv2.imwrite("Image-Converter/Preview.png", out)

        UI.ui.updatePic()

    def closing(self):
        image = cv2.imread("Image-Converter/Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=1)
        cv2.imwrite("Image-Converter/Preview.png", out)

        UI.ui.updatePic()

ep = ep()