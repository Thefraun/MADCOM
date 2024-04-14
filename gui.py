
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Notebook
from tkinter.ttk import Separator
from tkinter.ttk import Style
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from cloud_services import read_image, text_to_speech
from ai import AI
import time
import threading

#TODO: Add docstrings, documentation, pretty up?

# Defines the GUI class, containing the GUI and all functions associated
class GUI:
    def mode_toggle(self):
        """
        Toggle the program between light and dark mode
        """
        if self.mode_button.cget('text') == 'Light Mode':
            self.root.config(background=self.default_dark)
            self.top_frame.config(background=self.default_dark)
            self.space_label.config(background=self.default_dark, fg='#181A1B')
            self.heading_label.config(background=self.default_dark, fg='white')
            self.mode_button.configure(text='Dark Mode')
            self.mainframe.config(background=self.default_dark)
            self.left_frame.config(background=self.default_dark)
            self.style.theme_use('darkMode')
            self.right_frame.config(background=self.default_dark)
            self.advice_label.config(background=self.default_dark, fg='white')
            self.reset_button.config(bg='#0acd6f', highlightbackground='#0acd6f', activebackground='#0acd6f', fg='black')
            self.mode_button.config(bg='#0acd6f', highlightbackground='#0acd6f', activebackground='#0acd6f', fg='black')
            logo = Image.open('Images/ScriptSageDark.png')
            logo = ImageTk.PhotoImage(logo)
            self.heading_label.config(image=logo)
            self.heading_label.image = logo
        else:
            self.root.config(background=self.default_light)
            self.top_frame.config(background=self.default_light)
            self.space_label.config(background=self.default_light, fg='#EBEBEC')
            self.heading_label.config(background=self.default_light, fg='black')
            self.mode_button.configure(text='Light Mode')
            self.mainframe.config(background=self.default_light)
            self.left_frame.config(background=self.default_light)
            self.style.theme_use('lightMode')
            self.right_frame.config(background=self.default_light)
            self.advice_label.config(background=self.default_light, fg='black')
            self.reset_button.config(bg='#056939', highlightbackground='#056939', activebackground='#056939', fg='white')
            self.mode_button.config(bg='#056939', highlightbackground='#056939', activebackground='#056939', fg='white')
            logo = Image.open('Images/ScriptSage.png')
            logo = ImageTk.PhotoImage(logo)
            self.heading_label.config(image=logo)
            self.heading_label.image = logo
            
    def reset(self):
        """
        Resets the program to allow for the insertion of another prompt
        """
        ai.set_is_resetting(True)
        self.feedback_text.configure(state='normal')
        self.feedback_text.delete('1.0', 'end')
        self.feedback_text.configure(state='disabled')
        image = Image.open('Images/uploadImage.png')
        image = image.resize((550,600))
        image = ImageTk.PhotoImage(image)
        self.upload_image_button.configure(image=image)
        self.upload_image_button.image = image
        self.display_code_label.configure(text='This is where we show the code')
            
    def upload_file(self):
        """
        Asks the user to select a compatible file, and then opens the image and sends it to vision.py for processing
        """
        path = fd.askopenfilename(type=('*.jpg', '*.png', '*.jpeg'))
        if not path == '':
            self.root.config(cursor='wait')
            self.root.update()
            prompt_thread = threading.Thread(target=self.send_prompt, args=(path,), name='prompt_thread')
            prompt_thread.daemon = True
            prompt_thread.start()
            image = Image.open(path)
            image = image.resize((550,600))
            image = ImageTk.PhotoImage(image)
            self.upload_image_button.configure(image=image)
            self.upload_image_button.image = image
            self.root.config(cursor='arrow')
            self.root.update()
            
    def send_prompt(self, path):
        """
        Sends the prompt to vision.py for processing and displays the read prompt in the GUI
        """
        prompt = read_image(path)
        ai.set_prompt(prompt)
        self.display_code_label.configure(text=prompt)
        
    def read_aloud(self):
        text_to_speech_thread = threading.Thread(target=text_to_speech, args=('Hello',), name='text_to_speech_thread')
        text_to_speech_thread.daemon = True
        text_to_speech_thread.start()
        
    def recieve_advice(self):
        while True:
            chunk = ai.get_response_chunk()
            self.feedback_text.configure(state='normal')
            self.feedback_text.insert('end', chunk)
            self.feedback_text.see('end')
            self.feedback_text.configure(state='disabled')
            time.sleep(0.2)
            
    def __init__(self):
        
        # Create the main window
        self.root = Tk()

        # Create an instance of ttk style
        self.style = Style()

        # Create different colors to be used
        black = 'black'
        grey = 'grey'
        white = 'white' 
        self.default_light = '#EBEBEC'
        self.default_dark = '#181A1B'

        # Create font for tabs
        tab_font = Font(family='Futura', size=16)

        # Create style for light mode for Notebook
        self.style.theme_create( 'lightMode', settings ={
                'TNotebook': {
                    'configure': {'tabmargins': [5, 5, 10, 5], 'background': self.default_light }},
                'TNotebook.Tab': {
                    'configure': {'padding': [30, 10], 'borderwidth':[2], 'foreground': black, 'font': tab_font},
                    'map':       {'background': [('selected', self.default_light), ('!active', self.default_light)],
                                'expand': [('selected', [5, 5, 5, 5])]}}})


        # Create style for dark mode for Notebook
        self.style.theme_create( 'darkMode', settings ={
                'TNotebook': {
                    'configure': {'tabmargins': [5, 5, 10, 5],'background': self.default_dark }},
                'TNotebook.Tab': {
                    'configure': {'padding': [30, 10], 'borderwidth':[2], 'foreground': white, 'font': tab_font},
                    'map':       {'background': [('selected', self.default_dark), ('!active', self.default_dark), ('active', grey)],
                                'expand': [('selected', [5, 5, 5, 5])]}}})

        # Use light mode style
        self.style.theme_use('lightMode')

        # Make GUI full screen
        self.root.geometry('{0}x{1}+0+0'.format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))

        # Remove default title from GUI
        self.root.title('')

        #create and add a frame for the widgets at the top of the GUI
        self.top_frame = Frame(self.root)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.columnconfigure(2, weight=1)
        self.top_frame.pack(fill='x')

        #create and add a space to help keep the top widgets spaced out
        self.space_label = Label(self.top_frame, text='Light Mode', font=('Arial', 16), fg=self.default_light)
        self.space_label.grid(row=0, column=0, padx=(10,0))

        # Create font for the heading
        heading_font = Font(family='Helvetica', size=36, weight='bold')

        # Create and add a heading @ top of GUI w/ application name
        logo = Image.open('Images/ScriptSage.png')
        logo = ImageTk.PhotoImage(logo)
        self.heading_label = Label(self.top_frame, image=logo, font=heading_font, pady=15)
        self.heading_label.grid(row=0, column=1)

        # Create and add a button to switch between light and dark mode
        self.mode_button = Button(self.top_frame, text='Light Mode',fg='white', bg='#056939', highlightbackground='#056939', activebackground='#056939', command=self.mode_toggle, font=('Arial', 16), cursor='hand2')
        self.mode_button.grid(row=0, column=2, sticky='e', padx=(0,105), pady=(90,0))

        # Create and add a line separator
        self.top_seperator = Separator(self.root, orient='horizontal')
        self.top_seperator.pack(fill='x', padx='30')

        # Create and add another frame for the majority of the rest of the GUI widgets
        self.mainframe = Frame(self.root)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.pack(fill='x')

        # Create and add frame to hold widgets on the left side of the GUI
        self.left_frame = Frame(self.mainframe)
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.grid(row=0,column=0,pady=(0,10))

        # Create and add a frame to hold widgets on the right side of the
        self.right_frame = Frame(self.mainframe)
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.grid(row=0, column=1,pady=(0,45))

        # Create/load 'Upload Image' image:
        image = Image.open('Images/uploadImage.png')
        image = image.resize((550,600))
        image = ImageTk.PhotoImage(image)
        
        # Create and add tabbed section holding upload image button and label to display code from image
        self.tab_control = Notebook(self.left_frame)

        # Create tabs to switch between uploaded image and code from the image
        self.tab1 = Frame(self.tab_control)
        self.tab2 = Frame(self.tab_control)

        # Add tabs to the Notebook
        self.tab_control.add(self.tab1, text='Image')
        self.tab_control.add(self.tab2, text='Code')
        self.tab_control.grid(row=1,column=0, pady=(10,5))

        # Create and add the upload image button to the Notebook
        self.upload_image_button = Button(self.tab1, image=image, command=self.upload_file, cursor='hand2')
        self.upload_image_button.grid(column=0,  row=0)  

        # Create and add a label that diplays upload image's code to the Notebook
        self.display_code_label = Label(self.tab2, text ='This is where your code from the image will appear.', font=('Futura', 16), justify=LEFT)
        self.display_code_label.grid(column = 0, row = 0)

        # Create and add a label to explain text area
        self.advice_label = Label(self.right_frame, text='Advice from The Sage:', font=('Futura', 20))
        self.advice_label.grid(row=0, column=0, sticky='we', pady=(0,10))
        
        # Create a button that sits to the right of the advice label
        self.ask_question_button = Button(self.right_frame, text='Ask The Sage', font=('Futura', 18), command=self.read_aloud, cursor='hand2')
        self.ask_question_button.grid(row=0, column=0, sticky='e', pady=(0,10))

        # Create font for ai feedback text
        self.feedback_font = Font(family='Helvetica',size=18)

        # Create and add a text area for ai feedback:
        self.feedback_text = Text(self.right_frame, bg='lightgray', state='disabled', font=self.feedback_font, width=10, height=10, wrap=WORD)
        self.feedback_text.grid(row=1, column=0, ipadx=300, ipady=170)

        # Create and add a button to reset image and feedback
        self.reset_button = Button(self.left_frame, text='Reset', fg='white', bg='#056939', highlightbackground='#056939', activebackground='#056939', command=self.reset, font=('Arial', 16), cursor='hand2')
        self.reset_button.grid(row=2, column=0, sticky='w', pady=5)

        # Create and add a line separator
        self.bottom_seperator = Separator(self.root, orient='horizontal')
        self.bottom_seperator.pack(fill='x', padx='30')

        # Begins checking the response queue every 100 milliseconds
        
        recieve_advice_thread = threading.Thread(target=self.recieve_advice, name='recieve_advice_thread')
        recieve_advice_thread.daemon = True
        recieve_advice_thread.start()

        # Run GUI
        self.root.mainloop()
if __name__ == '__main__':
    ai = AI()
    gui = GUI()