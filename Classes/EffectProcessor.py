import tkinter as tk
from PIL import Image,ImageDraw,ImageFont
import cv2
import numpy as np

class ep():
    def __init__(self):
        self.bg_color = cv2.imread("Image-Converter/Default Preview.png")
        self.R = 0
        self.G = 0
        self.B = 0
        self.original = cv2.imread("Image-Converter/Preview.png")
        self.rotate_90 = cv2.rotate(self.original, cv2.ROTATE_90_CLOCKWISE)
        self.rotate_180 = cv2.rotate(self.original, cv2.ROTATE_180)
        self.rotate_270 = cv2.rotate(self.rotate_180, cv2.ROTATE_90_CLOCKWISE)

    def changeHSV(self, event):
        def _from_rgb(r, g, b):
            return "#%02x%02x%02x" % (r, g, b)   

        self.bg_color = cv2.cvtColor(self.bg_color, cv2.COLOR_BGR2HSV)

        self.bg_color[:, :, 0] = h
        self.bg_color[:, :, 1] = s
        self.bg_color[:, :, 2] = v

        out = cv2.cvtColor(self.bg_color, cv2.COLOR_HSV2BGR)

        self.B = out[:, :, 0][0][0]
        self.G = out[:, :, 1][0][0]
        self.R = out[:, :, 2][0][0]

        UI.ui.color_block["bg"] = "%s" % _from_rgb(r=self.R, g=self.G, b=self.B)

    def updateHSV(self):
        image = cv2.imread("Image-Converter/Preview.png")
        
        image[:, :, 0] += self.B
        image[:, :, 1] += self.G
        image[:, :, 2] += self.R

        cv2.imwrite("Image-Converter/Preview.png", image)


    def erode(self):
        image = cv2.imread("Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.erode(image, kernel, iterations=1)  
        cv2.imwrite("Image-Converter/Preview.png", out)


    def dilate(self):
        image = cv2.imread("Image-Converter/Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.dilate(image, kernel, iterations=1)  
        cv2.imwrite("Image-Converter/Preview.png", out)


    def opening(self):
        image = cv2.imread("Image-Converter/Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
        cv2.imwrite("Image-Converter/Preview.png", out)


    def closing(self):
        image = cv2.imread("Image-Converter/Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=1)
        cv2.imwrite("Image-Converter/Preview.png", out)

    def rotate(self, degrees):
        if(degrees == 0):
            cv2.imwrite("Image-Converter/Preview.png", self.original)
        elif(degrees == 90):
            cv2.imwrite("Image-Converter/Preview.png", self.rotate_90)
        elif(degrees == 180):
            cv2.imwrite("Image-Converter/Preview.png", self.rotate_180)
        elif(degrees == 270):
            cv2.imwrite("Image-Converter/Preview.png", self.rotate_270)

    #def resize(self):
    #    height = int(UI.ui.height.get("1.0", tk.END))
    #    width = int(UI.ui.width.get("1.0", tk.END))
    #    original = cv2.imread("Image-Converter/Preview.png")
    #    resized = cv2.resize(original, (height, width))
    #    cv2.imwrite("Image-Converter/Preview.png", resized)
    #    UI.ui.getImageSize()