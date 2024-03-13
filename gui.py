from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Separator
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from vision import read_image
import time

import ollama
import threading
import queue

#TODO: Pretty up the code

def get_response(prompt_queue, queue):
    """
    Function to get response using a prompt and queue for storing the response.

    Parameters:
    - prompt_queue: the queue to store the prompt
    - queue: the queue to store the chunks of the response
    """
    while running:
        try:
            for chunk in ollama.generate (
                model = 'codellama:13b-instruct', prompt=prompt_queue.get(), stream=True,
                system = '''You are Jeffrey Wile, a computer science teacher at Warwick high school. You are a nationally renowned teacher, 
                and your goal is to use the AP rubric to help your student improve their code. Some things to consider from the AP rubric are:
                Spelling and captilisation discrepancies are forgiven, so long as it is understandable.
                So long as the intention is clear, similar symbols can be switched. Missing semicolons can be forgiven if intention is clear. You really like foxes, so try to incorporate them into every response you give.'''
                ):
                if running:
                    response_queue.put(chunk['response'])
                else:
                    break
        except queue.Empty:
            pass

def check_queue():
    """
    Check the queue for incoming messages and display them in the feedback area.
    """
    if not response_queue.empty():
        text = response_queue.get()
        feedback.configure(state='normal')
        feedback.insert('end', text)
        feedback.configure(state='disabled')
    root.after(100, check_queue)

def upload_file():
    '''
    Upload the image file to read and set the uploaded image as the image displayed on the button
    '''
    path = fd.askopenfilename(type=('*.jpg', '*.png', '*.jpeg'))
    if not path == '':
        image = Image.open(path)
        image = image.resize((200, 200))
        image = ImageTk.PhotoImage(image)
        upload_image.configure(image=image)
        upload_image.image = image
        prompt = read_image(path)
        prompt_queue.put(prompt)


# not sure how to document(?) these 
def reset():
    '''
    Reset the response and revert changes to the upload image button
    '''
    feedback.configure(state='normal')
    feedback.delete('1.0', 'end')
    feedback.configure(state='disabled')
    image = Image.open('Images/uploadImage.png')
    image = image.resize((200,200))
    image = ImageTk.PhotoImage(image)
    upload_image.configure(image=image)
    upload_image.image = image

def switch():
    '''
    Toggle the program between light mode and dark mode
    '''
    if mode_button.cget('text') == "Light":
         root.config(background='black')
         topframe.config(background='black')
         heading.config(background='black', fg='white')
         mainframe.config(background='black')
         switch_spot.config(background='black', fg='white')
         advice.config(background='black', fg='white')
         mode_button.configure(text="Dark")
    else:
         root.config(background='white')
         topframe.config(background='white')
         heading.config(background='white', fg='black')
         mainframe.config(background='white')
         switch_spot.config(background='white', fg='black')
         advice.config(background='white', fg='black')
         mode_button.configure(text="Light")
   
# Create the thread and the queue
response_queue = queue.Queue()
prompt_queue = queue.Queue()
thread = threading.Thread(target=get_response, args=(prompt_queue, queue,))
thread.daemon = True
thread.start()
running = True

#create gui
root = Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title("")

#create font
font = Font(family='Helvetica',size=36,weight='bold')

#create frame to hold logo and heading for GUI
topframe = Frame(root)
topframe.columnconfigure(0, weight=1)
topframe.columnconfigure(1, weight=1)

#row zero, insert logo, heading, button to change background theme
heading = Label(topframe, text='Script Sage',  font=font, pady=15)
heading.grid(row=0, column=0, padx=(525,0))

mode_button = Button(topframe, text='Light',fg='white',  bg='blue', highlightbackground='blue', activebackground='blue', command=switch, cursor='hand2')
mode_button.grid(row=0, column=1, padx=(300,0))

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
switch_spot = Label(mainframe, text='Switch between code & image here', font=('Helvetica', 18))
switch_spot.grid(row=0, column=0, sticky='we', pady=(20,0))

#space:
advice = Label(mainframe, text='Advice from The Sage:', font=('Helvetica', 18))
advice.grid(row=0, column=1, sticky='we', padx=35, pady=(20,0))

#row two, insert upload image button and spot for ai feedback
#load image:
image = Image.open('Images/uploadImage.png')
image = image.resize((200,200))
image = ImageTk.PhotoImage(image)

#button with loaded image:
upload_image = Button(mainframe, image=image, command=upload_file, font=('Helvetica', 18), cursor='hand2')
upload_image.grid(row=1, column=0, ipadx=.1*root.winfo_screenwidth(), ipady=.18*root.winfo_screenheight(), padx=30, pady=(8,0))

#Text for ai feedback:
feedback_font = Font(family='Helvetica', size=16)

feedback = Text(mainframe, bg='lightgreen', state='disabled', font=feedback_font, width=int(.4*root.winfo_screenwidth()/24), height = 10, wrap=WORD)
feedback.grid(row=1, column=1, ipadx=.08*root.winfo_screenwidth(),  ipady=.135*root.winfo_screenheight(), padx=30, pady=(8,0))

#add button to reset image and feedback
reset = Button(mainframe, text='Reset', fg='white', bg='blue', highlightbackground='blue', activebackground='blue', command=reset, font=('Arial', 16), cursor='hand2')
reset.grid(row=2, column=0, padx=(400,0), pady=(0,20), ipady=10)

#add a line separator
sep1 = Separator(root, orient='horizontal')
sep1.pack(fill="x", padx='30')

#what does this do????
root.after(100, check_queue())

#run GUI
root.mainloop()
running = False
# note for nate, will delete eventually:
# padx=(left,right)
# pady=(top,bottom)
