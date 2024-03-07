from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Separator
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from vision import read_image
from tkmacosx import Button

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
def get_response(prompt_queue, queue):
    running = True
    while running:
        try:
            for chunk in ollama.generate (
                model = 'codellama:13b-instruct', prompt=prompt_queue.get(), stream=True,
                system = 'You are a computer science teacher.'
                ):
                if(running):
                    response_queue.put(chunk['response'])
                else:
                    break
            running = False
        except queue.Empty:
            pass

"""
Check the queue for incoming messages and display them in the feedback area.
"""
def check_queue():
    if not response_queue.empty():
        text = response_queue.get()
        feedback.configure(state='normal')
        feedback.insert('end', text)
        feedback.configure(state='disabled')
    root.after(100, check_queue)

def upload_file(thread):
    path = fd.askopenfilename(type=('*.jpg', '*.png', '*.jpeg'))
    prompt_queue.put(read_image(path))


# not sure how to document(?) this 
def reset():
    feedback.delete('1.0', END)
    
    
# Create the thread and the queue
response_queue = queue.Queue()
prompt_queue = queue.Queue()
running = True
thread = threading.Thread(target=get_response, args=(prompt_queue, queue,))
thread.start()

#create gui
root = Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title("")

#create font
font = Font(family='Helvetica',size=36,weight='bold')

#create heading @ top of GUI

#create frame to hold logo and heading for GUI
topframe = Frame(root)
topframe.columnconfigure(0, weight=1)
topframe.columnconfigure(1, weight=1)

#row zero, insert logo and heading
heading = Label(topframe, text='Script Sage', font=font, anchor='w', pady=15 )
heading.grid(row=0, column=1, sticky='we')

topframe.pack(fill='x')

#add a line separator
sep0 = Separator(root, orient='horizontal')
sep0.pack(fill='x', padx='30')

#create another frame for the rest of the GUI widgets
mainframe = Frame(root)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.pack(fill='x')

#row one, insert switch and space ---- this still needs to be worked on a lot
#switch:
switch = Label(mainframe, text='Switch between code & image here', font=('Helvetica', 18))
switch.grid(row=0, column=0, sticky='we', pady=(20,0))

#space:
advice = Label(mainframe, text='Advice from The Sage:', font=('Helvetica', 18))
advice.grid(row=0, column=1, sticky='we', padx=35, pady=(20,0))

#row two, insert upload image button and spot for ai feedback
#load image:
image = Image.open('uploadImage.png')
image = image.resize((200,200))
image = ImageTk.PhotoImage(image)

#button with loaded image:
uploadImage = Button(mainframe, image=image, command=lambda: upload_file(thread = thread), font=('Helvetica', 18))
uploadImage.grid(row=1, column=0, ipadx=.1*root.winfo_screenwidth(), ipady=.18*root.winfo_screenheight(), padx=30, pady=(5,0))
#Text for ai feedback:

feedbackFont = Font(family='Helvetica',size=24)

feedback = Text(mainframe, bg='lightgreen', state='disabled', font=feedbackFont, width=int(.4*root.winfo_screenwidth()/24), height = 10)
feedback.grid(row=1, column=1, ipadx=.08*root.winfo_screenwidth(),  ipady=.135*root.winfo_screenheight(), padx=30, pady=(5,0))
#add button to reset image and feedback
reset = Button(mainframe, text='Reset', fg='white', bg='blue', highlightbackground='blue', activebackground='blue', command=reset)
reset.grid(row=2, column=0, padx=(400,0), pady=(0,20))

#add a line separator
sep1 = Separator(root, orient='horizontal')
sep1.pack(fill="x", padx='30')

#what does this do????
root.after(100, check_queue())

#run GUI
root.mainloop()

running = False
thread.join()


# note for nate, will delete eventually:
# padx=(left,right)
# pady=(top,bottom)
