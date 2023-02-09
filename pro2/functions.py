import cv2,os
from scipy import signal


def draw_face_roi(face,img):
    try:
        x,y,w,h=[int(c)for c in face]
        delta =int( w*0.2)
        thickness =int( w*0.025)
        color=(255,0,0)     
        image=cv2.line(img,(x,y),(x+delta,y),color,thickness)
        image=cv2.line(image,(x,y),(x,y+delta),color,thickness)
        image=cv2.line(img,(x+w,y),(x+w-delta,y),color,thickness)
        image=cv2.line(image,(x+w,y),(x+w,y+delta),color,thickness)
        image=cv2.line(img,(x,y+h),(x+delta,y+h),color,thickness)
        image=cv2.line(image,(x,y+h),(x,y+h-delta),color,thickness)
        image=cv2.line(img,(x+w,y+h),(x+w-delta,y+h),color,thickness)
        image=cv2.line(image,(x+w,y+h),(x+w,y+h-delta),color,thickness)
    except:
        pass    
    

def crop_to_boundingbox(bb,frame):
    y,h,x,w=[int(c)for c in bb]
    return frame[y:y+h,x:x+w]
fs=30
bpf_div= 60 * fs / 2
b_BPF40220,a_BPF40220=signal.butter(10,([40/bpf_div,220/bpf_div]),'bandpass')

def bandpass_filter(sig):
    return signal.filtfilt(b_BPF40220,a_BPF40220,sig)


def put_bpm_onframe(bpm,frame):
    text=f'BPM : {bpm:.2f}'
    font=cv2.FONT_HERSHEY_SIMPLEX 
    org=(00,50)
    fontScale=1
    color=(0,0,255)
    thickness=2
    cv2.putText(frame,text,org,font,fontScale,color,thickness)