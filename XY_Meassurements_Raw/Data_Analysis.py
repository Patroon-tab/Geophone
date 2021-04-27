# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 16:19:07 2021

@author: Patrick
"""
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import signal

from matplotlib import ticker, cm
from scipy.fftpack import fftshift
from matplotlib.tri import Triangulation, TriAnalyzer, UniformTriRefiner
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from matplotlib.colors import LogNorm
import math

mypath = r"C:\Users\spadmin\Desktop\Data\XY_Meassurements_Raw"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
coordinatesx = []
coordinatesy = []
vals = []
color = ""
xses= []
yses= []
mags= []
nums = []
frstart = 2330
frend = 2350
divid = 1


#onlyfiles = ['Flur_15_-30_1.txt', 'Flur_15_-30_2.txt', 'Flur_15_-30_3.txt', 'Flur_15_470_1.txt', 'Flur_15_470_2.txt', 'Flur_15_470_3.txt', 'PR_40_30_1.txt', 'PR_40_30_2.txt', 'R1_190_25_1.txt', 'R1_190_25_2.txt', 'R1_190_25_3.txt', 'R1_240_380_1.txt', 'R1_240_380_2.txt', 'R1_240_380_3.txt',  'R2_180_150_1.txt', 'R2_180_150_2.txt', 'R2_180_150_3.txt', 'R2_180_400_1.txt', 'R2_180_400_2.txt', 'R2_180_400_3.txt', 'R2_480_370_1.txt', 'R2_480_370_2.txt', 'R2_480_370_3.txt', 'R3_10_25_1.txt', 'R3_10_25_2.txt', 'R3_10_25_3.txt', 'R3_115_330_1.txt', 'R3_115_330_2.txt', 'R3_115_330_3.txt', 'R3_510_130_1.txt', 'R3_510_130_2.txt', 'R3_510_130_3.txt', 'R4_80_200_1.txt', 'R4_80_200_2.txt', 'R4_80_200_3.txt', 'TR_-180_390_1.txt', 'TR_-180_390_2.txt', 'TR_-180_390_3.txt', 'TR_15_230_1.txt', 'TR_15_230_2.txt', 'TR_15_230_3.txt', 'TR_360_390_1.txt', 'TR_360_390_2.txt', 'TR_360_390_3.txt']
# 'R1_530_200_1.txt', 'R1_530_200_2.txt', 'R1_530_200_3.txt', 'R1_530_200_4.txt',
for q in onlyfiles:
    
    n = q.split("_")
    number = n[-1].split(".")
    if number[-1] == "txt":
      number = number[0]
      n = n[0:3]
      x = float(n[1])
      y = float(n[2])
    
      room = ""
      
      if n[0] == "R2":
          x = x
          y = y
          color = "blue"
          room = "R2"

      if n[0] == "R3":
        x = x+5.5
        y = (-1*y) - 30
        color = "green"
        room = "R3"

      if n[0] == "R1":
        x = x + 5
        y = y + 529
        color = "red"
        room = "R1"
        
      if n[0] == "Flur":
        x = (-1*x)-29
        y = y + 110
        color = "orange"
        room = "Flur"
        
      if n[0] == "TR":
        x = -x - 30
        y = y + 708
        color = "yellow"
        room = "TR"
        
      if n[0] == "PR":
        x = x + 214
        y = y + 961
        color = "black"
        room = "PR"

      if n[0] == "R4":

        x = x + 382
        y = (-1*y)  + 241
        color = "purple"
        room = "R4"

      n[1] = x 
      n[2] = y
      n.append(number)
      xses.append(x)
      yses.append(y)
      nums.append(number)
      vals.append(n)

      #plt.scatter(x,y, color=color)
      
      newname = room + "_" + str(x) + "_" +  str(y) + "_" + number + ".txt"


      
      f = open(q, "r")
      read = f.read().split(",")[:-1]
      data = np.asarray(read).astype(np.float64)
      samplepoints = data[0]
      duration = data[1]
      nn = np.mean(data[2:].reshape(-1, 1), axis=1)
      sr = ((samplepoints*1000000)/duration)/1
      sr = int(sr)
      f, Pxx_den = signal.welch(nn, sr, nperseg = (sr/divid) + -1)
      mag = np.trapz(Pxx_den[int(frstart/divid):int(frend/divid)], f[int(frstart/divid):int(frend/divid)])
      mag = math.log(mag)
      mags.append(mag)
      


# define grid.
xi = np.linspace(-700,538,1000)
yi = np.linspace(-375,1163,1000)
# grid the data.
zi = griddata((xses, yses), mags, (xi[None,:], yi[:,None]), method='nearest')
# contour the gridded data, plotting dots at the randomly spaced data points.
levels = 100
CS = plt.contourf(xi,yi,zi,ccmap ="hot", levels = levels)

plt.colorbar() # draw colorbar
# plot data points.
plt.scatter(xses, yses, color = "black")
plt.axis('square')
plt.title("Frequency Range: %d Hz - %d Hz"%(frstart, frend))
plt.xlabel("X-Coordinates[cm]")
plt.ylabel("Y-Coordinates[cm]")
plt.xlim(right = 538)
plt.show()
    