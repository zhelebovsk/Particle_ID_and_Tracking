import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os


class Snap:
    number_of_snaps = 0

    def __init__(self, path):
        self.name = os.path.basename(path)
        self.path = {'raw': path}
        self.number = Snap.number_of_snaps
        Snap.number_of_snaps += 1
        self.res = cv.imread(path)[:, :, 0].shape

if __name__ == '__main__':
    # Считывание всех имен нужного формата в папке данных
    os.chdir('data1')
    directories = 'raw'
    #print(os.getcwd())
    file_format = '.bmp'
    frames = []
    for file_name in os.listdir(directories):
        if file_name[-len(file_format):] == file_format:
            frames.append(Snap(os.getcwd() + '\\' + directories + '\\' + file_name))
    # Проверка наличия папок и создание
    directories = ('crop', 'subs', 'threshold', 'edge', 'detected')
    for directory in directories:
        if directory in os.listdir(os.getcwd()):
            for file in os.listdir(os.getcwd() + '\\' + directory):
                os.remove(os.getcwd() + '\\' + directory + '\\' + file)
                print(directory, ' ', file, ' ', 'has been removed')
            os.rmdir(directory)
        os.mkdir(directory)
        for frame in frames:
            frame.path[directory] = os.getcwd() + '\\' + directory + '\\' + frame.name
    # Обрезка и запись изображений
    for frame in frames:
        cr = cv.imread(frame.path['raw'])[:, 0:1000, 0]
        cv.imwrite(frame.path['crop'], cr)
    # Поиск минимумов
    background = cv.imread(frames[0].path['crop'])[:, :, 0]
    for frame in frames:
        background = np.minimum(cv.imread(frame.path['crop'])[:, :, 0], background)
        #comparison = cv.imread(frame.path['crop'])[:, :, 0] > background
    cv.imwrite(os.getcwd() + '\\' + 'background.bmp', background)
    # Вычитание фона
    for frame in frames:
        subs = cv.imread(frame.path['crop'])[:, :, 0] - background
        cv.imwrite(frame.path['subs'], subs)


    for frame in frames:
        edge = cv.imread(frame.path['subs'])[:, :, 0]
        edge = cv.Canny(edge, 40, 150)
        cv.imwrite(frame.path['edge'], edge)

    cv.imshow('a', edge)
    cv.waitKey(0)
    cv.destroyWindow('a')
