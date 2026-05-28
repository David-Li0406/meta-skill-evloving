---
name: shelby-protocol-expert
description: Use this skill when you need expertise in the Shelby Protocol for decentralized blob storage on the Aptos blockchain, including architecture, erasure coding, and SDK integration.
---

# Skill body

## When to Use
- Building decentralized applications (dApps) that require storage solutions.
- Integrating the Shelby SDK (TypeScript/Node.js/Browser).
- Understanding erasure coding and ensuring data durability.
- Working with storage providers and RPC servers.
- Handling high-performance storage needs for video streaming, AI training, and large datasets.

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

### Key Components
- **Aptos Smart Contract**: Manages system state, audits, and settlements.
- **Storage Providers**: Store erasure-coded chunks.
- **RPC Servers**: Provide user-facing API for erasure coding/decoding.
- **Private Network**: Ensures dedicated fiber for internal communication.

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

**Recovery**: Any 10 of 16 chunks can reconstruct the original data.

**Why Clay Codes?**
- Offers the same storage efficiency as Reed-Solomon.
- Requires 4x less bandwidth during recovery.
- Optimal for large-scale distributed storage.

### Blob Naming
Blob names follow the format:

```
<account>/<user-defined-path>
```

**Examples**:
- `0x123.../videos/intro.mp4`
- `0x123.../datasets/training/batch-001.parquet`

- Maximum length: 1024 characters.
- Must NOT end with `/`.
- Flat namespace (no directories, just paths).

## SDK Integration

### Installation
To install the necessary SDKs, run:

```bash
npm install @shelby-protocol/sdk @aptos-labs/ts-sdk
```

### Node.js Client Example
```typescript
import { ShelbyClient } from '@shelby-protocol/sdk';
```