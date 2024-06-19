import json
from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        # self.client.get("http://192.168.2.97:9050/")
        self.client.post("http://192.168.2.97:9050/chat/completions", data=json.dumps({
            "model": "internLM2-20B",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful, pattern-following assistant."
                },
                {
                    "role": "user",
                    "content": "hi"
                }
            ],
            "stream": True
        }))
