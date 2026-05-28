<overview>
Keys are identity in Nostr. A compromised key means complete account takeover. This reference covers secure key generation, storage, and best practices for protecting Nostr identities.
</overview>

<key_fundamentals>
## Key Structure

Nostr uses secp256k1 elliptic curve cryptography:
- **Secret key (sk):** 32 bytes (256 bits) - KEEP SECRET
- **Public key (pk):** 32 bytes (x-coordinate only) - Share freely
- **Signature:** 64 bytes (Schnorr BIP-340)

```typescript
import { generateSecretKey, getPublicKey } from 'nostr-tools/pure'

const sk = generateSecretKey()  // Uint8Array (32 bytes)
const pk = getPublicKey(sk)     // hex string (64 chars)
```
</key_fundamentals>

<human_readable>
## Human-Readable Formats (NIP-19)

```typescript
import * as nip19 from 'nostr-tools/nip19'

// Secret key
const nsec = nip19.nsecEncode(sk)  // nsec1...
// NEVER share nsec!

// Public key
const npub = nip19.npubEncode(pk)  // npub1...
// Safe to share

// With relay hints
const nprofile = nip19.nprofileEncode({
  pubkey: pk,
  relays: ['wss://relay.example.com']
})

// Decode any format
const { type, data } = nip19.decode('npub1...')
```

**Prefixes:**
- `nsec1` - Secret key (NEVER share)
- `npub1` - Public key
- `note1` - Event ID
- `nprofile1` - Profile with relays
- `nevent1` - Event with relays
- `naddr1` - Addressable event
</human_readable>

<storage_options>
## Storage Strategies

**Browser (Web Apps):**

| Method | Security | Persistence | Use Case |
|--------|----------|-------------|----------|
| Memory only | High | None | Session-only |
| localStorage | Low | Yes | **NOT RECOMMENDED** |
| IndexedDB encrypted | Medium | Yes | Long-term with password |
| NIP-46 (remote) | High | N/A | **RECOMMENDED** |

**Node.js / Server:**

| Method | Security | Use Case |
|--------|----------|----------|
| Environment var | Medium | Development |
| Encrypted file | High | Production |
| Hardware security module | Very High | High-value accounts |

**Mobile:**
- Use platform secure storage (Keychain/Keystore)
- Never store in plaintext
</storage_options>

<secure_storage>
## Secure Storage Implementation

**Browser with encryption:**

```typescript
import { generateSecretKey, getPublicKey } from 'nostr-tools/pure'

// Encrypt key with password before storage
async function encryptKey(sk: Uint8Array, password: string): Promise<string> {
  const salt = crypto.getRandomValues(new Uint8Array(16))
  const iv = crypto.getRandomValues(new Uint8Array(12))

  // Derive key from password
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(password),
    'PBKDF2',
    false,
    ['deriveBits', 'deriveKey']
  )

  const encryptionKey = await crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256' },
    keyMaterial,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt']
  )

  const encrypted = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    encryptionKey,
    sk
  )

  // Combine salt + iv + ciphertext
  const combined = new Uint8Array(salt.length + iv.length + encrypted.byteLength)
  combined.set(salt)
  combined.set(iv, salt.length)
  combined.set(new Uint8Array(encrypted), salt.length + iv.length)

  return btoa(String.fromCharCode(...combined))
}

async function decryptKey(encrypted: string, password: string): Promise<Uint8Array> {
  const combined = Uint8Array.from(atob(encrypted), c => c.charCodeAt(0))

  const salt = combined.slice(0, 16)
  const iv = combined.slice(16, 28)
  const ciphertext = combined.slice(28)

  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(password),
    'PBKDF2',
    false,
    ['deriveBits', 'deriveKey']
  )

  const encryptionKey = await crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256' },
    keyMaterial,
    { name: 'AES-GCM', length: 256 },
    false,
    ['decrypt']
  )

  const decrypted = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv },
    encryptionKey,
    ciphertext
  )

  return new Uint8Array(decrypted)
}
```
</secure_storage>

<nip46>
## NIP-46: Remote Signing (Bunker)

For web apps, use NIP-46 to keep keys on a separate device:

```typescript
import { generateSecretKey } from 'nostr-tools/pure'

// Client creates local keypair for communication
const localSk = generateSecretKey()

// User provides bunker connection string
// bunker://pubkey?relay=wss://relay.example.com

// Client requests signature from bunker
// Bunker (mobile app or hardware) signs events

// Benefits:
// - Keys never touch web browser
// - User approves each signature
// - Works across devices
```

**Bunker providers:**
- nsec.app
- Amber (Android)
- Nostrudel bunker mode
- Hardware signers
</nip46>

<key_derivation>
## Key Derivation

Derive multiple keys from a master seed:

```typescript
import { sha256 } from '@noble/hashes/sha256'
import { bytesToHex } from '@noble/hashes/utils'

function deriveKey(masterSeed: Uint8Array, path: string): Uint8Array {
  // Simple derivation (for more robust, use BIP-32)
  const combined = new TextEncoder().encode(bytesToHex(masterSeed) + path)
  return sha256(combined)
}

// Usage
const masterSeed = generateSecretKey()

const mainKey = deriveKey(masterSeed, 'main')
const chatKey = deriveKey(masterSeed, 'chat')
const appKey = deriveKey(masterSeed, 'app/myapp')
```
</key_derivation>

<backup>
## Key Backup

```typescript
// Export for backup (user must secure this!)
function exportKey(sk: Uint8Array): string {
  const nsec = nip19.nsecEncode(sk)
  return nsec  // User should write this down securely
}

// Import from backup
function importKey(nsec: string): Uint8Array {
  const { type, data } = nip19.decode(nsec)
  if (type !== 'nsec') throw new Error('Not a secret key')
  return data as Uint8Array
}

// Generate mnemonic (BIP-39) for backup
// Use a library like 'bip39' for mnemonic generation
```
</backup>

<security_practices>
## Security Best Practices

**DO:**
- Generate keys with cryptographically secure random
- Encrypt keys before any storage
- Use NIP-46 for web apps
- Clear keys from memory when done
- Backup keys securely (mnemonic or encrypted)
- Use different keys for different purposes

**DON'T:**
- Store keys in localStorage unencrypted
- Log keys or include in error messages
- Commit keys to git
- Send keys over network (except encrypted)
- Use predictable seeds
- Reuse keys across apps with different trust levels
</security_practices>

<key_rotation>
## Key Rotation

Nostr doesn't have native key rotation, but you can:

```typescript
// 1. Create new keypair
const newSk = generateSecretKey()
const newPk = getPublicKey(newSk)

// 2. Publish announcement from old key
const announcement = finalizeEvent({
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [['p', newPk]],
  content: `Migrating to new key: ${nip19.npubEncode(newPk)}`
}, oldSk)

// 3. Publish same announcement from new key
const confirmation = finalizeEvent({
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [['p', oldPk]],
  content: `Migrated from: ${nip19.npubEncode(oldPk)}`
}, newSk)

// 4. Rebuild followers/following from new key
// 5. Keep old key for verification but don't use for new content
```
</key_rotation>

<compromised_key>
## If Key Is Compromised

1. **Stop using the key immediately**
2. Generate new keypair
3. Announce migration from a trusted channel (not Nostr)
4. Publish deletion requests for sensitive content (kind 5)
5. Contact relay operators if needed
6. Rebuild identity with new key

**Prevention:**
- Regular security audits
- Monitor for unauthorized posts
- Use separate keys for different risk levels
- Implement NIP-46 for web apps
</compromised_key>
