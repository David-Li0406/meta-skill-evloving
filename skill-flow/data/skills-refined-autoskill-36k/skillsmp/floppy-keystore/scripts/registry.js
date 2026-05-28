/**
 * Clone Registry Module
 *
 * Manages the mother disk's registry of all spawned clones.
 * Tracks derivation indices, fork points, and sync history.
 *
 * Derivation Strategy:
 * - Each clone gets a unique BIP-44 account index
 * - Clone N uses path: m/44'/60'/N'/0/*
 * - This provides 2^31 addresses per clone (no collision possible)
 *
 * @module registry
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const CONFIG = require('./config');

const KEYSTORE_DIR = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR);
const REGISTRY_FILE = path.join(KEYSTORE_DIR, 'registry.json');

/**
 * Default registry structure
 */
function createEmptyRegistry(motherId) {
  return {
    version: 2,
    type: 'mother',
    motherId: motherId,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),

    // Derivation tracking
    // Index 0 is reserved for mother's own addresses
    // Clones start at index 1+
    nextIndex: 1,

    // Clone records
    clones: [],

    // Sync history
    syncHistory: []
  };
}

/**
 * Check if this disk is a mother (has registry)
 * @returns {boolean}
 */
function isMother() {
  return fs.existsSync(REGISTRY_FILE);
}

/**
 * Check if this disk is a clone (has clone metadata but no registry)
 * @returns {boolean}
 */
function isClone() {
  const manifestPath = path.join(KEYSTORE_DIR, 'identity', 'manifest.json');
  if (!fs.existsSync(manifestPath)) return false;

  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  return manifest.derivationIndex !== undefined && manifest.derivationIndex !== null;
}

/**
 * Get registry (mother disk only)
 * @returns {object|null}
 */
function getRegistry() {
  if (!fs.existsSync(REGISTRY_FILE)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(REGISTRY_FILE, 'utf8'));
}

/**
 * Save registry
 * @param {object} registry
 */
function saveRegistry(registry) {
  registry.updatedAt = new Date().toISOString();
  fs.writeFileSync(REGISTRY_FILE, JSON.stringify(registry, null, 2), { mode: 0o600 });

  // Sync to floppy
  try {
    const { execSync } = require('child_process');
    execSync('sync', { stdio: 'ignore' });
  } catch {
    // Ignore sync errors
  }
}

/**
 * Initialize this disk as a mother
 * @param {string} motherId - Unique identifier for this mother
 * @returns {object} The new registry
 */
function initializeMother(motherId) {
  if (isMother()) {
    throw new Error('This disk is already a mother');
  }

  if (isClone()) {
    throw new Error('This disk is a clone, cannot convert to mother');
  }

  const registry = createEmptyRegistry(motherId);
  saveRegistry(registry);

  return registry;
}

/**
 * Register a new clone (called on mother disk)
 *
 * @param {object} options
 * @param {string} options.cloneId - Unique identifier for the clone
 * @param {string} options.cloneName - Human-readable name
 * @param {number} options.forkSequence - Sequence number at fork point
 * @param {string} options.purpose - Purpose/description of this clone
 * @returns {object} Clone record with assigned derivation index
 */
function registerClone(options) {
  const registry = getRegistry();
  if (!registry) {
    throw new Error('This disk is not a mother. Run "init-mother" first.');
  }

  const { cloneId, cloneName, forkSequence = 0, purpose = '' } = options;

  // Check for duplicate ID
  if (registry.clones.find(c => c.id === cloneId)) {
    throw new Error(`Clone with ID "${cloneId}" already exists`);
  }

  // Assign next derivation index
  const derivationIndex = registry.nextIndex;
  registry.nextIndex++;

  // Create clone record
  const cloneRecord = {
    id: cloneId,
    name: cloneName || cloneId,
    derivationIndex,
    derivationPath: `m/44'/60'/${derivationIndex}'/0`,
    purpose,

    // Fork tracking
    forkedAt: new Date().toISOString(),
    forkSequence,

    // Sync tracking
    lastSyncToMother: null,
    lastSyncFromMother: null,
    lastSyncSequence: forkSequence,

    // Status
    status: 'active', // active, archived, revoked

    // Address will be populated when clone is created
    primaryAddress: null
  };

  registry.clones.push(cloneRecord);
  saveRegistry(registry);

  return cloneRecord;
}

/**
 * Update clone record (e.g., after sync)
 *
 * @param {string} cloneId
 * @param {object} updates
 * @returns {object} Updated clone record
 */
function updateClone(cloneId, updates) {
  const registry = getRegistry();
  if (!registry) {
    throw new Error('This disk is not a mother');
  }

  const index = registry.clones.findIndex(c => c.id === cloneId);
  if (index === -1) {
    throw new Error(`Clone "${cloneId}" not found`);
  }

  // Update allowed fields
  const allowedFields = [
    'name', 'purpose', 'status',
    'lastSyncToMother', 'lastSyncFromMother', 'lastSyncSequence',
    'primaryAddress',
    'expiresAt', 'ttlDays', 'xprvHash', 'birthCertificateHash'
  ];

  for (const field of allowedFields) {
    if (updates[field] !== undefined) {
      registry.clones[index][field] = updates[field];
    }
  }

  saveRegistry(registry);
  return registry.clones[index];
}

/**
 * Get clone record by ID
 *
 * @param {string} cloneId
 * @returns {object|null}
 */
function getClone(cloneId) {
  const registry = getRegistry();
  if (!registry) return null;

  return registry.clones.find(c => c.id === cloneId) || null;
}

/**
 * Get clone record by derivation index
 *
 * @param {number} index
 * @returns {object|null}
 */
function getCloneByIndex(index) {
  const registry = getRegistry();
  if (!registry) return null;

  return registry.clones.find(c => c.derivationIndex === index) || null;
}

/**
 * List all clones
 *
 * @param {object} filter - Optional filter
 * @param {string} filter.status - Filter by status
 * @returns {object[]}
 */
function listClones(filter = {}) {
  const registry = getRegistry();
  if (!registry) return [];

  let clones = [...registry.clones];

  if (filter.status) {
    clones = clones.filter(c => c.status === filter.status);
  }

  return clones;
}

/**
 * Record a sync event
 *
 * @param {object} syncEvent
 * @param {string} syncEvent.cloneId
 * @param {string} syncEvent.direction - 'push' (clone→mother) or 'pull' (mother→clone)
 * @param {number} syncEvent.entriesTransferred
 * @param {number} syncEvent.fromSequence
 * @param {number} syncEvent.toSequence
 */
function recordSync(syncEvent) {
  const registry = getRegistry();
  if (!registry) {
    throw new Error('This disk is not a mother');
  }

  const event = {
    ...syncEvent,
    timestamp: new Date().toISOString(),
    id: crypto.randomBytes(8).toString('hex')
  };

  registry.syncHistory.push(event);

  // Keep last 100 sync events
  if (registry.syncHistory.length > 100) {
    registry.syncHistory = registry.syncHistory.slice(-100);
  }

  // Update clone's sync timestamps
  const cloneIndex = registry.clones.findIndex(c => c.id === syncEvent.cloneId);
  if (cloneIndex !== -1) {
    if (syncEvent.direction === 'push') {
      registry.clones[cloneIndex].lastSyncToMother = event.timestamp;
    } else {
      registry.clones[cloneIndex].lastSyncFromMother = event.timestamp;
    }
    registry.clones[cloneIndex].lastSyncSequence = syncEvent.toSequence;
  }

  saveRegistry(registry);
  return event;
}

/**
 * Get sync history for a clone
 *
 * @param {string} cloneId
 * @param {number} limit
 * @returns {object[]}
 */
function getSyncHistory(cloneId, limit = 10) {
  const registry = getRegistry();
  if (!registry) return [];

  return registry.syncHistory
    .filter(e => e.cloneId === cloneId)
    .slice(-limit);
}

/**
 * Revoke a clone (mark as untrusted)
 *
 * @param {string} cloneId
 * @param {string} reason
 * @returns {object}
 */
function revokeClone(cloneId, reason = '') {
  const registry = getRegistry();
  if (!registry) {
    throw new Error('This disk is not a mother');
  }

  const index = registry.clones.findIndex(c => c.id === cloneId);
  if (index === -1) {
    throw new Error(`Clone "${cloneId}" not found`);
  }

  registry.clones[index].status = 'revoked';
  registry.clones[index].revokedAt = new Date().toISOString();
  registry.clones[index].revokeReason = reason;

  saveRegistry(registry);
  return registry.clones[index];
}

// ============================================================================
// Nullifier / Compromise Management
// ============================================================================

/**
 * Mark a clone as compromised after a certain point
 * All entries from this clone after the last trusted sync will be rejected
 *
 * @param {string} cloneId - ID of the compromised clone
 * @param {string} reason - Reason for marking as compromised
 * @returns {object} Updated clone record
 */
function markCompromised(cloneId, reason = '') {
  const registry = getRegistry();
  if (!registry) {
    throw new Error('This disk is not a mother');
  }

  const index = registry.clones.findIndex(c => c.id === cloneId);
  if (index === -1) {
    throw new Error(`Clone "${cloneId}" not found`);
  }

  const clone = registry.clones[index];

  // Mark as compromised - trust nothing after last successful sync
  clone.status = 'compromised';
  clone.compromisedAt = new Date().toISOString();
  clone.compromiseReason = reason;
  // lastTrustedSequence is the last sync sequence we trust
  clone.lastTrustedSequence = clone.lastSyncSequence || clone.forkSequence;
  clone.lastTrustedAt = clone.lastSyncToMother || clone.forkedAt;

  saveRegistry(registry);
  return clone;
}

/**
 * Clear compromised status (if clone is recovered/re-secured)
 *
 * @param {string} cloneId
 * @returns {object} Updated clone record
 */
function clearCompromised(cloneId) {
  const registry = getRegistry();
  if (!registry) {
    throw new Error('This disk is not a mother');
  }

  const index = registry.clones.findIndex(c => c.id === cloneId);
  if (index === -1) {
    throw new Error(`Clone "${cloneId}" not found`);
  }

  const clone = registry.clones[index];

  if (clone.status !== 'compromised') {
    throw new Error(`Clone "${cloneId}" is not marked as compromised`);
  }

  clone.status = 'active';
  delete clone.compromisedAt;
  delete clone.compromiseReason;
  delete clone.lastTrustedSequence;
  delete clone.lastTrustedAt;

  saveRegistry(registry);
  return clone;
}

/**
 * Check if an entry from a clone should be rejected
 * Returns rejection reason if entry is after the trust cutoff
 *
 * @param {string} cloneId - Source clone ID
 * @param {number} entrySequence - Sequence number of the entry
 * @param {string} entryCreatedAt - ISO timestamp of entry creation
 * @returns {object|null} { rejected: true, reason: '...' } or null if trusted
 */
function checkEntryTrust(cloneId, entrySequence, entryCreatedAt) {
  const registry = getRegistry();
  if (!registry) return null;

  const clone = registry.clones.find(c => c.id === cloneId);
  if (!clone) return null;

  // Check if clone is compromised
  if (clone.status === 'compromised') {
    // Reject if entry is after the last trusted point
    if (entrySequence > clone.lastTrustedSequence) {
      return {
        rejected: true,
        reason: `Entry sequence ${entrySequence} is after trust cutoff ${clone.lastTrustedSequence}`,
        lastTrustedSequence: clone.lastTrustedSequence,
        compromisedAt: clone.compromisedAt
      };
    }

    // Also check timestamp if available
    if (clone.lastTrustedAt && entryCreatedAt) {
      const trustedTime = new Date(clone.lastTrustedAt).getTime();
      const entryTime = new Date(entryCreatedAt).getTime();
      if (entryTime > trustedTime) {
        return {
          rejected: true,
          reason: `Entry created after trust cutoff time`,
          lastTrustedAt: clone.lastTrustedAt,
          compromisedAt: clone.compromisedAt
        };
      }
    }
  }

  // Check if clone is revoked (reject everything)
  if (clone.status === 'revoked') {
    return {
      rejected: true,
      reason: `Clone "${cloneId}" is revoked: ${clone.revokeReason || 'no reason'}`,
      revokedAt: clone.revokedAt
    };
  }

  return null; // Entry is trusted
}

/**
 * Get all compromised clones
 *
 * @returns {object[]} Array of compromised clone records
 */
function getCompromisedClones() {
  const registry = getRegistry();
  if (!registry) return [];

  return registry.clones.filter(c => c.status === 'compromised');
}

/**
 * Generate derivation path for a clone's Nth address
 *
 * @param {number} cloneIndex - Clone's derivation index
 * @param {number} addressIndex - Address index within clone (default: 0)
 * @param {string} chain - Chain ID (default: 'ethereum')
 * @returns {string} Full derivation path
 */
function getDerivationPath(cloneIndex, addressIndex = 0, chain = 'ethereum') {
  const chainConfig = CONFIG.getChainConfig(chain);
  if (!chainConfig) {
    throw new Error(`Unknown chain: ${chain}`);
  }

  // Use clone index as account level
  // Standard: m/purpose'/coin_type'/account'/change/address_index
  const coinType = chainConfig.coinType;
  return `m/44'/${coinType}'/${cloneIndex}'/0/${addressIndex}`;
}

/**
 * Get info about derivation space
 *
 * @returns {object}
 */
function getDerivationInfo() {
  const registry = getRegistry();

  return {
    totalClonesCreated: registry ? registry.nextIndex : 0,
    activeClones: registry ? registry.clones.filter(c => c.status === 'active').length : 0,
    maxClonesSupported: Math.pow(2, 31), // 2^31 hardened indices
    addressesPerClone: Math.pow(2, 31), // 2^31 addresses per clone
    derivationScheme: "m/44'/coin'/clone_index'/0/address_index"
  };
}

// ============================================================================
// Clone-side functions (for use on clone disks)
// ============================================================================

/**
 * Get this clone's metadata from manifest
 * @returns {object|null}
 */
function getCloneMetadata() {
  const manifestPath = path.join(KEYSTORE_DIR, 'identity', 'manifest.json');
  if (!fs.existsSync(manifestPath)) return null;

  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

  if (manifest.derivationIndex === undefined) {
    return null; // Not a clone
  }

  return {
    cloneId: manifest.diskId,
    cloneName: manifest.diskName,
    derivationIndex: manifest.derivationIndex,
    derivationPath: manifest.derivationPath,
    motherId: manifest.motherId,
    forkSequence: manifest.forkSequence,
    forkedAt: manifest.forkedAt
  };
}

/**
 * Get this disk's role
 * @returns {string} 'mother', 'clone', or 'standalone'
 */
function getDiskRole() {
  if (isMother()) return 'mother';
  if (isClone()) return 'clone';
  return 'standalone';
}

// ============================================================================
// Exports
// ============================================================================

module.exports = {
  // Registry management
  createEmptyRegistry,
  getRegistry,
  saveRegistry,
  initializeMother,

  // Clone management
  registerClone,
  updateClone,
  getClone,
  getCloneByIndex,
  listClones,
  revokeClone,

  // Compromise management
  markCompromised,
  clearCompromised,
  checkEntryTrust,
  getCompromisedClones,

  // Sync tracking
  recordSync,
  getSyncHistory,

  // Derivation
  getDerivationPath,
  getDerivationInfo,

  // Disk role detection
  isMother,
  isClone,
  getDiskRole,
  getCloneMetadata,

  // Paths
  REGISTRY_FILE
};
