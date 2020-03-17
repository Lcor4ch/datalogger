import serial
import time
import os
import pandas as pd
import random
import csv
from datetime import datetime, timedelta
import numpy as np

meses=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
dias = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo']


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
        os.mkdir(root_path + str(date_now.year))
        os.mkdir(root_path + str(date_now.year)+'\\'+meses[date_now.month-1])
        path_obj = root_path + str(date_now.year)+'\\'+meses[date_now.month-1]
    elif not date_pre.month == date_now.month:
        os.mkdir(root_path + str(date_now.year)+'\\'+meses[date_now.month-1])
        path_obj = root_path + str(date_now.year)+'\\'+meses[date_now.month-1]
    else:
        path_obj = current_path
    return path_obj

def coded_date(date):
    '''

    :param date: is a timeStamp
    :return: a numerical code for that date
    '''
    return 10000*date.year+100*date.month+date.day



def write_log(path, date_pre, date_now, to_print, dias):

    path1 = path + '\\' + dias[date_now.dayofweek] + ' ' + str(date_now.day) + '.csv'
    print(path1)
    header = ['Fecha', 'Temperatura', 'Humedad']
    with open(path1, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if not coded_date(date_pre) == coded_date(date_now):

            writer.writerow([g for g in header])

        writer.writerow([date_now, to_print[0], to_print[1]])

def gen_datetime(min_year=2000, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return (start + (end - start) * random.random()).replace(microsecond=0)



def crea_lista_dates(n):
    lista_dates = list([])
    for i in range(n):
        lista_dates.append(str(gen_datetime(min_year=2010, max_year=2010)))


    return lista_dates


def set_serial_data(serial_data):
    '''

    :param serial_data: es un string con dos valores separados por una coma
    :return: array conteniendo la data de serial_data, en float
    '''
    moj = serial_data.find(',')
    return np.array([float(serial_data[:moj]), float(serial_data[moj+1:])])



def datalogger_test(lista_dates):
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
             'noviembre', 'diciembre']
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    ser = serial.Serial("COM3", 9600, bytesize=8, parity=serial.PARITY_NONE, timeout=1)
    ser.flushInput()
    time.sleep(3)

    date_pre = pd.to_datetime('1/1/1900')
    path_log = 'C:\\Users\\usuario\\Desktop\\log\\'
    current_path = 'nada'
    i = 1
    for i in range(len(lista_dates)):

        b = ser.readline()
        string_n = b.decode("utf-8")  # decode byte string into Unicode
        date_now = lista_dates[i]
        to_print = set_serial_data(string_n.rstrip())
        current_path = path_by_date(path_log, current_path, date_pre, date_now, meses)
        write_log(current_path, date_pre, date_now, to_print, dias)
        date_pre = date_now
        time.sleep(3)


lista_dates = pd.to_datetime(crea_lista_dates(700), format='%Y-%m-%d %H:%M:%S').sort_values()
print(lista_dates[5].day,lista_dates[5].year,lista_dates[34].month)
datalogger_test(lista_dates)
