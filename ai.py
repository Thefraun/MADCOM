try: 
    import ollama
    has_ollama = True
except ImportError: 
    has_ollama = False
    print('Ollama is not installed. Please install Ollama to enable AI functionality.')
import threading
import queue
import time
class AI:
    global has_ollama
    def set_prompt(self, prompt):
        """
        Sets a prompt to be used in generate_response
        """
        self.prompt_queue.put(prompt)
        
    def set_is_resetting(self, is_resetting):
        """
        Sets if the AI is resetting
        """
        self.is_resetting = is_resetting
        
    def get_response_chunk(self):
        """
        Returns the last generated chunk from the queue
        """     
        return self.response_queue.get()

    
    def get_has_completed(self):
        '''
        Returns whether the AI has finished giving advice
        '''
        return self.has_completed
    
    def get_has_started(self):
        '''
        Returns whether the AI has started generating a response
        '''
        return self.has_started

    def generate_response_ai(self):
        """
        Generate a response based on prompts in the prompt_queue using AI, and puts it into the response_queue
        """
        while True:
            # Checks if there is a prompt in the queue
            # If there is, use the AI to generate a response to the prompt
            if not self.prompt_queue.empty():                
                # Start a thread to show the "Generating" message to the user as the response loads
                wait_thread = threading.Thread(target=self.wait_for_response, daemon=True, name='wait_thread')
                wait_thread.start()
                
                # Get the prompt and store it as the last inputted prompt
                self.last_prompt = self.prompt_queue.get()
                
                # Begin generating the response
                for chunk in ollama.generate(model='ScriptSage', prompt=self.last_prompt, stream=True, keep_alive=15):
                    # Flags that the response has begun, and the wait_thread should stop
                    self.has_started = True
                    
                    # Makes sure the program is not currently resetting
                    if not self.is_resetting:
                        # If it is not, add the chunk to the response_queue
                        self.response_queue.put(chunk['response'])
                        if chunk['done']:
                            # If the response is over, set the has_completed flag to true and the has_started flag to false
                            self.has_completed = True
                            self.has_started = False
                        else:
                            # If the response is not over, set the has_completed flag to false
                            self.has_completed = False
                    else:
                        # If the program is resetting, clear the response_queue, set the flags to false, and break from the current response
                        self.response_queue.queue.clear()
                        self.has_started = False
                        self.is_resetting = False
                        break
            # If the program is resetting outside of a response, set all flags to false
            if self.is_resetting:
                self.has_started = False
                self.has_completed = False
                self.is_resetting = False
            time.sleep(0.2)
            
    def generate_follow_up_ai(self, past_message):
        """
        Generate a follow-up based on a past message using AI
        """
        # Flags that the response is not completed and has not started responding
        self.has_completed = False
        self.has_started = False
        
        # Start a thread to show the "Generating" message to the user as the response loads
        wait_thread = threading.Thread(target=self.wait_for_response, daemon=True, name='wait_thread')
        wait_thread.start()
        
        # Begin generating the follow up message
        for chunk in ollama.chat(model = 'ScriptSage', messages=[{'role': 'user', 'content': self.last_prompt}, {'role': 'assistant', 'content': past_message}, {'role': 'user', 'content': 'Can you please give me more details about the errors in the code?'}], stream=True):
            self.has_started = True
            # Makes sure that the program is not currently resetting
            if not self.is_resetting:
                # Adds the generated chunk into the response_queue
                self.response_queue.put(chunk['message']['content'])
                if chunk['done']:
                    # If the response is over, set the has_completed flag to true
                    self.has_completed = True
                    self.has_started = False
                else:
                    # If the response is not over, set the has_completed flag to false
                    self.has_completed = False
            else:
                # If the AI is resetting, clear the response_queue and break from the current response
                self.response_queue.queue.clear()
                self.is_resetting = False
                break
            
    def generate_response_no_ai(self):
        """
        Generates a response when the user inputs a new prompt, without the use of AI
        """
        while True:
            # Checks if there is a prompt in the queue
            if not self.prompt_queue.empty():
                # If there is, get the prompt and store it as the last inputted prompt
                self.last_prompt = self.prompt_queue.get()
                
                # Checks whether the reset button has been pressed
                if not self.is_resetting:
                    # If it has not been pressed, generate a faux AI response, put it in the response queue, and indicate the response is over
                    self.response_queue.put('This is where the AI would give you feedback based on this code: ' + self.last_prompt)
                    self.has_completed = True
                else:
                    # If it has been pressed, reset the response queue, and indicate that the reset has completed and the response is not over
                    self.response_queue.queue.clear()
                    self.is_resetting = False
                    self.has_completed = False
    
    def wait_for_response(self):
        '''
        Provide visual to indicate that a response is being generated
        '''
        i = 1
        while not self.has_started:
            if not self.is_resetting:
                if i % 3 == 1:
                    self.response_queue.put('Generating.')
                elif i % 3 == 2:
                    self.response_queue.put('Generating..')
                else:
                    self.response_queue.put('Generating...')
                i+=1
                time.sleep(.5)
            else:
                break

    def __init__(self):
        """
        Creates an instance of the AI class and all of the associated variables
        """
        global has_ollama
        self.last_prompt = ''
        self.is_resetting = False
        self.has_completed = False
        self.has_started = False
        self.prompt_queue = queue.Queue()
        self.response_queue = queue.Queue()
        
        # If the Ollama library is installed, begin running the AI in a separate thread
        if has_ollama:
            ai_thread = threading.Thread(target=self.generate_response_ai, args=(), name='ai_thread')
            ai_thread.daemon = True
            ai_thread.start()
        else:
        # If the Ollama library is not installed, begin running a mock version of the AI in a separate thread
            no_ai_thread = threading.Thread(target=self.generate_response_no_ai, args=(), name='no_ai_thread')
            no_ai_thread.daemon = True
            no_ai_thread.start()