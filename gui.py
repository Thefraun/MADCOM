from tkinter import *
import ollama
import threading
import queue

#TODO: Pretty up the code

def get_response(prompt, queue):
    """
    Function to get response using a prompt and queue for storing the response.

    Parameters:
    - prompt: the prompt to generate the response
    - queue: the queue to store each chunk of the response

    Return type: None
    """
    for chunk in ollama.generate(
        model = 'codellama:13b-instruct', prompt=prompt, stream=True,
        system = 'You are a computer science teacher. If asked about non-computer science related questions, you simply politely decline to answer.'
        ):
        queue.put(chunk['response'])

def check_queue():
    """
    Check the queue for incoming messages and display them in the feedback area.
    """
    if not queue.empty():
        text = queue.get()
        feedback.configure(state='normal')
        feedback.insert('end', text)
        feedback.configure(state='disabled')
    root.after(100, check_queue)

# Create the thread and the queue, then begin the thread
running = True
queue = queue.Queue()
thread = threading.Thread(target=get_response, args=("DO NOT PRINT CODE", queue,))
thread.start()

root = Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(background='black')

root.title("Script Sage")
# frame1 = Frame(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightbackground="black", highlightthickness=5, bd= 0)
# frame1.pack()

heading = Label(root, text="Script Sage", font=('Arial', 18), bg="grey" )
heading.pack()

mainframe = Frame(root)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)

switch = Label(mainframe, text="Switch between code & image here", font=('Arial', 18))
switch.grid(row=0, column=0, sticky="we", pady=20)
uploadImage = Label(mainframe, text="Upload Image Here", font=('Arial', 18))
uploadImage.grid(row=1, column=0, sticky="we", pady=300)

space = Label(mainframe, text="", font=('Arial', 18))
space.grid(row=0, column=1, sticky="we")
#feedback = Label(mainframe, text="Receive your feedback here", font=('Arial', 18))
feedback = Text(mainframe, bg='white', state='disabled')
feedback.grid(row=1, column=1, sticky="we")

mainframe.pack(fill="x")

root.attributes('-fullscreen', True)

root.after(100, check_queue())

root.mainloop()

thread.join()