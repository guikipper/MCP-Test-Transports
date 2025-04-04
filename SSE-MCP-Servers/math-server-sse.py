#Servidor MCP feito em FastMCP com transporte SSE

from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math-SSE", host="127.0.0.2", port="3000")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return "It's always sunny in New York"

@mcp.tool()
def ask_sentence() -> str:
    return "Continue fazendo um ótimo trabalho, da equipe do Math-SSE!"

if __name__ == "__main__":
    mcp.run(transport="sse")