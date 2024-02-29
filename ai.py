import ollama
for chunk in ollama.generate(model = 'codellama:13b-instruct', prompt = 'Why is the sky blue?', stream = True):
  print(chunk['response'], end='', flush=True)
