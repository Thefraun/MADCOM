from tkinter import *

root = Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(background='black')

root.title("Script Sage")
# frame1 = Frame(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightbackground="black", highlightthickness=5, bd= 0)
# frame1.pack()

heading = Label(root, text="Script Sage", font=('Arial', 18), bg="grey" )
heading.pack()

mainframe = Frame(root)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)

switch = Label(mainframe, text="Switch between code & image here", font=('Arial', 18))
switch.grid(row=0, column=0, sticky="we", pady=20)
uploadImage = Label(mainframe, text="Upload Image Here", font=('Arial', 18))
uploadImage.grid(row=1, column=0, sticky="we", pady=300)

space = Label(mainframe, text="", font=('Arial', 18))
space.grid(row=0, column=1, sticky="we")
feedback = Label(mainframe, text="Receive your feedback here", font=('Arial', 18))
feedback.grid(row=1, column=1, sticky="we")

mainframe.pack(fill="x")

root.mainloop()
