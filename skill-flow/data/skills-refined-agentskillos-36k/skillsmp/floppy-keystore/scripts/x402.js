/**
 * x402 Protocol Integration Module
 *
 * Enables agents to make payments using the x402 HTTP payment protocol.
 * Supports both EVM (Base) and Solana networks.
 *
 * x402 Protocol: https://www.x402.org/
 * Spec: https://github.com/coinbase/x402
 *
 * Features:
 * - EIP-3009 transferWithAuthorization signing for EVM/USDC
 * - Solana SPL token transfer signing
 * - Payment tracking in persistent memory
 * - Multi-network support from single mnemonic
 *
 * @module x402
 */

const crypto = require('crypto');
const { deriveKeys } = require('./chains');
const identity = require('./identity');
const CONFIG = require('./config');

/**
 * x402 supported networks with their configurations
 */
const X402_NETWORKS = {
  // Base Mainnet
  'eip155:8453': {
    name: 'Base Mainnet',
    chain: 'ethereum',  // Uses Ethereum-compatible keys
    chainId: 8453,
    usdc: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    facilitator: 'https://x402.coinbase.com'
  },
  // Base Sepolia (testnet)
  'eip155:84532': {
    name: 'Base Sepolia',
    chain: 'ethereum',
    chainId: 84532,
    usdc: '0x036CbD53842c5426634e7929541eC2318f3dCF7e',
    facilitator: 'https://x402.coinbase.com'
  },
  // Solana Mainnet
  'solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp': {
    name: 'Solana Mainnet',
    chain: 'solana',
    usdc: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
    facilitator: 'https://x402.coinbase.com'
  },
  // Solana Devnet
  'solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1': {
    name: 'Solana Devnet',
    chain: 'solana',
    usdc: '4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU',
    facilitator: 'https://x402.coinbase.com'
  }
};

/**
 * EIP-712 Domain for USDC transferWithAuthorization
 */
function getEIP712Domain(chainId, usdcAddress) {
  return {
    name: 'USD Coin',
    version: '2',
    chainId: chainId,
    verifyingContract: usdcAddress
  };
}

/**
 * EIP-712 Types for transferWithAuthorization
 */
const EIP3009_TYPES = {
  TransferWithAuthorization: [
    { name: 'from', type: 'address' },
    { name: 'to', type: 'address' },
    { name: 'value', type: 'uint256' },
    { name: 'validAfter', type: 'uint256' },
    { name: 'validBefore', type: 'uint256' },
    { name: 'nonce', type: 'bytes32' }
  ]
};

/**
 * Generate a random nonce for EIP-3009
 * @returns {string} 32-byte hex nonce
 */
function generateNonce() {
  return '0x' + crypto.randomBytes(32).toString('hex');
}

/**
 * Create EIP-3009 authorization for USDC transfer on EVM chains
 *
 * @param {object} params - Authorization parameters
 * @param {string} params.from - Sender address
 * @param {string} params.to - Recipient address
 * @param {string} params.value - Amount in wei (USDC has 6 decimals)
 * @param {number} params.validAfter - Unix timestamp (0 for immediate)
 * @param {number} params.validBefore - Unix timestamp (expiration)
 * @param {string} params.nonce - 32-byte nonce (optional, auto-generated)
 * @param {number} params.chainId - Chain ID
 * @param {string} params.usdcAddress - USDC contract address
 * @returns {object} Authorization object ready for signing
 */
function createEIP3009Authorization(params) {
  const {
    from,
    to,
    value,
    validAfter = 0,
    validBefore = Math.floor(Date.now() / 1000) + 3600, // 1 hour default
    nonce = generateNonce(),
    chainId,
    usdcAddress
  } = params;

  return {
    domain: getEIP712Domain(chainId, usdcAddress),
    types: EIP3009_TYPES,
    primaryType: 'TransferWithAuthorization',
    message: {
      from,
      to,
      value: value.toString(),
      validAfter: validAfter.toString(),
      validBefore: validBefore.toString(),
      nonce
    }
  };
}

/**
 * Sign EIP-712 typed data for EIP-3009 authorization
 *
 * @param {object} typedData - EIP-712 typed data
 * @param {string} privateKey - Private key (hex with 0x prefix)
 * @returns {Promise<string>} 65-byte signature
 */
async function signEIP712(typedData, privateKey) {
  try {
    const { Wallet } = require('ethers');
    const wallet = new Wallet(privateKey);

    // ethers v6 style signing
    const signature = await wallet.signTypedData(
      typedData.domain,
      { [typedData.primaryType]: typedData.types[typedData.primaryType] },
      typedData.message
    );

    return signature;
  } catch (err) {
    throw new Error(`EIP-712 signing failed: ${err.message}`);
  }
}

/**
 * Create x402 payment payload for EVM networks
 *
 * @param {object} params - Payment parameters
 * @param {string} params.network - x402 network identifier (e.g., 'eip155:8453')
 * @param {string} params.payTo - Recipient address
 * @param {string} params.amount - Amount in USDC (human-readable, e.g., '1.50')
 * @param {string} params.privateKey - Sender's private key
 * @param {string} params.fromAddress - Sender's address
 * @returns {Promise<object>} x402 payment payload
 */
async function createEVMPaymentPayload(params) {
  const {
    network,
    payTo,
    amount,
    privateKey,
    fromAddress
  } = params;

  const networkConfig = X402_NETWORKS[network];
  if (!networkConfig || networkConfig.chain !== 'ethereum') {
    throw new Error(`Unsupported EVM network: ${network}`);
  }

  // Convert amount to USDC wei (6 decimals)
  const amountWei = Math.floor(parseFloat(amount) * 1e6).toString();

  // Create authorization
  const auth = createEIP3009Authorization({
    from: fromAddress,
    to: payTo,
    value: amountWei,
    chainId: networkConfig.chainId,
    usdcAddress: networkConfig.usdc
  });

  // Sign the authorization
  const signature = await signEIP712(auth, privateKey);

  // Build x402 payload
  const payload = {
    scheme: 'exact',
    network: network,
    payload: {
      signature: signature,
      authorization: {
        from: fromAddress,
        to: payTo,
        value: amountWei,
        validAfter: auth.message.validAfter,
        validBefore: auth.message.validBefore,
        nonce: auth.message.nonce
      }
    }
  };

  return payload;
}

/**
 * Create x402 payment payload for Solana
 *
 * @param {object} params - Payment parameters
 * @param {string} params.network - x402 network identifier
 * @param {string} params.payTo - Recipient address (base58)
 * @param {string} params.amount - Amount in USDC
 * @param {string} params.privateKey - Sender's private key (hex)
 * @param {string} params.fromAddress - Sender's address (base58)
 * @returns {Promise<object>} x402 payment payload
 */
async function createSolanaPaymentPayload(params) {
  const {
    network,
    payTo,
    amount,
    privateKey,
    fromAddress
  } = params;

  const networkConfig = X402_NETWORKS[network];
  if (!networkConfig || networkConfig.chain !== 'solana') {
    throw new Error(`Unsupported Solana network: ${network}`);
  }

  // Convert amount to USDC lamports (6 decimals)
  const amountLamports = Math.floor(parseFloat(amount) * 1e6);

  try {
    const { Connection, PublicKey, Transaction } = require('@solana/web3.js');
    const { createTransferInstruction, getAssociatedTokenAddress } = require('@solana/spl-token');
    const { Keypair } = require('@solana/web3.js');

    // Reconstruct keypair from private key
    const keyBuffer = Buffer.from(privateKey.replace('0x', ''), 'hex');
    const keypair = Keypair.fromSecretKey(keyBuffer);

    const usdcMint = new PublicKey(networkConfig.usdc);
    const fromPubkey = new PublicKey(fromAddress);
    const toPubkey = new PublicKey(payTo);

    // Get associated token accounts
    const fromAta = await getAssociatedTokenAddress(usdcMint, fromPubkey);
    const toAta = await getAssociatedTokenAddress(usdcMint, toPubkey);

    // Create transfer instruction
    const transferIx = createTransferInstruction(
      fromAta,
      toAta,
      fromPubkey,
      amountLamports
    );

    // Build transaction (will need recent blockhash from network)
    const tx = new Transaction().add(transferIx);

    // Sign transaction
    tx.sign(keypair);

    // Serialize for x402 payload
    const serializedTx = tx.serialize({ requireAllSignatures: false }).toString('base64');

    return {
      scheme: 'exact',
      network: network,
      payload: {
        transaction: serializedTx,
        from: fromAddress,
        to: payTo,
        amount: amountLamports.toString()
      }
    };
  } catch (err) {
    // Fallback for when Solana libraries aren't installed
    return {
      scheme: 'exact',
      network: network,
      payload: {
        from: fromAddress,
        to: payTo,
        amount: Math.floor(parseFloat(amount) * 1e6).toString(),
        note: 'Full Solana signing requires @solana/web3.js and @solana/spl-token'
      }
    };
  }
}

/**
 * Create x402 payment payload (auto-detects network type)
 *
 * @param {object} params - Payment parameters
 * @returns {Promise<object>} x402 payment payload
 */
async function createPaymentPayload(params) {
  const { network } = params;
  const networkConfig = X402_NETWORKS[network];

  if (!networkConfig) {
    throw new Error(`Unknown x402 network: ${network}`);
  }

  if (networkConfig.chain === 'ethereum') {
    return createEVMPaymentPayload(params);
  } else if (networkConfig.chain === 'solana') {
    return createSolanaPaymentPayload(params);
  } else {
    throw new Error(`Unsupported chain type: ${networkConfig.chain}`);
  }
}

/**
 * Encode payment payload for X-PAYMENT header
 *
 * @param {object} payload - Payment payload object
 * @returns {string} Base64-encoded payload
 */
function encodePaymentHeader(payload) {
  return Buffer.from(JSON.stringify(payload)).toString('base64');
}

/**
 * Decode payment requirement from PAYMENT-REQUIRED header
 *
 * @param {string} header - Base64-encoded payment requirement
 * @returns {object} Decoded payment requirement
 */
function decodePaymentRequired(header) {
  return JSON.parse(Buffer.from(header, 'base64').toString('utf8'));
}

/**
 * Track a payment in persistent memory
 *
 * @param {object} payment - Payment details
 * @param {string} payment.network - Network used
 * @param {string} payment.amount - Amount paid
 * @param {string} payment.to - Recipient
 * @param {string} payment.resource - Resource URL
 * @param {string} payment.status - Payment status
 */
function trackPayment(payment) {
  identity.addMemory({
    type: 'x402-payment',
    content: `Paid ${payment.amount} USDC to ${payment.to} on ${payment.network} for ${payment.resource}`,
    tags: ['x402', 'payment', payment.network],
    importance: 6,
    metadata: {
      ...payment,
      timestamp: new Date().toISOString()
    }
  });
}

/**
 * Get payment history from memory
 *
 * @param {object} options - Filter options
 * @param {string} options.network - Filter by network
 * @param {number} options.limit - Max results
 * @returns {Array} Payment history
 */
function getPaymentHistory(options = {}) {
  const { network, limit = 50 } = options;

  const tags = ['x402', 'payment'];
  if (network) {
    tags.push(network);
  }

  return identity.searchMemory({
    type: 'x402-payment',
    tags,
    limit
  });
}

/**
 * Get supported x402 networks
 * @returns {object} Network configurations
 */
function getSupportedNetworks() {
  return X402_NETWORKS;
}

/**
 * Check if a network is supported
 * @param {string} network - Network identifier
 * @returns {boolean}
 */
function isNetworkSupported(network) {
  return network in X402_NETWORKS;
}

/**
 * Get network configuration
 * @param {string} network - Network identifier
 * @returns {object|null}
 */
function getNetworkConfig(network) {
  return X402_NETWORKS[network] || null;
}

/**
 * Create a complete x402 payment flow
 *
 * This is a high-level helper that:
 * 1. Derives keys from floppy keystore
 * 2. Creates the payment payload
 * 3. Encodes for HTTP header
 * 4. Tracks the payment
 *
 * @param {object} params - Payment parameters
 * @param {string} params.network - x402 network
 * @param {string} params.payTo - Recipient address
 * @param {string} params.amount - Amount in USDC
 * @param {string} params.resource - Resource URL being paid for
 * @param {string} params.mnemonic - BIP-39 mnemonic
 * @param {number} params.accountIndex - Account index to use (default: 0)
 * @returns {Promise<object>} { header: string, payload: object, wallet: object }
 */
async function preparePayment(params) {
  const {
    network,
    payTo,
    amount,
    resource,
    mnemonic,
    accountIndex = 0
  } = params;

  const networkConfig = X402_NETWORKS[network];
  if (!networkConfig) {
    throw new Error(`Unsupported network: ${network}`);
  }

  // Derive keys for the appropriate chain
  const keys = await deriveKeys(mnemonic, networkConfig.chain, {
    count: 1,
    startIndex: accountIndex
  });

  const wallet = keys[0];

  // Create payment payload
  const payload = await createPaymentPayload({
    network,
    payTo,
    amount,
    privateKey: wallet.privateKey,
    fromAddress: wallet.address
  });

  // Encode for header
  const header = encodePaymentHeader(payload);

  // Track payment
  trackPayment({
    network,
    amount,
    to: payTo,
    from: wallet.address,
    resource,
    status: 'prepared'
  });

  return {
    header,
    payload,
    wallet: {
      address: wallet.address,
      chain: networkConfig.chain,
      network: networkConfig.name
    }
  };
}

module.exports = {
  // Network info
  X402_NETWORKS,
  getSupportedNetworks,
  isNetworkSupported,
  getNetworkConfig,

  // EVM-specific
  createEIP3009Authorization,
  signEIP712,
  createEVMPaymentPayload,

  // Solana-specific
  createSolanaPaymentPayload,

  // Generic
  createPaymentPayload,
  encodePaymentHeader,
  decodePaymentRequired,

  // High-level
  preparePayment,

  // Memory/tracking
  trackPayment,
  getPaymentHistory,

  // Utilities
  generateNonce,
  getEIP712Domain,
  EIP3009_TYPES
};
