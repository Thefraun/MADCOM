import ollama
#TODO: Add system prompt, add threading to deliver responses as stream
def getResponse(prompt):
  response = ''
  for chunk in ollama.generate(model = 'codellama:13b-instruct', prompt = prompt, stream = True):
    response += chunk['response']
  return response