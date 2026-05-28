/**
 * Identity and Memory Storage Module
 *
 * Provides persistent storage for agent identity, DID documents, and memory
 * on the floppy disk alongside cryptographic keys.
 *
 * Storage capacity: ~1.4 MB available after keystores
 *
 * Features:
 * - DID document storage (W3C DID Core compatible)
 * - Agent profile and identity
 * - Persistent memory/notes (encrypted or plain)
 * - Key-value metadata store
 *
 * @module identity
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const CONFIG = require('./config');

const IDENTITY_DIR = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR, 'identity');
const DID_FILE = path.join(IDENTITY_DIR, 'did.json');
const PROFILE_FILE = path.join(IDENTITY_DIR, 'profile.json');
const MEMORY_FILE = path.join(IDENTITY_DIR, 'memory.json');
const MEMORY_ENCRYPTED_FILE = path.join(IDENTITY_DIR, 'memory.enc');
const METADATA_FILE = path.join(IDENTITY_DIR, 'metadata.json');

/**
 * Ensure identity directory exists
 */
function ensureIdentityDir() {
  if (!fs.existsSync(IDENTITY_DIR)) {
    fs.mkdirSync(IDENTITY_DIR, { mode: 0o700, recursive: true });
  }
}

/**
 * Check if identity storage is available
 * @returns {boolean}
 */
function isIdentityAvailable() {
  try {
    const { execSync } = require('child_process');
    execSync(`mountpoint -q "${CONFIG.MOUNT_POINT}"`, { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

// ============================================================================
// DID Document Management
// ============================================================================

/**
 * Create a new DID document for the agent
 *
 * @param {object} options - DID options
 * @param {string} options.method - DID method (default: 'key')
 * @param {string} options.controller - Controller DID (optional)
 * @param {object[]} options.verificationMethods - Additional verification methods
 * @param {object[]} options.services - Service endpoints
 * @returns {object} The created DID document
 */
function createDIDDocument(options = {}) {
  ensureIdentityDir();

  const {
    method = 'key',
    controller = null,
    verificationMethods = [],
    services = []
  } = options;

  // Generate a unique DID identifier
  const didId = crypto.randomBytes(16).toString('hex');
  const did = `did:${method}:${didId}`;

  const didDocument = {
    '@context': [
      'https://www.w3.org/ns/did/v1',
      'https://w3id.org/security/suites/ed25519-2020/v1'
    ],
    id: did,
    controller: controller || did,
    created: new Date().toISOString(),
    updated: new Date().toISOString(),
    verificationMethod: [
      {
        id: `${did}#keys-1`,
        type: 'JsonWebKey2020',
        controller: did,
        // Public key will be derived from floppy keystore when needed
        publicKeyJwk: null
      },
      ...verificationMethods
    ],
    authentication: [`${did}#keys-1`],
    assertionMethod: [`${did}#keys-1`],
    keyAgreement: [],
    service: services
  };

  fs.writeFileSync(DID_FILE, JSON.stringify(didDocument, null, 2), { mode: 0o600 });
  syncDisk();

  return didDocument;
}

/**
 * Get the DID document
 * @returns {object|null}
 */
function getDIDDocument() {
  if (!fs.existsSync(DID_FILE)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(DID_FILE, 'utf8'));
}

/**
 * Update the DID document
 * @param {object} updates - Fields to update
 * @returns {object} Updated DID document
 */
function updateDIDDocument(updates) {
  const doc = getDIDDocument();
  if (!doc) {
    throw new Error('DID document not found. Create one first.');
  }

  const updated = {
    ...doc,
    ...updates,
    updated: new Date().toISOString()
  };

  // Preserve immutable fields
  updated.id = doc.id;
  updated.created = doc.created;

  fs.writeFileSync(DID_FILE, JSON.stringify(updated, null, 2), { mode: 0o600 });
  syncDisk();

  return updated;
}

/**
 * Add a service endpoint to the DID document
 * @param {object} service - Service to add
 */
function addDIDService(service) {
  const doc = getDIDDocument();
  if (!doc) {
    throw new Error('DID document not found');
  }

  doc.service = doc.service || [];
  doc.service.push({
    id: `${doc.id}#${service.id || 'service-' + (doc.service.length + 1)}`,
    type: service.type,
    serviceEndpoint: service.endpoint,
    ...service
  });

  return updateDIDDocument({ service: doc.service });
}

/**
 * Create an AT Protocol compatible DID document (did:web)
 *
 * AT Protocol requires specific fields:
 * - alsoKnownAs: Handle URI (at://handle.domain)
 * - verificationMethod: Multikey type with secp256k1 or P-256
 * - service: AtprotoPersonalDataServer endpoint
 *
 * @param {object} options - AT Protocol DID options
 * @param {string} options.domain - Web domain for did:web (e.g., 'example.com')
 * @param {string} options.handle - AT Protocol handle (e.g., 'alice.bsky.social')
 * @param {string} options.pdsUrl - Personal Data Server URL
 * @param {string} options.publicKeyMultibase - Multibase-encoded public key (optional)
 * @param {object[]} options.additionalServices - Additional service endpoints
 * @returns {object} AT Protocol compatible DID document
 */
function createATProtoDIDDocument(options = {}) {
  ensureIdentityDir();

  const {
    domain,
    handle,
    pdsUrl,
    publicKeyMultibase = null,
    additionalServices = []
  } = options;

  if (!domain) {
    throw new Error('domain is required for did:web');
  }

  if (!handle) {
    throw new Error('handle is required for AT Protocol DID');
  }

  if (!pdsUrl) {
    throw new Error('pdsUrl is required for AT Protocol DID');
  }

  const did = `did:web:${domain}`;

  // Build alsoKnownAs with AT Protocol handle
  const alsoKnownAs = [`at://${handle}`];

  // Build verification method
  const verificationMethod = [];
  if (publicKeyMultibase) {
    verificationMethod.push({
      id: `${did}#atproto`,
      type: 'Multikey',
      controller: did,
      publicKeyMultibase: publicKeyMultibase
    });
  } else {
    // Placeholder - key will be derived from floppy keystore
    verificationMethod.push({
      id: `${did}#atproto`,
      type: 'Multikey',
      controller: did,
      publicKeyMultibase: null // To be populated with actual key
    });
  }

  // Build services
  const services = [
    {
      id: '#atproto_pds',
      type: 'AtprotoPersonalDataServer',
      serviceEndpoint: pdsUrl
    },
    ...additionalServices
  ];

  const didDocument = {
    '@context': ['https://www.w3.org/ns/did/v1'],
    id: did,
    alsoKnownAs: alsoKnownAs,
    verificationMethod: verificationMethod,
    service: services
  };

  // Store metadata about the DID
  const metadata = {
    created: new Date().toISOString(),
    updated: new Date().toISOString(),
    protocol: 'atproto',
    handle: handle,
    domain: domain
  };

  // Save DID document
  fs.writeFileSync(DID_FILE, JSON.stringify(didDocument, null, 2), { mode: 0o600 });

  // Save metadata separately
  const metadataPath = path.join(IDENTITY_DIR, 'did-metadata.json');
  fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2), { mode: 0o600 });

  syncDisk();

  return didDocument;
}

/**
 * Get AT Protocol DID metadata
 * @returns {object|null}
 */
function getATProtoMetadata() {
  const metadataPath = path.join(IDENTITY_DIR, 'did-metadata.json');
  if (!fs.existsSync(metadataPath)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
}

/**
 * Update handle in AT Protocol DID document
 * @param {string} newHandle - New AT Protocol handle
 * @returns {object} Updated DID document
 */
function updateATProtoHandle(newHandle) {
  const doc = getDIDDocument();
  if (!doc) {
    throw new Error('DID document not found');
  }

  // Update alsoKnownAs
  doc.alsoKnownAs = [`at://${newHandle}`];

  fs.writeFileSync(DID_FILE, JSON.stringify(doc, null, 2), { mode: 0o600 });

  // Update metadata
  const metadataPath = path.join(IDENTITY_DIR, 'did-metadata.json');
  if (fs.existsSync(metadataPath)) {
    const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
    metadata.handle = newHandle;
    metadata.updated = new Date().toISOString();
    fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2), { mode: 0o600 });
  }

  syncDisk();
  return doc;
}

/**
 * Set the public key in the DID document for AT Protocol
 *
 * This derives the public key from the floppy keystore and encodes it
 * as multibase for AT Protocol compatibility.
 *
 * @param {string} publicKeyHex - Public key in hex format (from Ethereum derivation)
 * @returns {object} Updated DID document
 */
function setATProtoPublicKey(publicKeyHex) {
  const doc = getDIDDocument();
  if (!doc) {
    throw new Error('DID document not found');
  }

  // Convert hex public key to multibase format (base58btc with 'z' prefix)
  // AT Protocol uses compressed secp256k1 keys
  const keyBytes = Buffer.from(publicKeyHex.replace('0x', ''), 'hex');

  // Multicodec prefix for secp256k1-pub is 0xe7 0x01
  const multicodecPrefix = Buffer.from([0xe7, 0x01]);
  const multicodecKey = Buffer.concat([multicodecPrefix, keyBytes]);

  // Encode as base58btc with 'z' prefix (multibase)
  const bs58 = require('bs58') || { encode: (b) => b.toString('base64') };
  let publicKeyMultibase;
  try {
    publicKeyMultibase = 'z' + bs58.encode(multicodecKey);
  } catch {
    // Fallback if bs58 not available
    publicKeyMultibase = 'z' + multicodecKey.toString('base64');
  }

  // Update verification method
  if (doc.verificationMethod && doc.verificationMethod.length > 0) {
    doc.verificationMethod[0].publicKeyMultibase = publicKeyMultibase;
  }

  fs.writeFileSync(DID_FILE, JSON.stringify(doc, null, 2), { mode: 0o600 });
  syncDisk();

  return doc;
}

/**
 * Validate DID document for AT Protocol compatibility
 *
 * @param {object} doc - DID document to validate
 * @returns {object} Validation result { valid: boolean, errors: string[], warnings: string[] }
 */
function validateATProtoDID(doc = null) {
  const didDoc = doc || getDIDDocument();
  const errors = [];
  const warnings = [];

  if (!didDoc) {
    return { valid: false, errors: ['No DID document found'], warnings: [] };
  }

  // Check required fields
  if (!didDoc.id) {
    errors.push('Missing required field: id');
  } else if (!didDoc.id.startsWith('did:web:') && !didDoc.id.startsWith('did:plc:')) {
    errors.push('AT Protocol requires did:web or did:plc method');
  }

  if (!didDoc.alsoKnownAs || didDoc.alsoKnownAs.length === 0) {
    errors.push('Missing required field: alsoKnownAs (must contain at:// handle)');
  } else {
    const hasAtHandle = didDoc.alsoKnownAs.some(aka => aka.startsWith('at://'));
    if (!hasAtHandle) {
      errors.push('alsoKnownAs must contain at least one at:// handle URI');
    }
  }

  if (!didDoc.verificationMethod || didDoc.verificationMethod.length === 0) {
    errors.push('Missing required field: verificationMethod');
  } else {
    const atprotoKey = didDoc.verificationMethod.find(vm =>
      vm.id.includes('#atproto') || vm.type === 'Multikey'
    );
    if (!atprotoKey) {
      warnings.push('No verification method with #atproto id or Multikey type found');
    } else if (!atprotoKey.publicKeyMultibase) {
      warnings.push('Verification method missing publicKeyMultibase');
    }
  }

  if (!didDoc.service || didDoc.service.length === 0) {
    errors.push('Missing required field: service');
  } else {
    const pdsService = didDoc.service.find(s => s.type === 'AtprotoPersonalDataServer');
    if (!pdsService) {
      errors.push('Missing AtprotoPersonalDataServer service endpoint');
    }
  }

  // Check context
  if (!didDoc['@context'] || !didDoc['@context'].includes('https://www.w3.org/ns/did/v1')) {
    warnings.push('Missing or invalid @context');
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Export DID document for web hosting (did:web)
 *
 * Returns the document formatted for hosting at /.well-known/did.json
 *
 * @returns {string} JSON string ready for web hosting
 */
function exportDIDForWeb() {
  const doc = getDIDDocument();
  if (!doc) {
    throw new Error('No DID document found');
  }

  // Remove any internal metadata fields
  const exportDoc = { ...doc };
  delete exportDoc.created;
  delete exportDoc.updated;

  return JSON.stringify(exportDoc, null, 2);
}

/**
 * Create an ENS-based DID document (did:ens)
 *
 * Note: did:ens is NOT supported by AT Protocol (Bluesky).
 * Use this for general DID purposes with Ethereum ecosystem.
 *
 * The DID document should be stored in ENS text records:
 * - Key: "did" or "vnd.did"
 * - Value: JSON DID document
 *
 * @param {object} options - ENS DID options
 * @param {string} options.ensName - ENS name (e.g., 'chipprbots.eth')
 * @param {string} options.chainId - Ethereum chain ID (default: '1' for mainnet)
 * @param {object[]} options.services - Service endpoints
 * @returns {object} ENS DID document
 */
function createENSDIDDocument(options = {}) {
  ensureIdentityDir();

  const {
    ensName,
    chainId = '1',
    services = []
  } = options;

  if (!ensName) {
    throw new Error('ensName is required for did:ens');
  }

  if (!ensName.endsWith('.eth')) {
    throw new Error('ensName must end with .eth');
  }

  const did = `did:ens:${ensName}`;

  // Build verification method
  const verificationMethod = [{
    id: `${did}#controller`,
    type: 'EcdsaSecp256k1RecoveryMethod2020',
    controller: did,
    // The ENS owner address will be the controller
    blockchainAccountId: `eip155:${chainId}:ENS_OWNER_ADDRESS`
  }];

  const didDocument = {
    '@context': [
      'https://www.w3.org/ns/did/v1',
      'https://w3id.org/security/suites/secp256k1recovery-2020/v2'
    ],
    id: did,
    controller: did,
    verificationMethod: verificationMethod,
    authentication: [`${did}#controller`],
    assertionMethod: [`${did}#controller`],
    service: services
  };

  // Store metadata
  const metadata = {
    created: new Date().toISOString(),
    updated: new Date().toISOString(),
    protocol: 'ens',
    ensName: ensName,
    chainId: chainId
  };

  fs.writeFileSync(DID_FILE, JSON.stringify(didDocument, null, 2), { mode: 0o600 });

  const metadataPath = path.join(IDENTITY_DIR, 'did-metadata.json');
  fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2), { mode: 0o600 });

  syncDisk();

  return didDocument;
}

/**
 * Export DID document for ENS text record storage
 *
 * Returns a compact JSON string suitable for ENS text records.
 * Note: ENS text records have practical size limits (~10KB recommended).
 *
 * @returns {object} { textRecord: string, size: number, instructions: string }
 */
function exportDIDForENS() {
  const doc = getDIDDocument();
  if (!doc) {
    throw new Error('No DID document found');
  }

  // Create minimal document for ENS storage
  const exportDoc = { ...doc };
  delete exportDoc.created;
  delete exportDoc.updated;

  const json = JSON.stringify(exportDoc);
  const size = Buffer.byteLength(json, 'utf8');

  return {
    textRecord: json,
    size: size,
    sizeFormatted: `${(size / 1024).toFixed(2)} KB`,
    instructions: `
To store this DID in ENS:
1. Go to app.ens.domains
2. Select your domain
3. Add text record with key: "did"
4. Paste the textRecord value as the value
5. Save the transaction

The DID will be resolvable as: did:ens:${doc.id.replace('did:ens:', '')}

Note: did:ens is NOT supported by AT Protocol (Bluesky).
For Bluesky, use did:web with a traditional web domain.
    `.trim()
  };
}

// ============================================================================
// Agent Profile
// ============================================================================

/**
 * Create or update agent profile
 *
 * @param {object} profile - Profile data
 * @param {string} profile.name - Agent name
 * @param {string} profile.description - Agent description
 * @param {string} profile.version - Agent version
 * @param {string[]} profile.capabilities - List of capabilities
 * @param {object} profile.preferences - Agent preferences
 * @returns {object} The profile
 */
function setProfile(profile) {
  ensureIdentityDir();

  const existing = getProfile() || {};

  const updated = {
    ...existing,
    ...profile,
    updatedAt: new Date().toISOString(),
    createdAt: existing.createdAt || new Date().toISOString()
  };

  fs.writeFileSync(PROFILE_FILE, JSON.stringify(updated, null, 2), { mode: 0o600 });
  syncDisk();

  return updated;
}

/**
 * Get agent profile
 * @returns {object|null}
 */
function getProfile() {
  if (!fs.existsSync(PROFILE_FILE)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(PROFILE_FILE, 'utf8'));
}

// ============================================================================
// Persistent Memory
// ============================================================================

/**
 * Memory entry structure
 * @typedef {object} MemoryEntry
 * @property {string} id - Unique identifier
 * @property {number} sequence - Monotonic sequence number (for integrity verification)
 * @property {string} type - Entry type (note, context, fact, etc.)
 * @property {string} content - The content
 * @property {string[]} tags - Searchable tags
 * @property {number} importance - 1-10 importance score
 * @property {string} createdAt - ISO timestamp
 * @property {string} updatedAt - ISO timestamp
 * @property {string} previousHash - Hash chain link (for integrity verification)
 * @property {object} metadata - Additional metadata
 */

/**
 * Get all memory entries
 * @returns {MemoryEntry[]}
 */
function getMemory() {
  if (!fs.existsSync(MEMORY_FILE)) {
    return [];
  }
  const data = JSON.parse(fs.readFileSync(MEMORY_FILE, 'utf8'));
  return data.entries || [];
}

/**
 * Get memory data including metadata
 * @returns {object} { entries, stats, nextSequence }
 */
function getMemoryData() {
  if (!fs.existsSync(MEMORY_FILE)) {
    return { entries: [], stats: { count: 0 }, nextSequence: 1 };
  }
  const data = JSON.parse(fs.readFileSync(MEMORY_FILE, 'utf8'));
  return {
    entries: data.entries || [],
    stats: data.stats || { count: 0 },
    nextSequence: data.nextSequence || (data.entries?.length || 0) + 1
  };
}

/**
 * Get the next sequence number
 * @returns {number}
 */
function getNextSequence() {
  const data = getMemoryData();
  return data.nextSequence;
}

/**
 * Get the last entry hash for chain linking
 * @returns {string}
 */
function getLastEntryHash() {
  const entries = getMemory();
  if (entries.length === 0) {
    return '0x0';
  }
  // Sort by sequence to get the last one
  const sorted = [...entries].sort((a, b) => (b.sequence || 0) - (a.sequence || 0));
  const lastEntry = sorted[0];

  // Compute hash of last entry
  const integrity = require('./integrity');
  // Find the previous hash for this entry
  const prevEntry = sorted[1];
  const prevHash = prevEntry
    ? integrity.computeEntryHash(prevEntry, prevEntry.previousHash || '0x0')
    : '0x0';

  return integrity.computeEntryHash(lastEntry, prevHash);
}

/**
 * Add a memory entry
 *
 * @param {object} entry - Memory entry
 * @param {string} entry.type - Entry type
 * @param {string} entry.content - Content
 * @param {string[]} entry.tags - Tags
 * @param {number} entry.importance - Importance (1-10)
 * @param {object} options - Additional options
 * @param {boolean} options.updateManifest - Update manifest after adding (default: true)
 * @returns {MemoryEntry}
 */
function addMemory(entry, options = {}) {
  ensureIdentityDir();

  const memoryData = getMemoryData();
  const entries = memoryData.entries;
  const sequence = memoryData.nextSequence;

  // Get previous entry hash for chain linking
  const previousHash = getLastEntryHash();

  const newEntry = {
    id: crypto.randomBytes(8).toString('hex'),
    sequence,
    type: entry.type || 'note',
    content: entry.content,
    tags: entry.tags || [],
    importance: Math.min(10, Math.max(1, entry.importance || 5)),
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    previousHash,
    metadata: entry.metadata || {}
  };

  entries.push(newEntry);

  const data = {
    version: 1,
    entries,
    nextSequence: sequence + 1,
    stats: {
      count: entries.length,
      lastUpdated: new Date().toISOString()
    }
  };

  fs.writeFileSync(MEMORY_FILE, JSON.stringify(data, null, 2), { mode: 0o600 });
  syncDisk();

  // Update manifest (mark as having unsigned changes)
  if (options.updateManifest !== false) {
    updateManifestAfterChange();
  }

  return newEntry;
}

/**
 * Update manifest after a memory change
 * This marks the manifest as having unsigned changes
 */
function updateManifestAfterChange() {
  try {
    const integrity = require('./integrity');
    const entries = getMemory();
    const metadata = getMetadata();

    // Create/update manifest without signing
    integrity.createManifest(entries, {
      diskId: metadata['disk.name'] || 'unknown',
      diskName: metadata['disk.network'] || 'Unknown Disk'
    });
  } catch (e) {
    // Ignore errors during manifest update
    // The manifest will be updated when sign command is run
  }
}

/**
 * Search memory entries
 *
 * @param {object} query - Search query
 * @param {string} query.type - Filter by type
 * @param {string[]} query.tags - Filter by tags (any match)
 * @param {string} query.text - Full-text search in content
 * @param {number} query.minImportance - Minimum importance
 * @param {number} query.limit - Max results
 * @returns {MemoryEntry[]}
 */
function searchMemory(query = {}) {
  let entries = getMemory();

  if (query.type) {
    entries = entries.filter(e => e.type === query.type);
  }

  if (query.tags && query.tags.length > 0) {
    entries = entries.filter(e =>
      query.tags.some(tag => e.tags.includes(tag))
    );
  }

  if (query.text) {
    const searchTerm = query.text.toLowerCase();
    entries = entries.filter(e =>
      e.content.toLowerCase().includes(searchTerm)
    );
  }

  if (query.minImportance) {
    entries = entries.filter(e => e.importance >= query.minImportance);
  }

  // Sort by importance desc, then by date desc
  entries.sort((a, b) => {
    if (b.importance !== a.importance) {
      return b.importance - a.importance;
    }
    return new Date(b.createdAt) - new Date(a.createdAt);
  });

  if (query.limit) {
    entries = entries.slice(0, query.limit);
  }

  return entries;
}

/**
 * Update a memory entry
 *
 * @param {string} id - Entry ID
 * @param {object} updates - Fields to update
 * @param {object} options - Additional options
 * @param {boolean} options.updateManifest - Update manifest after change (default: true)
 * @returns {MemoryEntry|null}
 */
function updateMemory(id, updates, options = {}) {
  const memoryData = getMemoryData();
  const entries = memoryData.entries;
  const index = entries.findIndex(e => e.id === id);

  if (index === -1) {
    return null;
  }

  entries[index] = {
    ...entries[index],
    ...updates,
    id: entries[index].id, // Preserve ID
    sequence: entries[index].sequence, // Preserve sequence
    createdAt: entries[index].createdAt, // Preserve creation date
    previousHash: entries[index].previousHash, // Preserve chain link
    updatedAt: new Date().toISOString()
  };

  const data = {
    version: 1,
    entries,
    nextSequence: memoryData.nextSequence,
    stats: {
      count: entries.length,
      lastUpdated: new Date().toISOString()
    }
  };

  fs.writeFileSync(MEMORY_FILE, JSON.stringify(data, null, 2), { mode: 0o600 });
  syncDisk();

  // Update manifest
  if (options.updateManifest !== false) {
    updateManifestAfterChange();
  }

  return entries[index];
}

/**
 * Delete a memory entry
 *
 * Note: Deleting entries breaks the hash chain. The manifest will track
 * gaps in sequence numbers as a result of deletions.
 *
 * @param {string} id - Entry ID
 * @param {object} options - Additional options
 * @param {boolean} options.updateManifest - Update manifest after change (default: true)
 * @returns {boolean}
 */
function deleteMemory(id, options = {}) {
  const memoryData = getMemoryData();
  const entries = memoryData.entries;
  const filtered = entries.filter(e => e.id !== id);

  if (filtered.length === entries.length) {
    return false;
  }

  const data = {
    version: 1,
    entries: filtered,
    nextSequence: memoryData.nextSequence, // Don't reset sequence
    stats: {
      count: filtered.length,
      lastUpdated: new Date().toISOString()
    }
  };

  fs.writeFileSync(MEMORY_FILE, JSON.stringify(data, null, 2), { mode: 0o600 });
  syncDisk();

  // Update manifest
  if (options.updateManifest !== false) {
    updateManifestAfterChange();
  }

  return true;
}

/**
 * Clear all memory entries
 *
 * @param {object} options - Additional options
 * @param {boolean} options.updateManifest - Update manifest after change (default: true)
 */
function clearMemory(options = {}) {
  if (fs.existsSync(MEMORY_FILE)) {
    fs.unlinkSync(MEMORY_FILE);
    syncDisk();

    // Update manifest
    if (options.updateManifest !== false) {
      updateManifestAfterChange();
    }
  }
}

// ============================================================================
// Encrypted Memory (for sensitive data)
// ============================================================================

/**
 * Save encrypted memory
 *
 * @param {object} data - Data to encrypt
 * @param {string} password - Encryption password
 */
async function saveEncryptedMemory(data, password) {
  ensureIdentityDir();

  const salt = crypto.randomBytes(32);
  const iv = crypto.randomBytes(16);

  // Derive key with scrypt (lower params for faster operation)
  const key = crypto.scryptSync(password, salt, 32, {
    N: 16384,
    r: 8,
    p: 1
  });

  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const plaintext = JSON.stringify(data);

  const encrypted = Buffer.concat([
    cipher.update(plaintext, 'utf8'),
    cipher.final()
  ]);

  const authTag = cipher.getAuthTag();

  const envelope = {
    version: 1,
    cipher: 'aes-256-gcm',
    kdf: 'scrypt',
    kdfparams: { n: 16384, r: 8, p: 1, dklen: 32 },
    salt: salt.toString('hex'),
    iv: iv.toString('hex'),
    ciphertext: encrypted.toString('hex'),
    authTag: authTag.toString('hex'),
    createdAt: new Date().toISOString()
  };

  fs.writeFileSync(
    MEMORY_ENCRYPTED_FILE,
    JSON.stringify(envelope, null, 2),
    { mode: 0o600 }
  );
  syncDisk();
}

/**
 * Load encrypted memory
 *
 * @param {string} password - Decryption password
 * @returns {object} Decrypted data
 */
function loadEncryptedMemory(password) {
  if (!fs.existsSync(MEMORY_ENCRYPTED_FILE)) {
    return null;
  }

  const envelope = JSON.parse(fs.readFileSync(MEMORY_ENCRYPTED_FILE, 'utf8'));

  const salt = Buffer.from(envelope.salt, 'hex');
  const iv = Buffer.from(envelope.iv, 'hex');
  const ciphertext = Buffer.from(envelope.ciphertext, 'hex');
  const authTag = Buffer.from(envelope.authTag, 'hex');

  const key = crypto.scryptSync(password, salt, 32, {
    N: envelope.kdfparams.n,
    r: envelope.kdfparams.r,
    p: envelope.kdfparams.p
  });

  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag);

  const decrypted = Buffer.concat([
    decipher.update(ciphertext),
    decipher.final()
  ]);

  return JSON.parse(decrypted.toString('utf8'));
}

// ============================================================================
// Key-Value Metadata Store
// ============================================================================

/**
 * Get all metadata
 * @returns {object}
 */
function getMetadata() {
  if (!fs.existsSync(METADATA_FILE)) {
    return {};
  }
  return JSON.parse(fs.readFileSync(METADATA_FILE, 'utf8'));
}

/**
 * Set a metadata value
 *
 * @param {string} key - Key
 * @param {*} value - Value (must be JSON serializable)
 */
function setMetadataValue(key, value) {
  ensureIdentityDir();

  const metadata = getMetadata();
  metadata[key] = value;

  fs.writeFileSync(METADATA_FILE, JSON.stringify(metadata, null, 2), { mode: 0o600 });
  syncDisk();
}

/**
 * Get a metadata value
 *
 * @param {string} key - Key
 * @param {*} defaultValue - Default if not found
 * @returns {*}
 */
function getMetadataValue(key, defaultValue = null) {
  const metadata = getMetadata();
  return metadata.hasOwnProperty(key) ? metadata[key] : defaultValue;
}

/**
 * Delete a metadata value
 *
 * @param {string} key - Key
 */
function deleteMetadataValue(key) {
  const metadata = getMetadata();
  delete metadata[key];

  fs.writeFileSync(METADATA_FILE, JSON.stringify(metadata, null, 2), { mode: 0o600 });
  syncDisk();
}

// ============================================================================
// Disk Space Management
// ============================================================================

/**
 * Sync filesystem to ensure data is written
 */
function syncDisk() {
  try {
    const { execSync } = require('child_process');
    execSync('sync', { stdio: 'ignore' });
  } catch {
    // Ignore sync errors
  }
}

/**
 * Get storage statistics
 *
 * @returns {object} Storage stats
 */
function getStorageStats() {
  const FLOPPY_CAPACITY = 1474560; // 1.44 MB in bytes

  let usedBytes = 0;
  const files = {};

  const keystoreDir = path.join(CONFIG.MOUNT_POINT, CONFIG.KEYSTORE_DIR);

  function countDir(dir) {
    if (!fs.existsSync(dir)) return;

    const items = fs.readdirSync(dir);
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        countDir(fullPath);
      } else {
        usedBytes += stat.size;
        files[fullPath.replace(keystoreDir, '')] = stat.size;
      }
    }
  }

  if (fs.existsSync(keystoreDir)) {
    countDir(keystoreDir);
  }

  const availableBytes = FLOPPY_CAPACITY - usedBytes - 10240; // Reserve 10KB for filesystem

  return {
    capacity: FLOPPY_CAPACITY,
    capacityFormatted: formatBytes(FLOPPY_CAPACITY),
    used: usedBytes,
    usedFormatted: formatBytes(usedBytes),
    available: Math.max(0, availableBytes),
    availableFormatted: formatBytes(Math.max(0, availableBytes)),
    usedPercent: ((usedBytes / FLOPPY_CAPACITY) * 100).toFixed(1),
    files
  };
}

/**
 * Format bytes as human-readable string
 */
function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// ============================================================================
// Exports
// ============================================================================

module.exports = {
  // Availability
  isIdentityAvailable,
  ensureIdentityDir,

  // DID Document
  createDIDDocument,
  getDIDDocument,
  updateDIDDocument,
  addDIDService,

  // AT Protocol DID
  createATProtoDIDDocument,
  getATProtoMetadata,
  updateATProtoHandle,
  setATProtoPublicKey,
  validateATProtoDID,
  exportDIDForWeb,

  // ENS DID
  createENSDIDDocument,
  exportDIDForENS,

  // Profile
  setProfile,
  getProfile,

  // Memory (plain)
  getMemory,
  getMemoryData,
  getNextSequence,
  getLastEntryHash,
  addMemory,
  searchMemory,
  updateMemory,
  deleteMemory,
  clearMemory,
  updateManifestAfterChange,

  // Memory (encrypted)
  saveEncryptedMemory,
  loadEncryptedMemory,

  // Metadata
  getMetadata,
  setMetadataValue,
  getMetadataValue,
  deleteMetadataValue,

  // Storage
  getStorageStats,
  syncDisk,

  // Paths
  IDENTITY_DIR,
  DID_FILE,
  PROFILE_FILE,
  MEMORY_FILE,
  MEMORY_ENCRYPTED_FILE,
  METADATA_FILE
};
