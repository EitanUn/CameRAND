import math
import logging
import matplotlib.pyplot as plt
import numpy as np
import cv2
from chaotic_source import Random


def demo_dist(start, end, amount):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    x = []
    for i in range(amount):
        x.append(rand(cam, start, end))
    cam.release()

    # make data

    # plot:
    fig, ax = plt.subplots()
    xmax = end-1
    ymax = amount*10/(end-start)
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


def demo_pic(name):
    rand = Random()
    array = []
    for i in range(768):
        array.append(rand.get_int_range(0, 255))
    frame = np.array(array).reshape((16, 16, 3))
    print(frame.dtype)
    print(cv2.imwrite(name, frame))
    rand.pause()


if __name__ == '__main__':
    demo_pic("testpic.jpg")
