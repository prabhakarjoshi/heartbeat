import cv2
from pro1.pyramids import build_video_pyramid,collapse_laplacian_video_pyramid
import pro1.heartrate as hrt
# import pro1.preprocessing as pre
import pro1.eulerian as eul


# Frequency range for Fast-Fourier Transform
freq_min = 1
freq_max = 1.8
heart_rate=121
def calcul(video_frames, frame_ct, fps):
    # Preprocessing phase
    print("Reading + preprocessing video...")
    # heart_rate=121
    # video_frames, frame_ct, fps = preprocessing.read_video("videos/rohin_active.mov")

    # Build Laplacian video pyramid
    print("Building Laplacian video pyramid...")
    lap_video = build_video_pyramid(video_frames)

    amplified_video_pyramid = []

    for i, video in enumerate(lap_video):
        if i == 0 or i == len(lap_video)-1:
            print("poiuy")
            continue

        # Eulerian magnification with temporal FFT filtering
        print("Running FFT and Eulerian magnification...")
        result, fft, frequencies = eul.fft_filter(video, freq_min, freq_max, fps)
        lap_video[i] += result

        # Calculate heart rate
        print("Calculating heart rate...")
        global heart_rate
        heart_rate = hrt.find_heart_rate(fft, frequencies, freq_min, freq_max)

    # Collapse laplacian pyramid to generate final video
    print("Rebuilding final video...")
    amplified_frames = collapse_laplacian_video_pyramid(lap_video, frame_ct)
    #done to check for other errors
    # heart_rate=0
    # Output heart rate and final video
    # global heart_rate
    print("Heart rate: ", heart_rate, "bpm")
    print("Displaying final video...")

    for frame in amplified_frames:
        cv2.imshow("frame", frame)
        cv2.waitKey(10)
    cv2.destroyWindow("frame")



