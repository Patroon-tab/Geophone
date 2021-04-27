import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fftshift
import subprocess
import time
from scipy.signal import find_peaks
import os  

datasetname = "PR_40_30_2.txt"
plotname = "PR_40_30_2.png"
#Parameters
avgfactor = 1 #Over how many datapoints should it be averaged
desfreq = 2500 #Center of the peakdetection
wanwid = 300 # Distance from midpoint for peakdetection
lowpl = 0 #Lower limit of Welch plot
highpl = 3000 #Upper limit of Welch plot
peakthreshold = 0.00003 #Required threshold of peaks, the vertical distance to its neighboring samples.


#Calling C-Programm and wait for it to finish

subprocess.call(["./program"])
time.sleep(2)


#Reading and preparing data from C-Programm("Dataset.txt")
f = open("DATASET.txt", "r")
read = f.read().split(",")[:-1]
data = np.asarray(read).astype(np.float64)
samplepoints = data[0]
duration = data[1]
print("It took: %f seconds to meassure" %(duration/1000000))
nn = np.mean(data[2:].reshape(-1, avgfactor), axis=1)
sr = ((samplepoints*1000000)/duration)/avgfactor
os.rename('DATASET.txt',datasetname) 
#Get the average voltage accros the whole measurement useful to calibrate middle point
print("Average Voltage[V]: %f"%np.average(nn))

#Print out the sampling frequency
print("Samplingfrequency[Hz]: %f" %sr)

#Save Plot of raw data as "RawData.png"
plt.plot(nn)
plt.savefig("RawData.png")
plt.close()

#Save spectrum analysis with the Welch transformation as "Welch.png"
f, Pxx_den = signal.welch(nn, sr, nperseg = 1000, noverlap = 500)

#Peakdetection
wid = int((len(f)/f[-1])*wanwid)
fac = f[-1]/len(f)
pos = int((len(f)/f[-1])*desfreq)
peaks, _ = find_peaks(Pxx_den[(pos-wid):(pos+wid)], threshold=peakthreshold)
peaks = (peaks + pos) - wid

for x in peaks:
    textpeak = ("There is a peak at %f Hz in the desired range of %dHz - %dHz with an amplitude of %f V**2/Hz" % ((x*fac), (desfreq - wanwid), desfreq + wanwid, Pxx_den[x]))
    print(textpeak)
#Peakdetection End

plt.semilogy(peaks*fac, Pxx_den[peaks], "x")
plt.semilogy(f, Pxx_den)
plt.xlim(lowpl,highpl)
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.grid()
plt.savefig(plotname)
plt.close()









