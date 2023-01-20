import tkinter as tk
from PIL import Image,ImageDraw,ImageFont
import cv2
import numpy as np

class pp():
    def __init__(self):
        self.original = cv2.imread("Preview.png")
        self.h_filp = None
        self.v_filp = None
        self.b_flip = None

    def flip(self, mode):
        if(mode == 0):
            cv2.imwrite("Preview.png", self.original)
        elif(mode == 1):
            cv2.imwrite("Preview.png", self.h_flip)
        elif(mode == 2):
            cv2.imwrite("Preview.png", self.v_flip)
        elif(mode == 3):
            cv2.imwrite("Preview.png", self.b_flip)

    def rotate(self, angle):
        image = cv2.imread("Preview.png")
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        cv2.imwrite("Preview.png", result)

    def zoom(self, percent):
        image = cv2.imread("Preview.png")
        width = int(image.shape[1] * percent)
        height = int(image.shape[0] * percent)
        dim = (width, height)
        #resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        return dim

    def resize(self, dim):
        image = cv2.imread("Preview.png")
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite("Preview.png", resized)



