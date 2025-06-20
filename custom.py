# Custom is a program for editing game setting
# Custom це програма для зміни налаштуваннь гри
import tkinter
from settings import RES

window = tkinter.Tk("Custom")
window.geometry("450x800")

def save():
    pass

res_input = tkinter.Entry(window, )
savebutton = tkinter.Button(window, command=None)

res_input.pack()
savebutton.place(760, 225)

window.mainloop()