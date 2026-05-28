/**
 * Clone Module - Floppy Disk Cloning, Forking, and Sync
 *
 * Provides functionality to:
 * - Initialize mother disks
 * - Fork clones with unique derivation indices
 * - Sync changes between mother and clones (push/pull)
 * - Clone floppy keystores to backup disks
 *
 * @module clone
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { execSync } = require('child_process');
const CONFIG = require('./config');
const integrity = require('./integrity');
const registry = require('./registry');

const KEYSTORE_DIR = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR);
const IDENTITY_DIR = path.join(KEYSTORE_DIR, 'identity');

/**
 * Format bytes as human-readable string
 */
function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
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
 * Wait for user to press Enter
 */
async function waitForEnter(message = 'Press Enter to continue...') {
  await promptInput(message);
}

/**
 * Get all files in keystore directory recursively
 *
 * @returns {object[]} Array of { relativePath, absolutePath, size }
 */
function getKeystoreFiles() {
  const files = [];

  function scanDir(dir, baseDir) {
    if (!fs.existsSync(dir)) return;

    const items = fs.readdirSync(dir);
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        scanDir(fullPath, baseDir);
      } else {
        files.push({
          relativePath: path.relative(baseDir, fullPath),
          absolutePath: fullPath,
          size: stat.size
        });
      }
    }
  }

  scanDir(KEYSTORE_DIR, KEYSTORE_DIR);
  return files;
}

/**
 * Copy a single file preserving structure
 *
 * @param {string} srcPath - Source file path
 * @param {string} destDir - Destination base directory
 * @param {string} relativePath - Relative path within structure
 */
function copyFile(srcPath, destDir, relativePath) {
  const destPath = path.join(destDir, relativePath);
  const destFolder = path.dirname(destPath);

  // Create directory structure
  if (!fs.existsSync(destFolder)) {
    fs.mkdirSync(destFolder, { mode: 0o700, recursive: true });
  }

  // Copy file with same permissions
  fs.copyFileSync(srcPath, destPath);
  fs.chmodSync(destPath, 0o600);
}

/**
 * Clone source disk to destination
 *
 * This function assumes:
 * - Source disk is currently mounted
 * - Destination disk will be mounted at same location (after unmount/remount)
 *
 * @param {object} options - Clone options
 * @param {string} options.password - Password for signing
 * @param {string} options.newDiskId - Optional new disk ID (default: auto-generate)
 * @param {boolean} options.skipVerify - Skip verification steps
 * @returns {Promise<object>} Clone result
 */
async function cloneDisk(options = {}) {
  const result = {
    success: false,
    sourceManifest: null,
    cloneManifest: null,
    filesCopied: [],
    errors: []
  };

  try {
    // 1. Verify source disk
    console.log('\n1. Verifying source disk integrity...');
    const sourceVerify = integrity.verifyDiskIntegrity();

    if (!sourceVerify.valid) {
      console.log('   Warnings found on source disk:');
      sourceVerify.errors.forEach(e => console.log('   - ' + e));
      const proceed = await promptInput('   Continue anyway? (yes/no): ');
      if (proceed.toLowerCase() !== 'yes') {
        result.errors.push('User cancelled due to source verification warnings');
        return result;
      }
    } else {
      console.log('   Source disk verified');
    }

    result.sourceManifest = integrity.getManifest();

    // 2. Collect files to copy
    console.log('\n2. Collecting files...');
    const files = getKeystoreFiles();
    const totalSize = files.reduce((sum, f) => sum + f.size, 0);

    console.log(`   Found ${files.length} files (${formatBytes(totalSize)})`);

    // 3. Read all files into memory before unmounting
    console.log('\n3. Reading source files into memory...');
    const fileContents = {};
    for (const file of files) {
      fileContents[file.relativePath] = {
        content: fs.readFileSync(file.absolutePath),
        size: file.size
      };
      console.log(`   Read: ${file.relativePath} (${formatBytes(file.size)})`);
    }

    // 4. Prepare clone manifest
    const sourceManifest = result.sourceManifest || {};
    const cloneDiskId = options.newDiskId ||
      `${sourceManifest.diskId || 'unknown'}-backup-${Date.now().toString(36)}`;

    const cloneManifest = {
      ...sourceManifest,
      diskId: cloneDiskId,
      diskName: `${sourceManifest.diskName || 'Unknown'} (Clone)`,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      parentDiskId: sourceManifest.diskId,
      cloneGeneration: (sourceManifest.cloneGeneration || 0) + 1,
      // Signature will be updated after copy
      signature: null,
      signedAt: null,
      hasUnsignedChanges: true
    };

    // Update manifest in file contents
    const manifestRelPath = 'identity/manifest.json';
    fileContents[manifestRelPath] = {
      content: Buffer.from(JSON.stringify(cloneManifest, null, 2)),
      size: 0 // Will be updated
    };
    fileContents[manifestRelPath].size = fileContents[manifestRelPath].content.length;

    // 5. Unmount source disk
    console.log('\n4. Unmounting source disk...');
    try {
      execSync('sync', { stdio: 'ignore' });
      execSync(`sudo umount "${CONFIG.MOUNT_POINT}"`, { stdio: 'inherit' });
      console.log('   Source disk unmounted');
    } catch (e) {
      result.errors.push('Failed to unmount source disk: ' + e.message);
      return result;
    }

    // 6. Prompt for destination disk
    console.log('\n5. Insert destination floppy disk');
    console.log('   WARNING: All data on destination disk will be overwritten!');
    await waitForEnter('   Press Enter when ready...');

    // 7. Mount destination disk
    console.log('\n6. Mounting destination disk...');
    try {
      const mountOptions = CONFIG.MOUNT_OPTIONS.join(',');
      execSync(`sudo mount -o ${mountOptions} "${CONFIG.DEVICE}" "${CONFIG.MOUNT_POINT}"`, { stdio: 'inherit' });
      console.log('   Destination disk mounted');
    } catch (e) {
      result.errors.push('Failed to mount destination disk: ' + e.message);
      return result;
    }

    // 8. Clear existing data on destination (if any)
    console.log('\n7. Preparing destination disk...');
    const destKeystoreDir = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR);
    if (fs.existsSync(destKeystoreDir)) {
      try {
        fs.rmSync(destKeystoreDir, { recursive: true, force: true });
        console.log('   Cleared existing keystore directory');
      } catch (e) {
        console.log('   Warning: Could not clear existing directory: ' + e.message);
      }
    }

    // 9. Write files to destination
    console.log('\n8. Writing files to destination...');
    for (const [relativePath, data] of Object.entries(fileContents)) {
      const destPath = path.join(destKeystoreDir, relativePath);
      const destFolder = path.dirname(destPath);

      if (!fs.existsSync(destFolder)) {
        fs.mkdirSync(destFolder, { mode: 0o700, recursive: true });
      }

      fs.writeFileSync(destPath, data.content, { mode: 0o600 });
      console.log(`   Wrote: ${relativePath} (${formatBytes(data.size)})`);
      result.filesCopied.push(relativePath);
    }

    // 10. Sync to disk
    execSync('sync', { stdio: 'ignore' });
    console.log('   Synced to disk');

    // 11. Sign manifest if password provided
    if (options.password) {
      console.log('\n9. Signing clone manifest...');
      try {
        const { decryptMnemonic } = require('./keystore');
        const { deriveKeys } = require('./chains');

        // Load keystore and derive signing key
        const keystorePath = path.join(destKeystoreDir, CONFIG.KEYSTORE_FILENAME);
        const keystore = JSON.parse(fs.readFileSync(keystorePath, 'utf8'));
        const mnemonic = await decryptMnemonic(keystore, options.password);
        const keys = await deriveKeys(mnemonic, 'ethereum', { count: 1 });

        // Sign manifest
        const manifestPath = path.join(destKeystoreDir, 'identity', 'manifest.json');
        let manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

        const sigData = integrity.signManifest(manifest, keys[0].privateKey);
        manifest.signerAddress = sigData.signerAddress;
        manifest.signature = sigData.signature;
        manifest.signedAt = sigData.signedAt;
        manifest.hasUnsignedChanges = false;

        fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), { mode: 0o600 });
        execSync('sync', { stdio: 'ignore' });

        result.cloneManifest = manifest;
        console.log(`   Signed by: ${manifest.signerAddress}`);
      } catch (e) {
        console.log('   Warning: Could not sign manifest: ' + e.message);
        result.errors.push('Signing failed: ' + e.message);
      }
    } else {
      console.log('\n9. Manifest not signed (no password provided)');
      console.log('   Run "sign" command later to sign the manifest');
    }

    // 12. Verify clone
    if (!options.skipVerify) {
      console.log('\n10. Verifying clone integrity...');
      const cloneVerify = integrity.verifyDiskIntegrity();

      if (cloneVerify.valid || (cloneVerify.warnings.length > 0 && cloneVerify.errors.length === 0)) {
        console.log('    Clone verified');
        result.success = true;
      } else {
        console.log('    Clone verification issues:');
        cloneVerify.errors.forEach(e => console.log('    - ' + e));
        result.errors.push(...cloneVerify.errors);
      }
    } else {
      result.success = true;
    }

    // Final summary
    console.log('\n' + '='.repeat(50));
    if (result.success) {
      console.log('Clone complete!');
      console.log(`  Clone ID: ${cloneManifest.diskId}`);
      console.log(`  Parent: ${cloneManifest.parentDiskId}`);
      console.log(`  Generation: ${cloneManifest.cloneGeneration}`);
      console.log(`  Files: ${result.filesCopied.length}`);
    } else {
      console.log('Clone completed with errors:');
      result.errors.forEach(e => console.log('  - ' + e));
    }

  } catch (error) {
    result.errors.push('Clone failed: ' + error.message);
    console.error('\nClone failed:', error.message);
  }

  return result;
}

/**
 * Interactive clone workflow
 * Guides user through the entire clone process
 *
 * @param {Function} promptPassword - Password prompt function
 */
async function interactiveClone(promptPassword) {
  console.log('\n' + '='.repeat(50));
  console.log('  CLONE FLOPPY DISK');
  console.log('='.repeat(50));

  // Check source disk
  const manifest = integrity.getManifest();
  if (!manifest) {
    console.log('\nError: No manifest found on source disk.');
    console.log('Run "sign" command first to create a manifest.');
    return { success: false };
  }

  // Display source info
  console.log('\nSource Disk:');
  console.log(`  ID: ${manifest.diskId}`);
  console.log(`  Name: ${manifest.diskName}`);
  console.log(`  Signer: ${manifest.signerAddress || '(not signed)'}`);
  console.log(`  Entries: ${manifest.entryCount || 0}`);
  console.log(`  Last signed: ${manifest.signedAt || 'never'}`);

  // Confirm
  const confirm = await promptInput('\nProceed with clone? (yes/no): ');
  if (confirm.toLowerCase() !== 'yes') {
    console.log('Cancelled.');
    return { success: false };
  }

  // Get password
  let password = null;
  const signChoice = await promptInput('Sign the clone? (yes/no): ');
  if (signChoice.toLowerCase() === 'yes') {
    password = await promptPassword('Enter keystore password: ');
  }

  // Execute clone
  return await cloneDisk({ password });
}

/**
 * Restore from backup
 * Similar to clone but with different UX flow
 *
 * @param {object} options - Restore options
 */
async function restoreFromBackup(options = {}) {
  console.log('\n' + '='.repeat(50));
  console.log('  RESTORE FROM BACKUP');
  console.log('='.repeat(50));

  console.log('\nThis will restore a backup disk to a new disk.');
  console.log('The backup disk should be currently mounted.');

  // Verify it's a clone
  const manifest = integrity.getManifest();
  if (!manifest) {
    console.log('\nError: No manifest found. Is this a valid backup?');
    return { success: false };
  }

  if (!manifest.parentDiskId) {
    console.log('\nWarning: This disk does not appear to be a clone.');
    console.log(`  Disk ID: ${manifest.diskId}`);
  } else {
    console.log(`\nBackup of: ${manifest.parentDiskId}`);
    console.log(`Generation: ${manifest.cloneGeneration}`);
  }

  // Proceed with clone to restore
  return await cloneDisk(options);
}

// ============================================================================
// Mother/Clone Branching Operations
// ============================================================================

/**
 * Initialize current disk as a mother
 *
 * @param {string} motherId - Unique ID for this mother
 * @returns {object} Registry
 */
function initMother(motherId) {
  if (registry.isMother()) {
    throw new Error('This disk is already a mother');
  }

  if (registry.isClone()) {
    throw new Error('This disk is a clone, cannot convert to mother');
  }

  // Initialize registry
  const reg = registry.initializeMother(motherId);

  console.log('\nMother disk initialized!');
  console.log(`  ID: ${motherId}`);
  console.log(`  Next clone index: ${reg.nextIndex}`);
  console.log('\nYou can now fork clones with: node cli.js fork --name=<clone-name>');

  return reg;
}

/**
 * Create a birth certificate for a clone
 * Signed by mother to prove clone legitimacy
 *
 * @param {object} options
 * @param {string} options.cloneId - Clone ID
 * @param {string} options.motherId - Mother ID
 * @param {number} options.derivationIndex - Clone's derivation index
 * @param {string} options.xprvHash - Hash of clone's xprv (for verification)
 * @param {number} options.ttlDays - Time-to-live in days (default: 30)
 * @param {string} options.motherPrivateKey - Mother's ETH private key for signing
 * @returns {object} Birth certificate with signature
 */
function createBirthCertificate(options) {
  const {
    cloneId,
    motherId,
    derivationIndex,
    derivationPath,
    xprvHash,
    ttlDays = 30,
    motherPrivateKey
  } = options;

  const now = new Date();
  const expiresAt = new Date(now.getTime() + ttlDays * 24 * 60 * 60 * 1000);

  const certificate = {
    version: 1,
    cloneId,
    motherId,
    derivationIndex,
    derivationPath,
    xprvHash,
    createdAt: now.toISOString(),
    expiresAt: expiresAt.toISOString(),
    ttlDays
  };

  // Create message to sign
  const message = JSON.stringify(certificate, Object.keys(certificate).sort());
  const messageHash = require('ethers').hashMessage(message);

  // Sign with mother's key
  const { Wallet } = require('ethers');
  const wallet = new Wallet(motherPrivateKey);
  const signature = wallet.signMessageSync(message);

  return {
    ...certificate,
    motherAddress: wallet.address,
    signature
  };
}

/**
 * Verify a birth certificate
 *
 * @param {object} certificate - Birth certificate to verify
 * @param {string} expectedMotherAddress - Expected mother's ETH address
 * @returns {object} { valid, expired, errors }
 */
function verifyBirthCertificate(certificate, expectedMotherAddress) {
  const errors = [];

  // Reconstruct message
  const certCopy = { ...certificate };
  delete certCopy.motherAddress;
  delete certCopy.signature;
  const message = JSON.stringify(certCopy, Object.keys(certCopy).sort());

  // Verify signature
  const { verifyMessage } = require('ethers');
  let recoveredAddress;
  try {
    recoveredAddress = verifyMessage(message, certificate.signature);
  } catch (e) {
    errors.push('Invalid signature: ' + e.message);
    return { valid: false, expired: false, errors };
  }

  if (recoveredAddress.toLowerCase() !== expectedMotherAddress.toLowerCase()) {
    errors.push(`Signature not from expected mother (got ${recoveredAddress}, expected ${expectedMotherAddress})`);
  }

  // Check expiration
  const now = new Date();
  const expiresAt = new Date(certificate.expiresAt);
  const expired = now > expiresAt;

  if (expired) {
    errors.push(`Certificate expired at ${certificate.expiresAt}`);
  }

  return {
    valid: errors.length === 0,
    expired,
    recoveredAddress,
    errors
  };
}

/**
 * Prepare fork data on mother disk
 * Returns all data needed to create a clone with xprv isolation
 *
 * @param {object} options
 * @param {string} options.cloneId - ID for the new clone
 * @param {string} options.cloneName - Human-readable name
 * @param {string} options.purpose - Purpose description
 * @param {string} options.motherPassword - Password to decrypt mother's mnemonic (REQUIRED for xprv isolation)
 * @param {number} options.ttlDays - Clone time-to-live in days (default: 30)
 * @returns {Promise<object>} Fork data to write to clone disk
 */
async function prepareFork(options) {
  if (!registry.isMother()) {
    throw new Error('This disk is not a mother. Run "init-mother" first.');
  }

  const { cloneId, cloneName, purpose = '', motherPassword, ttlDays = 30 } = options;

  if (!cloneId) {
    throw new Error('Clone ID is required');
  }

  if (!motherPassword) {
    throw new Error('Mother password is required for secure xprv-based cloning');
  }

  // Get current state
  const identity = require('./identity');
  const entries = identity.getMemory();
  const currentManifest = integrity.getManifest();
  const currentSequence = entries.reduce((max, e) => Math.max(max, e.sequence || 0), 0);

  // Register clone and get derivation index
  const cloneRecord = registry.registerClone({
    cloneId,
    cloneName: cloneName || cloneId,
    forkSequence: currentSequence,
    purpose
  });

  // Decrypt mnemonic and derive xprv for clone's account
  const { decryptMnemonic } = require('./keystore');
  const { HDNodeWallet } = require('ethers');
  const keystorePath = path.join(KEYSTORE_DIR, CONFIG.KEYSTORE_FILENAME);

  if (!fs.existsSync(keystorePath)) {
    throw new Error('Mother keystore not found');
  }

  const keystore = JSON.parse(fs.readFileSync(keystorePath, 'utf8'));
  console.log('Decrypting mother keystore...');
  const mnemonic = await decryptMnemonic(keystore, motherPassword);

  // Derive the clone's xprv at its account level
  console.log(`Deriving xprv for clone account ${cloneRecord.derivationIndex}...`);
  const hdNode = HDNodeWallet.fromPhrase(mnemonic);
  // Derive to the account level: m/44'/60'/N'
  const cloneNode = hdNode.derivePath(`44'/60'/${cloneRecord.derivationIndex}'`);
  const xprv = cloneNode.extendedKey;

  // Get mother's signing key (account 0)
  const motherNode = hdNode.derivePath("44'/60'/0'/0/0");
  const motherPrivateKey = motherNode.privateKey;
  const motherAddress = motherNode.address;

  // Create xprv hash for verification
  const { keccak256 } = require('ethereum-cryptography/keccak');
  const { utf8ToBytes, bytesToHex } = require('ethereum-cryptography/utils');
  const xprvHash = bytesToHex(keccak256(utf8ToBytes(xprv)));

  // Create birth certificate
  console.log('Creating birth certificate...');
  const birthCertificate = createBirthCertificate({
    cloneId,
    motherId: registry.getRegistry().motherId,
    derivationIndex: cloneRecord.derivationIndex,
    derivationPath: cloneRecord.derivationPath,
    xprvHash,
    ttlDays,
    motherPrivateKey
  });

  // Read identity files (NOT the keystore - clone gets xprv instead)
  const files = {};
  const keystoreFiles = getKeystoreFiles();
  for (const file of keystoreFiles) {
    // Skip registry file - clones don't get it
    if (file.relativePath === 'registry.json') continue;
    // Skip mnemonic keystore - clone gets xprv keystore instead
    if (file.relativePath === CONFIG.KEYSTORE_FILENAME) continue;
    files[file.relativePath] = fs.readFileSync(file.absolutePath);
  }

  // Calculate expiration
  const expiresAt = new Date(Date.now() + ttlDays * 24 * 60 * 60 * 1000).toISOString();

  // Prepare clone manifest
  const cloneManifest = {
    ...(currentManifest || {}),
    diskId: cloneId,
    diskName: cloneName || cloneId,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),

    // Branching metadata
    motherId: registry.getRegistry().motherId,
    motherAddress,
    derivationIndex: cloneRecord.derivationIndex,
    derivationPath: cloneRecord.derivationPath,
    forkSequence: currentSequence,
    forkedAt: new Date().toISOString(),

    // TTL and certificate
    expiresAt,
    ttlDays,
    birthCertificateHash: bytesToHex(keccak256(utf8ToBytes(JSON.stringify(birthCertificate)))),

    // Keystore type
    keystoreType: 'xprv',

    // Legacy clone tracking
    parentDiskId: registry.getRegistry().motherId,
    cloneGeneration: 1,

    // Signature will be added when clone is signed
    signature: null,
    signedAt: null,
    hasUnsignedChanges: true
  };

  // Update clone record with TTL info
  registry.updateClone(cloneId, {
    expiresAt,
    ttlDays,
    primaryAddress: cloneNode.derivePath("0/0").address
  });

  console.log(`\nClone will use xprv isolation (no mnemonic shared)`);
  console.log(`TTL: ${ttlDays} days (expires ${expiresAt})`);

  return {
    cloneId,
    cloneName: cloneName || cloneId,
    cloneRecord,
    files,
    manifest: cloneManifest,
    forkSequence: currentSequence,
    motherId: registry.getRegistry().motherId,
    motherAddress,
    // xprv data for clone keystore
    _xprv: xprv,
    _xprvHash: xprvHash,
    _birthCertificate: birthCertificate,
    _expiresAt: expiresAt,
    _ttlDays: ttlDays
  };
}

/**
 * Write fork data to destination disk (clone disk)
 * Creates xprv-based keystore (no mnemonic shared)
 *
 * @param {object} forkData - Data from prepareFork()
 * @param {object} options - Write options
 * @param {string} options.clonePassword - Password for the clone's xprv keystore (REQUIRED)
 * @returns {Promise<boolean>} Success
 */
async function writeForkToDisk(forkData, options = {}) {
  const { files, manifest, cloneId, _xprv, _xprvHash, _birthCertificate, _expiresAt, _ttlDays } = forkData;
  const { clonePassword } = options;

  if (!clonePassword) {
    throw new Error('Clone password is required for xprv keystore');
  }

  if (!_xprv) {
    throw new Error('No xprv data found. Fork was not prepared with mother password.');
  }

  console.log(`\nWriting clone "${cloneId}" to disk...`);

  // Clear existing keystore if present
  if (fs.existsSync(KEYSTORE_DIR)) {
    fs.rmSync(KEYSTORE_DIR, { recursive: true, force: true });
  }

  // Create xprv keystore (NOT mnemonic keystore)
  console.log('  Creating xprv keystore (cryptographically isolated)...');
  const { encryptXprv } = require('./keystore');
  const xprvKeystore = await encryptXprv(_xprv, clonePassword, {
    cloneId,
    motherId: forkData.motherId,
    derivationIndex: forkData.cloneRecord.derivationIndex,
    derivationPath: forkData.cloneRecord.derivationPath,
    expiresAt: _expiresAt,
    birthCertificate: _birthCertificate
  });

  // Write all identity files
  let modifiedFiles = { ...files };

  for (const [relativePath, content] of Object.entries(modifiedFiles)) {
    const fullPath = path.join(KEYSTORE_DIR, relativePath);
    const dir = path.dirname(fullPath);

    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { mode: 0o700, recursive: true });
    }

    fs.writeFileSync(fullPath, content, { mode: 0o600 });
    console.log(`  Wrote: ${relativePath} (${content.length} bytes)`);
  }

  // Write xprv keystore
  const keystorePath = path.join(KEYSTORE_DIR, CONFIG.KEYSTORE_FILENAME);
  fs.writeFileSync(keystorePath, JSON.stringify(xprvKeystore, null, 2), { mode: 0o600 });
  console.log(`  Wrote: ${CONFIG.KEYSTORE_FILENAME} (xprv keystore)`);

  // Write birth certificate
  const certPath = path.join(IDENTITY_DIR, 'birth-certificate.json');
  if (!fs.existsSync(IDENTITY_DIR)) {
    fs.mkdirSync(IDENTITY_DIR, { mode: 0o700, recursive: true });
  }
  fs.writeFileSync(certPath, JSON.stringify(_birthCertificate, null, 2), { mode: 0o600 });
  console.log(`  Wrote: identity/birth-certificate.json`);

  // Write updated manifest
  const manifestPath = path.join(IDENTITY_DIR, 'manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), { mode: 0o600 });
  console.log(`  Wrote: identity/manifest.json`);

  // Update metadata with clone info
  const metadataPath = path.join(IDENTITY_DIR, 'metadata.json');
  let metadata = {};
  if (fs.existsSync(metadataPath)) {
    metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
  }
  metadata['disk.name'] = forkData.cloneId;
  metadata['disk.mother'] = forkData.motherId;
  metadata['disk.motherAddress'] = forkData.motherAddress;
  metadata['disk.derivationIndex'] = forkData.cloneRecord.derivationIndex;
  metadata['disk.keystoreType'] = 'xprv';
  metadata['disk.expiresAt'] = _expiresAt;
  metadata['disk.ttlDays'] = _ttlDays;
  fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2), { mode: 0o600 });
  console.log(`  Wrote: identity/metadata.json`);

  // Sync
  try {
    execSync('sync', { stdio: 'ignore' });
  } catch {}

  console.log('\n=== Clone Written Successfully ===');
  console.log(`  Keystore type: xprv (isolated, no mnemonic)`);
  console.log(`  Clone ID: ${cloneId}`);
  console.log(`  Mother: ${forkData.motherId}`);
  console.log(`  Derivation Index: ${forkData.cloneRecord.derivationIndex}`);
  console.log(`  Expires: ${_expiresAt}`);
  console.log(`  TTL: ${_ttlDays} days`);
  console.log('\n  This clone CANNOT access other accounts or derive the mnemonic.');

  return true;
}

/**
 * Get status of current disk
 *
 * @returns {object} Status information
 */
function getStatus() {
  const role = registry.getDiskRole();
  const manifest = integrity.getManifest();

  const status = {
    role,
    diskId: manifest?.diskId || 'unknown',
    diskName: manifest?.diskName || 'Unknown',
    entryCount: manifest?.entryCount || 0,
    lastSequence: manifest?.lastSequence || 0,
    hasUnsignedChanges: manifest?.hasUnsignedChanges || false,
    lastSigned: manifest?.signedAt || null
  };

  if (role === 'mother') {
    const reg = registry.getRegistry();
    status.motherId = reg.motherId;
    status.totalClones = reg.clones.length;
    status.activeClones = reg.clones.filter(c => c.status === 'active').length;
    status.nextIndex = reg.nextIndex;
  } else if (role === 'clone') {
    status.motherId = manifest?.motherId;
    status.derivationIndex = manifest?.derivationIndex;
    status.derivationPath = manifest?.derivationPath;
    status.forkSequence = manifest?.forkSequence;
    status.forkedAt = manifest?.forkedAt;
  }

  return status;
}

/**
 * Prepare push data (clone → mother)
 * Exports entries created since fork for mother to import
 *
 * @returns {object} Push data
 */
function preparePush() {
  const role = registry.getDiskRole();
  if (role !== 'clone') {
    throw new Error('Push can only be run from a clone disk');
  }

  const identity = require('./identity');
  const manifest = integrity.getManifest();
  const entries = identity.getMemory();

  // Find entries created since fork
  const forkSequence = manifest.forkSequence || 0;
  const newEntries = entries.filter(e => (e.sequence || 0) > forkSequence);

  return {
    cloneId: manifest.diskId,
    motherId: manifest.motherId,
    derivationIndex: manifest.derivationIndex,
    forkSequence,
    currentSequence: manifest.lastSequence,
    entries: newEntries,
    entryCount: newEntries.length,
    manifest: manifest
  };
}

/**
 * Import push data into mother
 *
 * @param {object} pushData - Data from preparePush()
 * @param {object} options
 * @param {boolean} options.dryRun - Just show what would be imported
 * @param {boolean} options.force - Import even if clone is compromised (dangerous)
 * @returns {object} Import result
 */
function importPush(pushData, options = {}) {
  const role = registry.getDiskRole();
  if (role !== 'mother') {
    throw new Error('Import can only be run on mother disk');
  }

  const { cloneId, entries, forkSequence, currentSequence } = pushData;

  // Verify clone is registered
  const cloneRecord = registry.getClone(cloneId);
  if (!cloneRecord) {
    throw new Error(`Clone "${cloneId}" is not registered with this mother`);
  }

  if (cloneRecord.status === 'revoked') {
    throw new Error(`Clone "${cloneId}" has been revoked`);
  }

  // Check for compromised status
  if (cloneRecord.status === 'compromised' && !options.force) {
    throw new Error(
      `Clone "${cloneId}" is marked as compromised since ${cloneRecord.compromisedAt}. ` +
      `Last trusted sequence: ${cloneRecord.lastTrustedSequence}. ` +
      `Use --force to import anyway (dangerous).`
    );
  }

  // Filter entries based on trust
  const trustedEntries = [];
  const rejectedEntries = [];

  for (const entry of entries) {
    const trustCheck = registry.checkEntryTrust(
      cloneId,
      entry.sequence,
      entry.createdAt
    );

    if (trustCheck && trustCheck.rejected && !options.force) {
      rejectedEntries.push({
        entry,
        reason: trustCheck.reason
      });
    } else {
      trustedEntries.push(entry);
    }
  }

  if (options.dryRun) {
    return {
      dryRun: true,
      cloneId,
      entriesWouldImport: trustedEntries.length,
      entriesWouldReject: rejectedEntries.length,
      rejectedReasons: rejectedEntries.map(r => ({
        sequence: r.entry.sequence,
        reason: r.reason
      })),
      fromSequence: forkSequence,
      toSequence: currentSequence
    };
  }

  // Import trusted entries with attribution
  const identity = require('./identity');
  let imported = 0;

  for (const entry of trustedEntries) {
    // Add with clone attribution
    identity.addMemory({
      type: entry.type,
      content: entry.content,
      tags: [...(entry.tags || []), `from:${cloneId}`],
      importance: entry.importance,
      metadata: {
        ...entry.metadata,
        sourceClone: cloneId,
        sourceSequence: entry.sequence,
        importedAt: new Date().toISOString()
      }
    });
    imported++;
  }

  // Record sync
  registry.recordSync({
    cloneId,
    direction: 'push',
    entriesTransferred: imported,
    entriesRejected: rejectedEntries.length,
    fromSequence: forkSequence,
    toSequence: currentSequence
  });

  return {
    cloneId,
    entriesImported: imported,
    entriesRejected: rejectedEntries.length,
    rejectedReasons: rejectedEntries.map(r => ({
      sequence: r.entry.sequence,
      reason: r.reason
    })),
    fromSequence: forkSequence,
    toSequence: currentSequence
  };
}

/**
 * Prepare pull data (mother → clone)
 * Gets entries from mother that clone doesn't have
 *
 * @param {object} cloneManifest - Clone's current manifest
 * @returns {object} Pull data
 */
function preparePull(cloneManifest) {
  const role = registry.getDiskRole();
  if (role !== 'mother') {
    throw new Error('Pull data can only be prepared from mother disk');
  }

  const identity = require('./identity');
  const entries = identity.getMemory();

  // Find entries created on mother since clone's fork
  // (entries that don't have sourceClone attribution)
  const forkSequence = cloneManifest.forkSequence || 0;
  const motherEntries = entries.filter(e => {
    const seq = e.sequence || 0;
    const isFromMother = !e.metadata?.sourceClone;
    return seq > forkSequence && isFromMother;
  });

  return {
    motherId: registry.getRegistry().motherId,
    cloneId: cloneManifest.diskId,
    forkSequence,
    entries: motherEntries,
    entryCount: motherEntries.length
  };
}

/**
 * Import pull data into clone
 *
 * @param {object} pullData - Data from preparePull()
 * @returns {object} Import result
 */
function importPull(pullData) {
  const role = registry.getDiskRole();
  if (role !== 'clone') {
    throw new Error('Import can only be run on clone disk');
  }

  const { motherId, entries } = pullData;
  const identity = require('./identity');

  let imported = 0;
  for (const entry of entries) {
    identity.addMemory({
      type: entry.type,
      content: entry.content,
      tags: [...(entry.tags || []), `from:mother`],
      importance: entry.importance,
      metadata: {
        ...entry.metadata,
        sourceMother: motherId,
        sourceSequence: entry.sequence,
        importedAt: new Date().toISOString()
      }
    });
    imported++;
  }

  return {
    motherId,
    entriesImported: imported
  };
}

// ============================================================================
// Exports
// ============================================================================

module.exports = {
  // Legacy clone operations
  cloneDisk,
  interactiveClone,
  restoreFromBackup,
  getKeystoreFiles,
  formatBytes,

  // Mother/Clone branching
  initMother,
  prepareFork,
  writeForkToDisk,
  getStatus,

  // Birth certificate
  createBirthCertificate,
  verifyBirthCertificate,

  // Sync operations
  preparePush,
  importPush,
  preparePull,
  importPull
};
