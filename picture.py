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
        
        camera_thread = threading.Thread(target=self.open_camera, name='camera_thread')
        camera_thread.daemon = True
        camera_thread.start()
    
        # Create an infinite loop for displaying app on screen 
        
        camera_thread = threading.Thread(target=self.open_camera, name='camera_thread')
        camera_thread.daemon = True
        camera_thread.start()
        
        self.app.mainloop() 
       
        
    def open_camera(self): 

        # Capture the video frame by frame 
        _, frame = self.vid.read() 

        # Convert image from one color space to other 
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
        opencv_image = cv2.flip(opencv_image, 1)

        # Capture the latest frame and transform to image 
        captured_image = Image.fromarray(opencv_image) 

        # Convert captured image to photoimage 
        photo_image = ImageTk.PhotoImage(image=captured_image)

        # Displaying photoimage in the label 
        self.label_widget.photo_image = photo_image

        # Configure image in the label 
        self.label_widget.configure(image=photo_image) 

        # Repeat the same process after every 10 seconds 
        self.label_widget.after(10, self.open_camera) 
        
    def capture_screen(self):
        # Capture the screen
        #screenshot = ImageGrab.grab(bbox=(0, 0, 800, 600))
        screenshot = ImageGrab.grab(bbox=(0, 0, 800, 600), xdisplay=":0")

        # Convert the image to bytes
        with BytesIO() as output:
            screenshot.save(output, format='PNG')
            image_bytes = output.getvalue()

        # You can save or process the image bytes here
        # For example, you can save it to a file:
        screenshot.show()
        #screenshot.save("screenshot.png")
        screenshot.save("/home/johnny/pictures/screenshot_filename.png")
