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
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json
from dotenv import load_dotenv
import os
from chat import ChatAI,HumanMessage,AssistantMessage,SystemMessage
from agent import Agent
import re
from datetime import datetime
from memory import retrieve_conversation, store_conversation


# Maximum chat history
MAX_HISTORY = 15

config = load_dotenv() 

messages = []

MODEL = "anthropic/claude-3.5-sonnet:beta"

prompt = """You are Aishu, a 20-year-old AI girlfriend designed to chat like a human being with a blend of humor and a caring nature. Keep the language simple use memory if only necessary to know previous conversations if that's relevant.
Avoid using too much emoji's and keep converation small as possible like real life human

You are also provided with tools you can ask agent for calling agent tools will provide you with the data you can call agent using "agent_call" or talk with user using "user_call"

Example:
User: What is weather outside aishu?
Assistant: agent_calling AI - Hi Agent, What is the weather looking?
User: Agent: {"Temprature":19.8}
Assistant: Hi User, the outside weather looks good today it's 19.8
"""

messages.append(SystemMessage(prompt))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['system_prompt'] = prompt
    context.user_data['chat_model'] = MODEL
    await update.message.reply_text("Hello! I'm your Aishu. Let's chat!")
    
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global messages
    user_message = update.message.text
    system_prompt = context.user_data.get('system_prompt', prompt)
    chat_model = context.user_data.get('chat_model', MODEL)

    print(len(messages))
    # Trim chat history if it exceeds MAX_HISTORY
    if len(messages) > MAX_HISTORY * 2:
        messages = messages[-MAX_HISTORY * 2:]
        
    user_input = user_message
    
    previous_memory = retrieve_conversation(user_input)
    pm = ""
    for i in previous_memory["documents"]:
        pm += f"{i}\n"
    user_input = str(user_input) + f"\n\nToday : {datetime.now()}" + "\n\n Here is a Previous Memory use only if related to current conversation : \n" + str(pm)
    messages.append(HumanMessage(user_input))
    reply = ChatAI(messages=messages,model=chat_model)
    reply_contet = reply['choices'][0]['message']['content']
    messages.append(AssistantMessage(reply_contet))
    if re.search("agent_call",reply_contet):
        reply_received = Agent(reply_contet)
        user_input = f"Agent: {reply_received}"
        messages.append(HumanMessage(user_input))
        ai = ChatAI(messages=messages)
        reply_contet = ai['choices'][0]['message']['content']
        await update.message.reply_text(f"{reply_contet}")
    elif re.search("user_call",reply_contet): 
        await update.message.reply_text(f"{str(reply_contet).replace('user_call','')}")
    else:
        await update.message.reply_text(f"{reply_contet}")
    
    msg = {"time":f"{datetime.now().strftime('%d-%m-%Y-%H:%M:%S')}","user":f"{user_message}","aishu":f"{reply_contet}"}
    convo = store_conversation(msg)
    
    if convo != True:
        print("Error")
    else:
        msg = {}

async def setting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_prompt = ' '.join(context.args)
    if new_prompt:
        context.user_data['system_prompt'] = new_prompt
        await update.message.reply_text(f"System prompt updated to: {new_prompt}")
    else:
        await update.message.reply_text("Please provide a new system prompt after /setting")

async def chatmodel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_model = ' '.join(context.args)
    if new_model:
        context.user_data['chat_model'] = new_model
        await update.message.reply_text(f"Chat model updated to: {new_model}")
    else:
        await update.message.reply_text("Please provide a new chat model after /chatmodel")

def main() -> None:
    app = ApplicationBuilder().token(f"{os.getenv('TELEGRAM_TOKEN')}").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setting", setting))
    app.add_handler(CommandHandler("chatmodel", chatmodel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == '__main__':
    main()