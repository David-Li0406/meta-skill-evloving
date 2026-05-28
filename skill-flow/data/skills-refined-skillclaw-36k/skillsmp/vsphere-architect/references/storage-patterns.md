# Storage Design Patterns

## Datastore Selection Guide

### Decision Matrix

| Requirement | VMFS | NFS | vSAN | vVols |
|------------|------|-----|------|-------|
| Block storage available | ✓ | | | ✓ |
| File storage available | | ✓ | | |
| Local disk only | | | ✓ | |
| Per-VM policies | Limited | Limited | ✓ | ✓ |
| Array offload | ✓ (VAAI) | ✓ (partial) | N/A | ✓ |
| Thin provisioning | ✓ | ✓ | ✓ | ✓ |
| Deduplication | Array | Array | ✓ | Array |

### VMFS Design

**VMFS 6 features:**
- 64TB max datastore
- 512e drive support
- Automatic space reclamation (UNMAP)
- SE Sparse (linked clone efficiency)

**Sizing datastores:**
```
Recommended: 20-40 VMs per datastore (manageability)
Max single VMDK: 62TB
```

**LUN sizing:**
- Larger LUNs = fewer devices to manage
- Smaller LUNs = better queue depth distribution
- Balance based on workload I/O patterns

**Queue depth considerations:**
```
Per-LUN queue depth × Number of LUNs = Host queue capacity
```

If many VMs on few LUNs, queue depth contention occurs.

### NFS Design

**Protocol comparison:**

| Feature | NFS v3 | NFS v4.1 |
|---------|--------|----------|
| Stateless/Stateful | Stateless | Stateful |
| Locking | External (NLM) | Built-in |
| Session trunking | No | Yes |
| Kerberos | Limited | Full |

**NFS best practices:**
- Dedicated VMkernel for NFS
- Jumbo frames if array supports
- Multiple NFS paths for redundancy (NFS v4.1)
- TCP window size optimization

**Mount options:**
```
/vol/datastore hostname(rw,no_root_squash,sync)
```

### vSAN Design

**Deployment options:**

| Type | Minimum Hosts | Use Case |
|------|---------------|----------|
| Original Storage Architecture (OSA) | 3 | Traditional vSAN |
| Express Storage Architecture (ESA) | 3 | NVMe-optimized |
| 2-node ROBO | 2 + witness | Remote/branch office |
| Stretched cluster | 2 sites + witness | Metro distance HA |

**Disk group design (OSA):**
```
Cache tier: 10% of capacity tier
Write buffer: ~70% of cache (write-intensive)
Read cache: ~30% of cache
```

**Storage policies:**

| Policy | Description | Capacity Impact |
|--------|-------------|-----------------|
| FTT=1, RAID-1 | Mirror, 1 failure | 2x |
| FTT=1, RAID-5 | Erasure coding | 1.33x |
| FTT=2, RAID-1 | Mirror, 2 failures | 3x |
| FTT=2, RAID-6 | Erasure coding | 1.5x |

**Stripe width:**
- Default: 1 (no striping)
- Increase for high-IOPS workloads
- Max: Number of fault domains - 1

## Storage I/O Control (SIOC)

Balances datastore access during contention:

**Enable when:**
- Multiple hosts share datastore
- Mixed priority workloads
- Latency-sensitive VMs present

**Configuration:**
```
Threshold: Default 30ms (trigger point)
Shares: Per-VM priority during throttling
```

**SIOC v2 (IO Filters):**
- Per-VMDK policies
- More granular than datastore-level
- Integrated with SPBM

## Multipathing

### Path Selection Policies

| Policy | Behavior | Best For |
|--------|----------|----------|
| Fixed | Single preferred path | Active/passive arrays |
| MRU (Most Recently Used) | Stick to current path | Active/passive arrays |
| Round Robin | Rotate paths | Active/active arrays |
| Fixed-AP | Fixed with auto-failover | Active/passive with failover |

**Round Robin tuning:**
```
# Default: 1000 I/Os before switch
esxcli storage nmp psp roundrobin deviceconfig set \
  -d <device> --iops=1 --type=iops
```

### ALUA (Asymmetric Logical Unit Access)

ALUA-aware arrays report path states:
- **Active Optimized**: Best performance
- **Active Non-Optimized**: Functional, higher latency
- **Standby**: Failover path

ESXi prefers Active Optimized paths automatically.

## Storage Performance

### Key Metrics

| Metric | Description | Warning |
|--------|-------------|---------|
| DAVG | Device average latency | >20ms |
| KAVG | Kernel average latency | >20ms |
| GAVG | Guest observed latency | >30ms |
| QAVG | Queue average latency | >10ms |
| CMDS/s | Commands per second | Context dependent |

**Relationship:**
```
GAVG = KAVG + QAVG
KAVG = DAVG + driver/queue time
```

### Troubleshooting Flow

1. **High DAVG**: Storage array issue
2. **High KAVG, low DAVG**: HBA/driver/path issue
3. **High QAVG**: Queue depth saturation
4. **High GAVG, low KAVG**: Guest I/O pattern issue

### Queue Depth Tuning

```bash
# View current queue depth
esxcli storage core device list -d <device> | grep "Queue"

# Adjust (requires reboot)
esxcli system module parameters set -m <driver> -p <parameter>=<value>
```

## VMDK Best Practices

### VMDK Placement

| Workload | Recommended Type | Notes |
|----------|------------------|-------|
| Database (OLTP) | Thick Eager | Consistent performance |
| File server | Thin | Capacity efficiency |
| Web server | Thick Lazy | Balance |
| FT-protected | Thick Eager | Required |

### Multi-VMDK Design

Separate VMDKs for:
- OS (C:) - Independent backup/recovery
- Applications - Lifecycle management
- Data - Performance isolation
- Logs - I/O pattern isolation

### Changed Block Tracking (CBT)

Required for incremental backups:
- Enabled per-VMDK
- Tracks changed blocks since snapshot
- Reset on storage vMotion

```
# Enable via API or extraConfig
ctkEnabled = "TRUE"
```
