# DRS Tuning Guide

## DRS Algorithm Overview

DRS evaluates cluster balance using these inputs:
1. Current host CPU/memory utilization
2. VM resource demands (active, entitled)
3. Affinity/anti-affinity constraints
4. Resource pool structure

**Imbalance threshold**: Standard deviation of host loads

## Automation Levels in Detail

### Manual

- All recommendations require approval
- Initial placement: Admin chooses host
- Use for: Change-controlled environments

### Partially Automated

- Initial placement: DRS chooses host
- Migrations: Require approval
- Use for: Production with change control

### Fully Automated

- Initial placement: DRS chooses host
- Migrations: Automatic based on threshold
- Use for: Most production workloads

## Migration Threshold Deep Dive

### Priority Levels

| Priority | Migration Threshold | Triggers |
|----------|-----------------------|----------|
| 1 | All levels (1-5) | Must moves (affinity violations, host maintenance) |
| 2 | Levels 2-5 | Significant capacity improvement |
| 3 | Levels 3-5 | Good capacity improvement |
| 4 | Levels 4-5 | Moderate improvement |
| 5 | Level 5 only | Minor improvement |

### Threshold Selection

**Level 1 (Conservative):**
- Minimal migrations
- Only mandatory moves
- Maximum stability

**Level 3 (Balanced, default):**
- Moderate migrations
- Significant improvements only
- Good for mixed workloads

**Level 5 (Aggressive):**
- Frequent migrations
- Small improvements trigger moves
- Maximum balance, most vMotions

## Resource Pool Hierarchy

### Expandable Reservations

**Enabled (default):**
- Pool can request resources beyond reservation from parent
- More flexible, less predictable

**Disabled:**
- Pool limited to its reservation
- Predictable isolation
- Can starve workloads if undersized

### Share Calculations

Shares are relative within sibling pools:

```
Pool A: 4000 shares (High)
Pool B: 2000 shares (Normal)
Pool C: 1000 shares (Low)

During contention:
Pool A: 4000/7000 = 57%
Pool B: 2000/7000 = 29%
Pool C: 1000/7000 = 14%
```

### Nested Pool Inheritance

```
Root Pool (8000 shares)
├── Production (4000 shares) → 50% of root
│   ├── Web (2000 shares) → 50% of Production = 25% of root
│   └── DB (2000 shares) → 50% of Production = 25% of root
└── Dev (4000 shares) → 50% of root
```

## Affinity Rules Configuration

### VM-VM Anti-Affinity (Must Separate)

**Use case**: HA cluster nodes

```yaml
Rule Name: SQL-AG-Separation
Rule Type: Separate Virtual Machines
VMs:
  - SQL-Node1
  - SQL-Node2
  - SQL-Node3
Enforcement: Required (Must)
```

**Warning**: Required rules can prevent HA restart if insufficient hosts.

### VM-VM Affinity (Keep Together)

**Use case**: App-tier and DB on same host for latency

```yaml
Rule Name: App-DB-Colocation
Rule Type: Keep Virtual Machines Together
VMs:
  - App-Server
  - DB-Server
Enforcement: Preferred (Should)
```

### VM-Host Affinity

**Use case**: License compliance (Oracle, SQL)

```yaml
Rule Name: Licensed-Hosts
Rule Type: Virtual Machines to Hosts
VM Group: Licensed-VMs
Host Group: Licensed-Hosts
Enforcement: Must run on hosts in group
```

### VM-Host Anti-Affinity

**Use case**: Keep production off certain hardware

```yaml
Rule Name: No-Prod-on-Old-Hosts
Rule Type: Virtual Machines to Hosts
VM Group: Production-VMs
Host Group: Old-Hosts
Enforcement: Must NOT run on hosts in group
```

## DRS Groups

### Creating Host Groups

1. Cluster > Configure > VM/Host Groups
2. Add Host Group
3. Select member hosts

### Creating VM Groups

1. Cluster > Configure > VM/Host Groups
2. Add VM Group
3. Select member VMs

**Dynamic membership**: Use vSphere Tags + VM Groups for auto-population.

## Advanced DRS Settings

### Key Parameters

```
# MinGoodness: Minimum improvement % to recommend migration
# Default: 0.0 (any improvement counts)
config.vpxd.drs.MinGoodness = 0.5

# MaxMovesPerHost: Max simultaneous vMotions per host
# Default: 8
config.vpxd.drs.MaxMovesPerHost = 4

# CostBenefit: Factor for vMotion cost vs benefit
# Higher = fewer migrations
config.vpxd.drs.CostBenefit = 0.5
```

### Per-VM DRS Settings

Override cluster DRS behavior per-VM:

| Setting | Effect |
|---------|--------|
| Disabled | No DRS recommendations for this VM |
| Partially Automated | Override for this VM only |
| Fully Automated | Override for this VM only |

**Use for:**
- VMs that shouldn't migrate (affinity workaround)
- VMs with specific automation needs

## DRS and Other Features

### DRS + HA Interaction

- HA restart honors affinity rules (if possible)
- Required rules can block HA restart
- HA doesn't consider DRS balance for restart placement

**Best practice**: Use "Preferred" for most rules, "Required" sparingly.

### DRS + vMotion Network

DRS migrations use vMotion network:
- Ensure adequate bandwidth
- Multiple vMotion VMkernels improve throughput
- vMotion over long distance affects migration time

### Predictive DRS

Uses vRealize Operations integration:
- Predicts workload demands
- Pre-positions VMs before contention
- Requires vROps license

### DRS in vSAN Stretched Clusters

**Affinity requirements:**
- VMs in Site A should prefer Site A hosts
- Witness host excluded from DRS

Configure site-based host groups and VM-Host affinity rules.

## Troubleshooting DRS

### No Recommendations

**Check:**
1. DRS enabled and set to appropriate automation
2. Cluster has >1 host with capacity
3. Affinity rules not blocking all moves
4. VM not individually set to DRS disabled

### Frequent Migrations

**Check:**
1. Migration threshold too aggressive (5)
2. Workload patterns highly variable
3. Host capacities significantly different

**Solution:**
- Lower migration threshold
- Use resource pools to isolate bursty workloads
- Consider VM-level DRS override

### DRS Faults

View in vCenter > Cluster > Monitor > DRS

Common faults:
- Incompatible CPU features
- Missing shared storage
- Network label mismatch
- Affinity rule conflicts
