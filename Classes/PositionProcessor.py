import cv2
import numpy as np

class pp():
    def __init__(self):
        self.filps = [None, None, None, None]

    def flip(self, mode):
        cv2.imwrite("Image-Converter/Preview.png", self.filps[mode])

    def rotate(self, angle):
        image = cv2.imread("Preview.png")
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        cv2.imwrite("Image-Converter/Preview.png", result)

    def zoom(self, percent):
        image = cv2.imread("Image-Converter/Preview.png")
        width = int(image.shape[1] * percent)
        height = int(image.shape[0] * percent)
        dim = (width, height)
        return dim

    def resize(self, dim):
        image = cv2.imread("Image-Converter/Preview.png")
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite("Image-Converter/Preview.png", resized)



