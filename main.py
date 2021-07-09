import cv2
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
        self.res = cv2.imread(path)[:, :, 0].shape

if __name__ == '__main__':
    # Считывание всех имен нужного формата в папке данных
    os.chdir('data1')
    directories = 'raw'
    print(os.getcwd())
    file_format = '.bmp'
    frames = []
    for file_name in os.listdir(directories):
        if file_name[-len(file_format):] == file_format:
            frames.append(Snap(os.getcwd() + '\\' + directories + '\\' + file_name))
    # Проверка наличия папок и создание
    directories = ('crop', 'subs', 'threshold', 'edge', 'detected')
    for i in directories:
        if i in os.listdir(os.getcwd()):
            os.rmdir(i)
        os.mkdir(i)
        for f in frames:
            f.path[i] = os.getcwd() + '\\' + i + '\\' + f.name
    im = cv2.imread(frames[0].path['raw'])[:, :, 0]
    cr = im[0:320, 0:1000]



