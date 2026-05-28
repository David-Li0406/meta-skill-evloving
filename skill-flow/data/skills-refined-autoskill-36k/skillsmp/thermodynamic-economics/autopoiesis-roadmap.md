# Autopoietic Closure Roadmap

## Purpose

This roadmap defines the path toward increasing autopoietic closure for the Univrs.io ecosystem. Based on the gap analysis in `autopoiesis-audit.md`, we establish concrete milestones for achievable closure levels.

**Design Principle**: Be honest about what's achievable. Level 2 (hardware autopoiesis) is not feasible. Level 3 (energy autopoiesis) is partially achievable. Level 1 (software autopoiesis) is our primary target.

---

## Level 1 Goals: Software Autopoiesis

Target Closure: 70% (from current 40%)

### Milestone 1.1: Spirit-to-Spirit Compilation

**Goal**: Enable Spirits to generate and compile other Spirits without external tooling.

**Timeline**: Q1 2026

**Deliverables**:
```
1. DOL-to-WASM compiler ported to WASM
2. Compiler packaged as Spirit (spirit://univrs/dol-compiler)
3. Key management Spirit for signing
4. Registry Spirit for distribution
5. Integration test: Spirit A generates and deploys Spirit B
```

**Technical Requirements**:
```dol
// Required capabilities for self-compilation
domain SpiritCompilation {
  capability CompileSpirit {
    permissions: [
      "fs:read:*.dol",        // Read DOL source
      "wasm:compile",         // WASM compilation
      "crypto:sign:spirit",   // Sign packages
      "network:publish"       // Publish to registry
    ]
  }

  workflow CompilePipeline {
    input: DOLSource
    stages: [
      parse    -> AST,
      typecheck -> TypedAST,
      lower    -> HIR,
      optimize -> OptHIR,
      codegen  -> WASM,
      package  -> Spirit,
      sign     -> SignedSpirit,
      publish  -> SpiritReference
    ]
  }
}
```

**Success Criteria**:
- [ ] Compiler Spirit compiles itself (self-hosting)
- [ ] New Spirits can be generated from templates
- [ ] Signing and verification work internally
- [ ] No external toolchain required for Spirit production

**Closure Impact**: +15% (40% -> 55%)

---

### Milestone 1.2: Self-Healing Network

**Goal**: Network can recover from node failures and partitions without human intervention.

**Timeline**: Q2 2026

**Deliverables**:
```
1. Erasure coding for data redundancy
2. Automatic failover with Raft/PBFT consensus
3. Partition detection and recovery protocol
4. Health monitoring and alerting (internal)
5. Load-triggered resource reallocation
```

**Technical Requirements**:
```yaml
# Self-healing network configuration
network:
  redundancy:
    replication_factor: 3
    erasure_coding:
      data_shards: 4
      parity_shards: 2

  failover:
    consensus: "raft"
    leader_election_timeout: 5s
    heartbeat_interval: 500ms

  partition_recovery:
    detection_threshold: 10s
    reconciliation_protocol: "crdt_merge"
    conflict_resolution: "last_writer_wins"

  health:
    monitoring_interval: 30s
    alerting: internal  # No external services
    auto_remediation: true
```

**Success Criteria**:
- [ ] Network survives 30% node failure
- [ ] Data recoverable from any 4 of 6 shards
- [ ] Partition heals within 60 seconds
- [ ] No human intervention for common failures

**Closure Impact**: +10% (55% -> 65%)

---

### Milestone 1.3: Self-Configuring VM

**Goal**: VUDO instances can adapt to workloads and update themselves.

**Timeline**: Q2 2026

**Deliverables**:
```
1. Adaptive fuel allocation based on demand
2. Capability auto-discovery from Spirit manifests
3. Self-update mechanism with signature verification
4. Resource-aware scheduling
5. Configuration inheritance from parent instances
```

**Technical Requirements**:
```rust
// Self-configuring VUDO traits
trait SelfConfiguring {
    /// Adjust fuel allocation based on recent usage
    fn adapt_fuel(&mut self, usage_history: &[FuelUsage]) -> FuelConfig;

    /// Discover required capabilities from Spirit manifest
    fn discover_capabilities(&self, spirit: &Spirit) -> Vec<Capability>;

    /// Apply update from trusted source
    fn self_update(&mut self, update: SignedUpdate) -> Result<(), UpdateError>;

    /// Schedule work based on available resources
    fn resource_schedule(&self, queue: &WorkQueue) -> Schedule;
}

// Update verification
impl SelfUpdate for VudoInstance {
    fn verify_update(&self, update: &SignedUpdate) -> bool {
        let trusted_keys = self.config.trusted_update_keys;
        trusted_keys.iter().any(|key| {
            update.verify_signature(key)
        })
    }
}
```

**Success Criteria**:
- [ ] Fuel adjusts automatically to workload
- [ ] New capabilities granted without restart
- [ ] Updates apply without manual deployment
- [ ] No external orchestration required

**Closure Impact**: +5% (65% -> 70%)

---

## Level 3 Goals: Energy Autopoiesis

Target Closure: 30% (from current 6%)

### Milestone 3.1: First Solar-Powered Node

**Goal**: Deploy and operate a single Hyphal node entirely on solar power.

**Timeline**: Q1 2026

**Deliverables**:
```
1. Hardware specification for solar node
2. Energy monitoring Spirit
3. Battery management integration
4. Graceful degradation during low power
5. Documentation of energy consumption patterns
```

**Hardware Specification**:
```yaml
solar_node_v1:
  compute:
    device: "Raspberry Pi 5 (8GB)"
    power_consumption: "5-15W typical, 27W max"

  solar:
    panel: "100W monocrystalline"
    efficiency: "~20%"
    peak_sun_hours: "4-6h (location dependent)"

  storage:
    battery: "12V 100Ah LiFePO4"
    capacity: "1200Wh"
    cycles: "3000+"

  autonomy:
    sunny_day: "continuous operation"
    cloudy_day: "8-12 hours"
    no_sun: "~24 hours at low power"

  monitoring:
    energy_in: "spirit://univrs/solar-monitor"
    energy_out: "spirit://univrs/power-meter"
    alerts: "spirit://univrs/energy-alert"
```

**Success Criteria**:
- [ ] Node operates 30 consecutive days on solar
- [ ] Energy data logged and reported
- [ ] Graceful shutdown on low battery
- [ ] Auto-restart when power returns

**Closure Impact**: +4% (6% -> 10%)

---

### Milestone 3.2: Net-Positive Energy Cluster

**Goal**: Deploy a cluster of nodes that produces more energy than it consumes.

**Timeline**: Q3 2026

**Deliverables**:
```
1. Multi-node solar cluster design
2. Energy sharing protocol between nodes
3. Excess energy accounting (credits)
4. EROEI monitoring dashboard
5. Scalability analysis
```

**Cluster Design**:
```
Net-Positive Cluster (Target: 5 nodes)

Energy Production:
  5 × 200W panels = 1000W nameplate
  × 15% capacity factor = 150W average
  × 24h = 3,600 Wh/day

Energy Consumption:
  5 × 10W nodes = 50W continuous
  × 24h = 1,200 Wh/day
  + 20% network overhead = 1,440 Wh/day

Net Energy:
  Production: 3,600 Wh/day
  Consumption: 1,440 Wh/day
  Surplus: 2,160 Wh/day (60% excess)

EROEI: 3,600 / 1,440 = 2.5:1

Note: This is system EROEI including only operational costs.
Full lifecycle EROEI including manufacturing is lower.
```

**Energy Sharing Protocol**:
```dol
domain EnergySharing {
  entity EnergyCredit {
    source_node: NodeId
    amount_wh: Energy
    timestamp: Timestamp
    valid_until: Timestamp
  }

  // Nodes with surplus share with nodes in deficit
  function redistributeEnergy(cluster: [Node]) -> [Transfer] {
    let surplus_nodes = cluster.filter(n => n.battery > 80%)
    let deficit_nodes = cluster.filter(n => n.battery < 30%)

    return matchSurplusToDeficit(surplus_nodes, deficit_nodes)
  }
}
```

**Success Criteria**:
- [ ] Cluster EROEI > 2.0 sustained for 90 days
- [ ] Energy credits tracked and balanced
- [ ] No grid dependency during normal operation
- [ ] Graceful degradation during extended low sun

**Closure Impact**: +10% (10% -> 20%)

---

### Milestone 3.3: Community Solar Network

**Goal**: Federated network of solar-powered node operators.

**Timeline**: Q4 2026

**Deliverables**:
```
1. Solar node operator onboarding guide
2. Energy contribution tracking
3. Incentive mechanism for renewable nodes
4. Geographic diversity analysis
5. Resilience testing across time zones
```

**Network Design**:
```
Community Solar Network

Geographic Distribution:
  - Americas: ~30% of nodes
  - Europe/Africa: ~30% of nodes
  - Asia/Pacific: ~40% of nodes

Sun-Following Strategy:
  As one region enters night, another enters day.
  Distributed network maintains continuous operation.

Minimum Viable Network:
  - 10 nodes across 3+ continents
  - Combined production > combined consumption
  - No single point of failure

Incentives:
  - Solar nodes receive CryptoSaint reputation bonus
  - Energy contributors earn network credits
  - Priority access to computational resources
```

**Success Criteria**:
- [ ] 10+ solar nodes across 3+ continents
- [ ] Network survives regional night/weather events
- [ ] Aggregate EROEI > 3.0
- [ ] New operators can join with documentation only

**Closure Impact**: +10% (20% -> 30%)

---

## Metrics for Measuring Closure Progress

### Software Autopoiesis Metrics

```yaml
metrics:
  spirit_self_production:
    description: "Percentage of Spirits produced by Spirits"
    calculation: "spirits_compiled_internally / total_spirits_produced"
    target: 0.80
    current: 0.00

  network_self_healing:
    description: "Percentage of failures recovered without intervention"
    calculation: "auto_recovered_failures / total_failures"
    target: 0.90
    current: 0.45

  vm_self_configuration:
    description: "Percentage of configuration done automatically"
    calculation: "auto_configs / total_config_changes"
    target: 0.70
    current: 0.30

  overall_software_closure:
    description: "Weighted average of software autopoiesis metrics"
    weights:
      spirit_self_production: 0.4
      network_self_healing: 0.35
      vm_self_configuration: 0.25
    target: 0.70
```

### Energy Autopoiesis Metrics

```yaml
metrics:
  energy_self_sufficiency:
    description: "Percentage of energy from internal sources"
    calculation: "energy_from_solar / total_energy_consumed"
    target: 0.50
    current: 0.00

  network_eroei:
    description: "Energy Return on Energy Invested for network"
    calculation: "energy_produced / energy_consumed"
    target: 3.0
    current: 0.0

  renewable_node_fraction:
    description: "Percentage of nodes on renewable energy"
    calculation: "solar_nodes / total_nodes"
    target: 0.30
    current: 0.00

  geographic_resilience:
    description: "Coverage across time zones"
    calculation: "timezones_covered / 24"
    target: 0.50
    current: 0.00
```

### Composite Closure Score

```python
def calculate_closure_score(metrics):
    """
    Calculate overall autopoietic closure score.

    Returns value between 0.0 (fully heteronomous) and 1.0 (fully autopoietic).
    """

    # Level 1: Software (max 40% of total)
    software_score = (
        metrics['spirit_self_production'] * 0.16 +
        metrics['network_self_healing'] * 0.14 +
        metrics['vm_self_configuration'] * 0.10
    )

    # Level 2: Hardware (max 20% of total)
    # Not achievable, always 0
    hardware_score = 0.0

    # Level 3: Energy (max 40% of total)
    energy_score = (
        metrics['energy_self_sufficiency'] * 0.20 +
        metrics['renewable_node_fraction'] * 0.10 +
        metrics['geographic_resilience'] * 0.10
    )

    return software_score + hardware_score + energy_score

# Example:
# Current: 0.00 + 0.00 + 0.00 = 0.00 (0%)
# Target:  0.28 + 0.00 + 0.20 = 0.48 (48%)
```

---

## Roadmap Timeline

```
2026
────────────────────────────────────────────────────────────────

Q1 2026: FOUNDATION
├── Milestone 1.1: Spirit-to-Spirit Compilation
│   ├── Week 1-4: Port compiler to WASM
│   ├── Week 5-8: Package as Spirit
│   └── Week 9-12: Integration testing
│
└── Milestone 3.1: First Solar Node
    ├── Week 1-4: Hardware procurement
    ├── Week 5-8: Node setup and testing
    └── Week 9-12: 30-day operation test

Q2 2026: SELF-SUFFICIENCY
├── Milestone 1.2: Self-Healing Network
│   ├── Week 1-4: Erasure coding implementation
│   ├── Week 5-8: Failover protocols
│   └── Week 9-12: Partition recovery
│
└── Milestone 1.3: Self-Configuring VM
    ├── Week 1-4: Adaptive fuel
    ├── Week 5-8: Capability discovery
    └── Week 9-12: Self-update mechanism

Q3 2026: ENERGY INTEGRATION
└── Milestone 3.2: Net-Positive Cluster
    ├── Week 1-4: Multi-node design
    ├── Week 5-8: Energy sharing protocol
    └── Week 9-12: 90-day operation test

Q4 2026: COMMUNITY SCALE
└── Milestone 3.3: Community Solar Network
    ├── Week 1-4: Onboarding documentation
    ├── Week 5-8: Operator recruitment
    └── Week 9-12: Geographic distribution

────────────────────────────────────────────────────────────────
```

---

## Risk Assessment

### High Risk

| Risk | Mitigation |
|------|------------|
| WASM compiler performance insufficient | Profile and optimize; accept longer compile times |
| Solar nodes not economically viable | Focus on low-power devices; community subsidies |
| Weather disrupts solar cluster | Geographic distribution; grid backup option |

### Medium Risk

| Risk | Mitigation |
|------|------------|
| Self-update mechanism exploited | Strict key management; staged rollouts |
| Network partition lasts longer than storage | Graceful degradation; data prioritization |
| Closure metrics gamed | Multiple independent measurements |

### Accepted Limitations

| Limitation | Rationale |
|------------|-----------|
| Level 2 (hardware) not achievable | Beyond scope; accept dependency on manufacturing |
| Full energy independence impossible | Realistic goal is partial closure + transparency |
| Human community always required | Feature, not bug; governance needs humans |

---

## Success Criteria Summary

| Milestone | Target Date | Key Metric | Target Value |
|-----------|-------------|------------|--------------|
| 1.1 Spirit Compilation | Q1 2026 | Self-compiled Spirits | > 0 |
| 1.2 Self-Healing Network | Q2 2026 | Auto-recovery rate | > 90% |
| 1.3 Self-Configuring VM | Q2 2026 | Auto-configuration rate | > 70% |
| 3.1 First Solar Node | Q1 2026 | Continuous solar days | > 30 |
| 3.2 Net-Positive Cluster | Q3 2026 | Cluster EROEI | > 2.0 |
| 3.3 Community Network | Q4 2026 | Geographic coverage | 3+ continents |

**Overall Target: 48% Autopoietic Closure by End of 2026**

This represents significant progress while remaining honest about fundamental thermodynamic constraints.

---

## References

1. autopoiesis-audit.md - Gap analysis
2. autopoiesis-checklist.md - Theoretical framework
3. eroei_calculator.py - Energy calculations
4. thermodynamic-economics-swarm.yaml - Initiative structure

---

*Roadmap Date: 2026-01-02*
*Status: Active*
*Next Review: Monthly*
