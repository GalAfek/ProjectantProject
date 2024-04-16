import tkinter as tk
import time
import threading
import SoapySDR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, lfilter
from PIL import Image, ImageTk  # Import PIL for handling images

running = False
def fm_demod(x, df=1.0, fc=0.0):
    n = np.arange(len(x))
    rx = x * np.exp(-1j * 2 * np.pi * fc * n)
    phi = np.arctan2(np.imag(rx), np.real(rx))
    y = np.diff(np.unwrap(phi) / (2 * np.pi * df))
    return y

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs  # Nyquist Frequency
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def update_plot(ax, x_data, y_data, title, mode):
    ax.clear()
    ax.plot(x_data, y_data, color="yellow")
    if mode == 1:
        ax.set_ylim(-300, 0)
        ax.set_xlabel("Frequency[Hz]", color="white")
        ax.set_ylabel("dBm", color="white")
    else:
        ax.set_xlabel("Time [mSec]", color="white")
        ax.set_ylabel("Voltage", color="white")
    ax.set_title(title, color="white")

def update_plots(fm_sample, time_axis_ms, filtered_real, filtered_imag, modulating_signal, power_dBm_demod, freq_axis_demod):
    titles = ['FM Signal in time Domain', 'Demodulated Signal in time Domain', 'Demodulated Signal in frequency Domain']
    time_frame_1 = len(time_axis_ms)//500
    time_frame_2 = len(time_axis_ms)//100
    freq_frame_1 = (len(freq_axis_demod)//20)
    # Create threads for each plot
    thread1 = threading.Thread(target=update_plot, args=(ax1, time_axis_ms[time_frame_1*2:time_frame_1*4:], filtered_real[time_frame_1*2:time_frame_1*4:],titles[0],0))
    thread2 = threading.Thread(target=update_plot, args=(ax2, time_axis_ms[time_frame_2*2:time_frame_2*4:], modulating_signal[time_frame_2*2:time_frame_2*4:],titles[1],0))
    thread3 = threading.Thread(target=update_plot, args=(ax3, freq_axis_demod, (power_dBm_demod-147),titles[2],1))
    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()
    # Join the threads to ensure they complete before moving on
    thread1.join()
    thread2.join()
    thread3.join()
    # Draw the updated plots
    canvas.draw()

def long_running_process():
    while running:
            sdr_device.readStream(rx_stream, [samples], num_samples)
            real_part = np.real(samples)
            imaginary_part = np.imag(samples)
            absolute_sample = np.abs(samples)
            time_axis_ms = np.arange(num_samples) / sample_rate * 1e3
            filtered_real = lowpass_filter(real_part, 100000, 1000000)
            filtered_imag = lowpass_filter(imaginary_part, 100000, 1000000)
            filtered_abs = lowpass_filter(absolute_sample, 100000, 1000000)



            fft_result = np.fft.fft(samples)
            freq_axis = np.fft.fftfreq(num_samples, d=1/sample_rate) / 1e6
            modulating_signal = fm_demod(samples, df=1.0, fc=5e6)


            
            # fft_result_demod = np.fft.fft(modulating_signal)
            filtered_modulating_signal = lowpass_filter(modulating_signal, 10000, 1000000)
            fft_result_demod = np.fft.fft(filtered_modulating_signal)




            time_axis_ms = np.arange(len(modulating_signal)) / sample_rate * 1e3
            power_dBm_demod = 10 * np.log10(1000*((np.abs(fft_result_demod)**2)/50))

            freq_axis_demod = np.fft.fftfreq(len(modulating_signal), d=1/sample_rate)

            target_frequency = 150  # Hz
            index_150hz = np.argmin(np.abs(freq_axis_demod - target_frequency))

            peak_amplitude = np.abs(fft_result_demod[index_150hz])
            threshold_amplitude = 5000  # Adjust as needed
            
            if peak_amplitude > threshold_amplitude:
                message_label.config(text="ID detected : ✓", fg="green", bg="#333333")
                # message_label.config(text="150 detected : ✓")
            else:
                message_label.config(text="ID not detected : ✗", fg="red", bg="#333333")
                # message_label.config(text="150 not detected : ✗")
            # print("Processing...")
            # update_plots(filtered_abs[1::], time_axis_ms, filtered_real, filtered_imag, filtered_modulating_signal, power_dBm_demod, freq_axis_demod)
            update_plots(filtered_abs[1::], time_axis_ms, filtered_real, filtered_imag, filtered_modulating_signal, power_dBm_demod, freq_axis_demod)
            # update_plots(filtered_abs[1::], time_axis_ms, filtered_real, filtered_imag, filtered_modulating_signal, power_dBm_demod, freq_axis_demod)
            time.sleep(0.1)

def run_sw():
    global running
    running = not running
    start_button.config(text="Off" if running else "On")
    # Create and launch a thread for the long-running process
    if running == True:
        t = threading.Thread(target=long_running_process)
        t.start()


device_id = 'driver=uhd,serial=30FA400'
sdr_device = SoapySDR.Device(device_id)
sample_rate = 1e6
sdr_device.setSampleRate(SoapySDR.SOAPY_SDR_RX, 0, sample_rate)
center_frequency = 5e6
sdr_device.setFrequency(SoapySDR.SOAPY_SDR_RX, 0, center_frequency)
rx_stream = sdr_device.setupStream(SoapySDR.SOAPY_SDR_RX, SoapySDR.SOAPY_SDR_CF32, [0])
sdr_device.activateStream(rx_stream)
num_samples = int(sample_rate)
samples = np.empty(num_samples, dtype=np.complex64)


# Create the main window
root = tk.Tk()
root.attributes('-zoomed', True)  # Full-screen without title bar
root.title("Amplitude Checker")
root.configure(bg="#333333")  # Set dark gray background


# Create a figure for plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), facecolor="#333333")
fig.subplots_adjust(hspace=0.5)
# Set text color to white
# Set tick label color to white
ax1.tick_params(axis="both", colors="white")
ax1.set_xlabel("Time (mSec)", color="white")
ax1.set_ylabel("Voltage", color="white")
ax1.set_title("FM Signal in Time Domain", color="white")

ax2.tick_params(axis="both", colors="white")
ax2.set_xlabel("Time (mSec)", color="white")
ax2.set_ylabel("Voltage", color="white")
ax2.set_title("Demodulated Signal in Time Domain", color="white")

ax3.tick_params(axis="both", colors="white")
ax3.set_xlabel("Frequency[Hz]", color="white")
ax3.set_ylabel("dBm", color="white", )
ax3.set_ylim(-300, 0)
ax3.set_title("Demodulated Signal in Frequency Domain", color="white")

# Set background color of axes to black
ax1.set_facecolor('#333333')
ax2.set_facecolor('#333333')
ax3.set_facecolor('#333333')

# Create a canvas and add the figure to it
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Label for messages
message_label = tk.Label(root, text="", font=("Helvetica", 50), bg="#333333")
message_label.pack(pady=80)

# Start button
start_button = tk.Button(root, text="On", command=run_sw, width=20, height=2, font=("Helvetica", 30), bg="#444444", fg="white")
start_button.pack(pady=10)

IDF_Image = Image.open('/home/sdr/Desktop/Gal_Project/IDF.png')
LF_Image = Image.open('/home/sdr/Desktop/Gal_Project/LF.png')
Hatal_Image = Image.open('/home/sdr/Desktop/Gal_Project/Hatal.png')

# Convert images to PhotoImage objects
photo1 = ImageTk.PhotoImage(IDF_Image)
photo2 = ImageTk.PhotoImage(LF_Image)
photo3 = ImageTk.PhotoImage(Hatal_Image)

# Create labels to display the images
label1 = tk.Label(root, image=photo1, bg="#333333")
label2 = tk.Label(root, image=photo2, bg="#333333")
label3 = tk.Label(root, image=photo3, bg="#333333")

# Place the labels on the canvas (adjust the coordinates as needed)
label1.place(x=10, y=10)
label2.place(x=80, y=10)
label3.place(x=150, y=10)



root.mainloop()