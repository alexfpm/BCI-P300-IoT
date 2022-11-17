

import numpy as np
from numpy.fft import fft, ifft




#-----------------------------------------------------------------
# CALCULATION OF BEST initT
#-----------------------------------------------------------------


#Function to calculate intersections of 2 plots with numerical methods!

def find_intersections(data1, data2):


    timeERP = np.arange(data1.shape[0]) / 250


    curve1 = data1
    curve2 = data2


    intersections = []
    prev_dif = 0

    t0, prev_c1, prev_c2 = None, None, None

    for t1, c1, c2 in zip(timeERP, curve1, curve2):
        new_dif = c2 - c1
        if np.abs(new_dif) < 1e-12: # found an exact zero, this is very unprobable
            intersections.append((t1, c1))
        elif new_dif * prev_dif < 0:  # the function changed signs between this point and the previous
            # do a linear interpolation to find the t between t0 and t1 where the curves would be equal
            # this is the intersection between the line [(t0, prev_c1), (t1, c1)] and the line [(t0, prev_c2), (t1, c2)]
            # because of the sign change, we know that there is an intersection between t0 and t1
            denom = prev_dif - new_dif
            intersections.append(((-new_dif*t0  + prev_dif*t1) / denom, (c1*prev_c2 - c2*prev_c1) / denom))
        t0, prev_c1, prev_c2, prev_dif = t1, c1, c2, new_dif


    return intersections




#MAIN ROUTINE THAT CALCULATES THE BEST INIT TO BEGIN:
#First appereance of a Gauss-shape stimulus, with some high value among the others

def calculate_optimal_init(f1_limit, erps):


    der_vec = []

    feature1_cont = 0
    feature2_cont = 0


    #Testing from init = 60 to init=90 (max until now)

    #for initT in range(70, 71):
    for initT in range(60, 90):


        #--------------------------------------------
        #CALCULATE SLICE OF ERPS BASED ON initT

        init_erps = np.empty(shape=(9, 100))



        for x in range(9):

            erpsAux = erps[x]

            erpsAux = erpsAux[initT : initT+100]

            init_erps[x] = erpsAux

        #--------------------------------------------
        #CREATE NEW ERPS

        f_erps_all = np.empty(shape = (9, 100))


        for x in range(9):

            f_erps_all[x] = fft(init_erps[x])



        #Take only the first 15 samples (until 32 Hz)
        f_erps = np.empty(shape = (9, 15))


        for x in range(9):

            auxfft = f_erps_all[x]

            auxfft = auxfft[0 : 15]


            f_erps[x] = auxfft



        new_erps = np.empty(shape = (9, 100))



        for x in range(9):

            new_erps[x] = ifft(f_erps_all[x])



        #------------------
        #Some variables to help

        testWindow = []
        mid_max = []
        options = []

        top2 = 0
        low_options = 0
        cut1 = 0
        cut2 = 0
        focus = 0


        feature1 = False
        feature2 = False
        skip = False
        #------------------



        #Setting the window of test
        for x in range(9):

            aux = new_erps[x]

            #Range to search the "gauss-form" stimulus
            testWindow.append(aux[40 : 60])


        #Maximum
        for x in range(9):
            aux = testWindow[x]

            options.append(aux[10]) #Copy of max with no sort
            mid_max.append(aux[10]) #Maximum occurs in 10 = mid of size

        mid_max.sort(reverse=True)



        #Discard first option if it's 0.0
        if mid_max[0] == 0.0:

            mid_max.pop(0)
            mid_max.append(0.0)





        #--------------------------------------
        top2 = sum(mid_max[0:1])/2
        low_options = sum(mid_max[3:6])/4
        #--------------------------------------



        #--------------------------------------
        #FEATURE 1

        #if (mid_max[0] - mid_max[1]) > 20:
        #if (mid_max[0] - mid_max[1]) > 30: #There is high difference between 1st and 2nd

        if np.abs((np.abs(mid_max[0]) - np.abs(mid_max[1]))) > f1_limit: #There is high difference between 1st and 2nd


            #Flag to indicate the activation of Feature 1:
            feature1 = True

            #Counter to know how many times it entered this feature
            feature1_cont = feature1_cont + 1


            print('Feature 1  activated with initT: ')
            print(initT)
            print('\n')



            for x in range(8):

                #Reseting derivatives array
                der_vec = []


                #TOP-2 Options of the iteration
                ind_op1 = options.index(mid_max[x])
                ind_op2 = options.index(mid_max[x+1])

                op1 = testWindow[ind_op1]
                op2 = testWindow[ind_op2]


                #Derivative of every ERP-piece in moment of interest
                for w in range(9):

                    #Derivative
                    der_vec.append(np.gradient(testWindow[w]))


                #If op1 is a downward pointing curve, IT'S NOT THE OBJECTIVE
                #Keeps trying with other options
                aux = der_vec[ind_op1]

                if aux[int(len(aux)/2)-3] < 0:

                    continue


                else: #It'a upward pointing curve: Gaussian form


                    #Finding where the options cut each other, to calculate
                    #the distance between these points. This may be a good
                    #feature


                    #----------------------------------------------------------
                    #Call the Function to calculate intersections (if exists)
                    cut_points = find_intersections(op1, op2)
                    #----------------------------------------------------------



                    if len(cut_points) == 2: #the plots have 2 clear intersections

                        aux1 = cut_points[0]
                        aux2 = cut_points[1]

                        cut1 = aux1[0]
                        cut2 = aux2[0]

                        #If the option 2 doesn't have a "Gauss-form" or cuts the
                        #first option too high, this is FALSE OBJECTIVE. So, it
                        #keeps searching
                        #if np.abs(cut2-cut1) <= 0.024: #Empirical value :v
                        if np.abs(cut2-cut1) <= 0.015: #Empirical value :v

                            print('Number of intersections: %d' % len(cut_points))
                            print('Local iteration number: %d' % x)
                            print('Difference of intersections: %f' % np.abs(cut2-cut1))


                            continue






                        else:

                            aux = np.abs(np.abs(op2[10])-np.abs(op1[10]))
                            print('Difference of max points: %f' % aux)
                            print('Local iteration number: %d' % x)

                            if np.abs(np.abs(op2[10])-np.abs(op1[10])) < 7:

                                continue

                            else:

                                #It's a very possible stimulus!

                                print('\n Possible stimulus detected!')
                                print('Difference of intersections: %f' % np.abs(cut2-cut1))

                                focus = 1


                                break







                    elif len(cut_points) == 4:

                        print('WORKING ON THIS CASE')
                        print('Number of intersections: %d' % len(cut_points))
                        print('Local iteration number: %d' % x)

                        aux1 = cut_points[1]
                        aux2 = cut_points[2]

                        cut1 = aux1[0]
                        cut2 = aux2[0]

                        #If the option 2 doesn't have a "Gauss-form" or cuts the
                        #first option too high, this is FALSE OBJECTIVE. So, it
                        #keeps searching
                        #if np.abs(cut2-cut1) <= 0.024: #Empirical value :v
                        if np.abs(cut2-cut1) <= 0.012: #Empirical value :v

                            print('Number of intersections: %d' % len(cut_points))
                            print('Local iteration number: %d' % x)
                            print('Difference of intersections: %f' % np.abs(cut2-cut1))


                            continue


                        else:

                            aux = der_vec[ind_op2]

                            if aux[int(len(aux)/2)-3] < 0:

                                print('Second option does NOT have a Gauss-shape\n')


                                continue

                            else:

                                print('\n Possible stimulus detected!')

                                focus = 1


                                break



                    elif len(cut_points) == 0:

                        print('WORKING ON THIS CASE')
                        print('Number of intersections: %d' % len(cut_points))
                        print('Local iteration number: %d' % x)


                        #focus = 1

                        break




        if focus == 1:

            print('\n')
            print('Local iteration number: %d' % x)
            print('Number of intersections: %d' % len(cut_points))



            if len(cut_points) == 1:

                #Analyze second option: if cuts the first option too high,
                # then maybe de algorith didn't detect it
                if np.abs(op1[7])-np.abs(op2[7]) > 90:

                    continue

                else:

                    #It's a very possible stimulus!

                    print('\n Possible stimulus detected!')

                    print('OJO AQUI PAPU')


                    break



            else:

                break



    return initT



#End of the main "for" loop
#--------------------------------------



# -----------------------------------------------
# COMPUTE CALCULATION
# -----------------------------------------------

def output_optimal_init(my_erps):

    optimal_init = calculate_optimal_init(30, my_erps)  # Initial threshold for Feature 1 = 30


    #Feature 3
    #The previous iteration reached the maximum value and it never
    #fulfilled the criterias

    feature3 = False
    feature3_cont = 0



    if optimal_init == 89:

        #Flag to indicate the activation of Feature 3:
        feature3 = True

        #Counter to know how many times it entered this feature
        feature3_cont = feature3_cont + 1



        limit_init = 89
        f1_threshold = 20

        while feature3:

            #Relaunching the previous function with different limit
            optimal_init = calculate_optimal_init(f1_threshold, my_erps)

            if optimal_init != limit_init:

                feature3 = False

                break

            else:
                f1_threshold = f1_threshold - 2


        print('\n Feature 3 was the judge with threshold:')
        print(f1_threshold)



    return optimal_init



#-------------------------------------------------------------------------------



