---
name: sigil-signing
description: Sign blockchain transactions using MPC presignatures stored on floppy disks. Requires physical disk insertion for each signature. Use when signing Ethereum transactions, checking disk status, managing presignatures, or working with air-gapped MPC wallets.
allowed-tools: Read, Bash, Glob, Grep
---

# Sigil MPC Signing

Sign blockchain transactions securely using 2-of-2 threshold ECDSA with physical key splitting via floppy disks.

## Quick Start

### 1. Check Daemon Status

```bash
# Verify daemon is running
pgrep -x sigil-daemon || echo "Daemon not running"

# Check socket exists
ls -la /tmp/sigil.sock
```

### 2. Check Disk Status

Before any signing operation, verify the signing disk is inserted and valid:

```bash
# Using the CLI
sigil-cli check-disk

# Or via IPC directly
echo '{"type":"GetDiskStatus"}' | nc -U /tmp/sigil.sock
```

**Expected output when disk is ready:**
```
Disk detected (sigil_7a3f)
├─ Presigs: 847/1000 remaining
└─ Expires: 12 days
```

### 3. Sign a Transaction

```bash
# Sign a transaction hash
sigil-cli sign \
  --hash "0x1234567890abcdef..." \
  --chain-id 1 \
  --description "Transfer 0.1 ETH to vitalik.eth"
```

## Core Workflow

When a user requests a blockchain transaction:

1. **Prepare transaction** - Build the unsigned transaction with proper nonce, gas, etc.
2. **Check disk** - Verify signing disk is inserted and has remaining presigs
3. **Request insertion** - If no disk, prompt user to insert their Sigil floppy
4. **Sign** - Execute signing via the daemon (uses one presignature)
5. **Broadcast** - Submit signed transaction to the network
6. **Log** - Update the disk's usage log with transaction hash

## IPC Protocol

The daemon listens on `/tmp/sigil.sock` using JSON-line protocol.

### Request: Check Disk Status

```json
{"type":"GetDiskStatus"}
```

**Response:**
```json
{
  "type": "DiskStatus",
  "detected": true,
  "child_id": "7a3f",
  "presigs_remaining": 847,
  "presigs_total": 1000,
  "days_until_expiry": 12,
  "is_valid": true
}
```

### Request: Sign Transaction

```json
{
  "type": "Sign",
  "message_hash": "0x1234...abcd",
  "chain_id": 1,
  "description": "Transfer 0.1 ETH"
}
```

**Response:**
```json
{
  "type": "SignResult",
  "signature": "abc123...",
  "presig_index": 153,
  "proof_hash": "def456..."
}
```

### Request: Update TX Hash

After broadcasting, record the actual transaction hash:

```json
{
  "type": "UpdateTxHash",
  "presig_index": 153,
  "tx_hash": "0x8f2a..."
}
```

## Error Handling

| Error | Meaning | Action |
|-------|---------|--------|
| `DaemonNotRunning` | Sigil daemon not started | Run `sigil-daemon` |
| `NoDiskDetected` | No floppy disk inserted | Prompt user to insert disk |
| `DiskExpired` | Presigs have expired | Need new disk from mother device |
| `NoPresigsRemaining` | All presigs consumed | Need new disk from mother device |
| `ReconciliationRequired` | Too many uses since last reconcile | Run reconciliation with mother |
| `InvalidSignature` | Disk signature verification failed | Disk may be corrupted |

## Security Properties

- **Physical consent**: Every signature requires disk insertion
- **Bounded exposure**: Stolen disk = max N signatures (typically 1000)
- **Audit trail**: All operations logged to disk with zkVM proofs
- **Chain isolation**: Chain ID prevents cross-chain replay

## User Interaction Patterns

### Transaction Confirmation

Always show transaction details before signing:

```
Transaction Summary:
├─ To: vitalik.eth (0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045)
├─ Amount: 0.1 ETH (~$370)
├─ Gas: ~21000 (0.0005 ETH / $1.85)
└─ Chain: Ethereum Mainnet

Please insert your signing disk to continue.
```

### Disk Status Display

```
✓ Disk detected (sigil_7a3f)
├─ Presigs: 847/1000 remaining
└─ Expires: 12 days

✓ Signing... ✓ Proving... ✓ Broadcasting...
✓ Confirmed: 0x8f2a...

Logged to disk. You may remove it now.
```

### Low Presig Warning

When presigs drop below 100:

```
⚠️ Warning: Only 87 presignatures remaining.
Consider generating a new disk from your mother device soon.
```

## Reference Documentation

- [REFERENCE.md](REFERENCE.md) - Complete API reference and data structures
- [DAEMON-SETUP.md](DAEMON-SETUP.md) - Daemon installation and configuration

## Supported Chains

| Chain ID | Network |
|----------|---------|
| 1 | Ethereum Mainnet |
| 5 | Goerli Testnet |
| 11155111 | Sepolia Testnet |
| 137 | Polygon |
| 42161 | Arbitrum One |
| 10 | Optimism |
| 8453 | Base |

## Example: Complete Transaction Flow

```python
# Pseudocode for agent transaction handling

async def handle_transfer_request(to_address, amount_eth, chain_id):
    # 1. Check disk status
    disk = await check_disk_status()

    if not disk.detected:
        return prompt_user("Please insert your signing disk.")

    if disk.presigs_remaining < 1:
        return error("No presignatures remaining. Generate new disk.")

    # 2. Build transaction
    tx = build_transaction(to_address, amount_eth, chain_id)

    # 3. Show confirmation
    show_transaction_summary(tx)

    # 4. Sign via daemon
    result = await sign_transaction(tx.hash, chain_id, tx.description)

    # 5. Broadcast
    tx_hash = await broadcast_transaction(tx, result.signature)

    # 6. Update log
    await update_tx_hash(result.presig_index, tx_hash)

    return success(f"Transaction confirmed: {tx_hash}")
```
