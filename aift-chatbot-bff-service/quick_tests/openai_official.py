from openai import OpenAI
from termcolor import colored
client = OpenAI()

"""
Non Streaming
"""
print(colored("Non Streaming", 'red'))
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(completion)

"""
Streaming
"""
print(colored('Streaming', 'red'))
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    stream=True
)
for chunk in completion:
    print(chunk.choices[0].delta)
