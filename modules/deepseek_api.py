# modules/deepseek_api.py
import os
from dotenv import load_dotenv
from openai import OpenAI

def query_deepseek(user_input: str, persona: str, context: list):
    """
    向 DeepSeek API 发送请求。
    persona: 学科人格提示词
    context: 上下文摘要列表
    """
    messages = [{"role": "system", "content": persona}]
    for ctx in context:
        messages.append({"role": "user", "content": ctx["question"]})
        messages.append({"role": "assistant", "content": ctx["answer"]})
    messages.append({"role": "user", "content": user_input})

    client = OpenAI(
        api_key="sk-c6288fcc0af5417091e8600660ab185e",
        base_url="https://api.deepseek.com"
    )

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.4,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ DeepSeek API 调用失败：{e}"
