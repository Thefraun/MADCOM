import tkinter as tk
from tkinter import filedialog as fd

def callback():
    name = fd.askopenfilename()
    print(name)
tk.Button(text = 'file upload', command = callback).pack()
tk.mainloop()