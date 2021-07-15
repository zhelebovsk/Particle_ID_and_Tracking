import cv2
import numpy as np
import canny



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
    del mask, kernel, img_original, h, w

    result = canny.numerate_parts(img_fill)

    qw = np.where(result == 15)
