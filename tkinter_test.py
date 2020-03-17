from tkinter import *
from tkinter import ttk


# creating a function called say_hi()

counter = 0


def counter_label(label):
    def count():
        global counter
        counter += 1
        label.config(text=str(counter))
        label.after(100, count)

    count()

def func1():
    root = tk.Tk()
    root.title("Counting Seconds")
    label = tk.Label(root, fg="green")
    label.pack()
    counter_label(label)
    button = tk.Button(root, text='Stop', width=25, command=quit)
    button.pack()
    root.mainloop()

def write_slogan():
        print("Tkinter is easy to use!")

def func2():
    root = Tk()
    frame = Frame(root)
    frame.pack()

    button = Button(frame,
                       text="QUIT",
                       fg="red",
                       command=root.destroy)
    button.pack(side=LEFT)
    slogan = Button(frame,
                       text="Hello",
                       command=write_slogan)
    slogan.pack(side=LEFT)

    root.mainloop()

def lol(l):
    l.configure(text='so?')
    l.pack()


def func3():
    root = Tk()
    frame = ttk.Frame(root)
    frame.pack()
    l = ttk.Label(frame, text="...")
    l.pack()
    button1 = ttk.Button(frame, text="QUIT", command=root.destroy)
    button1.pack(side=LEFT)
    button2 = ttk.Button(frame, text=" NOT QUIT", command=lol(l))
    button2.pack(side=RIGHT)
    root.mainloop()
func3()