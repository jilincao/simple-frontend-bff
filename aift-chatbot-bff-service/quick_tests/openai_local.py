from openai import OpenAI
from termcolor import colored

client = OpenAI(api_key="local", base_url="http://192.168.2.97:9050/vercel")
# client = OpenAI(api_key="local", base_url="http://192.168.2.97:9050")


"""
Non Streaming
"""
# print(colored("Non Streaming", 'red'))
# completion = client.chat.completions.create(
#     model="internLM2-20B",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Hello!"}
#     ]
# )

# print(completion)

"""
Streaming
"""
print(colored('Streaming', 'red'))
completion = client.chat.completions.create(
    model="internLM2-20B",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    stream=True
)
for chunk in completion:
    print(chunk.choices[0].delta)
