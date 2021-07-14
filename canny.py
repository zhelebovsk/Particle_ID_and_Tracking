import cv2
import numpy as np


def nothing(x):
    pass


if __name__ == '__main__':
    # считывание изображения
    img_original = cv2.imread('image.bmp')[:, :, 0]
    h, w = img_original.shape[:2]
    #mask = np.zeros((h + 2, w + 2), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # создание окна и трекбаров
    window = 'adj'
    cv2.namedWindow(window)
    cv2.createTrackbar('Gauss', window, 2, 10, nothing)
    cv2.createTrackbar('threshold1', window, 50, 400, nothing)
    cv2.createTrackbar('threshold2', window, 100, 400, nothing)

    while True:
        # снятие значений с баров
        gauss = cv2.getTrackbarPos('Gauss', window)
        threshold1 = cv2.getTrackbarPos('threshold1', window)
        threshold2 = cv2.getTrackbarPos('threshold2', window)
        # размытие изображение для удаления шумов
        if gauss > 0:
            img_blur = cv2.blur(img_original, (gauss, gauss))
        else:
            img_blur = img_original
        # преобразование Кэнни
        img_edges = cv2.Canny(img_blur, threshold1, threshold2)
        # заполение пустот
        img_fill = np.copy(img_edges)
        mask = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(img_fill, mask, (0, 0), 255)
        img_fill = cv2.bitwise_not(img_fill)
        img_fill = cv2.bitwise_or(img_fill, img_edges)
        img_fill = cv2.morphologyEx(img_fill, cv2.MORPH_OPEN, kernel)

        img_result = np.vstack((img_blur, img_edges, img_fill))
        cv2.imshow(window, img_result)
        #cv2.imshow(window, cv2.resize(img_result,(w, h)))

        if cv2.waitKey(0) == ord('q'):
            cv2.destroyAllWindows()
            break

