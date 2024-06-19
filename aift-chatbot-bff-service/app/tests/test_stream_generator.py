
from app.utils import invoke_langgraph_generation, stream_generator


model = "internlm2-chat-20B"
messages = [
    {
        "role": "system",
        "content": "You are a helpful, pattern-following assistant."
    },
    {
        "role": "user",
        "content": "Help me translate the following corporate jargon into plain English."
    }
]

for i, token in enumerate(invoke_langgraph_generation(model, messages)):
    print(i, token)
