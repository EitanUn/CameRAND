import math
import cv2


PCT_MAX = 4294967295

def get_rand_large(webcam):
    check, frame = webcam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (32, 32))
    numlist = []
    for i in frame.tolist():
        numlist.extend(i)
    bitlist = [str(x % 2) for x in numlist]
    num = "0b" + "".join(bitlist)
    return int(num, 2)


def get_rand_range(webcam, min: int, max: int):
    check, frame = webcam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (8, 4))
    numlist = []
    for i in frame.tolist():
        numlist.extend(i)
    bitlist = [str(x % 2) for x in numlist]
    num = "0b" + "".join(bitlist)
    pct = int(num, 2) / PCT_MAX
    return min + (max-min)*pct


def get_int_range(webcam, min: int, max: int):
    size = math.ceil(math.sqrt(max.bit_length()))
    check, frame = webcam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (size, size))
    numlist = []
    for i in frame.tolist():
        numlist.extend(i)
    bitlist = [str(x % 2) for x in numlist]
    num = "0b" + "".join(bitlist)
    pct = int(num, 2) / pow(2, pow(size, 2))
    return math.ceil(min + (max-min)*pct - 1)


if __name__ == '__main__':
    pass
