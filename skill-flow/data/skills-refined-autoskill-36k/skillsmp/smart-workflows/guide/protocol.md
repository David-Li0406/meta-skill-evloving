# MCP-B Protocol

## Overview

The MCP-B Protocol uses a 4-layer encoding for agent-to-agent communication.

## Layers

| Layer | Purpose | Example |
|-------|---------|---------|
| 1 | HEX/DECIMAL Routing | `7C1 5510` |
| 2 | BINARY State Vectors | `1011101010111111` |
| 3 | DOT-SEPARATED Tokens | `• payload • command` |
| 4 | INQC Commands | `I`/`N`/`Q`/`C` |

## INQC Commands

- **I** (INIT): Initialize connection
- **N** (NODE): Node registration/discovery
- **Q** (QUERY): Request data/state
- **C** (CONNECT): Establish persistent link

## Binary State Flags (16-bit)

| Bit | Flag | Description |
|-----|------|-------------|
| 0 | CONNECTED | Connection active |
| 1 | AUTHENTICATED | Auth verified |
| 2 | ENCRYPTED | Encryption enabled |
| 3 | COMPRESSED | Compression enabled |
| 4 | STREAMING | Streaming mode |
| 5 | BIDIRECTIONAL | Two-way comm |
| 6 | PERSISTENT | Persistent connection |
| 7 | PRIORITY | High priority |
| 8-15 | RESERVED | Custom flags |

## Usage

```python
from mcp_b import MCBAgent, MCBProtocol, encode_mcb, decode_mcb

# Create agents
agent1 = MCBAgent(agent_id="7C1", name="Claude")
agent2 = MCBAgent(agent_id="5510", name="HACKA")

# Initialize protocol
protocol = MCBProtocol(agent2)

# Send messages
init_msg = protocol.init_connection(agent1)
query_msg = protocol.query("7C1", {"status": 1})
```
