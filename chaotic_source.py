"""
Author: Eitan Unger
Date: 28/02/23
description: TRNG class for RSA key communication and TRNG final project, including mostly the Random class
based on camera digital chip interference as a true chaotic source
"""

import logging
import math
import cv2
import numpy as np


class Random:
    """
    a class similar to python's Random except using camera interference as a true chaotic source
    """
    def __init__(self):
        """
        generate an RNG object
        """
        # open up the camera
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        """
        stop the camera when the object is deleted
        """
        self.cam.release()

    def pause(self):
        """
        stop the camera to allow for another Random object to use it/extra protection in case __del__ doesn't trigger
        """
        self.cam.release()

    def cont(self):
        """
        restart the camera after pause
        """
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def get_random_bits(self, rang: int):
        """
        A function that gets a random string of bits that are roughly the size of rang
        :param rang: bit length
        :return: a string of random bits with length rang
        """
        # get the rough size of a square picture so that the number of pixels is around equal to the
        # number of required bits
        logging.debug("Random: Requested %d bits from camera" % rang)
        size = math.ceil(math.sqrt(rang))
        assert self.cam.isOpened()
        check, frame = self.cam.read()
        assert check == 1
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # check if the camera returned an image
        if frame is None:
            logging.exception("Random: Camera fail")
            raise RuntimeError("Camera malfunction, please try again. In case this error persists,"
                               " try replacing camera.")
        # get correct number of bits
        frame = cv2.resize(frame, (size, size))
        numlist = []
        # get a list of every pixel's luminance value
        for i in frame.tolist():
            numlist.extend(i)
        logging.debug("Random: Successfully got requested bits")
        # get the lsb of each value (most random) as a string in the correct length
        return "".join([str(x % 2) for x in numlist[:rang]])

    def get_rand_large(self, size: int):
        """
        get a large random integer, used for RSA keygen
        :return: large (128 byte) integer
        """
        logging.debug("Random: Requested number with %d size" % size)
        return int("0b" + self.get_random_bits(size), 2)

    def get_rand_range(self, start: float, stop: float):
        """
        Get a random floating point decimal number in range start, stop
        :param start: start of the range
        :param stop: end of the range
        :return: random float in the range
        """
        logging.debug("Random: Requested float in range %f to %f" % (start, stop))
        rang = (stop-start)
        bits = self.get_random_bits(36)
        num = int("0b" + bits, 2)
        pct = num/(pow(2, 36) - 1)
        # get a random number from 0 to rang and add it to start, promising a decimal in the range. pct is a random
        # percentage between 0 and 100 that is multiplied by rang to get the random number in range
        logging.debug("Random: Got number %f" % (start + rang*pct))
        return start + rang*pct

    def get_int_range(self, start: int, stop: int):
        """
        Get a random int between start and end
        :param start: start
        :param stop: end
        :return: a random int between start and end
        """
        logging.debug("Random: Requested float in range %d to %d" % (start, stop))
        rang = stop-start
        num = int("0b" + self.get_random_bits(rang.bit_length()), 2)
        # since this is an int, the num is only the same bit size as rang, and I must make sure it is smaller than it
        # or request another number
        while num > rang:
            logging.info("Random: Requested number between %d and %d, got %d instead" % (start, stop, num + start))
            num = int("0b" + self.get_random_bits(rang.bit_length()), 2)
        logging.debug("Random: Got number %d" % (start + num))
        return start + num

    def rand_pic(self, name):
        """
        Generate a random 16x16 image, mostly cosmetic but can be utilized in stenography or cryptography in rare cases
        :param name: filename to save the picture as
        """
        logging.debug("Random: Requested random image")
        check, frame = self.cam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (64, 96))
        numlist = []
        bytes_list = []
        for i in frame.tolist():
            numlist.extend(i)
        bits = "".join([str(x % 2) for x in numlist])
        logging.debug("Random: Got all bits for random image")
        # get 6144 bits (8*16*16*3) bits and split them into bytes, one for each color channel of each pixel, then
        # put them into an array and reshape it to 16x16x3
        while bits:
            bytes_list.append(int("0b" + bits[:8], 2))
            bits = bits[8:]
        photo = np.array(bytes_list).reshape((16, 16, 3))
        mul = np.ones((16, 16, 1))
        # resize the image from 16x16 to 256x256 without smoothing pixels using a kronecker product
        frame = np.kron(photo, mul)
        cv2.imwrite(name, frame)
        logging.debug("Random: Successfully saved random image")

    def shuffle(self, shuff: list):
        for i in range(len(shuff) - 1, 1, -1):
            place = self.get_int_range(0, i)
            shuff[i], shuff[place] = shuff[place], shuff[i]


def test_camera():
    """
    Function used to test if the camera is available
    :return: camera available t/f
    """
    logging.info("Testing for camera")
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # open camera
    res = not (cam is None or not cam.isOpened())  # check if object is an open camera or not
    logstring = "" if res else " not"
    logging.info("Camera is%s working" % logstring)
    cam.release()  # release camera in case it is valid to not hold it
    return res


if __name__ == '__main__':
    pass
