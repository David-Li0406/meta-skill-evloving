import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { AtlasIndexer } from '../core/indexer';
import { AtlasPacker } from '../core/packer';
import { AtlasGuardrails } from '../core/guardrails';

const server = new Server(
  {
    name: 'atlas-mcp',
    version: '1.0.18', // Sync with package
  },
  {
    capabilities: {
      tools: {},
    },
  },
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'atlas_index',
        description: 'Index the repository to update symbols and dependencies.',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'atlas_pack',
        description: 'Create a context pack for a task.',
        inputSchema: {
          type: 'object',
          properties: {
            task: { type: 'string', description: 'The task description' },
            budget: { type: 'number', description: 'Character budget' },
          },
          required: ['task'],
        },
      },
      {
        name: 'atlas_find_duplicates',
        description: 'Find duplicate symbols.',
        inputSchema: {
          type: 'object',
          properties: {
            intent: { type: 'string', description: 'Description of code you want to write' },
          },
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const rootPath = process.cwd(); // MCP server usually runs in the repo root

  switch (request.params.name) {
    case 'atlas_index': {
      const indexer = new AtlasIndexer(rootPath);
      await indexer.index();
      return {
        content: [
          {
            type: 'text',
            text: 'Indexing complete.',
          },
        ],
      };
    }
    case 'atlas_pack': {
      const packer = new AtlasPacker(rootPath);
      const args = request.params.arguments as any;
      const pack = packer.pack({
        task: args.task,
        budget: args.budget || 50000,
        mode: 'feature',
      });
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(pack, null, 2),
          },
        ],
      };
    }
    case 'atlas_find_duplicates': {
      const guard = new AtlasGuardrails(rootPath);
      const args = request.params.arguments as any;
      const results = guard.findDuplicates(args.intent || '');
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(results, null, 2),
          },
        ],
      };
    }
    default:
      throw new Error('Unknown tool');
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
