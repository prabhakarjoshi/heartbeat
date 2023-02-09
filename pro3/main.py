import io
import cv2
import time
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import time
import pro3.config as cf

face_classifier=cv2.CascadeClassifier("pro3\\haarcascade_frontalface_default.xml")
def algo3(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=face_classifier.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.putText(frame,"GENERATING ECG", (x-2,y-2),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255),1)
        t=np.average(gray)
        cf.heartbeat_values = cf.heartbeat_values[1:] + [t]
        cf.heartbeat_times = cf.heartbeat_times[1:] + [time.time()]
        cf.ax.plot(cf.heartbeat_times, cf.heartbeat_values)
        cf.fig.canvas.draw()
        plot_img_np = np.fromstring(cf.fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    
        plot_img_np = plot_img_np.reshape(cf.fig.canvas.get_width_height()[::-1] + (3,))
        plt.cla()
        # frame=img
        cv2.imshow('Graph', plot_img_np)
    # return frame



