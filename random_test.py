import math
import logging
from chaotic_source import get_int_range as rand, get_rand_range as rand_f
import matplotlib.pyplot as plt
import numpy as np
import cv2


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
        x = (rand_f(cam, 0, 1))
        y = (rand_f(cam, 0, 1))
        d = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        logging.debug("point %d is (%f, %f) and has a distance of %f" % (i, x, y, d))
        if 1 >= d:
            count += 1
    cam.release()
    pi = 4*count/amount
    print("pi is %f\nmargin of error is %.4f" % (pi, math.fabs(math.pi-pi)/math.pi))


if __name__ == '__main__':
    logging.basicConfig(filename="testlogs.log", level=logging.DEBUG)
    demo_pi(1000)
