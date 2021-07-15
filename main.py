import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import canny


class Snap:
    number_of_snaps = 0

    def __init__(self, path):
        self.name = os.path.basename(path)
        self.path = {'raw': path}
        self.number = Snap.number_of_snaps
        Snap.number_of_snaps += 1
        self.res = cv.imread(path)[:, :, 0].shape


class Particle:
    def __init__(self):
        self.A = 0
        self.c = [0, 0]
        self.pos = [0, 0]
        self.rect = [0, 0]


if __name__ == '__main__':
    # Считывание всех имен нужного формата в папке данных
    # Вход в папку с данными
    os.chdir('data1')
    directories = 'raw'
    file_format = '.bmp'
    # Считывание всех файлов нужного формата и запись пути в список
    frames = []
    for file_name in os.listdir(directories):
        if file_name[-len(file_format):] == file_format:
            frames.append(Snap(os.getcwd() + '\\' + directories + '\\' + file_name))
    # Перезапись всех папок
    directories = ('crop', 'subs', 'threshold', 'edge', 'fill', 'detected', 'proc')
    for directory in directories:
        if directory in os.listdir(os.getcwd()):
            for file in os.listdir(os.getcwd() + '\\' + directory):
                os.remove(os.getcwd() + '\\' + directory + '\\' + file)
                print(directory, ' ', file, ' ', 'has been removed')
            os.rmdir(directory)
        os.mkdir(directory)
        for frame in frames:
            frame.path[directory] = os.getcwd() + '\\' + directory + '\\' + frame.name
    del directory, directories
    # Обрезка и запись изображений
    for frame in frames:
        cr = cv.imread(frame.path['raw'])[:, 0:1000, 0]
        cv.imwrite(frame.path['crop'], cr)
    # Поиск минимумов
    background = cv.imread(frames[0].path['crop'])[:, :, 0]
    for frame in frames:
        background = np.minimum(cv.imread(frame.path['crop'])[:, :, 0], background)
    cv.imwrite(os.getcwd() + '\\' + 'background.bmp', background)
    # Вычитание фона
    for frame in frames:
        subs = cv.imread(frame.path['crop'])[:, :, 0] - background
        cv.imwrite(frame.path['subs'], subs)
    for frame in frames:
        edge = cv.imread(frame.path['subs'])[:, :, 0]
        edge = cv.blur(edge, (3, 3))
        edge = cv.Canny(edge, 100, 200)
        cv.imwrite(frame.path['edge'], edge)
    for frame in frames:
        fill = cv.imread(frame.path['edge'])[:, :, 0]
        fill = canny.fill_parts_n_remove_threads(fill)
        cv.imwrite(frame.path['fill'], fill)
    for frame in frames:
        proc = cv.imread(frame.path['fill'])[:, :, 0]
        proc = canny.numerate_parts(proc)
        cv.imwrite(frame.path['proc'], proc)
    cv.imshow('a', fill)
    cv.waitKey(0)
    cv.destroyWindow('a')
