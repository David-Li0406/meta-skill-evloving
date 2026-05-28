# LXMF Code Examples

Complete code examples for common LXMF operations.

## Table of Contents
- [Basic Message Sending](#basic-message-sending)
- [Receiving Messages](#receiving-messages)
- [Using Propagation Nodes](#using-propagation-nodes)
- [Running a Propagation Node](#running-a-propagation-node)
- [Stamps (Proof-of-Work)](#stamps-proof-of-work)
- [Tickets (Authentication)](#tickets-authentication)
- [Physical Layer Information](#physical-layer-information)
- [Testing and Debugging](#testing-and-debugging)

---

## Basic Message Sending

```python
import RNS
import LXMF
import time

# Initialize Reticulum
reticulum = RNS.Reticulum()

# Create router
router = LXMF.LXMRouter(storagepath="~/.myapp/lxmf")

# Create local identity and delivery destination
identity = RNS.Identity()
local_destination = router.register_delivery_identity(identity)

# To send a message, you need recipient's identity (from announcement or known)
recipient_hash = bytes.fromhex("c5e3842981456a23fc3332edc6056474")
recipient_identity = RNS.Identity.recall(recipient_hash)

if recipient_identity:
    # Create destination for recipient
    recipient_destination = RNS.Destination(
        recipient_identity,
        RNS.Destination.OUT,
        RNS.Destination.SINGLE,
        "lxmf",
        "delivery"
    )

    # Create and send message
    message = LXMF.LXMessage(
        recipient_destination,
        local_destination,
        "Hello, world!",
        title="Greeting",
        desired_method=LXMF.LXMessage.DIRECT
    )

    # Optional: callbacks
    message.register_delivery_callback(lambda msg: print("Delivered!"))
    message.register_failed_callback(lambda msg: print("Failed!"))

    router.handle_outbound(message)
```

---

## Receiving Messages

```python
import RNS
import LXMF
import time

def message_received(message):
    """Called when a message is received."""
    print(f"From: {RNS.prettyhexrep(message.source_hash)}")
    print(f"Title: {message.title}")
    print(f"Content: {message.content}")

    # Access fields
    fields = message.get_fields()
    if LXMF.FIELD_FILE_ATTACHMENTS in fields:
        for filename, data in fields[LXMF.FIELD_FILE_ATTACHMENTS]:
            print(f"Attachment: {filename} ({len(data)} bytes)")

# Setup
reticulum = RNS.Reticulum()
router = LXMF.LXMRouter(storagepath="~/.myapp/lxmf")
identity = RNS.Identity.from_file("~/.myapp/identity")  # Or create new
delivery_destination = router.register_delivery_identity(identity)

# Register callback
router.register_delivery_callback(message_received)

# Announce presence
delivery_destination.announce()

# Keep running
while True:
    time.sleep(1)
```

---

## Using Propagation Nodes

For sending messages to offline recipients:

```python
import LXMF

# Set outbound propagation node (for sending to offline recipients)
propagation_node_hash = bytes.fromhex("e75d9b6a69f82b48b6077cf2242d7499")
router.set_outbound_propagation_node(propagation_node_hash)

# Create propagated message
message = LXMF.LXMessage(
    destination,
    source,
    "This message will be stored on the propagation node",
    desired_method=LXMF.LXMessage.PROPAGATED
)

# Optional: fall back to propagation if direct fails
message.try_propagation_on_fail = True

router.handle_outbound(message)
```

---

## Running a Propagation Node

```python
import LXMF

# Create router with propagation settings
router = LXMF.LXMRouter(
    storagepath="~/.myapp/lxmf",
    propagation_limit=256,    # KB per transfer
    delivery_limit=1000       # Max messages per sync
)

# Enable propagation node mode
router.enable_propagation()

# Set message storage limit
router.set_information_storage_limit(kilobytes=50000)  # 50 MB

# The router will now accept and store messages for other destinations
```

---

## Stamps (Proof-of-Work)

LXMF supports proof-of-work stamps to prevent spam.

### Receiver: Require Stamps

```python
# Enable stamp enforcement
router = LXMF.LXMRouter(storagepath="...", enforce_stamps=True)

# Set stamp cost for a delivery identity (1-254, 0 disables)
router.set_inbound_stamp_cost(destination_hash, stamp_cost=8)
```

### Sender: Generate Stamps

```python
# stamp_cost parameter triggers automatic stamp generation
message = LXMF.LXMessage(
    dest, source, "content",
    desired_method=LXMF.LXMessage.DIRECT,
    stamp_cost=8
)
```

### External Stamp Generator (Android/Embedded)

For platforms where Python multiprocessing is problematic:

```python
import LXMF.LXStamper as LXStamper

def my_generator(workblock, stamp_cost):
    """Custom stamp generation (e.g., native code).

    Args:
        workblock: bytes - the work block to stamp
        stamp_cost: int - required stamp difficulty

    Returns:
        tuple: (stamp_bytes, rounds_computed)
    """
    # Your custom implementation here
    return (stamp_bytes, rounds)

LXStamper.set_external_generator(my_generator)
```

---

## Tickets (Authentication)

Tickets allow pre-authorized stamp bypass for trusted senders:

```python
# Include ticket for authentication
message = LXMF.LXMessage(
    dest, source, "content",
    desired_method=LXMF.LXMessage.DIRECT,
    include_ticket=True
)

# Ticket format in FIELD_TICKET: [expiry_timestamp, ticket_bytes]
# Tickets auto-renew when <14 days remain
```

---

## Physical Layer Information

Messages received carry physical layer stats when available:

```python
def message_received(message):
    # Signal info (available for all message types when transport provides it)
    rssi = message.rssi    # Received Signal Strength (dBm), or None
    snr = message.snr      # Signal to Noise Ratio (dB), or None
    q = message.q          # Link quality metric, or None

    # For opportunistic messages ONLY - use hasattr() to check
    if hasattr(message, 'receiving_interface'):
        interface = message.receiving_interface  # RNS interface object
    if hasattr(message, 'receiving_hops'):
        hops = message.receiving_hops            # Hop count from source

    # Delivery method used
    if message.method == LXMF.LXMessage.DIRECT:
        print("Received via direct link")
    elif message.method == LXMF.LXMessage.PROPAGATED:
        print("Received via propagation node")
```

**Note**: `receiving_interface` and `receiving_hops` are only set for opportunistic messages. They are not initialized in the message constructor, so always check with `hasattr()` or use `getattr(message, 'receiving_interface', None)`.

---

## Testing and Debugging

### Enable Verbose Logging

```python
import RNS
RNS.loglevel = RNS.LOG_VERBOSE  # Or LOG_DEBUG, LOG_EXTREME
```

### Pretty Print Hashes

```python
hash_bytes = bytes.fromhex("c5e3842981456a23fc3332edc6056474")
print(RNS.prettyhexrep(hash_bytes))
# Output: <c5e3842981456a23fc3332edc6056474>
```

### Check Message State

```python
print(f"State: {message.state}")
print(f"Method: {message.method}")
print(f"Representation: {message.representation}")
print(f"Hash: {RNS.prettyhexrep(message.hash)}")
```

### Announce App Data Format

LXMF uses msgpack-encoded lists for announcement app_data:

**Delivery Identity Announce (v0.5.0+)**:
```python
[
    display_name,   # bytes: UTF-8 encoded display name (or None)
    stamp_cost      # int: Required stamp cost for sending (or None)
]
```

**Propagation Node Announce**:
```python
[
    False,                      # 0: Legacy flag
    int(time.time()),           # 1: Node timebase (Unix timestamp)
    True,                       # 2: Propagation node active
    per_transfer_limit,         # 3: KB per transfer limit
    per_sync_limit,             # 4: KB per sync limit
    [stamp_cost, flexibility, peering_cost],  # 5: Stamp/peering config
    {                           # 6: Metadata dict (optional keys)
        PN_META_NAME: b"name",
        PN_META_VERSION: ...,
    }
]
```
