import tkinter as tk

root = tk.Tk()

root.wm_title('Welcome to iTeam')
root.minsize(500, 700)

def onClickAddCourse():
    root.destroy()


def onClickSearchLearners():
    root.destroy()


def onClickSearchCourse():
    root.destroy()


tk.Label(root, text='\nThis allow you to list your course\n(which allowes to be discovered by other learners)').grid(row=0)
button = tk.Button(root, text='Add Course', width=25, command=onClickAddCourse)
button.grid(row=1)

tk.Label(root, text='\nThis allow you to list your course\n(which allowes to be discovered by other learners)').grid(row=2)
button = tk.Button(root, text='Search Learners', width=25, command=onClickSearchLearners)
button.grid(row=3)

tk.Label(root, text='\nThis allow you to list your course\n(which allowes to be discovered by other learners)').grid(row=4)
button = tk.Button(root, text='Search Course', width=25, command=onClickSearchCourse)
button.grid(row=5)

root.mainloop()