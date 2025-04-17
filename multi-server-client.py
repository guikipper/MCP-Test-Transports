#Client que utiliza MultiServerMCPClient para conectar ao servidor MCP
#Permite conectar à vários servidores MCP por vez
#Problemas na conexão do STDIO (sem solução até o momento)

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import os

CLICKUP_API_KEY="pk_87967406_5A07ZEGIDJTWGZIYFNW8H5LPIRQMYPDK"
CLICKUP_TEAM_ID="9013593366"

model = ChatOpenAI(model="gpt-4o-mini")

async def main():
    
    servers_config = {
            "ClickUp": {
                "command": "npx",
                "args": [ 
                    "-y",
                    "@taazkareem/clickup-mcp-server@latest"],
                "env": {
                    "CLICKUP_API_KEY":CLICKUP_API_KEY,
                    "CLICKUP_TEAM_ID":CLICKUP_TEAM_ID,
                },
                "transport": "stdio",
            },
        }
   
    async with MultiServerMCPClient(servers_config) as client:
        tools = client.get_tools()
        agent = create_react_agent(model, tools)
        response = await agent.ainvoke({"messages": "Me retorne todas as tools"})
        print(response)

if __name__ == "__main__":
    asyncio.run(main())


