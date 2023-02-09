import cv2,time
import numpy as np
from scipy import signal
from pro2 import functions
import config as cnf

fs = 30
face_cascade=cv2.CascadeClassifier("haarcascades\\haarcascade_frontalface_default.xml")
tracker	=cv2.legacy.TrackerMOSSE_create()
cap=cv2.VideoCapture(0)
window=300
skin_vec=[0.3841,0.5121,0.7682]
B,G,R=0,1,2
found_face=False
initialized_tracker	=False
face_box=[]
mean_colors=[]
timestamps=[]
mean_colors_resampled=np.zeros((3,1))

def algo2(frame):
	global found_face
	global face_box
	global tracker
	global initialized_tracker
	global faces
	global mean_colors
	global timestamps
	global mean_colors_resampled

	# ret, frame = cap.read() 
	frame_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	
	if found_face and initialized_tracker:
		print("--")
		found_face,face_box=tracker.update(frame)
		# if not found_face:
		
	if not found_face:
		initialized_tracker=False
		faces=face_cascade.detectMultiScale(frame_gray,1.3,5)
		found_face=len(faces)>0

	if found_face and not initialized_tracker:			
		face_box=faces[0]
		tracker=cv2.legacy.TrackerMOSSE_create()
		tracker.init(frame,tuple(face_box))			
		initialized_tracker=True

	if found_face:
		face=functions.crop_to_boundingbox(face_box,frame)
		if face.shape[0]>0 and face.shape[1]>0:
			
			mean_colors+=[face.mean(axis=0).mean(axis=0)]
			timestamps+=[time.time()]
			functions.draw_face_roi(face_box,frame)
			t=np.arange(timestamps[0],timestamps[-1],1/fs)
			mean_colors_resampled=np.zeros((3,t.shape[0]))
			
			for color in [B,G,R]:
				resampled=np.interp(t,timestamps,np.array(mean_colors)[:,color])
				mean_colors_resampled[color]=resampled

	if mean_colors_resampled.shape[1]>window:
		col_c=np.zeros((3,window))
		for col in [B,G,R]:
			col_stride=mean_colors_resampled[col,-window:]
			y_ACDC=signal.detrend(col_stride/np.mean(col_stride))
			col_c[col]=y_ACDC*skin_vec[col]

		X_chrom=col_c[R]-col_c[G]
		Y_chrom=col_c[R]+col_c[G]-2*col_c[B]
		Xf=functions.bandpass_filter(X_chrom)
		Yf=functions.bandpass_filter(Y_chrom)
		Nx=np.std(Xf)
		Ny=np.std(Yf)
		alpha_CHROM=Nx/Ny

		x_stride=Xf-alpha_CHROM*Yf
		amplitude=np.abs(np.fft.fft(x_stride,window)[:int(window/2+1)])
		normalized_amplitude=amplitude/amplitude.max()
		
		frequencies=np.linspace(0,fs/2,int(window/2)+1)*60
		bpm_index=np.argmax(normalized_amplitude)
		bpm=frequencies[bpm_index]
		#snr=functions.calculateSNR(normalized_amplitude,bpm_index)
		if(bpm>60 and bpm<=100):
			functions.put_bpm_onframe(bpm,frame)
			cnf.results.append(bpm)
