"""
    Aishu AI Chatbot
    Copyright (C) 2024  Abhinand Dhandapani

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import requests
import json
from dotenv import load_dotenv
import os


config = load_dotenv()
MODEL = "anthropic/claude-3.5-sonnet:beta"

def ChatAI(model=MODEL,messages=None) -> dict:
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": f"{os.getenv('YOUR_SITE_URL')}", # Optional, for including your app on openrouter.ai rankings.
        "X-Title": f"{os.getenv('YOUR_APP_NAME')}", # Optional. Shows in rankings on openrouter.ai.
    },
    data=json.dumps({
        "model": model, # Optional
        "messages": messages
        
    })
    )

    return response.json()

def HumanMessage(content: str):
    return {"role":"user","content":content}

def AssistantMessage(content: str):
    return {"role":"assistant","content":content}

def SystemMessage(content: str):
    return {"role":"system","content":content}
