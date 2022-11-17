#CLASSIFIER: MAIN CALCULATION AND CRITERIAS

import numpy as np
from numpy.fft import fft, ifft

flagInd = np.zeros(9)
samplerate = 250



def target_predict(initT, erps, negative_shape):

    p3 = np.empty(shape=(9, 100))

    for x in range(9):
        erpsAux = erps[x]

        # EXTRACT FROM ERPS A WINDOW OF 0.4s
        erpsAux = erpsAux[initT: initT + 100]

        p3[x] = erpsAux

    # -----------------------------------------------------------------

    freq_erps_all = np.empty(shape=(9, 100))
    for x in range(9):
        freq_erps_all[x] = fft(p3[x])

    # -----------------------------------------------------------------

    new_erps = np.empty(shape=(9, 100))

    for x in range(9):
        new_erps[x] = ifft(freq_erps_all[x])


    # OPTIONS
    events = {
        1: "VEN",
        2: "BRZ",
        3: "USA",
        4: "UK",
        5: "JPN",
        6: "IND",
        7: "FIN",
        8: "ITA",
        9: "COL"
    }


    eventsR2 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    eventsR3 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    eventsR4 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    eventsR5 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    eventsR6 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    eventsR7 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}


    # -----------------------------------------------------------------
    # FFT: SHOW ONLY THE FIRST 15 SAMPLES (UNTIL 32 Hz)

    freq_erps = np.empty(shape=(9, 15))

    for x in range(9):
        auxfft = freq_erps_all[x]

        auxfft = auxfft[0: 15]


        freq_erps[x] = np.abs(auxfft)
        #freq_erps[x] = auxfft
    # -----------------------------------------------------------------


    # RULE 5:
    for x in range(9):

        auxfft = freq_erps[x]

        if 1 - (auxfft[0] / max(auxfft[0:2])) * 100 > 60:
            eventsR5[x + 1] = eventsR5[x + 1] + 1


    # RULE 7:

    options = []
    mid_max = []
    der_vec = []

    # Maximum
    for x in range(9):
        aux = new_erps[x]

        options.append(aux[int(len(aux) / 2)])  # Copy of max with no sort
        mid_max.append(aux[int(len(aux) / 2)])  # Maximum occurs in mid of size

    mid_max.sort(reverse=True)


    # Eliminate non-targets
    for x in range(9):

        # Rule2
        if eventsR2[x + 1] > 0:
            new_erps[x] = 0

        # Rule3
        if eventsR3[x + 1] > 0:
            new_erps[x] = 0

        # Rule4
        if eventsR4[x + 1] > 0:
            new_erps[x] = 0

        # Rule5
        if eventsR5[x + 1] > 0:
            new_erps[x] = 0

        # Rule6
        if eventsR6[x + 1] > 0:
            new_erps[x] = 0

        # Rule7
        if eventsR7[x + 1] > 0:
            new_erps[x] = 0


    # -----------------------------------------------------------
    # Criteria to adjust some possible false-negative results

    for w in range(9):
        # Derivative
        der_vec.append(np.gradient(new_erps[w]))

    pos_cont = False
    neg_cont = False

    for x in range(9):

        if mid_max[x] > 0:
            pos_cont = True

        if mid_max[x] < 0:
            neg_cont = True

    aux = mid_max

    aux.sort()

    if pos_cont == True and neg_cont == True:

        for x in range(4):

            ind_op1 = options.index(aux[x])

            op1 = new_erps[ind_op1]

            # If one of the last options have a upward-shape, but negative value,
            # then it should be turn to positive-value cuz it's a possible objective
            aux1 = der_vec[ind_op1]

            if aux1[int(len(aux1) / 2) - 2] > 0.8:
                new_erps[ind_op1] = -new_erps[ind_op1]

    # ------------------------------------------------------------------

    # -------------------------------------------------------
    # -------------------------------------------------------
    #
    # SELECTING THE MOST PROBABLE OPTIONS FROM THE ERPS
    #
    # -------------------------------------------------------
    # -------------------------------------------------------

    prob_events = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0
    }

    zero_cont = 0

    # For POSITIVE-SHAPE
    if negative_shape == False:

        # Create a dict with the max values from the ERPs
        for x in range(len(flagInd)):

            aux_prob = new_erps[x]

            prob_events[x + 1] = aux_prob[int(len(new_erps[x]) / 2)]

            # Cont for number of zero-options
            if np.all(aux_prob == 0):
                zero_cont = zero_cont + 1





    # For NEGATIVE-SHAPE
    else:

        # Analysis of options at mid-range
        pos_cont = 0
        neg_cont = 0

        for x in range(9):

            if options[x] > 0:
                pos_cont = pos_cont + 1

            if options[x] < 0:
                neg_cont = neg_cont + 1

        # #----------------------------------------
        # print("positive count: %d" % pos_cont)
        # print("negative count: %d" % neg_cont)
        # #----------------------------------------

        # ALL THE OPTIONS ARE POSITIVE
        if pos_cont == 9:

            for x in range(len(flagInd)):
                aux_prob = -new_erps[x]

                # Select the order using magnitudes at t=0.06 aprox. (new_erps)
                prob_events[x + 1] = aux_prob[15]





        # ALL THE OPTIONS ARE NEGATIVE
        elif neg_cont == 9:

            for x in range(len(flagInd)):
                aux_prob = new_erps[x]

                # Select the order using magnitudes at t=0.0820 aprox. (new_erps)
                prob_events[x + 1] = aux_prob[21]





        # THERE ARE POSITIVE AND NEGATIVE OPTIONS
        else:

            # Interpolation of Data, to obtain more samples
            from scipy.interpolate import make_interp_spline

            erps_interp = []

            timeERP = np.arange(new_erps[0].shape[0]) / samplerate

            timeERP_new = np.linspace(timeERP.min(), timeERP.max(), 500)

            for x in range(9):
                X_Y_Spline = make_interp_spline(timeERP, new_erps[x])

                erps_interp.append(X_Y_Spline(timeERP_new))

            # New derivatives to interpolated data:

            der_vec = []

            # --------------------------------------------
            for w in range(9):
                # Derivative
                der_vec.append(np.gradient(erps_interp[w]))
            # --------------------------------------------

            # Analysis using derivative for each ERP (in the middle of range)
            pos_cont = 0
            neg_cont = 0

            #------------------------------------------------------

            for x in range(9):

                aux = der_vec[x]

                # If upward-pointing shape
                if aux[int(len(aux) / 2) - 1] > 0:
                    pos_cont = pos_cont + 1

                    continue

                # If downward-pointing shape
                if aux[int(len(aux) / 2) - 1] < 0:
                    neg_cont = neg_cont + 1

                    continue

            # #----------------------------------------
            # print("\n")
            # print("positive curves: %d" % pos_cont)
            # print("negative curves: %d" % neg_cont)
            # print("\n")
            # #----------------------------------------

            # Create a dict with the max values from the ERPs for two cases:

            # There are more upward-pointing curves than downward-pointing
            if pos_cont > neg_cont:

                for x in range(len(flagInd)):
                    aux_prob = new_erps[x]

                    # Select the order using magnitudes at t=0.0820 aprox.
                    prob_events[x + 1] = aux_prob[21]



            # There are more downward-pointing curves than upward-pointing
            elif neg_cont > pos_cont:

                for x in range(len(flagInd)):
                    aux_prob = -new_erps[x]

                    # Select the order using magnitudes at t=0.148 aprox.
                    prob_events[x + 1] = aux_prob[37]




            # Tie, only possible on the case where a flag didn't appear
            # To solve it, the actual solution is to delete JPN from options
            # and, recalculate (with that, the number of options is again odd)
            else:

                # JPN is the 4th option
                der_vec[4] = np.zeros_like(der_vec[0])

                # Recalculate
                pos_cont = 0
                neg_cont = 0

                for x in range(9):

                    aux = der_vec[x]

                    # If upward-pointing shape
                    if aux[int(len(aux) / 2) - 1] > 0:
                        pos_cont = pos_cont + 1

                        continue

                    # If downward-pointing shape
                    if aux[int(len(aux) / 2) - 1] < 0:
                        neg_cont = neg_cont + 1

                        continue

                # There are more upward-pointing curves than downward-pointing
                if pos_cont > neg_cont:

                    for x in range(len(flagInd)):
                        aux_prob = new_erps[x]

                        # Select the order using magnitudes at t=0.0820 aprox.
                        prob_events[x + 1] = aux_prob[21]



                # There are more downward-pointing curves than upward-pointing
                elif neg_cont > pos_cont:

                    for x in range(len(flagInd)):
                        aux_prob = -new_erps[x]

                        # Select the order using magnitudes at t=0.148 aprox.
                        prob_events[x + 1] = aux_prob[37]

    # -------------------------------------------------------------


    # ------------------------
    # ADDITIONAL CRITERIAS
    # ------------------------

    # -------------------------------------------------------------
    # If all the new_erps are zero or just 1 option, use max time-magnitudes

    if np.all(new_erps == 0) or zero_cont == 8:

        for x in range(len(flagInd)):
            aux_prob = p3[x]

            prob_events[x + 1] = max(aux_prob[37:50])
    # -------------------------------------------------------------

    # SORTING THE EVENTS
    sort_events = sorted(prob_events.items(), key=lambda x: x[1], reverse=True)

    scores = []
    stimulus = []

    for x in range(len(sort_events)):

        aux = sort_events[x]

        if aux[1] != 0:
            scores.append(aux[1])
            stimulus.append(events[aux[0]])


    # -------------------------------------------------------------
    # TESTING:
    # ELIMINATES ONE OF THE OPTIONS IF THE DISTANCE BEWTWEEN 2 OPTIONS IS
    # EXTREMELY SMALL OR IN A SPECIAL RANGE (FOR NOW, ONLY APPLIES TO ORIGINALLY
    # POSITIVE-SHAPE TESTS)

    if negative_shape == False:

        ind_op1 = options.index(mid_max[0])
        ind_op2 = options.index(mid_max[1])

        op1 = new_erps[ind_op1]
        op2 = new_erps[ind_op2]

        dis = np.abs(op1[int(len(op1) / 2)] - op2[int(len(op2) / 2)])

        if dis > 25 and dis < 32:
            new_erps[ind_op2] = 0

        if dis < 2:
            new_erps[ind_op2] = 0

    # -------------------------------------------------------------


    # -------------------------------------------------------------
    # Moving JPN to last place
    try:

        # JPN goes to last place
        JpnInd = stimulus.index('JPN')
        auxSwap = scores[JpnInd]

        scores.pop(JpnInd)
        stimulus.pop(JpnInd)

        scores.append(auxSwap)
        stimulus.append('JPN')

    except:

        print('Jpn was not the Focus')


    return scores, stimulus


