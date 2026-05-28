# Univrs.io Ecosystem Sources

## The Value Proposition

> "Imagine. Summon. Create. Make the Univrs in your image."

This is the promise. The critique skill exists to examine whether the implementation serves this promise.

---

## Core Components

### DOL - Domain Ontology Language

**Repository:** `~/repos/univrs-dol`
**Purpose:** Turing-complete, ontology-first programming language
**Compiles to:** Rust, TypeScript, JSON Schema, WebAssembly

**Key Paths:**
```
univrs-dol/
├── metadol/src/
│   ├── lexer.rs          # Tokenization
│   ├── parser.rs         # AST construction
│   ├── typechecker.rs    # Type inference & checking
│   ├── validator.rs      # Semantic validation
│   ├── lower/            # AST → HIR lowering
│   ├── codegen/          # Code generation
│   │   ├── rust.rs       # Rust codegen (186KB)
│   │   ├── typescript.rs # TS codegen (27KB)
│   │   └── jsonschema.rs # Schema codegen
│   ├── mlir/             # MLIR pipeline for WASM
│   └── wasm/             # Direct WASM emission
├── dol-*/                # CLI tools
└── tests/                # 631 tests
```

**Critical Inspection Points:**
- Language design decisions in `parser.rs`
- Type system power in `typechecker.rs`
- Built-in macros (20 total) - what's baked in?
- Codegen targets - who benefits from each?

**Git Commands:**
```bash
git -C ~/repos/univrs-dol log --oneline -20
git -C ~/repos/univrs-dol diff --stat HEAD~10..HEAD
```

---

### VUDO - Virtual Universe Distribution Operating System

**Repository:** `~/repos/univrs-vudo`
**Purpose:** Capability-based WASM sandbox runtime
**Runtime:** Wasmtime v27

**Key Paths:**
```
univrs-vudo/
├── vudo/
│   ├── vudo_vm/src/
│   │   ├── sandbox.rs    # 6-state lifecycle (57KB)
│   │   ├── linker.rs     # Host function setup (85KB)
│   │   ├── fuel.rs       # Execution metering (20KB)
│   │   ├── capability.rs # Permission system (19KB)
│   │   └── host/         # Host function implementations
│   │       ├── credit.rs   # Credit ledger (37KB)
│   │       ├── network.rs  # P2P networking (36KB)
│   │       ├── storage.rs  # Persistent KV (14KB)
│   │       └── ...
│   ├── spirit_runtime/src/
│   │   ├── manifest.rs   # TOML parsing, Ed25519 (43KB)
│   │   └── registry/     # Package management
│   └── vudo_cli/         # CLI interface
└── tests/                # 362+ tests
```

**Critical Inspection Points:**
- Capability grants in `capability.rs` - who controls?
- Fuel metering in `fuel.rs` - extraction or fairness?
- Host functions in `host/` - what's exposed?
- Sandbox lifecycle in `sandbox.rs` - state transitions

**Git Commands:**
```bash
git -C ~/repos/univrs-vudo log --oneline -20
git -C ~/repos/univrs-vudo diff --stat HEAD~10..HEAD
```

---

### ENR - Entropy-Nexus-Revival

**Repository:** `~/repos/univrs-enr`
**Purpose:** Economic primitives for VUDO OS (mycelial network principles)

**Key Paths:**
```
univrs-enr/
├── src/
│   ├── core/             # Credits, NodeId, state, invariants
│   ├── entropy/          # 4 entropy types for cost calculation
│   ├── nexus/            # Hub-based aggregation, market-making
│   ├── revival/          # Resource decomposition & cycling
│   ├── septal/           # Circuit breakers, network reliability
│   ├── pricing/          # Fixed, Dynamic, Auction models
│   └── bridge/           # gossipsub integration
└── dol/                  # DOL specifications
    ├── core.dol
    ├── entropy.dol
    ├── nexus.dol
    ├── pricing.dol
    ├── revival.dol
    └── septal.dol
```

**Critical Inspection Points:**
- Pricing models in `pricing/` - who wins in each?
- Entropy calculations - what behavior is incentivized?
- Nexus topology - new centralization points?
- Revival rules - who decides resource recycling?

**Git Commands:**
```bash
git -C ~/repos/univrs-enr log --oneline -20
git -C ~/repos/univrs-enr diff --stat HEAD~10..HEAD
```

---

### CryptoSaint.io

**Repository:** `~/repos/cryptosaint.io`
**Purpose:** Mycelial credit system, mutual credit & reputation

**Key Paths:**
```
cryptosaint.io/
├── src/
│   ├── types/            # Agent, Community, Transaction, CreditOffer
│   ├── core/
│   │   ├── credit_engine.rs  # Mutual credit creation
│   │   ├── reputation.rs     # Trust scoring
│   │   └── consensus.rs      # Network agreement
│   ├── crypto/           # Ed25519, encryption
│   ├── network/          # P2P discovery, sync, gossip
│   ├── storage/          # IPFS, Sled, in-memory
│   └── api/              # REST endpoints
└── tests/
```

**Key Constants:**
```rust
DEFAULT_REPUTATION: 1.0
MIN_VALIDATION_REPUTATION: 2.0
MAX_REPUTATION: 10.0
MAX_CREDIT_NEW_AGENT: 100.0
DEFAULT_QUORUM_THRESHOLD: 0.5
```

**Critical Inspection Points:**
- Reputation algorithm in `reputation.rs` - gameable?
- Credit creation in `credit_engine.rs` - who can create?
- Consensus rules in `consensus.rs` - majority tyranny?
- Quorum threshold 50% - what decisions require it?

**Git Commands:**
```bash
git -C ~/repos/cryptosaint.io log --oneline -20
git -C ~/repos/cryptosaint.io diff --stat HEAD~10..HEAD
```

---

## Supporting Infrastructure

### learn.univrs.io

**Repository:** `~/repos/learn.univrs.io`
**Purpose:** Educational platform for the ecosystem

**Critical Questions:**
- Who creates the curriculum?
- What's taught vs. what's hidden?
- Is education empowering or gatekeeping?

---

### vudo.univrs.io

**Repository:** `~/repos/vudo.univrs.io`
**Purpose:** VUDO web interface (Physarum simulation showcase)

**Critical Questions:**
- Is this accessible to non-developers?
- Does the interface democratize or mystify?

---

### univrs.io

**Repository:** `~/repos/univrs.io`
**Purpose:** Main landing page and marketing

**Critical Questions:**
- Does marketing match implementation?
- What's promised that doesn't exist yet?

---

### univrs-docs

**Repository:** `~/repos/univrs-docs`
**Purpose:** Documentation

**Critical Questions:**
- Is documentation complete and accurate?
- Who is the audience - developers only?

---

### univrs-identity

**Repository:** `~/repos/univrs-identity`
**Purpose:** Identity system

**Critical Questions:**
- Is identity truly self-sovereign?
- What's the recovery mechanism?
- Can identity be transferred or sold?

---

### univrs-network

**Repository:** `~/repos/univrs-network`
**Purpose:** P2P network layer

**Critical Questions:**
- Who runs the network nodes?
- What's the cost of participation?
- Is there geographic centralization?

---

### univrs-orchestration

**Repository:** `~/repos/univrs-orchestration`
**Purpose:** System orchestration

**Critical Questions:**
- Who orchestrates?
- What decisions are automated vs. human?

---

### univrs-state

**Repository:** `~/repos/univrs-state`
**Purpose:** State management

**Critical Questions:**
- Where is state stored?
- Who can access state?
- Is state truly user-controlled?

---

## Monitoring Commands

### Recent Activity Across Ecosystem

```bash
# All repos activity summary
for repo in univrs-dol univrs-vudo univrs-enr cryptosaint.io learn.univrs.io vudo.univrs.io univrs.io univrs-docs univrs-identity univrs-network univrs-orchestration univrs-state; do
  echo "=== $repo ==="
  git -C ~/repos/$repo log --oneline -3 2>/dev/null || echo "  (not found)"
done
```

### Changes in Last Week

```bash
# Commits in last 7 days
for repo in univrs-dol univrs-vudo univrs-enr cryptosaint.io; do
  echo "=== $repo ==="
  git -C ~/repos/$repo log --oneline --since="7 days ago" 2>/dev/null || echo "  (no recent changes)"
done
```

### Release Tags

```bash
# Recent tags
for repo in univrs-dol univrs-vudo univrs-enr; do
  echo "=== $repo ==="
  git -C ~/repos/$repo tag --sort=-creatordate | head -5 2>/dev/null || echo "  (no tags)"
done
```

---

## Integration Points to Watch

### DOL → VUDO

- How DOL-compiled WASM runs in VUDO sandbox
- Capability requirements generated from DOL specs
- Type mappings between DOL types and WASM

### VUDO → CryptoSaint

- Host functions: `host_credit_*` connecting to ledger
- Pricing enforcement via fuel metering
- Reputation hooks in sandbox decisions

### ENR → CryptoSaint

- Entropy multipliers affecting pricing
- NodeId mapping to agent identity
- Revival mechanisms triggering credit redistribution

### All → User

- **The critical question:** Can an ordinary user actually "Imagine. Summon. Create."?
- Or is this a developer-only ecosystem with user-friendly marketing?

---

*Updated: December 2025*
