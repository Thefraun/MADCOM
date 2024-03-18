from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Notebook
from tkinter.ttk import Separator
from tkinter.ttk import Style
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from vision import read_image
import time

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
    global running
    global isResetting
    while running:
        if not prompt_queue.empty():
            for chunk in ollama.generate (
                model = 'codellama:13b-instruct', prompt=prompt_queue.get(), stream=True,
                system = '''You are Jeffrey Wile, a computer science teacher at Warwick high school. You are a nationally renowned teacher, 
                and your goal is to use the AP rubric to help your student improve their code. Some things to consider from the AP rubric are:
                Spelling and captilisation discrepancies are forgiven, so long as it is understandable.
                So long as the intention is clear, similar symbols can be switched. Missing semicolons can be forgiven if intention is clear. You really like foxes, so try to incorporate them into every response you give.'''
                ):
                    if isResetting:
                        response_queue.queue.clear()
                        isResetting = False
                        break
                    if running:
                        response_queue.put(chunk['response'])
                    else:
                        break

"""
Check the queue for incoming messages and display them in the feedback area.
"""
def check_queue():
    if not response_queue.empty() and not isResetting:
        text = response_queue.get()
        feedback_text.configure(state='normal')
        feedback_text.insert('end', text)
        feedback_text.see('end')
        feedback_text.configure(state='disabled')
    root.after(100, check_queue)

def upload_file():
    path = fd.askopenfilename(type=('*.jpg', '*.png', '*.jpeg'))
    if not path == '':
        feedback_text.configure(state='normal')
        feedback_text.delete('1.0', 'end')
        feedback_text.configure(state='disabled')
        image = Image.open(path)
        image = image.resize((200,200))
        image = ImageTk.PhotoImage(image)
        upload_image_button.configure(image=image)
        upload_image_button.image = image
        prompt = read_image(path)
        display_code_label.configure(text=prompt)
        prompt_queue.put(prompt)


# not sure how to document(?) these 
def reset():
    global isResetting
    global image
    isResetting = True
    feedback_text.configure(state='normal')
    feedback_text.delete('1.0', 'end')
    feedback_text.configure(state='disabled')
    upload_image_button.configure(image=image)
    upload_image_button.image = image
    display_code_label.configure(text='This is where we show the code')

def switch():
    if mode_button.cget('text') == "Light":
         root.config(background='#181A1B')
         heading.config(background='#181A1B', fg='white')
         mainframe.config(background='#181A1B')
         tab2.config(background='black')
         style.theme_use("darkMode")
         left_frame.config(background='#181A1B')
         right_frame.config(background='#181A1B')
         advice_label.config(background='#181A1B', fg='white')
         mode_button.configure(text="Dark")
    else:
         root.config(background='#EBEBEC')
         heading.config(background='#EBEBEC', fg='black')
         mainframe.config(background='#EBEBEC')
         left_frame.config(background='#EBEBEC')
         right_frame.config(background='#EBEBEC')
         style.theme_use("lightMode")
         advice_label.config(background='#EBEBEC', fg='black')
         mode_button.configure(text="Light")

# Create the thread and the queue
response_queue = queue.Queue()
prompt_queue = queue.Queue()
running = True
isResetting = False
thread = threading.Thread(target=get_response, args=(prompt_queue, queue,))
thread.daemon = True
thread.start()

#create GUI
root = Tk()

#create in instance of ttk style
style = Style()

#create different colors to be used
black = 'black'
grey = 'grey'
white = 'white' 
default_light = '#EBEBEC'
default_dark = '#181A1B'

#create style for light mode for Notebook
style.theme_create( "lightMode", settings ={
        "TNotebook": {
            "configure": {"tabmargins": [5, 5, 10, 5], "background": default_light }},
        "TNotebook.Tab": {
            "configure": {"padding": [30, 10], "borderwidth":[2], "foreground": black},
            "map":       {"background": [("selected", default_light), ('!active', default_light)],
                          "expand": [("selected", [5,5,5,5])]}}})

#create style for dark mode for Notebook
style.theme_create( "darkMode", settings ={
         "TNotebook": {
            "configure": {"tabmargins": [5, 5, 10, 5],"background": default_dark }},
         "TNotebook.Tab": {
            "configure": {"padding": [30, 10], "borderwidth":[2], "foreground": white},
            "map":       {"background": [("selected", default_dark), ('!active', default_dark), ('active', grey)],
                          "expand": [("selected", [5, 5, 5, 5])]}}})

#use light mode style
style.theme_use("lightMode")

#make GUI full screen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

#remove default title from GUI
root.title('')

#create font
font = Font(family='Helvetica',size=36,weight='bold')

#add a heading @ top of GUI w/ application name
heading = Label(root, text='Script Sage',  font=font, pady=15)
heading.pack(fill='x')

#add a line separator
top_seperator = Separator(root, orient='horizontal')
top_seperator.pack(fill='x', padx='30')

#create and add another frame for the majority of the rest of the GUI widgets
mainframe = Frame(root)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.pack(fill='x')

#create and add frame to hold widgets on the left side of the GUI
left_frame = Frame(mainframe)
left_frame.columnconfigure(0, weight=1)
left_frame.grid(row=0,column=0,pady=(0,10))

#create and add frame to hold widgets on the right side of the GUI
right_frame = Frame(mainframe)
right_frame.columnconfigure(0, weight=1)
right_frame.grid(row=0, column=1,pady=(0,10))

#load 'Upload Image' image:
image = Image.open('Images/uploadImage.png')
image = image.resize((200,200))
image = ImageTk.PhotoImage(image)

#create tabbed section holding upload image button and label to display code from image
tab_control = Notebook(left_frame)

#create tabs to switch between uploaded image and code from the image
tab1 = Frame(tab_control)
tab2 = Frame(tab_control)

#add tabs to the Notebook
tab_control.add(tab1, text='Image')
tab_control.add(tab2, text='Code') #, state='disabled'
tab_control.grid(row=1,column=0, pady=(10,5))

#add upload image button to the Notebook
upload_image_button = Button(tab1, image=image, command=upload_file, font=('Helvetica', 18), cursor='hand2')
upload_image_button.grid(column = 0,  row = 0, ipadx=.1*root.winfo_screenwidth(), ipady=.18*root.winfo_screenheight())  

#add label that diplays upload image's code to the Notebook
display_code_label = Label(tab2, text ='This is where we show the code')
display_code_label.grid(column = 0, row = 0, ipadx=.1*root.winfo_screenwidth(), ipady=.18*root.winfo_screenheight()) #ipady=image.height()+50

#add label to explain text area:
advice_label = Label(right_frame, text='Advice from The Sage:', font=('Helvetica', 18))
advice_label.grid(row=0, column=0, sticky='we', pady =(10,10))

#create font for ai feedback text
feedback_font = Font(family='Helvetica',size=18)

#add text area for ai feedback:
feedback_text = Text(right_frame, bg='lightgreen', state='disabled', font=feedback_font, width=int(.4*root.winfo_screenwidth()/24), height = 10, wrap=WORD)
feedback_text.grid(row=1, column=0, ipadx=.08*root.winfo_screenwidth(),  ipady=.135*root.winfo_screenheight(), padx=20)

#add button to reset image and feedback
reset_button = Button(left_frame, text='Reset', fg='white', bg='blue', highlightbackground='blue', activebackground='blue', command=reset, font=('Arial', 16), cursor='hand2')
reset_button.grid(row=2, column=0, sticky='w', padx=10, pady=5)

#add button to switch between light and dark mode
mode_button = Button(right_frame, text='Light',fg='white',  bg='blue', highlightbackground='blue', activebackground='blue', command=switch, font=('Arial', 16), cursor='hand2')
mode_button.grid(row=2, column=0, sticky='w', padx=10, pady=5)

#add a line separator
bottom_seperator = Separator(root, orient='horizontal')
bottom_seperator.pack(fill="x", padx='30')

#what does this do????
root.after(100, check_queue())

#run GUI
root.mainloop()

running = False
thread.join(1000)