from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Separator
from PIL import Image, ImageTk

import ollama
import threading
import queue

#TODO: Pretty up the code

"""
Function to get response using a prompt and queue for storing the response.

Parameters:
- prompt: the prompt to generate the response
- queue: the queue to store the response

Return type: None
"""
def get_response(prompt, queue):
    for chunk in ollama.generate (
        model = 'codellama:13b-instruct', prompt=prompt, stream=True,
        system = 'You are a computer science teacher. If asked about non-computer science related questions, you simply politely decline to answer.'
        ):
        queue.put(chunk['response'])

"""
Check the queue for incoming messages and display them in the feedback area.
"""
def check_queue():
    if not queue.empty():
        text = queue.get()
        feedback.configure(state='normal')
        feedback.insert('end', text)
        feedback.configure(state='disabled')
    root.after(100, check_queue)

# Create the thread and the queue, then begin the thread
running = True
queue = queue.Queue()
thread = threading.Thread(target=get_response, args=("Hello", queue,))
thread.start()

#create gui
root = Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title("")

#create font
font = Font(family="Helvetica",size=36,weight="bold")

#create heading @ top of GUI

#create frame to hold logo and heading for GUI
topframe = Frame(root)
topframe.columnconfigure(0, weight=1)
topframe.columnconfigure(1, weight=1)

#row zero, insert logo and heading
heading = Label(topframe, text="Script Sage", font=font, anchor='w', pady=15 )
heading.grid(row=0, column=1, sticky="we")

topframe.pack(fill="x")

#add a line separator
sep0 = Separator(root, orient='horizontal')
sep0.pack(fill="x", padx='30')

#create another frame for the rest of the GUI widgets
mainframe = Frame(root)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.pack(fill="x")

#row one, insert switch and space ---- this still needs to be worked on a lot
#switch:
switch = Label(mainframe, text="Switch between code & image here", font=('Helvetica', 18))
switch.grid(row=0, column=0, sticky="we", pady=(20,0))

#space:
advice = Label(mainframe, text="Advice from The Sage:", font=('Helvetica', 18))
advice.grid(row=0, column=1, sticky="we", padx=35, pady=(20,0))

#row two, insert upload image button and spot for ai feedback
#load image:
image = Image.open('duck.png')
image = ImageTk.PhotoImage(image)

#button with loaded image:
uploadImage = Button(mainframe, image=image, font=('Helvetica', 18))
uploadImage.grid(row=1, column=0, sticky="we", ipady=.23*root.winfo_screenheight(), padx=30, pady=(5,20)) 

#Text for ai feedback:
feedback = Text(mainframe, bg='lightblue', state='disabled')
feedback.grid(row=1, column=1, sticky="we", ipady=.135*root.winfo_screenheight(), padx=30, pady=(5,20))

#add a line separator
sep1 = Separator(root, orient='horizontal')
sep1.pack(fill="x", padx='30')

#what does this do????
root.after(100, check_queue())

#run GUI
root.mainloop()

thread.join()

# note for nate, will delete eventually:
# padx=(left,right)
# pady=(top,bottom)