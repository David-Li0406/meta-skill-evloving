---
name: shelby-protocol-expert
description: Use this skill when working with the Shelby Protocol for decentralized blob storage on the Aptos blockchain, including erasure coding, SDK integration, and storage management.
---

# Shelby Protocol Expert

Shelby is a decentralized blob storage network on the Aptos blockchain that utilizes erasure coding, micropayment channels, and dedicated private bandwidth.

## When to Use

- Building decentralized applications (dApps) that require storage solutions
- Integrating the Shelby SDK (TypeScript/Node.js/Browser)
- Understanding erasure coding and data durability
- Collaborating with storage providers and RPC servers
- Handling workloads such as video streaming, AI training, and large datasets

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
<blob_size> Blob → Split into chunksets → Erasure code each
                                         ↓
                               <number_of_chunks> chunks per chunkset
                               (<data_chunks> data + <parity_chunks> parity)
                                         ↓
                               Distributed to <number_of_providers> storage providers
```

**Recovery:** Any `<data_chunks>` of `<number_of_chunks>` can reconstruct the data.

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
  blobName: "<user_defined_path>",
  data: <file_buffer>,
  expirationTimestamp: Date.now() + <duration>, // e.g., 30 days
});
```

### Download Blob

```typescript
// Full blob
const data = await client.getBlob("<user_defined_path>");

// Byte range (efficient for large files)
const partial = await client.getBlob("<user_defined_path>", {
  range: { start: 0, end: <byte_range_end> },
});
```

### Multipart Upload (Large Files)

For files larger than 10MB:

```typescript
const upload = await client.startMultipartUpload({
  blobName: "<large_file_name>",
  expirationTimestamp: <future_timestamp>,
});

for (const [index, part] of <file_parts>.entries()) {
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
  rpcUrl: "<rpc_url>",
  paymentAmount: <payment_amount>, // in micro-units
});

// Multiple reads on the same session
for (const blobName of <blobs_to_download>) {
  await client.getBlob(blobName, { session });
}

await session.close();
```

## Token Economics

### Two-Token Model

| Token | Purpose |
|-------|---------|
| **APT** | Blockchain gas fees |
| **ShelbyUSD** | Storage and bandwidth payments |

### Funding

```bash
# APT from faucet
aptos account fund-with-faucet --profile <profile_name> --amount <amount>

# ShelbyUSD from faucet
# Visit: <faucet_url>
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
- Blobs are immutable (no updates, only overwrite)
- User-pays model (storage + bandwidth)

## Resources

- **Documentation:** https://docs.shelby.cloud
- **Faucet:** https://faucet.shelbynet.shelby.xyz
- **SDK:** `@shelby-protocol/sdk`