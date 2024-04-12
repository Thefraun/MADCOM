import ollama
import threading
import queue
import time

# TODO: Add Documentation
class AI:
    
    def set_prompt(self, prompt):
        self.prompt_queue.put(prompt)
        
    def set_is_resetting(self, is_resetting):
        self.is_resetting = is_resetting
        
    def get_response_chunk(self):
        return self.response_queue.get()

    def generate_response(self, prompt_queue):
        """
        Function to get response using a prompt and queue for storing the response.

        Parameters:
        - prompt: the prompt to generate the response
        - queue: the queue to store the response

        Return type: None
        """
        while True:
            if not prompt_queue.empty():
                for chunk in ollama.generate (
                    model = 'codellama:13b-instruct', prompt=prompt_queue.get(), stream=True,
                    system = '''Please analyse the following Python code. Please ignore any errors in indentation.
                                Thank you!''',
                    ):
                        if not self.is_resetting:
                            self.response_queue.put(chunk['response'])
                        else:
                            self.response_queue.queue.clear()
                            self.is_resetting = False
                            break
            else:
                time.sleep(0.1)

    def __init__(self):
        self.is_resetting = False
        self.prompt_queue = queue.Queue()
        self.response_queue = queue.Queue()
        ai_thread = threading.Thread(target=self.generate_response, args=(self.prompt_queue,), name='ai_thread')
        ai_thread.daemon = True
        ai_thread.start()