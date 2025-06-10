import os
import requests
from dotenv import load_dotenv
from .auth import fetch_deep_seek_api_key

load_dotenv(override=True)

api_key = os.getenv("OPENROUTER_API_KEY")
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

