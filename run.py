import numpy as np
import cv2
from pro1.preprocessing import algo1
from pro2.main import algo2
import copy
from pro3.main import algo3
from matplotlib import pyplot as plt


# Webcam Parameters
webcam = cv2.VideoCapture(0)
realWidth = 517
realHeight = 363
webcam.set(3, realWidth)
webcam.set(4, realHeight)
video_frames=[]

while (True):
    ret, frame1 = webcam.read()
    if ret == False:
        break
    frame2 = copy.copy(frame1)
    frame3 = copy.copy(frame1)
    
    # algo3(frame3)
    # algo2(frame2)
    if algo1(webcam,frame1,video_frames):
        cv2.imshow("Webcam Algo1", frame1)
    else:
        destroyWindow("Webcam Algo1")
    # cv2.imshow("Webcam Algo2", frame2)
    # cv2.imshow("Webcam Algo3", frame3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
