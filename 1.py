import cv2
import numpy as np
from matplotlib import pyplot as plt


def flood(mat, mat2, x, y, val):
    mat[x, y] = 0
    mat2[x, y] = val
    if x > 0:
        if mat[x - 1, y] != 0:
            flood(mat, mat2, x-1, y, val)
    if x < np.shape(mat)[0] - 1:
        if mat[x + 1, y] != 0:
            flood(mat, mat2, x + 1, y, val)
    if y > 0:
        if mat[x, y - 1] != 0:
            flood(mat, mat2, x, y - 1, val)
    if y < np.shape(mat)[1] - 1:
        if mat[x, y + 1] != 0:
            flood(mat, mat2, x, y + 1, val)


if __name__ == '__main__':
    img_original = cv2.imread('res.bmp')[:, :, 0]
    h, w = img_original.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    img_fill = np.copy(img_original)
    cv2.floodFill(img_fill, mask, (0, 0), 255)
    img_fill = cv2.bitwise_not(img_fill)
    img_fill = cv2.bitwise_or(img_fill,img_original)
    img_fill = cv2.morphologyEx(img_fill, cv2.MORPH_OPEN, kernel)



    k = 0
    #im_proc = np.zeros((h+2, w+2))
    #im_proc[1:-1, 1:-1] = np.copy(img_fill)
    im_proc = np.copy(img_fill)
    mat = np.zeros_like(im_proc)
    for i in range(h):
        for j in range(w):
            if im_proc[i, j] != 0:
                k += 1
                flood(im_proc, mat, i, j, k)

    result = np.where(mat == 15)
