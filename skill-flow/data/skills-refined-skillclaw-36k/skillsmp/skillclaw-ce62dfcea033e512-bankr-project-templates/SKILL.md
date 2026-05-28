---
name: bankr-project-templates
description: Use this skill when you need to scaffold a Bankr project, create a new Bankr bot, build a Bankr web service, or set up a Bankr CLI tool, with guidance on directory structures and templates for different types of Bankr API and SDK integrations.
---

# Bankr Project Templates

Directory structures and templates for Bankr API and SDK projects.

## Available Templates

| Template | Use Case | Key Features |
|----------|----------|--------------|
| **bot** | Automated tasks | Polling loop, scheduler, transaction execution, status streaming |
| **web-service** | HTTP APIs | REST endpoints, async handling, webhook support |
| **dashboard** | Web UIs | Frontend + backend, real-time updates, portfolio display |
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
│   ├── executor.ts        # Transaction execution (if applicable)
│   ├── types.ts           # TypeScript interfaces
│   └── config.ts          # Configuration loading
└── scripts/
    └── run.sh             # Convenience script
```

### Key Features

- **Polling loop**: Configurable interval for recurring checks or operations
- **Transaction execution**: Built-in support for sending transactions (if applicable)
- **Status streaming**: Real-time job status updates
- **Error handling**: Automatic retries with backoff
- **Graceful shutdown**: Handles SIGINT/SIGTERM

### Use Cases

- Price monitoring and alerts
- Automated trading strategies
- Portfolio rebalancing
- Scheduled market analysis
- DCA automation

### Entry Point Pattern (index.ts)

```typescript
import { bankrClient } from "./bankr-client";
import { executeTransaction } from "./executor"; // Optional, if applicable

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
        // Add your logic here
      }
    } catch (error) {
      console.error("Error:", error);
    }

    await new Promise(r => setTimeout(r, INTERVAL));
  }
}

runBot();
```