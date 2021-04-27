from MCP import MCP3008
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time
from scipy import signal
from scipy.fftpack import fftshift
from scipy import interpolate



adc = MCP3008()


#Number of Samplepoints
samplepoints = 1000000

#Initialise Arrays to store meassured values
nn = np.empty(samplepoints)
xx = np.empty(samplepoints)
rs = np.array([])

    
start = time.time()
value = 1
for x in range(samplepoints):

   
    value = adc.read(2)
    

    end = time.time()

    nn[x] = value
    xx[x] = end-start


end = time.time()
duration = end-start
print(duration)

fs = samplepoints/duration


f, Pxx_den = signal.welch(nn, fs)
plt.semilogy(f, Pxx_den)
#plt.ylim([0.5e-3, 1])
plt.xlim(0,3000)
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.savefig("TEST")










   
    

