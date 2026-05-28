---
name: shelby-protocol-expert
description: Use this skill when working with the Shelby Protocol for decentralized blob storage on the Aptos blockchain, including architecture, SDK integration, and erasure coding.
---

# Shelby Protocol Expert

Shelby is a decentralized blob storage network on the Aptos blockchain that utilizes erasure coding, micropayment channels, and dedicated private bandwidth.

## When to Use

- Building decentralized applications (dApps) that require storage solutions
- Integrating the Shelby SDK (TypeScript/Node.js/Browser)
- Understanding erasure coding and data durability
- Working with storage providers and RPC servers
- Handling high-performance storage needs for video streaming, AI training, and large datasets

## Architecture Overview

```
User (Public Internet)
  ↓
Shelby RPC Server (handles blob operations)
  ↓ (Private Fiber Network)
Storage Provider Servers (16 per placement group)
  ↓
Aptos L1 Blockchain (state management)
```

**Key Components:**
- **Aptos Smart Contract** - Manages system state, audits, and settlements
- **Storage Providers** - Store erasure-coded chunks
- **RPC Servers** - Provide user-facing API for erasure coding/decoding
- **Private Network** - Ensures dedicated fiber for internal communication

## Data Model

### Erasure Coding (Clay Codes)

Data is split and encoded for durability:

```
10MB Blob → Split into chunksets → Erasure code each
                                         ↓
                               16 chunks per chunkset
                               (10 data + 6 parity)
                                         ↓
                               Distributed to 16 storage providers
```

**Recovery:** Any 10 of 16 chunks can reconstruct the original data.

**Why Clay Codes?**
- Same storage efficiency as Reed-Solomon
- 4x less bandwidth during recovery
- Optimal for large-scale distributed storage

### Blob Naming

```
<account>/<user-defined-path>

Examples:
0x123.../videos/intro.mp4
0x123.../datasets/training/batch-001.parquet
```

- Max 1024 characters
- Must NOT end with `/`
- Flat namespace (no directories, just paths)

## SDK Integration

### Installation

```bash
npm install @shelby-protocol/sdk @aptos-labs/ts-sdk
```

### Node.js Client

```typescript
import { ShelbyNodeClient } from "@shelby-protocol/sdk/node";
import { Network } from "@aptos-labs/ts-sdk";

const client = new ShelbyNodeClient({
  network: Network.SHELBYNET,
  apiKey: process.env.SHELBY_API_KEY,
});
```

### Browser Client

```typescript
import { ShelbyClient } from "@shelby-protocol/sdk/browser";
import { Network } from "@aptos-labs/ts-sdk";

const client = new ShelbyClient({
  network: Network.SHELBYNET,
  apiKey: process.env.SHELBY_API_KEY,
});
```

## Common Operations

### Upload Blob

```typescript
const result = await client.uploadBlob({
  blobName: "<user-defined-path>",
  data: fileBuffer,
  expirationTimestamp: Date.now() + 30 * 24 * 60 * 60 * 1000, // 30 days
});
```

### Download Blob

```typescript
// Full blob
const data = await client.getBlob("<user-defined-path>");

// Byte range (efficient for large files)
const partial = await client.getBlob("<user-defined-path>", {
  range: { start: 0, end: 1024 },
});
```

### Multipart Upload (Large Files)

For files larger than 10MB:

```typescript
const upload = await client.startMultipartUpload({
  blobName: "<large-file-path>",
  expirationTimestamp: futureTimestamp,
});

for (const [index, part] of fileParts.entries()) {
  await client.uploadPart({
    uploadId: upload.id,
    partNumber: index,
    data: part,
  });
}

await client.completeMultipartUpload({ uploadId: upload.id });
```

### Session Management

Reuse sessions for multiple operations:

```typescript
const session = await client.createSession({
  rpcUrl: "https://api.shelbynet.shelby.xyz/shelby",
  paymentAmount: 1000000, // ShelbyUSD micro-units
});

// Multiple reads on the same session
for (const blobName of blobsToDownload) {
  await client.getBlob(blobName, { session });
}

await session.close();
```

## Token Economics

### Two-Token Model

| Token | Purpose |
|-------|---------|
| **APT** | Blockchain gas fees |
| **ShelbyUSD** | Payments for storage and bandwidth |

### Funding

```bash
# APT from faucet
aptos account fund-with-faucet --profile <your-profile> --amount <amount>

# ShelbyUSD from faucet
# Visit: https://faucet.shelbynet.shelby.xyz
```

## Use Cases

**Ideal Workloads:**
- Video streaming (high bandwidth reads)
- AI training/inference (large datasets)
- Data analytics (read-heavy patterns)
- Content delivery (static assets)
- Archival storage (long-term retention)

**Trade-offs:**
- Optimized for large files (10MB+ chunksets)
- Blobs are immutable (no updates, only overwrites)
- User-pays model (storage + bandwidth)

## Resources

- **Documentation:** https://docs.shelby.cloud
- **Faucet:** https://faucet.shelbynet.shelby.xyz
- **SDK:** `@shelby-protocol/sdk`