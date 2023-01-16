import cv2
import datetime



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



if __name__ == '__main__':
    webcam = cv2.VideoCapture(0)
    get_rand(webcam)
    webcam.release()
