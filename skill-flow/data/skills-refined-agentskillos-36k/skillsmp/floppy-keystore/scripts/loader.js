/**
 * Multi-chain key loader for floppy keystore
 *
 * This module provides functions for loading cryptographic keys from
 * an encrypted keystore stored on a floppy disk. It supports multiple
 * blockchain networks including Ethereum, Bitcoin, Zcash, Monero, and Solana.
 *
 * Usage in hardhat.config.js:
 *   const { loadFloppyKeysSync, isFloppyMounted } = require('./loader');
 *   module.exports = {
 *     networks: {
 *       mainnet: { accounts: loadFloppyKeysSync() }
 *     }
 *   };
 *
 * Multi-chain usage:
 *   const { deriveChainKeys } = require('./loader');
 *   const btcKeys = await deriveChainKeys('bitcoin', { count: 5 });
 *   const solKeys = await deriveChainKeys('solana', { count: 3 });
 *
 * @module loader
 */
const fs = require('fs');
const path = require('path');
const readline = require('readline');
const crypto = require('crypto');
const { decryptMnemonic } = require('./keystore');
const { deriveKeys, getChainSummary } = require('./chains');
const CONFIG = require('./config');

const KEYSTORE_PATH = path.join(
  CONFIG.MOUNT_POINT,
  CONFIG.KEYSTORE_DIR,
  CONFIG.KEYSTORE_FILENAME
);

const ADMIN_KEYSTORE_PATH = path.join(
  CONFIG.MOUNT_POINT,
  CONFIG.KEYSTORE_DIR,
  CONFIG.ADMIN_KEYSTORE_FILENAME
);

// Cache for session to avoid repeated password prompts
let cachedMnemonic = null;
let cachedAdminKey = null;
let cachedChainKeys = {};

/**
 * Check if floppy is mounted
 * @returns {boolean}
 */
function isFloppyMounted() {
  try {
    const { execSync } = require('child_process');
    execSync(`mountpoint -q "${CONFIG.MOUNT_POINT}"`, { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

/**
 * Check if mnemonic keystore exists
 * @returns {boolean}
 */
function keystoreExists() {
  return fs.existsSync(KEYSTORE_PATH);
}

/**
 * Check if admin keystore exists
 * @returns {boolean}
 */
function adminKeystoreExists() {
  return fs.existsSync(ADMIN_KEYSTORE_PATH);
}

/**
 * Prompt for password (async for interactive use)
 * @param {string} prompt - Prompt text
 * @returns {Promise<string>}
 */
function promptPasswordAsync(prompt) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: true
    });

    if (process.stdin.isTTY) {
      process.stdin.setRawMode(true);
    }

    process.stdout.write(prompt);

    let password = '';
    process.stdin.on('data', function handler(char) {
      const c = char.toString();

      if (c === '\n' || c === '\r' || c === '\u0004') {
        if (process.stdin.isTTY) {
          process.stdin.setRawMode(false);
        }
        process.stdin.removeListener('data', handler);
        rl.close();
        console.log();
        resolve(password);
      } else if (c === '\u0003') {
        process.exit(1);
      } else if (c === '\u007f' || c === '\b') {
        password = password.slice(0, -1);
      } else if (c.charCodeAt(0) >= 32) {
        password += c;
      }
    });
  });
}

/**
 * Load mnemonic from floppy keystore (async)
 * Caches the result for the session to avoid repeated prompts
 *
 * @returns {Promise<string>} The decrypted mnemonic
 * @throws {Error} If floppy not mounted or keystore not found
 */
async function loadMnemonicFromFloppy() {
  if (cachedMnemonic) {
    return cachedMnemonic;
  }

  if (!isFloppyMounted()) {
    throw new Error(
      `Floppy not mounted at ${CONFIG.MOUNT_POINT}. ` +
      'Run mount script first.'
    );
  }

  if (!keystoreExists()) {
    throw new Error(
      `Keystore not found at ${KEYSTORE_PATH}. ` +
      'Run create command first.'
    );
  }

  const keystoreJson = fs.readFileSync(KEYSTORE_PATH, 'utf8');
  const keystore = JSON.parse(keystoreJson);

  let password = process.env.FLOPPY_KEYSTORE_PASSWORD;

  // Auto-detect disk and resolve password from named env var
  if (!password) {
    const metadataPath = path.join(CONFIG.KEYSTORE_DIR, 'identity', 'metadata.json');
    if (fs.existsSync(metadataPath)) {
      try {
        const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
        const diskName = metadata['disk.name'];
        if (diskName) {
          const envKey = `FLOPPY_${diskName.toUpperCase()}_PASSWORD`;
          password = process.env[envKey];
          if (password) {
            console.log(`[Floppy] Auto-detected disk: ${diskName}`);
          }
        }
      } catch (e) {
        // Ignore metadata read errors
      }
    }
  }

  if (!password) {
    console.log('\n[Floppy Keystore] Password required for network operations');
    password = await promptPasswordAsync('Enter floppy keystore password: ');
  }

  cachedMnemonic = await decryptMnemonic(keystore, password);
  password = '';

  return cachedMnemonic;
}

/**
 * Derive keys for a specific blockchain from the mnemonic on floppy disk
 *
 * @param {string} chainId - Chain identifier (e.g., 'ethereum', 'bitcoin', 'solana')
 * @param {object} options - Derivation options
 * @param {number} options.count - Number of accounts (default: 1)
 * @param {number} options.startIndex - Starting index (default: 0)
 * @param {string} options.addressType - For Bitcoin: 'legacy', 'segwit', 'nativeSegwit', 'taproot'
 * @param {boolean} options.cache - Cache results (default: true)
 * @returns {Promise<Array>} Array of derived key objects
 */
async function deriveChainKeys(chainId, options = {}) {
  const {
    count = 1,
    startIndex = 0,
    addressType = null,
    cache = true
  } = options;

  // Check cache
  const cacheKey = `${chainId}:${startIndex}:${count}:${addressType || 'default'}`;
  if (cache && cachedChainKeys[cacheKey]) {
    return cachedChainKeys[cacheKey];
  }

  const mnemonic = await loadMnemonicFromFloppy();
  const keys = await deriveKeys(mnemonic, chainId, { count, startIndex, addressType });

  // Cache results
  if (cache) {
    cachedChainKeys[cacheKey] = keys;
  }

  return keys;
}

/**
 * Derive private keys for Ethereum (backwards compatible)
 *
 * @param {object} options - Options
 * @param {number} options.count - Number of accounts (default: 10)
 * @param {number} options.initialIndex - Starting index (default: 0)
 * @returns {Promise<string[]>} Array of private keys
 */
async function getFloppyPrivateKeys(options = {}) {
  const {
    count = 10,
    initialIndex = 0
  } = options;

  const mnemonic = await loadMnemonicFromFloppy();
  const { HDNodeWallet } = require('ethers');

  const keys = [];
  // ethers v6 requires explicit root path "m" to get master node
  const masterNode = HDNodeWallet.fromPhrase(mnemonic, undefined, "m");

  for (let i = initialIndex; i < initialIndex + count; i++) {
    const wallet = masterNode.derivePath(`m/44'/60'/0'/0/${i}`);
    keys.push(wallet.privateKey);
  }

  return keys;
}

/**
 * Get private keys for a specific chain
 *
 * @param {string} chainId - Chain identifier
 * @param {object} options - Options
 * @returns {Promise<string[]>} Array of private keys (format depends on chain)
 */
async function getChainPrivateKeys(chainId, options = {}) {
  const keys = await deriveChainKeys(chainId, options);
  return keys.map(k => k.privateKey);
}

/**
 * Get addresses for a specific chain
 *
 * @param {string} chainId - Chain identifier
 * @param {object} options - Options
 * @returns {Promise<string[]>} Array of addresses
 */
async function getChainAddresses(chainId, options = {}) {
  const keys = await deriveChainKeys(chainId, options);
  return keys.map(k => k.address);
}

/**
 * Load admin private key from floppy keystore
 * @returns {Promise<string>} The decrypted private key with 0x prefix
 */
async function loadAdminKeyFromFloppy() {
  if (cachedAdminKey) {
    return cachedAdminKey;
  }

  if (!isFloppyMounted()) {
    throw new Error(
      `Floppy not mounted at ${CONFIG.MOUNT_POINT}. Run mount script first.`
    );
  }

  if (!adminKeystoreExists()) {
    throw new Error(
      `Admin keystore not found at ${ADMIN_KEYSTORE_PATH}. ` +
      'Run store-admin-key script first.'
    );
  }

  const keystoreJson = fs.readFileSync(ADMIN_KEYSTORE_PATH, 'utf8');
  const keystore = JSON.parse(keystoreJson);

  let password = process.env.FLOPPY_KEYSTORE_PASSWORD;
  if (!password) {
    console.log('\n[Floppy Keystore] Password required for admin key');
    password = await promptPasswordAsync('Enter floppy keystore password: ');
  }

  const { crypto: cryptoParams } = keystore;

  const salt = Buffer.from(cryptoParams.kdfparams.salt, 'hex');
  const iv = Buffer.from(cryptoParams.cipherparams.iv, 'hex');
  const ciphertext = Buffer.from(cryptoParams.ciphertext, 'hex');
  const storedMac = Buffer.from(cryptoParams.mac, 'hex');

  const derivedKey = crypto.scryptSync(
    password,
    salt,
    cryptoParams.kdfparams.dklen,
    {
      N: cryptoParams.kdfparams.n,
      r: cryptoParams.kdfparams.r,
      p: cryptoParams.kdfparams.p
    }
  );

  // Admin keystore uses HMAC-SHA256 for MAC
  const mac = crypto.createHmac('sha256', derivedKey.slice(16, 32))
    .update(ciphertext)
    .digest();

  if (!mac.equals(storedMac)) {
    throw new Error('Invalid password - MAC verification failed');
  }

  const decipher = crypto.createDecipheriv(
    cryptoParams.cipher,
    derivedKey.slice(0, 16),
    iv
  );
  const decrypted = Buffer.concat([
    decipher.update(ciphertext),
    decipher.final()
  ]);

  cachedAdminKey = '0x' + decrypted.toString('hex');
  password = '';

  return cachedAdminKey;
}

/**
 * Get admin private key as array (for Hardhat accounts config)
 * @returns {Promise<string[]>}
 */
async function getAdminPrivateKey() {
  const key = await loadAdminKeyFromFloppy();
  return [key];
}

/**
 * Synchronously decrypt a keystore file
 * Supports both admin keystore (HMAC-SHA256) and mnemonic keystore (keccak256)
 *
 * @param {string} keystorePath - Path to keystore file
 * @param {string} password - Decryption password
 * @returns {Buffer|null} Decrypted data or null on failure
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

    let computedMac;
    if (keystoreType === 'admin-private-key') {
      computedMac = crypto.createHmac('sha256', derivedKey.slice(16, 32))
        .update(ciphertext)
        .digest();
    } else {
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

/**
 * Load keys from floppy keystore synchronously (for Hardhat config)
 *
 * @param {boolean} allowFallback - Allow PRIVATE_KEY env var fallback
 * @param {string} chainId - Chain to derive keys for (default: 'ethereum')
 * @returns {string[]} Array of private keys
 */
function loadFloppyKeysSync(allowFallback = false, chainId = 'ethereum') {
  if (!isFloppyMounted()) {
    console.warn('[Floppy] Disk not mounted at', CONFIG.MOUNT_POINT);
    if (allowFallback && process.env.PRIVATE_KEY) {
      console.log('[Floppy] Development mode: Using PRIVATE_KEY env var fallback');
      return [process.env.PRIVATE_KEY];
    }
    return [];
  }

  const password = process.env.FLOPPY_KEYSTORE_PASSWORD;
  if (!password) {
    console.warn('[Floppy] FLOPPY_KEYSTORE_PASSWORD not set');
    if (allowFallback && process.env.PRIVATE_KEY) {
      console.log('[Floppy] Development mode: Using PRIVATE_KEY env var fallback');
      return [process.env.PRIVATE_KEY];
    }
    return [];
  }

  const keystoreDir = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR);

  // Try admin keystore first
  const adminPath = path.join(keystoreDir, CONFIG.ADMIN_KEYSTORE_FILENAME);
  if (fs.existsSync(adminPath)) {
    const decrypted = decryptKeystoreSync(adminPath, password);
    if (decrypted) {
      console.log('[Floppy] Loaded admin key');
      return ['0x' + decrypted.toString('hex')];
    } else {
      console.warn('[Floppy] Invalid password for admin keystore');
      return [];
    }
  }

  // Try mnemonic keystore
  const mnemonicPath = path.join(keystoreDir, CONFIG.KEYSTORE_FILENAME);
  if (fs.existsSync(mnemonicPath)) {
    const decrypted = decryptKeystoreSync(mnemonicPath, password);
    if (decrypted) {
      try {
        const mnemonic = decrypted.toString('utf8');
        const chain = CONFIG.getChainConfig(chainId);

        if (!chain) {
          console.warn(`[Floppy] Unknown chain: ${chainId}, using ethereum`);
        }

        const derivationPath = chain ? chain.derivationPath : "m/44'/60'/0'/0";
        const { HDNodeWallet } = require('ethers');
        const wallet = HDNodeWallet.fromPhrase(mnemonic, undefined, `${derivationPath}/0`);
        console.log(`[Floppy] Loaded ${chain?.symbol || 'ETH'} wallet:`, wallet.address);
        return [wallet.privateKey];
      } catch (err) {
        console.warn('[Floppy] Failed to derive keys from mnemonic:', err.message);
        return [];
      }
    } else {
      console.warn('[Floppy] Invalid password for mnemonic keystore');
      return [];
    }
  }

  console.warn('[Floppy] No keystore found on disk');
  return [];
}

/**
 * Clear cached keys from memory
 */
function clearCache() {
  cachedMnemonic = null;
  cachedAdminKey = null;
  cachedChainKeys = {};
}

// Clear cache on process exit
process.on('exit', clearCache);
process.on('SIGINT', () => {
  clearCache();
  process.exit();
});
process.on('SIGTERM', () => {
  clearCache();
  process.exit();
});

module.exports = {
  // Async functions - Ethereum (backwards compatible)
  loadMnemonicFromFloppy,
  getFloppyPrivateKeys,
  loadAdminKeyFromFloppy,
  getAdminPrivateKey,

  // Multi-chain async functions
  deriveChainKeys,
  getChainPrivateKeys,
  getChainAddresses,

  // Sync functions (for Hardhat config)
  loadFloppyKeysSync,
  decryptKeystoreSync,

  // Status checks
  isFloppyMounted,
  keystoreExists,
  adminKeystoreExists,

  // Chain information
  getChainSummary,

  // Utility
  clearCache,
  CONFIG,

  // Paths
  KEYSTORE_PATH,
  ADMIN_KEYSTORE_PATH
};
