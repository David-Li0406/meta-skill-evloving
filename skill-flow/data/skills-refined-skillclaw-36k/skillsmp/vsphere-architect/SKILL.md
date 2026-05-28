---
name: vsphere-architect
description: |
  VMware vSphere architecture and design expertise for enterprise virtualization. Use when working with vSphere/ESXi for capacity planning, resource management, performance tuning, or infrastructure design. Covers CPU oversubscription, memory management, storage architecture, DRS, HA, networking, and best practices for enterprise deployments.
  
  Commands:
  - /vcpu-ratio - Explain vCPU:pCPU ratios and CPU oversubscription
  - /memory-mgmt - Memory management techniques and optimization
  - /storage-design - Storage architecture patterns and best practices
  - /drs-rules - DRS configuration and affinity/anti-affinity rules
  - /ha-design - High availability and fault tolerance design
  - /capacity-plan - Capacity planning methodology and ratios
  - /perf-troubleshoot - Performance troubleshooting with esxtop metrics
---

# vSphere Architect

## Commands

| Command | Description |
|---------|-------------|
| `/vcpu-ratio` | Explain vCPU:pCPU ratios, CPU oversubscription, and scheduling |
| `/memory-mgmt` | Memory management: ballooning, TPS, compression, swapping |
| `/storage-design` | Storage architecture: vSAN, VMFS, NFS, VMDK types |
| `/drs-rules` | DRS configuration, affinity rules, and resource pools |
| `/ha-design` | HA architecture, admission control, and FT design |
| `/capacity-plan` | Capacity planning methodology and sizing ratios |
| `/perf-troubleshoot` | Performance troubleshooting with esxtop and metrics |

### Command Examples

```
/vcpu-ratio explain how 4:1 affects scheduling
/memory-mgmt when does ballooning kick in vs compression?
/storage-design vSAN vs NFS for VDI workloads
/drs-rules anti-affinity for SQL Always On cluster
/ha-design admission control for N+1 with 4 hosts
/capacity-plan sizing for 500 VMs mixed workload
/perf-troubleshoot high CPU ready time on specific VMs
```

## CPU Architecture

### vCPU:pCPU Ratio

The vCPU:pCPU ratio emerges from cumulative CPU allocation decisions—it's not a single configurable setting.

**How the ratio is determined:**

- **VM-level CPU assignment**: Each VM's vCPU count (Edit Settings > CPU). Sum all vCPUs across VMs divided by physical cores = ratio
- **Resource pool reservations/limits**: Reservations guarantee minimum CPU; limits cap maximum. These influence scheduler aggressiveness during contention
- **CPU scheduler**: VMkernel distributes vCPU load across pCPUs using ready time and co-stop metrics. Not directly configurable
- **CPU affinity (optional)**: Pin vCPUs to specific pCPUs, controlling local scheduling ratios for latency-sensitive workloads
- **Power management**: Fewer active cores with power management enabled implicitly increases ratio

**Enterprise guidance:**

| Workload Type | Recommended Ratio | Notes |
|--------------|-------------------|-------|
| General purpose | 4:1 to 6:1 | Default for mixed workloads |
| CPU-intensive | 2:1 to 3:1 | Databases, analytics, compilation |
| VDI | 6:1 to 8:1 | Bursty, non-concurrent usage |
| Dev/Test | 8:1 to 10:1 | Tolerates contention |

**Validation metrics:**

- **CPU Ready** > 5% sustained = ratio too aggressive
- **Co-stop** > 3% = too many vCPUs per VM for workload
- **%USED** approaching 80% = add capacity

### CPU Ready vs Co-Stop

**CPU Ready**: Time a vCPU waits in run queue because no pCPU is available. Indicates host-level oversubscription.

**Co-Stop**: Time a vCPU waits for sibling vCPUs to be scheduled together (SMP VMs). Indicates the VM has more vCPUs than it can efficiently use.

```
# esxtop CPU view
Press 'c' for CPU view
Key columns: %RDY, %CSTP, %USED, %MLMTD
```

**Troubleshooting flow:**
1. High Ready + Low Co-stop → Host oversubscribed, reduce total vCPUs or add hosts
2. High Co-stop + Normal Ready → VM has too many vCPUs, reduce VM's vCPU count
3. High Ready + High MLMTD → Resource pool limit hit, raise limit or reservation

For detailed CPU scheduler internals, see [references/cpu-scheduler.md](references/cpu-scheduler.md).

## Memory Architecture

### Memory Reclamation Hierarchy

ESXi reclaims memory in this order (least to most disruptive):

1. **Transparent Page Sharing (TPS)** - Deduplicates identical pages. Salted by default for security (only intra-VM)
2. **Ballooning** - Guest driver (vmmemctl) requests memory from guest OS. Requires VMware Tools
3. **Compression** - Compresses pages before swapping. 4KB → typically 2KB
4. **Swapping** - Host swaps VM pages to disk. Severe performance impact

**State thresholds:**

| State | Free Memory | Techniques Active |
|-------|-------------|-------------------|
| High | > 6% | None |
| Soft | 4-6% | TPS, Balloon |
| Hard | 2-4% | TPS, Balloon, Compression |
| Low | < 2% | All including Swap |

**Memory metrics:**

- **MCTLSZ**: Balloon driver target size (MB)
- **SWCUR**: Current swap usage (MB)
- **CACHEUSD**: Compressed memory cache (MB)
- **%ACTV**: Actively used memory percentage

### Memory Overcommitment

Unlike CPU, memory overcommitment has severe performance implications when reclamation occurs.

**Conservative approach**: Size memory to 80% utilization with no overcommitment for production workloads.

**Aggressive approach**: 1.2:1 to 1.5:1 overcommitment acceptable if:
- VMware Tools installed (ballooning works)
- Guest OS can handle balloon requests
- SSD-backed swap file configured
- Non-latency-sensitive workloads

For memory sizing patterns, see [references/memory-sizing.md](references/memory-sizing.md).

## Storage Architecture

### Datastore Types

| Type | Use Case | Max Size | Pros | Cons |
|------|----------|----------|------|------|
| VMFS 6 | Block storage | 64TB | Mature, flexible | Requires SAN |
| NFS v3/v4.1 | File storage | Array limit | Simple, thin | Network dependent |
| vSAN | HCI | Cluster-wide | Integrated, policy-based | Requires local disks |
| vVols | Policy-based | Array limit | Granular control | Array support required |

### VMDK Types

- **Thick Eager Zeroed**: Best performance. Space allocated and zeroed at creation. Required for FT, MSCS
- **Thick Lazy Zeroed**: Space allocated, zeroed on first write. Good balance
- **Thin**: Space allocated on write. Best capacity. Performance penalty on first writes

### vSAN Architecture

**Requirements per host:**
- Minimum 1 SSD (cache tier) + 1 capacity device
- 10GbE minimum (25GbE recommended)
- VMkernel port group for vSAN traffic

**Design considerations:**
- FTT (Failures to Tolerate): Defines replica count. FTT=1 requires 3+ hosts
- Stripe width: Spreads I/O across disks for performance
- Deduplication/Compression: Reduce capacity, adds CPU overhead

For storage design patterns, see [references/storage-patterns.md](references/storage-patterns.md).

## DRS and Resource Pools

### DRS Automation Levels

| Level | Behavior |
|-------|----------|
| Manual | Recommendations only, no automatic moves |
| Partially Automated | Initial placement automatic, migrations manual |
| Fully Automated | All placement and migrations automatic |

**Migration threshold** (1-5):
- Level 1: Priority 1 recommendations only (mandatory moves)
- Level 5: All recommendations including minor improvements

### Resource Pool Design

Resource pools partition cluster resources. Key settings:

- **Reservation**: Guaranteed minimum resources
- **Limit**: Maximum resources (default unlimited)
- **Shares**: Relative priority during contention (Low/Normal/High/Custom)

**Anti-patterns to avoid:**
- Deeply nested pools (>3 levels)
- Reservations that exceed physical capacity
- Mixing VMs directly in cluster with resource pools

### Affinity Rules

| Rule Type | Purpose | Example |
|-----------|---------|---------|
| VM-VM Affinity | Keep VMs together | App + DB on same host for latency |
| VM-VM Anti-affinity | Separate VMs | HA cluster nodes on different hosts |
| VM-Host Affinity | Prefer hosts | License-bound software |
| VM-Host Anti-affinity | Avoid hosts | Keep prod off dev hardware |

**Required vs Preferred:**
- **Required (must)**: DRS won't violate. Can prevent HA failover
- **Preferred (should)**: DRS tries but will violate if necessary

For DRS tuning patterns, see [references/drs-tuning.md](references/drs-tuning.md).

## High Availability

### HA Admission Control

**Policies:**

| Policy | Behavior | Best For |
|--------|----------|----------|
| Host failures cluster tolerates | Reserve capacity for N host failures | Predictable sizing |
| Percentage of cluster resources | Reserve X% CPU/memory | Flexible environments |
| Dedicated failover hosts | Specific hosts as standby | Compliance requirements |

**Slot calculation** (for host failures method):
- Slot size = Largest VM reservation (or 32MHz CPU, 128MB memory if no reservations)
- Total slots = Sum of slots per host
- Available slots = Total - (N hosts worth of slots)

**Warning**: Large reservation on single VM can inflate slot size, wasting capacity.

### Fault Tolerance

**FT requirements:**
- Thick eager-zeroed disks
- vSphere FT logging network (10GbE minimum)
- Same CPU family primary/secondary
- Max 8 vCPUs per FT VM

**FT vs HA:**
- FT: Zero downtime, synchronous replication, significant resource overhead
- HA: Restart after failure, seconds of downtime, minimal overhead

For HA design patterns, see [references/ha-patterns.md](references/ha-patterns.md).

## Capacity Planning

### Sizing Methodology

1. **Inventory workloads**: Document CPU, memory, storage, network requirements
2. **Determine ratios**: Based on workload type (see CPU section)
3. **Calculate raw requirements**: Sum all resources
4. **Add HA overhead**: N+1 or N+2 based on SLA
5. **Add growth buffer**: Typically 20-30% for 12-18 months
6. **Validate with metrics**: Deploy, monitor, adjust

### Quick Sizing Formulas

**Hosts needed (N+1 HA):**
```
Hosts = ceiling((Total vCPUs / (Cores per Host × vCPU Ratio)) + 1)
```

**Memory calculation:**
```
Memory per Host = (Total VM Memory / Hosts) × 1.1 (10% ESXi overhead)
```

**Example**: 100 VMs, average 4 vCPU and 16GB RAM each
- Total vCPUs: 400
- Host: 32 cores, 4:1 ratio → 128 vCPUs per host
- Compute hosts: ceiling(400/128) + 1 = 4 + 1 = 5 hosts
- Memory per host: (100 × 16GB / 5) × 1.1 = 352GB → 384GB config

## Performance Troubleshooting

### esxtop Quick Reference

```bash
# Launch esxtop
esxtop

# Key views
c - CPU
m - Memory
n - Network
d - Disk adapter
u - Disk device
v - Disk VM
```

### Critical Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| CPU %RDY | >5% | >10% | Reduce oversubscription |
| CPU %CSTP | >3% | >5% | Reduce VM vCPU count |
| MEM %ACTV | >80% | >90% | Add memory or reduce VMs |
| KAVG (disk latency) | >20ms | >30ms | Check storage path |
| DAVG (device latency) | >20ms | >30ms | Storage array issue |
| %DRPTX/%DRPRX | >0.1% | >1% | Network saturation |

### Common Issues and Fixes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| High Ready across all VMs | Host oversubscribed | Add hosts, reduce vCPUs |
| High Ready on specific VMs | Resource pool limit | Raise limit/reservation |
| High Co-stop | Too many vCPUs | Reduce VM's vCPU count |
| Ballooning active | Memory pressure | Add RAM or reduce VMs |
| KAVG >> DAVG | HBA/path issue | Check multipathing, HBA |
| DAVG high | Storage array | Check array latency |

For detailed troubleshooting workflows, see [references/troubleshooting.md](references/troubleshooting.md).

## Command Handling

### /vcpu-ratio Command

When handling CPU ratio questions:
1. Explain the ratio is emergent, not directly configured
2. List the components that influence it (VM settings, pools, scheduler)
3. Provide recommended ratios for the workload type
4. Always mention validation metrics (Ready, Co-stop)
5. Tie back to capacity planning implications

### /memory-mgmt Command

When handling memory questions:
1. Explain the reclamation hierarchy and thresholds
2. Clarify ballooning requires VMware Tools
3. Discuss overcommitment implications honestly
4. Reference esxtop metrics for diagnosis
5. Provide sizing guidance based on workload type

### /storage-design Command

When handling storage questions:
1. Clarify requirements: performance, capacity, features
2. Compare relevant options (vSAN vs NFS vs VMFS)
3. Discuss VMDK types and their tradeoffs
4. Cover multipathing for SAN configurations
5. Reference vSAN requirements if applicable

### /drs-rules Command

When handling DRS questions:
1. Understand the placement constraint needed
2. Recommend rule type (affinity vs anti-affinity, VM vs Host)
3. Discuss required vs preferred implications
4. Warn about HA interaction with required rules
5. Provide specific configuration steps

### /ha-design Command

When handling HA questions:
1. Clarify availability requirements (SLA)
2. Recommend admission control policy
3. Discuss slot sizing implications
4. Cover network partitioning (isolation response)
5. Discuss FT if zero-downtime required

### /capacity-plan Command

When handling capacity questions:
1. Gather workload characteristics
2. Apply appropriate ratios
3. Include HA overhead
4. Add growth buffer
5. Provide host count and configuration recommendations

### /perf-troubleshoot Command

When handling performance questions:
1. Identify the symptom (CPU, memory, storage, network)
2. Reference relevant esxtop metrics
3. Compare against thresholds
4. Provide diagnostic flow
5. Recommend specific actions
