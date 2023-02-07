import io
import cv2
import time
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import time

# camera stream
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)
#for cropped frame
x, y, w, h = 450, 100, 100, 100
heartbeat_count = 128
heartbeat_values = [0] * heartbeat_count
all=[]
heartbeat_times = [time.time()] * heartbeat_count

# Matplotlib graph surface
fig = plt.figure()
ax = fig.add_subplot(111)

start = time.time()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == False:
        continue
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # img = img[50:1080-50, 50:1920-50]

    # Update the data
    t=np.average(img)
    heartbeat_values = heartbeat_values[1:] + [t]
    all.append(t)
    # a = np.array(all)
    
    heartbeat_times = heartbeat_times[1:] + [time.time()]
    # if 
    # print(len(heartbeat_values))
    # Draw matplotlib graph to numpy array
    ax.plot(heartbeat_times, heartbeat_values)
    fig.canvas.draw()
    plot_img_np = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')

    plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.cla()

    peaks2, _ = find_peaks(all, prominence=135.15)
    print(len(peaks2))
    end = time.time()
    print(len(peaks2)//end-start)
    # plt.subplot(2, 2, 2)
    # plt.plot(peaks2, heartbeat_values[peaks2], "ob")
    # plt.plot(heartbeat_values)
    # plt.legend(['prominence'])
    # plt.show()
    #Display frame

    # cv2.imshow('Crop', img)
    cv2.imshow('img', img)
    cv2.imshow('Graph', plot_img_np)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()





    # while(current!=NULL)
    # {
    #     slot_t* slot = (slot_t*) current->data;
    #     if(slot -> in_use == 0 && slot->size >= size)
    #     {
    #         slot -> in_use = 1;
    #         slot -> size_in_use = size;
    #         return block.buffer + new_offset;
    #     }
    #     new_offset += slot -> size;
    #     current = current -> next;
    # }