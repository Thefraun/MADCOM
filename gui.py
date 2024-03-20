
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Notebook
from tkinter.ttk import Separator
from tkinter.ttk import Style
from tkinter import filedialog as fd
from PIL import Image, ImageTk
#from vision import read_image
import time

#import ollama
import threading
import queue

#TODO: Pretty up the code

def get_response(prompt_queue, queue):
    """
    Function to get response using a prompt and queue for storing the response.

    Parameters:
    - prompt: the prompt to generate the response
    - queue: the queue to store the response

    Return type: None
    """
    global running
    global is_resetting
    global response_over
    while running:
        if not prompt_queue.empty():
            for chunk in ollama.generate (
                model = 'codellama:13b-instruct', prompt=prompt_queue.get(), stream=True,
                system = '''You are a computer science tutor. You will be given sections of code, and you must analyse and give feedback based on the usage of best practices, and whether it functions as it reasonably should.
                            Your response should be no longer than 500 characters. If it would be beneficial, include examples of what the code would output if given an input. Be sure to stay solely on the topic of coomputer science. DO NOT INCLUDE FOXES OR ANY MENTION OF THEM.
                            Also, please do not start writing code that is not necessary for the benefit of the student. Any code written should be in the same language that the prompt was provided in. Be concise and specific with every given response. If the prompt does not contain code, explain that you are
                            designed to analyse code, and cannot answer prompts unrelated to computer science.
                            Thank you!''',
                ):
                    response_over = False
                    if is_resetting:
                        response_queue.queue.clear()
                        is_resetting = False
                        break
                    if running:
                        response_queue.put(chunk['response'])
                    else:
                        break
            response_over = True
            
def check_queue():
    """
    Check the queue for incoming messages and display them in the feedback area.
    """
    if not response_queue.empty() and not is_resetting:
        text = response_queue.get()
        feedback_text.configure(state='normal')
        feedback_text.insert('end', text)
        feedback_text.see('end')
        feedback_text.configure(state='disabled')
    root.after(100, check_queue)

def upload_file():
    """
    Asks the user to select a compatible file, and then opens the image and sends it to vision.py for processing
    """
    path = fd.askopenfilename(type=('*.jpg', '*.png', '*.jpeg'))
    if not path == '':
        image = Image.open(path)
        image = image.resize((550,600))
        image = ImageTk.PhotoImage(image)
        upload_image_button.configure(image=image)
        upload_image_button.image = image
        prompt = read_image(path)
        display_code_label.configure(text=prompt)
        prompt_queue.put(prompt)


# not sure how to document(?) these 
def reset():
    """
    Resets the program to allow for the insertion of another prompt
    """
    global is_resetting
    global image
    global response_over
    is_resetting = True
    feedback_text.configure(state='normal')
    feedback_text.delete('1.0', 'end')
    feedback_text.configure(state='disabled')
    upload_image_button.configure(image=image)
    upload_image_button.image = image
    display_code_label.configure(text='This is where we show the code')
    if response_over:
        is_resetting = False

def switch():
    """
    Toggle the program between light and dark mode
    """
    if mode_button.cget('text') == 'Light Mode':
         root.config(background=default_dark)
         top_frame.config(background=default_dark)
         space_label.config(background=default_dark, fg='#181A1B')
         heading_label.config(background=default_dark, fg='white')
         mode_button.configure(text='Dark Mode')
         mainframe.config(background=default_dark)
         left_frame.config(background=default_dark)
         style.theme_use('darkMode')
         right_frame.config(background=default_dark)
         advice_label.config(background=default_dark, fg='white')
    else:
         root.config(background=default_light)
         top_frame.config(background=default_light)
         space_label.config(background=default_light, fg='#EBEBEC')
         heading_label.config(background=default_light, fg='black')
         mode_button.configure(text='Light Mode')
         mainframe.config(background=default_light)
         left_frame.config(background=default_light)
         style.theme_use('lightMode')
         right_frame.config(background=default_light)
         advice_label.config(background=default_light, fg='black')

# Create the thread and the queue
# Inspired by user Furas
response_queue = queue.Queue()
prompt_queue = queue.Queue()
running = True
is_resetting = False
response_over = False
thread = threading.Thread(target=get_response, args=(prompt_queue, queue,))
thread.daemon = True
thread.start()

# Create GUI
root = Tk()

# Create in instance of ttk style
style = Style()

# Create different colors to be used
black = 'black'
grey = 'grey'
white = 'white' 
default_light = '#EBEBEC'
default_dark = '#181A1B'

# Create font for tabs
tab_font = Font(family='Futura', size=16)

# Create style for light mode for Notebook
style.theme_create( 'lightMode', settings ={
        'TNotebook': {
            'configure': {'tabmargins': [5, 5, 10, 5], 'background': default_light }},
        'TNotebook.Tab': {
            'configure': {'padding': [30, 10], 'borderwidth':[2], 'foreground': black, 'font': tab_font},
            'map':       {'background': [('selected', default_light), ('!active', default_light)],
                          'expand': [('selected', [5, 5, 5, 5])]}}})


# Create style for dark mode for Notebook
style.theme_create( 'darkMode', settings ={
         'TNotebook': {
            'configure': {'tabmargins': [5, 5, 10, 5],'background': default_dark }},
         'TNotebook.Tab': {
            'configure': {'padding': [30, 10], 'borderwidth':[2], 'foreground': white, 'font': tab_font},
            'map':       {'background': [('selected', default_dark), ('!active', default_dark), ('active', grey)],
                          'expand': [('selected', [5, 5, 5, 5])]}}})

# Use light mode style
style.theme_use('lightMode')

# Make GUI full screen
root.geometry('{0}x{1}+0+0'.format(root.winfo_screenwidth(), root.winfo_screenheight()))

# Remove default title from GUI
root.title('')

#create and add a frame for the widgets at the top of the GUI
top_frame = Frame(root)
top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=1)
top_frame.columnconfigure(2, weight=1)
top_frame.pack(fill='x')

#create and add a space to help keep the top widgets spaced out
space_label = Label(top_frame, text='Light Mode', font=('Arial', 16), fg=default_light)
space_label.grid(row=0, column=0, padx=(10,0))

# Create font for the heading
heading_font = Font(family='Helvetica', size=36, weight='bold')

# Create and add a heading @ top of GUI w/ application name
heading_label = Label(top_frame, text='Script Sage', font=heading_font, pady=15)
heading_label.grid(row=0, column=1)

# Create and add a button to switch between light and dark mode
mode_button = Button(top_frame, text='Light Mode',fg='white',  bg='blue', highlightbackground='blue', activebackground='blue', command=switch, font=('Arial', 16), cursor='hand2')
mode_button.grid(row=0, column=2, sticky='e', padx=(0,10))

# Create and add a line separator
top_seperator = Separator(root, orient='horizontal')
top_seperator.pack(fill='x', padx='30')

# Create and add another frame for the majority of the rest of the GUI widgets
mainframe = Frame(root)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.pack(fill='x')

# Create and add frame to hold widgets on the left side of the GUI
left_frame = Frame(mainframe)
left_frame.columnconfigure(0, weight=1)
left_frame.grid(row=0,column=0,pady=(0,10))

# Create and add a frame to hold widgets on the right side of the GUI
right_frame = Frame(mainframe)
right_frame.columnconfigure(0, weight=1)
right_frame.grid(row=0, column=1,pady=(0,10))

# Create/load 'Upload Image' image:
image = Image.open('uploadImage.png')
image = image.resize((550,600))
image = ImageTk.PhotoImage(image)

# Create and add tabbed section holding upload image button and label to display code from image
tab_control = Notebook(left_frame)

# Create tabs to switch between uploaded image and code from the image
tab1 = Frame(tab_control)
tab2 = Frame(tab_control)

# Add tabs to the Notebook
tab_control.add(tab1, text='Image')
tab_control.add(tab2, text='Code')
tab_control.grid(row=1,column=0, pady=(10,5))

# Create and add the upload image button to the Notebook
upload_image_button = Button(tab1, image=image, command=upload_file, cursor='hand2')
upload_image_button.grid(column = 0,  row = 0)  

# Create and add a label that diplays upload image's code to the Notebook
display_code_label = Label(tab2, text ='This is where your code from the image will appear.')
display_code_label.grid(column = 0, row = 0)

# Create and add a label to explain text area
advice_label = Label(right_frame, text='Advice from The Sage:', font=('Futura', 20))
advice_label.grid(row=0, column=0, sticky='we', pady =(10,10))

# Create font for ai feedback text
feedback_font = Font(family='Helvetica',size=18)

# Create and add a text area for ai feedback:
feedback_text = Text(right_frame, bg='lightgreen', state='disabled', font=feedback_font, width=10, height=10, wrap=WORD)
feedback_text.grid(row=1, column=0, ipadx=300, ipady=165)

# Create and add a button to reset image and feedback
reset_button = Button(left_frame, text='Reset', fg='white', bg='blue', highlightbackground='blue', activebackground='blue', command=reset, font=('Arial', 16), cursor='hand2')
reset_button.grid(row=2, column=0, sticky='w', padx=10, pady=5)

# Create and add a line separator
bottom_seperator = Separator(root, orient='horizontal')
bottom_seperator.pack(fill='x', padx='30')

# Begins checking the response queue every 100 milliseconds
root.after(100, check_queue())

# Run GUI
root.mainloop()

# End the program and the thread
running = False
thread.join(1000)
