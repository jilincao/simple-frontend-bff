"""
https://cookbook.openai.com/examples/how_to_format_inputs_to_chatgpt_models

sample request body
{
    "model": "internLM2-20B",
    "messages": [
        {"role": "system", "content": "You are a helpful, pattern-following assistant."},
        {"role": "user", "content": "Help me translate the following corporate jargon into plain English."},
        {"role": "assistant", "content": "Sure, I'd be happy to!"},
        {"role": "user", "content": "New synergies will help drive top-line growth."},
        {"role": "assistant", "content": "Things working well together will increase revenue."},
        {"role": "user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
        {"role": "assistant", "content": "Let's talk later when we're less busy about how to do better."},
        {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
    ]
}

sample response 

{"role": "system", "content": "You are a helpful assistant."},
{"role": "user", "content": "Explain asynchronous programming in the style of the pirate Blackbeard."},

{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1694268190,
  "model": "gpt-3.5-turbo-0125",
  "system_fingerprint": "fp_44709d6fcb",
  "choices": [
    {
      "index": 0,
      "delta": {
        "role": "assistant",
        "content": ""
      },
      "logprobs": null,
      "finish_reason": null
    }
  ]
}


"""
from app.utils import accumulate_messages


class TestClass:

    def test_accumulate_messages(self):
        request_body = {
            "model": "internLM2-20B",
            "messages": [
                {"role": "system",
                    "content": "You are a helpful, pattern-following assistant."},
                {"role": "user", "content": "Help me translate the following corporate jargon into plain English."},
                {"role": "assistant", "content": "Sure, I'd be happy to!"},
                {"role": "user", "content": "New synergies will help drive top-line growth."},
                {"role": "assistant",
                 "content": "Things working well together will increase revenue."},
                {"role": "user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
                {"role": "assistant",
                 "content": "Let's talk later when we're less busy about how to do better."},
                {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
            ]
        }
        b = "system: You are a helpful, pattern-following assistant.\nuser: Help me translate the following corporate jargon into plain English.\nassistant: Sure, I'd be happy to!\nuser: New synergies will help drive top-line growth.\nassistant: Things working well together will increase revenue.\nuser: Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage.\nassistant: Let's talk later when we're less busy about how to do better.\nuser: This late pivot means we don't have time to boil the ocean for the client deliverable."
        a = accumulate_messages(request_body["messages"])
        assert a == b
