import cv2
import numpy as np
import pro1.config as cf
import time
from pro1.main import calcul

faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt0.xml")

def algo1(webcam,frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    roi_frame = frame
    face_rects = ()
    # Detect face
    if len(cf.video_frames) == 0:
        face_rects = faceCascade.detectMultiScale(gray, 1.3, 5)
    # Select ROI
    if len(face_rects) > 0:
        for (x, y, w, h) in face_rects:
            roi_frame = frame[y:y + h, x:x + w]
        if roi_frame.size != frame.size:
            roi_frame = cv2.resize(roi_frame, (500, 500))
            frame = np.ndarray(shape=roi_frame.shape, dtype="float")
            frame[:] = roi_frame * (1. / 255)
            cf.video_frames.append(frame)
    end=time.time()
    if(end-cf.start>5):
        cf.start=end
        fps = int(webcam.get(cv2.CAP_PROP_FPS))
        frame_ct = len(cf.video_frames)
        calcul(cf.video_frames, frame_ct, fps)
        cf.video_frames=[]
    # cap.release()

    # return video_frames, frame_ct, fps

