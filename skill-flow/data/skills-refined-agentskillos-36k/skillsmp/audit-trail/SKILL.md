---
name: audit-trail
description: Commits transaction hash to immutable AgentDB ledger for complete audit trail of clinical analysis
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I commit a Merkle proof to the AgentDB ledger to create an immutable audit trail. I hash the encrypted payload and store the transaction hash for tamper-evident logging.

## When to use me

Use this when:

- Data encryption is complete and you need to create an audit trail
- You're creating a tamper-evident record of the analysis
- You need to log the transaction for compliance requirements

## Key Concepts

- **Merkle Proof**: Cryptographic proof of data integrity
- **Transaction Hash**: SHA-256 hash of encrypted payload
- **Immutable Ledger**: Append-only storage for audit records
- **audit_logged**: State flag (goal state reached)

## Source Files

- `services/agentDB.ts`: Audit trail implementation
- `services/crypto.ts`: Hash generation

## Code Patterns

- Generate SHA-256 hash of encrypted payload
- Store transaction hash with metadata in AgentDB
- Return confirmation of audit commitment

## Operational Constraints

- Creates immutable record - ensure data is correct before committing
- Transaction hash used for future verification
- This is the final step - audit_logged: true means pipeline complete
