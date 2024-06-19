from __future__ import annotations
import json
import time
import requests

request_body = {
    "model": "internLM2-20B",
    "messages": [
        {"role": "system", "content": "You are a helpful, pattern-following assistant."},
        {"role": "user", "content": "Help me translate the following corporate jargon into plain English."},
        {"role": "assistant", "content": "Sure, I'd be happy to!"},
        {"role": "user", "content": "New synergies will help drive top-line growth."},
        {"role": "assistant",
            "content": "Things working well together will increase revenue."},
        {"role": "user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
        {"role": "assistant",
            "content": "Let's talk later when we're less busy about how to do better."},
        {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
    ],
    "stream": True
}


def make_response_json_stream(content: str = ""):
    return {
        "id": "chatcmpl-9RzWgX2FzFZh39LuE2RYAaYhJAVm1",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "choices": [
            {
                "index": 0,
                "delta": {
                    "role": "assistant",
                    "content": content
                },
                "logprobs": None,
                "finish_reason": None
            }
        ]
    }


def make_response_json(content: str = ""):
    obj = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "gpt-3.5-turbo-0125",
        "system_fingerprint": "fp_44709d6fcb",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": f"{content}",
            },
            "logprobs": None,
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 12,
            "total_tokens": 21
        }
    }
    return obj


last = {"id": "chatcmpl-9RzWgX2FzFZh39LuE2RYAaYhJAVm1", "object": "chat.completion.chunk", "created": 1716458390,
        "model": "gpt-3.5-turbo-0125", "system_fingerprint": None, "choices": [{"index": 0, "delta": {}, "logprobs": None, "finish_reason": "stop"}]}


def invoke_langgraph_generation(request_body):
    url = "http://192.168.2.95:10050/api/zero_agent/langgraph"
    with requests.post(url, json=request_body, stream=True) as response:
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                message = chunk
                llm_response = message.decode('utf-8')
                yield json.loads(llm_response)['data']
    return None


def invoke_general_chatting(request_body):
    url = "http://192.168.2.95:10020/api/llm/chatting"
    with requests.post(url, json=request_body, stream=True) as response:
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                message = chunk
                llm_response = message.decode('utf-8')
                yield json.loads(llm_response)['data']
    return None


def stream_generator_general_chatting(request_body):
    for token in invoke_general_chatting(request_body):
        res = make_response_json_stream(token)
        yield json.dumps(res)
    yield json.dumps(last)
    yield "[DONE]"


def mock_streaming_text():
    for x in list("Help me translate the following corporate jargon into plain English."):
        yield x


def stream_generator(request_body):
    for token in invoke_langgraph_generation(request_body):
        res = make_response_json_stream(token)
        yield json.dumps(res)
    yield "[DONE]"
