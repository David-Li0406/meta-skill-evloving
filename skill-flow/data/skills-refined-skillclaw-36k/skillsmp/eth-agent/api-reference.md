# eth-agent API Reference

## AgentWallet

### Constructor Options

```typescript
interface AgentWalletConfig {
  // Required
  privateKey: string;           // Hex-encoded private key
  rpcUrl: string;               // Ethereum RPC endpoint

  // Optional - Safety
  limits?: {
    perTransaction?: string;    // Max per single transaction
    perHour?: string;           // Hourly spending cap
    perDay?: string;            // Daily spending cap
    perWeek?: string;           // Weekly spending cap
    emergencyStopBelow?: string; // Halt if balance drops below
  };

  // Optional - Approval
  approvalConfig?: {
    requireApprovalWhen?: {
      amountExceeds?: string;
      recipientIsNew?: boolean;
      recipientNotInTrusted?: boolean;
    };
    trustedAddresses?: string[];
  };
  onApprovalRequired?: (request: ApprovalRequest) => Promise<boolean>;

  // Optional - Address Policy
  addressPolicy?: {
    mode: 'allowlist' | 'blocklist';
    addresses: string[];
  };

  // Optional - ENS
  ensRpcUrl?: string;            // Separate RPC for ENS resolution
}
```

### Methods

#### ETH Operations

```typescript
// Send ETH
wallet.send(options: { to: string; amount: string | bigint }): Promise<TransactionResult>
wallet.safeSend(options): Promise<Result<TransactionResult>>

// Get balance
wallet.getBalance(address?: string): Promise<bigint>
wallet.safeGetBalance(address?: string): Promise<Result<bigint>>

// Preview transaction
wallet.preview(options: { to: string; amount: string }): Promise<TransactionPreview>
```

#### Stablecoin Operations

```typescript
// Send specific stablecoins
wallet.sendUSDC(options: { to: string; amount: string }): Promise<TransactionResult>
wallet.sendUSDT(options: { to: string; amount: string }): Promise<TransactionResult>
wallet.safeSendUSDC(options): Promise<Result<TransactionResult>>
wallet.safeSendUSDT(options): Promise<Result<TransactionResult>>

// Send any stablecoin
wallet.sendStablecoin(options: {
  token: StablecoinInfo;
  to: string;
  amount: string
}): Promise<TransactionResult>

// Get balances
wallet.getStablecoinBalance(token: StablecoinInfo): Promise<string>  // Formatted
wallet.getStablecoinBalances(): Promise<StablecoinBalances>          // All tokens
```

#### Token Operations (Generic ERC-20)

```typescript
wallet.transferToken(options: {
  token: Address;
  to: string;
  amount: string | bigint
}): Promise<TransactionResult>

wallet.getTokenBalance(token: Address, address?: string): Promise<bigint>
```

#### Limits & Approval

```typescript
wallet.getLimits(): Promise<LimitsStatus>
wallet.checkApproval(request: ApprovalRequest): Promise<ApprovalResult>
```

### Properties

```typescript
wallet.address: Address          // Wallet address (readonly)
```

### Payment Watching Methods

```typescript
// Watch for incoming stablecoin payments (returns watcher that can be stopped)
wallet.onStablecoinReceived(
  handler: (payment: IncomingPayment) => void,
  options?: { tokens?: StablecoinInfo[]; pollingInterval?: number }
): PaymentWatcher

// Wait for a specific payment (promise-based)
wallet.waitForPayment(options?: {
  token?: StablecoinInfo;
  minAmount?: string;
  timeout?: number;
}): Promise<IncomingPayment>
```

#### Bridge Operations

```typescript
// Bridge tokens with auto-selected route
wallet.bridge(options: {
  token: StablecoinInfo;
  amount: string;
  destinationChainId: number;
  recipient?: string;
  preference?: RoutePreference;
  protocol?: string;  // Force specific protocol
}): Promise<BridgeResult>

// Safe version - returns Result instead of throwing
wallet.safeBridge(options: BridgeOptions): Promise<Result<BridgeResult>>

// Compare available routes before bridging
wallet.compareBridgeRoutes(options: {
  token: StablecoinInfo;
  amount: string;
  destinationChainId: number;
  preference?: RoutePreference;
}): Promise<BridgeRouteComparison>

// Preview bridge with full validation
wallet.previewBridgeWithRouter(options: {
  token: StablecoinInfo;
  amount: string;
  destinationChainId: number;
  preference?: RoutePreference;
}): Promise<BridgePreview>

// Get status using unified tracking ID
wallet.getBridgeStatusByTrackingId(trackingId: string): Promise<UnifiedBridgeStatus>

// Wait for bridge completion
wallet.waitForBridgeByTrackingId(trackingId: string): Promise<Hex>

// Get minimum bridge amount for a token
wallet.getMinBridgeAmount(token: StablecoinInfo): { raw: bigint; formatted: string; usd: number }

// Legacy direct CCTP methods
wallet.bridgeUSDC(options: { amount: string; destinationChainId: number; recipient?: string }): Promise<BridgeUSDCResult>
wallet.safeBridgeUSDC(options): Promise<Result<BridgeUSDCResult>>
wallet.previewBridgeUSDC(options): Promise<BridgePreviewResult>
wallet.getBridgeStatus(messageHash: Hex): Promise<BridgeStatusResult>
wallet.waitForBridgeAttestation(messageHash: Hex): Promise<Hex>
wallet.getBridgeLimits(): BridgeLimitsStatus
wallet.getBridgeHistory(options?: { hours?: number; limit?: number }): BridgeHistoryEntry[]
```

## SmartAgentWallet

Extends AgentWallet with ERC-4337 smart account capabilities.

### Additional Constructor Options

```typescript
interface SmartAgentWalletConfig extends AgentWalletConfig {
  bundlerUrl: string;            // ERC-4337 bundler endpoint
  paymaster?: Paymaster;         // Optional paymaster for gasless tx
  entryPoint?: Address;          // Custom entry point (default: v0.7)
}
```

### Additional Methods

```typescript
// Gasless transfers (no ETH needed for gas)
smartWallet.sendUSDCGasless(options: { to: string; amount: string }): Promise<UserOpResult>
smartWallet.sendStablecoinGasless(options: {
  token: StablecoinInfo;
  to: string;
  amount: string
}): Promise<UserOpResult>

// Batch transfers (multiple recipients, one transaction)
smartWallet.sendStablecoinBatch(options: {
  token: StablecoinInfo;
  transfers: Array<{ to: string; amount: string }>;
}): Promise<BatchTransferResult>

// Get smart account address (deterministic)
smartWallet.getSmartAccountAddress(): Address
```

## Stablecoins

### Token Objects

```typescript
import { USDC, USDT, USDS, DAI, PYUSD, FRAX } from '@lambdaclass/eth-agent';

interface StablecoinInfo {
  symbol: string;           // e.g., "USDC"
  name: string;             // e.g., "USD Coin"
  decimals: number;         // e.g., 6 for USDC, 18 for DAI
  addresses: {
    [chainId: number]: Address;
  };
}
```

### Utility Functions

```typescript
// Get address for specific chain
getStablecoinAddress(token: StablecoinInfo, chainId: number): Address | undefined

// Get all stablecoins available on a chain
getStablecoinsForChain(chainId: number): StablecoinInfo[]

// Check if address is a known stablecoin
isKnownStablecoin(address: Address): boolean

// Parse/format amounts
parseStablecoinAmount(amount: string | number, decimals: number): bigint
formatStablecoinAmount(raw: bigint, decimals: number): string
```

### Chain IDs

```typescript
// Common chain IDs
const ETHEREUM = 1;
const ARBITRUM = 42161;
const OPTIMISM = 10;
const BASE = 8453;
const POLYGON = 137;
const AVALANCHE = 43114;
```

## Result Type

```typescript
// Creating results
ok<T>(value: T): Ok<T>
err<E>(error: E): Err<E>

// Checking results
isOk<T>(result: Result<T>): result is Ok<T>
isErr<T>(result: Result<T>): result is Err<T>

// Extracting values
unwrap<T>(result: Result<T>): T                    // Throws if Err
unwrapOr<T>(result: Result<T>, defaultValue: T): T // Returns default if Err

// Pattern matching
matchResult(result)
  .ok(value => ...)
  .errWith({ code: 'SPECIFIC_ERROR' }, error => ...)
  .err(error => ...)
  .run()
```

## Error Codes

```typescript
type ErrorCode =
  // Transaction errors
  | 'INSUFFICIENT_FUNDS'
  | 'INSUFFICIENT_GAS'
  | 'NONCE_TOO_LOW'
  | 'TRANSACTION_REVERTED'
  | 'TRANSACTION_UNDERPRICED'

  // Limit errors
  | 'PER_TRANSACTION_LIMIT_EXCEEDED'
  | 'HOURLY_LIMIT_EXCEEDED'
  | 'DAILY_LIMIT_EXCEEDED'
  | 'WEEKLY_LIMIT_EXCEEDED'
  | 'EMERGENCY_STOP_TRIGGERED'

  // Approval errors
  | 'APPROVAL_REQUIRED'
  | 'APPROVAL_DENIED'
  | 'APPROVAL_TIMEOUT'

  // Address errors
  | 'ADDRESS_NOT_ALLOWED'
  | 'ADDRESS_BLOCKED'
  | 'INVALID_ADDRESS'
  | 'ENS_NOT_FOUND'

  // Network errors
  | 'RPC_ERROR'
  | 'NETWORK_ERROR'
  | 'TIMEOUT';
```

## Payment Watching

Payment watching is accessed through AgentWallet methods:

```typescript
// Callback-based watching
const watcher = wallet.onStablecoinReceived(
  (payment) => {
    console.log(`Received ${payment.formattedAmount} ${payment.token.symbol}`);
  },
  { tokens: [USDC, USDT], pollingInterval: 15000 }
);

// Stop when done
watcher.stop();

// Promise-based waiting
const payment = await wallet.waitForPayment({
  token: USDC,
  minAmount: '100',
  timeout: 60000,
});

interface IncomingPayment {
  token: StablecoinInfo;
  from: Address;
  to: Address;
  amount: bigint;
  formattedAmount: string;     // Human-readable
  transactionHash: string;
  blockNumber: number;
}
```

## Units

```typescript
// ETH units
ETH(amount: string | number): bigint    // "1.5" -> 1500000000000000000n
GWEI(amount: string | number): bigint   // "20" -> 20000000000n
WEI(amount: bigint | number): bigint    // passthrough

// Generic parsing
parseUnits(amount: string, decimals: number): bigint
formatUnits(amount: bigint, decimals: number): string
```

## AI Integration Tools

Import from the integrations subpath:

### Anthropic

```typescript
import { anthropicTools } from '@lambdaclass/eth-agent/integrations';

const tools = anthropicTools(wallet);

tools.definitions    // Tool definitions for Claude API
tools.execute(name: string, input: object): Promise<ToolResult>
```

### OpenAI

```typescript
import { openaiTools } from '@lambdaclass/eth-agent/integrations';

const tools = openaiTools(wallet);

tools.definitions    // Function definitions for OpenAI API
tools.execute(name: string, args: object): Promise<ToolResult>
```

### LangChain

```typescript
import { langchainTools } from '@lambdaclass/eth-agent/integrations';

const tools = langchainTools(wallet);
// Returns array of LangChain Tool instances
```

## Paymasters

```typescript
// Remote paymaster (calls external service)
import { createRemotePaymaster } from '@lambdaclass/eth-agent';

const paymaster = createRemotePaymaster({
  url: string;              // Paymaster service URL
  headers?: Record<string, string>;  // Optional auth headers
});

// Verifying paymaster (uses local signer)
import { createVerifyingPaymaster } from '@lambdaclass/eth-agent';

const paymaster = createVerifyingPaymaster({
  address: Address;         // Paymaster contract address
  signer: Signer;           // Signer for paymaster signature
});
```

## Bridge Types

### RoutePreference

```typescript
interface RoutePreference {
  priority: 'speed' | 'cost' | 'reliability';
  maxFeeUSD?: number;           // Maximum total fee
  maxTimeMinutes?: number;      // Maximum bridge time
  maxSlippageBps?: number;      // e.g., 50 = 0.5% max slippage
  preferredProtocols?: string[];
  excludeProtocols?: string[];
}
```

### BridgeQuote

```typescript
interface BridgeQuote {
  protocol: string;
  inputAmount: bigint;
  outputAmount: bigint;       // After fees and slippage
  fee: {
    protocol: bigint;
    gas: bigint;
    total: bigint;
    totalUSD: number;
  };
  slippage?: {
    expectedBps: number;
    maxBps: number;
  };
  estimatedTime: { minSeconds: number; maxSeconds: number; display: string };
  route: {
    sourceChainId: number;
    destinationChainId: number;
    token: string;
    steps: number;
    description: string;
  };
  expiry: Date;
}
```

### BridgeResult

```typescript
interface BridgeResult {
  success: boolean;
  protocol: string;
  trackingId: string;           // Unified tracking ID
  sourceTxHash: Hash;
  amount: { raw: bigint; formatted: string };
  fee: { raw: bigint; formatted: string; usd: number };
  sourceChain: { id: number; name: string };
  destinationChain: { id: number; name: string };
  recipient: Address;
  estimatedTime: { minSeconds: number; maxSeconds: number; display: string };
  summary: string;              // Human-readable summary
  remainingLimits?: {
    perTransaction: bigint;
    daily: bigint;
  };
}
```

### UnifiedBridgeStatus

```typescript
interface UnifiedBridgeStatus {
  trackingId: string;
  protocol: string;
  status: BridgeStatus;         // 'pending_burn' | 'burn_confirmed' | 'attestation_pending' | etc.
  sourceTxHash: Hash;
  amount: { raw: bigint; formatted: string };
  progress: number;             // 0-100
  message: string;              // Human-readable status
  updatedAt: Date;
  error?: string;
}
```

### BridgePreview

```typescript
interface BridgePreview {
  canBridge: boolean;
  blockers: string[];           // Reasons why can't bridge
  quote: BridgeQuote | null;    // Recommended quote
  allQuotes: BridgeQuote[];     // All available quotes
  sourceChain: { id: number; name: string };
  destinationChain: { id: number; name: string };
  amount: { raw: bigint; formatted: string };
  balance: { raw: bigint; formatted: string };
  needsApproval: boolean;
}
```

### Bridge Error Codes

```typescript
type BridgeErrorCode =
  | 'BRIDGE_NO_ROUTE'               // No bridge supports this route
  | 'BRIDGE_QUOTE_EXPIRED'          // Quote expired before execution
  | 'BRIDGE_PROTOCOL_UNAVAILABLE'   // Protocol temporarily down
  | 'BRIDGE_VALIDATION_FAILED'      // Request validation failed
  | 'BRIDGE_INSUFFICIENT_LIQUIDITY' // Not enough liquidity
  | 'BRIDGE_SLIPPAGE_EXCEEDED';     // Slippage exceeds max
```
