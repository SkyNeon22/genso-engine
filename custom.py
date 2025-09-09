# Custom is a program for editing game setting
import tkinter
import pymsgbox
from configs.config import RES

window = tkinter.Tk(className="Custom")
window.geometry("320x480")

def save():
    window.quit()

def cancel():
    window.quit()

savebutton = tkinter.Button(window,
                            command=save,
                            text="Save config")

cancelbutton = tkinter.Button(window,
                            command=quit,
                            text="Cancel")

savebutton.place(x=244, y=450)
cancelbutton.place(x=190, y=450)

window.mainloop()