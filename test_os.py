import os
import numpy as np
import random
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mtp
import queue
def gen_datetime(min_year=2000, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

def plot_datalogger_data(data):
    '''

    :param data: es un df que contiene en las primera columna fechas en formato string, y las demás columnas son los resultados de mediciones hechas en las respectivas fechas
    :return: nada
    '''
    dates = mtp.dates.date2num([datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in (data_tot.iloc[:,0]).values[:]])
    fig, (ax1, ax2) = plt.subplots(2,1)

    xfmt = mtp.dates.DateFormatter('%Y-%m-%d %H:%M:%S')



    plt.subplot(2,1,1)
    plt.subplots_adjust(bottom=0.1, hspace=0.7)
    plt.xticks(rotation=25)
    ax1 = plt.gca()
    ax1.xaxis.set_major_formatter(xfmt)
    plt.plot(dates, data.iloc[:,1].values)
    plt.subplot(2,1,2)
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(rotation=25)
    ax2 = plt.gca()
    ax2.xaxis.set_major_formatter(xfmt)
    plt.plot(dates, data.iloc[:,2].values)
    plt.show()

queue=queue.Queue()

def retrieve_data(first_date, last_date):

    return 0



print(os.path.exists('C:\\Users\\usuario\\Desktop\\log\\2019\\septiembre\\jueves 12.csv'))

data = pd.read_csv('C:\\Users\\usuario\\Desktop\\log\\2019\\septiembre\\lunes 23.csv')
data2 = pd.read_csv('C:\\Users\\usuario\\Desktop\\log\\2019\\septiembre\\martes 24.csv')

print(list(data))
data_tot = pd.concat([data, data2], axis=0)
plot_datalogger_data(data_tot)
lista = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in (data_tot.iloc[:,0]).values[:]]
print(type(lista[54]))
dates = mtp.dates.date2num(lista)

plt.subplots_adjust(bottom=0.1)
plt.xticks(rotation=25)
ax=plt.gca()
xfmt = mtp.dates.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.plot(dates,data_tot.loc[:,'Humedad'].values)
plt.show()
