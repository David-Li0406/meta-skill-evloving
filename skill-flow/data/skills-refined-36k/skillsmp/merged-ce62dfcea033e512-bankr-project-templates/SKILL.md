---
name: bankr-project-templates
description: Use this skill when you need to scaffold a Bankr project, create a new Bankr bot, build a Bankr web service, create a Bankr dashboard, or develop a Bankr CLI tool.
---

# Bankr Project Templates

Directory structures and templates for Bankr API and SDK projects.

## Available Templates

| Template | Use Case | Key Features |
|----------|----------|--------------|
| **bot** | Automated tasks | Polling loop, scheduler, transaction execution |
| **web-service** | HTTP APIs | REST endpoints, async handling, webhook support |
| **dashboard** | Web UIs | Frontend + backend, portfolio display |
| **cli** | Command-line tools | Subcommands, interactive prompts |

## Bot Template

For automated trading bots, price monitors, portfolio rebalancers, and scheduled tasks.

### Directory Structure

```
{project-name}/
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── index.ts           # Main entry point with scheduler
│   ├── bankr-client.ts    # Bankr API/SDK client
│   ├── executor.ts        # Transaction execution
│   ├── types.ts           # TypeScript interfaces
│   └── config.ts          # Configuration loading
└── scripts/
    └── run.sh             # Convenience script
```

### Key Features

- **Polling loop**: Configurable interval for recurring operations
- **Transaction execution**: Built-in integration for sending transactions
- **Status streaming**: Real-time job progress updates
- **Error handling**: Automatic retries with backoff
- **Graceful shutdown**: Handles SIGINT/SIGTERM

### Use Cases

- Price monitoring and alerts
- Automated swap strategies
- Portfolio rebalancing
- Scheduled market analysis
- DCA-like automation

### Entry Point Pattern (index.ts)

```typescript
import { bankrClient } from "./bankr-client";
import { executeTransaction } from "./executor";

const INTERVAL = 60000; // 1 minute

async function runBot() {
  console.log("Starting Bankr bot...");

  while (true) {
    try {
      const result = await bankrClient.promptAndWait({
        prompt: "Check ETH price",
        onStatusUpdate: (msg) => console.log("Status:", msg),
      });

      if (result.status === "completed") {
        console.log("Result:", result.response);

        // Execute transactions if returned
        if (result.transactions?.length) {
          for (const tx of result.transactions) {
            await executeTransaction(tx);
          }
        }
      }
    } catch (error) {
      console.error("Error:", error);
    }

    await new Promise((r) => setTimeout(r, INTERVAL));
  }
}

runBot();
```

## Web Service Template

For HTTP APIs that wrap Bankr functionality for mobile apps or integrations.

### Directory Structure

```
{project-name}/
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── index.ts           # Server entry point
│   ├── server.ts          # Express/Fastify server setup
│   ├── routes/
│   │   ├── health.ts      # Health check endpoint
│   │   ├── swap.ts        # Swap endpoints
│   │   └── portfolio.ts   # Portfolio endpoints
│   ├── bankr-client.ts    # Bankr API/SDK client
│   ├── types.ts           # TypeScript interfaces
│   └── config.ts          # Configuration loading
└── scripts/
    └── run.sh
```

### Key Features

- **REST API endpoints**: Clean API design
- **Request validation**: Input sanitization
- **Async handling**: Non-blocking operations
- **Rate limiting**: Prevent abuse
- **CORS**: Cross-origin support

### Use Cases

- API gateway for Bankr
- Mobile app backend
- Trading API for integrations
- Webhook-driven automation

### Additional Dependencies

```json
{
  "dependencies": {
    "express": "^4.18.0"
  }
}
```

## Dashboard Template

For web UIs with portfolio tracking, swap interfaces, or monitoring.

### Directory Structure

```
{project-name}/
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
├── server/
│   ├── index.ts           # Backend server
│   ├── bankr-client.ts    # Bankr API/SDK client
│   ├── routes/
│   │   └── api.ts         # API routes for frontend
│   └── types.ts
├── public/
│   ├── index.html         # Main HTML page
│   ├── styles.css         # Basic styles
│   └── app.js             # Frontend JavaScript
└── scripts/
    └── run.sh
```

### Key Features

- **Simple frontend**: HTML/CSS/JS (no build step required)
- **Backend API**: Express server for Bankr operations
- **Portfolio display**: Token balances and values
- **Swap interface**: Execute swaps through UI

### Use Cases

- Portfolio tracking dashboard
- Personal trading interface
- Market monitoring
- Position management

## CLI Template

For command-line tools with subcommands and interactive features.

### Directory Structure

```
{project-name}/
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── index.ts           # CLI entry with commander.js
│   ├── commands/
│   │   ├── swap.ts        # Swap commands
│   │   ├── balance.ts     # Balance query commands
│   │   └── send.ts        # Transfer commands
│   ├── bankr-client.ts    # Bankr API/SDK client
│   ├── executor.ts        # Transaction execution
│   └── types.ts
└── scripts/
    └── run.sh
```

### Key Features

- **Commander.js**: CLI framework with subcommands
- **Interactive prompts**: User input when needed
- **Progress indicators**: Status during SDK calls
- **Colored output**: Better UX
- **Transaction confirmation**: Review before execute

### Use Cases

- Personal trading tool
- Scripting and automation
- Quick balance checks
- Batch swap operations

### Additional Dependencies

```json
{
  "dependencies": {
    "commander": "^12.0.0"
  }
}
```

### CLI Pattern (index.ts)

```typescript
import { program } from "commander";
import { swap } from "./commands/swap";
import { balance } from "./commands/balance";

program
  .name("bankr-cli")
  .description("CLI for Bankr operations")
  .version("1.0.0");

program
  .command("balance")
  .description("Get wallet balances")
  .action(balance);

program
  .command("swap <amount> <from> <to>")
  .description("Swap tokens")
  .option("-c, --chain <chain>", "Target chain", "base")
  .option("-y, --yes", "Skip confirmation")
  .action(swap);

program.parse();
```

## Choosing a Template

| Need | Recommended Template |
|------|---------------------|
| Automated recurring tasks | **bot** |
| HTTP API for mobile/web | **web-service** |
| Visual interface | **dashboard** |
| Terminal-based tool | **cli** |
| Price alerts | **bot** |
| Portfolio viewer | **dashboard** |
| Quick trades | **cli** |

## Common Files

All templates share common files. Load the appropriate client patterns for:
- `bankr-client.ts` - Complete API/SDK client
- `executor.ts` - Transaction execution
- `package.json` - Base dependencies
- `tsconfig.json` - TypeScript config
- `.env.example` - Environment template
- `.gitignore` - Standard ignores

## Next Steps After Scaffolding

1. **Install dependencies**: `bun install` or `npm install`
2. **Configure API key**: Copy `.env.example` to `.env` and add `BANKR_API_KEY` or `BANKR_PRIVATE_KEY`
3. **Customize**: Modify the template for your use case
4. **Run**: `bun dev` or `npm run dev` for development
5. **Build**: `bun run build` or `npm run build` for production