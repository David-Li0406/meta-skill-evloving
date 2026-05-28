<overview>
NIP-44 defines the current standard for encrypted payloads in Nostr. It supersedes NIP-04 (which is deprecated and insecure). Use NIP-44 for any encrypted communication between Nostr users.
</overview>

<nip04_warning>
## NIP-04 Is Deprecated

**DO NOT use NIP-04 for new implementations:**

- No message authentication (messages can be altered undetected)
- Uses AES-CBC without HMAC
- Leaks metadata (pubkeys, timestamps visible)
- Not versioned (cannot upgrade)

If you see `nip04.encrypt()` in code, replace with NIP-44.
</nip04_warning>

<nip44_overview>
## NIP-44 Design

NIP-44 provides:
- **ChaCha20** for encryption (faster than AES, better multi-key security)
- **HMAC-SHA256** for authentication
- **Custom padding** for reduced size leakage
- **Versioning** for future algorithm changes

**Current version:** 2

**Limitations:**
- No forward secrecy (compromised key decrypts all past messages)
- No deniability (signature proves authorship)
- No post-compromise security
- Metadata (pubkeys, timestamps) still visible
</nip44_overview>

<basic_usage>
## Basic Encryption

```typescript
import * as nip44 from 'nostr-tools/nip44'
import { generateSecretKey, getPublicKey } from 'nostr-tools/pure'

// Two users
const aliceSk = generateSecretKey()
const alicePk = getPublicKey(aliceSk)
const bobSk = generateSecretKey()
const bobPk = getPublicKey(bobSk)

// Alice encrypts for Bob
const conversationKey = nip44.getConversationKey(aliceSk, bobPk)
const plaintext = 'Secret message'
const ciphertext = nip44.encrypt(plaintext, conversationKey)

// Bob decrypts (same conversation key!)
const bobConversationKey = nip44.getConversationKey(bobSk, alicePk)
const decrypted = nip44.decrypt(ciphertext, bobConversationKey)
// decrypted === 'Secret message'
```

**Key insight:** The conversation key is symmetric. Both parties derive the same key using their own secret key + the other's public key.
</basic_usage>

<conversation_key>
## Conversation Key Management

Cache conversation keys for performance:

```typescript
class ConversationKeyCache {
  private keys = new Map<string, Uint8Array>()

  constructor(private sk: Uint8Array) {}

  get(peerPk: string): Uint8Array {
    if (!this.keys.has(peerPk)) {
      this.keys.set(peerPk, nip44.getConversationKey(this.sk, peerPk))
    }
    return this.keys.get(peerPk)!
  }

  // Clear when done (security)
  clear() {
    this.keys.clear()
  }
}
```
</conversation_key>

<encrypted_events>
## Creating Encrypted Events

```typescript
interface EncryptedPayload {
  type: string
  data: unknown
}

function createEncryptedEvent(
  recipientPk: string,
  payload: EncryptedPayload,
  kind: number,
  sk: Uint8Array
): Event {
  const conversationKey = nip44.getConversationKey(sk, recipientPk)
  const encrypted = nip44.encrypt(JSON.stringify(payload), conversationKey)

  return finalizeEvent({
    kind,
    created_at: Math.floor(Date.now() / 1000),
    tags: [['p', recipientPk]],
    content: encrypted
  }, sk)
}

function decryptEvent<T>(event: Event, sk: Uint8Array): T {
  const senderPk = event.pubkey
  const conversationKey = nip44.getConversationKey(sk, senderPk)
  const decrypted = nip44.decrypt(event.content, conversationKey)
  return JSON.parse(decrypted) as T
}
```
</encrypted_events>

<group_encryption>
## Group Encryption

For groups, distribute a shared secret:

```typescript
// Leader generates shared secret
const sharedSecret = generateSecretKey()

// Encrypt shared secret for each member
async function inviteMember(memberPk: string, leaderSk: Uint8Array): Promise<Event> {
  const conversationKey = nip44.getConversationKey(leaderSk, memberPk)
  const encrypted = nip44.encrypt(
    Buffer.from(sharedSecret).toString('hex'),
    conversationKey
  )

  return finalizeEvent({
    kind: 24,  // Group invitation kind
    created_at: Math.floor(Date.now() / 1000),
    tags: [['p', memberPk]],
    content: encrypted
  }, leaderSk)
}

// Member receives invitation
function acceptInvitation(inviteEvent: Event, memberSk: Uint8Array): Uint8Array {
  const conversationKey = nip44.getConversationKey(memberSk, inviteEvent.pubkey)
  const secretHex = nip44.decrypt(inviteEvent.content, conversationKey)
  return hexToBytes(secretHex)
}

// Group messages use shared secret
function encryptForGroup(message: string, sharedSecret: Uint8Array): string {
  return nip44.encrypt(message, sharedSecret)
}

function decryptFromGroup(ciphertext: string, sharedSecret: Uint8Array): string {
  return nip44.decrypt(ciphertext, sharedSecret)
}
```
</group_encryption>

<nip17_overview>
## NIP-17: Private Direct Messages

For full privacy (hiding who is communicating), use NIP-17 which combines:
- **NIP-44** for encryption
- **NIP-59** for gift wrapping (hiding metadata)

```typescript
// NIP-17 structure:
// 1. Create the DM content
// 2. Encrypt with NIP-44
// 3. Wrap in a "seal" (kind 13)
// 4. Wrap again in "gift wrap" (kind 1059) with a random key
// 5. Publish gift wrap to recipient's inbox relays

// This hides:
// - Who is talking to whom (pubkeys not visible)
// - When messages were sent (timestamps randomized)
// - Message content (double encrypted)
```

For full NIP-17 implementation, see the nostr-tools examples or use a library that implements it.
</nip17_overview>

<error_handling>
## Error Handling

```typescript
function safeDecrypt(ciphertext: string, key: Uint8Array): string | null {
  try {
    return nip44.decrypt(ciphertext, key)
  } catch (err) {
    if (err instanceof Error) {
      if (err.message.includes('invalid MAC')) {
        console.error('Message was tampered with or wrong key')
      } else if (err.message.includes('invalid base64')) {
        console.error('Malformed ciphertext')
      } else if (err.message.includes('unknown version')) {
        console.error('Unsupported NIP-44 version')
      }
    }
    return null
  }
}
```
</error_handling>

<security_considerations>
## Security Considerations

**What NIP-44 protects:**
- Content confidentiality (only intended recipient can read)
- Content integrity (tampering is detected)

**What NIP-44 does NOT protect:**
- Metadata (pubkeys and timestamps are visible)
- Forward secrecy (old messages decryptable if key compromised)
- Deniability (signatures prove authorship)
- Anonymity (your pubkey is on the event)

**Mitigations:**
- Use NIP-17 gift wrapping for metadata privacy
- Rotate keys periodically for limited forward secrecy
- Use ephemeral keys for sensitive one-time communications
- Consider NIP-46 remote signing to protect keys

**Storage:**
- Never log decrypted content
- Clear conversation keys when session ends
- Store encrypted content, decrypt on demand
</security_considerations>

<migration_from_nip04>
## Migrating from NIP-04

```typescript
// OLD (NIP-04) - DO NOT USE
import * as nip04 from 'nostr-tools/nip04'
const encrypted = await nip04.encrypt(sk, recipientPk, message)

// NEW (NIP-44)
import * as nip44 from 'nostr-tools/nip44'
const conversationKey = nip44.getConversationKey(sk, recipientPk)
const encrypted = nip44.encrypt(message, conversationKey)
```

Key differences:
- NIP-44 uses conversation key (cache it!)
- NIP-44 is synchronous (no await needed)
- NIP-44 has different ciphertext format
- Events should use different kinds
</migration_from_nip04>
