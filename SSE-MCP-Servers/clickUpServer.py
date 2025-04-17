import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Carrega variáveis do .env
load_dotenv()
CLICKUP_API_KEY = "pk_87967406_5A07ZEGIDJTWGZIYFNW8H5LPIRQMYPDK"
HEADERS = {"Authorization": CLICKUP_API_KEY}

# Inicia o MCP server
mcp = FastMCP("ClickUpAgent", host="127.0.0.3", port="3000")

@mcp.tool()
async def get_workspaces() -> str:
    """Retorna os workspaces disponíveis no ClickUp."""
    async with httpx.AsyncClient() as client:
        res = await client.get("https://api.clickup.com/api/v2/team", headers=HEADERS)
        data = res.json()
        return f"Workspaces: {', '.join(team['name'] for team in data['teams'])}"

@mcp.tool()
async def get_tasks_from_list(list_id: str) -> str:
    """Lista tarefas de uma lista específica."""
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=HEADERS)
        data = res.json()
        tasks = data.get("tasks", [])
        if not tasks:
            return "Nenhuma tarefa encontrada nesta lista."
        return "\n".join([f"- {t['name']}" for t in tasks])

@mcp.tool()
async def create_task_in_list(list_id: str, task_name: str, task_description: str) -> str:
    """Cria uma tarefa nova em uma lista específica."""
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    payload = {
        "name": task_name,
        "description": task_description
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=HEADERS, json=payload)
        if res.status_code in [200, 201]:
            return f"Tarefa '{task_name}' criada com sucesso!"
        return f"Erro: {res.status_code} - {res.text}"
    
async def get_workspaces() -> str:
    """Retorna os workspaces disponíveis no ClickUp."""
    async with httpx.AsyncClient() as client:
        res = await client.get("https://api.clickup.com/api/v2/team", headers=HEADERS)
        data = res.json()
        return f"Workspaces: {', '.join(team['name'] for team in data['teams'])}"

@mcp.tool()
async def get_tasks_from_list(list_id: str) -> str:
    """Lista tarefas de uma lista específica."""
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=HEADERS)
        data = res.json()
        tasks = data.get("tasks", [])
        if not tasks:
            return "Nenhuma tarefa encontrada nesta lista."
        return "\n".join([f"- {t['name']}" for t in tasks])

if __name__ == "__main__":
    mcp.run(transport="sse")