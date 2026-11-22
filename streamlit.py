
from google.antigravity import Agent, LocalAgentConfig
from dotenv import load_dotenv
import os
from tools import *
import asyncio
import streamlit as st

# Start reading from .env file
load_dotenv()

# LocalAgentConfig class is responsible for connecting llm and passing Python functions as a tool.
config = LocalAgentConfig(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-3.5-flash-lite",
    tools=[addNumbers, multiNumbers, subNumbers, divNumbers, saveFile, readFile]
)

# List of tools for AI to execute
available_tools: dict = {
    "addNumbers": addNumbers,
    "multiNumbers": multiNumbers,
    "subNumbers": subNumbers,
    "divNumbers": divNumbers,
    "saveFile": saveFile,
    "readFile": readFile
}


async def callAgent(user_input):

    # Grab the response from Gemini.
    async with Agent(config) as agent:

        response = await agent.chat(user_input)

        agent_reply = ""

        # Check whether AI is using our defined tools or not.
        async for tool in response.tool_calls:

            toolArgs = dict(tool.args)

            agent_reply += f"\nAgent is using tool: {tool.name}\n"
            agent_reply += f"Tool Arguments: {toolArgs}\n"

            result = available_tools.get(tool.name)(**toolArgs)

            agent_reply += f"Agent Reply: {result}\n"

        return agent_reply if agent_reply else str(response)


# Streamlit UI
st.title("🤖 Gemini AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# User input
user_input = st.chat_input("Ask something...")

if user_input:

    if user_input.lower() == "exit":

        st.session_state.messages.append({
            "role": "assistant",
            "content": "Bye Bye"
        })

        st.rerun()

    else:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):

            with st.spinner("Agent is thinking..."):

                response = asyncio.run(callAgent(user_input))

                st.write(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
