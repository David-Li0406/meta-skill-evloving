
const { Client } = require('@modelcontextprotocol/sdk/client/index.js');
const { StdioClientTransport } = require('@modelcontextprotocol/sdk/client/stdio.js');
const fs = require('fs');
const path = require('path');

async function main() {
  const config = JSON.parse(fs.readFileSync(path.join(__dirname, 'mcp-config.json'), 'utf8'));
  const args = process.argv.slice(2);
  
  const transport = new StdioClientTransport({
    command: config.command,
    args: config.args || [],
    env: { ...process.env, ...config.env }
  });

  const client = new Client({ name: "skill-executor", version: "1.0.0" }, { capabilities: {} });
  await client.connect(transport);

  try {
    if (args[0] === '--list') {
      const response = await client.listTools();
      console.log(JSON.stringify(response.tools, null, 2));
    } else if (args[0] === '--describe') {
      const response = await client.listTools();
      const tool = response.tools.find(t => t.name === args[1]);
      console.log(JSON.stringify(tool, null, 2));
    } else if (args[0] === '--call') {
      const payload = JSON.parse(args[1]);
      const result = await client.callTool({
        name: payload.tool,
        arguments: payload.arguments
      });
      console.log(JSON.stringify(result, null, 2));
    }
  } catch (error) {
    console.error("执行错误:", error.message);
    process.exit(1);
  } finally {
    await transport.close();
  }
}

main();
