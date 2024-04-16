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
        Generate a response based on prompts in the prompt_queue.
        
        Parameters:
            prompt_queue (Queue): A queue containing prompts to generate responses for.
        
        Returns:
            None
        """
        while True:
            if not self.prompt_queue.empty():
                for chunk in ollama.generate (
                    model = 'codellama:13b-instruct', prompt=self.prompt_queue.get(), stream=True,
                    system = '''Please analyse the following Python code. Please ignore any errors in indentation.
                                Your response to any prompt cannot be over 500 characters or 5 sentences. If your response is over 500 characters or 5 sentences,
                                You will be punished.
                                Thank you!''',
                ):
                    if not self.is_resetting:
                        self.response_queue.put(chunk['response'])
                    else:
                        self.response_queue.queue.clear()
                        self.is_resetting = False
                        break
                self.has_completed = True
            if self.is_resetting:
                self.has_completed = False
                self.is_resetting = False
            time.sleep(0.2)
            
    def generate_response_no_ai(self, prompt_queue):
        while True:
            if not self.prompt_queue.empty():
                if not self.is_resetting:
                    self.response_queue.put('This is where the AI would give you feedback.')
                    self.has_completed = True
                else:
                    self.response_queue.queue.clear()
                    self.is_resetting = False
                    self.has_completed = False

    def __init__(self):
        global has_ollama
        self.is_resetting = False
        self.has_completed = False
        self.prompt_queue = queue.Queue()
        self.response_queue = queue.Queue()
        if has_ollama:
            ai_thread = threading.Thread(target=self.generate_response_ai, args=(self.prompt_queue,), name='ai_thread')
            ai_thread.daemon = True
            ai_thread.start()
        else:
            no_ai_thread = threading.Thread(target=self.generate_response_no_ai, args=(self.prompt_queue,), name='no_ai_thread')