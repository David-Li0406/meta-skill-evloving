/**
 * Configuration for floppy disk keystore
 *
 * This module provides configuration for the floppy keystore skill.
 * All values can be overridden via environment variables.
 */

/**
 * Supported blockchain chains with their configurations
 * Based on SLIP-0044 registered coin types
 * @see https://github.com/satoshilabs/slips/blob/master/slip-0044.md
 */
const CHAINS = {
  // Ethereum and EVM-compatible chains
  ethereum: {
    name: 'Ethereum',
    symbol: 'ETH',
    coinType: 60,
    curve: 'secp256k1',
    derivationPath: "m/44'/60'/0'/0",
    addressPrefix: '0x',
    keyFormat: 'hex',
    networks: ['mainnet', 'sepolia', 'holesky', 'arbitrum', 'optimism', 'polygon', 'base']
  },

  // Bitcoin with multiple address types
  bitcoin: {
    name: 'Bitcoin',
    symbol: 'BTC',
    coinType: 0,
    curve: 'secp256k1',
    derivationPath: "m/84'/0'/0'/0",  // Native SegWit (bech32) by default
    addressPrefix: 'bc1',
    keyFormat: 'wif',
    networks: ['mainnet', 'testnet', 'signet'],
    // Additional derivation paths for different address types
    addressTypes: {
      legacy: { purpose: 44, prefix: '1', name: 'P2PKH (Legacy)' },
      segwit: { purpose: 49, prefix: '3', name: 'P2SH-SegWit' },
      nativeSegwit: { purpose: 84, prefix: 'bc1q', name: 'P2WPKH (Native SegWit)' },
      taproot: { purpose: 86, prefix: 'bc1p', name: 'P2TR (Taproot)' }
    }
  },

  // Zcash transparent addresses
  zcash: {
    name: 'Zcash',
    symbol: 'ZEC',
    coinType: 133,
    curve: 'secp256k1',
    derivationPath: "m/44'/133'/0'/0",
    addressPrefix: 't1',
    keyFormat: 'wif',
    networks: ['mainnet', 'testnet'],
    // Note: Sapling/Orchard shielded addresses require different derivation (ZIP-32)
    addressTypes: {
      transparent: { purpose: 44, prefix: 't1', name: 'Transparent (t-addr)' }
      // Shielded addresses (z-addr) would require ZIP-32 implementation
    }
  },

  // Monero - uses different key structure
  monero: {
    name: 'Monero',
    symbol: 'XMR',
    coinType: 128,
    curve: 'ed25519',
    derivationPath: "m/44'/128'/0'/0",
    addressPrefix: '4',  // Standard address
    keyFormat: 'hex',
    networks: ['mainnet', 'stagenet', 'testnet'],
    // Monero has unique key structure: spend key + view key
    keyTypes: {
      spend: 'Private Spend Key',
      view: 'Private View Key'
    },
    // Note: Monero native wallets use 25-word mnemonic (different from BIP-39)
    // This implementation derives from BIP-39 for compatibility
    nativeWordCount: 25
  },

  // Solana
  solana: {
    name: 'Solana',
    symbol: 'SOL',
    coinType: 501,
    curve: 'ed25519',
    derivationPath: "m/44'/501'/0'/0'",  // Note: Solana uses hardened at end
    addressPrefix: '',  // Base58 encoded, no prefix
    keyFormat: 'base58',
    networks: ['mainnet-beta', 'devnet', 'testnet']
  },

  // Ethereum Classic (uses same derivation as ETH but different coin type)
  ethereumClassic: {
    name: 'Ethereum Classic',
    symbol: 'ETC',
    coinType: 61,
    curve: 'secp256k1',
    derivationPath: "m/44'/61'/0'/0",
    addressPrefix: '0x',
    keyFormat: 'hex',
    networks: ['mainnet', 'mordor']
  }
};

/**
 * Chain aliases for convenience
 */
const CHAIN_ALIASES = {
  'eth': 'ethereum',
  'btc': 'bitcoin',
  'zec': 'zcash',
  'xmr': 'monero',
  'sol': 'solana',
  'etc': 'ethereumClassic'
};

/**
 * Get chain configuration by name or alias
 * @param {string} chainId - Chain name or alias
 * @returns {object|null} Chain configuration or null if not found
 */
function getChainConfig(chainId) {
  const normalized = chainId.toLowerCase();
  const resolved = CHAIN_ALIASES[normalized] || normalized;
  return CHAINS[resolved] || null;
}

/**
 * List all supported chains
 * @returns {string[]} Array of chain IDs
 */
function listChains() {
  return Object.keys(CHAINS);
}

module.exports = {
  // Floppy device path
  DEVICE: process.env.FLOPPY_DEVICE || '/dev/sde',

  // Mount point
  MOUNT_POINT: process.env.FLOPPY_MOUNT || '/mnt/floppy',

  // Keystore file paths on floppy
  KEYSTORE_DIR: '.keystore',
  KEYSTORE_FILENAME: 'mnemonic-keystore.json',
  ADMIN_KEYSTORE_FILENAME: 'admin-keystore.json',

  // KDF parameters (scrypt) - strong security
  SCRYPT_N: 262144,  // 2^18 - ~512MB memory
  SCRYPT_R: 8,
  SCRYPT_P: 1,
  SCRYPT_DKLEN: 32,

  // Admin key uses lower params for faster operation
  ADMIN_SCRYPT_N: 16384,  // 2^14 - ~16MB memory

  // Cipher
  CIPHER: 'aes-128-ctr',

  // Mount options for security
  MOUNT_OPTIONS: [
    'noexec',      // Prevent executable files
    'nosuid',      // Ignore setuid bits
    'nodev',       // Ignore device files
    'umask=077',   // Owner-only permissions (rwx------)
    'sync',        // Synchronous writes
    'flush'        // Flush frequently
  ],

  // Multi-chain support
  CHAINS,
  CHAIN_ALIASES,
  getChainConfig,
  listChains,

  // Default chain for backwards compatibility
  DEFAULT_CHAIN: 'ethereum'
};
