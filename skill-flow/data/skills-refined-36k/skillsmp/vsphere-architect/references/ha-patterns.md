# High Availability Design Patterns

## HA Architecture

### HA Components

1. **FDM Agent**: Runs on each host, handles failure detection
2. **Primary Host**: Elected host managing cluster state
3. **Secondary Hosts**: Backup hosts, can become primary

### Primary Election

Election criteria (in order):
1. Most datastores accessible
2. Highest moref ID (tie-breaker)

**Primary responsibilities:**
- Monitor secondary hosts
- Make restart decisions
- Manage cluster state on datastores

## Admission Control Policies

### Host Failures Cluster Tolerates

**How it works:**
- Calculates "slots" per host
- Reserves N hosts worth of slots

**Slot calculation:**
```
CPU Slot Size = Max(largest_vm_cpu_reservation, 32MHz)
Memory Slot Size = Max(largest_vm_memory_reservation, 128MB) + VM overhead
```

**Capacity calculation:**
```
Total Slots = Sum(floor(host_cpu/cpu_slot) × floor(host_memory/mem_slot))
Reserved Slots = N × (average slots per host)
Available Slots = Total - Reserved
```

**Pros:**
- Predictable capacity reservation
- Clear failover capacity

**Cons:**
- Large VM reservations inflate slot size
- Can waste capacity

**Best practice**: Set consistent reservations or use percentage-based policy.

### Percentage of Cluster Resources

**How it works:**
- Reserves X% of total CPU and Y% of total memory
- Doesn't use slot calculation

**Configuration:**
```
Reserved CPU: 25% (for N+1 with 4 hosts)
Reserved Memory: 25%
```

**Calculation formula:**
```
Percentage = 100 / (Number of hosts) × N failures
```

**Pros:**
- Not affected by VM reservation variations
- More efficient capacity usage

**Cons:**
- Less predictable (percentage of what?)
- Doesn't guarantee specific VM count

### Dedicated Failover Hosts

**How it works:**
- Specific hosts held in standby
- VMs only placed there after failure

**Use cases:**
- Compliance requirements
- License separation
- Predictable failover targets

**Configuration:**
1. Designate failover hosts
2. DRS keeps VMs off these hosts (normally)
3. HA uses them for restart

## Failure Detection

### Host Failure Detection

**Network heartbeat:**
- Primary sends heartbeats every 1 second
- Failure threshold: 15 seconds (configurable)

**Datastore heartbeat:**
- Backup heartbeat mechanism
- Uses datastore files as heartbeat
- Helps distinguish host failure from network isolation

### Network Isolation

**Scenario**: Host can't reach other hosts but is still running

**Detection:**
1. Host loses network heartbeat from primary
2. Host attempts datastore heartbeat
3. If datastore heartbeat succeeds → host isolated, not failed

**Isolation response options:**

| Response | Behavior |
|----------|----------|
| Disabled | Leave VMs running |
| Shutdown | Graceful shutdown, then HA restart elsewhere |
| Power Off | Immediate power off, HA restart elsewhere |

**Recommendation**: "Shutdown" for most cases. "Power Off" if shutdown hangs.

### Isolation Address

**Purpose**: Additional isolation detection

**Default**: Default gateway

**Custom configuration:**
```
das.isolationaddress0 = 10.0.0.1
das.isolationaddress1 = 10.0.0.2
```

### All Paths Down (APD)

**Scenario**: Storage paths unavailable but host running

**APD handling:**
- VM response: Issue events, optional restart
- VMCP (VM Component Protection): Automated response

**APD timeout**: 140 seconds default

### Permanent Device Loss (PDL)

**Scenario**: Array reports device permanently gone

**PDL handling:**
- Immediate HA response
- Restart VMs on other hosts with access

## VM Restart Priority

### Priority Levels

| Priority | Restart Order | Use Case |
|----------|---------------|----------|
| Highest | 1st | Infrastructure (DNS, AD, vCenter) |
| High | 2nd | Critical applications |
| Medium | 3rd (default) | Normal applications |
| Low | 4th | Non-critical workloads |
| Lowest | Last | Dev/test |
| Disabled | Never | Manually managed |

### Restart Orchestration

**Dependencies:**
- VM Orchestration: Delay based on VM readiness
- Condition: VMware Tools heartbeat, custom application heartbeat

**Configuration:**
```
VM A restart → Wait for Tools heartbeat → Then restart VM B
```

## Fault Tolerance (FT)

### FT Architecture

**Components:**
- Primary VM: Active, serving requests
- Secondary VM: Passive, receiving logs
- FT Logging: Continuous state replication

**Network requirements:**
- Dedicated FT logging network
- 10GbE minimum bandwidth
- Low latency (<10ms RTT)

### FT Requirements Checklist

| Requirement | Specification |
|-------------|---------------|
| Disk format | Thick Eager Zeroed |
| Max vCPUs | 8 |
| Max memory | 128GB |
| Compatible hardware | Same CPU family |
| Network | FT logging VMkernel |
| EVC | Recommended (ensures CPU compat) |

### FT vs HA Comparison

| Aspect | HA | FT |
|--------|----|----|
| Downtime | Seconds-minutes | None |
| Resource overhead | Minimal | 2x (duplicate VM) |
| Complexity | Low | High |
| VM limitations | None | Restrictive |
| Use case | General workloads | Zero-downtime critical |

## Design Patterns

### N+1 Design

**Configuration:**
- 4 hosts, tolerate 1 failure
- Each host runs 75% capacity
- 25% headroom for failover

**Admission control:**
```
Host failures: 1
Or Percentage: 25% CPU, 25% memory
```

### N+2 Design

**Configuration:**
- 5+ hosts, tolerate 2 failures
- More resilient for large clusters
- Required for stretched clusters

**Admission control:**
```
Host failures: 2
Or Percentage: 40% (for 5 hosts)
```

### Stretched Cluster HA

**Requirements:**
- vSAN stretched cluster or metro storage
- Witness for quorum
- Site-aware placement

**HA behavior:**
- Site failure: Restart VMs at surviving site
- Witness decides quorum in split-brain

### Edge/ROBO Design

**2-node with witness:**
- Witness provides quorum
- Single host failure tolerated
- No live migration during failure

**HA configuration:**
- Host failures: 1
- Admission control aware of limited capacity

## Monitoring HA Health

### Key Indicators

```
vCenter > Cluster > Monitor > vSphere HA
```

**Check:**
- Cluster status (green/yellow/red)
- Host status (connected, partitioned, isolated)
- Protected VMs count
- Slot information (if using slot policy)

### HA Events

Critical events to monitor:
- `com.vmware.vc.ha.ClusterFailoverResourcesReduced`
- `com.vmware.vc.ha.VmRestartedByHA`
- `com.vmware.vc.ha.HostDeclaredAsDown`
- `com.vmware.vc.ha.HostIsolated`

### Testing HA

**Safe testing:**
1. Enter maintenance mode (tests VM migration)
2. Simulate network isolation (requires lab)
3. Pull storage path (tests APD/PDL)

**Never in production:**
- Hard power-off hosts (risk of data corruption)
- Network disconnect without planning
