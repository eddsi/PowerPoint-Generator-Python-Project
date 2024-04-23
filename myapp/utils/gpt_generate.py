import os

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def chat_development(user_message):
    conversation = build_conversation(user_message)
    try:
        assistant_message = generate_assistant_message(conversation)
    except openai.error.RateLimitError as e:
        assistant_message = "Rate limit exceeded. Sleeping for a bit..."

    return assistant_message


def build_conversation(user_message):
    return [
        {"role": "system",
         "content": "你是一个提供幻灯片演示想法的助手。回答时，请根据幻灯片的数量为每张幻灯片提供总结内容。答案的格式必须是“Slide X（幻灯片编号）：{内容标题} /n Content：/n 带有一些要点的内容。”“Keyword：/n 提供代表每张幻灯片的最重要的关键词（两个词以内）。”"},
        {"role": "user", "content": user_message}
    ]


def generate_assistant_message(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    return response['choices'][0]['message']['content']
