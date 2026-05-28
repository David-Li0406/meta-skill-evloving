---
name: gdl90-adsb
description: GDL 90 protocol implementation for ADS-B receivers. Use when decoding traffic data from Stratux, ForeFlight Sentry, or other GDL 90 compatible devices. Includes message decoders, traffic simulators, and receiver client implementations.
---

# GDL 90 ADS-B

## Overview

Parse and encode GDL 90 protocol messages for ADS-B receiver integration.

## Message Types

| ID | Name | Description |
|----|------|-------------|
| 0x00 | Heartbeat | GPS status, UTC time |
| 0x07 | Uplink Data | FIS-B weather, TFRs |
| 0x0A | Ownship Report | Own aircraft position |
| 0x0B | Ownship Geo Alt | Geometric altitude |
| 0x14 | Traffic Report | Other aircraft |
| 0xCC | Stratux Status | Stratux-specific |

## Quick Start

### Decode GDL 90 Stream

```python
from gdl90_decoder import GDL90Decoder

decoder = GDL90Decoder()

# From UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(('', 4000))
    while True:
        data, addr = sock.recvfrom(4096)
        messages = decoder.decode(data)
        for msg in messages:
            if msg['type'] == 'traffic':
                print(f"Traffic: {msg['callsign']} at {msg['altitude']} ft")
```

### Connect to Stratux

```python
from stratux_client import StratuxClient

client = StratuxClient('192.168.10.1')
client.connect()

for traffic in client.get_traffic():
    print(f"{traffic['icao']}: {traffic['lat']}, {traffic['lon']}")
```

### Generate Test Traffic

```python
from traffic_simulator import TrafficSimulator

sim = TrafficSimulator()
sim.add_aircraft('N12345', lat=33.94, lon=-118.40, alt=5000, hdg=270)
sim.start(port=4000)
```

## References

- GDL 90 message specifications: `references/message_types.md`
- FIS-B weather products: `references/fisb_products.md`
- Stratux extensions: `references/stratux_extensions.md`

## Scripts

| Script | Description |
|--------|-------------|
| `gdl90_decoder.py` | Decode GDL 90 messages |
| `gdl90_encoder.py` | Encode GDL 90 messages |
| `traffic_simulator.py` | Generate test traffic |
| `stratux_client.py` | Connect to Stratux receiver |
