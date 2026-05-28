#!/usr/bin/env node
/**
 * Floppy Disk Keystore Manager CLI
 *
 * Multi-chain key management from encrypted floppy disk storage.
 *
 * Commands:
 *   mount           - Mount the floppy disk securely
 *   unmount         - Sync and unmount the floppy disk
 *   create          - Create a new encrypted mnemonic keystore
 *   test            - Test keystore decryption
 *   info            - Show keystore information
 *   chains          - List supported blockchain chains
 *   derive <chain>  - Derive keys for a specific chain
 *   address <chain> - Show addresses for a specific chain
 *   help            - Show this help message
 */
const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { execSync } = require('child_process');
const { encryptMnemonic, decryptMnemonic, decryptXprv, getKeystoreType } = require('./keystore');
const { deriveKeys, deriveKeysFromXprv, getChainSummary } = require('./chains');
const identity = require('./identity');
const integrity = require('./integrity');
const cloneModule = require('./clone');
const registry = require('./registry');
const CONFIG = require('./config');

const KEYSTORE_PATH = path.join(
  CONFIG.MOUNT_POINT,
  CONFIG.KEYSTORE_DIR,
  CONFIG.KEYSTORE_FILENAME
);

const IDENTITY_DIR = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR, 'identity');

/**
 * Resolve password from env vars with auto-detection
 * Checks FLOPPY_KEYSTORE_PASSWORD first, then FLOPPY_<DISKNAME>_PASSWORD
 */
function resolvePassword() {
  // Check explicit password first
  if (process.env.FLOPPY_KEYSTORE_PASSWORD) {
    return process.env.FLOPPY_KEYSTORE_PASSWORD;
  }

  // Try to auto-detect from disk metadata
  const metadataPath = path.join(IDENTITY_DIR, 'metadata.json');
  if (fs.existsSync(metadataPath)) {
    try {
      const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
      const diskName = metadata['disk.name'];
      if (diskName) {
        // Normalize disk name for env var: uppercase, replace hyphens/spaces with underscores
        const normalizedName = diskName.toUpperCase().replace(/[-\s]/g, '_');
        const envKey = `FLOPPY_${normalizedName}_PASSWORD`;
        if (process.env[envKey]) {
          return process.env[envKey];
        }
      }
    } catch (e) {
      // Ignore metadata read errors
    }
  }

  return null;
}

/**
 * Prompt for password without echoing
 */
function promptPassword(prompt) {
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
 * Prompt for text input
 */
function promptInput(prompt) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    rl.question(prompt, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

/**
 * Check if floppy is mounted
 */
function isMounted() {
  try {
    execSync(`mountpoint -q "${CONFIG.MOUNT_POINT}"`, { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

/**
 * Mount the floppy disk
 */
function mountFloppy() {
  const scriptPath = path.join(__dirname, 'mount.sh');
  execSync(`bash "${scriptPath}"`, { stdio: 'inherit' });
}

/**
 * Unmount the floppy disk
 */
function unmountFloppy() {
  const scriptPath = path.join(__dirname, 'unmount.sh');
  execSync(`bash "${scriptPath}"`, { stdio: 'inherit' });
}

/**
 * Create a new encrypted keystore
 */
async function createKeystore() {
  if (!isMounted()) {
    console.log('Mounting floppy disk...');
    mountFloppy();
  }

  if (fs.existsSync(KEYSTORE_PATH)) {
    console.error('Error: Keystore already exists at', KEYSTORE_PATH);
    console.error('Remove it first to create a new one.');
    process.exit(1);
  }

  console.log('\n=== Create Encrypted Mnemonic Keystore ===\n');
  console.log('This mnemonic will be used to derive keys for ALL supported chains:');
  console.log('  - Ethereum (ETH) and EVM chains');
  console.log('  - Bitcoin (BTC) - Legacy, SegWit, Taproot');
  console.log('  - Zcash (ZEC) - Transparent addresses');
  console.log('  - Monero (XMR) - Derived from BIP-39');
  console.log('  - Solana (SOL)');
  console.log('');
  console.log('Enter your BIP-39 mnemonic phrase (12 or 24 words):');

  const mnemonic = await promptInput('> ');

  const password = await promptPassword('Enter encryption password (min 8 chars): ');

  if (password.length < 8) {
    console.error('Error: Password must be at least 8 characters');
    process.exit(1);
  }

  const passwordConfirm = await promptPassword('Confirm password: ');

  if (password !== passwordConfirm) {
    console.error('Error: Passwords do not match');
    process.exit(1);
  }

  console.log('\nEncrypting mnemonic...');

  try {
    const keystore = await encryptMnemonic(mnemonic, password);

    // Create keystore directory if needed
    const keystoreDir = path.dirname(KEYSTORE_PATH);
    if (!fs.existsSync(keystoreDir)) {
      fs.mkdirSync(keystoreDir, { mode: 0o700, recursive: true });
    }

    // Write keystore with restricted permissions
    fs.writeFileSync(
      KEYSTORE_PATH,
      JSON.stringify(keystore, null, 2),
      { mode: 0o600 }
    );

    // Sync to ensure data is written to floppy
    execSync('sync');

    console.log('\nKeystore created successfully!');
    console.log('Location:', KEYSTORE_PATH);
    console.log('Word count:', keystore.wordCount);
    console.log('ID:', keystore.id);
    console.log('\nYou can now derive keys for any supported chain.');
    console.log('Run: node cli.js chains  - to see supported chains');
    console.log('Run: node cli.js derive ethereum  - to derive Ethereum keys');
    console.log('\nRemember to unmount the floppy when done.');

  } catch (error) {
    console.error('Error creating keystore:', error.message);
    process.exit(1);
  }
}

/**
 * Test keystore decryption
 */
async function testKeystore() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    console.error('Run mount command first');
    process.exit(1);
  }

  if (!fs.existsSync(KEYSTORE_PATH)) {
    console.error('Error: Keystore not found at', KEYSTORE_PATH);
    process.exit(1);
  }

  console.log('\n=== Test Keystore Decryption ===\n');

  const keystoreJson = fs.readFileSync(KEYSTORE_PATH, 'utf8');
  const keystore = JSON.parse(keystoreJson);

  console.log('Keystore ID:', keystore.id);
  console.log('Word count:', keystore.wordCount);

  const password = await promptPassword('Enter keystore password: ');

  try {
    console.log('\nDecrypting...');
    const mnemonic = await decryptMnemonic(keystore, password);

    console.log('\nDecryption successful!');
    console.log('Word count verified:', mnemonic.split(' ').length);

  } catch (error) {
    console.error('\nDecryption failed:', error.message);
    process.exit(1);
  }
}

/**
 * Show keystore info
 */
function showInfo() {
  console.log('\n=== Floppy Keystore Info ===\n');

  if (!isMounted()) {
    console.log('Floppy status: NOT MOUNTED');
    console.log('Run mount command to access keystore');
    return;
  }

  console.log('Floppy status: MOUNTED at', CONFIG.MOUNT_POINT);

  // Check mnemonic keystore
  if (!fs.existsSync(KEYSTORE_PATH)) {
    console.log('\nMnemonic keystore: NOT FOUND');
  } else {
    const keystoreJson = fs.readFileSync(KEYSTORE_PATH, 'utf8');
    const keystore = JSON.parse(keystoreJson);

    console.log('\nMnemonic keystore: FOUND');
    console.log('  ID:', keystore.id);
    console.log('  Type:', keystore.type);
    console.log('  Word count:', keystore.wordCount);
    console.log('  KDF:', keystore.crypto.kdf);
    console.log('  Cipher:', keystore.crypto.cipher);
  }

  // Check admin keystore
  const adminKeystorePath = path.join(
    CONFIG.MOUNT_POINT,
    CONFIG.KEYSTORE_DIR,
    CONFIG.ADMIN_KEYSTORE_FILENAME
  );

  if (!fs.existsSync(adminKeystorePath)) {
    console.log('\nAdmin keystore: NOT FOUND');
  } else {
    const keystoreJson = fs.readFileSync(adminKeystorePath, 'utf8');
    const keystore = JSON.parse(keystoreJson);

    console.log('\nAdmin keystore: FOUND');
    console.log('  Type:', keystore.type);
    console.log('  Address:', keystore.address);
    console.log('  Created:', keystore.meta?.createdAt || 'unknown');
  }

  console.log('\n=== Supported Chains ===\n');
  const chains = getChainSummary();
  chains.forEach(chain => {
    console.log(`  ${chain.symbol.padEnd(5)} - ${chain.name} (${chain.curve})`);
  });
}

/**
 * List supported chains
 */
function listChains() {
  console.log('\n=== Supported Blockchain Chains ===\n');

  const chains = getChainSummary();

  chains.forEach(chain => {
    console.log(`${chain.name} (${chain.symbol})`);
    console.log(`  ID:         ${chain.id}`);
    console.log(`  Curve:      ${chain.curve}`);
    console.log(`  Path:       ${chain.derivationPath}`);
    console.log(`  Networks:   ${chain.networks.join(', ')}`);
    if (chain.addressTypes) {
      console.log(`  Addr Types: ${chain.addressTypes.join(', ')}`);
    }
    console.log('');
  });

  console.log('Aliases:');
  Object.entries(CONFIG.CHAIN_ALIASES).forEach(([alias, chain]) => {
    console.log(`  ${alias} -> ${chain}`);
  });
}

/**
 * Derive keys for a specific chain
 */
async function deriveChainKeys(chainId, options = {}) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  if (!fs.existsSync(KEYSTORE_PATH)) {
    console.error('Error: Keystore not found');
    process.exit(1);
  }

  const chain = CONFIG.getChainConfig(chainId);
  if (!chain) {
    console.error(`Error: Unknown chain '${chainId}'`);
    console.error('Run: node cli.js chains  - to see supported chains');
    process.exit(1);
  }

  console.log(`\n=== Derive ${chain.name} (${chain.symbol}) Keys ===\n`);

  // Get password
  let password = resolvePassword();
  if (!password) {
    password = await promptPassword('Enter keystore password: ');
  }

  // Decrypt keystore
  const keystoreJson = fs.readFileSync(KEYSTORE_PATH, 'utf8');
  const keystore = JSON.parse(keystoreJson);
  const keystoreType = getKeystoreType(keystore);

  // Parse options
  const count = parseInt(options.count) || 1;
  const startIndex = parseInt(options.start) || 0;
  const addressType = options.type || null;

  let keys;

  try {
    if (keystoreType === 'xprv') {
      // Clone disk - derive from xprv
      console.log('\nDecrypting xprv (clone disk)...');
      const xprv = await decryptXprv(keystore, password);

      console.log(`\nDeriving ${count} key(s) starting at index ${startIndex}...`);
      console.log('(Derivation limited to this clone\'s account branch)');

      keys = await deriveKeysFromXprv(xprv, chainId, { count, startIndex });
    } else {
      // Mother disk - derive from mnemonic
      console.log('\nDecrypting mnemonic...');
      const mnemonic = await decryptMnemonic(keystore, password);

      console.log(`\nDeriving ${count} key(s) starting at index ${startIndex}...`);
      if (addressType) {
        console.log(`Address type: ${addressType}`);
      }

      keys = await deriveKeys(mnemonic, chainId, { count, startIndex, addressType });
    }

    console.log('\n--- Derived Keys ---\n');

    keys.forEach((key, i) => {
      console.log(`Account ${key.index}:`);
      console.log(`  Path:    ${key.path}`);
      console.log(`  Address: ${key.address}`);

      // For Monero, show both keys
      if (key.privateSpendKey) {
        console.log(`  Spend Key: ${key.privateSpendKey.slice(0, 16)}...`);
        console.log(`  View Key:  ${key.privateViewKey.slice(0, 16)}...`);
      } else {
        console.log(`  Private: ${key.privateKey.slice(0, 16)}...`);
      }

      if (key.addressType) {
        console.log(`  Type:    ${key.addressType}`);
      }
      if (key.note) {
        console.log(`  Note:    ${key.note}`);
      }
      console.log('');
    });

  } catch (error) {
    console.error('Error deriving keys:', error.message);
    process.exit(1);
  }
}

/**
 * Show addresses for a chain (without showing private keys)
 */
async function showAddresses(chainId, options = {}) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  if (!fs.existsSync(KEYSTORE_PATH)) {
    console.error('Error: Keystore not found');
    process.exit(1);
  }

  const chain = CONFIG.getChainConfig(chainId);
  if (!chain) {
    console.error(`Error: Unknown chain '${chainId}'`);
    process.exit(1);
  }

  console.log(`\n=== ${chain.name} (${chain.symbol}) Addresses ===\n`);

  let password = resolvePassword();
  if (!password) {
    password = await promptPassword('Enter keystore password: ');
  }

  const keystoreJson = fs.readFileSync(KEYSTORE_PATH, 'utf8');
  const keystore = JSON.parse(keystoreJson);
  const keystoreType = getKeystoreType(keystore);

  console.log('\nDecrypting...');

  const count = parseInt(options.count) || 5;
  const startIndex = parseInt(options.start) || 0;
  const addressType = options.type || null;

  try {
    let keys;

    if (keystoreType === 'xprv') {
      // Clone disk - derive from xprv
      console.log('(Clone disk - deriving from xprv)');
      const xprv = await decryptXprv(keystore, password);
      keys = await deriveKeysFromXprv(xprv, chainId, { count, startIndex });
    } else {
      // Mother disk - derive from mnemonic
      const mnemonic = await decryptMnemonic(keystore, password);
      keys = await deriveKeys(mnemonic, chainId, { count, startIndex, addressType });
    }

    console.log('');
    keys.forEach(key => {
      const typeStr = key.addressType ? ` (${key.addressType})` : '';
      console.log(`[${key.index}] ${key.address}${typeStr}`);
    });
    console.log('');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Print usage help
 */
function showHelp() {
  console.log(`
Floppy Disk Keystore Manager - Multi-Chain Support

=== Key Management ===
  mount              - Mount the floppy disk securely
  unmount            - Sync and unmount the floppy disk
  create             - Create a new encrypted mnemonic keystore
  test               - Test keystore decryption
  info               - Show keystore information and supported chains
  chains             - List all supported blockchain chains
  derive <chain>     - Derive keys for a specific chain
  address <chain>    - Show addresses for a chain (no private keys)

=== Identity & Memory ===
  storage            - Show disk space usage
  did <cmd>          - Manage DID document (create, show, add-service)
  profile <cmd>      - Manage agent profile (set, show)
  memory <cmd>       - Manage persistent memory (add, list, search, delete, clear)
  metadata <cmd>     - Key-value metadata store (set, get, list, delete)

=== Integrity & Backup ===
  verify             - Verify disk integrity (non-interactive)
  sign               - Sign/re-sign manifest with keystore key
  clone              - Clone disk to backup floppy
  diff <path>        - Compare current disk with another manifest

=== Mother/Clone Branching (xprv Isolation) ===
  init-mother        - Initialize this disk as a mother
  fork               - Create a new clone with xprv isolation (cryptographically isolated)
  fork-write         - Write fork data to clone disk (after disk swap)
  status             - Show disk role, TTL, and status
  log                - Show clone registry (mother) or sync history
  push               - Export clone changes for mother import
  pull               - Import mother changes to clone
  verify-cert        - Verify clone's birth certificate

=== Compromise Management ===
  mark-compromised   - Mark a clone as compromised (on mother disk)
  clear-compromised  - Clear compromised status from a clone
  list-compromised   - List all compromised clones

=== Help ===
  help               - Show this help message

Derive Options:
  --count=N          - Number of accounts to derive (default: 1)
  --start=N          - Starting index (default: 0)
  --type=TYPE        - Address type (for Bitcoin: legacy, segwit, nativeSegwit, taproot)

Memory Options:
  --type=TYPE        - Entry type (note, context, fact, etc.)
  --tags=a,b,c       - Comma-separated tags
  --importance=N     - Importance 1-10 (default: 5)
  --content=TEXT     - Memory content

Examples:
  # Key derivation
  node cli.js derive ethereum --count=5
  node cli.js derive bitcoin --type=nativeSegwit --count=3

  # DID management
  node cli.js did create --method=key
  node cli.js did add-service --type=AgentService --endpoint=https://...

  # Memory management
  node cli.js memory add --content="User prefers dark mode" --tags=preference --importance=7
  node cli.js memory list --type=note
  node cli.js memory search --text="dark mode"

  # Metadata
  node cli.js metadata set --key=lastSync --value="2025-01-15"
  node cli.js metadata get --key=lastSync

  # Integrity verification
  node cli.js verify                    # Verify disk integrity
  node cli.js sign                      # Sign manifest after changes
  node cli.js clone                     # Clone to backup disk
  node cli.js diff /path/to/manifest.json  # Compare with another disk

  # Mother/Clone branching (xprv isolation)
  node cli.js init-mother --id=mordor   # Make this disk a mother
  node cli.js fork --id=agent-1 --name="Agent Alpha" --ttl=30  # Fork a clone
  node cli.js fork-write                # Write clone to new floppy (after swap)
  node cli.js status                    # Show current disk role and TTL
  node cli.js verify-cert               # Verify clone's birth certificate
  node cli.js log                       # Show clone registry or history
  node cli.js push                      # Export clone changes (run on clone)
  node cli.js pull                      # Import mother changes (after disk swap)

  # Compromise management (on mother)
  node cli.js mark-compromised --id=agent-1 --reason="Lost"
  node cli.js list-compromised
  node cli.js clear-compromised --id=agent-1

Supported Chains:
  ethereum (eth)     - Ethereum and EVM chains
  bitcoin (btc)      - Bitcoin (multiple address types)
  zcash (zec)        - Zcash transparent addresses
  monero (xmr)       - Monero (derived from BIP-39)
  solana (sol)       - Solana
  ethereumClassic    - Ethereum Classic

Environment Variables:
  FLOPPY_DEVICE              - Device path (default: /dev/sde)
  FLOPPY_MOUNT               - Mount point (default: /mnt/floppy)
  FLOPPY_KEYSTORE_PASSWORD   - Keystore password (for non-interactive use)

Storage Capacity:
  ~1.4 MB available for identity, memory, and metadata after keystores
`);
}

// ============================================================================
// Identity & Memory Commands
// ============================================================================

/**
 * Show storage stats
 */
function showStorage() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  console.log('\n=== Floppy Disk Storage ===\n');

  const stats = identity.getStorageStats();

  console.log(`Capacity:  ${stats.capacityFormatted}`);
  console.log(`Used:      ${stats.usedFormatted} (${stats.usedPercent}%)`);
  console.log(`Available: ${stats.availableFormatted}`);

  console.log('\nFiles:');
  Object.entries(stats.files).forEach(([file, size]) => {
    console.log(`  ${file.padEnd(35)} ${identity.getStorageStats().usedFormatted ? (size + ' B').padStart(10) : ''}`);
  });
}

/**
 * Create or show DID document
 */
async function manageDID(subcommand, options) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  switch (subcommand) {
    case 'create': {
      const existing = identity.getDIDDocument();
      if (existing && !options.force) {
        console.error('DID document already exists. Use --force to overwrite.');
        console.log('Current DID:', existing.id);
        process.exit(1);
      }

      const method = options.method || 'key';
      const doc = identity.createDIDDocument({ method });

      console.log('\n=== DID Document Created ===\n');
      console.log('DID:', doc.id);
      console.log('Controller:', doc.controller);
      console.log('Created:', doc.created);
      console.log('\nVerification Methods:');
      doc.verificationMethod.forEach(vm => {
        console.log(`  - ${vm.id} (${vm.type})`);
      });
      break;
    }

    case 'show':
    default: {
      const doc = identity.getDIDDocument();
      if (!doc) {
        console.log('No DID document found. Create one with: did create');
        return;
      }

      console.log('\n=== DID Document ===\n');
      console.log(JSON.stringify(doc, null, 2));
      break;
    }

    case 'add-service': {
      if (!options.type || !options.endpoint) {
        console.error('Usage: did add-service --type=TYPE --endpoint=URL [--id=ID]');
        process.exit(1);
      }

      const doc = identity.addDIDService({
        id: options.id,
        type: options.type,
        endpoint: options.endpoint
      });

      console.log('Service added to DID document');
      console.log('Services:', doc.service.length);
      break;
    }

    case 'atproto': {
      // Create AT Protocol compatible DID
      if (!options.domain || !options.handle || !options.pds) {
        console.error('Usage: did atproto --domain=DOMAIN --handle=HANDLE --pds=PDS_URL');
        console.error('');
        console.error('Example:');
        console.error('  did atproto --domain=agent.example.com --handle=agent.bsky.social --pds=https://bsky.social');
        process.exit(1);
      }

      const existing = identity.getDIDDocument();
      if (existing && !options.force) {
        console.error('DID document already exists. Use --force to overwrite.');
        console.log('Current DID:', existing.id);
        process.exit(1);
      }

      const doc = identity.createATProtoDIDDocument({
        domain: options.domain,
        handle: options.handle,
        pdsUrl: options.pds
      });

      console.log('\n=== AT Protocol DID Created ===\n');
      console.log('DID:', doc.id);
      console.log('Handle:', doc.alsoKnownAs[0]);
      console.log('PDS:', doc.service.find(s => s.type === 'AtprotoPersonalDataServer')?.serviceEndpoint);
      console.log('\nNote: Run "did setkey" to set the public key from your keystore.');
      console.log('      Then run "did export" to get the document for web hosting.');
      break;
    }

    case 'setkey': {
      // Set the public key from the floppy keystore
      const doc = identity.getDIDDocument();
      if (!doc) {
        console.error('No DID document found. Create one first.');
        process.exit(1);
      }

      const password = options.password || process.env.FLOPPY_KEYSTORE_PASSWORD ||
        await promptPassword('Keystore password: ');

      const { loadMnemonicFromFloppyWithPassword, deriveChainKeys } = require('./loader');

      try {
        // Load keystore and derive first key
        const keystoreFile = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR, CONFIG.KEYSTORE_FILENAME);
        const keystore = JSON.parse(fs.readFileSync(keystoreFile, 'utf8'));
        const mnemonic = await decryptMnemonic(keystore, password);

        // Derive Ethereum key (secp256k1 - compatible with AT Protocol)
        const keys = await deriveKeys(mnemonic, 'ethereum', { count: 1 });
        const publicKey = keys[0].publicKey;

        // Set in DID document
        const updated = identity.setATProtoPublicKey(publicKey);

        console.log('\n=== Public Key Set ===\n');
        console.log('Key ID:', updated.verificationMethod[0].id);
        console.log('Type:', updated.verificationMethod[0].type);
        console.log('Public Key (multibase):', updated.verificationMethod[0].publicKeyMultibase?.substring(0, 40) + '...');
      } catch (err) {
        console.error('Error setting public key:', err.message);
        process.exit(1);
      }
      break;
    }

    case 'validate': {
      // Validate DID for AT Protocol
      const result = identity.validateATProtoDID();

      console.log('\n=== AT Protocol DID Validation ===\n');
      console.log('Valid:', result.valid ? 'Yes' : 'No');

      if (result.errors.length > 0) {
        console.log('\nErrors:');
        result.errors.forEach(e => console.log('  - ' + e));
      }

      if (result.warnings.length > 0) {
        console.log('\nWarnings:');
        result.warnings.forEach(w => console.log('  - ' + w));
      }

      if (result.valid) {
        console.log('\nDID document is valid for AT Protocol.');
        console.log('Host at: https://<domain>/.well-known/did.json');
      }
      break;
    }

    case 'export': {
      // Export DID for web hosting
      try {
        const json = identity.exportDIDForWeb();
        console.log(json);

        if (options.file) {
          fs.writeFileSync(options.file, json);
          console.error(`\nExported to: ${options.file}`);
        } else {
          console.error('\nTo save to file: did export --file=did.json');
          console.error('Host at: https://<domain>/.well-known/did.json');
        }
      } catch (err) {
        console.error('Error exporting:', err.message);
        process.exit(1);
      }
      break;
    }

    case 'handle': {
      // Update AT Protocol handle
      if (!options.handle) {
        console.error('Usage: did handle --handle=NEW_HANDLE');
        process.exit(1);
      }

      const doc = identity.updateATProtoHandle(options.handle);
      console.log('Handle updated to:', doc.alsoKnownAs[0]);
      break;
    }

    case 'ens': {
      // Create ENS-based DID
      if (!options.name) {
        console.error('Usage: did ens --name=NAME.eth [--chain=1]');
        console.error('');
        console.error('Example:');
        console.error('  did ens --name=chipprbots.eth');
        console.error('');
        console.error('Note: did:ens is NOT supported by AT Protocol (Bluesky).');
        console.error('      Use "did atproto" for Bluesky compatibility.');
        process.exit(1);
      }

      const existing = identity.getDIDDocument();
      if (existing && !options.force) {
        console.error('DID document already exists. Use --force to overwrite.');
        console.log('Current DID:', existing.id);
        process.exit(1);
      }

      const doc = identity.createENSDIDDocument({
        ensName: options.name,
        chainId: options.chain || '1'
      });

      console.log('\n=== ENS DID Created ===\n');
      console.log('DID:', doc.id);
      console.log('Chain ID:', options.chain || '1');
      console.log('\nTo publish this DID:');
      console.log('1. Run: did export-ens');
      console.log('2. Add the text record to your ENS domain');
      console.log('\nNote: This DID is NOT compatible with AT Protocol (Bluesky).');
      break;
    }

    case 'export-ens': {
      // Export DID for ENS text record
      try {
        const result = identity.exportDIDForENS();

        console.log('\n=== ENS DID Export ===\n');
        console.log('Size:', result.sizeFormatted);
        console.log('\nText Record Value:');
        console.log(result.textRecord);
        console.log('\n' + result.instructions);
      } catch (err) {
        console.error('Error exporting:', err.message);
        process.exit(1);
      }
      break;
    }
  }
}

/**
 * Manage agent profile
 */
async function manageProfile(subcommand, options) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  switch (subcommand) {
    case 'set': {
      const profile = {};

      if (options.name) profile.name = options.name;
      if (options.description) profile.description = options.description;
      if (options.version) profile.version = options.version;

      if (Object.keys(profile).length === 0) {
        // Interactive mode
        profile.name = await promptInput('Agent name: ');
        profile.description = await promptInput('Description: ');
        profile.version = await promptInput('Version (e.g., 1.0.0): ');
      }

      const result = identity.setProfile(profile);
      console.log('\nProfile updated:');
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case 'show':
    default: {
      const profile = identity.getProfile();
      if (!profile) {
        console.log('No profile found. Create one with: profile set');
        return;
      }

      console.log('\n=== Agent Profile ===\n');
      console.log(JSON.stringify(profile, null, 2));
      break;
    }
  }
}

/**
 * Manage memory entries
 */
async function manageMemory(subcommand, options) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  switch (subcommand) {
    case 'add': {
      let content = options.content;
      if (!content) {
        content = await promptInput('Memory content: ');
      }

      const entry = identity.addMemory({
        type: options.type || 'note',
        content,
        tags: options.tags ? options.tags.split(',') : [],
        importance: parseInt(options.importance) || 5
      });

      console.log('\nMemory added:');
      console.log(`  ID: ${entry.id}`);
      console.log(`  Type: ${entry.type}`);
      console.log(`  Importance: ${entry.importance}/10`);
      break;
    }

    case 'list': {
      const entries = identity.searchMemory({
        type: options.type,
        tags: options.tags ? options.tags.split(',') : null,
        minImportance: options.importance ? parseInt(options.importance) : null,
        limit: options.limit ? parseInt(options.limit) : 20
      });

      console.log(`\n=== Memory Entries (${entries.length}) ===\n`);

      if (entries.length === 0) {
        console.log('No entries found.');
        return;
      }

      entries.forEach(entry => {
        const preview = entry.content.length > 60
          ? entry.content.slice(0, 60) + '...'
          : entry.content;
        console.log(`[${entry.id}] (${entry.type}, imp:${entry.importance}) ${preview}`);
        if (entry.tags.length > 0) {
          console.log(`         Tags: ${entry.tags.join(', ')}`);
        }
      });
      break;
    }

    case 'show': {
      const id = options.id || args[2];
      if (!id) {
        console.error('Usage: memory show --id=ID');
        process.exit(1);
      }

      const entries = identity.getMemory();
      const entry = entries.find(e => e.id === id);

      if (!entry) {
        console.error('Entry not found:', id);
        process.exit(1);
      }

      console.log('\n=== Memory Entry ===\n');
      console.log(JSON.stringify(entry, null, 2));
      break;
    }

    case 'search': {
      const text = options.text || args[2];
      if (!text) {
        console.error('Usage: memory search --text=QUERY');
        process.exit(1);
      }

      const entries = identity.searchMemory({ text, limit: 10 });

      console.log(`\n=== Search Results (${entries.length}) ===\n`);
      entries.forEach(entry => {
        console.log(`[${entry.id}] ${entry.content.slice(0, 80)}...`);
      });
      break;
    }

    case 'delete': {
      const id = options.id || args[2];
      if (!id) {
        console.error('Usage: memory delete --id=ID');
        process.exit(1);
      }

      if (identity.deleteMemory(id)) {
        console.log('Deleted:', id);
      } else {
        console.error('Entry not found:', id);
      }
      break;
    }

    case 'clear': {
      const confirm = await promptInput('Clear ALL memory? Type "yes" to confirm: ');
      if (confirm === 'yes') {
        identity.clearMemory();
        console.log('Memory cleared.');
      } else {
        console.log('Cancelled.');
      }
      break;
    }

    default:
      console.log('Usage: memory <add|list|show|search|delete|clear>');
  }
}

/**
 * Manage metadata key-value store
 */
function manageMetadata(subcommand, options) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  switch (subcommand) {
    case 'set': {
      const key = options.key || args[2];
      const value = options.value || args[3];

      if (!key || value === undefined) {
        console.error('Usage: metadata set --key=KEY --value=VALUE');
        process.exit(1);
      }

      // Try to parse as JSON
      let parsedValue = value;
      try {
        parsedValue = JSON.parse(value);
      } catch {
        // Keep as string
      }

      identity.setMetadataValue(key, parsedValue);
      console.log(`Set ${key} = ${JSON.stringify(parsedValue)}`);
      break;
    }

    case 'get': {
      const key = options.key || args[2];
      if (!key) {
        console.error('Usage: metadata get --key=KEY');
        process.exit(1);
      }

      const value = identity.getMetadataValue(key);
      if (value === null) {
        console.log(`Key '${key}' not found`);
      } else {
        console.log(JSON.stringify(value, null, 2));
      }
      break;
    }

    case 'list':
    default: {
      const metadata = identity.getMetadata();
      console.log('\n=== Metadata ===\n');
      console.log(JSON.stringify(metadata, null, 2));
      break;
    }

    case 'delete': {
      const key = options.key || args[2];
      if (!key) {
        console.error('Usage: metadata delete --key=KEY');
        process.exit(1);
      }

      identity.deleteMetadataValue(key);
      console.log(`Deleted: ${key}`);
      break;
    }
  }
}

// ============================================================================
// Integrity & Backup Commands
// ============================================================================

/**
 * Verify disk integrity
 */
function verifyDisk() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const result = integrity.verifyDiskIntegrity();

  // Display formatted output
  console.log('');
  console.log('='.repeat(59));
  console.log('  FLOPPY DISK INTEGRITY VERIFICATION');
  console.log('='.repeat(59));
  console.log(`  Disk: ${result.diskName || 'Unknown'} (${result.diskId || 'unknown'})`);
  console.log(`  Signer: ${result.signerAddress || '(not signed)'}`);
  console.log('='.repeat(59));

  // Show check results
  const manifest = integrity.getManifest();

  if (result.checks.signature) {
    console.log(`  ✓ Signature:       VALID`);
  } else if (manifest?.signature) {
    console.log(`  ✗ Signature:       INVALID`);
  } else {
    console.log(`  - Signature:       NOT SIGNED`);
  }

  if (result.checks.merkleRoot) {
    console.log(`  ✓ Merkle root:     ${manifest?.merkleRoot?.slice(0, 18)}...`);
  } else {
    console.log(`  ✗ Merkle root:     MISMATCH`);
  }

  if (result.checks.entryCount) {
    console.log(`  ✓ Entry count:     ${result.entryCount} memories`);
  } else {
    console.log(`  ✗ Entry count:     MISMATCH`);
  }

  if (result.sequenceRange) {
    const gapStr = result.checks.noGaps ? 'no gaps' : 'HAS GAPS';
    console.log(`  ${result.checks.noGaps ? '✓' : '!'} Sequence range:  ${result.sequenceRange.min} → ${result.sequenceRange.max} (${gapStr})`);
  } else {
    console.log(`  - Sequence range:  (no entries)`);
  }

  if (result.checks.chainHead) {
    console.log(`  ✓ Chain integrity: All links valid`);
  } else {
    console.log(`  ! Chain integrity: Links may have changed`);
  }

  // File hashes
  const fileHashCount = Object.keys(result.fileHashes || {}).length;
  const matchingFiles = Object.values(result.fileHashes || {}).filter(v => v).length;
  if (result.checks.fileHashes) {
    console.log(`  ✓ File hashes:     ${matchingFiles}/${fileHashCount} match`);
  } else {
    console.log(`  ! File hashes:     ${matchingFiles}/${fileHashCount} match`);
  }

  console.log('='.repeat(59));

  // Status
  if (result.valid) {
    console.log(`  Status: VERIFIED ✓`);
  } else if (result.errors.length === 0) {
    console.log(`  Status: VALID (with warnings)`);
  } else {
    console.log(`  Status: VERIFICATION FAILED ✗`);
  }

  if (result.hasUnsignedChanges) {
    console.log(`  NOTE: Manifest has unsigned changes`);
  }

  if (result.lastSigned) {
    console.log(`  Last signed: ${result.lastSigned}`);
  }

  console.log('='.repeat(59));
  console.log('');

  // Show errors and warnings
  if (result.errors.length > 0) {
    console.log('Errors:');
    result.errors.forEach(e => console.log(`  ✗ ${e}`));
    console.log('');
  }

  if (result.warnings.length > 0) {
    console.log('Warnings:');
    result.warnings.forEach(w => console.log(`  ! ${w}`));
    console.log('');
  }

  // Exit code
  process.exit(result.valid ? 0 : 1);
}

/**
 * Sign or re-sign manifest
 */
async function signManifest() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  console.log('\n=== Sign Manifest ===\n');

  // Get current manifest state
  const existingManifest = integrity.getManifest();
  if (existingManifest) {
    console.log(`Disk: ${existingManifest.diskName || 'Unknown'} (${existingManifest.diskId})`);
    console.log(`Entries: ${existingManifest.entryCount || 0}`);
    if (existingManifest.signedAt) {
      console.log(`Last signed: ${existingManifest.signedAt}`);
    }
    console.log('');
  }

  // Get password
  let password = resolvePassword();
  if (!password) {
    password = await promptPassword('Enter keystore password: ');
  }

  try {
    // Load keystore and derive signing key
    console.log('Deriving signing key...');
    const keystoreJson = fs.readFileSync(KEYSTORE_PATH, 'utf8');
    const keystore = JSON.parse(keystoreJson);
    const mnemonic = await decryptMnemonic(keystore, password);
    const keys = await deriveKeys(mnemonic, 'ethereum', { count: 1 });
    const privateKey = keys[0].privateKey;

    // Get current entries
    const entries = identity.getMemory();
    const metadata = identity.getMetadata();

    // Create and sign manifest
    console.log('Signing manifest...');
    const manifest = integrity.createManifest(entries, {
      diskId: metadata['disk.name'] || existingManifest?.diskId || 'unknown',
      diskName: metadata['disk.network'] || existingManifest?.diskName || 'Unknown Disk',
      privateKey
    });

    console.log('\nManifest signed successfully!');
    console.log(`  Merkle root: ${manifest.merkleRoot.slice(0, 22)}...`);
    console.log(`  Entry count: ${manifest.entryCount}`);
    console.log(`  Signer: ${manifest.signerAddress}`);
    console.log(`  Signed at: ${manifest.signedAt}`);

  } catch (error) {
    console.error('Error signing manifest:', error.message);
    process.exit(1);
  }
}

/**
 * Clone disk to backup
 */
async function cloneDisk() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  await cloneModule.interactiveClone(promptPassword);
}

/**
 * Compare two disk manifests
 */
function diffDisks(otherPath) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  if (!otherPath) {
    console.error('Error: Please specify path to other manifest');
    console.error('Usage: node cli.js diff /path/to/manifest.json');
    process.exit(1);
  }

  // Load current manifest
  const currentManifest = integrity.getManifest();
  if (!currentManifest) {
    console.error('Error: No manifest found on current disk');
    console.error('Run "sign" command first to create a manifest');
    process.exit(1);
  }

  // Load other manifest
  let otherManifest;
  try {
    otherManifest = JSON.parse(fs.readFileSync(otherPath, 'utf8'));
  } catch (error) {
    console.error('Error reading other manifest:', error.message);
    process.exit(1);
  }

  // Compare
  const diff = integrity.diffManifests(currentManifest, otherManifest);

  console.log('\n=== Disk Comparison ===\n');
  console.log(`Current disk: ${currentManifest.diskId} (${currentManifest.diskName})`);
  console.log(`Other disk:   ${otherManifest.diskId} (${otherManifest.diskName})`);
  console.log(`Relationship: ${diff.relationship}`);
  console.log('');

  if (diff.identical) {
    console.log('Result: IDENTICAL');
  } else {
    console.log('Result: DIFFERENT');
    console.log('\nDifferences:');
    diff.differences.forEach(d => {
      console.log(`  ${d.field}:`);
      console.log(`    Current: ${typeof d.disk1 === 'string' ? d.disk1.slice(0, 40) : d.disk1}${typeof d.disk1 === 'string' && d.disk1.length > 40 ? '...' : ''}`);
      console.log(`    Other:   ${typeof d.disk2 === 'string' ? d.disk2.slice(0, 40) : d.disk2}${typeof d.disk2 === 'string' && d.disk2.length > 40 ? '...' : ''}`);
    });
  }
  console.log('');
}

// ============================================================================
// Mother/Clone Branching Commands
// ============================================================================

/**
 * Initialize disk as mother
 */
function initMother(options) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const motherId = options.id;
  if (!motherId) {
    console.error('Error: Mother ID required');
    console.error('Usage: node cli.js init-mother --id=<mother-id>');
    process.exit(1);
  }

  try {
    cloneModule.initMother(motherId);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Fork a new clone with xprv isolation
 */
async function forkClone(options) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const cloneId = options.id;
  if (!cloneId) {
    console.error('Error: Clone ID required');
    console.error('Usage: node cli.js fork --id=<clone-id> [--name=<name>] [--purpose=<purpose>] [--ttl=30]');
    console.error('');
    console.error('Options:');
    console.error('  --id=ID       Clone identifier (required)');
    console.error('  --name=NAME   Human-readable name');
    console.error('  --purpose=TXT Purpose description');
    console.error('  --ttl=DAYS    Time-to-live in days (default: 30)');
    process.exit(1);
  }

  try {
    console.log('\n=== Fork New Clone (xprv Isolation) ===\n');
    console.log('This creates a cryptographically isolated clone:');
    console.log('  - Clone receives extended private key (xprv) for its account only');
    console.log('  - Clone CANNOT access other accounts or derive the mnemonic');
    console.log('  - Clone has its own unique password');
    console.log('  - Clone has a time-to-live (TTL) requiring periodic reconciliation');
    console.log('');

    // Get mother password (required for xprv derivation)
    let motherPassword = resolvePassword();
    if (!motherPassword) {
      motherPassword = await promptPassword('Enter mother keystore password: ');
    }

    const ttlDays = parseInt(options.ttl) || 30;

    console.log('\nPreparing fork data on mother disk...');

    const forkData = await cloneModule.prepareFork({
      cloneId,
      cloneName: options.name || cloneId,
      purpose: options.purpose || '',
      motherPassword,
      ttlDays
    });

    console.log(`\nClone registered:`);
    console.log(`  ID: ${forkData.cloneId}`);
    console.log(`  Derivation Index: ${forkData.cloneRecord.derivationIndex}`);
    console.log(`  Derivation Path: ${forkData.cloneRecord.derivationPath}`);
    console.log(`  Fork Sequence: ${forkData.forkSequence}`);
    console.log(`  TTL: ${forkData._ttlDays} days`);
    console.log(`  Expires: ${forkData._expiresAt}`);
    console.log(`  Mother Address: ${forkData.motherAddress}`);
    console.log(`  Isolation: xprv (no mnemonic shared)`);

    // Save fork data to temp file
    const tempPath = '/tmp/fork-data.json';
    const exportData = {
      ...forkData,
      // Store xprv data for write step (will be encrypted with clone password)
      files: Object.fromEntries(
        Object.entries(forkData.files).map(([k, v]) => [k, v.toString('base64')])
      )
    };
    fs.writeFileSync(tempPath, JSON.stringify(exportData));
    console.log(`\nFork data saved to: ${tempPath}`);

    console.log('\n--- Next Steps ---');
    console.log('1. Swap to blank floppy disk');
    console.log('2. Remount: sudo umount /mnt/floppy && sudo mount -o umask=000 /dev/sde /mnt/floppy');
    console.log('3. Run: node cli.js fork-write');
    console.log('   (You will be prompted to set a NEW password for the clone)');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Write fork data to disk (after disk swap)
 * Creates xprv-based keystore with clone's unique password
 */
async function forkWrite() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const tempPath = '/tmp/fork-data.json';
  if (!fs.existsSync(tempPath)) {
    console.error('Error: No fork data found. Run "fork" command first on mother disk.');
    process.exit(1);
  }

  try {
    // Load fork data
    const exportData = JSON.parse(fs.readFileSync(tempPath, 'utf8'));
    const forkData = {
      ...exportData,
      files: Object.fromEntries(
        Object.entries(exportData.files).map(([k, v]) => [k, Buffer.from(v, 'base64')])
      )
    };

    console.log('\n=== Write Clone to Disk (xprv Isolation) ===\n');
    console.log(`Clone ID: ${forkData.cloneId}`);
    console.log(`Mother: ${forkData.motherId}`);
    console.log(`Derivation Index: ${forkData.cloneRecord.derivationIndex}`);
    console.log(`Expires: ${forkData._expiresAt}`);
    console.log('');

    // Get clone password from env or prompt
    let clonePassword = process.env.FLOPPY_CLONE_PASSWORD;

    if (!clonePassword) {
      console.log('Set a UNIQUE password for this clone.');
      console.log('This password is independent from the mother - it encrypts only this clone\'s xprv.');
      console.log('(Or set FLOPPY_CLONE_PASSWORD env var)');
      console.log('');
      clonePassword = await promptPassword('Enter NEW password for this clone: ');

      if (clonePassword.length < 8) {
        console.error('Error: Password must be at least 8 characters');
        process.exit(1);
      }

      const confirmPassword = await promptPassword('Confirm new password: ');
      if (clonePassword !== confirmPassword) {
        console.error('Error: Passwords do not match');
        process.exit(1);
      }
    } else {
      console.log('Using clone password from FLOPPY_CLONE_PASSWORD env var');
      if (clonePassword.length < 8) {
        console.error('Error: Password must be at least 8 characters');
        process.exit(1);
      }
    }

    // Write to disk
    await cloneModule.writeForkToDisk(forkData, { clonePassword });

    // Clean up temp file
    fs.unlinkSync(tempPath);

    console.log('\nRun "node cli.js status" to verify.');
    console.log('Run "node cli.js verify-cert" to verify birth certificate.');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Show disk status
 */
function showStatus() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  try {
    const status = cloneModule.getStatus();
    const manifest = integrity.getManifest();

    console.log('\n=== Disk Status ===\n');
    console.log(`Role: ${status.role.toUpperCase()}`);
    console.log(`Disk ID: ${status.diskId}`);
    console.log(`Name: ${status.diskName}`);
    console.log(`Entries: ${status.entryCount}`);
    console.log(`Last Sequence: ${status.lastSequence}`);
    console.log(`Unsigned Changes: ${status.hasUnsignedChanges ? 'Yes' : 'No'}`);
    console.log(`Last Signed: ${status.lastSigned || 'Never'}`);

    if (status.role === 'mother') {
      console.log('\n--- Mother Info ---');
      console.log(`Mother ID: ${status.motherId}`);
      console.log(`Total Clones: ${status.totalClones}`);
      console.log(`Active Clones: ${status.activeClones}`);
      console.log(`Next Index: ${status.nextIndex}`);
    } else if (status.role === 'clone') {
      console.log('\n--- Clone Info ---');
      console.log(`Mother ID: ${status.motherId}`);
      console.log(`Mother Address: ${manifest?.motherAddress || 'Unknown'}`);
      console.log(`Derivation Index: ${status.derivationIndex}`);
      console.log(`Derivation Path: ${status.derivationPath}`);
      console.log(`Fork Sequence: ${status.forkSequence}`);
      console.log(`Forked At: ${status.forkedAt}`);

      // Check keystore type
      const keystorePath = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR, CONFIG.KEYSTORE_FILENAME);
      if (fs.existsSync(keystorePath)) {
        const keystore = JSON.parse(fs.readFileSync(keystorePath, 'utf8'));
        console.log(`Keystore Type: ${keystore.type === 'xprv' ? 'xprv (isolated)' : 'mnemonic (shared)'}`);
      }

      // Show TTL/expiration info
      if (manifest?.expiresAt) {
        const now = new Date();
        const expiresAt = new Date(manifest.expiresAt);
        const daysRemaining = Math.ceil((expiresAt - now) / (24 * 60 * 60 * 1000));

        console.log('\n--- TTL Status ---');
        console.log(`TTL: ${manifest.ttlDays || 'Unknown'} days`);
        console.log(`Expires At: ${manifest.expiresAt}`);

        if (daysRemaining <= 0) {
          console.log(`Status: EXPIRED (${Math.abs(daysRemaining)} days ago)`);
        } else if (daysRemaining <= 7) {
          console.log(`Status: EXPIRING SOON (${daysRemaining} days remaining)`);
        } else {
          console.log(`Status: Valid (${daysRemaining} days remaining)`);
        }
      }
    }

    console.log('');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Show clone log/registry
 */
function showLog() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const role = registry.getDiskRole();

  if (role === 'mother') {
    const reg = registry.getRegistry();
    console.log('\n=== Clone Registry ===\n');
    console.log(`Mother ID: ${reg.motherId}`);
    console.log(`Created: ${reg.createdAt}`);
    console.log(`Total Clones: ${reg.clones.length}`);
    console.log('');

    if (reg.clones.length === 0) {
      console.log('No clones registered yet.');
      console.log('Create one with: node cli.js fork --id=<clone-id>');
    } else {
      console.log('Clones:');
      reg.clones.forEach((c, i) => {
        const statusIcon = c.status === 'active' ? '✓' : c.status === 'revoked' ? '✗' : '○';
        console.log(`  ${statusIcon} [${c.derivationIndex}] ${c.id} (${c.name})`);
        console.log(`      Path: ${c.derivationPath}`);
        console.log(`      Forked: ${c.forkedAt}`);
        console.log(`      Purpose: ${c.purpose || '(none)'}`);
        if (c.lastSyncToMother) {
          console.log(`      Last Push: ${c.lastSyncToMother}`);
        }
        console.log('');
      });
    }

    // Show recent sync history
    if (reg.syncHistory && reg.syncHistory.length > 0) {
      console.log('Recent Syncs:');
      reg.syncHistory.slice(-5).forEach(s => {
        const dir = s.direction === 'push' ? '→' : '←';
        console.log(`  ${s.timestamp} | ${s.cloneId} ${dir} mother | ${s.entriesTransferred} entries`);
      });
      console.log('');
    }

  } else if (role === 'clone') {
    const manifest = integrity.getManifest();
    console.log('\n=== Clone Info ===\n');
    console.log(`Clone ID: ${manifest.diskId}`);
    console.log(`Mother: ${manifest.motherId}`);
    console.log(`Derivation Index: ${manifest.derivationIndex}`);
    console.log(`Derivation Path: ${manifest.derivationPath}`);
    console.log(`Forked At: ${manifest.forkedAt}`);
    console.log(`Fork Sequence: ${manifest.forkSequence}`);
    console.log(`Current Sequence: ${manifest.lastSequence}`);
    console.log(`Entries Since Fork: ${(manifest.lastSequence || 0) - (manifest.forkSequence || 0)}`);
    console.log('');

  } else {
    console.log('\nThis disk is standalone (neither mother nor clone).');
    console.log('Initialize as mother with: node cli.js init-mother --id=<mother-id>');
    console.log('');
  }
}

/**
 * Export push data (clone → mother)
 */
function pushChanges() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  try {
    const pushData = cloneModule.preparePush();

    console.log('\n=== Push Data ===\n');
    console.log(`Clone ID: ${pushData.cloneId}`);
    console.log(`Mother ID: ${pushData.motherId}`);
    console.log(`Fork Sequence: ${pushData.forkSequence}`);
    console.log(`Current Sequence: ${pushData.currentSequence}`);
    console.log(`Entries to Push: ${pushData.entryCount}`);

    if (pushData.entryCount === 0) {
      console.log('\nNo new entries to push.');
      return;
    }

    // Save push data
    const tempPath = '/tmp/push-data.json';
    fs.writeFileSync(tempPath, JSON.stringify(pushData, null, 2));
    console.log(`\nPush data saved to: ${tempPath}`);

    console.log('\n--- Next Steps ---');
    console.log('1. Swap to mother floppy disk');
    console.log('2. Remount the disk');
    console.log('3. Run: node cli.js push-import');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Import push data (on mother)
 */
function pushImport(options) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const tempPath = '/tmp/push-data.json';
  if (!fs.existsSync(tempPath)) {
    console.error('Error: No push data found. Run "push" command first on clone disk.');
    process.exit(1);
  }

  try {
    const pushData = JSON.parse(fs.readFileSync(tempPath, 'utf8'));

    console.log('\n=== Import Push Data ===\n');
    console.log(`From Clone: ${pushData.cloneId}`);
    console.log(`Entries: ${pushData.entryCount}`);

    if (options.dryRun) {
      const result = cloneModule.importPush(pushData, { dryRun: true });
      console.log(`\nDry run: Would import ${result.entriesWouldImport} entries`);
      return;
    }

    const result = cloneModule.importPush(pushData);
    console.log(`\nImported ${result.entriesImported} entries from ${result.cloneId}`);

    // Clean up
    fs.unlinkSync(tempPath);
    console.log('Push data cleared.');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Prepare pull data (on mother for clone)
 */
function pullChanges() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const tempPath = '/tmp/clone-manifest.json';
  if (!fs.existsSync(tempPath)) {
    console.error('Error: No clone manifest found.');
    console.error('First, on the clone disk, run: node cli.js pull-request');
    process.exit(1);
  }

  try {
    const cloneManifest = JSON.parse(fs.readFileSync(tempPath, 'utf8'));
    const pullData = cloneModule.preparePull(cloneManifest);

    console.log('\n=== Pull Data ===\n');
    console.log(`For Clone: ${pullData.cloneId}`);
    console.log(`Entries to Pull: ${pullData.entryCount}`);

    if (pullData.entryCount === 0) {
      console.log('\nNo new entries from mother.');
      return;
    }

    // Save pull data
    const pullPath = '/tmp/pull-data.json';
    fs.writeFileSync(pullPath, JSON.stringify(pullData, null, 2));
    console.log(`\nPull data saved to: ${pullPath}`);

    console.log('\n--- Next Steps ---');
    console.log('1. Swap to clone floppy disk');
    console.log('2. Remount the disk');
    console.log('3. Run: node cli.js pull-import');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Request pull (on clone, saves manifest for mother)
 */
function pullRequest() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const manifest = integrity.getManifest();
  if (!manifest || !manifest.motherId) {
    console.error('Error: This disk is not a clone');
    process.exit(1);
  }

  const tempPath = '/tmp/clone-manifest.json';
  fs.writeFileSync(tempPath, JSON.stringify(manifest, null, 2));

  console.log('\n=== Pull Request ===\n');
  console.log(`Clone ID: ${manifest.diskId}`);
  console.log(`Fork Sequence: ${manifest.forkSequence}`);
  console.log(`Clone manifest saved to: ${tempPath}`);

  console.log('\n--- Next Steps ---');
  console.log('1. Swap to mother floppy disk');
  console.log('2. Remount the disk');
  console.log('3. Run: node cli.js pull');
}

/**
 * Import pull data (on clone)
 */
function pullImport() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const tempPath = '/tmp/pull-data.json';
  if (!fs.existsSync(tempPath)) {
    console.error('Error: No pull data found. Run "pull" command first on mother disk.');
    process.exit(1);
  }

  try {
    const pullData = JSON.parse(fs.readFileSync(tempPath, 'utf8'));

    console.log('\n=== Import Pull Data ===\n');
    console.log(`From Mother: ${pullData.motherId}`);
    console.log(`Entries: ${pullData.entryCount}`);

    const result = cloneModule.importPull(pullData);
    console.log(`\nImported ${result.entriesImported} entries from mother`);

    // Clean up
    fs.unlinkSync(tempPath);
    console.log('Pull data cleared.');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// ============================================================================
// Compromise Management Commands
// ============================================================================

/**
 * Mark a clone as compromised
 */
function markCloneCompromised(options) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const cloneId = options.id;
  if (!cloneId) {
    console.error('Error: Clone ID required');
    console.error('Usage: node cli.js mark-compromised --id=<clone-id> [--reason=<reason>]');
    process.exit(1);
  }

  try {
    const result = registry.markCompromised(cloneId, options.reason || '');

    console.log('\n=== Clone Marked as Compromised ===\n');
    console.log(`Clone ID: ${result.id}`);
    console.log(`Status: ${result.status}`);
    console.log(`Compromised At: ${result.compromisedAt}`);
    console.log(`Reason: ${result.compromiseReason || '(none provided)'}`);
    console.log(`Last Trusted Sequence: ${result.lastTrustedSequence}`);
    console.log(`Last Trusted At: ${result.lastTrustedAt}`);
    console.log('\nEntries from this clone after the trust cutoff will be rejected on import.');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Clear compromised status from a clone
 */
function clearCloneCompromised(options) {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const cloneId = options.id;
  if (!cloneId) {
    console.error('Error: Clone ID required');
    console.error('Usage: node cli.js clear-compromised --id=<clone-id>');
    process.exit(1);
  }

  try {
    const result = registry.clearCompromised(cloneId);

    console.log('\n=== Compromised Status Cleared ===\n');
    console.log(`Clone ID: ${result.id}`);
    console.log(`Status: ${result.status}`);
    console.log('\nThis clone is now trusted again. Future imports will be accepted.');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * List compromised clones
 */
function listCompromised() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  try {
    const compromised = registry.getCompromisedClones();

    console.log('\n=== Compromised Clones ===\n');

    if (compromised.length === 0) {
      console.log('No clones are currently marked as compromised.');
      return;
    }

    compromised.forEach(clone => {
      console.log(`Clone: ${clone.id} (${clone.name})`);
      console.log(`  Compromised At: ${clone.compromisedAt}`);
      console.log(`  Reason: ${clone.compromiseReason || '(none)'}`);
      console.log(`  Last Trusted Sequence: ${clone.lastTrustedSequence}`);
      console.log(`  Last Trusted At: ${clone.lastTrustedAt}`);
      console.log('');
    });

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Verify birth certificate (on clone disk)
 */
function verifyCertificate() {
  if (!isMounted()) {
    console.error('Error: Floppy not mounted');
    process.exit(1);
  }

  const certPath = path.join(IDENTITY_DIR, 'birth-certificate.json');
  if (!fs.existsSync(certPath)) {
    console.error('Error: No birth certificate found. This may not be a clone disk.');
    process.exit(1);
  }

  try {
    const certificate = JSON.parse(fs.readFileSync(certPath, 'utf8'));
    const manifest = integrity.getManifest();

    console.log('\n=== Birth Certificate Verification ===\n');
    console.log(`Clone ID: ${certificate.cloneId}`);
    console.log(`Mother ID: ${certificate.motherId}`);
    console.log(`Derivation Index: ${certificate.derivationIndex}`);
    console.log(`Derivation Path: ${certificate.derivationPath}`);
    console.log(`Created At: ${certificate.createdAt}`);
    console.log(`Expires At: ${certificate.expiresAt}`);
    console.log(`TTL: ${certificate.ttlDays} days`);
    console.log(`Mother Address: ${certificate.motherAddress}`);
    console.log('');

    // Verify signature
    const result = cloneModule.verifyBirthCertificate(
      certificate,
      certificate.motherAddress
    );

    if (result.valid) {
      console.log('✓ Signature: VALID');
      console.log(`  Signed by: ${result.recoveredAddress}`);
    } else {
      console.log('✗ Signature: INVALID');
      result.errors.forEach(e => console.log(`  Error: ${e}`));
    }

    // Check expiration
    const now = new Date();
    const expiresAt = new Date(certificate.expiresAt);
    const daysRemaining = Math.ceil((expiresAt - now) / (24 * 60 * 60 * 1000));

    if (result.expired) {
      console.log(`✗ Status: EXPIRED (${Math.abs(daysRemaining)} days ago)`);
    } else if (daysRemaining <= 7) {
      console.log(`! Status: EXPIRING SOON (${daysRemaining} days remaining)`);
    } else {
      console.log(`✓ Status: VALID (${daysRemaining} days remaining)`);
    }

    // Verify xprv hash matches keystore
    const keystorePath = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR, CONFIG.KEYSTORE_FILENAME);
    if (fs.existsSync(keystorePath)) {
      const keystore = JSON.parse(fs.readFileSync(keystorePath, 'utf8'));
      if (keystore.clone && keystore.clone.xprvHash) {
        if (keystore.clone.xprvHash === certificate.xprvHash) {
          console.log('✓ xprv Hash: MATCHES');
        } else {
          console.log('✗ xprv Hash: MISMATCH (keystore may have been tampered)');
        }
      }
    }

    console.log('');

    if (result.valid && !result.expired) {
      console.log('Certificate is VALID and CURRENT.');
    } else if (!result.valid) {
      console.log('Certificate verification FAILED.');
      process.exit(1);
    } else {
      console.log('Certificate has EXPIRED. Reconcile with mother to renew.');
      process.exit(1);
    }

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

/**
 * Parse command line options
 */
function parseOptions(args) {
  const options = {};
  args.forEach(arg => {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      options[key] = value || true;
    }
  });
  return options;
}

// Main CLI handler
const args = process.argv.slice(2);
const command = args[0];
const subcommand = args[1];
// Parse options from all args (parseOptions ignores non-option args)
const options = parseOptions(args);

switch (command) {
  case 'mount':
    mountFloppy();
    break;

  case 'unmount':
    unmountFloppy();
    break;

  case 'create':
    createKeystore().catch(console.error);
    break;

  case 'test':
    testKeystore().catch(console.error);
    break;

  case 'info':
    showInfo();
    break;

  case 'chains':
    listChains();
    break;

  case 'derive':
    if (!subcommand) {
      console.error('Error: Please specify a chain (e.g., derive ethereum)');
      process.exit(1);
    }
    deriveChainKeys(subcommand, options).catch(console.error);
    break;

  case 'address':
  case 'addresses':
    if (!subcommand) {
      console.error('Error: Please specify a chain (e.g., address bitcoin)');
      process.exit(1);
    }
    showAddresses(subcommand, options).catch(console.error);
    break;

  case 'storage':
    showStorage();
    break;

  case 'did':
    manageDID(subcommand, options).catch(console.error);
    break;

  case 'profile':
    manageProfile(subcommand, options).catch(console.error);
    break;

  case 'memory':
    manageMemory(subcommand, options).catch(console.error);
    break;

  case 'metadata':
    manageMetadata(subcommand, options);
    break;

  case 'detect':
  case 'which':
    // Run disk detection script
    require('./disk-detect');
    break;

  // Integrity & Backup commands
  case 'verify':
    verifyDisk();
    break;

  case 'sign':
    signManifest().catch(console.error);
    break;

  case 'clone':
  case 'backup':
    cloneDisk().catch(console.error);
    break;

  case 'diff':
  case 'compare':
    diffDisks(subcommand);
    break;

  // Mother/Clone branching commands
  case 'init-mother':
    initMother(options);
    break;

  case 'fork':
    forkClone(options).catch(console.error);
    break;

  case 'fork-write':
    forkWrite().catch(console.error);
    break;

  case 'status':
    showStatus();
    break;

  case 'log':
    showLog();
    break;

  case 'push':
    pushChanges();
    break;

  case 'push-import':
    pushImport(options);
    break;

  case 'pull':
    pullChanges();
    break;

  case 'pull-request':
    pullRequest();
    break;

  case 'pull-import':
    pullImport();
    break;

  // Compromise management commands
  case 'mark-compromised':
  case 'compromised':
    markCloneCompromised(options);
    break;

  case 'clear-compromised':
  case 'uncompromised':
    clearCloneCompromised(options);
    break;

  case 'list-compromised':
    listCompromised();
    break;

  case 'verify-cert':
  case 'verify-certificate':
    verifyCertificate();
    break;

  case 'help':
  case '--help':
  case '-h':
    showHelp();
    break;

  default:
    showHelp();
}
