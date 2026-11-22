from google.antigravity import Agent,LocalAgentConfig
from dotenv import load_dotenv
import os
from tools import *
import asyncio
#Start reading from .env file
load_dotenv()

#LocalAgentConfig class is responsible for connecting llm and passing Python functions as a tool.
config = LocalAgentConfig(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-3.5-flash-lite",
    tools=[addNumbers,multiNumbers,subNumbers,divNumbers,saveFile,readFile]
)
#list of tools for AI to execute
available_tools:dict ={
    "addNumbers":addNumbers,
    "multiNumbers":multiNumbers,
    "subNumbers":subNumbers,
    "divNumbers":divNumbers,
    "saveFile": saveFile,
    "readFile": readFile
}

async def callAgent():
    #Chat Loop
    while True:
        user_input = input("You:")
        if user_input.lower()=='exit':
            print("Agent: Bye Bye")
            return
        #Grabing the response from Gemini.
        async with Agent(config) as agent:
            response = await agent.chat(user_input)
            #Now we must need to check whether AI is using Our defined tools or not.
            async for tool in response.tool_calls:
                print("Agent is using tool :",tool.name)
                toolArgs = dict(tool.args)
                print("Too Arguments :",toolArgs)
                #Manual checking 
                # if tool.name == "addNumbers":
                #     result = addNumbers(toolArgs.get("a"),toolArgs.get("b"))
                # elif tool.name =="multiNumbers":
                #     result = multiNumbers(toolArgs.get("a"),toolArgs.get("b"))
                result = available_tools.get(tool.name)(**toolArgs)
                print("Agent Reply :",result)

#MainScript from where Python will start to execute the Program.
if __name__ == "__main__":
    asyncio.run(main=callAgent())