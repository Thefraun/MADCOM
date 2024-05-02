# Importing tkinter module
from tkinter import *
import cv2 
from PIL import Image, ImageTk 
import threading

class Camera:
    
    def __init__(self):
        # Define a video capture object 
        self.vid = cv2.VideoCapture(0) # 2 -> index of webcam cuz its the second camera option

        # Declare the width and height in variables 
        width, height = 800, 600
        # Set the width and height 
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

        # Create a GUI app 
        self.app = Toplevel()
        # Set the size of the app window
        self.app.geometry(f'{width}x{height}')

        # Bind the app with Escape keyboard to 
        # quit app whenever pressed 
        self.app.bind('<Escape>', lambda e: self.app.quit()) 

        # Create a label and display it on app 
        self.label_widget = Label(self.app) 
        self.label_widget.pack() 
        
        # Create a button to open the camera in GUI app
        self.button = Button(self.app, text='take picture', command=self.capture_screen, cursor='hand2')
        self.button.pack()
        
        camera_thread = threading.Thread(target=self.open_camera, name='camera_thread')
        camera_thread.daemon = True
        camera_thread.start()
    
        # Create an infinite loop for displaying app on screen 
        
        self.app.mainloop() 
       
        
    def open_camera(self): 

        # Capture the video frame by frame 
        _, frame = self.vid.read() 

        # Convert image from one color space to other 
        self.opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
        self.opencv_image = cv2.flip(self.opencv_image, 1)

        # Capture the latest frame and transform to image 
        self.captured_image = Image.fromarray(self.opencv_image) 

        # Convert captured image to photoimage 
        self.photo_image = ImageTk.PhotoImage(image=self.captured_image)

        # Displaying photoimage in the label 
        self.label_widget.photo_image = self.photo_image

        # Configure image in the label 
        self.label_widget.configure(image=self.photo_image) 

        # Repeat the same process after every 10 seconds 
        self.label_widget.after(10, self.open_camera) 
        
    def get_path(self):
        return self.path
        
    def capture_screen(self):
        self.picture = self.captured_image
        self.path = "/home/johnny/pictures/screenshot_filename.png"
        self.picture.save(self.path)
        return self.path