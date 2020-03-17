import tkinter as tk
from tkinter import ttk

from tkcalendar import Calendar


class Example1():
    def __init__(self, root):
        self.top = tk.Toplevel(root)

        self.cal = Calendar(self.top, font="Arial 14", selectmode='day',
                            cursor="hand1", year=2018, month=2, day=5)
        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.top, text="ok", command=self.print_sel).pack()
        ttk.Button(self.top, text="exit", command=self.quit1).pack()

        self.date = ''

        self.top.grab_set()

    def print_sel(self):
        self.date = self.cal.selection_get()

    def quit1(self):
        self.top.destroy()


class App():
    def __init__(self):
        self.root = tk.Tk()
        s = ttk.Style(self.root)
        s.theme_use('clam')

        ttk.Button(self.root, text='Last Date', command=self.last).pack(padx=10, pady=10)
        ttk.Button(self.root, text='Next Date', command=self.next).pack(padx=10, pady=10)

        self.last_date = ''
        self.next_date = ''

        self.root.mainloop()

    def last(self):
        cal = Example1(self.root)
        self.root.wait_window(cal.top)
        self.last_date = cal.date

    def next(self):
        cal = Example1(self.root)
        self.root.wait_window(cal.top)
        self.next_date = cal.date


app = App()
print('Last date: {}'.format(app.last_date))
print('Next date: {}'.format(app.next_date))