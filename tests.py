import math
import logging
from chaotic_source import get_int_range as rand, get_rand_range as rand_r, \
    get_rand_large as rand_l, get_random_bits as rand_b
import matplotlib.pyplot as plt
import numpy as np
import cv2
from random import random
from RSA import is_prime


def demo_dist(min, max, amount):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    x = []
    for i in range(amount):
        x.append(rand(cam, min, max))
    cam.release()

    # make data

    # plot:
    fig, ax = plt.subplots()
    xmax = max-1
    ymax = amount*10/(max-min)
    ax.hist(x, bins=xmax, linewidth=0.02, edgecolor="white")
    ax.set(xlim=(0, xmax), xticks=np.arange(1, xmax),
           ylim=(0, ymax), yticks=np.arange(1, ymax))

    plt.show()


def demo_pi(amount):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0
    for i in range(amount):
        x = (rand_r(cam, 0, 1))
        y = (rand_r(cam, 0, 1))
        d = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        logging.debug("point %d is (%f, %f) and has a distance of %f" % (i, x, y, d))
        if 1 >= d:
            count += 1
    cam.release()
    pi = 4*count/amount
    print("pi is %f\nmargin of error is %.4f" % (pi, math.fabs(math.pi-pi)/math.pi))

"""
from chaotic_source import get_int_range as rand
import cv2
import numpy
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
array = []
for i in range(192):
    array.append(rand(cam, 0, 255))
print(numpy.array(array))
frame = numpy.ndarray(shape=(8, 8, 3), buffer=)
print(cv2.imwrite("demo_im.png", frame))
cam.release()

"""
if __name__ == '__main__':
    logging.basicConfig(filename="testlogs.log", level=logging.DEBUG)
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    rang = (1 - 0)
    num = int("0b" + rand_b(cam, rang), 2)
    pct = num / (1 << num.bit_length())
    print(num, "\n", 1 << num.bit_length(), "\n", pct)
    cam.release()

