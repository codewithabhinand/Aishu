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

from chat import ChatAI, HumanMessage, SystemMessage, AssistantMessage
import re
import tool

def Agent(ai_message: str):
    messages = []

    prompt = f"""You have provided with the following tools,
    You are required to thing through the requirements and use the tools in here:

    Tools:

    {tool.tool_str()}

    You are asked to thing through the prompt and use the "Act" action to call the tools.
    """.strip()
    messages.append(SystemMessage(prompt))
    messages.append(HumanMessage(ai_message))

    output = ChatAI(messages=messages)
    content = output['choices'][0]['message']['content']
    
    match = re.search(r"Act: \w+",content)
    val = match.group(0)
    val = val.split(":")
    act_xt = val[-1].strip()

    def Temprature_Extractor():
        return {"temprature":19.8}
    tools = tool.tool_dict()
    
    try:
        value = tools[f"{act_xt}"]
    except:
        value = "No Tool Listed"

    return str(value) + "\n\nKeep the reply small and simple avoid adding thanks for information and things"
    