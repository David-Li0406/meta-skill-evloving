# Performance Troubleshooting Guide

## Methodology

### Troubleshooting Flow

```
1. Identify symptoms (user-reported or alert)
2. Determine scope (single VM, host, cluster, entire infrastructure)
3. Isolate resource (CPU, memory, storage, network)
4. Analyze metrics (esxtop, vCenter, vROps)
5. Identify root cause
6. Apply fix
7. Verify resolution
```

### Data Collection

**Real-time analysis:**
```bash
esxtop
```

**Historical batch:**
```bash
esxtop -b -d 5 -n 720 > esxtop_1hr.csv
```

**vm-support bundle:**
```bash
vm-support
```

## CPU Troubleshooting

### Symptom: VM is Slow

**Step 1: Check CPU Ready (%RDY)**

```
esxtop > c (CPU view)
Look at %RDY column for the VM
```

| %RDY | Interpretation | Action |
|------|----------------|--------|
| <2% | Normal | Look elsewhere |
| 2-5% | Elevated | Monitor, consider right-sizing |
| 5-10% | High | Reduce oversubscription |
| >10% | Critical | Immediate action needed |

**Step 2: Check Co-Stop (%CSTP)**

| %CSTP | Interpretation | Action |
|-------|----------------|--------|
| <1% | Normal | No issue |
| 1-3% | Elevated | Consider reducing vCPUs |
| >3% | High | Reduce vCPU count |

**Step 3: Check %MLMTD**

Non-zero = VM hitting resource limit. Raise limit or remove it.

### Symptom: Entire Host Slow

**Check host CPU usage:**
```
esxtop > c
Look at PCPU USED% line
```

If >80%:
- Host is CPU-saturated
- Migrate VMs away or add capacity

**Check power management:**
```
esxcli hardware cpu global get
```

If P-states active, VMs may see latency during frequency scaling.

### CPU Affinity Investigation

```bash
# Check VM CPU affinity
vim-cmd vmsvc/get.summary <vmid> | grep affinity

# View all pinned VMs
esxcli hardware cpu global get
```

## Memory Troubleshooting

### Symptom: VM Memory Pressure

**Step 1: Check balloon activity**

```
esxtop > m (memory view)
MCTLSZ column = balloon target (MB)
```

If MCTLSZ > 0:
- Host is requesting memory back
- Check if VMware Tools is running in guest

**Step 2: Check swap activity**

```
SWCUR = Current swap usage (MB)
SWR/s = Swap read rate
SWW/s = Swap write rate
```

Active swapping = severe performance issue.

**Step 3: Check compression**

```
CACHEUSD = Compressed cache (MB)
```

High compression indicates memory pressure.

### Symptom: Host Memory Pressure

**Check host memory state:**
```bash
esxcli system stats memory get
```

Look at "State": High (good), Soft, Hard, Low (bad)

**Memory pressure hierarchy:**
```
High → Soft → Hard → Low
      TPS    Balloon+Compress    Swap
```

### NUMA Imbalance

**Symptoms:**
- Inconsistent VM performance
- Some VMs faster than others on same host

**Investigation:**
```
esxtop > m
N = NUMA home node
NLOC% = Locality (100% = all memory on home node)
```

Low NLOC% = remote memory access → higher latency.

## Storage Troubleshooting

### Symptom: VM Disk Latency

**Step 1: Check latency in esxtop**

```
esxtop > v (disk VM view)
```

| Metric | Description | Warning |
|--------|-------------|---------|
| GAVG | Guest observed latency | >30ms |
| KAVG | Kernel latency | >20ms |
| DAVG | Device latency | >20ms |
| QAVG | Queue latency | >10ms |

**Step 2: Determine bottleneck location**

```
If DAVG high, KAVG ≈ DAVG:
→ Storage array issue

If KAVG >> DAVG:
→ ESXi-side issue (driver, queue, path)

If GAVG >> KAVG:
→ Guest-side I/O pattern issue

If QAVG high:
→ Queue depth saturation
```

**Step 3: Check path status**

```bash
esxcli storage nmp device list
```

Look for:
- Dead paths
- Path states (Active, Standby, Dead)
- Round-robin working

### Symptom: Entire Datastore Slow

**Check Storage I/O Control:**
```
esxtop > u (disk device view)
Look for throttling indicators
```

**Check queue depth:**
```
ACTV = Active commands
QUED = Queued commands
```

If QUED consistently > 0:
- Queue depth saturation
- Consider increasing queue depth or spreading workload

### VMFS Locking Issues

**Symptoms:**
- VM operations hang
- Slow power operations

**Investigation:**
```bash
# Check lock status
vmkfstools -D /vmfs/volumes/<datastore>/<vm>/<file>.vmdk
```

**Common causes:**
- Stale .lck files
- Hung vMotion
- Backup software

## Network Troubleshooting

### Symptom: Network Packet Drops

**Check in esxtop:**
```
esxtop > n (network view)
%DRPTX = Transmit drops
%DRPRX = Receive drops
```

| Drop Rate | Action |
|-----------|--------|
| <0.1% | Usually acceptable |
| 0.1-1% | Investigate |
| >1% | Fix required |

**Common causes:**
- Ring buffer exhaustion
- vSwitch oversubscription
- Physical NIC issues

### Symptom: High Network Latency

**Check vmkernel route:**
```bash
esxcli network ip route list
```

**Check physical NIC:**
```bash
esxcli network nic stats get -n vmnic0
```

Look for:
- Errors
- CRC errors
- Collisions (shouldn't happen on switched networks)

### vSwitch vs dvSwitch Issues

**Standard vSwitch:**
- Per-host configuration
- Check consistency across hosts

**Distributed vSwitch:**
- Single configuration
- Check uplink status per host

```bash
esxcli network vswitch dvs vmware list
```

## Cluster-Level Issues

### DRS Not Migrating VMs

**Check:**
1. DRS enabled and automation level appropriate
2. vMotion network functional
3. No affinity rules blocking moves
4. Compatible EVC mode

```
vCenter > Cluster > Monitor > DRS > Recommendations
```

### HA Issues

**Check cluster health:**
```
vCenter > Cluster > Monitor > vSphere HA
```

**Check host isolation:**
```bash
# On host
esxcli system settings advanced list -o /Misc/HotEjectDisks
```

### vMotion Failures

**Common causes:**
- CPU incompatibility → Enable EVC
- Network issues → Check vMotion VMkernel
- Storage not shared → Verify datastore access
- VM state (CD connected, USB passthrough)

```bash
# Check vMotion compatibility
vim-cmd vmsvc/vmotion.check <vmid> <dest_host>
```

## Tools Summary

### esxtop Quick Keys

| Key | View | Key Columns |
|-----|------|-------------|
| c | CPU | %RDY, %CSTP, %USED, %MLMTD |
| m | Memory | MCTLSZ, SWCUR, %ACTV, NLOC% |
| n | Network | %DRPTX, %DRPRX, MbTX, MbRX |
| d | Disk Adapter | CMDS/s, READS/s, WRITES/s |
| u | Disk Device | DAVG, KAVG, GAVG |
| v | Disk VM | GAVG, per-VM I/O |

### vscsiStats (Storage Deep Dive)

```bash
# Enable
vscsiStats -s -w <world_id>

# Collect (run workload)
vscsiStats -l -w <world_id>

# Histogram
vscsiStats -p latency -w <world_id>
```

### Log Locations

| Log | Path | Use |
|-----|------|-----|
| vmkernel | /var/log/vmkernel.log | Kernel events |
| hostd | /var/log/hostd.log | Host daemon |
| vpxa | /var/log/vpxa.log | vCenter agent |
| vmware.log | <VM folder>/vmware.log | Per-VM events |
| fdm | /var/log/fdm.log | HA agent |
