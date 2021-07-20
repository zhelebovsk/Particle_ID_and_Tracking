import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import canny
from datetime import datetime
import sys


class Snap:
    number_of_snaps = 0

    def __init__(self, path):
        self.name = os.path.basename(path)
        self.path = {'raw': path}
        self.number = Snap.number_of_snaps
        Snap.number_of_snaps += 1
        self.particles = []


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
                print(datetime.now().time(), directory, ' ', file, ' ', 'has been removed')
            os.rmdir(directory)
        os.mkdir(directory)
        for frame in frames:
            frame.path[directory] = os.getcwd() + '\\' + directory + '\\' + frame.name
    del directory, directories, frame, file_format, file_name

    # Обрезка и запись изображений
    # Поиск минимумов
    cr = cv.imread(frames[0].path['raw'])[:, 0:1000, 0]
    cv.imwrite(frames[0].path['crop'], cr)
    background = cr
    for frame in frames:
        cr = cv.imread(frame.path['raw'])[:, 0:1000, 0]
        cv.imwrite(frame.path['crop'], cr)
        background = np.minimum(cr, background)
    cv.imwrite(os.getcwd() + '\\' + 'background.bmp', background)
    print(datetime.now().time(), 'Background has been found')
    # Вычитание фона
    for frame in frames:
        subs = cv.imread(frame.path['crop'])[:, :, 0] - background
        cv.imwrite(frame.path['subs'], subs)
        edge = subs
        # Размытие по гауссу 3х3
        edge = cv.blur(edge, (3, 3))
        # Cany 100 200 границы
        edge = cv.Canny(edge, 100, 200)
        cv.imwrite(frame.path['edge'], edge)
        fill = edge
        # Открытие структурным элементом - крест
        fill = canny.fill_parts_n_remove_threads(fill,  ellipse_size=3)
        cv.imwrite(frame.path['fill'], fill)
        proc = fill
        proc = canny.numerate_parts(proc)
        cv.imwrite(frame.path['proc'], proc)
        frame.particles = sorted(canny.count(proc))

    #a = []
    #b = []
    #for frame in frames:
    #    for part in frame.particles:
    #        a.append(int(part.c[0]))
    #        b.append(int(part.c[1]))

    cv.imshow('a', fill)
    cv.waitKey(0)
    cv.destroyWindow('a')
