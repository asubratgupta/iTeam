import tkinter as tk
import time
from tkinter import messagebox

root = tk.Tk()

root.wm_title('Sign Up')
root.minsize(500, 700)

tk.Label(root, text='Full Name').grid(row=0)
tk.Label(root, text='Email').grid(row=1)
tk.Label(root, text='Password').grid(row=2)
e1 = tk.Entry(root)
e2 = tk.Entry(root)
e3 = tk.Entry(root)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

# Location Drop Down
# Create a Tkinter variable
tkvar = tk.StringVar(root)

# Dictionary with options
choices = ['India','US','UK','Other']
tkvar.set('India') # set the default option

popupMenu = tk.OptionMenu(root, tkvar, *choices)
tk.Label(root, text="Choose Location").grid(row = 3, column = 0)
popupMenu.grid(row = 3, column =1)

def change_dropdown(*args):
   return tkvar.get()

# link function to change dropdown
tkvar.trace('w', change_dropdown)

# Interests CheckBox
tk.Label(root, text='Choose Interests').grid(row=4, column=0)
var1 = tk.IntVar()
tk.Checkbutton(root, text='male', variable=var1).grid(row=4, column=1, sticky=tk.W)
var2 = tk.IntVar()
tk.Checkbutton(root, text='female', variable=var2).grid(row=5, column=1, sticky=tk.W)


full_name, email, password, location, interests = '', '', '', '', dict()
def update(*args):
   global full_name, email, password, location, interests
   full_name, email, password, location, interests = e1.get(), e2.get(), e3.get(), change_dropdown(), {'male': var1.get(), 'female':var2.get()}

button = tk.Button(root, text='Submit', width=25, command=update)
button.grid(row=10, column=1)

def print_val():
   print(full_name, email, password, location, interests)
button = tk.Button(root, text='Print me', width=25, command=print_val)
button.grid(row=11, column=1)

root.mainloop()