try: 
    import ollama
    has_ollama = True
except ImportError: 
    has_ollama = False
    print('Ollama is not installed. Please install Ollama to enable AI functionality.')
import threading
import queue
import time
# TODO: Add documentation
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
        return self.has_completed

    def generate_response_ai(self):
        """
        Generate a response based on prompts in the prompt_queue using AI, and puts it into the response_queue
        """
        while True:
            if not self.prompt_queue.empty():
                self.last_prompt = self.prompt_queue.get()
                for chunk in ollama.generate(model='ScriptSage', prompt=self.last_prompt, stream=True):
                    if not self.is_resetting:
                        self.response_queue.put(chunk['response'])
                        if chunk['done']:
                            self.has_completed = True
                        else:
                            self.has_completed = False
                    else:
                        self.response_queue.queue.clear()
                        self.is_resetting = False
                        break
            if self.is_resetting:
                self.has_completed = False
                self.is_resetting = False
            time.sleep(0.2)
            
    def generate_follow_up_ai(self, past_message):
        """
        Generate a follow-up based on a past message using AI
        """
        self.has_completed = False
        for chunk in ollama.chat(model = 'ScriptSage', messages=[{'role': 'user', 'content': self.last_prompt}, {'role': 'assistant', 'content': past_message}, {'role': 'user', 'content': 'Can you please give me more details about the errors?'}], stream=True):
            if not self.is_resetting:
                self.response_queue.put(chunk['message']['content'])
            else:
                self.response_queue.queue.clear()
                self.is_resetting = False
                break
        self.has_completed = True
    def generate_response_no_ai(self):
        """
        Generates a response when the user inputs a new prompt, without the use of AI
        """
        while True:
            if not self.prompt_queue.empty():
                self.last_prompt = self.prompt_queue.get()
                if not self.is_resetting:
                    self.response_queue.put('This is where the AI would give you feedback based on this code: ' + self.last_prompt)
                    self.has_completed = True
                else:
                    self.response_queue.queue.clear()
                    self.is_resetting = False
                    self.has_completed = False

    def __init__(self):
        """
        Creates an instance of the Ollama class and all of the associated variables
        """
        global has_ollama
        self.last_prompt = ''
        self.is_resetting = False
        self.has_completed = False
        self.prompt_queue = queue.Queue()
        self.response_queue = queue.Queue()
        if has_ollama:
            ai_thread = threading.Thread(target=self.generate_response_ai, args=(), name='ai_thread')
            ai_thread.daemon = True
            ai_thread.start()
        else:
            no_ai_thread = threading.Thread(target=self.generate_response_no_ai, args=(), name='no_ai_thread')
            no_ai_thread.daemon = True
            no_ai_thread.start()