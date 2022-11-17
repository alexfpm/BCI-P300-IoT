
#ANIMATED PLOT WITH KIVY (WORKING!)



from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import numpy as np
import matplotlib.pyplot as plt

from kivy.properties import ObjectProperty



Builder.load_file("SPI_front_end.kv")



class GraphView(BoxLayout):
    """Widget for displaying Matplotlib graphs"""
    
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
    
        #Same minutes
        if minO == minN:
            
            #Adjust window every 5 seconds
            if secN > secO + 5:
                
                meanY = sum(data)/len(data)
                
        
                #y_rangeNew = [meanY-1e-3, meanY+1e-3]
                y_rangeNew = [meanY-3e-3, meanY+3e-3]
                
                self.ax.set_ylim(y_rangeNew)
                
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
                
                self.ax.set_ylim(y_rangeNew)
                
                minO = minN
                secO = secN
                
                
                return minO, secO 
    
    
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    
    def start(self):
        
        import serial
        
        
        global ser
        ser = serial.Serial('COM4', 230400)
        ser.close()
        ser.open()
        
        # ------------------------------------------
        # BEGIN SAMPLING
        Aviso = input("Enter an 'x' to begin sampling: ")
        ser.write(bytes(Aviso,'utf-8'))
        # ------------------------------------------
        
        
        # SKIP THE INITIAL INFO
        intro = ser.read(size=2269)  # For NORMAL ELECTRODE
        
        # Parameters
        global x_len
        x_len = 2000  # Number of points to display

        # y_range = [-3e-5, -1e-5]  # Range of possible Y values to display (INPUT SHORT TEST)

        #y_range = [-100e-3, 10e-3]  # Range of possible Y values to display (NORMAL ELECTRODE)
        y_range = [-100e-3, 100e-3]
        
        
        # Save Figure, Axis
        self.fig, self.ax = plt.subplots()
        
        self.ax.set_ylim(y_range)
        
        
        global xs
        xs = np.linspace(0, x_len, x_len)
        
        global ys
        ys = [0] * x_len
        
  
        
        # Data used for initialization
        #x = np.linspace(-5, 5, x_len)
        #y = np.random.rand(x_len)
        
        # Counter for storing drawing status
        self.counter = 0
        
        # Save the first drawn Line as well
        self.line, = self.ax.plot(xs, ys, '#bf5c22')
        
        
        #Clear previous widgets, before adding the graph
        self.box1.clear_widgets()
        
        # Adding a graph as a widget
        widget = FigureCanvasKivyAgg(self.fig)
        self.box1.add_widget(widget)
        

        # Set a timer to refresh the display every second
        #Clock.schedule_interval(self.update_view, 0.01)
        Clock.schedule_interval(self.update_view, 0.02)
        
    
    #Defining the desired Channel to plot
    global Canal1
    Canal1 = []
    
    
    def update_view(self, *args, **kwargs):
        
        import math
        
        #Canal1 = []
        
        
        #Reading data from ADS1299:

        #for x in range(0, math.ceil(fs / 20) - 1):
        for x in range(0, math.ceil(fs / 20) - 1):
            
            data = ser.readline()
            dataConverted = data.decode('UTF-8')

            measureNice = dataConverted.split(", ")
            measureNice.pop(0)
            #measureNice.pop(8)
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
        self.counter += x_len / 30  # Displacement
        
        # Create data with displaced values
        xnew = np.linspace(0 + self.counter,
                           x_len + self.counter,
                           x_len)
        
        #y = np.random.rand(x_len)
        
        
        # Set data to Line
        #self.line.set_ydata(ynew)
        self.line.set_data(xnew, ynew)
        
        # Adjusting the appearance of the graph
        self.ax.relim()
        self.ax.autoscale_view()
        
        # Redraw
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
        
        #-------------------------------------------
        #AUTO ADJUST Y-LIM OF THE WINDOW
        
        import datetime
        from datetime import datetime
        
        timeNew = datetime.now()
        timeNew = timeNew.strftime("%H:%M:%S.%f")
        
        minutesNew = float(timeNew[3:5])
        secNew = float(timeNew[6:15])
        
        
        self.calculate_sec(minutesOld, secOld, minutesNew, secNew, outSignal)
        #-------------------------------------------
        
        
    
    
    def stop(self):
        
        comFinish = 'z'
        ser.write(bytes(comFinish, 'utf-8'))
        ser.close()
        
        Clock.unschedule(self.update_view)
        


class RootWidget(BoxLayout):
    """Prepare a widget for adding children"""


class GraphApp(App):
    """Applications that display Matplotlib graphs"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Matplotlib graph on Kivy'

    def build(self):
        return RootWidget()


def main():
    # Start the application
    app = GraphApp()
    app.run()


if __name__ == '__main__':
    main()