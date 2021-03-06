from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

__author__ = 'Dania'
import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
class mclass:
    def __init__(self,  window):
        self.box = Entry(window)
        self.button = Button (window, text="check", command=self.plot)
        self.box.pack ()
        self.button.pack()

    def plot (self):
        x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
            19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])

        plt.scatter(v,x,color='red')
        plt.plot(p, range(2 +max(x)),color='blue')
        plt.gca().invert_yaxis()

        plt.suptitle ("Estimation Grid", fontsize=16)
        plt.ylabel("Y", fontsize=14)
        plt.xlabel("X", fontsize=14)
        plt.show()
        plt.gcf().canvas.draw()
        fig = plt.figure()
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().grid(row=1,column=24)
        canvas.draw()

window= Tk()
start= mclass(window)
window.mainloop()
