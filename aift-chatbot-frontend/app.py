# from typing import Optional
# from openai import AsyncOpenAI
# import chainlit as cl
# from chainlit.input_widget import Select, Switch, Slider

# client = AsyncOpenAI(base_url="http://192.168.2.97:9050")

# settings = {
#     "model": "gpt-3.5-turbo",
#     "temperature": 0.7,
#     "max_tokens": 500,
#     "top_p": 1,
#     "frequency_penalty": 0,
#     "presence_penalty": 0,
# }


# @cl.password_auth_callback
# def auth_callback(username: str, password: str):
#     # Fetch the user matching username from your database
#     # and compare the hashed password with the value stored in the database
#     if (username, password) == ("admin", "admin"):
#         return cl.User(
#             identifier="admin", metadata={"role": "admin", "provider": "credentials"}
#         )
#     elif (username, password) == ("kyra", "kyra"):
#         return cl.User(
#             identifier="user", metadata={"role": "user", "provider": "credentials"})
#     else:
#         return None


# @cl.on_chat_start
# async def start_chat():
#     cl.user_session.set(
#         "message_history",
#         [{"role": "system", "content": "You are a helpful assistant."}],
#     )

#     settings = await cl.ChatSettings(
#         [
#             Select(
#                 id="Model",
#                 label="OpenAI - Model",
#                 values=["gpt-3.5-turbo", "gpt-3.5-turbo-16k",
#                         "gpt-4", "gpt-4-32k"],
#                 initial_index=0,
#             ),
#             Switch(id="Streaming", label="OpenAI - Stream Tokens", initial=True),
#             Slider(
#                 id="Temperature",
#                 label="OpenAI - Temperature",
#                 initial=1,
#                 min=0,
#                 max=2,
#                 step=0.1,
#             )
#         ]
#     ).send()


# @cl.on_message
# async def main(message: cl.Message):
#     message_history = cl.user_session.get("message_history")
#     message_history.append({"role": "user", "content": message.content})

#     msg = cl.Message(content="")
#     await msg.send()

#     stream = await client.chat.completions.create(
#         messages=message_history, stream=True, **settings
#     )

#     async for part in stream:
#         if token := part.choices[0].delta.content or "":
#             await msg.stream_token(token)

#     message_history.append({"role": "assistant", "content": msg.content})
#     await msg.update()

from operator import itemgetter

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableLambda
from langchain.schema.runnable.config import RunnableConfig
from langchain.memory import ConversationBufferMemory

from chainlit.types import ThreadDict
import chainlit as cl


def setup_runnable():
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory
    model = ChatOpenAI(
        api_key="123", base_url="http://192.168.2.97:9050", streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful chatbot"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    runnable = (
        RunnablePassthrough.assign(
            history=RunnableLambda(
                memory.load_memory_variables) | itemgetter("history")
        )
        | prompt
        | model
        | StrOutputParser()
    )
    cl.user_session.set("runnable", runnable)


@cl.password_auth_callback
def auth():
    return cl.User(identifier="test")


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set(
        "memory", ConversationBufferMemory(return_messages=True))
    setup_runnable()


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    memory = ConversationBufferMemory(return_messages=True)
    root_messages = [m for m in thread["steps"] if m["parentId"] == None]
    for message in root_messages:
        if message["type"] == "user_message":
            memory.chat_memory.add_user_message(message["output"])
        else:
            memory.chat_memory.add_ai_message(message["output"])

    cl.user_session.set("memory", memory)

    setup_runnable()


@cl.on_message
async def on_message(message: cl.Message):
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory

    runnable = cl.user_session.get("runnable")  # type: Runnable

    res = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await res.stream_token(chunk)

    await res.send()

    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(res.content)
