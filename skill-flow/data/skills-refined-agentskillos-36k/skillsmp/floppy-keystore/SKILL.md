---
name: floppy-keystore
description: Manage encrypted multi-chain cryptocurrency keys stored on floppy disks. Supports Ethereum, Bitcoin, Zcash, Monero, and Solana. Use when working with floppy disk keystores, deriving keys for multiple blockchains, mounting/unmounting floppy drives, or configuring secure air-gapped key storage. One mnemonic, all chains.
allowed-tools: Read, Bash, Glob, Grep
---

# Floppy Disk Keystore Skill

Multi-chain cryptocurrency key management using physical floppy disks for air-gapped storage.

## Overview

This skill enables secure management of encrypted cryptographic keys stored on floppy disks. A single BIP-39 mnemonic phrase can derive keys for multiple blockchain networks:

| Chain | Symbol | Curve | Networks |
|-------|--------|-------|----------|
| Ethereum | ETH | secp256k1 | mainnet, sepolia, arbitrum, optimism, polygon, base |
| Bitcoin | BTC | secp256k1 | mainnet, testnet (Legacy, SegWit, Taproot) |
| Zcash | ZEC | secp256k1 | mainnet, testnet (transparent addresses) |
| Monero | XMR | ed25519 | mainnet, stagenet, testnet |
| Solana | SOL | ed25519 | mainnet-beta, devnet, testnet |
| Ethereum Classic | ETC | secp256k1 | mainnet, mordor |

## Quick Start

### 1. Mount the Floppy Disk

```bash
node .claude/skills/floppy-keystore/scripts/cli.js mount
```

### 2. Create an Encrypted Keystore

```bash
node .claude/skills/floppy-keystore/scripts/cli.js create
# Enter your BIP-39 mnemonic (12 or 24 words)
# Set encryption password
```

### 3. Derive Keys for Any Chain

```bash
# Ethereum keys
node cli.js derive ethereum --count=5

# Bitcoin Native SegWit addresses
node cli.js derive bitcoin --type=nativeSegwit --count=3

# Solana keys
node cli.js derive solana --count=2

# Show addresses only (no private keys)
node cli.js address monero --count=10
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `mount` | Mount floppy disk with secure options |
| `unmount` | Safely unmount floppy disk |
| `create` | Create new encrypted mnemonic keystore |
| `test` | Test keystore decryption |
| `info` | Show keystore status and supported chains |
| `chains` | List all supported blockchain chains |
| `derive <chain>` | Derive keys for a specific chain |
| `address <chain>` | Show addresses only (no private keys) |

### Derive Options

```bash
--count=N     # Number of accounts to derive (default: 1)
--start=N     # Starting index (default: 0)
--type=TYPE   # Address type (Bitcoin: legacy, segwit, nativeSegwit, taproot)
```

## Programmatic Usage

### Basic Ethereum (Hardhat Compatible)

```javascript
const { loadFloppyKeysSync } = require('./.claude/skills/floppy-keystore/scripts/loader');

module.exports = {
  networks: {
    mainnet: {
      url: "https://eth.llamarpc.com",
      accounts: loadFloppyKeysSync()
    }
  }
};
```

### Multi-Chain Key Derivation

```javascript
const { deriveChainKeys, getChainAddresses } = require('./loader');

// Derive Ethereum keys
const ethKeys = await deriveChainKeys('ethereum', { count: 5 });

// Derive Bitcoin keys (Native SegWit)
const btcKeys = await deriveChainKeys('bitcoin', {
  count: 3,
  addressType: 'nativeSegwit'
});

// Derive Solana keys
const solKeys = await deriveChainKeys('solana', { count: 2 });

// Get just addresses
const xmrAddresses = await getChainAddresses('monero', { count: 10 });
```

### Key Object Structure

```javascript
// Ethereum/Bitcoin/Zcash (secp256k1)
{
  chain: 'ETH',
  index: 0,
  path: "m/44'/60'/0'/0/0",
  privateKey: '0x...',
  publicKey: '0x...',
  address: '0x...'
}

// Monero (ed25519 - dual key)
{
  chain: 'XMR',
  index: 0,
  path: 'derived/0',
  privateSpendKey: '...',
  privateViewKey: '...',
  address: '4...'
}

// Solana (ed25519)
{
  chain: 'SOL',
  index: 0,
  path: "m/44'/501'/0'/0'",
  privateKey: '...',
  publicKey: '...',  // Base58
  address: '...'     // Same as publicKey
}
```

## Bitcoin Address Types

Bitcoin supports multiple address formats:

| Type | Purpose | Prefix | Description |
|------|---------|--------|-------------|
| `legacy` | 44 | 1... | P2PKH (Original format) |
| `segwit` | 49 | 3... | P2SH-wrapped SegWit |
| `nativeSegwit` | 84 | bc1q... | P2WPKH (Recommended) |
| `taproot` | 86 | bc1p... | P2TR (Latest) |

```bash
# Derive Bitcoin Taproot addresses
node cli.js derive bitcoin --type=taproot --count=5
```

## Derivation Paths

Standard BIP-44 paths used for each chain:

| Chain | Path | Notes |
|-------|------|-------|
| Ethereum | `m/44'/60'/0'/0/{i}` | Standard EVM path |
| Bitcoin | `m/84'/0'/0'/0/{i}` | Native SegWit default |
| Zcash | `m/44'/133'/0'/0/{i}` | Transparent addresses |
| Monero | `m/44'/128'/0'/0/{i}` | Derived from BIP-39 |
| Solana | `m/44'/501'/{i}'/0'` | Hardened derivation |
| ETC | `m/44'/61'/0'/0/{i}` | Ethereum Classic |

## Security Model

### Encryption

- **KDF**: scrypt (N=262144, r=8, p=1) - ~512MB memory
- **Cipher**: AES-128-CTR
- **MAC**: keccak256 (mnemonic) / HMAC-SHA256 (admin keys)
- **Timing-safe**: Constant-time comparison

### Mount Security

```bash
noexec      # Prevent executable files
nosuid      # Ignore setuid bits
nodev       # Ignore device files
umask=077   # Owner-only permissions
sync,flush  # Immediate write-through
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLOPPY_DEVICE` | `/dev/sde` | Floppy device path |
| `FLOPPY_MOUNT` | `/mnt/floppy` | Mount point directory |
| `FLOPPY_KEYSTORE_PASSWORD` | - | Password for non-interactive use |

## Optional Dependencies

For full functionality on all chains, install these optional packages:

```bash
# Bitcoin address generation
npm install bitcoinjs-lib tiny-secp256k1 ecpair

# Solana key derivation
npm install @solana/web3.js ed25519-hd-key bip39

# Monero address generation
npm install monero-javascript
```

Without these packages, the skill will:
- Still derive valid private keys
- Show hash160/partial addresses with notes about missing libraries
- Work fully for Ethereum and EVM chains (uses ethers.js)

## File Structure

```
/mnt/floppy/
  .keystore/
    mnemonic-keystore.json   # Encrypted BIP-39 mnemonic (all chains)
    admin-keystore.json      # Single admin key (optional)
```

## Troubleshooting

### "Floppy not mounted"
```bash
# Check if device exists
ls -la /dev/sde

# Mount manually
sudo mount -t vfat /dev/sde /mnt/floppy -o noexec,nosuid,nodev,umask=077
```

### "Unknown chain"
```bash
# List supported chains
node cli.js chains

# Use alias
node cli.js derive btc   # Same as 'bitcoin'
node cli.js derive eth   # Same as 'ethereum'
```

### Missing addresses for Bitcoin/Solana/Monero
Install the optional dependencies for full address generation:
```bash
npm install bitcoinjs-lib tiny-secp256k1 ecpair  # Bitcoin
npm install @solana/web3.js ed25519-hd-key       # Solana
```

## x402 Protocol Support

The floppy keystore fully supports the [x402 payment protocol](https://www.x402.org/) for HTTP-native payments.

### Supported x402 Networks

| Network | Chain | USDC Contract |
|---------|-------|---------------|
| `eip155:8453` | Base Mainnet | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| `eip155:84532` | Base Sepolia | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |
| `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | Solana Mainnet | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | Solana Devnet | `4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU` |

### Making x402 Payments

```javascript
const { preparePayment } = require('./scripts/x402');
const { loadMnemonicFromFloppy } = require('./scripts/loader');

// Load mnemonic from floppy
const mnemonic = await loadMnemonicFromFloppy();

// Prepare payment for Base network
const payment = await preparePayment({
  network: 'eip155:8453',
  payTo: '0x1234...recipient',
  amount: '0.50',  // 0.50 USDC
  resource: 'https://api.example.com/data',
  mnemonic
});

// Use in HTTP request
const response = await fetch('https://api.example.com/data', {
  headers: {
    'X-PAYMENT': payment.header
  }
});
```

### EIP-3009 Signing (EVM/Base)

For EVM networks, x402 uses EIP-3009 `transferWithAuthorization`:

```javascript
const { createEVMPaymentPayload, encodePaymentHeader } = require('./scripts/x402');
const { deriveChainKeys } = require('./scripts/loader');

// Get Ethereum keys from floppy
const keys = await deriveChainKeys('ethereum', { count: 1 });
const wallet = keys[0];

// Create payment payload
const payload = await createEVMPaymentPayload({
  network: 'eip155:8453',  // Base mainnet
  payTo: '0x1234...merchant',
  amount: '1.00',
  privateKey: wallet.privateKey,
  fromAddress: wallet.address
});

// Encode for header
const header = encodePaymentHeader(payload);
```

### Solana Payments

```javascript
const { createSolanaPaymentPayload } = require('./scripts/x402');
const { deriveChainKeys } = require('./scripts/loader');

// Get Solana keys from floppy
const keys = await deriveChainKeys('solana', { count: 1 });

const payload = await createSolanaPaymentPayload({
  network: 'solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp',
  payTo: 'Merchant...base58',
  amount: '2.00',
  privateKey: keys[0].privateKey,
  fromAddress: keys[0].address
});
```

### Payment Tracking

Payments are automatically tracked in persistent memory:

```javascript
const { getPaymentHistory, trackPayment } = require('./scripts/x402');

// Get payment history
const history = getPaymentHistory({ network: 'eip155:8453', limit: 10 });

// Manual tracking
trackPayment({
  network: 'eip155:8453',
  amount: '1.00',
  to: '0x...',
  resource: 'https://api.example.com',
  status: 'completed'
});
```

### x402 Protocol Flow

```
1. Client requests protected resource
2. Server responds: 402 Payment Required + PAYMENT-REQUIRED header
3. Client decodes payment requirements
4. Client creates payment payload (EIP-3009 or SPL transfer)
5. Client signs with floppy keystore keys
6. Client retries with X-PAYMENT header
7. Facilitator verifies and settles payment
8. Server returns resource
```

## Additional Documentation

- [REFERENCE.md](REFERENCE.md) - Full API documentation
- [HARDHAT-INTEGRATION.md](HARDHAT-INTEGRATION.md) - Hardhat configuration guide

## Agent Identity & Persistent Memory

The floppy disk has ~1.4 MB available after keystores for storing agent identity and memory.

### Storage Capacity

```bash
node cli.js storage
# Capacity:  1.4 MB
# Used:      1.2 KB (0.1%)
# Available: 1.43 MB
```

### DID Document

Create and manage a W3C DID document for your agent:

```bash
# Create DID
node cli.js did create --method=key

# View DID document
node cli.js did show

# Add service endpoint
node cli.js did add-service --type=AgentService --endpoint=https://agent.example.com
```

### AT Protocol (Bluesky) DID Support

Create DID documents compatible with the AT Protocol (Bluesky, etc.):

```bash
# Create AT Protocol DID (did:web)
node cli.js did atproto --domain=agent.example.com --handle=agent.bsky.social --pds=https://bsky.social

# Set signing key from keystore
node cli.js did setkey

# Validate for AT Protocol
node cli.js did validate

# Export for web hosting
node cli.js did export --file=did.json
# Host at: https://agent.example.com/.well-known/did.json

# Update handle
node cli.js did handle --handle=newhandle.bsky.social
```

**AT Protocol DID Requirements:**
- `did:web` or `did:plc` method
- `alsoKnownAs` with `at://` handle URI
- `Multikey` verification method with secp256k1 key
- `AtprotoPersonalDataServer` service endpoint

```javascript
// Programmatic usage
const identity = require('./scripts/identity');

// Create AT Protocol DID
const doc = identity.createATProtoDIDDocument({
  domain: 'agent.example.com',
  handle: 'agent.bsky.social',
  pdsUrl: 'https://bsky.social'
});

// Set public key from Ethereum-derived key
identity.setATProtoPublicKey(publicKeyHex);

// Validate
const result = identity.validateATProtoDID();
if (result.valid) {
  const json = identity.exportDIDForWeb();
  // Host json at /.well-known/did.json
}
```

### ENS DID Support (did:ens)

For Ethereum ecosystem identity using ENS domains:

```bash
# Create ENS-based DID
node cli.js did ens --name=chipprbots.eth

# Export for ENS text record
node cli.js did export-ens
# Copy the output and add as "did" text record in ENS app
```

**Important:** `did:ens` is **NOT supported** by AT Protocol (Bluesky). Use `did:web` for Bluesky compatibility.

```javascript
// Programmatic usage
const doc = identity.createENSDIDDocument({
  ensName: 'chipprbots.eth',
  chainId: '1'  // Ethereum mainnet
});

// Export for ENS storage
const { textRecord, instructions } = identity.exportDIDForENS();
// Store textRecord in ENS "did" text record
```

**ENS vs AT Protocol DIDs:**

| Feature | did:ens | did:web (AT Protocol) |
|---------|---------|----------------------|
| Storage | ENS text records | Web server /.well-known/did.json |
| Bluesky/AT Protocol | Not supported | Supported |
| Ethereum ecosystem | Native | Separate |
| Resolution | ENS resolvers | HTTP |
| Cost | Gas fees for updates | Web hosting |

### Agent Profile

Store agent identity information:

```bash
# Set profile (interactive)
node cli.js profile set

# Set profile with options
node cli.js profile set --name="TradingAgent" --version="1.0.0"

# View profile
node cli.js profile show
```

### Persistent Memory

Store notes, facts, and context that persist across sessions:

```bash
# Add memory
node cli.js memory add --content="User prefers BTC over ETH" --tags=preference --importance=8

# List memories
node cli.js memory list

# Search
node cli.js memory search --text="preference"

# Filter by importance
node cli.js memory list --importance=7

# Delete
node cli.js memory delete --id=abc123
```

### Key-Value Metadata

Simple key-value store for configuration:

```bash
# Set value
node cli.js metadata set --key=lastSync --value="2025-01-15T10:00:00Z"

# Get value
node cli.js metadata get --key=lastSync

# List all
node cli.js metadata list
```

### Programmatic Usage

```javascript
const identity = require('./scripts/identity');

// DID Document
const did = identity.createDIDDocument({ method: 'key' });
console.log(did.id);  // did:key:abc123...

// Memory
identity.addMemory({
  type: 'fact',
  content: 'User wallet is 0x123...',
  tags: ['user', 'wallet'],
  importance: 9
});

const memories = identity.searchMemory({ tags: ['user'], limit: 5 });

// Metadata
identity.setMetadataValue('config.theme', 'dark');
const theme = identity.getMetadataValue('config.theme');
```

## Security Best Practices

1. **Physical security** - Store floppy in secure location
2. **Strong password** - Use 16+ characters
3. **Unmount immediately** - Don't leave mounted
4. **Never share mnemonic** - One mnemonic = all chains
5. **Test before production** - Verify addresses on testnets first
