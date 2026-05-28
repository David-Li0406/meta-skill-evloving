# Hardhat Integration Guide

This guide shows how to integrate the floppy keystore with Hardhat for secure blockchain deployments.

## Basic Setup

### 1. Import the Loader

```javascript
// hardhat.config.js
const {
  loadFloppyKeysSync,
  isFloppyMounted,
  keystoreExists,
  CONFIG: FLOPPY_CONFIG
} = require('./.claude/skills/floppy-keystore/scripts/loader');
```

### 2. Synchronous Decryption Function

Hardhat requires synchronous account loading at config time. Here's the full implementation:

```javascript
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * Synchronously decrypt a keystore file
 * Supports both admin keystore (HMAC-SHA256) and mnemonic keystore (keccak256)
 */
function decryptKeystoreSync(keystorePath, password) {
  try {
    const keystoreJson = fs.readFileSync(keystorePath, 'utf8');
    const keystore = JSON.parse(keystoreJson);
    const { crypto: cryptoParams } = keystore;
    const keystoreType = keystore.type;

    const salt = Buffer.from(cryptoParams.kdfparams.salt, 'hex');
    const iv = Buffer.from(cryptoParams.cipherparams.iv, 'hex');
    const ciphertext = Buffer.from(cryptoParams.ciphertext, 'hex');
    const storedMac = Buffer.from(cryptoParams.mac, 'hex');

    // Derive key (allocate 512MB for high N scrypt)
    const derivedKey = crypto.scryptSync(
      password,
      salt,
      cryptoParams.kdfparams.dklen,
      {
        N: cryptoParams.kdfparams.n,
        r: cryptoParams.kdfparams.r,
        p: cryptoParams.kdfparams.p,
        maxmem: 512 * 1024 * 1024
      }
    );

    // Verify MAC
    let computedMac;
    if (keystoreType === 'admin-private-key') {
      // Admin keystore: HMAC-SHA256
      computedMac = crypto.createHmac('sha256', derivedKey.slice(16, 32))
        .update(ciphertext)
        .digest();
    } else {
      // Mnemonic keystore: keccak256
      const { keccak256 } = require('ethers');
      const macInput = Buffer.concat([
        Buffer.from(derivedKey.slice(16, 32)),
        ciphertext
      ]);
      computedMac = Buffer.from(keccak256(macInput).slice(2), 'hex');
    }

    if (!computedMac.equals(storedMac)) {
      return null;
    }

    // Decrypt
    const decipher = crypto.createDecipheriv(
      cryptoParams.cipher,
      derivedKey.slice(0, 16),
      iv
    );
    return Buffer.concat([
      decipher.update(ciphertext),
      decipher.final()
    ]);
  } catch (err) {
    return null;
  }
}
```

### 3. Key Loading Function

```javascript
/**
 * Load keys from floppy keystore
 * @param {boolean} allowFallback - Allow PRIVATE_KEY env var fallback
 * @returns {string[]} Array of private keys
 */
function loadFloppyKeysSync(allowFallback = false) {
  if (!isFloppyMounted()) {
    console.warn('[Floppy] Disk not mounted');
    if (allowFallback && process.env.PRIVATE_KEY) {
      return [process.env.PRIVATE_KEY];
    }
    return [];
  }

  const password = process.env.FLOPPY_KEYSTORE_PASSWORD;
  if (!password) {
    console.warn('[Floppy] FLOPPY_KEYSTORE_PASSWORD not set');
    if (allowFallback && process.env.PRIVATE_KEY) {
      return [process.env.PRIVATE_KEY];
    }
    return [];
  }

  const keystoreDir = path.join(FLOPPY_CONFIG.MOUNT_POINT, FLOPPY_CONFIG.KEYSTORE_DIR);

  // Try admin keystore first
  const adminPath = path.join(keystoreDir, 'admin-keystore.json');
  if (fs.existsSync(adminPath)) {
    const decrypted = decryptKeystoreSync(adminPath, password);
    if (decrypted) {
      console.log('[Floppy] Loaded admin key');
      return ['0x' + decrypted.toString('hex')];
    }
    console.warn('[Floppy] Invalid password for admin keystore');
    return [];
  }

  // Try mnemonic keystore
  const mnemonicPath = path.join(keystoreDir, 'mnemonic-keystore.json');
  if (fs.existsSync(mnemonicPath)) {
    const decrypted = decryptKeystoreSync(mnemonicPath, password);
    if (decrypted) {
      const mnemonic = decrypted.toString('utf8');
      const { HDNodeWallet } = require('ethers');
      const wallet = HDNodeWallet.fromPhrase(mnemonic, undefined, "m/44'/60'/0'/0/0");
      console.log('[Floppy] Loaded mnemonic wallet:', wallet.address);
      return [wallet.privateKey];
    }
    console.warn('[Floppy] Invalid password for mnemonic keystore');
    return [];
  }

  console.warn('[Floppy] No keystore found');
  return [];
}
```

## Network Configuration

### Production Networks (No Fallback)

For production networks, **never** allow environment variable fallbacks:

```javascript
// Load keys at config time
const productionKeys = loadFloppyKeysSync(false);

module.exports = {
  networks: {
    mainnet: {
      url: process.env.MAINNET_RPC_URL || "https://eth.llamarpc.com",
      chainId: 1,
      accounts: productionKeys,
    },
    polygon: {
      url: "https://polygon-rpc.com",
      chainId: 137,
      accounts: productionKeys,
    }
  }
};
```

### Development Networks (With Fallback)

For local development, allow fallback to environment variables:

```javascript
const devKeys = loadFloppyKeysSync(true);

module.exports = {
  networks: {
    hardhat: {
      chainId: 1337,
    },
    localhost: {
      url: "http://127.0.0.1:8545",
      accounts: devKeys.length ? devKeys : undefined,
    }
  }
};
```

### Mixed Configuration Example

```javascript
const floppyKeys = loadFloppyKeysSync(false);
const devKeys = loadFloppyKeysSync(true);

module.exports = {
  networks: {
    // Development - allows PRIVATE_KEY fallback
    hardhat: { chainId: 1337 },
    localhost: {
      url: "http://127.0.0.1:8545",
      accounts: devKeys,
    },

    // Testnets - floppy required
    sepolia: {
      url: "https://rpc.sepolia.org",
      chainId: 11155111,
      accounts: floppyKeys,
    },
    mordor: {
      url: "https://rpc.mordor.etccooperative.org",
      chainId: 63,
      accounts: floppyKeys,
    },

    // Production - floppy absolutely required
    mainnet: {
      url: process.env.MAINNET_RPC_URL,
      chainId: 1,
      accounts: floppyKeys,
    }
  }
};
```

## Multiple Accounts

For deploying with multiple accounts from HD wallet:

```javascript
const { getFloppyPrivateKeys } = require('./scripts/loader');

// In an async context (not at config top-level)
async function getDeploymentAccounts() {
  return await getFloppyPrivateKeys({ count: 5, initialIndex: 0 });
}

// For config, you need synchronous loading
function loadMultipleKeysSync(count = 5) {
  const password = process.env.FLOPPY_KEYSTORE_PASSWORD;
  if (!password) return [];

  const mnemonicPath = '/mnt/floppy/.keystore/mnemonic-keystore.json';
  const decrypted = decryptKeystoreSync(mnemonicPath, password);
  if (!decrypted) return [];

  const mnemonic = decrypted.toString('utf8');
  const { HDNodeWallet } = require('ethers');
  const masterNode = HDNodeWallet.fromPhrase(mnemonic);

  const keys = [];
  for (let i = 0; i < count; i++) {
    const wallet = masterNode.derivePath(`m/44'/60'/0'/0/${i}`);
    keys.push(wallet.privateKey);
  }
  return keys;
}
```

## Deployment Workflow

### 1. Before Deployment

```bash
# Mount the floppy disk
npm run floppy:mount

# Verify keystore
npm run floppy:info

# Set password (don't put in .env file!)
export FLOPPY_KEYSTORE_PASSWORD="your-password"
```

### 2. Deploy

```bash
npx hardhat run scripts/deploy.js --network mainnet
```

### 3. After Deployment

```bash
# Unmount immediately
npm run floppy:unmount

# Clear password from environment
unset FLOPPY_KEYSTORE_PASSWORD
```

## Security Best Practices

1. **Never commit passwords** - Use environment variables set in the current shell only
2. **Unmount immediately** - Don't leave the floppy mounted longer than necessary
3. **No fallback in production** - Always use `loadFloppyKeysSync(false)` for mainnet
4. **Physical security** - Store the floppy disk in a secure location
5. **Verify addresses** - Check the loaded wallet address before deploying
6. **Test first** - Always deploy to testnets before mainnet

## Troubleshooting

### Config loads but no accounts

```javascript
// Add debug logging
const keys = loadFloppyKeysSync(false);
console.log('[Debug] Loaded keys count:', keys.length);
console.log('[Debug] Floppy mounted:', isFloppyMounted());
console.log('[Debug] Keystore exists:', keystoreExists());
```

### Memory errors during decryption

Increase Node.js memory limit:

```bash
NODE_OPTIONS="--max-old-space-size=1024" npx hardhat compile
```

### Different MAC algorithms

The skill supports two keystore types with different MACs:
- **admin-keystore.json**: Uses HMAC-SHA256
- **mnemonic-keystore.json**: Uses keccak256

Ensure you're using the correct verification for each type.
