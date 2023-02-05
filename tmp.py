import cv2
import config as cf
import numpy as np
def algo1(frame):
  
    # Helper Methods
    def buildGauss(frame, levels):
        pyramid = [frame]
        for level in range(levels):
            frame = cv2.pyrDown(frame)
            pyramid.append(frame)
        return pyramid
    def reconstructFrame(pyramid, index, levels):
        filteredFrame = pyramid[index]
        for level in range(levels):
            filteredFrame = cv2.pyrUp(filteredFrame)
        filteredFrame = filteredFrame[:cf.videoHeight, :cf.videoWidth]
        return filteredFrame

    cf.init()
    detectionFrame = frame[cf.videoHeight//2:cf.realHeight-cf.videoHeight//2, cf.videoWidth//2:cf.realWidth-cf.videoWidth//2, :]

    # Construct Gaussian Pyramid
    cf.videoGauss[cf.bufferIndex] = buildGauss(detectionFrame, cf.levels+1)[cf.levels]
    fourierTransform = np.fft.fft(cf.videoGauss, axis=0)

    # Bandpass Filter
    fourierTransform[cf.mask == False] = 0

    # Grab a Pulse
    if cf.bufferIndex % cf.bpmCalculationFrequency == 0:
        cf.i = cf.i + 1
        for buf in range(cf.bufferSize):
            cf.fourierTransformAvg[buf] = np.real(fourierTransform[buf]).mean()
        hz = cf.frequencies[np.argmax(cf.fourierTransformAvg)]
        bpm = 60.0 * hz
        cf.bpmBuffer[cf.bpmBufferIndex] = bpm
        cf.bpmBufferIndex = (cf.bpmBufferIndex + 1) % cf.bpmBufferSize

    # Amplify
    filtered = np.real(np.fft.ifft(fourierTransform, axis=0))
    filtered = filtered * cf.alpha

    # Reconstruct Resulting Frame
    filteredFrame = reconstructFrame(filtered, cf.bufferIndex, cf.levels)
    outputFrame = detectionFrame + filteredFrame
    outputFrame = cv2.convertScaleAbs(outputFrame)

    cf.bufferIndex = (cf.bufferIndex + 1) % cf.bufferSize

    frame[cf.videoHeight//2:cf.realHeight-cf.videoHeight//2, cf.videoWidth//2:cf.realWidth-cf.videoWidth//2, :] = outputFrame
    cv2.rectangle(frame, (cf.videoWidth//2 , cf.videoHeight//2), (cf.realWidth-cf.videoWidth//2, cf.realHeight-cf.videoHeight//2), cf.boxColor, cf.boxWeight)
    if cf.i > cf.bpmBufferSize:
        cv2.putText(frame, "BPM: %d" % cf.bpmBuffer.mean(), cf.bpmTextLocation, cf.font, cf.fontScale,cf.fontColor, cf.lineType)
    else:
        cv2.putText(frame, "Calculating BPM...", cf.loadingTextLocation, cf.font, cf.fontScale, cf.fontColor, cf.lineType)



