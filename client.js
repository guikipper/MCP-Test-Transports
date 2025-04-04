//Cliente Javascript que conecta ao servidor MCP, com transporte STDIO utilizando Client

import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { ChatOpenAI } from '@langchain/openai';
import { createReactAgent } from '@langchain/langgraph/prebuilt';
import { loadMcpTools } from '@langchain/mcp-adapters';

// Initialize the ChatOpenAI model
const model = new ChatOpenAI({ modelName: 'gpt-4' });

// Create transport for stdio connection
const transport = new StdioClientTransport({
  command: 'python',
  args: ['math_server.py'],
});

// Initialize the client
const client = new Client({
  name: 'math-client',
  version: '1.0.0',
});

try {
  // Connect to the transport
  await client.connect(transport);

  // Get tools
  const tools = await loadMcpTools("math", client);

  // Create and run the agent
  const agent = createReactAgent({ llm: model, tools });
  const agentResponse = await agent.invoke({
    messages: [{ role: 'user', content: "Do you have a phrase for me?" }],
  });
  console.log(agentResponse);
} catch (e) {
  console.error(e);
} finally {
  // Clean up connection
  await client.close();
}