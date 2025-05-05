from tkinter import *
from tkinter import ttk
import os
import customtkinter

root = Tk()
current_path = os.path.dirname(os.path.realpath(__file__))
image = PhotoImage(file=current_path + "\Images\spy.png")
width = 640
height = 360
x = (root.winfo_screenwidth()//2)-(width//2)
y = (root.winfo_screenheight()//2)-(height//2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
root.overrideredirect(True)

root.config(background = "#0F0F0F")

bg_label = Label(root, image = image, bg = "#0F0F0F")
bg_label.place(x = 0, y = 0)

progress_label = Label(root, text = "Loading...", font = ("cascadia code", 7, "bold"), fg = "#FFFFFF", bg = "#0F0F0F")
progress_label.place(x = 20, y = 320)

welcome_label = Label(text = "Social Spy", bg = "#0F0F0F", font = ("cascadia code", 17, "bold"), fg = "#FFFFFF")
welcome_label.place(x = 10, y = 0)

progress = ttk.Style()
progress.theme_use('clam')
progress.configure("red.Horizontal.TProgressbar", background = "#108cff")

progress = customtkinter.CTkProgressBar(root, height = 2, width = 600, progress_color = "#FFFFFF")
progress.place(x = 20, y = 340)

def top():
    root.withdraw()
    os.system("python Main.py")
    root.destroy()

i = 0

def load():
    global i
    if i <= 100:
        txt = 'Loading...' + (str(i) + '%')
        progress_label.config(text = txt)
        progress_label.after(17, load)
        progress.set(i/100)
        i += 1
    else:
        top()

load()

root.resizable(False, False)
root.mainloop()