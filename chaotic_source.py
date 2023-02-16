import logging
import math
import cv2
import numpy as np


PCT_MAX = 4294967295

class Random:
    def __init__(self):
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        self.cam.release()

    def pause(self):
        self.cam.release()

    def cont(self):
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def get_random_bits(self, rang):
        size = math.ceil(math.sqrt(rang.bit_length()))
        check, frame = self.cam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (size, size))
        numlist = []
        for i in frame.tolist():
            numlist.extend(i)
        return "".join([str(x % 2) for x in numlist[:rang.bit_length()]])

    def get_rand_large(self):
        return int("0b" + self.get_random_bits(1024), 2)

    def get_rand_range(self, start: int, stop: int):
        rang = (stop-start)
        bits = self.get_random_bits(36)
        num = int("0b" + bits, 2)
        pct = num/(1 << len(bits))
        return start + rang*pct

    def get_int_range(self, start: int, stop: int):
        rang = (stop-start)
        num = int("0b" + self.get_random_bits(rang), 2)
        while num > rang:
            logging.info("Requested number between %d and %d, got %d instead" % (start, stop, num))
            num = int("0b" + self.get_random_bits(rang), 2)
        return start + num

    def rand_pic(self, name):
        channels = []
        arr1 = []
        arr2 = []
        for i in range(16):
            for j in range(16):
                for k in range(3):
                    channels.append(self.get_int_range(0, 255))
                for k in range(16):
                    arr1.extend(channels)
                channels = []
            for j in range(16):
                arr2.extend(arr1)
            arr1 = []
        frame = np.array(arr2).reshape((256, 256, 3))
        cv2.imwrite(name, frame)


if __name__ == '__main__':
    pass
