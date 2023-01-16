import math

import cv2


def get_rand(webcam):
    check, frame = webcam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (32, 32))
    numlist = []
    for i in frame.tolist():
        numlist.extend(i)
    bitlist = [str(x % 2) for x in numlist]
    num = "0b" + "".join(bitlist)
    return int(num, 2)

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
    webcam = cv2.VideoCapture(0)
    count = 0
    for i in range(5000):
        if math.sqrt(math.pow(demo_pi(webcam), 2) + math.pow(demo_pi(webcam), 2)) < 1:
            count += 1
    print(count*4/5000)
    webcam.release()
