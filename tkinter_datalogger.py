from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import queue
import threading
import serial
import numpy as np
import csv
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mtp
from pandas.plotting import register_matplotlib_converters
mtp.use("TkAgg")
from datetime import datetime, timedelta, date
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

register_matplotlib_converters()

s = serial.Serial('COM3', 9600)

meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
             'noviembre', 'diciembre']
dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

date_pre = datetime.now()-timedelta(1)
path_log = 'C:\\Users\\usuario\\Desktop\\log\\'
current_path = 'nada'


def date_string():
    ff = time.localtime(time.time())
    string = str(ff.tm_year)+'/'+str(ff.tm_mon)+'/'+str(ff.tm_mday)+ ' '+str(ff.tm_hour)+':'+str(ff.tm_min)+':'+str(ff.tm_sec)
    return pd.to_datetime(string)

def path_by_date(root_path, current_path, date_pre, date_now, meses):
    '''

    :param root_path: direccion adonde irán a parar los datos y carpetas que se crearán
    :param date_pre: fecha de la medición anterior (es un timeStamp)
    :param date_now: fecha de la medición actual (también es un timeStamp)
    :return: dirección completa donde irá a parar el próximo dato
    '''
    if not date_pre.year == date_now.year:
        if not os.path.exists(root_path + str(date_now.year)):
            os.mkdir(root_path + str(date_now.year))
            os.mkdir(root_path + str(date_now.year)+'\\'+meses[date_now.month-1])
        path_obj = root_path + str(date_now.year)+'\\'+meses[date_now.month-1]
    elif not date_pre.month == date_now.month:
        if not os.path.exists(root_path + str(date_now.year)+'\\'+meses[date_now.month-1]):
            os.mkdir(root_path + str(date_now.year)+'\\'+meses[date_now.month-1])
        path_obj = root_path + str(date_now.year)+'\\'+meses[date_now.month-1]
    else:
        path_obj = root_path + str(date_now.year)+'\\'+meses[date_now.month-1]
    return path_obj

def coded_date(date):
    '''

    :param date: is a timeStamp
    :return: a numerical code for that date
    '''
    return 10000*date.year+100*date.month+date.day



def write_log(path, date_pre, date_now, to_print, dias):

    path1 = path + '\\' + dias[date_now.dayofweek] + ' ' + str(date_now.day) + '.csv'
    header = ['Fecha', 'Temperatura', 'Humedad']
    if not os.path.exists(path1):
        with open(path1, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([g for g in header])
            writer.writerow([date_now, to_print[0], to_print[1]])
    else:
        with open(path1, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([date_now, to_print[0], to_print[1]])


def set_serial_data(serial_data):
    '''

    :param serial_data: es un string con dos valores separados por una coma
    :return: array conteniendo la data de serial_data, en float
    '''
    moj = serial_data.find(',')

    return np.array([float(serial_data[:moj]), float(serial_data[moj+1:])])


class calendario():
    def __init__(self, root, mini=date(year=2019,month=9,day=11)):
        self.top = Toplevel(root)
        self.cal = Calendar(self.top, font=('Times New Roman', 14), selectmode='day',
                             mindate=mini,
                             maxdate=date.today()-timedelta(1), cursor='arrow')
        self.cal.pack(padx=7, pady=11)
        ttk.Button(self.top, text='ok',command=self.get_sel).pack()
        self.date = ''

        self.top.grab_set()

    def get_sel(self):
        self.date = self.cal.selection_get()


        self.top.destroy()

    def format_date(self):
        return str(self.date.day)+'\\'+str(self.date.month)+'\\'+str(self.date.year)


def path_from_date(date):
    global meses
    global dias
    return str(date.year)+'\\'+meses[date.month-1]+'\\'+dias[date.weekday()]+' '+str(date.day)+'.csv'

def set_data_datalogger(data):
    fechas2 = list((data.iloc[:,0]).values[:])

    fechas = mtp.dates.date2num([datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in fechas2]).reshape(-1,1)
    #fechas = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in (data.iloc[:,0]).values[:]]

    temperaturas=data.loc[:,'Temperatura'].values.reshape(-1,1)
    humedades=data.loc[:,'Humedad'].values.reshape(-1,1)

    return fechas, temperaturas, humedades, fechas2

def subplotting(fechas, temperaturas, humedades):
    xfmt = mtp.dates.DateFormatter('%Y-%m-%d %H:%M:%S')

    plt.subplot(2, 1, 1)
    plt.subplots_adjust(bottom=0.1, hspace=0.7)
    plt.xticks(rotation=25)
    ax1 = plt.gca()
    ax1.xaxis.set_major_formatter(xfmt)
    plt.plot(fechas, temperaturas,'b')
    plt.subplot(2, 1, 2)
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=25)
    ax2 = plt.gca()
    ax2.xaxis.set_major_formatter(xfmt)
    plt.plot(fechas, humedades,'b')
    plt.show()




def retrieve_data(first_date, last_date, path):


    count = 0
    F, T, H = np.array([1]), np.array([1]), np.array([1])
    for i in range((last_date-first_date).days+1):

        date_path = path_from_date(first_date+timedelta(i))
        if os.path.exists(path + date_path):
            if i > 0:
                ag_fe, ag_te, ag_hu = fechas[-1], temperaturas[-1], humedades[-1]
            fechas, temperaturas, humedades = set_data_datalogger(pd.read_csv(path + date_path))

            if i > 0:
                fechas,temperaturas, humedades = np.vstack([ag_fe, fechas]), np.vstack([ag_te, temperaturas]), np.vstack([ag_hu,humedades])
            #subplotting(xfmt, fechas, temperaturas, humedades)
            F, T, H = np.vstack((F, fechas)), np.vstack((T, temperaturas)), np.vstack((H, humedades))
        else:
            count = count+1
            pass
    F, T, H = F[1:,:], T[1:,:], H[1:,:]

    #subplotting(F,T,H)

    return np.hstack((F, T, H))

def retrieve_data2(first_date, last_date, path):


    count = 0
    F, T, H, F2 = np.array([1]), np.array([1]), np.array([1]), []
    for i in range((last_date-first_date).days+1):

        date_path = path_from_date(first_date+timedelta(i))
        if os.path.exists(path + date_path):

            fechas, temperaturas, humedades, fechas2 = set_data_datalogger(pd.read_csv(path + date_path))


            #subplotting(xfmt, fechas, temperaturas, humedades)
            F, T, H, F2 = np.vstack((F, fechas)), np.vstack((T, temperaturas)), np.vstack((H, humedades)), F2+fechas2
        else:
            count = count+1
            pass


    #subplotting(F,T,H)

    return np.hstack((F, T, H)), F2

class SerialThread(threading.Thread):
    def __init__(self, queue, i):
        threading.Thread.__init__(self)
        self.queue = queue
        self.i = i
        self.text = ''
    def run(self):
        global s
        t_start = time.perf_counter()
        while True:
            if s.inWaiting():
                #print(s.readline(s.inWaiting()).decode("utf-8"))

                text = set_serial_data(s.readline(s.inWaiting()).decode("utf-8"))

                self.i = self.i + time.perf_counter()-t_start
                self.queue.put(text)
                t_start = time.perf_counter()
            else:
                pass


class App():

    def __init__(self):
        self.root = Tk()
        style_temp = ttk.Style()
        style_hum = ttk.Style()
        style_comun = ttk.Style()
        style_boton = ttk.Style()
        self.root.title('Datalogger')
        style_temp.configure("T.TLabel", font=('Impact', 62), foreground='white', background='black')
        style_hum.configure("H.TLabel", font=('Impact', 62), foreground='white', background='black')
        style_comun.configure("Common.TLabel", font=('Times New Roman', 15), foreground='black')
        style_boton.configure("boton.TLabel", font=('Arial', 18), foreground='red', background='black', relief=RIDGE)

        content = ttk.Frame(self.root, padding="12 12 12 12")
        self.root.pack_propagate(0)
        self.root.frame_temp = ttk.Label(content, text='--' + 'ºC', style="T.TLabel", width=5)
        self.root.frame_hum = ttk.Label(content, text='--' + '%', style="H.TLabel", width=5)

        self.root.cal_from = ttk.Button(content, text='from', width=12,command=self.first_date)
        self.root.cal_to = ttk.Button(content, text='to', width=12, command=self.last_date)
        self.root.label_from = ttk.Label(content, text='', style="Common.TLabel")
        self.root.label_to = ttk.Label(content, text='', style="Common.TLabel")
        self.root.label_blank = ttk.Label(content, text='', style="Common.TLabel")
        self.root.label_temp = ttk.Label(content, text='Temperatura', style="Common.TLabel")
        self.root.label_hum = ttk.Label(content, text='Humedad', style="Common.TLabel")
        self.root.label_blank2 = ttk.Label(content, text='', style="Common.TLabel")
        self.root.boton_plot = ttk.Button(content, text='PLOT', style="boton.TLabel", command=self.plot_action)
        self.root.boton_plot['state'] = 'disabled'
        content.grid(column=0, row=0)
        self.root.frame_temp.grid(column=0, row=0, columnspan=2, rowspan=3, sticky=W)
        self.root.frame_hum.grid(column=3, row=0, columnspan=2, rowspan=3, sticky=W)
        self.root.label_temp.grid(column=0, row=4, columnspan=2, sticky=S)
        self.root.label_hum.grid(column=3, row=4, columnspan=2, sticky=S)
        self.root.label_blank.grid(column=2, row=0, sticky=S)
        self.root.label_blank2.grid(column=0, row=5, sticky=S)
        self.root.label_from.grid(column=1, row=6, sticky=[E])
        self.root.label_to.grid(column=1, row=7, sticky=E)
        self.root.cal_from.grid(column=0, row=6, sticky=S)
        self.root.cal_to.grid(column=0, row=7, sticky=[S])
        self.root.boton_plot.grid(column=4, row=6, rowspan=2)

        self.init_date = ''
        self.fin_date = ''
        self.i = 0
        self.o = 0
        self.path = 'C:\\Users\\usuario\\Desktop\\log\\'
        self.queue = queue.Queue()
        self.thread = SerialThread(self.queue, self.i)
        self.thread.start()
        self.process_serial()
        self.write_csv()



    def first_date(self):
        cal = calendario(self.root)
        self.root.wait_window(cal.top)
        self.init_date = cal.date
        if self.init_date != '' and self.fin_date != '':
            self.root.boton_plot['state'] = 'normal'
        self.root.label_from.configure(text=cal.format_date())


    def last_date(self):
        cal = calendario(self.root, mini=self.init_date)
        self.root.wait_window(cal.top)
        self.fin_date = cal.date
        if self.init_date != '' and self.fin_date != '':
            self.root.boton_plot['state'] = 'normal'
        self.root.label_to.configure(text=cal.format_date())

    def plot_action(self):
        #if self.inti_date!='' and self.fin_date!='':


        data, f2 = retrieve_data2(self.init_date, self.fin_date, self.path)

        xfmt = mtp.dates.DateFormatter('%Y-%m-%d %H:%M:%S')
        fig = Figure(figsize=(10,8))
        newWindow = Toplevel(self.root)

        ax1 = fig.add_subplot(211)
        #ax2 = fig.add_subplot(122)

        lis = [f2[i] for i in np.arange(1,len(f2),120*((self.fin_date-self.init_date).days)+1)]

        ax1.set_xticks([data[i,0] for i in np.arange(1,len(f2),120*((self.fin_date-self.init_date).days)+1)])
        ax1.set_xticklabels(lis, rotation=75)
        ax1.xaxis.set_major_formatter(xfmt)

        #ax2.set_xticklabels(data[1:, 0], rotation=45)
        canvas = FigureCanvasTkAgg(fig, master=newWindow)

        ax1.set_title('Temperatura y Humedad')
        #ax2.set_title('Humedad')

        ax1.plot(data[1:,0],data[1:,1],'b',data[1:,0],data[1:,2],'r')

        #self.l2 = ax2.plot(data[1:,0],data[1:,2])
        toolbar = NavigationToolbar2Tk(canvas, newWindow)
        toolbar.update()
        #self.ax1.xticks(rotation=25)
        #self.ax2.xticks(rotation=25)
        canvas.draw()
        canvas.get_tk_widget().pack()
        newWindow.wait_window()

        self.reset_plot_command()





    def reset_plot_command(self):
       self.root.label_to.configure(text='')
       self.root.label_from.configure(text='')
       self.init_date, self.fin_date = '', ''
       self.root.boton_plot['state'] = 'disabled'


    def process_serial(self):

        while self.queue.qsize():
            try:

                v = self.queue.get()
                self.text = v
                self.root.frame_temp.configure(text=str(v[0])+'ºC')
                self.root.frame_hum.configure(text=str(v[1])+'%')

            except queue.Empty:
                pass

        self.root.after(100, self.process_serial)

    def write_csv(self):
        date_pre = datetime.now() - timedelta(1)
        current_path = 'nada'

        while self.thread.i > 30:
        #while self.queue.qsize():
            try:
                #if np.floor(self.counter.peek())>30:
                    #v = self.queue.get()
                    date_now = pd.to_datetime(time.strftime('%Y-%m-%d %H:%M:%S'))
                    current_path = path_by_date(self.path, current_path, date_pre, date_now, meses)
                    write_log(current_path, date_pre, date_now, self.text, dias)
                    date_pre = date_now

                    self.thread.i = 0
                 #   self.counter.reset()
                #else:
                 #   pass
            except self.queue.Empty:

                pass

        self.root.after(100, self.write_csv)



app = App()
app.root.mainloop()






