/**
 * Multi-chain key derivation module
 *
 * Derives private keys and addresses for multiple blockchain networks
 * from a single BIP-39 mnemonic phrase.
 *
 * Supported chains:
 * - Ethereum (ETH) and EVM-compatible chains
 * - Bitcoin (BTC) - Legacy, SegWit, Native SegWit, Taproot
 * - Zcash (ZEC) - Transparent addresses
 * - Monero (XMR) - Derived from BIP-39 (not native 25-word)
 * - Solana (SOL)
 * - Ethereum Classic (ETC)
 *
 * @module chains
 */

const crypto = require('crypto');
const { getChainConfig, CHAINS } = require('./config');

/**
 * Derive keys for a specific chain from a mnemonic
 *
 * @param {string} mnemonic - BIP-39 mnemonic phrase
 * @param {string} chainId - Chain identifier (e.g., 'ethereum', 'bitcoin', 'solana')
 * @param {object} options - Derivation options
 * @param {number} options.count - Number of accounts to derive (default: 1)
 * @param {number} options.startIndex - Starting index (default: 0)
 * @param {string} options.addressType - For Bitcoin: 'legacy', 'segwit', 'nativeSegwit', 'taproot'
 * @returns {Promise<Array<{privateKey: string, publicKey: string, address: string, path: string}>>}
 */
async function deriveKeys(mnemonic, chainId, options = {}) {
  const chain = getChainConfig(chainId);
  if (!chain) {
    throw new Error(`Unsupported chain: ${chainId}`);
  }

  const {
    count = 1,
    startIndex = 0,
    addressType = null
  } = options;

  switch (chain.curve) {
    case 'secp256k1':
      return deriveSecp256k1Keys(mnemonic, chain, { count, startIndex, addressType });
    case 'ed25519':
      return deriveEd25519Keys(mnemonic, chain, { count, startIndex });
    default:
      throw new Error(`Unsupported curve: ${chain.curve}`);
  }
}

/**
 * Derive secp256k1 keys (Ethereum, Bitcoin, Zcash, etc.)
 */
async function deriveSecp256k1Keys(mnemonic, chain, options) {
  const { HDNodeWallet } = require('ethers');
  const { count, startIndex, addressType } = options;

  const results = [];

  // Determine derivation path
  let basePath = chain.derivationPath;

  // For Bitcoin, handle different address types
  if (chain.symbol === 'BTC' && addressType && chain.addressTypes[addressType]) {
    const purpose = chain.addressTypes[addressType].purpose;
    basePath = `m/${purpose}'/${chain.coinType}'/0'/0`;
  }

  // Create master node from mnemonic (ethers v6 requires explicit root path)
  const masterNode = HDNodeWallet.fromPhrase(mnemonic, undefined, "m");

  for (let i = startIndex; i < startIndex + count; i++) {
    const path = `${basePath}/${i}`;
    const wallet = masterNode.derivePath(path);

    const result = {
      chain: chain.symbol,
      index: i,
      path: path,
      privateKey: wallet.privateKey,
      publicKey: wallet.publicKey,
      address: null
    };

    // Generate chain-specific address
    switch (chain.symbol) {
      case 'ETH':
      case 'ETC':
        result.address = wallet.address;
        break;

      case 'BTC':
        result.address = await deriveBitcoinAddress(wallet, addressType || 'nativeSegwit', chain);
        result.addressType = addressType || 'nativeSegwit';
        break;

      case 'ZEC':
        result.address = await deriveZcashAddress(wallet, chain);
        break;

      default:
        // For other secp256k1 chains, use ethereum-style address
        result.address = wallet.address;
    }

    results.push(result);
  }

  return results;
}

/**
 * Derive ed25519 keys (Solana, Monero)
 */
async function deriveEd25519Keys(mnemonic, chain, options) {
  const { count, startIndex } = options;

  switch (chain.symbol) {
    case 'SOL':
      return deriveSolanaKeys(mnemonic, chain, { count, startIndex });
    case 'XMR':
      return deriveMoneroKeys(mnemonic, chain, { count, startIndex });
    default:
      throw new Error(`Ed25519 derivation not implemented for ${chain.symbol}`);
  }
}

/**
 * Derive Solana keys using ed25519
 */
async function deriveSolanaKeys(mnemonic, chain, options) {
  const { count, startIndex } = options;
  const results = [];

  try {
    // Try to use @solana/web3.js if available
    const { Keypair } = require('@solana/web3.js');
    const { mnemonicToSeedSync } = require('bip39');
    const { derivePath } = require('ed25519-hd-key');

    const seed = mnemonicToSeedSync(mnemonic);

    for (let i = startIndex; i < startIndex + count; i++) {
      const path = `m/44'/501'/${i}'/0'`;
      const derived = derivePath(path, seed.toString('hex'));
      const keypair = Keypair.fromSeed(derived.key);

      results.push({
        chain: chain.symbol,
        index: i,
        path: path,
        privateKey: Buffer.from(keypair.secretKey).toString('hex'),
        publicKey: keypair.publicKey.toBase58(),
        address: keypair.publicKey.toBase58()
      });
    }
  } catch (err) {
    // Fallback: derive using basic ed25519 from seed
    const { mnemonicToSeedSync } = require('ethereum-cryptography/bip39');
    const { wordlist } = require('ethereum-cryptography/bip39/wordlists/english');

    const seed = mnemonicToSeedSync(mnemonic, wordlist);

    for (let i = startIndex; i < startIndex + count; i++) {
      const path = `m/44'/501'/${i}'/0'`;
      // Use HMAC-SHA512 to derive key material
      const derivedSeed = crypto.createHmac('sha512', `ed25519 seed`)
        .update(Buffer.concat([seed, Buffer.from(path)]))
        .digest();

      const privateKey = derivedSeed.slice(0, 32);

      results.push({
        chain: chain.symbol,
        index: i,
        path: path,
        privateKey: privateKey.toString('hex'),
        publicKey: '(requires @solana/web3.js)',
        address: '(requires @solana/web3.js)',
        note: 'Install @solana/web3.js and ed25519-hd-key for full Solana support'
      });
    }
  }

  return results;
}

/**
 * Derive Monero keys
 *
 * Monero uses a different key structure with spend key and view key.
 * This derives from BIP-39 mnemonic (not native Monero 25-word format).
 */
async function deriveMoneroKeys(mnemonic, chain, options) {
  const { count, startIndex } = options;
  const results = [];

  try {
    // Try to use monero-javascript if available
    const monerojs = require('monero-javascript');

    for (let i = startIndex; i < startIndex + count; i++) {
      // Derive seed from mnemonic + account index
      const accountSeed = crypto.createHash('sha256')
        .update(mnemonic + i.toString())
        .digest();

      const wallet = await monerojs.createWalletKeys({
        privateSpendKey: accountSeed.toString('hex')
      });

      results.push({
        chain: chain.symbol,
        index: i,
        path: `derived/${i}`,
        privateSpendKey: await wallet.getPrivateSpendKey(),
        privateViewKey: await wallet.getPrivateViewKey(),
        publicSpendKey: await wallet.getPublicSpendKey(),
        publicViewKey: await wallet.getPublicViewKey(),
        address: await wallet.getPrimaryAddress()
      });
    }
  } catch (err) {
    // Fallback: derive basic keys without full Monero library
    const { keccak256 } = require('ethereum-cryptography/keccak');

    for (let i = startIndex; i < startIndex + count; i++) {
      // Derive spend key from mnemonic
      const spendKeySeed = crypto.createHash('sha256')
        .update(mnemonic + ':spend:' + i.toString())
        .digest();

      // Reduce to valid ed25519 scalar (Monero-style)
      const spendKey = reduceScalar(spendKeySeed);

      // Derive view key: keccak256(spend_key) reduced
      const viewKeySeed = Buffer.from(keccak256(spendKey));
      const viewKey = reduceScalar(viewKeySeed);

      results.push({
        chain: chain.symbol,
        index: i,
        path: `derived/${i}`,
        privateSpendKey: spendKey.toString('hex'),
        privateViewKey: viewKey.toString('hex'),
        publicSpendKey: '(requires monero-javascript)',
        publicViewKey: '(requires monero-javascript)',
        address: '(requires monero-javascript)',
        note: 'Install monero-javascript for full Monero support'
      });
    }
  }

  return results;
}

/**
 * Reduce a 32-byte value to a valid ed25519 scalar (Monero-style)
 */
function reduceScalar(input) {
  // Monero uses a specific scalar reduction
  // This is a simplified version - full implementation requires curve operations
  const result = Buffer.from(input);
  result[0] &= 248;
  result[31] &= 127;
  result[31] |= 64;
  return result;
}

/**
 * Derive Bitcoin address from wallet
 */
async function deriveBitcoinAddress(wallet, addressType, chain) {
  try {
    const bitcoin = require('bitcoinjs-lib');
    const ecc = require('tiny-secp256k1');
    const { ECPairFactory } = require('ecpair');

    const ECPair = ECPairFactory(ecc);

    // Get private key bytes (remove 0x prefix)
    const privateKeyHex = wallet.privateKey.slice(2);
    const keyPair = ECPair.fromPrivateKey(Buffer.from(privateKeyHex, 'hex'));

    const network = bitcoin.networks.bitcoin;

    switch (addressType) {
      case 'legacy':
        // P2PKH address (starts with 1)
        const p2pkh = bitcoin.payments.p2pkh({
          pubkey: keyPair.publicKey,
          network
        });
        return p2pkh.address;

      case 'segwit':
        // P2SH-P2WPKH address (starts with 3)
        const p2sh = bitcoin.payments.p2sh({
          redeem: bitcoin.payments.p2wpkh({
            pubkey: keyPair.publicKey,
            network
          }),
          network
        });
        return p2sh.address;

      case 'nativeSegwit':
        // P2WPKH address (starts with bc1q)
        const p2wpkh = bitcoin.payments.p2wpkh({
          pubkey: keyPair.publicKey,
          network
        });
        return p2wpkh.address;

      case 'taproot':
        // P2TR address (starts with bc1p)
        const p2tr = bitcoin.payments.p2tr({
          internalPubkey: keyPair.publicKey.slice(1, 33),
          network
        });
        return p2tr.address;

      default:
        return deriveBitcoinAddressFallback(wallet, addressType);
    }
  } catch (err) {
    return deriveBitcoinAddressFallback(wallet, addressType);
  }
}

/**
 * Fallback Bitcoin address derivation without bitcoinjs-lib
 */
function deriveBitcoinAddressFallback(wallet, addressType) {
  const { ripemd160 } = require('ethereum-cryptography/ripemd160');
  const { sha256 } = require('ethereum-cryptography/sha256');

  // Get compressed public key
  const pubKeyHex = wallet.publicKey;

  // Hash160 = RIPEMD160(SHA256(pubkey))
  const pubKeyBytes = Buffer.from(pubKeyHex.slice(2), 'hex');
  const hash160 = ripemd160(sha256(pubKeyBytes));

  return `(requires bitcoinjs-lib for ${addressType} address, hash160: ${Buffer.from(hash160).toString('hex')})`;
}

/**
 * Derive Zcash transparent address
 */
async function deriveZcashAddress(wallet, chain) {
  try {
    // Try zcash library if available
    const zcash = require('zcash');
    // Implementation would go here
    return deriveBitcoinAddressFallback(wallet, 'legacy').replace('bitcoinjs-lib', 'zcash library');
  } catch (err) {
    // Fallback: Zcash t-addresses are similar to Bitcoin legacy
    const { ripemd160 } = require('ethereum-cryptography/ripemd160');
    const { sha256 } = require('ethereum-cryptography/sha256');

    const pubKeyBytes = Buffer.from(wallet.publicKey.slice(2), 'hex');
    const hash160 = ripemd160(sha256(pubKeyBytes));

    // Zcash mainnet t-address prefix is 0x1CB8
    return `(Zcash transparent, hash160: ${Buffer.from(hash160).toString('hex')})`;
  }
}

/**
 * Get a summary of supported chains and their features
 * @returns {object[]} Array of chain summaries
 */
function getChainSummary() {
  return Object.entries(CHAINS).map(([id, chain]) => ({
    id,
    name: chain.name,
    symbol: chain.symbol,
    curve: chain.curve,
    derivationPath: chain.derivationPath,
    networks: chain.networks,
    addressTypes: chain.addressTypes ? Object.keys(chain.addressTypes) : null
  }));
}

/**
 * Validate that a private key is valid for a specific chain
 * @param {string} privateKey - Private key to validate
 * @param {string} chainId - Chain identifier
 * @returns {boolean} True if valid
 */
function validatePrivateKey(privateKey, chainId) {
  const chain = getChainConfig(chainId);
  if (!chain) return false;

  // Remove 0x prefix if present
  const keyHex = privateKey.startsWith('0x') ? privateKey.slice(2) : privateKey;

  // Check length (32 bytes = 64 hex chars)
  if (keyHex.length !== 64) return false;

  // Check valid hex
  if (!/^[0-9a-fA-F]+$/.test(keyHex)) return false;

  // For secp256k1, check within curve order
  if (chain.curve === 'secp256k1') {
    const keyBigInt = BigInt('0x' + keyHex);
    const curveOrder = BigInt('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141');
    if (keyBigInt <= 0n || keyBigInt >= curveOrder) return false;
  }

  return true;
}

/**
 * Format a private key for a specific chain
 * @param {string} privateKey - Private key (hex)
 * @param {string} chainId - Chain identifier
 * @returns {string} Formatted private key
 */
function formatPrivateKey(privateKey, chainId) {
  const chain = getChainConfig(chainId);
  if (!chain) return privateKey;

  const keyHex = privateKey.startsWith('0x') ? privateKey.slice(2) : privateKey;

  switch (chain.keyFormat) {
    case 'hex':
      return '0x' + keyHex;

    case 'wif':
      // Would need bitcoinjs-lib for proper WIF encoding
      return '(WIF format requires bitcoinjs-lib)';

    case 'base58':
      // Would need bs58 for base58 encoding
      return '(Base58 format requires bs58)';

    default:
      return '0x' + keyHex;
  }
}

/**
 * Derive keys from an extended private key (xprv)
 * Used by clones that only have their branch, not the full mnemonic
 *
 * @param {string} xprv - Extended private key (base58)
 * @param {string} chainId - Chain identifier
 * @param {object} options - Derivation options
 * @param {number} options.count - Number of addresses to derive (default: 1)
 * @param {number} options.startIndex - Starting index (default: 0)
 * @returns {Promise<Array>} Derived keys
 */
async function deriveKeysFromXprv(xprv, chainId, options = {}) {
  const chain = getChainConfig(chainId);
  if (!chain) {
    throw new Error(`Unsupported chain: ${chainId}`);
  }

  // Only secp256k1 chains support xprv derivation (EVM chains)
  if (chain.curve !== 'secp256k1') {
    throw new Error(`xprv derivation not supported for ${chain.curve} chains`);
  }

  const { HDNodeWallet } = require('ethers');
  const { count = 1, startIndex = 0 } = options;

  // Parse xprv - it's already at account level (m/44'/60'/N')
  const hdNode = HDNodeWallet.fromExtendedKey(xprv);

  const results = [];

  for (let i = startIndex; i < startIndex + count; i++) {
    // Derive: account_xprv/0/address_index
    // The xprv is at m/44'/60'/N', so we add 0/i for external chain
    const wallet = hdNode.derivePath(`0/${i}`);

    const result = {
      chain: chain.symbol,
      index: i,
      path: `xprv/0/${i}`,
      privateKey: wallet.privateKey,
      publicKey: wallet.publicKey,
      address: wallet.address
    };

    // Handle ETC (Ethereum Classic) - same format as ETH
    if (chain.symbol === 'ETC') {
      result.network = chain.networks?.[0] || 'mainnet';
    }

    results.push(result);
  }

  return results;
}

module.exports = {
  deriveKeys,
  deriveKeysFromXprv,
  getChainSummary,
  validatePrivateKey,
  formatPrivateKey,

  // Export individual derivation functions for advanced use
  deriveSecp256k1Keys,
  deriveEd25519Keys,
  deriveSolanaKeys,
  deriveMoneroKeys,
  deriveBitcoinAddress,
  deriveZcashAddress
};
