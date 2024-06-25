
from __future__ import annotations
import uvicorn
from utils import stream_generator, stream_generator_general_chatting
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import os
import signal
from pydantic import BaseModel
import json
from fastapi import Body, FastAPI, Response
from typing import Any, Dict, List, Optional, Annotated
from pydantic import ValidationError, BaseModel
from sse_starlette.sse import EventSourceResponse


app = FastAPI()

#  WARNING:  Invalid HTTP request received. is due to https, you should use http
#  400 BAD REQUEST is due to CORS, examples as follows
origins = [
    "http://192.168.2.97",
    "http://192.168.2.95",
    "http://localhost:3001",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello():
    return {"message": "Hello World"}


async def test_ss_generator():
    for s in "test event stream":
        yield f"event: locationUpdate\ndata: {s}\n\n"


@app.get("/test/ss")
async def test_ss():
    return StreamingResponse(test_ss_generator(), media_type="text/event-stream")


class Message(BaseModel):
    role: str
    content: str


class ChatCompletion(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = None


@app.post('/vercel/chat/completions')
def vercel_chat_completions(request_body: Annotated[Dict[Any, Any],  Body(
    openapi_examples={
        "default": {
            "summary": "streaming",
            "value": {
                "model": "internLM2-20B",
                "messages": [
                    {"role": "system",
                     "content": "You are a helpful, pattern-following assistant."},
                    {"role": "user", "content": "who are you"}
                ],
                "stream": True
            }},
        "normal": {
            "summary": "non streaming",
            "value": {
                "model": "internLM2-20B",
                "messages": [
                    {"role": "system",
                     "content": "You are a helpful, pattern-following assistant."},
                    {"role": "user", "content": "Help me translate the following corporate jargon into plain English."}
                ],
            }}
    }
)]):
    try:
        stream = request_body.get('stream', True)
        if stream:
            # Somehow openai library only accepts EventSourceResponse
            return EventSourceResponse(stream_generator_general_chatting(request_body))
            # return StreamingResponse(stream_generator(json.loads(request_body.model_dump_json())), media_type='text/plain')
        else:
            # return JSONResponse(content=make_response_json(prompt))
            return "Not Implemented"
    except ValidationError as e:
        print(e.errors())


@app.post('/chat/completions')
@app.post('/v1/chat/completions')
def chat_completions(request_body: Annotated[ChatCompletion, Body(
    openapi_examples={
        "default": {
            "summary": "streaming",
            "value": {
                "model": "internLM2-20B",
                "messages": [
                    {"role": "system",
                     "content": "You are a helpful, pattern-following assistant."},
                    {"role": "user", "content": "你们有哪些拖把的品牌"}
                ],
                "stream": True
            }},
        "normal": {
            "summary": "non streaming",
            "value": {
                "model": "internLM2-20B",
                "messages": [
                    {"role": "system",
                     "content": "You are a helpful, pattern-following assistant."},
                    {"role": "user", "content": "Help me translate the following corporate jargon into plain English."}
                ],
            }}
    }
)]):
    try:
        print('request_body', request_body)
        stream = request_body.stream
        if stream:
            # Somehow openai library only accepts EventSourceResponse
            return EventSourceResponse(stream_generator(json.loads(request_body.model_dump_json())))
            # return StreamingResponse(stream_generator(json.loads(request_body.model_dump_json())), media_type='text/plain')
        else:
            # return JSONResponse(content=make_response_json(prompt))
            return "Not Implemented"
    except ValidationError as e:
        print(e.errors())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9050)
