from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import queue
import threading
import serial
import numpy as np

def set_serial_data(serial_data):
    '''

    :param serial_data: es un string con dos valores separados por una coma
    :return: array conteniendo la data de serial_data, en float
    '''
    moj = serial_data.find(',')

    return np.array([float(serial_data[:moj]), float(serial_data[moj+1:])])

class SerialThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        s = serial.Serial('COM3',9600)
        while True:
            if s.inWaiting():
                text = set_serial_data(s.readline(s.inWaiting()).decode("utf-8"))
                self.queue.put(text)

class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        style_temp = ttk.Style()
        style_hum = ttk.Style()
        style_comun = ttk.Style()
        style_boton = ttk.Style()

        style_temp.configure("T.TLabel", font=('Impact', 62), foreground='yellow', background='green')
        style_hum.configure("H.TLabel", font=('Impact', 62), foreground='blue', background='gray')
        style_comun.configure("Common.TLabel", font=('Times New Roman', 15), foreground='black')
        style_boton.configure("boton.TLabel", font=('Arial', 18), foreground='red', background='black', relief=RIDGE)

        content = ttk.Frame(self, padding="12 12 12 12")
        self.frame_temp = ttk.Label(content, text='14' + 'ºC', style="T.TLabel")
        self.frame_hum = ttk.Label(content, text='17' + '%', style="H.TLabel")

        self.cal_from = DateEntry(content, width=12, background='darkblue',
                             foreground='white', borderwidth=2, year=2007)
        self.cal_to = DateEntry(content, width=12, background='darkblue',
                           foreground='white', borderwidth=2, year=2019)
        self.label_from = ttk.Label(content, text='desde: ', style="Common.TLabel")
        self.label_to = ttk.Label(content, text='hasta: ', style="Common.TLabel")
        self.label_blank = ttk.Label(content, text='', style="Common.TLabel")
        self.label_temp = ttk.Label(content, text='Temperatura', style="Common.TLabel")
        self.label_hum = ttk.Label(content, text='Humedad', style="Common.TLabel")
        self.label_blank2 = ttk.Label(content, text='', style="Common.TLabel")
        self.boton_plot = ttk.Button(content, text='PLOT', style="boton.TLabel", command=self.destroy)

        content.grid(column=0, row=0)
        self.frame_temp.grid(column=0, row=0, columnspan=2, rowspan=3, sticky=W)
        self.frame_hum.grid(column=3, row=0, columnspan=2, rowspan=3, sticky=W)
        self.label_temp.grid(column=0, row=4, columnspan=2, sticky=S)
        self.label_hum.grid(column=3, row=4, columnspan=2, sticky=S)
        self.label_blank.grid(column=2, row=0, sticky=S)
        self.label_blank2.grid(column=0, row=5, sticky=S)
        self.label_from.grid(column=0, row=6, sticky=[W])
        self.label_to.grid(column=0, row=7, sticky=W)
        self.cal_from.grid(column=1, row=6, sticky=S)
        self.cal_to.grid(column=1, row=7, sticky=[S])
        self.boton_plot.grid(column=4, row=6, rowspan=2)

        self.queue = queue.Queue()
        thread = SerialThread(self.queue)
        thread.start()
        self.process_serial()

    def process_serial(self):
        while self.queue.qsize():
            try:
                v = self.queue.get()
                self.label_temp.configure(text=str(v[0])+'ºC')
                self.label_hum.configure(text=str(v[1])+'%')
            except queue.Empty:
                pass
        self.after(100, self.process_serial)

root = Tk()
root.title("datalogger")

style_temp = ttk.Style()
style_hum = ttk.Style()
style_comun = ttk.Style()
style_boton = ttk.Style()

style_temp.configure("T.TLabel", font=('Impact',62),foreground='yellow',background='green')
style_hum.configure("H.TLabel", font=('Impact',62), foreground='blue', background='gray')
style_comun.configure("Common.TLabel", font=('Times New Roman', 15), foreground='black')
style_boton.configure("boton.TLabel",font=('Arial',18),foreground='red', background='black', relief=RIDGE)
content = ttk.Frame(root, padding="12 12 12 12")



frame_temp = ttk.Label(content, text='14'+'ºC', style="T.TLabel")
frame_hum = ttk.Label(content, text='17'+'%', style="H.TLabel")

cal_from = DateEntry(content, width=12, background='darkblue',
                foreground='white', borderwidth=2, year=2007)
cal_to = DateEntry(content, width=12, background='darkblue',
                foreground='white', borderwidth=2, year=2019)
label_from = ttk.Label(content, text='desde: ', style="Common.TLabel")
label_to = ttk.Label(content, text='hasta: ', style="Common.TLabel")
label_blank = ttk.Label(content, text='', style="Common.TLabel")
label_temp = ttk.Label(content, text='Temperatura', style="Common.TLabel")
label_hum = ttk.Label(content, text='Humedad', style="Common.TLabel")
label_blank2 = ttk.Label(content, text='', style="Common.TLabel")
boton_plot = ttk.Button(content,text='PLOT',style="boton.TLabel", command=root.destroy)


content.grid(column=0, row=0)
frame_temp.grid(column=0,row=0, columnspan=2, rowspan=3, sticky=W)
frame_hum.grid(column=3, row=0, columnspan=2, rowspan=3, sticky=W)
label_temp.grid(column=0,row=4,columnspan=2,sticky=S)
label_hum.grid(column=3,row=4,columnspan=2,sticky=S)
label_blank.grid(column=2, row=0,sticky=S)
label_blank2.grid(column=0, row=5,sticky=S)
label_from.grid(column=0, row=6,sticky=[W])
label_to.grid(column=0, row=7,sticky=W)
cal_from.grid(column=1, row=6,sticky=S)
cal_to.grid(column=1, row=7,sticky=[S])
boton_plot.grid(column=4, row=6, rowspan=2)
root.mainloop()