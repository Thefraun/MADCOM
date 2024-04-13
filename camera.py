# Importing tkinter module
from tkinter import *
import cv2 
from PIL import Image, ImageTk 
class Camera:
    
    def __init__(self):
        # Define a video capture object 
        self.vid = cv2.VideoCapture(2) # 2 -> index of webcam cuz its the second camera option

        # Declare the width and height in variables 
        width, height = 800, 600
        # Set the width and height 
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

        # Create a GUI app 
        self.app = Tk() 

        # Bind the app with Escape keyboard to 
        # quit app whenever pressed 
        self.app.bind('<Escape>', lambda e: self.app.quit()) 

        # Create a label and display it on app 
        self.label_widget = Label(self.app) 
        self.label_widget.pack() 
        self.open_camera()

    # Create a function to open camera and 
    # display it in the label_widget on app 

    def open_camera(self): 

        # Capture the video frame by frame 
        _, frame = self.vid.read() 

        # Convert image from one color space to other 
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

        # Capture the latest frame and transform to image 
        captured_image = Image.fromarray(opencv_image) 

        # Convert captured image to photoimage 
        photo_image = ImageTk.PhotoImage(image=captured_image) 

        # Displaying photoimage in the label 
        self.label_widget.photo_image = photo_image 

        # Configure image in the label 
        self.label_widget.configure(image=photo_image) 

        # Repeat the same process after every 10 seconds 
        self.label_widget.after(10, open_camera) 
        
        # Create an infinite loop for displaying app on screen 
        self.app.mainloop() 
