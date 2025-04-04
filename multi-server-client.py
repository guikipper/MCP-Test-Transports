#Client que utiliza MultiServerMCPClient para conectar ao servidor MCP
#Permite conectar à vários servidores MCP por vez
#Problemas na conexão do STDIO (sem solução até o momento)

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import sys

async def main():
    model = ChatOpenAI(model="gpt-4o-mini")
    servers_config = {
        "math": { 
          "command": "python",
          "args": [r"STDIO-MCP-Servers\math-server.py"],
          "transport": "stdio",
       },
    }
        #"math-SSE": {
        #    # make sure you start your weather server on port 8000
        #    "url": "http://127.0.0.2:3000/sse",
        #    "transport": "sse",
        #},

        #       "weather": {
        #    # make sure you start your weather server on port 8000
        #    "url": "http://127.0.0.1:3000/sse",
        #    "transport": "sse",
        #},
   
    async with MultiServerMCPClient(servers_config) as client:
        tools = client.get_tools()
        agent = create_react_agent(model, tools)
        response = await  agent.ainvoke({"messages": "What is 35+4"})
        print(response)

if __name__ == "__main__":
    asyncio.run(main())


