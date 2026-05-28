# Floppy Keystore API Reference

## Module: loader.js

The main integration module for loading keys from floppy disk with multi-chain support.

### Core Functions

#### `isFloppyMounted()`

Check if the floppy disk is mounted.

```javascript
const { isFloppyMounted } = require('./scripts/loader');

if (isFloppyMounted()) {
  console.log('Floppy disk is ready');
}
```

**Returns:** `boolean`

---

#### `loadMnemonicFromFloppy()`

Load and decrypt the mnemonic from floppy disk. Caches result for session.

```javascript
const { loadMnemonicFromFloppy } = require('./scripts/loader');

const mnemonic = await loadMnemonicFromFloppy();
```

**Returns:** `Promise<string>` - The decrypted BIP-39 mnemonic phrase

**Throws:** `Error` if floppy not mounted, keystore not found, or password incorrect

---

### Multi-Chain Functions

#### `deriveChainKeys(chainId, options)`

Derive keys for a specific blockchain from the mnemonic on floppy disk.

```javascript
const { deriveChainKeys } = require('./scripts/loader');

// Derive Ethereum keys
const ethKeys = await deriveChainKeys('ethereum', { count: 5 });

// Derive Bitcoin Native SegWit keys
const btcKeys = await deriveChainKeys('bitcoin', {
  count: 3,
  addressType: 'nativeSegwit'
});

// Derive Solana keys
const solKeys = await deriveChainKeys('solana', { count: 2 });
```

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `chainId` | `string` | - | Chain identifier (e.g., 'ethereum', 'bitcoin', 'solana') |
| `options.count` | `number` | `1` | Number of accounts to derive |
| `options.startIndex` | `number` | `0` | Starting derivation index |
| `options.addressType` | `string` | `null` | Address type (Bitcoin only) |
| `options.cache` | `boolean` | `true` | Cache results for session |

**Returns:** `Promise<Array<KeyObject>>` - Array of derived key objects

**Key Object Structure (secp256k1 chains):**
```javascript
{
  chain: 'ETH',
  index: 0,
  path: "m/44'/60'/0'/0/0",
  privateKey: '0x...',
  publicKey: '0x...',
  address: '0x...',
  addressType: 'nativeSegwit'  // Bitcoin only
}
```

**Key Object Structure (Monero):**
```javascript
{
  chain: 'XMR',
  index: 0,
  path: 'derived/0',
  privateSpendKey: '...',
  privateViewKey: '...',
  publicSpendKey: '...',
  publicViewKey: '...',
  address: '4...'
}
```

---

#### `getChainPrivateKeys(chainId, options)`

Get just the private keys for a specific chain.

```javascript
const { getChainPrivateKeys } = require('./scripts/loader');

const keys = await getChainPrivateKeys('ethereum', { count: 5 });
// keys = ['0x...', '0x...', '0x...', '0x...', '0x...']
```

**Returns:** `Promise<string[]>` - Array of private keys

---

#### `getChainAddresses(chainId, options)`

Get just the addresses for a specific chain.

```javascript
const { getChainAddresses } = require('./scripts/loader');

const addresses = await getChainAddresses('bitcoin', {
  count: 5,
  addressType: 'nativeSegwit'
});
// addresses = ['bc1q...', 'bc1q...', ...]
```

**Returns:** `Promise<string[]>` - Array of addresses

---

#### `getChainSummary()`

Get a summary of all supported chains.

```javascript
const { getChainSummary } = require('./scripts/loader');

const chains = getChainSummary();
chains.forEach(chain => {
  console.log(`${chain.symbol}: ${chain.name} (${chain.curve})`);
});
```

**Returns:** `Array<ChainSummary>`

```javascript
{
  id: 'bitcoin',
  name: 'Bitcoin',
  symbol: 'BTC',
  curve: 'secp256k1',
  derivationPath: "m/84'/0'/0'/0",
  networks: ['mainnet', 'testnet', 'signet'],
  addressTypes: ['legacy', 'segwit', 'nativeSegwit', 'taproot']
}
```

---

### Ethereum Functions (Backwards Compatible)

#### `getFloppyPrivateKeys(options)`

Derive Ethereum private keys (backwards compatible API).

```javascript
const { getFloppyPrivateKeys } = require('./scripts/loader');

const keys = await getFloppyPrivateKeys({ count: 10, initialIndex: 0 });
```

**Returns:** `Promise<string[]>` - Array of Ethereum private keys

---

#### `loadFloppyKeysSync(allowFallback, chainId)`

Synchronously load keys for Hardhat config.

```javascript
const { loadFloppyKeysSync } = require('./scripts/loader');

// Ethereum (default)
const ethKeys = loadFloppyKeysSync(false);

// Other chain
const etcKeys = loadFloppyKeysSync(false, 'ethereumClassic');

// With fallback for development
const devKeys = loadFloppyKeysSync(true);  // Falls back to PRIVATE_KEY env var
```

**Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `allowFallback` | `boolean` | `false` | Allow PRIVATE_KEY env var fallback |
| `chainId` | `string` | `'ethereum'` | Chain to derive keys for |

**Returns:** `string[]` - Array of private keys (synchronous)

---

## Module: chains.js

Low-level chain derivation functions.

### Functions

#### `deriveKeys(mnemonic, chainId, options)`

Derive keys directly from a mnemonic.

```javascript
const { deriveKeys } = require('./scripts/chains');

const mnemonic = 'abandon abandon ...';
const keys = await deriveKeys(mnemonic, 'bitcoin', {
  count: 5,
  startIndex: 0,
  addressType: 'taproot'
});
```

---

#### `validatePrivateKey(privateKey, chainId)`

Validate a private key for a specific chain.

```javascript
const { validatePrivateKey } = require('./scripts/chains');

if (validatePrivateKey('0x...', 'ethereum')) {
  console.log('Valid Ethereum private key');
}
```

**Returns:** `boolean`

---

## Module: config.js

Configuration and chain definitions.

### Chain Configuration

```javascript
const { CHAINS, getChainConfig, listChains } = require('./scripts/config');

// Get specific chain config
const btcConfig = getChainConfig('bitcoin');
console.log(btcConfig.derivationPath);  // "m/84'/0'/0'/0"

// List all chain IDs
const chainIds = listChains();
// ['ethereum', 'bitcoin', 'zcash', 'monero', 'solana', 'ethereumClassic']
```

### Chain Aliases

```javascript
const { CHAIN_ALIASES } = require('./scripts/config');

// eth -> ethereum
// btc -> bitcoin
// zec -> zcash
// xmr -> monero
// sol -> solana
// etc -> ethereumClassic
```

### Supported Chains

| Chain | Coin Type | Curve | Default Path |
|-------|-----------|-------|--------------|
| ethereum | 60 | secp256k1 | m/44'/60'/0'/0 |
| bitcoin | 0 | secp256k1 | m/84'/0'/0'/0 |
| zcash | 133 | secp256k1 | m/44'/133'/0'/0 |
| monero | 128 | ed25519 | m/44'/128'/0'/0 |
| solana | 501 | ed25519 | m/44'/501'/0'/0' |
| ethereumClassic | 61 | secp256k1 | m/44'/61'/0'/0 |

---

## Module: keystore.js

Encryption/decryption functions.

### Functions

#### `encryptMnemonic(mnemonic, password)`

Encrypt a BIP-39 mnemonic phrase.

```javascript
const { encryptMnemonic } = require('./scripts/keystore');

const keystore = await encryptMnemonic(
  'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about',
  'strongpassword'
);
```

**Returns:** `Promise<object>` - Keystore JSON object

---

#### `decryptMnemonic(keystore, password)`

Decrypt a mnemonic from keystore format.

```javascript
const { decryptMnemonic } = require('./scripts/keystore');

const mnemonic = await decryptMnemonic(keystore, 'strongpassword');
```

**Returns:** `Promise<string>` - Decrypted mnemonic phrase

---

## Bitcoin Address Types

### Usage

```javascript
const { deriveChainKeys } = require('./scripts/loader');

// Legacy (P2PKH) - starts with '1'
const legacy = await deriveChainKeys('bitcoin', { addressType: 'legacy' });

// SegWit (P2SH-P2WPKH) - starts with '3'
const segwit = await deriveChainKeys('bitcoin', { addressType: 'segwit' });

// Native SegWit (P2WPKH) - starts with 'bc1q' (recommended)
const native = await deriveChainKeys('bitcoin', { addressType: 'nativeSegwit' });

// Taproot (P2TR) - starts with 'bc1p'
const taproot = await deriveChainKeys('bitcoin', { addressType: 'taproot' });
```

### Derivation Paths

| Type | Purpose | Path |
|------|---------|------|
| legacy | 44 | m/44'/0'/0'/0/{i} |
| segwit | 49 | m/49'/0'/0'/0/{i} |
| nativeSegwit | 84 | m/84'/0'/0'/0/{i} |
| taproot | 86 | m/86'/0'/0'/0/{i} |

---

## Monero Key Structure

Monero uses a dual-key system:

```javascript
const { deriveChainKeys } = require('./scripts/loader');

const xmrKeys = await deriveChainKeys('monero', { count: 1 });

console.log(xmrKeys[0]);
// {
//   chain: 'XMR',
//   index: 0,
//   path: 'derived/0',
//   privateSpendKey: '...',  // Used for spending
//   privateViewKey: '...',   // Used for viewing incoming transactions
//   publicSpendKey: '...',
//   publicViewKey: '...',
//   address: '4...'          // Standard Monero address
// }
```

**Note:** This derives keys from BIP-39 mnemonic, not native Monero 25-word format. For full Monero address generation, install `monero-javascript`.

---

## Solana Key Structure

Solana uses ed25519 with hardened derivation:

```javascript
const { deriveChainKeys } = require('./scripts/loader');

const solKeys = await deriveChainKeys('solana', { count: 1 });

console.log(solKeys[0]);
// {
//   chain: 'SOL',
//   index: 0,
//   path: "m/44'/501'/0'/0'",
//   privateKey: '...',      // 64 bytes (seed + public key)
//   publicKey: '...',       // Base58 encoded
//   address: '...'          // Same as publicKey on Solana
// }
```

**Note:** For full Solana support, install `@solana/web3.js` and `ed25519-hd-key`.

---

## Error Handling

```javascript
const { deriveChainKeys, isFloppyMounted, keystoreExists } = require('./scripts/loader');

try {
  // Pre-check
  if (!isFloppyMounted()) {
    throw new Error('Please mount floppy disk first');
  }
  if (!keystoreExists()) {
    throw new Error('Please create keystore first');
  }

  const keys = await deriveChainKeys('ethereum', { count: 5 });
} catch (err) {
  if (err.message.includes('Invalid password')) {
    console.error('Wrong password');
  } else if (err.message.includes('Unsupported chain')) {
    console.error('Chain not supported');
  } else {
    console.error('Error:', err.message);
  }
}
```

---

## Memory Management

Keys are cached for the session and cleared on exit:

```javascript
const { clearCache } = require('./scripts/loader');

// Manually clear cached keys
clearCache();

// Automatic clearing on:
// - process.exit
// - SIGINT (Ctrl+C)
// - SIGTERM
```
