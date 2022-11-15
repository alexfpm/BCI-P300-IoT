# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 18:35:58 2022

@author: AlexPM
"""

import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.signal import butter, filtfilt, lfilter, freqz
from scipy import signal
import math
from matplotlib.widgets import Button

import datetime
from datetime import datetime


#--------------------------------------------------------------
#SERIAL PORT DECLARATION
#--------------------------------------------------------------

ser = serial.Serial('COM4', 230400)

ser.close()

#--------------------------------------------------------------
#OPENING SERIAL PORT AND COMMUNICATION
#--------------------------------------------------------------
ser.open()


Aviso = input("Enter an 'x' to begin sampling: ")

ser.write(bytes(Aviso,'utf-8'))



#SKIP THE INITIAL INFO
# intro = ser.read(size = 2006)  #For INPUT SHORT

intro = ser.read(size = 2269)  #For NORMAL ELECTRODE


time.sleep(0.05)


#MAKE SOME MEASUREMENTS
# data2 = ser.readline()
# data3 = ser.readline()

#DATA DECODING
# dataConverted = intro.decode('UTF-8')
# dataConverted2 = data2.decode('UTF-8')
# dataConverted3 = data3.decode('UTF-8')

#--------------------------------------------------------------
#DATA PREPROCESSING
#--------------------------------------------------------------

# measureNice = dataConverted2.split(", ")
# measureNice.pop(0)
# measureNice.pop(8)

# measureNice = np.array(measureNice)
# measureNice = measureNice.astype(float)

#--------------------------------------------------------------
#ADITIONAL VARIABLES
#--------------------------------------------------------------

backupMeasures = []


Canal1 = []
Canal2 = []
Canal3 = []

#--------------------------------------------------------------
#ANIMATION!
#--------------------------------------------------------------

# Parameters
x_len = 2000         # Number of points to display

#y_range = [-3e-5, -1e-5]  # Range of possible Y values to display (INPUT SHORT TEST)

y_range = [-100e-3, 10e-3]  # Range of possible Y values to display (NORMAL ELECTRODE)



# Create figure for plotting
fig = plt.figure()

#CH1
ax = fig.add_subplot(1, 1, 1)
ax.set_ylim(y_range)

# #CH2
# ax = fig.add_subplot(3, 1, 2)
# ax.set_ylim(y_range)

# #CH3
# ax = fig.add_subplot(3, 1, 3)
# ax.set_ylim(y_range)


xs = list(range(0, x_len))

ys = [0] * x_len
#ys2 = [0] * x_len
#ys3 = [0] * x_len


#CHANNELS
# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys, '#1D45D8')
#line2, = ax.plot(xs, ys, '#0c912b')
#line3, = ax.plot(xs, ys, '#91190c')


# Add labels
plt.title('EEG Data: Time series (LIVE - with Electrodes)')
plt.xlabel('Samples')
plt.ylabel('Volts [V]')



#-----------------------------------------------------------------
#FILTERING
#-----------------------------------------------------------------


# Filter requirements
T = 1.0/9         # Sample Period

fs = 250.0       # sample rate, Hz (SPS)
cutoff = 20      # desired cutoff frequency of the filter, Hz

nyq = 0.5 * fs   # Nyquist Frequency

#order = 7       # Order of filter
#order = 10
order = 20

n = int(T * fs)  # total number of samples



#LPF - METHOD 1
#-----------------------------------------------------------------

#Filter implementation using scipy

def butter_lowpass_filter(data, cutoff, fs, order):
    
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    #y = filtfilt(b, a, data, padlen=26)
    
    return y
#-----------------------------------------------------------------



#LPF - METHOD 2
#-----------------------------------------------------------------

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter2(data, cutoff, fs, order):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

#-----------------------------------------------------------------



#NOTCH (NOT USED WITH DC SOURCE)
#-----------------------------------------------------------------

# Create/view notch filter
samp_freq = 250  # Sample frequency (Hz or SPS)
notch_freq = 60.0  # Frequency to be removed from signal (Hz)
quality_factor = 30.0  # Quality factor

# Design a notch filter using signal.iirnotch
b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)




#----------------------------------------------------------------
# BUTTONS FOR:
#    
#       1) CLOSING SERIAL PORT AND STOP SAMPLING
#       2) SCALE y-limits (y_range)
#       3) ADJUST VIEW OF SIGNAL
#----------------------------------------------------------------

class Index:
    ind = 0

    def stop(self, event):
        self.ind += 1
        
        comFinish = 'z'
        ser.write(bytes(comFinish,'utf-8'))
        ser.close()
    
    
    def scale(self, event):
        self.ind += 1
        
        #PARA CANAL 1
        meanY = sum(Canal1)/len(Canal1)
        
        y_rangeNew = [meanY-1e-3, meanY+1e-3]
        ax.set_ylim(y_rangeNew)
        
        
    def autoset(self, event):
        self.ind += 1
        
        meanY = sum(Canal1)/len(Canal1)
        
        y_rangeNew = [meanY-3e-3, meanY+3e-3]
        ax.set_ylim(y_rangeNew)
        
#-----------------------------------------------------------------


timeOld = datetime.now()
timeOld = timeOld.strftime("%H:%M:%S.%f")

minutesOld = float(timeOld[3:5])
secOld = float(timeOld[6:15])


#-----------------------------------------------------------------
#Function to adjust the window Automatically
def calculate_sec(minO, secO, minN, secN, data):
    
    #Same minutes
    if minO == minN:
        
        #Adjust window every 5 seconds
        if secN > secO + 5:
            
            meanY = sum(data)/len(data)
            
    
            #y_rangeNew = [meanY-1e-3, meanY+1e-3]
            y_rangeNew = [meanY-3e-3, meanY+3e-3]
            
            ax.set_ylim(y_rangeNew)
            
            minO = minN
            secO = secN
            
            
            return minO, secO
        
    
    #Different minutes
    if minN > minO:
        
        #Adjust window every 5 seconds
        if secN + (60 - secO) > 5:
            
            meanY = sum(data)/len(data)
    
    
            #y_rangeNew = [meanY-1e-3, meanY+1e-3]
            y_rangeNew = [meanY-3e-3, meanY+3e-3]
            
            ax.set_ylim(y_rangeNew)
            
            minO = minN
            secO = secN
            
            
            return minO, secO

#-----------------------------------------------------------------   



# This function is called periodically from FuncAnimation
def animate(i, ys):

    #Reading data from ADS1299:
        
    for x in range(0, math.ceil(fs/20)-1):
        
        data = ser.readline()
        dataConverted = data.decode('UTF-8')
    
        measureNice = dataConverted.split(", ")
        measureNice.pop(0)
        measureNice.pop(8)
    
        measureNice = np.array(measureNice)
        measureNice = measureNice.astype(float)
    
            
        #CONVERSION TO VOLTAGE (POSSIBLE FORMULA :D)
        measureNice = measureNice*0.37/((2**24)-1)
        
        #-------------------------------------------------------------------
        # #Some try to attenuate the effect of drastic changes on the samples
        
        # measureNiceMean = sum(measureNice)/len(measureNice)
        
        # for w in range(0, len(measureNice)-1):
            
        #     if measureNice[w] > 1.1*measureNiceMean or measureNice[w] < 0.9*measureNiceMean:
        #         measureNice[w] = measureNiceMean
            
        #-------------------------------------------------------------------
        
        
        Canal1.append(measureNice[0])  
        #Canal2.append(measureNice[1])
        #Canal3.append(measureNice[2])
    
    
    
    
    # #------------------------------------------------------------
    # #LPF FILTER - METHOD 1
    # outSignal = butter_lowpass_filter(Canal1, cutoff, fs, order)
    # #------------------------------------------------------------
    
    
    #------------------------------------------------------------
    #LPF FILTER - METHOD 2
    
    outSignal = butter_lowpass_filter2(Canal1, cutoff, fs, order)
    #outSignal2 = butter_lowpass_filter2(Canal2, cutoff, fs, order)
    #outSignal3 = butter_lowpass_filter2(Canal3, cutoff, fs, order)
    #------------------------------------------------------------
     
    

        
    # Add measurements to lists (channels)
    #ys.append(measureNice[0])
    #backupMeasures.append(measureNice[0])
    
    #ys.append(outSignal)
    #backupMeasures.extend(outSignal)
    
    
    ys.extend(outSignal)
    #ys2.extend(outSignal2)
    #ys3.extend(outSignal3)
    
    

    # Limit y list to set number of items
    ys = ys[-x_len:]
    #ys2 = ys2[-x_len:]
    #ys3 = ys3[-x_len:]
    

    # Update line with new Y values
    line.set_ydata(ys)
    #line2.set_ydata(ys2)
    #line3.set_ydata(ys3)
    
    
    #-------------------------------------------
    #AUTO ADJUST Y-LIM OF THE WINDOW
    
    timeNew = datetime.now()
    timeNew = timeNew.strftime("%H:%M:%S.%f")
    
    minutesNew = float(timeNew[3:5])
    secNew = float(timeNew[6:15])
    
    
    calculate_sec(minutesOld, secOld, minutesNew, secNew, outSignal)
    #-------------------------------------------
    


    return line,


#-----------------------------------------------------------------
# newYRange = backupMeasures[len(backupMeasures)-27:len(backupMeasures)]
# meanY = float(sum(newYRange)/len(newYRange))

# y_range = [meanY-10e-3, meanY+10e-3]  # Range of possible Y values to display (NORMAL ELECTRODE)
#-----------------------------------------------------------------



#-----------------------------------------------------------------
# DEFINITION OF BUTTONS LOCATION AND SET CALLBACKS
#-----------------------------------------------------------------

#FOR 1 CHANNEL:
axstop = plt.axes([0.81, 0.12, 0.1, 0.075])
axscale = plt.axes([0.59, 0.12, 0.1, 0.075])
axauto = plt.axes([0.7, 0.12, 0.1, 0.075])


# #FOR 3 CHANNELS:
# axstop = plt.axes([0.92, 0.8, 0.07, 0.05])
# axauto = plt.axes([0.92, 0.73, 0.07, 0.05])
# axscale = plt.axes([0.92, 0.66, 0.07, 0.05])


callback = Index()

bstop = Button(axstop, 'Stop')
bstop.on_clicked(callback.stop)

bauto = Button(axauto, 'Auto')
bauto.on_clicked(callback.autoset)

bscale = Button(axscale, 'Scale')
bscale.on_clicked(callback.scale)




#-----------------------------------------------------------------
# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=10,
    blit=True)



plt.show()





