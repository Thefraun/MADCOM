from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Notebook
from tkinter.ttk import Separator
from tkinter.ttk import Style
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from cloud_services import read_image, text_to_speech
from ai import AI
import threading
import cv2

# Defines the GUI class, containing the GUI and all functions associated
class GUI:
    def mode_toggle(self):
        """
        Toggle the program between light and dark mode
        """
        if self.mode_button.cget('text') == 'Dark Mode':
            # If the program is in light mode, sets all widgets to dark mode
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
            # If the program is in dark mode, sets all widgets to light mode
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
        
        # Resets the upload image button and take picture button to restore them to their original images
        self.upload_image_button.configure(image=self.upload_image)
        self.upload_image_button.image = self.upload_image
        self.take_picture_button.configure(image=self.take_picture_image)
        self.take_picture_button.image = self.take_picture_image
        
        # Changes the display code label back to its original text
        self.code_text.configure(state='normal')
        self.code_text.delete('1.0', 'end')
        
        # Makes the read_aloud_button invisible
        self.display_hidden_buttons(False)
        
    def create_video_gui(self):
        
        self.reset()
        # Create a GUI app 
        self.app = Toplevel()
        
        # Create an instance of the VideoCapture object
        self.vid = cv2.VideoCapture()
        
        # Create and add a button to open the camera in GUI app
        button = Button(self.app, text='Take Picture', command=self.capture_screen, cursor='hand2', fg='white', bg='#056939', highlightbackground='#056939', activebackground='#056939')
        button.pack(fill='both', expand=True, side=BOTTOM)

        # Create a label and display it on app
        self.label_widget = Label(self.app, text='Loading camera...', font=('Helvetica', 20))
        self.label_widget.pack()
                
        # Make the window modal, disables any interaction with the main window
        self.app.grab_set()
        
        # Starts the camera and begins displaying the video feed
        self.start_camera()
        
        self.app.protocol('WM_DELETE_WINDOW', self.app_close_operation)
        
        # Create an infinite loop to show the video capture
        self.app.mainloop()
                
    def start_camera(self):
    
        # Create a video capture object and attempts to open a connected camera
        self.vid.open(2, cv2.CAP_DSHOW)
        
        # Sets the size of the window
        self.app.geometry('800x600')
        
        # Check if the video capture option was correctly opened, and if not, use the webcam
        if not self.vid.isOpened():
            self.vid.open(0, cv2.CAP_DSHOW)
            self.app.geometry('800x520')
        
        # Set the width and height of the capture frames
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)
        
        # Begin capturing video
        self.capture_video()
        
    def capture_video(self): 
        
        # Capture the video frame by frame 
        _, frame = self.vid.read() 

        # Convert image from one color space to other 
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
        # Capture the latest frame and transform to image 
        self.captured_image = Image.fromarray(opencv_image) 

        # Convert captured image to photoimage 
        photo_image = ImageTk.PhotoImage(image=self.captured_image)

        # Displaying photoimage in the label 
        self.label_widget.image = photo_image

        # Configure image in the label 
        self.label_widget.configure(image=photo_image, text='')
        
        # Repeat the function every 10 milliseconds
        self.app.after(10, self.capture_video)
        
    def capture_screen(self):
        
        # Saves the taken picture
        picture = self.captured_image
        path = "C:/Users/logan/Pictures/Code/takenPicture.png"
        picture.save(path)
        
        # Closes the picture window
        self.app_close_operation()
        
        # Sends the picture to Azure for processing
        prompt_thread = threading.Thread(target=self.send_uploaded_prompt, args=(path,), name='prompt_thread')
        prompt_thread.daemon = True
        prompt_thread.start()
        
        # Sets the upload_image_button to display the uploaded image
        image = Image.open(path)
        image = image.resize((550,600))
        image = ImageTk.PhotoImage(image)
        self.take_picture_button.configure(image=image)
        self.upload_image_button.image = image
        
    def app_close_operation(self):
        '''
        Destroys all widgets in the app, and closes the camera connection
        '''
        self.app.destroy()
        self.vid.release()
            
    def upload_file(self):
        """
        Asks the user to select a compatible file, and then opens the image and sends it to Azure for processing
        """
        # Resets the program so that multiple prompts are not uploaded at once
        self.reset()
        # Asks the user to open a file and stores the path of the file
        path = fd.askopenfilename(type=('*.jpg', '*.png', '*.jpeg'))
        
        # Checks if the path is empty before performing any other actions
        if not path == '':
            # Check if the program has been reset, and if not, resets
            if not self.feedback_text.get('1.0', 'end').__len__() == 0:
                self.reset()
            
            # Begins a thread of the function send_prompt to read the prompt and send it to the AI
            prompt_thread = threading.Thread(target=self.send_uploaded_prompt, args=(path,), name='prompt_thread')
            prompt_thread.daemon = True
            prompt_thread.start()
            
            # Sets the upload_image_button to display the uploaded image
            image = Image.open(path)
            image = image.resize((550,600))
            image = ImageTk.PhotoImage(image)
            self.upload_image_button.configure(image=image)
            self.upload_image_button.image = image
        
    def send_written_prompt(self):
        """
        Reads the written code from the code_text area, and sends it to the AI for processing
        """
        # Checks if the feedback text field has been reset, and if not resets the feedback area
        if not self.feedback_text.get('1.0', 'end').__len__() == 0:
            ai.set_is_resetting(True)
            self.feedback_text.configure(state='normal')
            self.feedback_text.delete('1.0', 'end')
            self.feedback_text.configure(state='disabled')
            self.upload_image_button.configure(image=self.upload_image)
            self.take_picture_button.configure(image=self.take_picture_image)
            self.display_hidden_buttons(False)
        
        # Disables the text field so that the prompt cannot be altered
        self.code_text.configure(state='disabled')
        
        # Reads the prompt and sends it to the AI to be processed
        prompt = self.code_text.get('1.0', 'end')
        ai.set_prompt(prompt)
        
    def send_uploaded_prompt(self, path):
        """
        Sends the prompt to Azure for processing and displays the read prompt in the GUI
        """
        # Sends the image to Azure for processing
        prompt = read_image(path)
        
        # Sends the returned text from Azure into the AI as the prompt
        ai.set_prompt(prompt)
        
        # Displays the prompt in the code tab
        self.code_text.insert('1.0', prompt)
        self.code_text.configure(state='disabled')
        
    def display_hidden_buttons(self, make_visible):
        """
        Sets the visibility of the read aloud button and the follow up button
        """
        if make_visible:
            self.read_aloud_button.grid(row=0, column=0, sticky='e', pady=(0,5))
            self.follow_up_button.grid(row=2, column=0, sticky='w', pady=(0,5))
        else:
            self.read_aloud_button.grid_forget()
            self.follow_up_button.grid_forget()
        
    def read_aloud(self):
        '''
        Begins the text to speech thread, which reads the text in the feedback_text area
        '''
        text_to_speech_thread = threading.Thread(target=text_to_speech, args=(self.feedback_text.get('1.0','end'),), name='text_to_speech_thread')
        text_to_speech_thread.daemon = True
        text_to_speech_thread.start()
        
    def display_advice(self):
        '''
        Displays the advice that the AI has generated in the feedback_text area
        '''
        # Creates a flag for whether the hidden buttons are visible
        hidden_buttons_visible = False
        # Initiates an infinite loop to keep the thread running
        while True:
            # Checks if the AI has finished giving advice
            # If the AI has not completed giving advice, prints the next chunk of advice
            if not ai.get_has_completed():
                # Gets the most recent chunk from the AI and prints it in the feedback_text area
                chunk = ai.get_response_chunk()
                # Checks if the chunk received is empty or not
                if chunk != '':
                    if not ai.has_started:
                        # If the AI has not started responding, display the generating message to the user
                        self.feedback_text.configure(state='normal')
                        self.feedback_text.delete('1.0', 'end')
                        self.feedback_text.insert('1.0', chunk)
                        self.feedback_text.configure(state='disabled')
                    else:
                        # If the AI has started responding, delete the previous text in feedback_text and insert the new text
                        self.feedback_text.configure(state='normal')
                        if self.feedback_text.get('1.0', '13.0').startswith('Generating'):
                            self.feedback_text.delete('1.0', 'end')
                        self.feedback_text.insert('end', chunk)
                        self.feedback_text.see('end')
                        self.feedback_text.configure(state='disabled')
                        # Resets the flag for whether the hidden buttons are visible
                        hidden_buttons_visible = False
                        
            # If the AI has completed giving advice, and the read_aloud_button and follow_up_button are not already visible, display the buttons
            elif ai.get_has_completed() and not hidden_buttons_visible:
                self.display_hidden_buttons(True)
                self.code_text.configure(state='normal')
                self.take_picture_button.configure(cursor='hand2', command=self.create_video_gui)
                self.upload_image_button.configure(cursor='hand2', command=self.upload_file)
                hidden_buttons_visible = True
                
    def follow_up(self):
        '''
        Prompts the AI to generate more details on the advice it previously gave
        '''
        # Begin generating follow up advice on a new thread
        follow_up_thread = threading.Thread(target=ai.generate_follow_up_ai, args=(self.feedback_text.get('1.0','end'),), name='follow_up_thread')
        follow_up_thread.daemon = True
        follow_up_thread.start()
        
        # Clears the previous advice
        self.feedback_text.configure(state='normal')
        self.feedback_text.delete('1.0', 'end')
        self.feedback_text.configure(state='disabled')
                            
    def __init__(self):
        '''
        Initialise the main GUI
        '''
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
                    'configure': {'padding': [25, 10], 'borderwidth':[2], 'foreground': black, 'font': tab_font},
                    'map':       {'background': [('selected', self.default_light), ('!active', self.default_light)],
                                'expand': [('selected', [5, 5, 5, 5])]}}})

        # Create style for dark mode for Notebook
        self.style.theme_create( 'darkMode', settings ={
                'TNotebook': {
                    'configure': {'tabmargins': [5, 5, 10, 5],'background': self.default_dark }},
                'TNotebook.Tab': {
                    'configure': {'padding': [25, 10], 'borderwidth':[2], 'foreground': white, 'font': tab_font},
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
        self.space_label.grid(row=0, column=0, padx=(138,0))

        # Create font for the heading
        heading_font = Font(family='Helvetica', size=36, weight='bold')

        # Create and add a heading @ top of GUI w/ application name
        logo = Image.open('Images/ScriptSage.png')
        logo = ImageTk.PhotoImage(logo)
        self.heading_label = Label(self.top_frame, image=logo, font=heading_font, pady=15)
        self.heading_label.grid(row=0, column=1)

        # Create and add a button to switch between light and dark mode
        self.mode_button = Button(self.top_frame, text='Dark Mode',fg='white', bg='#056939', highlightbackground='#056939', activebackground='#056939', command=self.mode_toggle, font=('Arial', 16), cursor='hand2')
        self.mode_button.grid(row=0, column=2, sticky='e', padx=(0,138))

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
        self.upload_image = Image.open('Images/uploadImage.png')
        self.upload_image = self.upload_image.resize((550, 600))
        self.upload_image = ImageTk.PhotoImage(self.upload_image)
        
        # Create/load 'Take Picture' image:
        self.take_picture_image = Image.open('Images/takePicture.png')
        self.take_picture_image = self.take_picture_image.resize((550, 600))
        self.take_picture_image = ImageTk.PhotoImage(self.take_picture_image)
        
        # Create and add tabbed section holding upload image button and label to display code from image
        self.tab_control = Notebook(self.left_frame)

        # Create tabs to switch between uploaded image and code from the image
        self.upload_tab = Frame(self.tab_control)
        self.code_tab = Frame(self.tab_control)
        self.picture_tab = Frame(self.tab_control)

        # Add tabs to the Notebook
        self.tab_control.add(self.picture_tab, text='Take a Picture')
        self.tab_control.add(self.upload_tab, text='Upload Image')
        self.tab_control.add(self.code_tab, text='Write Code')
        self.tab_control.grid(row=1,column=0, pady=(10,5))
        
        # Create and add the take picture button to the Notebook
        self.take_picture_button = Button(self.picture_tab, image=self.take_picture_image, command=self.create_video_gui, cursor='hand2')
        self.take_picture_button.grid(column=0, row=0)

        # Create and add the upload image button to the Notebook
        self.upload_image_button = Button(self.upload_tab, image=self.upload_image, command=self.upload_file, cursor='hand2')
        self.upload_image_button.grid(column=0, row=0)  

        # Create and add a text field and button to submit written code to the Notebook
        self.code_text = Text(self.code_tab, wrap=WORD, font=('Futura', 16), width=45, height=25, padx=7, pady=2)
        self.edit_code_button = Button(self.code_tab, text='Submit Code', cursor='hand2', width=78, height=3, bg="#056939", fg=white, command=self.send_written_prompt)
        self.edit_code_button.grid(column=0, row=0, sticky='s', pady=(10,0))
        self.code_text.grid(column=0, row=0, pady=(0, 0))

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
        self.feedback_text = Text(self.right_frame, bg='lightgray', state='disabled', font=self.feedback_font, width=46, height=22, wrap=WORD, padx=7, pady=2)
        self.feedback_text.grid(row=1, column=0, pady=(0,15), sticky='ns')
        
        # Create follow up button
        self.follow_up_button = Button(self.right_frame, text='Follow Up', fg='white', bg='#056939', highlightbackground='#056939', activebackground='#056939', command=self.follow_up, font=('Arial', 16), cursor='hand2')

        # Create and add a button to reset image and feedback
        self.reset_button = Button(self.left_frame, text='Reset', fg='white', bg='#056939', highlightbackground='#056939', activebackground='#056939', command=self.reset, font=('Arial', 16), cursor='hand2')
        self.reset_button.grid(row=2, column=0, sticky='w', pady=(10,5))

        # Create and add a line separator
        self.bottom_seperator = Separator(self.root, orient='horizontal')
        self.bottom_seperator.pack(fill='x', padx='30')

        # Begins checking the response queue every 200 milliseconds
        recieve_advice_thread = threading.Thread(target=self.display_advice, name='recieve_advice_thread')
        recieve_advice_thread.daemon = True
        recieve_advice_thread.start()
    
        # Run GUI
        self.root.mainloop()
        
# Begin the program
if __name__ == '__main__':
    ai = AI()
    gui = GUI()