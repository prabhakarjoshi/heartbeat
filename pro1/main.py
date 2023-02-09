import cv2
from pro1.pyramids import build_video_pyramid,collapse_laplacian_video_pyramid
import pro1.heartrate as hrt
# import pro1.preprocessing as pre
import pro1.eulerian as eul
import config as cnf


freq_min = 1
freq_max = 1.8
heart_rate=121
def calcul(video_frames, frame_ct, fps):

    print("Building Laplacian video pyramid...")
    lap_video = build_video_pyramid(video_frames)

    amplified_video_pyramid = []

    for i, video in enumerate(lap_video):
        if i == 0 or i == len(lap_video)-1:
            # print("poiuy")
            continue

        result, fft, frequencies = eul.fft_filter(video, freq_min, freq_max, fps)
        lap_video[i] += result

        # Calculate heart rate
        print("Calculating heart rate...")
        global heart_rate
        heart_rate = hrt.find_heart_rate(fft, frequencies, freq_min, freq_max)

    # amplified_frames = collapse_laplacian_video_pyramid(lap_video, frame_ct)
    # global heart_rate
    print("Heart rate: ", heart_rate, "bpm")
    cnf.results.append(heart_rate)
    print("Displaying final video...")

    # for frame in amplified_frames:
    #     cv2.imshow("frame", frame)
    #     cv2.waitKey(10)
    # cv2.destroyWindow("frame")



