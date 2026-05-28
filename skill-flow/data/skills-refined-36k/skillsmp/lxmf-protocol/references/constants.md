# LXMF Constants Reference

Complete reference for all LXMF constants and configuration values.

## Table of Contents
- [Field Constants](#field-constants)
- [Renderer Types](#renderer-types)
- [Delivery Methods](#delivery-methods)
- [Message States](#message-states)
- [Message Representation](#message-representation)
- [Ticket Constants](#ticket-constants)
- [Propagation States](#propagation-states)
- [Propagation Node Metadata](#propagation-node-metadata)
- [LXMRouter Configuration](#lxmrouter-configuration)

---

## Field Constants

Integer keys for the `fields` dictionary in LXMessage payload.

```python
import LXMF

# Core interoperability fields
LXMF.FIELD_EMBEDDED_LXMS      = 0x01  # Embedded LXMF messages
LXMF.FIELD_TELEMETRY          = 0x02  # Telemetry data
LXMF.FIELD_TELEMETRY_STREAM   = 0x03  # Streaming telemetry
LXMF.FIELD_ICON_APPEARANCE    = 0x04  # Icon/appearance data
LXMF.FIELD_FILE_ATTACHMENTS   = 0x05  # File attachments: [[filename, bytes], ...]
LXMF.FIELD_IMAGE              = 0x06  # Image data
LXMF.FIELD_AUDIO              = 0x07  # Audio data
LXMF.FIELD_THREAD             = 0x08  # Thread/conversation ID
LXMF.FIELD_COMMANDS           = 0x09  # Command structures
LXMF.FIELD_RESULTS            = 0x0A  # Command results
LXMF.FIELD_GROUP              = 0x0B  # Group information
LXMF.FIELD_TICKET             = 0x0C  # Authentication ticket
LXMF.FIELD_EVENT              = 0x0D  # Event data
LXMF.FIELD_RNR_REFS           = 0x0E  # Resource/reference information
LXMF.FIELD_RENDERER           = 0x0F  # Message renderer specification

# Custom data fields
LXMF.FIELD_CUSTOM_TYPE        = 0xFB  # Custom data type identifier
LXMF.FIELD_CUSTOM_DATA        = 0xFC  # Custom data payload
LXMF.FIELD_CUSTOM_META        = 0xFD  # Custom metadata

# Debug fields
LXMF.FIELD_NON_SPECIFIC       = 0xFE  # Non-specific/generic data
LXMF.FIELD_DEBUG              = 0xFF  # Debug/development field
```

---

## Renderer Types

Values for `FIELD_RENDERER` to specify message formatting.

```python
import LXMF

LXMF.RENDERER_PLAIN           = 0x00  # Plain text
LXMF.RENDERER_MICRON          = 0x01  # Micron format
LXMF.RENDERER_MARKDOWN        = 0x02  # Markdown
LXMF.RENDERER_BBCODE          = 0x03  # BBCode
```

---

## Delivery Methods

```python
from LXMF import LXMessage

LXMessage.OPPORTUNISTIC = 0x01  # Single packet, no link (max ~295 bytes)
LXMessage.DIRECT        = 0x02  # Establish link first, then transfer
LXMessage.PROPAGATED    = 0x03  # Via propagation node (for offline recipients)
LXMessage.PAPER         = 0x05  # QR code/URI encoding for offline transmission
```

| Method | Use Case | Max Size | Requires |
|--------|----------|----------|----------|
| `DIRECT` | Default for most uses | Unlimited (via Resource) | Path to destination |
| `OPPORTUNISTIC` | Quick small messages | ~295 bytes | Announced destination |
| `PROPAGATED` | Offline recipients | Large (node dependent) | Propagation node set |
| `PAPER` | Offline/QR transmission | ~2.9 KB | Nothing (generates URI) |

---

## Message States

```python
from LXMF import LXMessage

# Outbound states
LXMessage.GENERATING    = 0x00  # Stamp/content being generated
LXMessage.OUTBOUND      = 0x01  # Queued for delivery
LXMessage.SENDING       = 0x02  # Currently being transmitted
LXMessage.SENT          = 0x04  # Transmitted (opportunistic) or propagated
LXMessage.DELIVERED     = 0x08  # Confirmed delivered (direct)
LXMessage.REJECTED      = 0xFD  # Delivery rejected (by propagation node)
LXMessage.CANCELLED     = 0xFE  # Delivery cancelled by user
LXMessage.FAILED        = 0xFF  # Delivery failed after retries

# State flow: GENERATING -> OUTBOUND -> SENDING -> SENT/DELIVERED/REJECTED/CANCELLED/FAILED
```

---

## Message Representation

```python
from LXMF import LXMessage

LXMessage.UNKNOWN   = 0x00  # Not yet determined
LXMessage.PACKET    = 0x01  # Fits in single packet
LXMessage.RESOURCE  = 0x02  # Requires multi-packet Resource transfer
```

---

## Ticket Constants

Tickets allow pre-authorized stamp bypass for trusted senders.

```python
from LXMF import LXMessage

LXMessage.TICKET_EXPIRY   = 21*24*60*60  # 21 days validity (1,814,400 seconds)
LXMessage.TICKET_GRACE    = 5*24*60*60   # 5 days grace for time drift (432,000 seconds)
LXMessage.TICKET_RENEW    = 14*24*60*60  # Auto-renew when <14 days left (1,209,600 seconds)
LXMessage.TICKET_INTERVAL = 1*24*60*60   # 1 day between reissues (86,400 seconds)
LXMessage.COST_TICKET     = 0x100        # Special stamp value indicating ticket auth
```

---

## Propagation States

States for LXMRouter propagation sync operations.

```python
from LXMF import LXMRouter

# Normal flow states
LXMRouter.PR_IDLE               = 0x00  # Not syncing
LXMRouter.PR_PATH_REQUESTED     = 0x01  # Requesting path to peer
LXMRouter.PR_LINK_ESTABLISHING  = 0x02  # Establishing link to peer
LXMRouter.PR_LINK_ESTABLISHED   = 0x03  # Link established
LXMRouter.PR_REQUEST_SENT       = 0x04  # Sync request sent
LXMRouter.PR_RECEIVING          = 0x05  # Receiving messages
LXMRouter.PR_RESPONSE_RECEIVED  = 0x06  # Response received
LXMRouter.PR_COMPLETE           = 0x07  # Sync complete

# Failure states
LXMRouter.PR_NO_PATH            = 0xf0  # No path available to peer
LXMRouter.PR_LINK_FAILED        = 0xf1  # Link establishment failed
LXMRouter.PR_TRANSFER_FAILED    = 0xf2  # Transfer failed during sync
LXMRouter.PR_NO_IDENTITY_RCVD   = 0xf3  # Identity not received from peer
LXMRouter.PR_NO_ACCESS          = 0xf4  # Access denied by peer
LXMRouter.PR_FAILED             = 0xfe  # General failure

# Filter constants
LXMRouter.PR_ALL_MESSAGES       = 0x00  # Request all messages in sync
```

---

## Propagation Node Metadata

Keys for propagation node announce metadata dictionary.

```python
import LXMF

LXMF.PN_META_VERSION        = 0x00  # Node version info
LXMF.PN_META_NAME           = 0x01  # Node display name (bytes)
LXMF.PN_META_SYNC_STRATUM   = 0x02  # Sync stratum level
LXMF.PN_META_SYNC_THROTTLE  = 0x03  # Sync throttle configuration
LXMF.PN_META_AUTH_BAND      = 0x04  # Authentication band
LXMF.PN_META_UTIL_PRESSURE  = 0x05  # Utility pressure metric
LXMF.PN_META_CUSTOM         = 0xFF  # Custom metadata
```

---

## LXMRouter Configuration

Default values (set via constructor parameters):

```python
from LXMF import LXMRouter

# Delivery settings
LXMRouter.MAX_DELIVERY_ATTEMPTS = 5       # Retries before marking failed
LXMRouter.PROCESSING_INTERVAL   = 4       # Seconds between queue processing
LXMRouter.DELIVERY_RETRY_WAIT   = 10      # Seconds between retries
LXMRouter.PATH_REQUEST_WAIT     = 7       # Seconds to wait for path response
LXMRouter.MAX_PATHLESS_TRIES    = 1       # Attempts without known path

# Link settings
LXMRouter.LINK_MAX_INACTIVITY   = 10*60   # 10 minutes link timeout
LXMRouter.P_LINK_MAX_INACTIVITY = 3*60    # 3 minutes for propagation links

# Message retention
LXMRouter.MESSAGE_EXPIRY        = 30*24*60*60  # 30 days message retention
LXMRouter.STAMP_COST_EXPIRY     = 45*24*60*60  # 45 days stamp cost cache

# Propagation limits (constructor parameters)
LXMRouter.PROPAGATION_LIMIT     = 256     # KB per sync transfer
LXMRouter.DELIVERY_LIMIT        = 1000    # Max messages per sync
```

### Setting Limits

```python
# Set limits via constructor
router = LXMF.LXMRouter(
    storagepath="~/.myapp/lxmf",
    propagation_limit=256,      # KB per transfer
    delivery_limit=1000,        # Max messages per sync
    sync_limit=8                # Concurrent syncs
)

# Set message storage limit via method
router.set_information_storage_limit(kilobytes=2000)

# Get current storage size
current_size = router.message_storage_size()
```
