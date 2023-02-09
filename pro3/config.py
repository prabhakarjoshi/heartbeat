from matplotlib import pyplot as plt
import time

heartbeat_count = 200
fig = plt.figure()
ax = fig.add_subplot(111)
beat_vals = [0] * heartbeat_count
beat_times = [time.time()] * heartbeat_count
