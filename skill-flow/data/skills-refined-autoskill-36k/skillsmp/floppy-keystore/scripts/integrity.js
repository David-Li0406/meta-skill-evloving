/**
 * Integrity Module - Merkle Tree, Signing, and Verification
 *
 * Provides cryptographic verification for floppy disk keystores:
 * - Merkle tree construction from memory entries
 * - ETH signature of manifest (signed by disk's derived key)
 * - Non-interactive verification
 * - Gap detection for sequence numbers
 *
 * @module integrity
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { keccak256 } = require('ethereum-cryptography/keccak');
const { secp256k1 } = require('ethereum-cryptography/secp256k1');
const { bytesToHex, hexToBytes, utf8ToBytes } = require('ethereum-cryptography/utils');
const CONFIG = require('./config');

const IDENTITY_DIR = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR, 'identity');
const MANIFEST_FILE = path.join(IDENTITY_DIR, 'manifest.json');

// ============================================================================
// Entry Hash Computation
// ============================================================================

/**
 * Compute deterministic hash for a memory entry
 * Hash includes chain link to previous entry for ordering verification
 *
 * @param {object} entry - Memory entry
 * @param {string} previousHash - Hash of previous entry (or '0x0' for first)
 * @returns {string} Hex-encoded keccak256 hash
 */
function computeEntryHash(entry, previousHash = '0x0') {
  // Build deterministic string representation
  const data = [
    entry.id,
    String(entry.sequence || 0),
    entry.content,
    entry.createdAt,
    previousHash
  ].join('|');

  const hash = keccak256(utf8ToBytes(data));
  return '0x' + bytesToHex(hash);
}

/**
 * Compute hash for an entire entry with all fields
 * Used for file-level integrity checking
 *
 * @param {object} entry - Complete memory entry
 * @returns {string} Hex-encoded hash
 */
function computeFullEntryHash(entry) {
  const sorted = JSON.stringify(entry, Object.keys(entry).sort());
  const hash = keccak256(utf8ToBytes(sorted));
  return '0x' + bytesToHex(hash);
}

// ============================================================================
// Merkle Tree Construction
// ============================================================================

/**
 * Build Merkle tree from memory entries
 *
 * @param {object[]} entries - Array of memory entries (must have sequence numbers)
 * @returns {object} { root, tree, proofs, chainHead }
 */
function buildMerkleTree(entries) {
  if (!entries || entries.length === 0) {
    return {
      root: '0x0',
      tree: [],
      proofs: {},
      chainHead: '0x0',
      entryHashes: []
    };
  }

  // Sort entries by sequence number
  const sorted = [...entries].sort((a, b) => (a.sequence || 0) - (b.sequence || 0));

  // Compute chained hashes for each entry
  const entryHashes = [];
  let previousHash = '0x0';

  for (const entry of sorted) {
    const hash = computeEntryHash(entry, previousHash);
    entryHashes.push({
      id: entry.id,
      sequence: entry.sequence || 0,
      hash
    });
    previousHash = hash;
  }

  const chainHead = previousHash;

  // Build Merkle tree from entry hashes
  const leaves = entryHashes.map(e => e.hash);
  const tree = [leaves];
  const proofs = {};

  // Initialize proof paths for each leaf
  leaves.forEach((_, i) => {
    proofs[entryHashes[i].id] = { path: [], indices: [] };
  });

  // Build tree level by level
  let currentLevel = leaves;
  let levelIndex = 0;

  while (currentLevel.length > 1) {
    const nextLevel = [];

    for (let i = 0; i < currentLevel.length; i += 2) {
      const left = currentLevel[i];
      const right = currentLevel[i + 1] || left; // Duplicate if odd

      // Combine and hash
      const combined = left < right ? left + right : right + left;
      const parentHash = '0x' + bytesToHex(keccak256(utf8ToBytes(combined)));
      nextLevel.push(parentHash);

      // Update proofs for leaves in this subtree
      for (let j = 0; j < entryHashes.length; j++) {
        const leafIndex = Math.floor(j / Math.pow(2, levelIndex));
        const pairIndex = Math.floor(leafIndex / 2) * 2;

        if (Math.floor(leafIndex) === pairIndex || Math.floor(leafIndex) === pairIndex + 1) {
          const isLeft = leafIndex % 2 === 0;
          const siblingHash = isLeft ? (currentLevel[leafIndex + 1] || left) : currentLevel[leafIndex - 1];

          if (levelIndex === Math.floor(Math.log2(j + 1)) || levelIndex < tree.length) {
            // Only add sibling if at the correct level
          }
        }
      }
    }

    tree.push(nextLevel);
    currentLevel = nextLevel;
    levelIndex++;
  }

  const root = currentLevel[0] || '0x0';

  // Rebuild proofs correctly
  for (let i = 0; i < entryHashes.length; i++) {
    const proof = buildProofForIndex(tree, i);
    proofs[entryHashes[i].id] = proof;
  }

  return {
    root,
    tree,
    proofs,
    chainHead,
    entryHashes,
    entryCount: entries.length
  };
}

/**
 * Build Merkle proof for a specific leaf index
 *
 * @param {string[][]} tree - Complete Merkle tree
 * @param {number} leafIndex - Index of the leaf
 * @returns {object} { path, indices }
 */
function buildProofForIndex(tree, leafIndex) {
  const path = [];
  const indices = [];
  let currentIndex = leafIndex;

  for (let level = 0; level < tree.length - 1; level++) {
    const currentLevel = tree[level];
    const isLeft = currentIndex % 2 === 0;
    const siblingIndex = isLeft ? currentIndex + 1 : currentIndex - 1;

    if (siblingIndex < currentLevel.length) {
      path.push(currentLevel[siblingIndex]);
      indices.push(isLeft ? 'right' : 'left');
    } else if (currentLevel.length % 2 === 1 && currentIndex === currentLevel.length - 1) {
      // Odd number of nodes, duplicate the last
      path.push(currentLevel[currentIndex]);
      indices.push('right');
    }

    currentIndex = Math.floor(currentIndex / 2);
  }

  return { path, indices };
}

/**
 * Verify a Merkle proof
 *
 * @param {string} leafHash - Hash of the leaf to verify
 * @param {object} proof - { path, indices }
 * @param {string} root - Expected Merkle root
 * @returns {boolean}
 */
function verifyMerkleProof(leafHash, proof, root) {
  let currentHash = leafHash;

  for (let i = 0; i < proof.path.length; i++) {
    const sibling = proof.path[i];
    const isLeft = proof.indices[i] === 'left';

    const combined = isLeft ? sibling + currentHash : currentHash + sibling;
    currentHash = '0x' + bytesToHex(keccak256(utf8ToBytes(combined)));
  }

  return currentHash === root;
}

// ============================================================================
// Manifest Signing
// ============================================================================

/**
 * Create signature message for manifest
 *
 * @param {object} manifest - Manifest data to sign
 * @returns {Uint8Array} Message hash to sign
 */
function createSignatureMessage(manifest) {
  // Create deterministic message from key fields
  const message = [
    'FLOPPY_KEYSTORE_MANIFEST_V1',
    manifest.diskId,
    manifest.merkleRoot,
    String(manifest.entryCount),
    String(manifest.lastSequence),
    manifest.chainHead
  ].join('|');

  return keccak256(utf8ToBytes(message));
}

/**
 * Sign manifest with private key
 *
 * @param {object} manifestData - Manifest data to sign
 * @param {Uint8Array|string} privateKey - Private key (hex or bytes)
 * @returns {object} { signature, signerAddress, signedAt }
 */
function signManifest(manifestData, privateKey) {
  const messageHash = createSignatureMessage(manifestData);

  // Convert private key if needed
  const keyBytes = typeof privateKey === 'string'
    ? hexToBytes(privateKey.replace('0x', ''))
    : privateKey;

  // Sign with secp256k1
  const signature = secp256k1.sign(messageHash, keyBytes);

  // Get public key and derive address
  const publicKey = secp256k1.getPublicKey(keyBytes, false);
  const publicKeyHash = keccak256(publicKey.slice(1)); // Remove 0x04 prefix
  const address = '0x' + bytesToHex(publicKeyHash.slice(-20));

  return {
    signature: '0x' + signature.toCompactHex() + (signature.recovery === 0 ? '1b' : '1c'),
    signerAddress: address,
    signedAt: new Date().toISOString()
  };
}

/**
 * Verify manifest signature
 *
 * @param {object} manifest - Complete manifest with signature
 * @returns {object} { valid, recoveredAddress, error }
 */
function verifyManifestSignature(manifest) {
  if (!manifest.signature || !manifest.signerAddress) {
    return { valid: false, error: 'No signature present' };
  }

  try {
    const messageHash = createSignatureMessage(manifest);
    const sigBytes = hexToBytes(manifest.signature.replace('0x', ''));

    // Extract recovery bit
    const recoveryBit = sigBytes[64] - 27;
    const signatureBytes = sigBytes.slice(0, 64);

    // Create signature object
    const sig = secp256k1.Signature.fromCompact(signatureBytes).addRecoveryBit(recoveryBit);

    // Recover public key
    const publicKey = sig.recoverPublicKey(messageHash);
    const publicKeyBytes = publicKey.toRawBytes(false);
    const publicKeyHash = keccak256(publicKeyBytes.slice(1));
    const recoveredAddress = '0x' + bytesToHex(publicKeyHash.slice(-20));

    const valid = recoveredAddress.toLowerCase() === manifest.signerAddress.toLowerCase();

    return {
      valid,
      recoveredAddress,
      expectedAddress: manifest.signerAddress,
      error: valid ? null : 'Signature does not match signer address'
    };
  } catch (error) {
    return { valid: false, error: error.message };
  }
}

// ============================================================================
// Manifest Management
// ============================================================================

/**
 * Get current manifest
 *
 * @returns {object|null}
 */
function getManifest() {
  if (!fs.existsSync(MANIFEST_FILE)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(MANIFEST_FILE, 'utf8'));
}

/**
 * Save manifest to disk
 *
 * @param {object} manifest - Manifest to save
 */
function saveManifest(manifest) {
  const dir = path.dirname(MANIFEST_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { mode: 0o700, recursive: true });
  }

  fs.writeFileSync(MANIFEST_FILE, JSON.stringify(manifest, null, 2), { mode: 0o600 });

  // Sync to floppy
  try {
    const { execSync } = require('child_process');
    execSync('sync', { stdio: 'ignore' });
  } catch {
    // Ignore sync errors
  }
}

/**
 * Create or update manifest from current memory state
 *
 * @param {object[]} entries - Memory entries
 * @param {object} options - { diskId, diskName, privateKey, derivationIndex, motherId, forkSequence }
 * @returns {object} Updated manifest
 */
function createManifest(entries, options = {}) {
  const existing = getManifest();

  // Build Merkle tree
  const { root, chainHead, entryCount, entryHashes } = buildMerkleTree(entries);

  // Get file hashes
  const fileHashes = computeFileHashes();

  // Compute last sequence
  const lastSequence = entries.reduce((max, e) => Math.max(max, e.sequence || 0), 0);

  const manifest = {
    version: 1,
    diskId: options.diskId || existing?.diskId || 'unknown',
    diskName: options.diskName || existing?.diskName || 'Unknown Disk',
    createdAt: existing?.createdAt || new Date().toISOString(),
    updatedAt: new Date().toISOString(),

    // Integrity
    merkleRoot: root,
    entryCount,
    lastSequence,
    chainHead,

    // File hashes
    files: fileHashes,

    // Clone tracking (legacy)
    parentDiskId: existing?.parentDiskId || options.parentDiskId || null,
    cloneGeneration: existing?.cloneGeneration || options.cloneGeneration || 0,

    // Mother/Clone relationship (new branching model)
    motherId: existing?.motherId || options.motherId || null,
    derivationIndex: existing?.derivationIndex ?? options.derivationIndex ?? null,
    derivationPath: existing?.derivationPath || options.derivationPath || null,
    forkSequence: existing?.forkSequence ?? options.forkSequence ?? null,
    forkedAt: existing?.forkedAt || options.forkedAt || null,

    // Signature (to be added)
    signerAddress: existing?.signerAddress || null,
    signature: null,
    signedAt: null,

    // Unsigned changes marker
    hasUnsignedChanges: true
  };

  // Sign if private key provided
  if (options.privateKey) {
    const sigData = signManifest(manifest, options.privateKey);
    manifest.signerAddress = sigData.signerAddress;
    manifest.signature = sigData.signature;
    manifest.signedAt = sigData.signedAt;
    manifest.hasUnsignedChanges = false;
  }

  saveManifest(manifest);
  return manifest;
}

/**
 * Compute SHA256 hashes of identity files
 *
 * @returns {object} Map of filename to hash
 */
function computeFileHashes() {
  const hashes = {};
  const files = ['memory.json', 'profile.json', 'metadata.json', 'did.json'];

  for (const file of files) {
    const filePath = path.join(IDENTITY_DIR, file);
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath);
      const hash = crypto.createHash('sha256').update(content).digest('hex');
      hashes[file] = '0x' + hash;
    }
  }

  return hashes;
}

// ============================================================================
// Verification
// ============================================================================

/**
 * Verify disk integrity (non-interactive)
 *
 * @returns {object} Verification result
 */
function verifyDiskIntegrity() {
  const result = {
    valid: true,
    checks: {},
    errors: [],
    warnings: []
  };

  // Check manifest exists
  const manifest = getManifest();
  if (!manifest) {
    result.valid = false;
    result.errors.push('No manifest found');
    return result;
  }

  result.diskId = manifest.diskId;
  result.diskName = manifest.diskName;
  result.signerAddress = manifest.signerAddress;

  // 1. Verify signature
  if (manifest.signature) {
    const sigResult = verifyManifestSignature(manifest);
    result.checks.signature = sigResult.valid;
    if (!sigResult.valid) {
      result.valid = false;
      result.errors.push('Signature verification failed: ' + sigResult.error);
    }
  } else {
    result.checks.signature = false;
    result.warnings.push('Manifest is not signed');
  }

  // 2. Load and verify memory entries
  const memoryPath = path.join(IDENTITY_DIR, 'memory.json');
  let entries = [];
  if (fs.existsSync(memoryPath)) {
    const memoryData = JSON.parse(fs.readFileSync(memoryPath, 'utf8'));
    entries = memoryData.entries || [];
  }

  // 3. Verify Merkle root
  const { root, chainHead, entryCount } = buildMerkleTree(entries);
  result.checks.merkleRoot = root === manifest.merkleRoot;
  if (!result.checks.merkleRoot) {
    result.valid = false;
    result.errors.push(`Merkle root mismatch: computed ${root.slice(0, 18)}... vs manifest ${manifest.merkleRoot?.slice(0, 18)}...`);
  }

  // 4. Verify entry count
  result.checks.entryCount = entryCount === manifest.entryCount;
  if (!result.checks.entryCount) {
    result.valid = false;
    result.errors.push(`Entry count mismatch: ${entryCount} vs ${manifest.entryCount}`);
  }

  result.entryCount = entryCount;

  // 5. Verify chain head
  result.checks.chainHead = chainHead === manifest.chainHead;
  if (!result.checks.chainHead) {
    result.warnings.push('Chain head mismatch (entries may have been reordered)');
  }

  // 6. Check for sequence gaps
  const gapResult = detectSequenceGaps(entries);
  result.checks.noGaps = gapResult.valid;
  result.sequenceRange = gapResult.range;
  if (!gapResult.valid) {
    result.warnings.push(`Sequence gaps detected: missing ${gapResult.missing.join(', ')}`);
  }

  // 7. Verify file hashes
  const currentHashes = computeFileHashes();
  const fileHashResults = {};
  let allFilesMatch = true;

  for (const [file, hash] of Object.entries(manifest.files || {})) {
    const matches = currentHashes[file] === hash;
    fileHashResults[file] = matches;
    if (!matches) {
      allFilesMatch = false;
    }
  }

  result.checks.fileHashes = allFilesMatch;
  result.fileHashes = fileHashResults;
  if (!allFilesMatch) {
    const mismatched = Object.entries(fileHashResults)
      .filter(([, v]) => !v)
      .map(([k]) => k);
    result.warnings.push(`File hash mismatch for: ${mismatched.join(', ')}`);
  }

  // 8. Check for unsigned changes
  result.hasUnsignedChanges = manifest.hasUnsignedChanges || false;
  if (result.hasUnsignedChanges) {
    result.warnings.push('Manifest has unsigned changes');
  }

  result.lastSigned = manifest.signedAt;

  return result;
}

/**
 * Detect gaps in sequence numbers
 *
 * @param {object[]} entries - Memory entries
 * @returns {object} { valid, missing, range }
 */
function detectSequenceGaps(entries) {
  if (!entries || entries.length === 0) {
    return { valid: true, missing: [], range: null };
  }

  const sequences = entries
    .map(e => e.sequence)
    .filter(s => typeof s === 'number')
    .sort((a, b) => a - b);

  if (sequences.length === 0) {
    return { valid: true, missing: [], range: null };
  }

  const missing = [];
  const min = sequences[0];
  const max = sequences[sequences.length - 1];

  for (let i = min; i <= max; i++) {
    if (!sequences.includes(i)) {
      missing.push(i);
    }
  }

  return {
    valid: missing.length === 0,
    missing,
    range: { min, max }
  };
}

/**
 * Compare two disks and return differences
 *
 * @param {object} manifest1 - First disk manifest
 * @param {object} manifest2 - Second disk manifest
 * @returns {object} Diff result
 */
function diffManifests(manifest1, manifest2) {
  const diff = {
    identical: true,
    differences: []
  };

  // Compare key fields
  const fieldsToCompare = [
    'merkleRoot',
    'entryCount',
    'lastSequence',
    'chainHead',
    'signerAddress'
  ];

  for (const field of fieldsToCompare) {
    if (manifest1[field] !== manifest2[field]) {
      diff.identical = false;
      diff.differences.push({
        field,
        disk1: manifest1[field],
        disk2: manifest2[field]
      });
    }
  }

  // Compare file hashes
  const allFiles = new Set([
    ...Object.keys(manifest1.files || {}),
    ...Object.keys(manifest2.files || {})
  ]);

  for (const file of allFiles) {
    const hash1 = manifest1.files?.[file];
    const hash2 = manifest2.files?.[file];
    if (hash1 !== hash2) {
      diff.identical = false;
      diff.differences.push({
        field: `files.${file}`,
        disk1: hash1 || '(missing)',
        disk2: hash2 || '(missing)'
      });
    }
  }

  // Check clone relationship
  if (manifest1.diskId === manifest2.parentDiskId) {
    diff.relationship = 'disk2 is clone of disk1';
    diff.cloneGeneration = manifest2.cloneGeneration;
  } else if (manifest2.diskId === manifest1.parentDiskId) {
    diff.relationship = 'disk1 is clone of disk2';
    diff.cloneGeneration = manifest1.cloneGeneration;
  } else if (manifest1.parentDiskId === manifest2.parentDiskId && manifest1.parentDiskId) {
    diff.relationship = 'sibling clones';
  } else {
    diff.relationship = 'unrelated';
  }

  return diff;
}

// ============================================================================
// Exports
// ============================================================================

module.exports = {
  // Entry hashing
  computeEntryHash,
  computeFullEntryHash,

  // Merkle tree
  buildMerkleTree,
  buildProofForIndex,
  verifyMerkleProof,

  // Signing
  createSignatureMessage,
  signManifest,
  verifyManifestSignature,

  // Manifest
  getManifest,
  saveManifest,
  createManifest,
  computeFileHashes,

  // Verification
  verifyDiskIntegrity,
  detectSequenceGaps,
  diffManifests,

  // Paths
  MANIFEST_FILE
};
