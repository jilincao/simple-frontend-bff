import requests


url = "http://192.168.2.95:10050/api/zero_agent/langgraph"
prompt = '你们有哪些拖把的品牌'

# state = {"keys": {"question": prompt}, "messages": []}

request_body = {

    "model": "internlm2-chat-20b",

    "messages": [

        {"role": "system", "content": "You are a helpful, pattern-following assistant."},

        {"role": "user", "content": prompt},

    ]

}
with requests.post(url, json=request_body, stream=True) as response:
    for chunk in response.iter_content(chunk_size=None):
        if chunk:
            message = chunk
            llm_response = message.decode('utf-8')
            print(llm_response)
