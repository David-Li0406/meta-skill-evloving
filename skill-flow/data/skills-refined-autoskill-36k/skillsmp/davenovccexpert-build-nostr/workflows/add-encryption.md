# Workflow: Add Encrypted Communication

<required_reading>
**Read these reference files NOW:**
1. references/encryption-nip44.md
2. references/key-management.md
3. references/nips-overview.md
</required_reading>

<process>
## Step 1: Understand Encryption Options

| NIP | Status | Use Case |
|-----|--------|----------|
| NIP-04 | **DEPRECATED** | Do NOT use - no authentication, leaks metadata |
| NIP-44 | Current | Encrypted payloads - use this |
| NIP-17 | Recommended | Full DM privacy with gift wrapping |

**For app data exchange:** Use NIP-44 for payload encryption.

## Step 2: Install and Import NIP-44

```typescript
import * as nip44 from 'nostr-tools/nip44'
import { generateSecretKey, getPublicKey } from 'nostr-tools/pure'
```

## Step 3: Encrypt Content

```typescript
// Your secret key and recipient's public key
const senderSk = generateSecretKey()
const recipientPk = '...' // 32-byte hex pubkey

// Create conversation key (cached per recipient)
const conversationKey = nip44.getConversationKey(senderSk, recipientPk)

// Encrypt message
const plaintext = JSON.stringify({ secret: 'data' })
const ciphertext = nip44.encrypt(plaintext, conversationKey)

// ciphertext is base64-encoded, ready for event content
```

## Step 4: Decrypt Content

```typescript
// Recipient uses their secret key and sender's public key
const recipientSk = generateSecretKey()
const senderPk = getPublicKey(senderSk)

// Create same conversation key (symmetric!)
const conversationKey = nip44.getConversationKey(recipientSk, senderPk)

// Decrypt
const decrypted = nip44.decrypt(ciphertext, conversationKey)
const data = JSON.parse(decrypted)
```

## Step 5: Create Encrypted Event Helper

```typescript
interface EncryptedEventOptions {
  kind: number
  recipientPubkey: string
  data: unknown
  tags?: string[][]
}

function createEncryptedEvent(
  options: EncryptedEventOptions,
  sk: Uint8Array
): Event {
  const conversationKey = nip44.getConversationKey(sk, options.recipientPubkey)
  const plaintext = JSON.stringify(options.data)
  const encrypted = nip44.encrypt(plaintext, conversationKey)

  const tags: string[][] = [
    ['p', options.recipientPubkey],  // Mark recipient
    ...(options.tags ?? [])
  ]

  return finalizeEvent({
    kind: options.kind,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: encrypted
  }, sk)
}
```

## Step 6: Create Decryption Helper

```typescript
function decryptEvent<T>(event: Event, sk: Uint8Array): T {
  // Find sender (the event author)
  const senderPk = event.pubkey

  const conversationKey = nip44.getConversationKey(sk, senderPk)
  const decrypted = nip44.decrypt(event.content, conversationKey)

  return JSON.parse(decrypted) as T
}
```

## Step 7: Implement Encrypted Pub/Sub

```typescript
class EncryptedChannel {
  private conversationKeys = new Map<string, Uint8Array>()

  constructor(
    private pool: SimplePool,
    private relays: string[],
    private sk: Uint8Array,
    private channelKind = 25044  // Ephemeral encrypted
  ) {}

  private pk = getPublicKey(this.sk)

  private getConversationKey(peerPk: string): Uint8Array {
    if (!this.conversationKeys.has(peerPk)) {
      this.conversationKeys.set(peerPk, nip44.getConversationKey(this.sk, peerPk))
    }
    return this.conversationKeys.get(peerPk)!
  }

  async send(recipientPk: string, data: unknown): Promise<string> {
    const key = this.getConversationKey(recipientPk)
    const encrypted = nip44.encrypt(JSON.stringify(data), key)

    const event = finalizeEvent({
      kind: this.channelKind,
      created_at: Math.floor(Date.now() / 1000),
      tags: [['p', recipientPk]],
      content: encrypted
    }, this.sk)

    await Promise.any(this.pool.publish(this.relays, event))
    return event.id
  }

  subscribe(
    peerPk: string,
    onMessage: (data: unknown, event: Event) => void
  ) {
    const key = this.getConversationKey(peerPk)

    return this.pool.subscribeMany(
      this.relays,
      [{
        kinds: [this.channelKind],
        authors: [peerPk],
        '#p': [this.pk],
        since: Math.floor(Date.now() / 1000)
      }],
      {
        onevent(event) {
          try {
            const decrypted = nip44.decrypt(event.content, key)
            onMessage(JSON.parse(decrypted), event)
          } catch (err) {
            console.error('Decryption failed:', err)
          }
        }
      }
    )
  }
}
```

## Step 8: Key Exchange for Groups

For multi-party encryption, use a shared secret:

```typescript
// Leader creates shared secret
const sharedSecret = generateSecretKey()

// Encrypt shared secret for each member
function inviteMember(memberPk: string, sk: Uint8Array): Event {
  const conversationKey = nip44.getConversationKey(sk, memberPk)
  const encrypted = nip44.encrypt(
    Buffer.from(sharedSecret).toString('hex'),
    conversationKey
  )

  return finalizeEvent({
    kind: 24,  // Encrypted channel invitation
    created_at: Math.floor(Date.now() / 1000),
    tags: [['p', memberPk]],
    content: encrypted
  }, sk)
}

// Group messages use shared secret directly
function encryptForGroup(data: unknown): string {
  // Use shared secret as conversation key
  return nip44.encrypt(JSON.stringify(data), sharedSecret)
}
```

## Step 9: Verify Encryption

```typescript
async function testEncryption() {
  const alice = generateSecretKey()
  const bob = generateSecretKey()
  const alicePk = getPublicKey(alice)
  const bobPk = getPublicKey(bob)

  const original = { message: 'secret', value: 42 }

  // Alice encrypts for Bob
  const aliceKey = nip44.getConversationKey(alice, bobPk)
  const encrypted = nip44.encrypt(JSON.stringify(original), aliceKey)

  // Bob decrypts
  const bobKey = nip44.getConversationKey(bob, alicePk)
  const decrypted = JSON.parse(nip44.decrypt(encrypted, bobKey))

  console.log('Match:', JSON.stringify(original) === JSON.stringify(decrypted))
}
```
</process>

<anti_patterns>
Avoid:
- Using NIP-04 (deprecated, insecure, leaks metadata)
- Storing conversation keys without considering memory
- Not handling decryption failures gracefully
- Assuming encryption hides metadata (pubkeys and timestamps visible)
- Reusing nonces (NIP-44 generates fresh ones automatically)
- Large encrypted payloads (encryption has overhead)
</anti_patterns>

<success_criteria>
A properly encrypted implementation:
- Uses NIP-44 (not NIP-04)
- Caches conversation keys for performance
- Handles decryption errors gracefully
- Marks recipients with p-tags
- Tests encryption/decryption round-trip
- Documents that metadata is still visible
- For full privacy, considers NIP-17 gift wrapping
</success_criteria>
