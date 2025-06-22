from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import asyncio

# 1) load your .env first so that os.getenv can see GROQ_API_KEY
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY") or ""

async def main():
    client = MultiServerMCPClient({
        "math": {
            "command": "uv",
            "args": ["run","mathserver.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    }) # type: ignore[arg-type]

    # fetch the tool definitions
    tools = await client.get_tools()

    # create a Groq‐backed chat model
    model = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

    # wrap it in a REACT‐style agent with those tools
    agent = create_react_agent(model, tools=tools)

    # *** note the key is "messages" here, not "message" ***
    math_response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "What's (2 + 2) multiplied by 15?"}
        ]
    })

    # and when you print, pull from 'messages' as well
    print("Math response:", math_response["messages"][-1].content)

    weather_response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "What's the weather in Tokyo?"}
        ]
    })
    print("Weather response:", weather_response["messages"][-1].content)

asyncio.run(main())
