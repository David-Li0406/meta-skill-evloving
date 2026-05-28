---
name: bankr-client-sdk-patterns
description: Use this skill when you need to implement a Bankr client or SDK, create common project files, or execute transactions with the Bankr API.
---

# Bankr Client and SDK Patterns

Reusable client code and common files for Bankr API and SDK projects.

## bankr-client.ts

The core API/SDK client module for all Bankr projects:

```typescript
import "dotenv/config";
import { BankrClient } from "@bankr/sdk";

// ============================================
// Validation
// ============================================

if (!process.env.BANKR_API_KEY && !process.env.BANKR_PRIVATE_KEY) {
  throw new Error("BANKR_API_KEY or BANKR_PRIVATE_KEY environment variable is required.");
}

// ============================================
// Client Setup
// ============================================

export const bankrClient = new BankrClient({
  privateKey: process.env.BANKR_PRIVATE_KEY as `0x${string}`,
  walletAddress: process.env.BANKR_WALLET_ADDRESS,
  ...(process.env.BANKR_API_URL && { baseUrl: process.env.BANKR_API_URL }),
});

// Export the wallet address for reference
export const walletAddress = bankrClient.getWalletAddress();

// ============================================
// Types
// ============================================

export type JobStatus = "pending" | "processing" | "completed" | "failed" | "cancelled";

export interface JobStatusResponse {
  success: boolean;
  jobId: string;
  status: JobStatus;
  prompt: string;
  response?: string;
  transactions?: Transaction[];
  error?: string;
  createdAt: string;
}

export type Transaction = {
  type: string;
  metadata: {
    chainId: number;
    to: string;
    data: string;
    value: string;
    gas: string;
  };
};

// ============================================
// API Functions
// ============================================

export async function submitPrompt(prompt: string): Promise<{ jobId: string }> {
  const response = await fetch(`${process.env.BANKR_API_URL}/agent/prompt`, {
    method: "POST",
    headers: {
      "x-api-key": process.env.BANKR_API_KEY,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${await response.text()}`);
  }

  return response.json();
}

export async function getJobStatus(jobId: string): Promise<JobStatusResponse> {
  const response = await fetch(`${process.env.BANKR_API_URL}/agent/job/${jobId}`, {
    headers: { "x-api-key": process.env.BANKR_API_KEY },
  });

  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${await response.text()}`);
  }

  return response.json();
}

export async function executeTransaction(tx: Transaction): Promise<string> {
  const client = createWalletClient(tx.metadata.chainId);
  const hash = await client.sendTransaction({
    to: tx.metadata.to,
    data: tx.metadata.data,
    value: BigInt(tx.metadata.value),
    gas: BigInt(tx.metadata.gas),
  });

  return hash;
}
```

## Common Files

### package.json

Base package.json for all Bankr projects:

```json
{
  "name": "{project-name}",
  "version": "0.1.0",
  "description": "{description}",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts"
  },
  "dependencies": {
    "dotenv": "^16.3.1",
    "@bankr/sdk": "^1.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "tsx": "^4.7.0",
    "typescript": "^5.3.0"
  }
}
```

### tsconfig.json

TypeScript configuration:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### .env.example

Environment variables template:

```bash
# Bankr API/SDK Configuration
BANKR_API_KEY=bk_your_api_key_here
BANKR_PRIVATE_KEY=0x...
BANKR_WALLET_ADDRESS=0x...
BANKR_API_URL=https://api.bankr.bot
```

### .gitignore

Standard ignore patterns:

```
# Dependencies
node_modules/

# Build output
dist/

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
npm-debug.log*

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
```

## Usage Patterns

### Basic Usage

```typescript
import { bankrClient } from "./bankr-client";

const result = await bankrClient.promptAndWait({
  prompt: "What is the price of ETH?",
  onStatusUpdate: (msg) => console.log("Progress:", msg),
});

console.log(result.response);
```

### With Transaction Execution

```typescript
import { bankrClient } from "./bankr-client";
import { executeTransaction } from "./executor";

const result = await bankrClient.promptAndWait({
  prompt: "Swap 0.1 ETH to USDC on Base",
});

if (result.status === "completed" && result.transactions?.length) {
  const hash = await executeTransaction(result.transactions[0]);
  console.log("Executed:", hash);
}
```

### With Error Handling

```typescript
import { bankrClient } from "./bankr-client";

async function performSwap(prompt: string) {
  try {
    const result = await bankrClient.promptAndWait({ prompt });
    if (result.status === "completed") {
      console.log("Success:", result.response);
    } else if (result.status === "failed") {
      console.error("Failed:", result.error);
    }
  } catch (error) {
    console.error("Error:", error.message);
  }
}
```

## API Reference

Consult the `bankr-api-basics` skill for:
- Complete endpoint documentation
- Authentication details
- Response field descriptions
- Error codes and handling

Consult the `sdk-capabilities` skill for:
- Complete operation reference
- Supported chains and tokens
- Example prompts for each operation