# import io
import cv2
import time
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks
# import time
import pro3.config as cf

face_classifier=cv2.CascadeClassifier("haarcascades\\haarcascade_frontalface_default.xml")
def algo3(frame):
# rgb
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=face_classifier.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        cv2.putText(frame,"GENERATING ECG", (x-2,y-2),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255),1)
        t=np.average(gray)
        cf.beat_vals = cf.beat_vals[1:] + [t]
        cf.beat_times = cf.beat_times[1:] + [time.time()]
        cf.ax.plot(cf.beat_times, cf.beat_vals)
        cf.fig.canvas.draw()
        plotted_img = np.fromstring(cf.fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    
        plotted_img = plotted_img.reshape(cf.fig.canvas.get_width_height()[::-1] + (3,))
        plt.cla()
        # frame=img
        cv2.imshow('Graph', plotted_img)
    # return frame



