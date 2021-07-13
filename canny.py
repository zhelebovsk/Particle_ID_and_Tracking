import cv2
import numpy as np
img_original = cv2.imread('image.bmp')
cv2.namedWindow('Canny')


def nothing(x):
    pass


cv2.createTrackbar('Gauss','Canny',0,10,nothing)
cv2.createTrackbar('threshold1','Canny',50,400,nothing)
cv2.createTrackbar('threshold2','Canny',100,400,nothing)
while(1):
    gauss = cv2.getTrackbarPos('Gauss', 'Canny')
    threshold1=cv2.getTrackbarPos('threshold1','Canny')
    threshold2=cv2.getTrackbarPos('threshold2','Canny')

    img_edges = img_original
    if gauss > 0:
        img_edges = cv2.blur(img_edges,(gauss,gauss))
    img_edges=cv2.Canny(img_edges,threshold1,threshold2)

    cv2.imshow('original',np.vstack((img_original,img_original,img_original)))
    cv2.imshow('Canny',img_edges)  
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()
