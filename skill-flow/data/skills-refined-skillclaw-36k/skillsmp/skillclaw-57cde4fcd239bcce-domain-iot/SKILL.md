---
name: domain-iot
description: Use this skill when building IoT applications that require considerations for network reliability, power management, and security.
---

# IoT Domain

> **Layer 3: Domain Constraints**

## Domain Constraints → Design Implications

| Domain Rule          | Design Constraint | Rust Implication               |
|----------------------|-------------------|--------------------------------|
| Unreliable network    | Offline-first      | Local buffering                |
| Power constraints      | Efficient code     | Sleep modes, minimal alloc     |
| Resource limits        | Small footprint     | no_std where needed            |
| Security               | Encrypted comms     | TLS, signed firmware           |
| Reliability            | Self-recovery       | Watchdog, error handling       |
| OTA updates            | Safe upgrades       | Rollback capability            |

---

## Critical Constraints

### Network Unreliability

```
RULE: Network can fail at any time
WHY: Wireless, remote locations
RUST: Local queue, retry with backoff
```

### Power Management

```
RULE: Minimize power consumption
WHY: Battery life, energy costs
RUST: Sleep modes, efficient algorithms
```

### Device Security

```
RULE: All communication encrypted
WHY: Physical access possible
RUST: TLS, signed messages
```

---

## Trace Down ↓

From constraints to design (Layer 2):

```
"Need offline-first design"
    ↓ m12-lifecycle: Local buffer with persistence
    ↓ m13-domain-error: Retry with backoff

"Need power efficiency"
    ↓ domain-embedded: no_std patterns
    ↓ m10-performance: Minimal allocations

"Need reliable messaging"
    ↓ m07-concurrency: Async with timeout
    ↓ MQTT: QoS levels
```

---

## Environment Comparison

| Environment      | Stack                | Crates                     |
|------------------|----------------------|----------------------------|
| Linux gateway     | tokio + std          | rumqttc, reqwest          |
| MCU device        | embassy + no_std      | embedded-hal               |
| Hybrid            | Split workloads       | Both                       |

## Key Crates

| Purpose           | Crate                  |
|-------------------|-----------------------|
| MQTT (std)        | rumqttc, paho-mqtt    |
| Embedded          | embedded-hal, embassy  |
| Async (std)       | tokio                 |
| Async (no_std)    | embassy                |
| Logging (no_std)  | defmt                  |
| Logging (std)     | tracing                |

## Design Patterns

| Pattern           | Purpose               | Implementation             |
|-------------------|-----------------------|----------------------------|
| Pub/Sub           | Device comms          | MQTT topics                |
| Edge compute      | Local processing       | Filter before upload       |
| OTA updates       | Firmware upgrade       | Signed + rollback          |
| Power mgmt        | Battery life           | Sleep + wake events        |
| Store & forward   | Network reliability    | Local queue                |

## Code Pattern: MQTT Client

```rust
use rumqttc::{AsyncClient, MqttOptions};
```