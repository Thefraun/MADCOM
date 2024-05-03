
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

#TODO: Make the thing work, especially code label

# Defines the GUI class, containing the GUI and all functions associated
class GUI:
    def mode_toggle(self):
        """
        Toggle the program between light and dark mode
        """
        if self.mode_button.cget('text') == 'Dark Mode':
            # Sets all widgets to dark mode
            self.root.config(background=self.default_dark)
            self.top_frame.config(background=self.default_dark)
            self.space_label.config(background=self.default_dark, fg='#181A1B')
            self.heading_label.config(background=self.default_dark, fg='white')
            self.mode_button.configure(text='Light Mode')
            self.mainframe.config(background=self.default_dark)
            self.left_frame.config(background=self.default_dark)
            self.style.theme_use('darkMode')
            self.right_frame.config(background=self.default_dark)
            self.advice_label.config(background=self.default_dark, fg='white')
            self.reset_button.config(bg='#0acd6f', fg='black', highlightbackground='#0acd6f', activebackground='#0acd6f')
            self.mode_button.config(bg='#0acd6f', fg='black', highlightbackground='#0acd6f', activebackground='#0acd6f')
            self.edit_code_button.config(bg='#0acd6f', fg='black', highlightbackground='#0acd6f', activebackground='#0acd6f')
            logo = Image.open('Images/ScriptSageDark.png')
            logo = ImageTk.PhotoImage(logo)
            self.heading_label.config(image=logo)
            self.heading_label.image = logo
        else:
            # Sets all widgets to light mode
            self.root.config(background=self.default_light)
            self.top_frame.config(background=self.default_light)
            self.space_label.config(background=self.default_light, fg='#EBEBEC')
            self.heading_label.config(background=self.default_light, fg='black')
            self.mode_button.configure(text='Dark Mode')
            self.mainframe.config(background=self.default_light)
            self.left_frame.config(background=self.default_light)
            self.style.theme_use('lightMode')
            self.right_frame.config(background=self.default_light)
            self.advice_label.config(background=self.default_light, fg='black')
            self.reset_button.config(bg='#056939', highlightbackground='#056939', activebackground='#056939', fg='white')
            self.mode_button.config(bg='#056939', highlightbackground='#056939', activebackground='#056939', fg='white')
            self.edit_code_button.config(bg='#056939', fg='white', highlightbackground='#056939', activebackground='#056939')
            logo = Image.open('Images/ScriptSage.png')
            logo = ImageTk.PhotoImage(logo)
            self.heading_label.config(image=logo)
            self.heading_label.image = logo
            
    def reset(self):
        """
        Resets the program to allow for the insertion of another prompt
        """
        # Sends a signal to the AI class telling it to reset
        ai.set_is_resetting(True)
        
        # Deletes all text in the feedback box
        self.feedback_text.configure(state='normal')
        self.feedback_text.delete('1.0', 'end')
        self.feedback_text.configure(state='disabled')
        
        # Resets the upload image button to restore it to the original image
        image = Image.open('Images/uploadImage.png')
        image = image.resize((550,600))
        image = ImageTk.PhotoImage(image)
        self.upload_image_button.configure(image=image)
        self.upload_image_button.image = image
        
        # Changes the display code label back to its original text
        self.display_code_text.configure(state='normal')
        self.display_code_text.delete('1.0', 'end')
        
        # Makes the read_aloud_button invisible
        self.display_hidden_buttons(False)
            
    def upload_file(self):
        """
        Asks the user to select a compatible file, and then opens the image and sends it to vision.py for processing
        """
        # Asks the user to open a file and stores the path of the file
        path = fd.askopenfilename(type=('*.jpg', '*.png', '*.jpeg'))
        
        # Checks if the path is empty before performing any other actions
        if not path == '':
            
            # Check if the program has been reset, and if not, resets
            if not self.feedback_text.get('1.0', 'end').__len__() == 0:
                self.reset()
            
            # Begins a thread of the function send_prompt to read the prompt and send it to the AI
            prompt_thread = threading.Thread(target=self.send_prompt, args=(path,), name='prompt_thread')
            prompt_thread.daemon = True
            prompt_thread.start()
            
            # Sets the upload_image_button to display the uploaded image
            image = Image.open(path)
            image = image.resize((550,600))
            image = ImageTk.PhotoImage(image)
            self.upload_image_button.configure(image=image)
            self.upload_image_button.image = image
            
    # Waiting for Johnny
    def upload_taken_picture(self):
        """
        Opens the camera and allows the user to take a photo, and then sends it to vision.py for processing
        """
        
    def send_written_prompt(self):
        """
        Sends the prompt to vision.py for processing and displays the read prompt in the GUI
        """
        self.display_code_text.configure(state='disabled')
        prompt = self.display_code_text.get('1.0', 'end')
        ai.set_prompt(prompt)
        
    def send_uploaded_prompt(self, path):
        """
        Sends the prompt to vision.py for processing and displays the read prompt in the GUI
        """
        prompt = read_image(path)
        ai.set_prompt(prompt)
        self.display_code_text.insert('start', prompt)
        self.display_code_text.configure(state='disabled')
        
    def display_hidden_buttons(self, make_visible):
        """
        Sets the visibility of the read aloud button
        """
        if make_visible:
            self.read_aloud_button.grid(row=0, column=0, sticky='e', pady=(0,5))
            self.details_button.grid(row=2, column=0, sticky='w', pady=5)
        else:
            self.read_aloud_button.grid_forget()
            self.details_button.grid_forget()
        
    def read_aloud(self):
        text_to_speech_thread = threading.Thread(target=text_to_speech, args=(self.feedback_text.get('1.0','end'),), name='text_to_speech_thread')
        text_to_speech_thread.daemon = True
        text_to_speech_thread.start()
        
    def display_advice(self):
        read_aloud_visible = False
        while True:
            if not ai.get_has_completed():
                chunk = ai.get_response_chunk()
                self.feedback_text.configure(state='normal')
                self.feedback_text.insert('end', chunk)
                self.feedback_text.see('end')
                self.feedback_text.configure(state='disabled')
                read_aloud_visible = False
            elif ai.get_has_completed() and not read_aloud_visible:
                self.display_hidden_buttons(True)
                read_aloud_visible = True
                
    def follow_up(self):
        follow_up_thread = threading.Thread(target=ai.generate_follow_up_ai, args=(self.feedback_text.get('1.0','end'),), name='follow_up_thread')
        follow_up_thread.daemon = True
        follow_up_thread.start()
        self.feedback_text.configure(state='normal')
        self.feedback_text.delete('1.0', 'end')
        self.feedback_text.configure(state='disabled')
                            
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
        self.mode_button = Button(self.top_frame, text='Dark Mode',fg='white', bg='#056939', highlightbackground='#056939', activebackground='#056939', command=self.mode_toggle, font=('Arial', 16), cursor='hand2')
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
        self.right_frame.grid(row=0, column=1,pady=(0,10))
        
        # Create/load 'Upload Image' image:
        upload_image = Image.open('Images/uploadImage.png')
        upload_image = upload_image.resize((550, 600))
        upload_image = ImageTk.PhotoImage(upload_image)
        
        # Create and add tabbed section holding upload image button and label to display code from image
        self.tab_control = Notebook(self.left_frame)

        # Create tabs to switch between uploaded image and code from the image
        self.upload_tab = Frame(self.tab_control)
        self.code_tab = Frame(self.tab_control)
        self.picture_tab = Frame(self.tab_control)

        # Add tabs to the Notebook
        self.tab_control.add(self.picture_tab, text='Take a Picture')
        self.tab_control.add(self.upload_tab, text='Upload Image')
        self.tab_control.add(self.code_tab, text='Code')
        self.tab_control.grid(row=1,column=0, pady=(10,5))

        # Create and add the upload image button to the Notebook
        self.upload_image_button = Button(self.upload_tab, image=upload_image, command=self.upload_file, cursor='hand2')
        self.upload_image_button.grid(column=0, row=0)  

        # Create and add a label that diplays upload image's code to the Notebook
        self.display_code_text = Text(self.code_tab, wrap=WORD, font=('Futura', 16), width=46, height=25)
        self.edit_code_button = Button(self.code_tab, text='Edit Code', cursor='hand2', width=77, height=3, bg="#056939", fg=white, command=self.send_written_prompt)
        self.edit_code_button.grid(column=0, row=0, sticky='s')
        self.display_code_text.grid(column=0, row=0)
        
        # Create and add a label that displays the image taken from the camera

        # Create and add a label to explain text area
        self.advice_label = Label(self.right_frame, text='Advice from The Sage:', font=('Futura', 20))
        self.advice_label.grid(row=0, column=0, sticky='we', pady=(0,10))
        
        # Create and load the read aloud image (Credit to: https://freeicons.io/profile/22578)
        read_aloud_image = Image.open('Images/readAloud.png')
        read_aloud_image = ImageTk.PhotoImage(read_aloud_image)
        
        # Create and add a button to read the feedback aloud
        self.read_aloud_button = Button(self.right_frame, image=read_aloud_image, command=self.read_aloud, cursor='hand2')

        # Create font for ai feedback text
        self.feedback_font = Font(family='Helvetica', size=18)

        # Create and add a text area for ai feedback:
        self.feedback_text = Text(self.right_frame, bg='lightgray', state='disabled', font=self.feedback_font, width=46, height=22, wrap=WORD)
        self.feedback_text.grid(row=1, column=0)
        
        # Create follow up button
        self.details_button = Button(self.right_frame, text='Follow Up', fg='white', bg='#056939', highlightbackground='#056939', activebackground='#056939', command=self.follow_up, font=('Arial', 16), cursor='hand2')

        # Create and add a button to reset image and feedback
        self.reset_button = Button(self.left_frame, text='Reset', fg='white', bg='#056939', highlightbackground='#056939', activebackground='#056939', command=self.reset, font=('Arial', 16), cursor='hand2')
        self.reset_button.grid(row=2, column=0, sticky='w', pady=5)

        # Create and add a line separator
        self.bottom_seperator = Separator(self.root, orient='horizontal')
        self.bottom_seperator.pack(fill='x', padx='30')

        # Begins checking the response queue every 200 milliseconds
        recieve_advice_thread = threading.Thread(target=self.display_advice, name='recieve_advice_thread')
        recieve_advice_thread.daemon = True
        recieve_advice_thread.start()

        # Run GUI
        self.root.mainloop()
        
if __name__ == '__main__':
    ai = AI()
    gui = GUI()