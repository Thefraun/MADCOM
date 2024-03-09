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
    while True:
        try:
            for chunk in ollama.generate (
                model = 'codellama:13b-instruct', prompt=prompt_queue.get(), stream=True,
                system = '''You are Jeffrey Wile, a computer science teacher at Warwick high school. You are a nationally renowned teacher, 
                and your goal is to use the AP rubric to help your student improve their code. Some things to consider from the AP rubric are:
                Spelling and captilisation discrepancies are forgiven, so long as it is understandable.
                So long as the intention is clear, similar symbols can be switched. Missing semicolons can be forgiven if intention is clear. You really like foxes, so try to incorporate them into every response you give.'''
                ):
                 response_queue.put(chunk['response'])
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

def upload_file():
    path = fd.askopenfilename(type=('*.jpg', '*.png', '*.jpeg'))
    image = Image.open(path)
    image = image.resize((100,100))
    image = ImageTk.PhotoImage(image)
    uploadImage.configure(image=image)
    uploadImage.image = image
    prompt = read_image(path)
    prompt_queue.put(prompt)
    tabControl.config(tab1, state='enabled') # idk if this works, should allow to switch to label after image is uploaded

# not sure how to document(?) these 
def reset():
    feedback.configure(state='normal')
    feedback.delete('1.0', 'end')
    feedback.configure(state='disabled')

def switch():
    if modeButton.cget('text') == "Light":
         root.config(background='#181A1B')
         heading.config(background='#181A1B', fg='white')
         mainframe.config(background='#181A1B')
         style.theme_use("darkMode")
         leftFrame.config(background='#181A1B')
         rightFrame.config(background='#181A1B')
         adviceLabel.config(background='#181A1B', fg='white')
         modeButton.configure(text="Dark")
    else:
         root.config(background='#EBEBEC')
         heading.config(background='#EBEBEC', fg='black')
         mainframe.config(background='#EBEBEC')
         leftFrame.config(background='#EBEBEC')
         rightFrame.config(background='#EBEBEC')
         style.theme_use("lightMode")
         adviceLabel.config(background='#EBEBEC', fg='black')
         modeButton.configure(text="Light")
   
# Create the thread and the queue
response_queue = queue.Queue()
prompt_queue = queue.Queue()
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
defaultLight = '#EBEBEC'
defaultDark = '#181A1B'

#create style for light mode for Notebook
style.theme_create( "lightMode", settings ={
        "TNotebook": {
            "configure": {"tabmargins": [5, 5, 10, 5], "background": defaultLight }},
        "TNotebook.Tab": {
            "configure": {"padding": [30, 10], "borderwidth":[2], "foreground": black},
            "map":       {"background": [("selected", defaultLight), ('!active', defaultLight)],
                          "expand": [("selected", [0,0,0,0])]}}})

#use light mode style
style.theme_use("lightMode")

#create style for dark mode for Notebook
style.theme_create( "darkMode", settings ={
         "TNotebook": {
            "configure": {"tabmargins": [5, 5, 10, 5],"background": defaultDark }},
         "TNotebook.Tab": {
            "configure": {"padding": [30, 10], "borderwidth":[2], "foreground": white},
            "map":       {"background": [("selected", defaultDark), ('!active', defaultDark), ('active', grey)],
                          "expand": [("selected", [1, 1, 1, 1])]}}})

#make GUI full screen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

#remove title from GUI
root.title('')

#create font
font = Font(family='Helvetica',size=36,weight='bold')

#add a heading @ top of GUI w/ application name
heading = Label(root, text='Script Sage',  font=font, pady=15)
heading.pack(fill='x')

#add a line separator
sep0 = Separator(root, orient='horizontal')
sep0.pack(fill='x', padx='30')

#create and add another frame for the majority of the rest of the GUI widgets
mainframe = Frame(root)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.pack(fill='x')

#create and add frame to hold widgets on the left side of the GUI
leftFrame = Frame(mainframe)
leftFrame.columnconfigure(0, weight=1)
leftFrame.grid(row=0,column=0,pady=(0,10))

#create and add frame to hold widgets on the right side of the GUI
rightFrame = Frame(mainframe)
rightFrame.columnconfigure(0, weight=1)
rightFrame.grid(row=0, column=1,pady=(0,10))

#load 'Upload Image' image:
image = Image.open('uploadImage.png')
image = image.resize((200,200))
image = ImageTk.PhotoImage(image)

#create tabbed section holding upload image button and label to display code from image
tabControl = Notebook(leftFrame)

#create tabs to switch between uploaded image and code from the image
tab1 = Frame(tabControl)
tab2 = Frame(tabControl)

#add tabs to the Notebook
tabControl.add(tab1, text='Image')
tabControl.add(tab2, text='Code') #, state='disabled'
tabControl.grid(row=1,column=0, pady=0)

#add upload image button to the Notebook
uploadImage = Button(tab1, image=image, command=upload_file, font=('Helvetica', 18), cursor='hand2').grid(column = 0,  row = 0, ipadx=.1*root.winfo_screenwidth(), ipady=.18*root.winfo_screenheight())  

#add label that diplays upload image's code to the Notebook
displayImageCode = Label(tab2,  text ='This is where we show the code').grid(column = 0, row = 0, ipadx=.1*root.winfo_screenwidth(), ipady=.18*root.winfo_screenheight(),) 

#add label to explain text area:
adviceLabel = Label(rightFrame, text='Advice from The Sage:', font=('Helvetica', 18))
adviceLabel.grid(row=0, column=0, sticky='we', pady =(10,10))

#create font for ai feedback text
feedbackFont = Font(family='Helvetica',size=24)

#add text area for ai feedback:
feedback = Text(rightFrame, bg='lightgreen', state='disabled', font=feedbackFont, width=int(.4*root.winfo_screenwidth()/24), height = 10, wrap=WORD)
feedback.grid(row=1, column=0, ipadx=.08*root.winfo_screenwidth(),  ipady=.135*root.winfo_screenheight(), padx=20)

#add button to reset image and feedback
reset = Button(leftFrame, text='Reset', fg='white', bg='blue', highlightbackground='blue', activebackground='blue', command=reset, font=('Arial', 16), cursor='hand2')
reset.grid(row=2, column=0, sticky='w', padx=10, pady=5)

#add button to switch between light and dark mode
modeButton = Button(rightFrame, text='Light',fg='white',  bg='blue', highlightbackground='blue', activebackground='blue', command=switch, font=('Arial', 16), cursor='hand2')
modeButton.grid(row=2, column=0, sticky='w', padx=10, pady=5)

#add a line separator
sep1 = Separator(root, orient='horizontal')
sep1.pack(fill="x", padx='30')

#what does this do????
root.after(100, check_queue())

#run GUI
root.mainloop()

thread.join()
