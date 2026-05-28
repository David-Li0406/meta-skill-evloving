---
name: lxmf-reticulum
description: LXMF (Lightweight Extensible Message Format) and Reticulum protocol development. Use when working with LXMF messaging, Reticulum networking, propagation nodes, LXMessage creation, LXMRouter configuration, or related Python applications. Triggers on questions about destination hashes, identity hashes, message delivery methods, propagation nodes, stamps, or LXMF field constants.
---

# LXMF & Reticulum Development

## Quick Reference

- **LXMF Repository**: https://github.com/markqvist/LXMF
- **Reticulum Repository**: https://github.com/markqvist/Reticulum
- **Reticulum Manual**: https://reticulum.network/manual/

```bash
pip install rns lxmf
```

---

## Critical Concepts: Hashes & Identities

**This is the most common source of confusion in LXMF/Reticulum development.**

| Hash Type | Length | Derivation | Usage |
|-----------|--------|------------|-------|
| **Identity Hash** | 16 bytes | `truncated_hash(public_key)` | Identifies a cryptographic identity across all destinations |
| **Destination Hash** | 16 bytes | `truncated_hash(name_hash + identity_hash)` | Addresses a specific endpoint (e.g., LXMF address) |

One identity can have **many** destination hashes (one per app/aspect combination).

### Converting Between Them

```python
import RNS

# From identity hash to destination hash
identity_hash = bytes.fromhex("2cc20b9429c522e232710372dd5b7c47")
identity = RNS.Identity.recall(identity_hash, from_identity_hash=True)
lxmf_hash = RNS.Destination.hash_from_name_and_identity("lxmf.delivery", identity)

# From destination hash (LXMF address), recall the identity
destination_hash = bytes.fromhex("c5e3842981456a23fc3332edc6056474")
identity = RNS.Identity.recall(destination_hash)  # from_identity_hash=False is default
```

### Message ID vs Transient ID

| ID Type | Derivation | Usage |
|---------|------------|-------|
| **message_id** | `SHA-256(destination + source + payload)` | Canonical identifier, computed locally (never transmitted) |
| **transient_id** | `SHA-256(encrypted_payload)` | Used for propagated messages where payload is encrypted |

---

## Message Structure

### Wire Format (112 bytes overhead)

```
[Destination: 16 bytes][Source: 16 bytes][Signature: 64 bytes][Payload: variable]
```

### Payload (msgpack list)

```python
[
    timestamp,   # float: seconds since Unix epoch
    title,       # bytes: message title (can be empty)
    content,     # bytes: message body (can be empty)
    fields       # dict: extensible fields (see references/constants.md)
]
```

---

## Delivery Methods

| Method | Value | Use Case | Max Size |
|--------|-------|----------|----------|
| `DIRECT` | 0x02 | Default - establishes link | Unlimited |
| `OPPORTUNISTIC` | 0x01 | Quick small messages | ~295 bytes |
| `PROPAGATED` | 0x03 | Offline recipients | Node dependent |
| `PAPER` | 0x05 | QR/URI for offline | ~2.9 KB |

**Note**: When `desired_method=None`, LXMF defaults to `DIRECT`. Always specify explicitly for clarity.

---

## Message States

| State | Value | Meaning |
|-------|-------|---------|
| `GENERATING` | 0x00 | Stamp/content being generated |
| `OUTBOUND` | 0x01 | Queued for delivery |
| `SENDING` | 0x02 | Currently transmitting |
| `SENT` | 0x04 | Transmitted (opportunistic/propagated) |
| `DELIVERED` | 0x08 | Confirmed delivered (direct only) |
| `REJECTED` | 0xFD | Rejected by propagation node |
| `CANCELLED` | 0xFE | Cancelled by user |
| `FAILED` | 0xFF | Failed after retries |

Flow: `GENERATING -> OUTBOUND -> SENDING -> SENT/DELIVERED/REJECTED/CANCELLED/FAILED`

---

## Quick Patterns

### Send a Message

```python
import RNS, LXMF

reticulum = RNS.Reticulum()
router = LXMF.LXMRouter(storagepath="~/.myapp/lxmf")
identity = RNS.Identity()
local_dest = router.register_delivery_identity(identity)

recipient_identity = RNS.Identity.recall(recipient_hash)
recipient_dest = RNS.Destination(
    recipient_identity, RNS.Destination.OUT,
    RNS.Destination.SINGLE, "lxmf", "delivery"
)

message = LXMF.LXMessage(
    recipient_dest, local_dest, "Hello!",
    desired_method=LXMF.LXMessage.DIRECT
)
message.register_delivery_callback(lambda m: print("Delivered"))
router.handle_outbound(message)
```

### Receive Messages

```python
def on_message(message):
    print(f"From: {RNS.prettyhexrep(message.source_hash)}")
    print(f"Content: {message.content}")

router.register_delivery_callback(on_message)
delivery_dest.announce()
```

### Use Propagation

```python
router.set_outbound_propagation_node(propagation_node_hash)
message = LXMF.LXMessage(dest, src, "content",
                          desired_method=LXMF.LXMessage.PROPAGATED)
# Or fall back to propagation if direct fails:
message.try_propagation_on_fail = True
```

See [references/examples.md](references/examples.md) for complete examples.

---

## Common Pitfalls

### 1. Default delivery method

When `desired_method=None`, LXMF defaults to `DIRECT`. This works but is implicit. Always specify the method explicitly:

```python
# Explicit is better
message = LXMF.LXMessage(dest, source, "content",
                          desired_method=LXMF.LXMessage.DIRECT)
```

### 2. GROUP destinations don't support OPPORTUNISTIC

GROUP destinations can't be announced. Use `PROPAGATED` method:

```python
message = LXMF.LXMessage(group_dest, source, "content",
                          desired_method=LXMF.LXMessage.PROPAGATED)
```

### 3. Confusing identity hash with destination hash

If you have an "LXMF address", that's a **destination hash**. Use `RNS.Identity.recall(dest_hash)` to get the identity. Only use `from_identity_hash=True` when you specifically have an identity hash.

### 4. Message too large for OPPORTUNISTIC

Max ~295 bytes for opportunistic. Use `DIRECT` for larger content:

```python
message = LXMF.LXMessage(dest, source, large_content,
                          desired_method=LXMF.LXMessage.DIRECT)
```

### 5. Not waiting for path discovery

Sending fails if path not known. Either request path first or enable fallback:

```python
RNS.Transport.request_path(destination_hash)
time.sleep(7)  # PATH_REQUEST_WAIT

# Or use fallback:
message.try_propagation_on_fail = True
```

### 6. Accessing opportunistic-only attributes

`receiving_interface` and `receiving_hops` only exist on opportunistic messages:

```python
# Safe access pattern
interface = getattr(message, 'receiving_interface', None)
hops = getattr(message, 'receiving_hops', None)
```

### 7. Setting router limits incorrectly

Limits are constructor parameters, not assignable properties:

```python
# WRONG: These are not assignable
# router.propagation_limit = 256

# CORRECT: Use constructor
router = LXMF.LXMRouter(storagepath="...", propagation_limit=256)

# For storage limit, use the setter method
router.set_information_storage_limit(kilobytes=2000)
```

---

## Stamps & Tickets

**Stamps**: Proof-of-work to prevent spam (cost 1-254).

```python
# Receiver requires stamps
router = LXMF.LXMRouter(storagepath="...", enforce_stamps=True)
router.set_inbound_stamp_cost(dest_hash, stamp_cost=8)

# Sender generates stamp
message = LXMF.LXMessage(dest, src, "content",
                          desired_method=LXMF.LXMessage.DIRECT,
                          stamp_cost=8)
```

**Tickets**: Pre-authorized stamp bypass for trusted senders.

```python
message = LXMF.LXMessage(dest, src, "content",
                          desired_method=LXMF.LXMessage.DIRECT,
                          include_ticket=True)
```

---

## Reference Files

- **[references/constants.md](references/constants.md)**: All FIELD_*, RENDERER_*, state constants, PR_* propagation states, PN_META_* constants, LXMRouter configuration
- **[references/examples.md](references/examples.md)**: Complete code examples for sending, receiving, propagation nodes, stamps, physical layer info, debugging

---

## Related Projects

- **Sideband**: Full-featured LXMF client (Android/Linux/macOS)
- **Nomad Network**: Terminal-based LXMF client with propagation node hosting
- **MeshChat**: Web-based LXMF client
- **lxmd**: Lightweight LXMF daemon (included with lxmf package)
