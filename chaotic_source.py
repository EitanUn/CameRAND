import math
import cv2


PCT_MAX = 4294967295


def get_random_bits(webcam, rang):
    size = min(math.ceil(math.sqrt(rang.bit_length())), 6)
    check, frame = webcam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (size, size))
    numlist = []
    for i in frame.tolist():
        numlist.extend(i)
    return "".join([str(x % 2) for x in numlist])


def get_rand_large(webcam):
    return int("0b" + get_random_bits(webcam, 1024), 2)


def get_rand_range(webcam, start: int, stop: int):
    rang = (stop-start)
    num = int("0b" + get_random_bits(webcam, rang), 2)
    pct = num/(1 << num.bit_length())
    return start + rang*pct


def get_int_range(webcam, start: int, stop: int):
    rang = (stop-start)
    num = int("0b" + get_random_bits(webcam, rang), 2)
    while num > rang:
        num = int("0b" + get_random_bits(webcam, rang), 2)
    return start + num


if __name__ == '__main__':
    pass
