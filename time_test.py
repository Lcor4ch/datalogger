import time
import pandas as pd
import os
import numpy as np
ff = time.localtime(time.time())
lista=['16/4/2016','15/7/2016','14/8/2017','25/5/2018','26/4/2018','17/1/2019','23/1/2015','24/9/2019','23/4/2019','16/12/2017','3/4/2016','4/5/2021']

lista_ff = pd.to_datetime(lista)
lista_ff = lista_ff.sort_values()
root_path = 'C:\\Users\\usuario\\Desktop\\log\\'


print(lista_ff[5].day,lista_ff[5].month,lista_ff[5].year)
meses=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
dias = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo']
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

def coded_date(date):
    '''

    :param date: is a timeStamp
    :return: a numerical code for that date
    '''
    return 10000*date.year+100*date.month+date.day

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

print(coded_date(date_string()))
print(str(date_string())[11:])
print(str(pd.to_datetime('1/1/12 10:10:10'))[11:])
print(pd.to_datetime('15/2/0'))



string = '19.00, 15.23'
mojon = string.find(',')

print((float(string[:mojon])))
print((float(string[mojon+1:])))

print((time.time()))