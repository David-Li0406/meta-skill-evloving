# Sigil API Reference

Complete reference for the Sigil MPC signing system.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Agent                          │
│                         │                                │
│                    sigil-cli                             │
│                         │                                │
│              Unix Socket IPC                             │
│                         ▼                                │
│    ┌────────────────────────────────────────────┐       │
│    │              sigil-daemon                   │       │
│    │  ┌──────────┬──────────────┬────────────┐  │       │
│    │  │DiskWatcher│  AgentStore │   Signer   │  │       │
│    │  └──────────┴──────────────┴────────────┘  │       │
│    └────────────────────────────────────────────┘       │
│                         │                                │
│              Floppy Disk (/media/*/SIGIL*)               │
└─────────────────────────────────────────────────────────┘
```

## Disk Format

The Sigil disk uses a custom binary format on a 1.44MB floppy disk.

### Header Layout (0x0000 - 0x00FF)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0x0000 | 8 | magic | "SIGILDSK" ASCII magic bytes |
| 0x0008 | 4 | version | Format version (currently 1) |
| 0x000C | 32 | child_id | SHA-256 hash of child public key |
| 0x002C | 33 | child_pubkey | Compressed secp256k1 public key |
| 0x004D | 32 | derivation_path | BIP-32 derivation path hash |
| 0x006D | 4 | presig_total | Total presignatures on disk |
| 0x0071 | 4 | presig_used | Number of used presignatures |
| 0x0075 | 8 | created_at | Unix timestamp of creation |
| 0x007D | 8 | expires_at | Unix timestamp of expiry |
| 0x0085 | 8 | reconciliation_deadline | Max time before reconciliation |
| 0x008D | 4 | max_uses_before_reconcile | Usage limit before reconcile |
| 0x0091 | 4 | uses_since_reconcile | Current reconciliation counter |
| 0x0095 | 64 | mother_signature | ECDSA signature from mother |

### Presignature Table (0x0100 - 0x3E8FF)

Each presignature occupies 256 bytes:

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0x00 | 33 | R_point | Compressed EC point (nonce commitment) |
| 0x21 | 32 | k_cold | Cold share of nonce scalar |
| 0x41 | 32 | chi_cold | Cold share of signature scalar |
| 0x61 | 1 | status | 0=Fresh, 1=Used, 2=Voided |
| 0x62 | 158 | reserved | Reserved for future use |

### Usage Log (0x3E900 - EOF)

Variable-length log entries:

```rust
struct UsageLogEntry {
    presig_index: u32,      // Which presig was used
    timestamp: u64,         // When it was used
    message_hash: [u8; 32], // What was signed
    signature: [u8; 64],    // The resulting signature
    chain_id: u32,          // Target blockchain
    tx_hash: [u8; 32],      // Broadcast transaction hash
    zkproof_hash: [u8; 32], // SP1 proof hash
    description_len: u16,   // Length of description
    description: [u8],      // UTF-8 description (max 256 bytes)
}
```

## IPC Protocol

Communication uses Unix domain sockets with JSON-line protocol (one JSON object per line).

### Socket Path

Default: `/tmp/sigil.sock`
Configurable via: `/etc/sigil/daemon.json`

### Request Types

#### Ping

Health check for daemon connectivity.

```json
{"type": "Ping"}
```

**Response:**
```json
{"type": "Pong", "version": "0.1.0"}
```

#### GetDiskStatus

Query current disk state.

```json
{"type": "GetDiskStatus"}
```

**Response (disk present):**
```json
{
  "type": "DiskStatus",
  "detected": true,
  "child_id": "7a3f2b1c",
  "presigs_remaining": 847,
  "presigs_total": 1000,
  "days_until_expiry": 12,
  "is_valid": true
}
```

**Response (no disk):**
```json
{
  "type": "DiskStatus",
  "detected": false,
  "child_id": null,
  "presigs_remaining": null,
  "presigs_total": null,
  "days_until_expiry": null,
  "is_valid": null
}
```

#### Sign

Sign a message hash using a presignature.

```json
{
  "type": "Sign",
  "message_hash": "0x1a2b3c4d5e6f...",
  "chain_id": 1,
  "description": "Transfer 0.1 ETH to alice.eth"
}
```

**Parameters:**
- `message_hash`: Hex-encoded 32-byte hash (keccak256 of RLP-encoded tx)
- `chain_id`: EIP-155 chain identifier
- `description`: Human-readable description (max 256 chars)

**Response (success):**
```json
{
  "type": "SignResult",
  "signature": "abc123def456...",
  "presig_index": 153,
  "proof_hash": "789012345678..."
}
```

**Response (error):**
```json
{
  "type": "Error",
  "message": "No presignatures remaining"
}
```

#### UpdateTxHash

Record the broadcast transaction hash for audit.

```json
{
  "type": "UpdateTxHash",
  "presig_index": 153,
  "tx_hash": "0x8f2a3b4c5d6e..."
}
```

**Response:**
```json
{"type": "Ok"}
```

#### GetPresigCount

Get remaining presignature count.

```json
{"type": "GetPresigCount"}
```

**Response:**
```json
{
  "type": "PresigCount",
  "remaining": 847,
  "total": 1000
}
```

#### ListChildren

List all known child disks.

```json
{"type": "ListChildren"}
```

**Response:**
```json
{
  "type": "ChildList",
  "children": [
    {"child_id": "7a3f2b1c", "last_seen": 1704067200},
    {"child_id": "9e8d7c6b", "last_seen": 1703980800}
  ]
}
```

#### WatchDisk

Stream disk insertion/removal events.

```json
{"type": "WatchDisk"}
```

**Response (streamed):**
```json
{"type": "DiskEvent", "event": "inserted", "child_id": "7a3f2b1c"}
{"type": "DiskEvent", "event": "removed", "child_id": "7a3f2b1c"}
```

## CLI Tool Reference

### sigil-cli check-disk

Check signing disk status.

```bash
sigil-cli check-disk [--json]
```

**Output:**
```
Disk detected (sigil_7a3f)
├─ Presigs: 847/1000 remaining
└─ Expires: 12 days
```

**JSON output:**
```json
{
  "detected": true,
  "disk_id": "7a3f",
  "presigs_remaining": 847,
  "presigs_total": 1000,
  "days_until_expiry": 12,
  "is_valid": true
}
```

### sigil-cli sign

Sign a transaction hash.

```bash
sigil-cli sign \
  --hash <HASH> \
  --chain-id <CHAIN_ID> \
  --description <DESC> \
  [--json]
```

**Arguments:**
- `--hash`: 32-byte hex-encoded message hash (with or without 0x prefix)
- `--chain-id`: EIP-155 chain identifier (1=mainnet, 5=goerli, etc.)
- `--description`: Human-readable transaction description

**Output:**
```
✓ Signing... ✓ Proving... ✓ Done
├─ Signature: 0x1a2b3c...
├─ v: 27
├─ r: 0xabc...
├─ s: 0xdef...
├─ Presig: #153
└─ Proof: 0x789...
```

### sigil-cli update-tx

Update transaction hash after broadcast.

```bash
sigil-cli update-tx \
  --presig-index <INDEX> \
  --tx-hash <HASH>
```

## Rust API (sigil-cli crate)

### SigilClient

```rust
use sigil_cli::client::SigilClient;

// Create client with default socket
let client = SigilClient::new();

// Or with custom socket path
let client = SigilClient::with_socket_path("/custom/path.sock".into());
```

### Methods

```rust
// Health check
let version = client.ping().await?;

// Get disk status
let status = client.get_disk_status().await?;
println!("Presigs: {}/{}", status.presigs_remaining, status.presigs_total);

// Sign a transaction
let result = client.sign(
    "0x1234567890abcdef...",  // message_hash
    1,                         // chain_id
    "Transfer 0.1 ETH"         // description
).await?;

// Update tx hash after broadcast
client.update_tx_hash(result.presig_index, "0x8f2a...").await?;

// Get presig count
let (remaining, total) = client.get_presig_count().await?;
```

### Error Types

```rust
pub enum ClientError {
    ConnectionFailed(String),  // Socket connection error
    DaemonNotRunning,          // Daemon not started
    RequestFailed(String),     // Generic request error
    NoDiskDetected,            // No floppy inserted
    SigningFailed(String),     // Signing operation failed
    Io(std::io::Error),        // I/O error
    Serialization(serde_json::Error), // JSON error
}
```

## Tool Definitions (for Claude)

### SignTransactionTool

```rust
pub struct SignTransactionTool {
    /// Transaction hash (keccak256 of RLP-encoded tx)
    pub transaction_hash: String,

    /// EIP-155 chain ID
    pub chain_id: u32,

    /// Human-readable description
    pub description: String,
}
```

### CheckDiskTool

```rust
pub struct CheckDiskTool {}  // No parameters
```

### EstimateTransactionTool

```rust
pub struct EstimateTransactionTool {
    /// Target address
    pub to: String,

    /// Value in wei
    pub value: String,

    /// Transaction data (optional)
    pub data: Option<String>,

    /// Chain ID
    pub chain_id: u32,
}
```

## Cryptographic Details

### Signature Scheme

- **Algorithm**: ECDSA on secp256k1
- **Key splitting**: 2-of-2 additive secret sharing
- **Nonce generation**: Deterministic with RFC 6979 + random component

### Presignature Protocol

1. **Mother generates**: Random `k`, computes `R = k·G`
2. **Split nonce**: `k = k_cold + k_agent`
3. **Split scalar**: `chi = chi_cold + chi_agent` where `chi = x` (private key)
4. **Cold share to disk**: `(R, k_cold, chi_cold)`
5. **Agent share to daemon**: `(R, k_agent, chi_agent)`

### Signing Completion

```
Input: message_hash z, presig (R, k_cold, chi_cold, k_agent, chi_agent)

1. k = k_cold + k_agent
2. chi = chi_cold + chi_agent
3. r = R.x mod n
4. s = k^(-1) * (z + r * chi) mod n
5. Return (r, s)
```

### zkVM Proof

Each signature generates an SP1 proof attesting:
- Correct presig consumption
- Valid signature computation
- Proper disk state transition

Proof hash is stored in usage log for audit.

## Configuration

### Daemon Config (/etc/sigil/daemon.json)

```json
{
  "agent_store_path": "/var/lib/sigil/agent_store",
  "ipc_socket_path": "/tmp/sigil.sock",
  "enable_zkvm_proving": false,
  "disk_mount_pattern": "/media/*/SIGIL*",
  "signing_timeout_secs": 60,
  "dev_mode": false
}
```

### udev Rules (/etc/udev/rules.d/99-sigil.rules)

```
SUBSYSTEM=="block", KERNEL=="fd*", ACTION=="add", \
  RUN+="/usr/bin/sigil-mount %k"

SUBSYSTEM=="block", KERNEL=="fd*", ACTION=="remove", \
  RUN+="/usr/bin/sigil-unmount %k"
```
