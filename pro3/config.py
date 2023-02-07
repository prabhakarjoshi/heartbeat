from matplotlib import pyplot as plt
import time

heartbeat_count = 128
fig = plt.figure()
ax = fig.add_subplot(111)
heartbeat_values = [0] * heartbeat_count
heartbeat_times = [time.time()] * heartbeat_count
