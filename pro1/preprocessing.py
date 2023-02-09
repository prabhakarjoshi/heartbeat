import cv2
import numpy as np
import pro1.config as cf
import time
from pro1.main import calcul
import threading

faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt0.xml")
# def algomluti
def algo1(webcam,frame,video_frames):
    if(cf.start !=0):
        return False
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    roi_frame = frame
    face_rects = ()
    face_rects = faceCascade.detectMultiScale(gray, 1.3, 5)
    # Select ROI
    if len(face_rects) > 0:
        for (x, y, w, h) in face_rects:
            roi_frame = frame[y:y + h, x:x + w]
            roi_frame = cv2.resize(roi_frame, (500, 500))
            frame = np.ndarray(shape=roi_frame.shape, dtype="float")
            frame[:] = roi_frame * (1. / 255)
            video_frames.append(frame)
    end=time.time()
    if(end-cf.start>15 and len(video_frames)>100):
        cf.start=end
        fps = int(webcam.get(cv2.CAP_PROP_FPS))
        frame_ct = len(video_frames)

        t1 = threading.Thread(target=calcul, args=(video_frames, frame_ct, fps,))
        t1.start()
        # print("plot")
        # cf.start=end
        # print("qqqq",frame_ct)
        # calcul(video_frames, frame_ct, fps)
        video_frames=[]
    return True

