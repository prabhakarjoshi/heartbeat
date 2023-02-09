from scipy import signal


# Calculate heart rate from FFT peaks
def find_heart_rate(fft, freqs, freq_min, freq_max):
    fft_maximums = []
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",freq_min)
    for i in range(fft.shape[0]):
        if freq_min <= freqs[i] <= freq_max:
            fftMap = abs(fft[i])
            fft_maximums.append(fftMap.max())
        else:
            fft_maximums.append(0)

    peaks, properties = signal.find_peaks(fft_maximums)
    max_peak = -1
    max_freq = 0

    # Find frequency with max amplitude in peaks
    for peak in peaks:
        if fft_maximums[peak] > max_freq:
            max_freq = fft_maximums[peak]
            max_peak = peak
    print("qwertyuiiuytrertyuiuytrrrrtyuuuuuuuiiiiiii")
    print(freqs[max_peak])
    return freqs[max_peak] * 60
