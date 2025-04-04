import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# langGraph agent / LLM
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools  # é usado para carregar as ferramentas do servidor MCP para serem usadas em agentes de LangChain.
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# Instanciando o modelo
model = ChatOpenAI(model="gpt-4o-mini")

server_params = StdioServerParameters(
    command="python",
    args=[r"STDIO-MCP-Servers\math-server.py"]
)

# Função assíncrona para rodar o código
async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Iniciar Conexão
            await session.initialize()

            # Converter MCP tools para LangChain Tools
            tools = await load_mcp_tools(session)

            # Criar e rodar o agente    
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": "what's (3+5) x 12?"})

            # Exibir resposta do agente
            for m in agent_response['messages']:
                m.pretty_print()

# Rodar a função assíncrona
asyncio.run(run())
