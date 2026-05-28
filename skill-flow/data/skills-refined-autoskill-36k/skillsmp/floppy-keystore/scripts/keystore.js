/**
 * Ethereum-style keystore for mnemonic phrases
 * Adapts the Web3 Secret Storage Definition for mnemonic storage
 *
 * Security features:
 * - scrypt KDF with high N parameter (2^18)
 * - AES-128-CTR encryption
 * - keccak256 MAC for integrity verification
 * - Timing-safe comparison
 * - Memory clearing of sensitive data
 */
const crypto = require('crypto');
const { scrypt } = require('ethereum-cryptography/scrypt');
const { keccak256 } = require('ethereum-cryptography/keccak');
const { validateMnemonic } = require('ethereum-cryptography/bip39');
const { wordlist } = require('ethereum-cryptography/bip39/wordlists/english');
const { bytesToHex, hexToBytes, utf8ToBytes } = require('ethereum-cryptography/utils');
const CONFIG = require('./config');

/**
 * Encrypt a mnemonic phrase to keystore format
 * @param {string} mnemonic - BIP-39 mnemonic phrase (12 or 24 words)
 * @param {string} password - Encryption password
 * @returns {Promise<object>} Encrypted keystore JSON object
 */
async function encryptMnemonic(mnemonic, password) {
  // Normalize and validate mnemonic
  const normalizedMnemonic = mnemonic.trim().toLowerCase().replace(/\s+/g, ' ');
  const words = normalizedMnemonic.split(' ');

  if (words.length !== 12 && words.length !== 24) {
    throw new Error('Mnemonic must be 12 or 24 words');
  }

  if (!validateMnemonic(normalizedMnemonic, wordlist)) {
    throw new Error('Invalid mnemonic phrase - words not in BIP-39 wordlist or invalid checksum');
  }

  // Generate random salt and IV
  const salt = crypto.randomBytes(32);
  const iv = crypto.randomBytes(16);

  // Derive key using scrypt
  console.log('Deriving key (this may take a moment)...');
  const derivedKey = await scrypt(
    utf8ToBytes(password),
    salt,
    CONFIG.SCRYPT_N,
    CONFIG.SCRYPT_P,
    CONFIG.SCRYPT_R,
    CONFIG.SCRYPT_DKLEN
  );

  // Use first 16 bytes for AES-128
  const encryptionKey = derivedKey.slice(0, 16);

  // Encrypt the mnemonic using AES-128-CTR
  const cipher = crypto.createCipheriv('aes-128-ctr', encryptionKey, iv);
  const mnemonicBytes = Buffer.from(normalizedMnemonic, 'utf8');
  const ciphertext = Buffer.concat([cipher.update(mnemonicBytes), cipher.final()]);

  // Calculate MAC: keccak256(derivedKey[16:32] || ciphertext)
  const macInput = Buffer.concat([
    Buffer.from(derivedKey.slice(16, 32)),
    ciphertext
  ]);
  const mac = keccak256(macInput);

  // Clear sensitive data from memory
  encryptionKey.fill(0);
  mnemonicBytes.fill(0);

  return {
    version: 3,
    id: crypto.randomUUID(),
    type: 'mnemonic',
    wordCount: words.length,
    crypto: {
      cipher: CONFIG.CIPHER,
      cipherparams: { iv: iv.toString('hex') },
      ciphertext: ciphertext.toString('hex'),
      kdf: 'scrypt',
      kdfparams: {
        dklen: CONFIG.SCRYPT_DKLEN,
        n: CONFIG.SCRYPT_N,
        r: CONFIG.SCRYPT_R,
        p: CONFIG.SCRYPT_P,
        salt: salt.toString('hex')
      },
      mac: bytesToHex(mac)
    }
  };
}

/**
 * Decrypt a mnemonic from keystore format
 * @param {object} keystore - Keystore JSON object
 * @param {string} password - Decryption password
 * @returns {Promise<string>} Decrypted mnemonic phrase
 */
async function decryptMnemonic(keystore, password) {
  if (keystore.version !== 3) {
    throw new Error('Unsupported keystore version');
  }

  if (keystore.type !== 'mnemonic') {
    throw new Error('Keystore is not a mnemonic keystore');
  }

  const { crypto: cryptoParams } = keystore;

  if (cryptoParams.kdf !== 'scrypt') {
    throw new Error('Unsupported KDF: ' + cryptoParams.kdf);
  }

  // Parse hex values
  const salt = Buffer.from(cryptoParams.kdfparams.salt, 'hex');
  const iv = Buffer.from(cryptoParams.cipherparams.iv, 'hex');
  const ciphertext = Buffer.from(cryptoParams.ciphertext, 'hex');
  const expectedMac = hexToBytes(cryptoParams.mac);

  // Derive key using scrypt
  console.log('Deriving key (this may take a moment)...');
  const derivedKey = await scrypt(
    utf8ToBytes(password),
    salt,
    cryptoParams.kdfparams.n,
    cryptoParams.kdfparams.p,
    cryptoParams.kdfparams.r,
    cryptoParams.kdfparams.dklen
  );

  // Verify MAC
  const macInput = Buffer.concat([
    Buffer.from(derivedKey.slice(16, 32)),
    ciphertext
  ]);
  const computedMac = keccak256(macInput);

  if (!constantTimeCompare(computedMac, expectedMac)) {
    throw new Error('Invalid password or corrupted keystore');
  }

  // Decrypt
  const encryptionKey = derivedKey.slice(0, 16);
  const decipher = crypto.createDecipheriv('aes-128-ctr', encryptionKey, iv);
  const mnemonicBytes = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  const mnemonic = mnemonicBytes.toString('utf8');

  // Clear sensitive data
  encryptionKey.fill(0);

  // Validate decrypted mnemonic
  const words = mnemonic.split(' ');
  if (words.length !== keystore.wordCount) {
    throw new Error('Decrypted mnemonic word count mismatch');
  }

  if (!validateMnemonic(mnemonic, wordlist)) {
    throw new Error('Decrypted mnemonic is invalid');
  }

  return mnemonic;
}

/**
 * Constant-time comparison to prevent timing attacks
 * @param {Uint8Array} a
 * @param {Uint8Array} b
 * @returns {boolean}
 */
function constantTimeCompare(a, b) {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a[i] ^ b[i];
  }
  return result === 0;
}

/**
 * Encrypt an extended private key (xprv) to keystore format
 * Used for clones that only get their branch, not the full mnemonic
 *
 * @param {string} xprv - Extended private key (base58)
 * @param {string} password - Encryption password
 * @param {object} metadata - Additional metadata (cloneId, motherId, etc.)
 * @returns {Promise<object>} Encrypted keystore JSON object
 */
async function encryptXprv(xprv, password, metadata = {}) {
  // Validate xprv format (starts with xprv for mainnet or tprv for testnet)
  if (!xprv.startsWith('xprv') && !xprv.startsWith('tprv')) {
    throw new Error('Invalid extended private key format');
  }

  // Generate random salt and IV
  const salt = crypto.randomBytes(32);
  const iv = crypto.randomBytes(16);

  // Derive key using scrypt
  console.log('Deriving key (this may take a moment)...');
  const derivedKey = await scrypt(
    utf8ToBytes(password),
    salt,
    CONFIG.SCRYPT_N,
    CONFIG.SCRYPT_P,
    CONFIG.SCRYPT_R,
    CONFIG.SCRYPT_DKLEN
  );

  // Use first 16 bytes for AES-128
  const encryptionKey = derivedKey.slice(0, 16);

  // Encrypt the xprv using AES-128-CTR
  const cipher = crypto.createCipheriv('aes-128-ctr', encryptionKey, iv);
  const xprvBytes = Buffer.from(xprv, 'utf8');
  const ciphertext = Buffer.concat([cipher.update(xprvBytes), cipher.final()]);

  // Calculate MAC: keccak256(derivedKey[16:32] || ciphertext)
  const macInput = Buffer.concat([
    Buffer.from(derivedKey.slice(16, 32)),
    ciphertext
  ]);
  const mac = keccak256(macInput);

  // Clear sensitive data from memory
  encryptionKey.fill(0);
  xprvBytes.fill(0);

  return {
    version: 3,
    id: crypto.randomUUID(),
    type: 'xprv',  // Different from 'mnemonic'
    crypto: {
      cipher: CONFIG.CIPHER,
      cipherparams: { iv: iv.toString('hex') },
      ciphertext: ciphertext.toString('hex'),
      kdf: 'scrypt',
      kdfparams: {
        dklen: CONFIG.SCRYPT_DKLEN,
        n: CONFIG.SCRYPT_N,
        r: CONFIG.SCRYPT_R,
        p: CONFIG.SCRYPT_P,
        salt: salt.toString('hex')
      },
      mac: bytesToHex(mac)
    },
    // Clone-specific metadata
    clone: {
      cloneId: metadata.cloneId || null,
      motherId: metadata.motherId || null,
      derivationIndex: metadata.derivationIndex || 0,
      derivationPath: metadata.derivationPath || null,
      xprvHash: bytesToHex(keccak256(utf8ToBytes(xprv))), // For verification
      createdAt: new Date().toISOString(),
      expiresAt: metadata.expiresAt || null,
      birthCertificate: metadata.birthCertificate || null
    }
  };
}

/**
 * Decrypt an extended private key from keystore format
 * @param {object} keystore - Keystore JSON object
 * @param {string} password - Decryption password
 * @returns {Promise<string>} Decrypted xprv
 */
async function decryptXprv(keystore, password) {
  if (keystore.version !== 3) {
    throw new Error('Unsupported keystore version');
  }

  if (keystore.type !== 'xprv') {
    throw new Error('Keystore is not an xprv keystore');
  }

  const { crypto: cryptoParams } = keystore;

  if (cryptoParams.kdf !== 'scrypt') {
    throw new Error('Unsupported KDF: ' + cryptoParams.kdf);
  }

  // Parse hex values
  const salt = Buffer.from(cryptoParams.kdfparams.salt, 'hex');
  const iv = Buffer.from(cryptoParams.cipherparams.iv, 'hex');
  const ciphertext = Buffer.from(cryptoParams.ciphertext, 'hex');
  const expectedMac = hexToBytes(cryptoParams.mac);

  // Derive key using scrypt
  console.log('Deriving key (this may take a moment)...');
  const derivedKey = await scrypt(
    utf8ToBytes(password),
    salt,
    cryptoParams.kdfparams.n,
    cryptoParams.kdfparams.p,
    cryptoParams.kdfparams.r,
    cryptoParams.kdfparams.dklen
  );

  // Verify MAC
  const macInput = Buffer.concat([
    Buffer.from(derivedKey.slice(16, 32)),
    ciphertext
  ]);
  const computedMac = keccak256(macInput);

  if (!constantTimeCompare(computedMac, expectedMac)) {
    throw new Error('Invalid password or corrupted keystore');
  }

  // Decrypt
  const encryptionKey = derivedKey.slice(0, 16);
  const decipher = crypto.createDecipheriv('aes-128-ctr', encryptionKey, iv);
  const xprvBytes = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
  const xprv = xprvBytes.toString('utf8');

  // Clear sensitive data
  encryptionKey.fill(0);

  // Validate decrypted xprv format
  if (!xprv.startsWith('xprv') && !xprv.startsWith('tprv')) {
    throw new Error('Decrypted data is not a valid extended private key');
  }

  return xprv;
}

/**
 * Check if keystore is xprv type (clone) vs mnemonic type (mother)
 * @param {object} keystore - Keystore JSON object
 * @returns {string} 'xprv', 'mnemonic', or 'unknown'
 */
function getKeystoreType(keystore) {
  if (keystore.type === 'xprv') return 'xprv';
  if (keystore.type === 'mnemonic') return 'mnemonic';
  return 'unknown';
}

module.exports = {
  encryptMnemonic,
  decryptMnemonic,
  encryptXprv,
  decryptXprv,
  getKeystoreType,
  constantTimeCompare
};
