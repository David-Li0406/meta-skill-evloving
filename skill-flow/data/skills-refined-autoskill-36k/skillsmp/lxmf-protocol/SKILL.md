---
name: lxmf-protocol
description: Deep knowledge of LXMF (Lightweight Extensible Message Format) protocol and Reticulum integration. Use when working with LXMF messaging, LXMessage creation, LXMRouter configuration, propagation nodes, delivery methods (OPPORTUNISTIC, DIRECT, PROPAGATED), stamps, tickets, or RNS destinations and links.
---

# LXMF Protocol Development

This skill provides comprehensive knowledge for developing with the LXMF protocol.

## Primary Reference

Comprehensive documentation is in the `references/` directory:
- **Protocol guide**: Read `references/protocol-guide.md`
- **Constants reference**: Read `references/constants.md`
- **Code examples**: Read `references/examples.md`

## Quick Concepts

### Hash Types (Critical Distinction)

| Hash Type | Derivation | Usage |
|-----------|------------|-------|
| **Identity Hash** | `truncated_hash(public_key)` | Identifies cryptographic identity |
| **Destination Hash** | `truncated_hash(name_hash + identity_hash)` | Addresses specific endpoint (LXMF address) |

```python
# From identity hash to LXMF destination
identity = RNS.Identity.recall(identity_hash, from_identity_hash=True)
lxmf_hash = RNS.Destination.hash_from_name_and_identity("lxmf.delivery", identity)

# From LXMF address (destination hash), recall identity
identity = RNS.Identity.recall(destination_hash)  # from_identity_hash=False
```

### Delivery Methods

| Method | Value | Use Case | Max Size |
|--------|-------|----------|----------|
| `DIRECT` | 0x02 | Default - establishes link | Unlimited |
| `OPPORTUNISTIC` | 0x01 | Quick small messages | ~295 bytes |
| `PROPAGATED` | 0x03 | Offline recipients | Node dependent |
| `PAPER` | 0x05 | QR/URI for offline | ~2.9 KB |

### Message States

```
GENERATING (0x00) -> OUTBOUND (0x01) -> SENDING (0x02) ->
SENT (0x04) / DELIVERED (0x08) / REJECTED (0xFD) / CANCELLED (0xFE) / FAILED (0xFF)
```

## Common Patterns

### Sending a Message

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
router.handle_outbound(message)
```

### Receiving Messages

```python
def on_message(message):
    print(f"From: {RNS.prettyhexrep(message.source_hash)}")
    print(f"Content: {message.content}")

router.register_delivery_callback(on_message)
delivery_dest.announce()
```

## Common Pitfalls

1. **Confusing identity hash with destination hash** - LXMF addresses are destination hashes
2. **Message too large for OPPORTUNISTIC** - Max ~295 bytes, use DIRECT for larger
3. **Not waiting for path discovery** - Use `RNS.Transport.request_path()` and wait
4. **Accessing opportunistic-only attributes** - Use `getattr(message, 'receiving_interface', None)`
5. **Setting router limits incorrectly** - Limits are constructor params, not assignable

## Key Source Files

| File | Purpose |
|------|---------|
| `LXMF/LXMessage.py` | Message class - states, methods, pack/unpack |
| `LXMF/LXMRouter.py` | Routing - delivery, propagation, callbacks |
| `LXMF/LXMPeer.py` | Peer sync - offer/request protocol |
| `LXMF/LXStamper.py` | Proof-of-work stamps |
| `LXMF/LXMF.py` | Constants - fields, renderers |

## Debugging

Enable verbose logging:
```python
import RNS
RNS.loglevel = RNS.LOG_VERBOSE  # Or LOG_DEBUG, LOG_EXTREME
```

Check message state:
```python
print(f"State: {message.state}, Method: {message.method}")
print(f"Hash: {RNS.prettyhexrep(message.hash)}")
```
