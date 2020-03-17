from datetime import datetime, timedelta
import csv
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import matplotlib as mtp
import numpy as np

meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
             'noviembre', 'diciembre']
dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
path = 'C:\\Users\\usuario\\Desktop\\log\\'

date_first=datetime.now()-timedelta(1)
date_last=date_first+timedelta(5)

print(date_last, meses[date_first.month], dias[date_last.weekday()], type(date_last))


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

@timeit
def path_from_date(date):
    global meses
    global dias
    return str(date.year)+'\\'+meses[date.month-1]+'\\'+dias[date.weekday()]+' '+str(date.day)+'.csv'

def set_data_datalogger(data):
    fechas = mtp.dates.date2num([datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in (data.iloc[:,0]).values[:]]).reshape(-1,1)
    temperaturas=data.loc[:,'Temperatura'].values.reshape(-1,1)
    humedades=data.loc[:,'Humedad'].values.reshape(-1,1)
    print(humedades.shape)
    return fechas, temperaturas, humedades

def subplotting(xfmt, fechas, temperaturas, humedades):
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


@timeit
def retrieve_and_plot(first_date, last_date, path):

    xfmt = mtp.dates.DateFormatter('%Y-%m-%d %H:%M:%S')

    for i in range((last_date-first_date).days+1):
        date_path = path_from_date(first_date+timedelta(i))
        if os.path.exists(path + date_path):
            if i>0:
                ag_fe, ag_te, ag_hu = fechas[-1], temperaturas[-1], humedades[-1]
            fechas, temperaturas, humedades = set_data_datalogger(pd.read_csv(path + date_path))
            if i>0:
                fechas,temperaturas, humedades=np.vstack([ag_fe,fechas]),np.vstack([ag_te,temperaturas]),np.vstack([ag_hu,humedades])
            subplotting(xfmt, fechas, temperaturas, humedades)

        else:
            pass

    plt.show()


print((date_first.date()).weekday())
print(date_last.date())
print((date_last-date_first).days)
print((date_first+timedelta(5)).date()==date_last.date())

f=np.arange(0,150)
g=np.arange(151,200)


first_date=datetime.now()-timedelta(7)
last_date=datetime.now()

retrieve_and_plot(last_date,last_date,path)

data = pd.read_csv('C:\\Users\\usuario\\Desktop\\log\\2019\\septiembre\\lunes 23.csv')
f,t,h=set_data_datalogger(data)

print(f,t,h)


#plt.plot(f,np.sin(f),'o')
#plt.plot(g,np.exp(-g),'*')
#plt.show()


