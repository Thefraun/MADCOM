try: import ollama 
except ImportError: print('Ollama is not installed. Please install it and try again.')
import threading
import queue
import time

# TODO: Add documentation
class AI:
    
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

    def generate_response(self, prompt_queue):
        """
        Generate a response based on prompts in the prompt_queue.
        
        Parameters:
            prompt_queue (Queue): A queue containing prompts to generate responses for.
        
        Returns:
            None
        """
        while True:
            if not prompt_queue.empty():
                for chunk in ollama.generate (
                    model = 'codellama:13b-instruct', prompt=prompt_queue.get(), stream=True,
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
            if(self.is_resetting):
                self.is_resetting = False
            else:
                time.sleep(0.1)

    def __init__(self):
        self.is_resetting = False
        self.prompt_queue = queue.Queue()
        self.response_queue = queue.Queue()
        ai_thread = threading.Thread(target=self.generate_response, args=(self.prompt_queue,), name='ai_thread')
        ai_thread.daemon = True
        ai_thread.start()