# PlanetServe Integration

> Decentralized infrastructure for scalable, privacy-preserving distributed computing in MyceliaNetwork.

Based on: [PlanetServe: Democratizing AI by Enabling Serverless Decentralized LLM Serving](https://arxiv.org/abs/2504.20101) (Fang et al., 2025)

## Overview

This module integrates PlanetServe's overlay network capabilities into MyceliaNetwork to solve scaling challenges for decentralized social coordination. The integration provides:

- **Reputation Scoring**: Asymmetric reward/punishment system that incentivizes honest behavior
- **Hash-Radix Tree (HR-Tree)**: Efficient decentralized workload distribution with delta synchronization
- **S-IDA**: Secure Information Dispersal Algorithm for anonymous communication
- **BFT Verification Committee**: Tendermint-based consensus for consistent reputation updates

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MyceliaNetwork Node                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  PlanetServe Layer                   │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │    │
│  │  │  Reputation │  │   HR-Tree   │  │    S-IDA    │  │    │
│  │  │   Manager   │  │   Router    │  │  Encoder/   │  │    │
│  │  │             │  │             │  │   Decoder   │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │    │
│  │         │                │                │         │    │
│  │  ┌──────┴────────────────┴────────────────┴──────┐  │    │
│  │  │           Verification Committee              │  │    │
│  │  │        (BFT Consensus / Tendermint)           │  │    │
│  │  └───────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│  ┌─────────────────────────┴─────────────────────────┐      │
│  │              libp2p Network Layer                  │      │
│  │         (Gossipsub / mDNS / TCP+Noise)            │      │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Module Reference

### Location

All PlanetServe code is in `mycelia/src/planetserve/`:

```
planetserve/
├── mod.rs           # Module exports and PlanetServeLayer
├── config.rs        # Configuration structs
├── reputation.rs    # NodeReputation, ReputationManager
├── hr_tree.rs       # HRTree data structure
├── sida.rs          # SidaEncoder, SidaDecoder
└── verification.rs  # BFT verification committee
```

### Quick Start

```rust
use planetserve::{PlanetServeLayer, PlanetServeConfig};

// Create with defaults
let config = PlanetServeConfig::default();
let layer = PlanetServeLayer::new(config);

// Update node reputation
let new_score = layer.update_node_reputation("peer-123", 0.85).await;

// Check if trusted
if layer.is_node_trusted("peer-123").await {
    // Route work to this node
}

// Anonymous message encoding
let session_ids: Vec<[u8; 32]> = get_proxy_session_ids();
let cloves = layer.encode_anonymous(message, destination, session_ids)?;
```

## Components

### 1. Reputation Scoring

**Formula**: `R(T) = α·R(T-1) + β·C(T)`

Where:
- `α = 0.4`: History weight
- `β = 0.6`: Current performance weight
- `C(T)`: Credit score in epoch T (0.0 - 1.0)

**Asymmetric Punishment**: When abnormal ratio exceeds γ (0.2), apply punishment:

```
punishment_factor = (w + 1) / (w + c/γ + 2)
R(T) = α·R(T-1) + punishment_factor·C(T)
```

Where `w` is sliding window size (5 epochs) and `c` is count of abnormal scores.

**Usage**:

```rust
use planetserve::reputation::{NodeReputation, ReputationConfig};

let config = ReputationConfig::default();
let mut rep = NodeReputation::new("node-1".into(), config);

// Good performance
rep.update(0.9);  // Score increases
rep.update(0.85); // Score increases

// Bad performance triggers punishment
rep.update(0.1);  // Abnormal, enters window
rep.update(0.1);  // Another abnormal score

// Check status
if rep.is_trusted() {
    println!("Node is trusted: {}", rep.score());
}
```

### 2. Hash-Radix Tree (HR-Tree)

Distributed data structure for efficient workload routing based on content similarity.

**Key Features**:
- 8-bit hash fingerprints per tree level
- Configurable chunk lengths from Sentry nodes
- Delta synchronization (5-second intervals)
- Load-balanced node selection

**Usage**:

```rust
use planetserve::hr_tree::{HRTree, NodeMetadata, ChunkConfig};

let config = ChunkConfig::default();
let mut tree = HRTree::new(config);

// Insert node with its cached content
let metadata = NodeMetadata {
    node_address: "10.0.0.5:8080".into(),
    lb_factor: 0.3,
    reputation: 0.8,
    last_update: current_timestamp(),
};
tree.insert(content_bytes, metadata);

// Search for best node to handle similar content
let (prefix_len, candidates) = tree.search(new_content);
if let Some(best) = tree.get_best_node(&candidates) {
    // Route to best.node_address
}

// Delta sync for network efficiency
let delta = tree.generate_delta(last_sync_time);
broadcast_delta(delta);
```

### 3. S-IDA Anonymous Communication

Secure Information Dispersal Algorithm combining:
- **AES-256-GCM**: Message encryption
- **Rabin's IDA**: Message splitting into n fragments
- **Shamir's Secret Sharing**: Key distribution

**Parameters**:
- `n = 4`: Total number of cloves (message fragments)
- `k = 3`: Threshold for reconstruction

**Usage**:

```rust
use planetserve::sida::{SidaEncoder, SidaDecoder, SidaConfig};

let config = SidaConfig::default(); // n=4, k=3
let encoder = SidaEncoder::new(config.clone());
let decoder = SidaDecoder::new(config);

// Encode message for anonymous transmission
let session_ids = get_proxy_session_ids(); // 4 session IDs
let cloves = encoder.encode(
    b"Secret credit transaction",
    "destination-node",
    session_ids
)?;

// Each clove routes through different proxy
for (clove, proxy) in cloves.iter().zip(proxies.iter()) {
    proxy.send(clove).await?;
}

// Receiver reconstructs with k cloves
let received_cloves = collect_cloves().await;
let message = decoder.decode(&received_cloves)?;
```

### 4. BFT Verification Committee

Tendermint-based consensus for reputation updates.

**Protocol**:
1. Leader selected by VRF on previous epoch's commit hash
2. Leader sends challenge prompts to target nodes
3. Nodes return signed responses through anonymous overlay
4. Leader computes perplexity scores
5. Two-phase voting: Pre-Vote → Pre-Commit
6. Commit if 2n/3+1 nodes agree

**Usage**:

```rust
use planetserve::verification::{
    BasicVerificationCommittee,
    EpochRunner,
    VerificationConfig,
};
use std::sync::Arc;

let config = VerificationConfig::default();
let committee = Arc::new(BasicVerificationCommittee::new(
    "validator-1".into(),
    vec!["v1", "v2", "v3", "v4"].into_iter().map(String::from).collect(),
    config,
    reputation_manager.clone(),
));

// Run epoch verification loop
let runner = EpochRunner::new(committee, 60, 10); // 60s epochs, 10 nodes/epoch
runner.run(known_nodes).await;
```

## Configuration

### Default Values

```rust
// Reputation
ReputationConfig {
    alpha: 0.4,              // History weight
    beta: 0.6,               // Current weight
    window_size: 5,          // Sliding window epochs
    gamma: 0.2,              // Punishment threshold
    trust_threshold: 0.4,    // Minimum for trusted
    initial_score: 0.5,      // Starting reputation
}

// HR-Tree
ChunkConfig {
    chunk_lengths: [32, 64, 128, 256],
    hash_bits: 8,
    sync_interval_secs: 5,
}

// S-IDA
SidaConfig {
    n: 4,  // Total cloves
    k: 3,  // Reconstruction threshold
}

// Verification
VerificationConfig {
    epoch_duration_secs: 60,
    nodes_per_epoch: 10,
    response_timeout_secs: 30,
}
```

### Custom Configuration

```rust
let config = PlanetServeConfig::default()
    .with_reputation(ReputationConfig {
        alpha: 0.3,
        beta: 0.7,
        ..Default::default()
    })
    .with_sida(SidaConfig { n: 5, k: 3 });

let layer = PlanetServeLayer::new(config);
```

## Integration with MyceliaNetwork

### Gossipsub Integration

The PlanetServe layer integrates with libp2p's gossipsub for message routing:

```rust
// In message handler
fn handle_gossipsub_message(
    &mut self,
    message: GossipsubMessage,
    planetserve: &PlanetServeLayer,
) {
    let source = message.source.unwrap();

    // Check reputation before processing
    if planetserve.is_node_trusted(&source.to_string()).await {
        // Process message
        self.process_trusted_message(message).await;

        // Update reputation positively
        planetserve.update_node_reputation(
            &source.to_string(),
            0.8
        ).await;
    } else {
        // Log and potentially quarantine
        tracing::warn!("Untrusted message from {}", source);
    }
}
```

### Anonymous Credit Transactions

For CryptoSaint integration:

```rust
async fn send_anonymous_credit(
    planetserve: &PlanetServeLayer,
    amount: u64,
    recipient: &str,
) -> Result<(), CreditError> {
    let tx = CreditTransaction::new(amount, recipient);
    let tx_bytes = bincode::serialize(&tx)?;

    // Get proxy session IDs from established paths
    let session_ids = proxy_manager.get_session_ids()?;

    // Encode for anonymous transmission
    let cloves = planetserve.encode_anonymous(
        &tx_bytes,
        recipient,
        session_ids
    )?;

    // Route each clove through its proxy
    for (clove, proxy) in cloves.iter().zip(proxies.iter()) {
        proxy.route_clove(clove).await?;
    }

    Ok(())
}
```

## Testing

Run the test suite:

```bash
cd mycelia
cargo test planetserve
```

Individual module tests:

```bash
cargo test planetserve::reputation
cargo test planetserve::hr_tree
cargo test planetserve::sida
cargo test planetserve::verification
```

## Performance Targets

| Metric | Target |
|--------|--------|
| Reputation update latency | <1ms |
| HR-tree search latency | <0.1ms |
| Delta sync overhead | <10% of full broadcast |
| S-IDA encode latency | <0.5ms |
| S-IDA decode latency | <0.5ms |
| Path establishment | <200ms |

## References

1. [PlanetServe Paper](https://arxiv.org/abs/2504.20101)
2. [Rabin's Information Dispersal Algorithm](https://dl.acm.org/doi/10.1145/62212.62213)
3. [Shamir's Secret Sharing](https://dl.acm.org/doi/10.1145/359168.359176)
4. [Tendermint Consensus](https://arxiv.org/abs/1807.04938)
