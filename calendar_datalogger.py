from tkcalendar import Calendar, DateEntry

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from datetime import datetime, timedelta
import pandas as pd






def open_calendar():
    def print_sel():
        print(cal.selection_get())
        cal.see(datetime(year=2016, month=2, day=5))


    global button1
    button1.config(state='disabled')
    top = tk.Toplevel(root)
    maxdate= pd.to_datetime(datetime.strftime(datetime.now()-timedelta(1), '%d-%m-%Y'))
    cal = Calendar(top = top, font="Arial 14", selectmode='day', locale='es_ES',
                   mindate=pd.to_datetime('15-09-2019'), maxdate=maxdate, disabledforeground='red',
                   cursor="arrow")
    cal.pack(padx=10,pady=10,fill='both', expand=True)
    ttk.Button(cal, text="ok", command=print_sel).pack()

root = tk.Tk()
button1 = tk.Button(root, text='Seleccionar fecha', command=open_calendar, state='normal')
button1.pack()





root.mainloop()