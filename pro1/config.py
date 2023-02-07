import cv2
import numpy as np

firstFrame=None
firstGauss=None
videoGauss=None
fourierTransformAvg=None
frequencies=None
mask=None

i=0
realWidth = 320
realHeight = 240
videoWidth = 160
videoHeight = 120
videoChannels = 3
videoFrameRate = 15
 # Color Magnification Parameters
levels = 3
alpha = 170
minFrequency = 1.0
maxFrequency = 2.0
bufferSize = 150
bufferIndex = 0
# Output Display Parameters
font = cv2.FONT_HERSHEY_SIMPLEX
loadingTextLocation = (20, 30)
bpmTextLocation = (videoWidth//2 + 5, 30)
fontScale = 1
fontColor = (255,255,255)
lineType = 2
boxColor = (0, 255, 0)
boxWeight = 3
# Heart Rate Calculation Variables
bpmCalculationFrequency = 15
bpmBufferIndex = 0
bpmBufferSize = 10
bpmBuffer = np.zeros((bpmBufferSize))


def init():
    def buildGauss(frame, levels):
        pyramid = [frame]
        for level in range(levels):
            frame = cv2.pyrDown(frame)
            pyramid.append(frame)
        return pyramid
    global firstFrame
    global firstGauss
    global videoGauss
    global fourierTransformAvg
    global frequencies
    global mask

    # Bandpass Filter for Specified Frequencies
    frequencies = (1.0*videoFrameRate) * np.arange(bufferSize) / (1.0*bufferSize)
    mask = (frequencies >= minFrequency) & (frequencies <= maxFrequency)


    # Initialize Gaussian Pyramid
    firstFrame = np.zeros((videoHeight, videoWidth, videoChannels))
    firstGauss = buildGauss(firstFrame, levels+1)[levels]
    videoGauss = np.zeros((bufferSize, firstGauss.shape[0], firstGauss.shape[1], videoChannels))
    fourierTransformAvg = np.zeros((bufferSize))

    