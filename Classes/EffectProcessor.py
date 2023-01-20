import tkinter as tk
from PIL import Image,ImageDraw,ImageFont
import cv2
import numpy as np

class ep():
    def __init__(self):
        self.bg_color = cv2.imread("Default Preview.png")
        self.R = 0
        self.G = 0
        self.B = 0

    def changeHSV(self, h,s,v):
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

        return "%s" % _from_rgb(r=self.R, g=self.G, b=self.B)

    def updateHSV(self, state):
        image = cv2.imread("Preview.png")
        
        if(state):
            image[:, :, 0] += self.B
            image[:, :, 1] += self.G
            image[:, :, 2] += self.R
        else:
            image[:, :, 0] -= self.B
            image[:, :, 1] -= self.G
            image[:, :, 2] -= self.R

        cv2.imwrite("Preview.png", image)


    def erode(self):
        image = cv2.imread("Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.erode(image, kernel, iterations=1)  
        cv2.imwrite("Preview.png", out)


    def dilate(self):
        image = cv2.imread("Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.dilate(image, kernel, iterations=1)  
        cv2.imwrite("Preview.png", out)


    def opening(self):
        image = cv2.imread("Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
        cv2.imwrite("Preview.png", out)


    def closing(self):
        image = cv2.imread("Preview.png")
        kernel = np.ones((5,5), np.uint8)  
        out = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=1)
        cv2.imwrite("Preview.png", out)

    def gradient(self):
        image = cv2.imread("Preview.png")
        kernel = np.ones((5,5), np.uint8)
        out = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations=1)
        cv2.imwrite("Preview.png", out)
