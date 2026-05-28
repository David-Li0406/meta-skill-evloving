# CPU Scheduler Deep Dive

## VMkernel Scheduler Architecture

The VMkernel CPU scheduler uses a proportional-share algorithm with multiple scheduling contexts:

### Scheduling Contexts

1. **World**: Basic schedulable entity (VM vCPU, VMkernel thread, etc.)
2. **Resource Pool**: Group of worlds sharing resources
3. **Cell**: NUMA node-aware scheduling domain

### Scheduler Algorithm

The scheduler uses **Borrowed Virtual Time (BVT)** algorithm:

```
Effective Virtual Time = Actual Virtual Time - Warp (based on shares/reservations)
```

Worlds with lower effective virtual time get scheduled first.

### Co-scheduling (Relaxed Co-scheduling)

For SMP VMs, the scheduler attempts to run sibling vCPUs together but allows "skew":

- **Skew threshold**: Maximum time difference between sibling vCPUs
- **Co-stop**: When skew exceeds threshold, faster vCPUs are halted
- Default skew threshold: ~4ms

**Implications:**
- VMs with many vCPUs relative to workload waste cycles in co-stop
- Right-size vCPUs to actual parallel thread count needed

### NUMA Scheduling

ESXi is NUMA-aware and tries to:

1. Keep VM memory and vCPUs on same NUMA node
2. Migrate VMs to less loaded NUMA nodes
3. Respect NUMA home node for memory allocation

**NUMA-related settings:**
```
Numa.PreferHT = 1  # Prefer hyperthreads on same NUMA node
Numa.RebalanceEnable = 1  # Enable NUMA rebalancing
Numa.RebalancePeriod = 2000  # Rebalance check interval (ms)
```

### CPU Shares Calculation

During contention, CPU time is allocated proportionally to shares:

| Level | Shares per vCPU |
|-------|-----------------|
| Low | 500 |
| Normal | 1000 |
| High | 2000 |

**Example**: Two 4-vCPU VMs, one High (8000 total), one Low (2000 total)
- High VM gets: 8000/(8000+2000) = 80%
- Low VM gets: 2000/(8000+2000) = 20%

### Reservations and Limits

**Reservations:**
- Guarantee minimum MHz
- Scheduler won't start VMs if reservation can't be met
- Admission control considers reservations

**Limits:**
- Cap maximum MHz
- VM is throttled when hitting limit
- Shows as %MLMTD in esxtop

### Hyperthreading Considerations

With HT enabled:
- Each logical processor (HT) is a schedulable pCPU
- Core co-scheduling: Scheduler aware of HT pairs
- HT efficiency: ~1.25x single thread, not 2x

**HT sharing modes:**
- None: vCPU gets whole core
- Any: vCPU can share with any other vCPU
- Internal: vCPU only shares with same VM's vCPUs

### Advanced Settings

```
# Scheduler parameters (Advanced Settings)
Cpu.HTWholeCoreThreshold = 50  # Minimum %busy before HT sharing
Cpu.CreditAgePeriod = 3000  # Credit aging period (ms)
Cpu.CreditBorrowMin = 50  # Minimum credits to borrow
```

## Latency-Sensitive Workloads

For VMs requiring consistent low latency:

1. **Latency sensitivity = High**
   - Exclusive pCPU scheduling
   - No HT sharing
   - Memory pre-reservation

2. **CPU affinity** (use sparingly)
   - Pins vCPUs to specific pCPUs
   - Breaks DRS, complicates HA
   - Only for extreme requirements

3. **Power management = High Performance**
   - Disables CPU frequency scaling
   - All cores at max frequency

## Monitoring Scheduler Health

### Key esxtop Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| %RDY | Wait time for pCPU | <5% |
| %CSTP | Co-stop time | <3% |
| %MLMTD | Limited by resource limit | 0% |
| %SWPWT | Waiting on swapped memory | 0% |
| %WAIT | I/O and idle wait | Varies |
| %USED | Actual CPU consumed | Context dependent |

### Calculating Real CPU Demand

```
True Demand = %USED + %RDY + %CSTP
```

If True Demand >> %USED, the VM is CPU-constrained.

### Batch Mode esxtop

For historical analysis:
```bash
esxtop -b -d 5 -n 100 > esxtop.csv
```
- `-b`: Batch mode
- `-d 5`: 5-second interval
- `-n 100`: 100 iterations
