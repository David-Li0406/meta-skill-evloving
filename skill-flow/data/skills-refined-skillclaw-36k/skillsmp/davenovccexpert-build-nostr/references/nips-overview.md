<overview>
NIPs (Nostr Implementation Possibilities) are protocol standards that document what can be implemented by Nostr clients and relays. NIP-01 is the core protocol; all others are optional extensions. NIPs enable interoperability across the ecosystem.
</overview>

<core_nips>
## Essential NIPs

| NIP | Name | Status | Description |
|-----|------|--------|-------------|
| 01 | Basic Protocol | Required | Core event structure, relay communication |
| 02 | Follow List | Recommended | Contact list (kind 3) |
| 10 | Conventions for Clients | Recommended | Reply threading, mentions |
| 11 | Relay Info | Recommended | Relay metadata endpoint |
| 19 | Bech32 Entities | Recommended | npub, nsec, note, nprofile, etc. |
</core_nips>

<messaging_nips>
## Messaging & Encryption

| NIP | Name | Status | Notes |
|-----|------|--------|-------|
| 04 | Encrypted DMs | **DEPRECATED** | Insecure, use NIP-17 |
| 17 | Private DMs | Active | Full privacy with gift wrapping |
| 44 | Encrypted Payloads | Active | Modern encryption standard |
| 59 | Gift Wrap | Active | Hides metadata |
</messaging_nips>

<identity_nips>
## Identity & Authentication

| NIP | Name | Description |
|-----|------|-------------|
| 05 | DNS Verification | user@domain.com verification |
| 42 | Relay Auth | Client authentication to relays |
| 46 | Remote Signing | Bunker protocol for key management |
</identity_nips>

<content_nips>
## Content Types

| NIP | Kind | Name |
|-----|------|------|
| 01 | 1 | Short Text Note |
| 23 | 30023 | Long-form Content |
| 25 | 7 | Reactions |
| 36 | 1984 | Reports |
| 57 | 9735 | Zaps (Lightning) |
| 65 | 10002 | Relay List Metadata |
</content_nips>

<application_nips>
## Application Integration

| NIP | Name | Use Case |
|-----|------|----------|
| 78 | App Data | Arbitrary application data |
| 89 | App Handlers | App registration |
| 90 | Data Vending | Paid data services |
| 96 | File Storage | File hosting |
| 98 | HTTP Auth | NIP-98 auth for HTTP |
</application_nips>

<event_handling_nips>
## Event Handling

| NIP | Name | Description |
|-----|------|-------------|
| 09 | Event Deletion | Request to delete events |
| 16 | Event Treatment | Ephemeral, replaceable, addressable |
| 33 | Addressable Events | Parameterized replaceable events |
| 40 | Expiration | Event expiration timestamp |
</event_handling_nips>

<implementation_priority>
## Implementation Priority

**Must Have:**
- NIP-01 (Core protocol)
- NIP-19 (Bech32 encoding)

**Should Have:**
- NIP-02 (Follow list)
- NIP-10 (Reply threading)
- NIP-11 (Relay info)
- NIP-44 (Encryption)

**Nice to Have:**
- NIP-05 (DNS verification)
- NIP-42 (Relay auth)
- NIP-57 (Zaps)
- NIP-65 (Relay list)
</implementation_priority>

<nip_status>
## NIP Status Guide

| Status | Meaning |
|--------|---------|
| Final | Stable, widely implemented |
| Draft | Under development, may change |
| Deprecated | Don't use for new implementations |
| Obsolete | Replaced by another NIP |
</nip_status>

<checking_nips>
## Finding NIP Information

**Official sources:**
- https://github.com/nostr-protocol/nips
- https://nips.nostr.com/
- https://nostr-nips.com/

**Relay NIP support:**
```typescript
async function getRelayNips(relay: string): Promise<number[]> {
  const info = await getRelayInfo(relay)
  return info?.supported_nips ?? []
}
```
</checking_nips>

<common_nip_patterns>
## Common NIP Patterns in Code

**NIP-01: Basic event:**
```typescript
const event = finalizeEvent({
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [],
  content: 'Hello'
}, sk)
```

**NIP-10: Reply threading:**
```typescript
// Reply to an event
const tags = [
  ['e', originalEventId, '', 'reply'],
  ['p', originalAuthor]
]
```

**NIP-19: Encode/decode:**
```typescript
const npub = nip19.npubEncode(pk)
const { type, data } = nip19.decode(npub)
```

**NIP-44: Encryption:**
```typescript
const key = nip44.getConversationKey(sk, recipientPk)
const encrypted = nip44.encrypt(message, key)
```

**NIP-65: User relays:**
```typescript
const relayList = await pool.get(relays, {
  kinds: [10002],
  authors: [userPk]
})
const userRelays = relayList?.tags
  .filter(t => t[0] === 'r')
  .map(t => t[1])
```
</common_nip_patterns>

<nip_resources>
## Resources

- **GitHub:** https://github.com/nostr-protocol/nips
- **Nostr NIPs site:** https://nips.nostr.com/
- **Nostr Compass:** https://nostrcompass.org/ (weekly updates)
- **nostr-tools:** Implements most NIPs

For any NIP, check the official repo for the current specification.
</nip_resources>
