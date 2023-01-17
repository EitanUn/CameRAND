import math

import cv2


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
    return min + (max-min)*pct


def demo_pi(webcam):
    check, frame = webcam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (5, 5))
    numlist = []
    for i in frame.tolist():
        numlist.extend(i)
    bitlist = [str(x % 2) for x in numlist]
    num = "0b" + "".join(bitlist)
    return int(num, 2) / 33554431


if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    count = 0
    for i in range(100000):
        if math.sqrt(math.pow(demo_pi(cam), 2) + math.pow(demo_pi(cam), 2)) < 1:
            count += 1
    print(count*4/100000)
    cam.release()
