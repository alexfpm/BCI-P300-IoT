#---------------
#By: Alex FPM
#---------------
import time

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty, ColorProperty

#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.clock import Clock

import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, ifft



# Here for providing colour to the background
from kivy.core.window import Window

# Setting the window size
Window.clearcolor = (1, 1, 1, 1) # White background
Window.size = (960, 650)

# Setting the window Position (on the PC screen)
Window.top = 60
Window.left = 200

# Some general files to extract variables
import variables_Nice
import variables_Nice_revFilt



# Time-Series Data
class Tab1(MDFloatLayout, MDTabsBase):

    box = ObjectProperty(None)
    chk1 = ObjectProperty(None)
    chk2 = ObjectProperty(None)
    dialog = ObjectProperty(None)
    op1 = ObjectProperty(None)
    op2 = ObjectProperty(None)


    def add_plot_ch1(self):

        if self.op2.active:
            erps, flagInd, samplerate, neg_shape, ch1, names_files = variables_Nice_revFilt.output_erps(1)

        else:
            erps, flagInd, samplerate, neg_shape, ch1, names_files = variables_Nice.output_erps(1)


        #CH1 Plot
        figCH1 = plt.figure()
        time_vec = np.arange(ch1.shape[0]) / 250

        #plt.plot(time_vec[1000:14000], ch1[1000:14000], '#1fa321')
        plt.plot(time_vec, ch1, '#1fa321')


        plt.ylabel('Amplitude [μV]')
        plt.xlabel('Time [s]')
        plt.legend(["CH1"], loc="upper right")

        plt.grid(True)
        self.fig1 = figCH1

        return self.fig1


    def add_plot_ch2(self):

        if self.op2.active:
            from variables_Nice_revFilt_two import ch2_Cz

        else:
            from variables_Nice_two import ch2_Cz


        #CH2 Plot
        figCH2 = plt.figure()
        time_vec = np.arange(ch2_Cz.shape[0]) / 250

        #plt.plot(time_vec[1000:14000], ch2_Cz[1000:14000], '#1d2c82')
        plt.plot(time_vec, ch2_Cz, '#1d2c82')

        plt.ylabel('Amplitude [μV]')
        plt.xlabel('Time [s]')
        plt.legend(["CH2"], loc="upper right")

        plt.grid(True)
        self.fig2 = figCH2

        return self.fig2


    def add_plot_ch3(self):

        if self.op2.active:
            from variables_Nice_revFilt_three import ch3_Pz

        else:
            from variables_Nice_three import ch3_Pz


        #CH3 Plot
        figCH3 = plt.figure()
        time_vec = np.arange(ch3_Pz.shape[0]) / 250

        #plt.plot(time_vec[1000:14000], ch3_Pz[1000:14000], '#fc5e03')
        plt.plot(time_vec, ch3_Pz, '#fc5e03')

        plt.ylabel('Amplitude [μV]')
        plt.xlabel('Time [s]')
        plt.legend(["CH3"], loc="upper right")

        plt.grid(True)
        self.fig3 = figCH3

        return self.fig3


    #Main PLOT Button
    def show_plot(self):
        plt.close('all')
        self.box.clear_widgets()

        if self.chk1.active:
            self.fig1 = Tab1.add_plot_ch1(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig1))

        if self.chk2.active:
            self.fig2 = Tab1.add_plot_ch2(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig2))

        if self.chk3.active:
            self.fig3 = Tab1.add_plot_ch3(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig3))


        #No channel selected
        if self.chk1.active==False and self.chk2.active==False and self.chk3.active==False:

            self.dialog = MDDialog(
                title="No channel selected!",
                text = "Please select a channel",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release = self.close_dialog_box
                    ),
                ],
            )
            self.dialog.open()


    def close_dialog_box(self, obj):
        # Close warning message
        self.dialog.dismiss()


# FFT
class Tab2(MDFloatLayout, MDTabsBase):

    box = ObjectProperty(None)
    chk1 = ObjectProperty(None)
    chk2 = ObjectProperty(None)
    dialog = ObjectProperty(None)
    op1 = ObjectProperty(None)
    op2 = ObjectProperty(None)

    def add_plot_ch1(self):

        if self.op2.active:
            erps, flagInd, samplerate, neg_shape, ch1, names_files = variables_Nice_revFilt.output_erps(1)

        else:
            erps, flagInd, samplerate, neg_shape, ch1, names_files = variables_Nice.output_erps(1)


        # FFT calculation
        freq_ch1 = np.abs(fft(ch1))

        # Frequency vector
        N1 = len(freq_ch1)
        n1 = np.arange(N1)
        T1 = N1 / samplerate
        freq_vec = n1 / T1

        # CH1 Plot
        figCH1 = plt.figure()

        plt.plot(freq_vec[0: 2000], freq_ch1[0: 2000], '#1fa321')

        plt.ylabel('Amplitude')
        plt.xlabel('Frequency [Hz]')
        plt.legend(["CH1"], loc="upper right")

        plt.grid(True)
        self.fig1 = figCH1

        return self.fig1


    def add_plot_ch2(self):

        if self.op2.active:
            erps, flagInd, samplerate, neg_shape, ch2_Cz, names_files = variables_Nice_revFilt.output_erps(2)

        else:
            erps, flagInd, samplerate, neg_shape, ch2_Cz, names_files = variables_Nice.output_erps(2)


        # FFT calculation
        freq_ch2 = np.abs(fft(ch2_Cz))

        # Frequency vector
        N1 = len(freq_ch2)
        n1 = np.arange(N1)
        T1 = N1 / samplerate
        freq_vec = n1 / T1

        # CH2 Plot
        figCH2 = plt.figure()

        plt.plot(freq_vec[0: 2000], freq_ch2[0: 2000], '#1d2c82')

        plt.ylabel('Amplitude')
        plt.xlabel('Frequency [Hz]')
        plt.legend(["CH2"], loc="upper right")

        plt.grid(True)
        self.fig2 = figCH2

        return self.fig2


    def add_plot_ch3(self):

        if self.op2.active:
            erps, flagInd, samplerate, neg_shape, ch3_Pz, names_files = variables_Nice_revFilt.output_erps(3)

        else:
            erps, flagInd, samplerate, neg_shape, ch3_Pz, names_files = variables_Nice.output_erps(3)


        # FFT calculation
        freq_ch3 = np.abs(fft(ch3_Pz))

        # Frequency vector
        N1 = len(freq_ch3)
        n1 = np.arange(N1)
        T1 = N1 / samplerate
        freq_vec = n1 / T1

        # CH3 Plot
        figCH3 = plt.figure()

        plt.plot(freq_vec[0: 2000], freq_ch3[0: 2000], '#fc5e03')

        plt.ylabel('Amplitude')
        plt.xlabel('Frequency [Hz]')
        plt.legend(["CH3"], loc="upper right")

        plt.grid(True)
        self.fig3 = figCH3

        return self.fig3


    # Main PLOT Button
    def show_plot(self):
        plt.close('all')
        self.box.clear_widgets()

        if self.chk1.active:
            self.fig1 = Tab2.add_plot_ch1(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig1))

        if self.chk2.active:
            self.fig2 = Tab2.add_plot_ch2(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig2))

        if self.chk3.active:
            self.fig3 = Tab2.add_plot_ch3(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig3))

        # No channel selected
        if self.chk1.active == False and self.chk2.active == False and self.chk3.active == False:
            self.dialog = MDDialog(
                title="No channel selected!",
                text="Please select a channel",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_dialog_box
                    ),
                ],
            )
            self.dialog.open()

    def close_dialog_box(self, obj):
        # Close warning message
        self.dialog.dismiss()



# ERP
class Tab3(MDFloatLayout, MDTabsBase):

    box = ObjectProperty(None)
    chk1 = ObjectProperty(None)
    chk2 = ObjectProperty(None)
    dialog = ObjectProperty(None)
    op1 = ObjectProperty(None)
    op2 = ObjectProperty(None)

    slider_val_1 = ObjectProperty(None)
    slider_val_2 = ObjectProperty(None)

    show_sliders = BooleanProperty(False)



    def add_plot_ch2(self):

        if self.op2.active:
            from variables_Nice_revFilt_two import erps_ch2

        else:
            from variables_Nice_two import erps_ch2


        # -----------------------------------------------------------------
        # ERP's PLOT
        # -----------------------------------------------------------------

        # CH2 Plot
        figCH2 = plt.figure()
        timeERP = np.arange(erps_ch2[0].shape[0]) / 250

        # Plotting selected data
        colors = ['r', '#35ad09', 'k', '#0838a8', 'm', 'c', '#fc5e03', '#aaaaaa', 'y']

        for x in range(9):
            plt.plot(timeERP, erps_ch2[x], colors[x])

        plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

        plt.ylabel('Volts [μV]')
        plt.xlabel('Time [s]')
        plt.title("ERP's from Flag's Interface: CH2")

        plt.grid(True)
        self.fig1 = figCH2

        return self.fig1


    def add_plot_ch3(self):

        if self.op2.active:
            from variables_Nice_revFilt_three import erps_ch3

        else:
            from variables_Nice_three import erps_ch3


        # -----------------------------------------------------------------
        # ERP's PLOT
        # -----------------------------------------------------------------

        # CH3 Plot
        figCH3 = plt.figure()
        timeERP = np.arange(erps_ch3[0].shape[0]) / 250

        # Plotting selected data
        colors = ['r', '#35ad09', 'k', '#0838a8', 'm', 'c', '#fc5e03', '#aaaaaa', 'y']

        for x in range(9):
            plt.plot(timeERP, erps_ch3[x], colors[x])

        plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

        plt.ylabel('Volts [μV]')
        plt.xlabel('Time [s]')
        plt.title("ERP's from Flag's Interface: CH3")

        plt.grid(True)
        self.fig2 = figCH3

        return self.fig2


    # Main PLOT Button
    def show_plot(self):
        plt.close('all')
        self.box.clear_widgets()


        if self.chk1.active:
            self.fig1 = Tab3.add_plot_ch2(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig1))

            # Unhide sliders
            self.show_sliders = True


        if self.chk2.active:
            self.fig2 = Tab3.add_plot_ch3(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig2))

            # Unhide sliders
            self.show_sliders = True


        # No channel selected
        if self.chk1.active == False and self.chk2.active == False:

            # Hide sliders
            self.show_sliders = False

            # Warning message
            self.dialog = MDDialog(
                title="No channel selected!",
                text="Please select a channel",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_dialog_box
                    ),
                ],
            )
            self.dialog.open()

    def close_dialog_box(self, obj):
        # Close warning message
        self.dialog.dismiss()


    def change_window_r(self, time_r):

        # ESSENTIAL: The below command "plt.close('all')" is the key to clear all figures
        # and assure the best performance, with no warnings or Memory-filling issues (checked against Task Manager)
        plt.close('all')
        self.box.clear_widgets()


        # Checkbox for CH2
        if self.chk1.active:

            if self.op2.active:
                from variables_Nice_revFilt_two import erps_ch2

            else:
                from variables_Nice_two import erps_ch2

            # -----------------------------------------------------------------
            # ERP's PLOT
            # -----------------------------------------------------------------

            # CH2 Plot
            figCH2 = plt.figure()
            timeERP = np.arange(erps_ch2[0].shape[0]) / 250

            # Window-adjust with Sliders
            timeERP = timeERP[int(self.slider_val_2.value): int(time_r)]

            aux = int(time_r) - int(self.slider_val_2.value)
            erps_slider = np.empty([9, aux])

            for x in range(9):
                aux = erps_ch2[x]

                aux = aux[int(self.slider_val_2.value): int(time_r)]

                erps_slider[x] = aux


            # Plotting selected data
            colors = ['r', '#35ad09', 'k', '#0838a8', 'm', 'c', '#fc5e03', '#aaaaaa', 'y']

            for x in range(9):
                plt.plot(timeERP, erps_slider[x], colors[x])

            plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

            plt.ylabel('Volts [μV]')
            plt.xlabel('Time [s]')
            plt.title("ERP's from Flag's Interface: CH2")

            plt.grid(True)
            self.fig1 = figCH2

            self.box.add_widget(FigureCanvasKivyAgg(self.fig1))


        # Checkbox for CH3
        if self.chk2.active:

            if self.op2.active:
                from variables_Nice_revFilt_three import erps_ch3

            else:
                from variables_Nice_three import erps_ch3


            # -----------------------------------------------------------------
            # ERP's PLOT
            # -----------------------------------------------------------------

            # CH3 Plot
            figCH3 = plt.figure()
            timeERP = np.arange(erps_ch3[0].shape[0]) / 250


            # Window-adjust with Sliders
            timeERP = timeERP[int(self.slider_val_2.value): int(time_r)]

            aux = int(time_r) - int(self.slider_val_2.value)
            erps_slider = np.empty([9, aux])

            for x in range(9):
                aux = erps_ch3[x]

                aux = aux[int(self.slider_val_2.value): int(time_r)]

                erps_slider[x] = aux


            # Plotting selected data
            colors = ['r', '#35ad09', 'k', '#0838a8', 'm', 'c', '#fc5e03', '#aaaaaa', 'y']

            for x in range(9):
                plt.plot(timeERP, erps_slider[x], colors[x])

            plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

            plt.ylabel('Volts [μV]')
            plt.xlabel('Time [s]')
            plt.title("ERP's from Flag's Interface: CH3")

            plt.grid(True)
            self.fig2 = figCH3


            self.box.add_widget(FigureCanvasKivyAgg(self.fig2))



    def change_window_l(self, time_l):

        #ESSENTIAL: The below command "plt.close('all')" is the key to clear all figures
        # and assure the best performance, with no warnings or Memory-filling issues (checked against Task Manager)
        plt.close('all')
        self.box.clear_widgets()


        # Checkbox for CH2
        if self.chk1.active:

            if self.op2.active:
                from variables_Nice_revFilt_two import erps_ch2

            else:
                from variables_Nice_two import erps_ch2

            # -----------------------------------------------------------------
            # ERP's PLOT
            # -----------------------------------------------------------------

            # CH2 Plot
            figCH2 = plt.figure()
            timeERP = np.arange(erps_ch2[0].shape[0]) / 250

            # Window-adjust with Sliders
            timeERP = timeERP[int(time_l): int(self.slider_val_1.value)]

            aux = int(self.slider_val_1.value) - int(time_l)
            erps_slider = np.empty([9, aux])

            for x in range(9):
                aux = erps_ch2[x]

                aux = aux[int(time_l): int(self.slider_val_1.value)]

                erps_slider[x] = aux


            # Plotting selected data
            colors = ['r', '#35ad09', 'k', '#0838a8', 'm', 'c', '#fc5e03', '#aaaaaa', 'y']

            for x in range(9):
                plt.plot(timeERP, erps_slider[x], colors[x])

            plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

            plt.ylabel('Volts [μV]')
            plt.xlabel('Time [s]')
            plt.title("ERP's from Flag's Interface: CH2")

            plt.grid(True)
            self.fig1 = figCH2

            self.box.add_widget(FigureCanvasKivyAgg(self.fig1))


        # Checkbox for CH3
        if self.chk2.active:

            if self.op2.active:
                from variables_Nice_revFilt_three import erps_ch3

            else:
                from variables_Nice_three import erps_ch3


            # -----------------------------------------------------------------
            # ERP's PLOT
            # -----------------------------------------------------------------

            # CH3 Plot
            figCH3 = plt.figure()
            timeERP = np.arange(erps_ch3[0].shape[0]) / 250


            # Window-adjust with Sliders
            timeERP = timeERP[int(time_l): int(self.slider_val_1.value)]

            aux = int(self.slider_val_1.value) - int(time_l)
            erps_slider = np.empty([9, aux])

            for x in range(9):
                aux = erps_ch3[x]

                aux = aux[int(time_l): int(self.slider_val_1.value)]

                erps_slider[x] = aux


            # Plotting selected data
            colors = ['r', '#35ad09', 'k', '#0838a8', 'm', 'c', '#fc5e03', '#aaaaaa', 'y']

            for x in range(9):
                plt.plot(timeERP, erps_slider[x], colors[x])

            plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

            plt.ylabel('Volts [μV]')
            plt.xlabel('Time [s]')
            plt.title("ERP's from Flag's Interface: CH3")

            plt.grid(True)
            self.fig2 = figCH3


            self.box.add_widget(FigureCanvasKivyAgg(self.fig2))



# New ERPs
class Tab4(MDFloatLayout, MDTabsBase):
    box = ObjectProperty(None)
    chk1 = ObjectProperty(None)
    chk2 = ObjectProperty(None)
    dialog = ObjectProperty(None)
    op1 = ObjectProperty(None)
    op2 = ObjectProperty(None)

    slider_val_1 = ObjectProperty(None)
    slider_val_2 = ObjectProperty(None)

    show_sliders = BooleanProperty(False)




    def add_plot_ch2(self):

        if self.op2.active:
            erps_ch2, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice_revFilt.output_erps(2)

        else:
            erps_ch2, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice.output_erps(2)

        import init_calculator
        initT = init_calculator.output_optimal_init(erps_ch2)


        p3 = np.empty(shape=(9, 100))

        for x in range(9):
            erpsAux = erps_ch2[x]

            # EXTRACT FROM ERPS A WINDOW OF 0.4s
            erpsAux = erpsAux[initT: initT + 100]

            p3[x] = erpsAux

        # -----------------------------------------------------------------

        freq_erps_all = np.empty(shape=(9, 100))
        for x in range(9):
            freq_erps_all[x] = fft(p3[x])
            #freq_erps_all[x] = np.abs(fft(p3[x]))

        # -----------------------------------------------------------------

        new_erps = np.empty(shape=(9, 100))

        for x in range(9):

            new_erps[x] = ifft(freq_erps_all[x])
            #new_erps[x] = np.abs(ifft(freq_erps_all[x]))


        # -----------------------------------------------------------------
        # ERP's PLOT
        # -----------------------------------------------------------------

        # CH2 Plot
        figCH2 = plt.figure()
        timeERP = np.arange(new_erps[0].shape[0]) / 250

        # Plotting selected data
        plt.plot(timeERP, new_erps[0], 'r')
        plt.plot(timeERP, new_erps[1], '#35ad09')
        plt.plot(timeERP, new_erps[2], 'k')
        plt.plot(timeERP, new_erps[3], '#0838a8')
        plt.plot(timeERP, new_erps[4], 'm')
        plt.plot(timeERP, new_erps[5], 'c')
        plt.plot(timeERP, new_erps[6], '#fc5e03')
        plt.plot(timeERP, new_erps[7], '#aaaaaa')
        plt.plot(timeERP, new_erps[8], 'y')

        plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

        plt.ylabel('Volts [μV]')
        plt.xlabel('Time [s]')
        plt.title("ERP's from Flag's Interface: CH2")

        plt.grid(True)
        self.fig1 = figCH2

        return self.fig1


    def add_plot_ch3(self):

        if self.op2.active:
            erps_ch3, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice_revFilt.output_erps(3)

        else:
            erps_ch3, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice.output_erps(3)

        import init_calculator
        initT = init_calculator.output_optimal_init(erps_ch3)


        p3 = np.empty(shape=(9, 100))

        for x in range(9):
            erpsAux = erps_ch3[x]

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

        # -----------------------------------------------------------------
        # ERP's PLOT
        # -----------------------------------------------------------------

        # CH3 Plot
        figCH3 = plt.figure()
        timeERP = np.arange(new_erps[0].shape[0]) / 250

        # Plotting selected data
        plt.plot(timeERP, new_erps[0], 'r')
        plt.plot(timeERP, new_erps[1], '#35ad09')
        plt.plot(timeERP, new_erps[2], 'k')
        plt.plot(timeERP, new_erps[3], '#0838a8')
        plt.plot(timeERP, new_erps[4], 'm')
        plt.plot(timeERP, new_erps[5], 'c')
        plt.plot(timeERP, new_erps[6], '#fc5e03')
        plt.plot(timeERP, new_erps[7], '#aaaaaa')
        plt.plot(timeERP, new_erps[8], 'y')

        plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

        plt.ylabel('Volts [μV]')
        plt.xlabel('Time [s]')
        plt.title("ERP's from Flag's Interface: CH3")

        plt.grid(True)
        self.fig2 = figCH3

        return self.fig2

    # Main PLOT Button
    def show_plot(self):
        plt.close('all')
        self.box.clear_widgets()


        if self.chk1.active:
            self.fig1 = Tab4.add_plot_ch2(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig1))

            # Unhide sliders
            self.show_sliders = True


        if self.chk2.active:
            self.fig2 = Tab4.add_plot_ch3(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig2))

            # Unhide sliders
            self.show_sliders = True


        # No channel selected
        if self.chk1.active == False and self.chk2.active == False:

            # Hide sliders
            self.show_sliders = False

            # Warning message
            self.dialog = MDDialog(
                title="No channel selected!",
                text="Please select a channel",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_dialog_box
                    ),
                ],
            )
            self.dialog.open()

    def close_dialog_box(self, obj):
        # Close warning message
        self.dialog.dismiss()


    def change_window_r(self, time_r):

        # ESSENTIAL: The below command "plt.close('all')" is the key to clear all figures
        # and assure the best performance, with no warnings or Memory-filling issues (checked against Task Manager)
        plt.close('all')
        self.box.clear_widgets()

        # Checkbox for CH2
        if self.chk1.active:

            if self.op2.active:
                from variables_Nice_revFilt_two import erps_ch2

            else:
                from variables_Nice_two import erps_ch2

            import init_calculator
            initT = init_calculator.output_optimal_init(erps_ch2)


            p3 = np.empty(shape=(9, 100))

            for x in range(9):
                erpsAux = erps_ch2[x]

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

            # -----------------------------------------------------------------
            # ERP's PLOT
            # -----------------------------------------------------------------

            # CH2 Plot
            figCH2 = plt.figure()
            timeERP = np.arange(new_erps[0].shape[0]) / 250

            # Window-adjust with Sliders
            timeERP = timeERP[int(self.slider_val_2.value): int(time_r)]

            aux = int(time_r) - int(self.slider_val_2.value)
            new_erps_s = np.empty([9, aux])

            for x in range(9):
                aux = new_erps[x]

                aux = aux[int(self.slider_val_2.value): int(time_r)]

                new_erps_s[x] = aux

            # Plotting selected data
            plt.plot(timeERP, new_erps_s[0], 'r')
            plt.plot(timeERP, new_erps_s[1], '#35ad09')
            plt.plot(timeERP, new_erps_s[2], 'k')
            plt.plot(timeERP, new_erps_s[3], '#0838a8')
            plt.plot(timeERP, new_erps_s[4], 'm')
            plt.plot(timeERP, new_erps_s[5], 'c')
            plt.plot(timeERP, new_erps_s[6], '#fc5e03')
            plt.plot(timeERP, new_erps_s[7], '#aaaaaa')
            plt.plot(timeERP, new_erps_s[8], 'y')

            plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

            plt.ylabel('Volts [μV]')
            plt.xlabel('Time [s]')
            plt.title("ERP's from Flag's Interface: CH2")

            plt.grid(True)
            self.fig1 = figCH2

            self.box.add_widget(FigureCanvasKivyAgg(self.fig1))

        # Checkbox for CH3
        if self.chk2.active:

            if self.op2.active:
                from variables_Nice_revFilt_three import erps_ch3

            else:
                from variables_Nice_three import erps_ch3

            import init_calculator
            initT = init_calculator.output_optimal_init(erps_ch3)


            p3 = np.empty(shape=(9, 100))

            for x in range(9):
                erpsAux = erps_ch3[x]

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

            # -----------------------------------------------------------------
            # ERP's PLOT
            # -----------------------------------------------------------------

            # CH3 Plot
            figCH3 = plt.figure()
            timeERP = np.arange(new_erps[0].shape[0]) / 250

            # Window-adjust with Sliders
            timeERP = timeERP[int(self.slider_val_2.value): int(time_r)]

            aux = int(time_r) - int(self.slider_val_2.value)
            new_erps_s = np.empty([9, aux])

            for x in range(9):
                aux = new_erps[x]

                aux = aux[int(self.slider_val_2.value): int(time_r)]

                new_erps_s[x] = aux


            # Plotting selected data
            plt.plot(timeERP, new_erps_s[0], 'r')
            plt.plot(timeERP, new_erps_s[1], '#35ad09')
            plt.plot(timeERP, new_erps_s[2], 'k')
            plt.plot(timeERP, new_erps_s[3], '#0838a8')
            plt.plot(timeERP, new_erps_s[4], 'm')
            plt.plot(timeERP, new_erps_s[5], 'c')
            plt.plot(timeERP, new_erps_s[6], '#fc5e03')
            plt.plot(timeERP, new_erps_s[7], '#aaaaaa')
            plt.plot(timeERP, new_erps_s[8], 'y')

            plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

            plt.ylabel('Volts [μV]')
            plt.xlabel('Time [s]')
            plt.title("ERP's from Flag's Interface: CH3")

            plt.grid(True)
            self.fig2 = figCH3

            self.box.add_widget(FigureCanvasKivyAgg(self.fig2))


    def change_window_l(self, time_l):

        # ESSENTIAL: The below command "plt.close('all')" is the key to clear all figures
        # and assure the best performance, with no warnings or Memory-filling issues (checked against Task Manager)
        plt.close('all')
        self.box.clear_widgets()

        # Checkbox for CH2
        if self.chk1.active:

            if self.op2.active:
                from variables_Nice_revFilt_two import erps_ch2

            else:
                from variables_Nice_two import erps_ch2

            import init_calculator
            initT = init_calculator.output_optimal_init(erps_ch2)


            p3 = np.empty(shape=(9, 100))

            for x in range(9):
                erpsAux = erps_ch2[x]

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

            # -----------------------------------------------------------------
            # ERP's PLOT
            # -----------------------------------------------------------------

            # CH2 Plot
            figCH2 = plt.figure()
            timeERP = np.arange(new_erps[0].shape[0]) / 250

            # Window-adjust with Sliders
            timeERP = timeERP[int(time_l): int(self.slider_val_1.value)]

            aux = int(self.slider_val_1.value) - int(time_l)
            new_erps_s = np.empty([9, aux])

            for x in range(9):
                aux = new_erps[x]

                aux = aux[int(time_l): int(self.slider_val_1.value)]

                new_erps_s[x] = aux


            # Plotting selected data
            plt.plot(timeERP, new_erps_s[0], 'r')
            plt.plot(timeERP, new_erps_s[1], '#35ad09')
            plt.plot(timeERP, new_erps_s[2], 'k')
            plt.plot(timeERP, new_erps_s[3], '#0838a8')
            plt.plot(timeERP, new_erps_s[4], 'm')
            plt.plot(timeERP, new_erps_s[5], 'c')
            plt.plot(timeERP, new_erps_s[6], '#fc5e03')
            plt.plot(timeERP, new_erps_s[7], '#aaaaaa')
            plt.plot(timeERP, new_erps_s[8], 'y')

            plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

            plt.ylabel('Volts [μV]')
            plt.xlabel('Time [s]')
            plt.title("ERP's from Flag's Interface: CH2")

            plt.grid(True)
            self.fig1 = figCH2

            self.box.add_widget(FigureCanvasKivyAgg(self.fig1))

        # Checkbox for CH3
        if self.chk2.active:

            if self.op2.active:
                from variables_Nice_revFilt_three import erps_ch3

            else:
                from variables_Nice_three import erps_ch3

            import init_calculator
            initT = init_calculator.output_optimal_init(erps_ch3)


            p3 = np.empty(shape=(9, 100))

            for x in range(9):
                erpsAux = erps_ch3[x]

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

            # -----------------------------------------------------------------
            # ERP's PLOT
            # -----------------------------------------------------------------

            # CH3 Plot
            figCH3 = plt.figure()
            timeERP = np.arange(new_erps[0].shape[0]) / 250

            # Window-adjust with Sliders
            timeERP = timeERP[int(time_l): int(self.slider_val_1.value)]

            aux = int(self.slider_val_1.value) - int(time_l)
            new_erps_s = np.empty([9, aux])

            for x in range(9):
                aux = new_erps[x]

                aux = aux[int(time_l): int(self.slider_val_1.value)]

                new_erps_s[x] = aux


            # Plotting selected data
            plt.plot(timeERP, new_erps_s[0], 'r')
            plt.plot(timeERP, new_erps_s[1], '#35ad09')
            plt.plot(timeERP, new_erps_s[2], 'k')
            plt.plot(timeERP, new_erps_s[3], '#0838a8')
            plt.plot(timeERP, new_erps_s[4], 'm')
            plt.plot(timeERP, new_erps_s[5], 'c')
            plt.plot(timeERP, new_erps_s[6], '#fc5e03')
            plt.plot(timeERP, new_erps_s[7], '#aaaaaa')
            plt.plot(timeERP, new_erps_s[8], 'y')

            plt.legend(["Ven", "Brz", "Usa", "UK", "Jpn", "Ind", "Fin", "Ita", "Col"], loc="upper right")

            plt.ylabel('Volts [μV]')
            plt.xlabel('Time [s]')
            plt.title("ERP's from Flag's Interface: CH3")

            plt.grid(True)
            self.fig2 = figCH3

            self.box.add_widget(FigureCanvasKivyAgg(self.fig2))


# Target Prediction and IoT
class Tab5(MDFloatLayout, MDTabsBase):

    box = ObjectProperty(None)
    chk1 = ObjectProperty(None)
    chk2 = ObjectProperty(None)
    dialog = ObjectProperty(None)
    op1 = ObjectProperty(None)
    op2 = ObjectProperty(None)


    def add_plot_ch2(self):

        import init_calculator
        import classifier_Output

        if self.op2.active:
            erps_ch2, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice_revFilt.output_erps(2)

        else:
            erps_ch2, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice.output_erps(2)


        optimal_init = init_calculator.output_optimal_init(erps_ch2)

        scores, stimulus = classifier_Output.target_predict(optimal_init, erps_ch2, neg_shape)

        # -----------------------
        # RESULTS AND CHART
        # -----------------------

        # Printing the Results:
        figCH2 = plt.figure()

        plt.bar(stimulus, scores)
        plt.ylabel('Scores')

        if names_files[0] == '_UK': names_files[0] = 'UK'

        plt.suptitle('CH2 Most probable Options - Focus: %s' % names_files[0])


        self.fig1 = figCH2

        return self.fig1


    def add_plot_ch3(self):

        import init_calculator
        import classifier_Output

        if self.op2.active:
            erps_ch3, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice_revFilt.output_erps(3)

        else:
            erps_ch3, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice.output_erps(3)


        optimal_init = init_calculator.output_optimal_init(erps_ch3)

        scores, stimulus = classifier_Output.target_predict(optimal_init, erps_ch3, neg_shape)

        # -----------------------
        # RESULTS AND CHART
        # -----------------------

        # Printing the Results:
        figCH3 = plt.figure()

        plt.bar(stimulus, scores)
        plt.ylabel('Scores')

        if names_files[0] == '_UK': names_files[0] = 'UK'

        plt.suptitle('CH3 Most probable Options - Focus: %s' % names_files[0])


        self.fig2 = figCH3

        return self.fig2


    # Main PLOT Button
    def show_plot(self):
        plt.close('all')
        self.box.clear_widgets()

        if self.chk1.active:
            self.fig1 = Tab5.add_plot_ch2(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig1))

        if self.chk2.active:
            self.fig2 = Tab5.add_plot_ch3(self)
            self.box.add_widget(FigureCanvasKivyAgg(self.fig2))

        # No channel selected
        if self.chk1.active == False and self.chk2.active == False:

            # Warning message
            self.dialog = MDDialog(
                title="No channel selected!",
                text="Please select AT LEAST one channel",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_dialog_box
                    ),
                ],
            )
            self.dialog.open()

    def close_dialog_box(self, obj):
        # Close warning message
        self.dialog.dismiss()


    def run_action_iot(self):

        import init_calculator
        import classifier_Output

        # There are 2 selected channels
        if self.chk1.active == True and self.chk2.active == True:
            # Warning message
            self.dialog = MDDialog(
                title="Two (2) channels selected",
                text="Please note: select ONLY 1 channel and then retry",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_dialog_box
                    ),
                ],
            )
            self.dialog.open()

        # No channel selected
        elif self.chk1.active == False and self.chk2.active == False:
            # Warning message
            self.dialog = MDDialog(
                title="No channel selected!",
                text="Please select ONLY 1 channel and retry",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_dialog_box
                    ),
                ],
            )
            self.dialog.open()


        else:  # No errors. Proceeding to execute the actions
            if self.chk1.active:
                # CH2 (Cz)
                if self.op2.active:
                    erps_ch2, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice_revFilt.output_erps(2)
                else:
                    erps_ch2, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice.output_erps(2)

                optimal_init = init_calculator.output_optimal_init(erps_ch2)
                scores, stimulus = classifier_Output.target_predict(optimal_init, erps_ch2, neg_shape)


            elif self.chk2.active:
                # CH3 (Pz)
                if self.op2.active:
                    erps_ch3, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice_revFilt.output_erps(3)
                else:
                    erps_ch3, flagInd, samplerate, neg_shape, ch_nice, names_files = variables_Nice.output_erps(3)

                optimal_init = init_calculator.output_optimal_init(erps_ch3)
                scores, stimulus = classifier_Output.target_predict(optimal_init, erps_ch3, neg_shape)


            import IoT_Actions

            # Predicted action
            target = stimulus[0]

            # Executing the detected action
            IoT_Actions.options_menu(target)



# Real-Time Mode
class Tab6(MDFloatLayout, MDTabsBase):

    box1 = ObjectProperty(None)



    # FILTERING
    # Filter requirements
    T = 1.0 / 9  # Sample Period

    global fs
    fs = 250.0  # sample rate, Hz (SPS)

    global cutoff
    cutoff = 20  # desired cutoff frequency of the filter, Hz

    nyq = 0.5 * fs  # Nyquist Frequency

    # order = 7       # Order of filter
    # order = 10
    global order
    order = 20

    n = int(T * fs)  # total number of samples

    # -----------------------------------------------------------------
    # LPF - METHOD 2
    # -----------------------------------------------------------------

    def butter_lowpass(self, cutoff, fs, order=5):

        from scipy.signal import butter

        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter2(self, data, cutoff, fs, order):

        from scipy.signal import lfilter

        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y


    # ------------------------------------------------------------------
    import datetime
    from datetime import datetime

    global timeOld
    timeOld = datetime.now()
    timeOld = timeOld.strftime("%H:%M:%S.%f")

    global minutesOld
    minutesOld = float(timeOld[3:5])

    global secOld
    secOld = float(timeOld[6:15])
    # ------------------------------------------------------------------


    def calculate_sec(self, minO, secO, minN, secN, data):

        # Same minutes
        if minO == minN:

            # Adjust window every 3 seconds
            if secN > secO + 3:
                meanY = sum(data) / len(data)

                # y_rangeNew = [meanY-1e-3, meanY+1e-3]
                y_rangeNew = [meanY - 3e-3, meanY + 3e-3]

                self.ax.set_ylim(y_rangeNew)

                minO = minN
                secO = secN

                return minO, secO

        # Different minutes
        if minN > minO:

            # Adjust window every 3 seconds
            if secN + (60 - secO) > 3:
                meanY = sum(data) / len(data)

                # y_rangeNew = [meanY-1e-3, meanY+1e-3]
                y_rangeNew = [meanY - 3e-3, meanY + 3e-3]

                self.ax.set_ylim(y_rangeNew)

                minO = minN
                secO = secN

                return minO, secO


    # -----------------------------------------------------------------------
    def warning_serial(self):
        self.dialog = MDDialog(
            title="No device detected!",
            text="Please connect ADS1299/Arduino to Serial Port and retry",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=self.close_dialog_box
                ),
            ],
        )
        self.dialog.open()

    def close_dialog_box(self, obj):
        # Close warning message
        self.dialog.dismiss()
    # -----------------------------------------------------------------------


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):

        import serial
        import time

        # Trying to begin SPI communication
        try:
            global ser
            ser = serial.Serial('COM4', 230400)
            ser.close()
            ser.open()

        # There is no ADS1299/Arduino connected to the Serial Port
        except:
            self.warning_serial()
            return  # the return 'stops' the current function

        # ------------------------------------------
        # BEGIN SAMPLING
        # Aviso = input("Enter an 'x' to begin sampling: ")
        # ser.write(bytes(Aviso, 'utf-8'))

        Aviso = bytes('x', 'utf-8')
        time.sleep(2)
        ser.write(Aviso)
        # ------------------------------------------


        # SKIP THE INITIAL INFO
        intro = ser.read(size=2269)  # For NORMAL ELECTRODE

        # Parameters
        global x_len
        x_len = 2000  # Number of points to display

        # y_range = [-3e-5, -1e-5]  # Range of possible Y values to display (INPUT SHORT TEST)

        # y_range = [-100e-3, 10e-3]  # Range of possible Y values to display (NORMAL ELECTRODE)
        y_range = [-100e-3, 100e-3]

        # Save Figure, Axis
        self.fig, self.ax = plt.subplots()

        # Limits for amplitude values (y values)
        self.ax.set_ylim(y_range)

        # Title and Labels for axes
        self.ax.set_title("LIVE Data from ADS1299: CH1")
        self.ax.set_ylabel("Amplitude [V]")
        self.ax.set_xlabel("Time [s]")


        global xs
        # xs = np.linspace(0, x_len, x_len)

        global time_window
        time_window = 1.3
        xs = np.linspace(0, time_window, x_len)

        global ys
        ys = [0] * x_len


        # Counter for storing drawing status
        self.counter = 0

        # Save the first drawn Line as well
        self.line, = self.ax.plot(xs, ys, '#bf5c22')

        # Clear previous widgets, before adding the graph
        self.box1.clear_widgets()

        # Adding a graph as a widget
        widget = FigureCanvasKivyAgg(self.fig)
        self.box1.add_widget(widget)

        # Set a timer to refresh the display every second
        # Clock.schedule_interval(self.update_view, 0.01)
        Clock.schedule_interval(self.update_view, 0.02)



    # Defining the desired Channel to plot
    global Canal1
    Canal1 = []


    def update_view(self, *args, **kwargs):

        import math

        # Canal1 = []

        # Reading data from ADS1299:

        # for x in range(0, math.ceil(fs / 20) - 1):
        for x in range(0, math.ceil(fs / 20) - 1):
            data = ser.readline()
            dataConverted = data.decode('UTF-8')

            measureNice = dataConverted.split(", ")
            measureNice.pop(0)
            # measureNice.pop(8)
            measureNice.pop()

            measureNice = np.array(measureNice)
            measureNice = measureNice.astype(float)

            # CONVERSION TO VOLTAGE
            measureNice = measureNice * 0.37 / ((2 ** 24) - 1)

            Canal1.append(measureNice[0])

        # LPF FILTER - METHOD 2
        outSignal = self.butter_lowpass_filter2(Canal1, cutoff, fs, order)

        ys.extend(outSignal)

        # Limit y list to set number of items
        ynew = ys[-x_len:]

        # Update data
        self.counter += time_window / 30  # Displacement

        # Create data with displaced values
        xnew = np.linspace(0 + self.counter,
                           time_window + self.counter,
                           x_len)


        # Set data to Line
        # self.line.set_ydata(ynew)
        self.line.set_data(xnew, ynew)

        # Adjusting the appearance of the graph
        self.ax.relim()
        self.ax.autoscale_view()

        # Redraw
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # -------------------------------------------
        # AUTO ADJUST Y-LIM OF THE WINDOW

        import datetime
        from datetime import datetime

        timeNew = datetime.now()
        timeNew = timeNew.strftime("%H:%M:%S.%f")

        minutesNew = float(timeNew[3:5])
        secNew = float(timeNew[6:15])

        self.calculate_sec(minutesOld, secOld, minutesNew, secNew, outSignal)
        # -------------------------------------------


    def stop(self):

        try:
            comFinish = 'z'
            ser.write(bytes(comFinish, 'utf-8'))
            ser.close()

            Clock.unschedule(self.update_view)

        except:
            self.warning_serial()
            return



# # Example Tab
# class Tab7(MDFloatLayout, MDTabsBase):
#
#     box = ObjectProperty(None)
#
#
#     def add_plot(self):
#
#         fig99 = plt.figure()
#
#         z1 = [0, 1, 2, 3, 4, 5]
#         z2 = [0, 10, 20, 30, 40, 50]
#
#         plt.plot(z1, z2)
#         #plt.suptitle('Example Plot')
#         plt.title('Example Plot')
#
#         self.fig10 = fig99
#
#         return self.fig10
#
#
#     def show_plot(self):
#
#         plt.close('all')
#         self.box.clear_widgets()
#
#         self.fig10 = Tab7.add_plot(self)
#         self.box.add_widget(FigureCanvasKivyAgg(self.fig10))



class mainApp(MDApp):

    def build(self):
        return Builder.load_file("styles_layouts.kv")


# Running app
mainApp().run()


