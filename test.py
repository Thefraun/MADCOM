# File to test any function calls
# Encode file path so as to not encounter any unicode issues | May or may not be needed

import tkinter as tk  # PEP8: `import *` is not preferred
import time

import threading
import queue
import datetime

import random

# --- functions ---

def calculations(q):
    while running:
        # some calculations
        time.sleep(random.randint(1, 10))
        # create message
        text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # send message using queue
        q.put(text)
        
def check_queue():
    # check if there is new message in queue
    if not q.empty():
        # get new message
        text = q.get()
        # append in `Text`
        textbox.insert('end', text + '\n') 

    # repeate after 0.1s
    window.after(100, check_queue) # 100ms = 0.1s
    
# --- main ---

running = True
q = queue.Queue()

t = threading.Thread(target=calculations, args=(q,))
t.start()

# - GUI -

window = tk.Tk()
window.geometry("600x600")

textbox = tk.Text(window, bg='gray')
textbox.pack()

button = tk.Button(window, text='Exit', command=window.destroy)
button.pack()

window.after(100, check_queue) # 100ms = 0.1s

window.mainloop()

# - end - 

running = False  # stop loop in thread
t.join()         # wait for the end of thread
