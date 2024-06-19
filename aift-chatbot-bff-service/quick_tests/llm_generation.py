import requests

url = "http://192.168.2.95:10000/api/llm/generation"

request_body = {
    "model": "internlm2-chat-20B",
    "prompt": "New synergies will help drive top-line growth.",
    "messages": [
        [
            "Help me translate the following corporate jargon into plain English.",
            "Sure, I'd be happy to!"
        ]
    ],
    "stream": True
}

with requests.post(url, json=request_body, stream=True) as response:
    for chunk in response.iter_content(chunk_size=None):
        if chunk:
            message = chunk
            llm_response = message.decode('utf-8')
            print(llm_response)
