#!/usr/bin/python3
from tkinter import *
window = Tk()
window.title('test')
window.geometry('420x300')

lbl = Label(window, text='- moje soubory jsou dobre zorganizovane\n- moje soubory maji mene nez 200GB')
lbl.grid(column=0, row=0)
txt = Entry(window)
txt.grid(column=3, row=0)

def clicked():
    lbl.configure(text='or maybe nut')

btn = Button(window, text='change my mind', command=clicked)
btn.grid(column=0, row=1)
window.mainloop()
