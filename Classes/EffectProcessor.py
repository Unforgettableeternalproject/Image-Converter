import tkinter as tk
from PIL import Image,ImageDraw,ImageFont
import cv2
import numpy as np

class ep():
    def __init__(self) -> None:
        pass
    
    def changeHSV(self, h, s, v):
        image = cv2.imread("Preview.png")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


        image[:, :, 0] = h
        image[:, :, 1] = s
        image[:, :, 2] = v

        out = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        cv2.imwrite("Preview.png", out)

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
        out = cv2.morphologyEx(image,cv2.MORPH_GRADIENT,kernel,iterations=1)
        cv2.imwrite("Preview.png", out)