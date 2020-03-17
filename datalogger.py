import serial
import time
import os
import pandas as pd
import csv
import numpy as np
from datetime import datetime, timedelta
#ser = serial.Serial("COM3", 9600,bytesize=8,parity=serial.PARITY_NONE,timeout=1)
#ser.flushInput()
#time.sleep(3)

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
        if not os.path.exists(root_path + str(date_now.year)):
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



def datalogger():
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
             'noviembre', 'diciembre']
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    ser = serial.Serial("COM3", 9600, bytesize=8, parity=serial.PARITY_NONE, timeout=1)
    ser.flushInput()
    time.sleep(3)
    date_pre = pd.to_datetime('1/1/1900')
    path_log = 'C:\\Users\\usuario\\Desktop\\log\\'
    current_path='nada'
    i = 1
    time.sleep(3)
    while i == 1:
        b = ser.readline()

        string_n = b.decode("utf-8")  # decode byte string into Unicode
        if not len(string_n) == 0:
            date_now = pd.to_datetime(time.strftime('%Y-%m-%d %H:%M:%S'))


            to_print = set_serial_data(string_n.rstrip())

            current_path = path_by_date(path_log, current_path, date_pre, date_now, meses)
            write_log(current_path, date_pre, date_now, to_print, dias)
            date_pre = date_now
        else:
            print('tu vieja')
        #time.sleep(3)

def datalogger2():
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
             'noviembre', 'diciembre']
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    ser = serial.Serial("COM3", 9600, bytesize=8, parity=serial.PARITY_NONE, timeout=1)


    date_pre = datetime.now()-timedelta(1)
    path_log = 'C:\\Users\\usuario\\Desktop\\log\\'
    current_path='nada'
    i = 1
    while i == 1:
        ser.flushInput()

        time.sleep(15)
        t1 = time.time()
        b = ser.readline()
        string_n = b.decode("utf-8")  # decode byte string into Unicode
        date_now = pd.to_datetime(time.strftime('%Y-%m-%d %H:%M:%S'))
        to_print = set_serial_data(string_n.rstrip())

        current_path = path_by_date(path_log, current_path, date_pre, date_now, meses)
        write_log(current_path, date_pre, date_now, to_print, dias)
        date_pre = date_now


        time.sleep(15-(time.time() - t1))




datalogger2()
path_log = 'C:\\Users\\usuario\\Desktop\\log'

header = ['fecha', 'Temperatura', 'Humedad']

data =[]# empty list to store the data
i = 1
#while i==1:



current_path = 'nada'
date_pre = pd.to_datetime('1/1/1900')


for i in range(100):
    b = ser.readline()
    print(b)
    # read a byte string
    string_n = b.decode("utf-8")  # decode byte string into Unicode
    string = string_n.rstrip() # remove \n and \r
            # convert string to float
    date_now = pd.to_datetime(time.strftime())
    str_time = date_string()
    to_print = set_serial_data(string_n.rstrip())
    current_path = path_by_date(path_log, current_path, date_pre, date_now, meses)
    write_log(current_path, date_pre, date_now, to_print, dias)
    date_pre = date_now
    time.sleep(3)           # wait (sleep) 0.1 seconds

ser.close()
for line in data:
    print(line)