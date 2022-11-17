

import time
import numpy as np
from scipy.signal import butter, filtfilt, lfilter
from scipy import signal
from numpy.fft import fft, ifft
import os
import datetime




def erps_calculation(arduinoData, opSesameData, datesArduino, option):


    medicionesRAW = arduinoData

    
    #Se declaran los canales
    Canal1 = []
    
    Canal2 = []
    
    Canal3 = []
    
    Canal4 = []
    
    Canal5 = []
    
    Canal6 = []
    
    Canal7 = []
    
    Canal8 = []
    
    
    
    #-----------------------------------------------------------------
    
    medicionesRAWCopy = medicionesRAW
    
    
    intro = medicionesRAWCopy[0:2294]
    
    # #DATA FROM ANANCONDA PROMPT
    # data = medicionesRAWCopy[0 : len(medicionesRAWCopy) - 22]
    
    
    
    #DATA FROM PUTTY
    data = medicionesRAWCopy[medicionesRAWCopy.find('test')+5 : len(medicionesRAWCopy) - 21]
    
    #-----------------------------------------------------------------
    
    
    
    #Empezar a dividir los datos en sus respectivos canales
    
    medicionesArray = data.split(", ")
    medicionesArray = np.array(medicionesArray)
    
    
    for x in range(0, len(medicionesArray)-1, 9):
        
        Canal1.append(float(medicionesArray[x+1]))
        Canal2.append(float(medicionesArray[x+2]))
        Canal3.append(float(medicionesArray[x+3]))
        Canal4.append(float(medicionesArray[x+4]))
        Canal5.append(float(medicionesArray[x+5]))
        Canal6.append(float(medicionesArray[x+6]))
        Canal7.append(float(medicionesArray[x+7]))
        Canal8.append(float(medicionesArray[x+8]))
    #-----------------------------------------------------------------
    
    Canal1 = np.array(Canal1)
    Canal1 = Canal1.astype(float)
    
    Canal2 = np.array(Canal2)
    Canal2 = Canal2.astype(float)
    
    Canal3 = np.array(Canal3)
    Canal3 = Canal3.astype(float)
    
    Canal4 = np.array(Canal4)
    Canal4 = Canal4.astype(float)
    
    Canal5 = np.array(Canal5)
    Canal5 = Canal5.astype(float)
    
    Canal6 = np.array(Canal6)
    Canal6 = Canal6.astype(float)
    
    Canal7 = np.array(Canal7)
    Canal7 = Canal7.astype(float)
    
    Canal8 = np.array(Canal8)
    Canal8 = Canal8.astype(float)
    
    
    #-----------------------------------------------------------------
    #CONVERT VALUES TO VOLTAGES
    #-----------------------------------------------------------------
    
    
    for x in range(0, len(Canal1)):
        
        Canal1[x] = Canal1[x]*0.37/((2**24)-1)
        Canal2[x] = Canal2[x]*0.37/((2**24)-1)
        Canal3[x] = Canal3[x]*0.37/((2**24)-1)
        
    
    #-----------------------------------------------------------------
    #FILTERING
    #-----------------------------------------------------------------
    
    
    #LPF AND HPF
    #-----------------------------------------------------------------
    
    # Filter requirements
    T = 20.0         # Sample Period
    fs = 250.0       # sample rate, Hz (SPS)
    cutoff = 30      # desired cutoff frequency of the filter, Hz , slightly higher than desired
    
    nyq = 0.5 * fs   # Nyquist Frequency
    
    order = 20       # Order of filter
    n = int(T * fs)  # total number of samples
    
    
    #LPF Filter implementation using scipy
    
    def butter_lowpass_filter(data, cutoff, fs, order):
        normal_cutoff = cutoff / nyq
        # Get the filter coefficients 
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y = filtfilt(b, a, data)
        return y
    
    
    
    #HPF Filter implementation using scipy
    
    def butter_highpass(cutoff, fs, order=6):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = signal.butter(order, normal_cutoff, btype = "high", analog = False)
        return b, a
    
    def butter_highpass_filter(data, cutoff, fs, order):
        b, a = butter_highpass(cutoff, fs, order=order)
        y = signal.filtfilt(b, a, data)
        return y
    
    
    
    
    # LPF: Filter the data
    y = butter_lowpass_filter(Canal1, cutoff, fs, order)
    
    y2_1 = butter_lowpass_filter(Canal2, cutoff, fs, order)
    
    y3 = butter_lowpass_filter(Canal3, cutoff, fs, order)



    # -----------------------------------------------------
    # HPF: Filter the data

    if option == 1:
        y2 = butter_highpass_filter(y, 0.5, fs, 6)

    if option == 2:
        y2 = butter_highpass_filter(y2_1, 0.5, fs, 6)

    if option == 3:
        y2 = butter_highpass_filter(y3, 0.5, fs, 6)
    # -----------------------------------------------------



    time.sleep(0.1)
    #-----------------------------------------------------------------
    
    
    
    #NOTCH (NOT NECESSARY FOR DC SOURCE)
    #-----------------------------------------------------------------
    
    # Create/view notch filter
    samp_freq = 250  # Sample frequency (Hz or SPS)
    
    notch_freq = 0.5  # Frequency to be removed from signal (Hz)
    
    quality_factor = 30.0  # Quality factor
    
    
    # Design a notch filter using signal.iirnotch
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
    
    # Apply notch filter to the noisy signal using signal.filtfilt
    outputSignal = signal.filtfilt(b_notch, a_notch, y)
    
    
    
    
    
    
    #-------------------------------------------------------------------------
    #-------------------------------------------------------------------------
    #
    # SUPER IMPORTANT!: STABILIZATION OF THE MEASURES
    #
    #-------------------------------------------------------------------------
    #-------------------------------------------------------------------------
    
    #For the first 1000 samples:
    #piece1 = y2[200 : 1000]
    
    #Normally:
    piece = y2[1000 : 2000]
    
    
    
    
    #Line paralel to piece of data: Aproximation by lines :3
    x = np.arange(piece.shape[0]) / samp_freq
    
    m = (piece[len(piece)-1] - piece[0]) / 4
    
    b = piece[0]
    
    referenceLine = m*x + b
    
    
    
    #Vector of distances of the data respect to reference
    distancesEEG = np.empty(shape=(len(x)))
    
    
    
    for w in range(len(x)):
        
        distancesEEG[w] = piece[w] - referenceLine[w]
    
    
    
    
    
    #---------------------------------------------------------
    #MAKING OF: SMALL LINES TO APROXIMATE THE ORIGINAL DATA
    
    sizeOfLine = 125
    
    #numRep = 80
    numRep = 120
    
    
    piece = y2[sizeOfLine : 2*sizeOfLine]
    x = np.arange(piece.shape[0]) / samp_freq
    
    
    distancesEEG = np.empty(shape=(len(x)))
    
    distancesEEG2 = np.empty(shape=(len(x)*(numRep-1)))
    
    
    
    
    for z in range(1, numRep):
        
        piece = y2[z*sizeOfLine : (z+1)*sizeOfLine]
        
        x = np.arange(piece.shape[0]) / samp_freq
        
        m = (piece[len(piece)-1] - piece[0]) / 0.5
    
        b = piece[0]
    
        referenceLine = m*x + b
        
        
        
        
        for w in range(len(x)):
        
            distancesEEG[w] = piece[w] - referenceLine[w]
        
        
        distancesEEG2[(z-1)*sizeOfLine : z*sizeOfLine] = distancesEEG
    #---------------------------------------------------------
    
    
    
    #Creation of stabilized data
    
    ch_Nice = np.empty(shape = (15000))
    
    ch_Nice[125 : len(ch_Nice)] = distancesEEG2
    
    ch_Nice[0 : 124] = np.mean(distancesEEG2)
    
    
    
    
    
    
    
    # #-----------------------------------------------------------------
    # #DATA FROM OPENSESAME
    # #-----------------------------------------------------------------
    
    # #-----------------------------------------------------------------
    
    # f = open('subject-0.csv', 'r')
    # logFileRAW = f.read()
    # f.close()
    # #-----------------------------------------------------------------
    
    
    logFileRAW = opSesameData
    
    
    
    
    
    logFileRAWCopy = logFileRAW
    
    
    preLogFile = logFileRAW.split("\n")
    
    
    logFile = preLogFile[0 : len(preLogFile) - 4]
    
    
    flags = []
    momentOfStimulus = []
    onsetsMy = []
    
    
    for count, value in enumerate(logFile):
        
        if len(logFile[count]) > 1 and len(logFile[count]) < 5:
            
            flags.append(logFile[count])
            
        if len(logFile[count]) > 5:
            
            momentOfStimulus.append(logFile[count])
    
    
    
         
    for x in range(0, len(momentOfStimulus)):
        
        aux = momentOfStimulus[x]
        aux = aux[7:16]
        aux = np.array(aux)
        aux = aux.astype(float)
        
        momentOfStimulus[x] = aux
        
    momentOfStimulus = np.array(momentOfStimulus)
    
    
    #Scale stimulus times to secs (they are originally milisecs)
    momentOfStimulus = momentOfStimulus/1000
    
    
    
    #-----------------------------------------------------------------
    # SYNCHRONIZATION
    #-----------------------------------------------------------------
    
    #Adjust synchronization between OpenSesame and the sampling from Arduino:
    # +: Goes to right
    # -: Goes to left
    
    
    #DATA FROM PUTTY
    
    endOpSesame = preLogFile[len(preLogFile) - 3]
    endOpSesame = endOpSesame[endOpSesame.find('=')+2 : len(endOpSesame)-1]
    
    
    # try:
    #     endArduino = datetime.datetime.fromtimestamp(os.stat('DataFromArduino.txt').st_mtime)
    # except:
    #     endArduino = datesArduino
    
    
    endArduino = datesArduino
    
    
    
    endArduino = endArduino.strftime("%m/%d/%Y, %H:%M:%S.%f")
    endArduino = endArduino[12 : len(endArduino)]
    
    
    
    minutOpSesame = int(endOpSesame[3:5])
    minutArduino = int(endArduino[3:5])
    
    secOpSesame  = float(endOpSesame[6:len(endOpSesame)])
    secArduino = float(endArduino[6:len(endArduino)])
    
    
    if minutArduino == minutOpSesame:
        
        syncT = secArduino - (secOpSesame + 20.0)
    
    else:
        
        secOpSesame = secOpSesame - 40.0
        
        syncT = secArduino - secOpSesame
    
    
    
    
    syncT = str(syncT)
    syncT = syncT[0:5]
    syncT = float(syncT)
    
    #Adjust moment of reference:
    momentOfStimulus = momentOfStimulus - syncT
    
    
    # momentOfStimulus = momentOfStimulus - 0.00
    
    #-----------------------------------------------------------------
    
    
    
    #-----------------------------------------------------------------
    #CHANNEL WITH EVENTS
    #-----------------------------------------------------------------
    
    #EPOCHS
    
    event_id = {
        'ven': 1,
        'col': 2,
        'uk': 3,
        'usa': 4,
        'fin': 5,
        'ita': 6,
        'jpn': 7,
        'brz': 8,
        'ind': 9,
    }
    
    
    labels2 = np.zeros(len(ch_Nice))
    
    ch_Nice = ch_Nice*1000
    
    
    #CH2
    samplerate = 250.
    timeLine = np.arange(ch_Nice.shape[0]) / samplerate
    
    
       
    
    
    #-----------------------------------------------------------------
    #TRIALS AND ERP
    #-----------------------------------------------------------------
    
    print(momentOfStimulus[:10])  # Print the first 10 onsets
    print('Number of onsets:', len(momentOfStimulus))
    
    print('Flag shown at each onset:', flags[:10])
    
          
            
         
            
    #Creation of index of appereances for each flag
    
    venInd = []
    colInd = []
    brzInd = []
    usaInd = []
    ukInd = []
    jpnInd = []
    indInd = []
    finInd = []
    itaInd = []
    
    
    
    for count, value in enumerate(flags):
        
        if flags[count] == 'ven':
            venInd.append(count)
        
        if flags[count] == 'col':
            colInd.append(count)
        
        if flags[count] == 'brz':
            brzInd.append(count)
        
        if flags[count] == 'usa':
            usaInd.append(count)
        
        if flags[count] == 'uk':
            ukInd.append(count)
        
        if flags[count] == 'jpn':
            jpnInd.append(count)
        
        if flags[count] == 'ind':
            indInd.append(count)
            
        if flags[count] == 'fin':
            finInd.append(count)
        
        if flags[count] == 'ita':
            itaInd.append(count)
    
    
    
    #Array with all the amount of appearances for each flag
    flagInd = [venInd, brzInd, usaInd, ukInd, jpnInd, indInd, finInd, itaInd, colInd]
    
    flagInd2 = []
    
    for x in range(len(flagInd)):
        
        flagInd2.append(len(flagInd[x]))
        
    
    #Smallest index in flags array
    minInd = min(flagInd2)
    
    
    #-----------------------------------------------------------------
    #SNIPPET TO EXTRACT FROM MEASUREMENTS
    #-----------------------------------------------------------------
    
    #We'll cut one-second-long pieces of EEG signal that start from the moment a card was shown. These pieces will be named 'trials'
    
    snippet = int(2*samp_freq)
    #-----------------------------------------------------------------
    
    
    
    #Creation of trials and ERPs:
    
    timesVen = np.zeros(len(venInd))
    timesBrz = np.zeros(len(brzInd))
    timesUsa = np.zeros(len(usaInd))
    timesUk = np.zeros(len(ukInd))
    timesJpn = np.zeros(len(jpnInd))
    timesInd = np.zeros(len(indInd))
    timesFin = np.zeros(len(finInd))
    timesIta = np.zeros(len(itaInd))
    timesCol = np.zeros(len(colInd))
    
    
    
    timesVec = [timesVen, timesBrz, timesUsa, timesUk, timesJpn, timesInd, timesFin, timesIta, timesCol]
    
    #-----------------------------------------------------------------
    
    #conversionTime = 1000*(5/20)
    
    
    conversionTime = 1000*(15/60)
    
    
    #-----------------------------------------------------------------
    
    
    
    trialsVen = []
    trialsBrz = []
    trialsUsa = []
    trialsUk = []
    trialsJpn = []
    trialsInd = []
    trialsFin = []
    trialsIta = []
    trialsCol = []
    
    
    
    trialsFlags = [trialsVen, trialsBrz, trialsUsa, trialsUk, trialsJpn, trialsInd, trialsFin, trialsIta, trialsCol]
    
    
    
    #METHOD: ALL TRIALS
    
    
    #-----------------------------------------------------------------
    for w in range(len(flagInd)):
        
        aux1 = timesVec[w]
        aux2 = flagInd[w]
        
        for x in range(flagInd2[w]):
            
            aux1[x] = momentOfStimulus[aux2[x]]*conversionTime
            aux1 = aux1.astype(int)
            
            
            #"y2" for CH2-Cz and "y3" for CH3-Pz
            trialsFlags[w].append(ch_Nice[aux1[x] : aux1[x]+snippet])
    #-----------------------------------------------------------------    
        
    
    
    
    
    
    
    for x in range(len(event_id)):
        
        #trialsFlags[x].pop(len(venInd)-1)
        #trialsFlags[x].pop(len(venInd)-2)
        trialsFlags[x] = np.array(trialsFlags[x])
    
    #-----------------------------------------------------------------
    
    
    
    #ERPs for each event
    
    erpVen = np.zeros(snippet)
    erpBrz = erpVen
    erpUsa = erpVen
    erpUk = erpVen
    erpJpn = erpVen
    erpInd = erpVen
    erpFin = erpVen
    erpIta = erpVen
    erpCol = erpVen
    
    erps = [erpVen, erpBrz, erpUsa, erpUk, erpJpn, erpInd, erpFin, erpIta, erpCol]
    erps = np.array(erps)
    
    
    
    for x in range(len(erps)):
        
        if len(trialsFlags[x]) == 0: #The flag didn't appear on the test
            
            erps[x] = 0.0
        
        else:
            
            erps[x] = sum(trialsFlags[x])/len(trialsFlags[x])
        
        
    
    
    
    #Adding offset to move all the ERPs to a similar reference
    for x in range(len(erps)):
        
        offset = 0.0 - (sum(erps[x])/len(erps[x]))
        
        erps[x] = erps[x] + offset
        
    
    
    
        
    time.sleep(0.1)
    
    #-----------------------------------------------------------------
    
    
    
    
    #-----------------------------------------------------------------
    
    #Scale to microvolts:
    
    erps = erps*1000
    
    #-----------------------------------------------------------------
    
    
    
    
    timeERP = np.arange(erpVen.shape[0]) / samplerate
    
    #-----------------------------------------------------------------

    # -------------------------------------------------------------
    # ADJUSTING THE ANALISYS FOR NEGATIVE-FORM RESULTS

    p3aux = erps

    # p3neg = np.empty(shape=(9, 250))
    p3neg = np.empty(shape=(9, 50))

    for x in range(len(flagInd)):
        erpsAux = p3aux[x]

        # EXTRACT FROM ERPS THE TIME RANGE BETWEEN 0.2s AND 0.4s
        # Possible adjust: whole time range until 1s
        # erpsAux = erpsAux[0 : int(len(erpsAux)/2)]

        erpsAux = erpsAux[50: 100]

        p3neg[x] = erpsAux

    # Original ERPs sorted in ascending order
    erps_sorted = np.sort(p3aux)

    # Evaluate ERP's values on first stimulus to determine if it's a "negative-shape"
    negative_shape = False

    # ------------
    p_peaks = 0
    n_peaks = 0
    # ------------

    for x in range(len(flagInd)):

        min_val = False
        max_val = False

        aux = erps_sorted[x]

        # Find if there are global minimum values
        if min(p3neg[x]) in aux[0:5]:
            min_val = True

            n_peaks = n_peaks + 1

        # Find if there are global maximum values
        if max(aux[len(aux) - 6: len(aux)]) in p3neg[x]:
            max_val = True

            p_peaks = p_peaks + 1

        # #----------------------------------------------
        # print("ERP number: %d" % x)
        # print("Min val result: %s" % min_val)
        # print("Max val result: %s" % max_val)
        # print("\n")
        # #----------------------------------------------

    # ----------------------------------------
    # EVALUATE RESULTS

    print("\n")
    print("Negative peaks result: %d" % n_peaks)
    print("Positive peaks result: %d" % p_peaks)
    print("\n")

    w = True

    # REAL CONDITION:

    if n_peaks > p_peaks:

        print("NEGATIVE-SHAPE TEST")
        print("\n")

        # FORCE FILTERING FOR THE ACTUAL TEST:
        # if w == False:

        # --------------------------------------------------------------
        # LOCAL RECALCULATION OF ERPS WITH ADITIONAL FILTERING


        # -----------------------------------------------------
        # FILTERING FFT FROM 0.5 TO 30 Hz

        # ---------------------------
        if option == 1:
            test_filt = fft(Canal1)

        elif option == 2:
            test_filt = fft(Canal2)

        elif option == 3:
            test_filt = fft(Canal3)
        # ---------------------------



        test_filt[0: 29] = 0

        test_filt[1801: len(test_filt) - 1800] = 0

        # TESTING
        test_filt[119] = 0
        test_filt[179] = 0
        test_filt[14881] = 0
        test_filt[14821] = 0

        test_filt[len(test_filt) - 30: len(test_filt)] = 0
        # -----------------------------------------------------

        y2 = ifft(test_filt)

        # -----------------------------------------------------------------
        # REMOVE ECG-LIKE PEAKS AND SIMILAR PEAKS (ARTIFACTS)

        ch2_Filtered = y2 * 1000

        for x in range(0, len(ch2_Filtered)):

            val = ch2_Filtered[x]

            # Find positive peaks inside EEG measures. Threshold: 0.3
            if val > 0.3:

                p_peak = val

                cont = x

                next_val = 0

                # Find the max-value of the peak (probabbly the center of the gauss-shape)
                while p_peak > next_val:

                    try:
                        next_val = ch2_Filtered[cont + 1]
                    except:
                        break

                    if next_val > p_peak:

                        p_peak = next_val

                        cont = cont + 1

                    else:
                        break

                # Removing the artifacts
                ch2_Filtered[cont - 5: cont + 5] = 0

        for x in range(0, len(ch2_Filtered)):

            val = ch2_Filtered[x]

            # Find negative peaks inside EEG measures. Threshold: -0.15
            if val < -0.15:

                n_peak = val

                cont = x

                next_val = 0

                # Find the max-value of the peak (probabbly the center of the gauss-shape)
                while n_peak < next_val:

                    try:
                        next_val = ch2_Filtered[cont + 1]
                    except:
                        break

                    if next_val < n_peak:

                        n_peak = next_val

                        cont = cont + 1

                    else:
                        break

                # Removing the artifacts
                ch2_Filtered[cont - 5: cont + 5] = 0

        y2 = ch2_Filtered / 1000

        # -----------------------------
        # TRIALS AND ERP
        # -----------------------------

        y2 = y2 * 1000

        # METHOD: ALL TRIALS

        trialsVen = []
        trialsBrz = []
        trialsUsa = []
        trialsUk = []
        trialsJpn = []
        trialsInd = []
        trialsFin = []
        trialsIta = []
        trialsCol = []

        trialsFlags = [trialsVen, trialsBrz, trialsUsa, trialsUk, trialsJpn, trialsInd, trialsFin, trialsIta, trialsCol]

        # ---------------------------------------------------------------
        for w in range(len(flagInd)):

            aux1 = timesVec[w]
            aux2 = flagInd[w]

            for x in range(flagInd2[w]):
                aux1[x] = momentOfStimulus[aux2[x]] * conversionTime
                aux1 = aux1.astype(int)

                # "y2" for CH2-Cz and "y3" for CH3-Pz
                trialsFlags[w].append(y2[aux1[x]: aux1[x] + snippet])
        # ---------------------------------------------------------------

        for x in range(len(event_id)):
            trialsFlags[x] = np.array(trialsFlags[x])

        # ERPs for each event

        erps = [erpVen, erpBrz, erpUsa, erpUk, erpJpn, erpInd, erpFin, erpIta, erpCol]
        erps = np.array(erps)

        for x in range(len(erps)):

            if len(trialsFlags[x]) == 0:  # The flag didn't appear on the test

                erps[x] = 0.0

            else:

                erps[x] = sum(trialsFlags[x]) / len(trialsFlags[x])

        # Adding offset to move all the ERPs to a similar reference
        for x in range(len(erps)):
            offset = 0.0 - (sum(erps[x]) / len(erps[x]))

            erps[x] = erps[x] + offset

        # Scale to microvolts:
        erps = erps * 1000

        # --------------------------------------------------------------

        negative_shape = True


    # ----------------------------------------

    else:

        print("POSITIVE-SHAPE TEST")
        print("\n")

    # Change option place if the test is detected as "negative-shape"
    if negative_shape:
        erps = -erps

    # --------------------------------------------------------------------



    return erps, flagInd, samplerate, negative_shape, ch_Nice
    #-----------------------------------------------------------------
    




#-----------------------------------------------------------------
# MAIN CONTROLLER
#-----------------------------------------------------------------


def output_erps(option):

    #---------
    mode = 1
    #---------


    if mode == 1 or mode == 4:

        # Folder Path
        path = r"C:\Users\AlexPM\Documents\University\Proyecto de Grado\DISEÑO Y DESARROLLO\GUI and Data Processing\v13.0_ImageAnalysisMode\v13.0_ImageAnalysisMode"


    else:

        # Folder Path
        path = r"C:\Users\AlexPM\Documents\University\Proyecto de Grado\DISEÑO Y DESARROLLO\GUI and Data Processing\Databases - clean tests\PRUEBAS_3.0\My Tests\Test 1 - Con Delay 5s\DB1"
    # -----------------------------------------------------------------


    if mode == 1 or mode == 4:

        # Change the directory
        os.chdir(path)

        # ---------------------
        mediciones = []
        timesArduino = []
        timesOpSesame = []

        names_files = []
        # ---------------------

        # iterate through all files in path
        for file in os.listdir():

            # Check whether file is in text format
            if file.endswith(".txt"):
                # --------------------------------------------------
                # Saving the name of the objective
                names_files.append(file[len(file) - 7: len(file) - 4])
                # --------------------------------------------------

                file_path = f"{path}\{file}"

                with open(file_path, 'r') as f:
                    mediciones.append(f.read())
                    timesArduino.append(datetime.datetime.fromtimestamp(os.stat(file_path).st_mtime))

            # Check if the file is the .csv from Open Sesame
            if file.endswith(".csv"):
                file_path = f"{path}\{file}"

                with open(file_path, 'r') as f:
                    timesOpSesame.append(f.read())





        erps, flagInd, samplerate, neg_shape, CH_Nice = erps_calculation(mediciones[0], timesOpSesame[0], timesArduino[0], option)


    return erps, flagInd, samplerate, neg_shape, CH_Nice, names_files




#--------------------------------------------------------------------
#
# ██████  ██    ██                                               
# ██   ██  ██  ██  ██                                            
# ██████    ████                                                 
# ██   ██    ██    ██                                            
# ██████     ██                                                  
                                                               
                                                               
#  █████  ██      ███████ ██   ██     ███████ ██████  ███    ███ 
# ██   ██ ██      ██       ██ ██      ██      ██   ██ ████  ████ 
# ███████ ██      █████     ███       █████   ██████  ██ ████ ██ 
# ██   ██ ██      ██       ██ ██      ██      ██      ██  ██  ██ 
# ██   ██ ███████ ███████ ██   ██     ██      ██      ██      ██ 
#
#--------------------------------------------------------------------





