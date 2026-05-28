---
name: bankr-client-patterns
description: Use this skill when you need to implement a Bankr client, create reusable client code, or set up common project files for Bankr API or SDK integrations.
---

# Bankr Client Patterns

Reusable client code and common files for Bankr API and SDK projects.

## bankr-client.ts

The core client module for all Bankr projects:

```typescript
import "dotenv/config";
import { BankrClient } from "@bankr/sdk";

// ============================================
// Validation
// ============================================

if (!process.env.BANKR_PRIVATE_KEY) {
  throw new Error(
    "BANKR_PRIVATE_KEY environment variable is required. " +
      "This wallet pays $0.01 USDC per request (needs USDC on Base)."
  );
}

// ============================================
// Client Setup
// ============================================

/**
 * Bankr Client
 *
 * Provides AI-powered Web3 operations with micropayments.
 * Each API request costs $0.01 USDC (paid from payment wallet on Base).
 *
 * @example
 * ```typescript
 * import { bankrClient } from "./bankr-client";
 *
 * // Token swap
 * const swap = await bankrClient.promptAndWait({
 *   prompt: "Swap 0.1 ETH to USDC on Base",
 * });
 *
 * // Check balances
 * const balances = await bankrClient.promptAndWait({
 *   prompt: "What are my token balances?",
 * });
 * ```
 *
 * @see https://www.npmjs.com/package/@bankr/sdk
 */
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
  richData?: RichData[];
  statusUpdates?: StatusUpdate[];
  error?: string;
  createdAt: string;
  startedAt?: string;
  completedAt?: string;
  cancelledAt?: string;
  processingTime?: number;
  cancellable?: boolean;
}

export interface StatusUpdate {
  message: string;
  timestamp: string;
}

// Transaction types
export type Transaction =
  | SwapTransaction
  | ApprovalTransaction
  | TransferErc20Transaction
  | TransferEthTransaction
  | ConvertEthToWethTransaction
  | ConvertWethToEthTransaction
  | TransferNftTransaction
  | MintManifoldNftTransaction
  | MintSeaDropNftTransaction
  | BuyNftTransaction
  | AvantisTradeTransaction
  | SwapCrossChainTransaction
  | ManageBankrStakingTransaction;

interface BaseTransactionMetadata {
  __ORIGINAL_TX_DATA__: {
    chain: string;
    humanReadableMessage: string;
    inputTokenAddress: string;
    inputTokenAmount: string;
    inputTokenTicker: string;
    outputTokenAddress: string;
    outputTokenTicker: string;
    receiver: string;
  };
  transaction: {
    chainId: number;
    to: string;
    data: string;
    gas: string;
    gasPrice: string;
    value: string;
  };
}

export interface SwapTransaction {
  type: "swap";
  metadata: BaseTransactionMetadata & {
    approvalRequired?: boolean;
    approvalTx?: { to: string; data: string };
    permit2?: object;
  };
}

export interface ApprovalTransaction {
  type: "approval";
  metadata: BaseTransactionMetadata;
}
```