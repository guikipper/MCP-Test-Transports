#Servidor MCP feito em FastMCP com transporte SSE

from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather", host="127.0.0.1", port="3000")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return "It's always sunny in New York"

@mcp.tool()
def ask_phrase() -> str:
    return "Continue fazendo um ótimo trabalho, da equipe do Weather Service!"

if __name__ == "__main__":
    mcp.run(transport="sse")