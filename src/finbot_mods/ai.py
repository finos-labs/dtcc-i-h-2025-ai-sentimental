import os
import requests
from dotenv import load_dotenv
from .auth import fetch_deep_seek_api_key
from .db_init import db
from .web_init import run_rag_query

api_key = fetch_deep_seek_api_key()

def ask_deepseek(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",  # Or your domain
        "X-Title": "DeepSeek Chat"
    }

    body = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"
    

from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import create_sql_agent

def ask_langchain_db(prompt):
    llm = init_chat_model("us.anthropic.claude-3-5-sonnet-20240620-v1:0", model_provider="bedrock_converse")
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    res = agent_executor.invoke({"input": prompt})
    return res["output"][0]["text"]