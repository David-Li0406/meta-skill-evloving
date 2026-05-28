# Memory Sizing and Management

## Memory Allocation Model

ESXi uses a four-level memory allocation model:

```
Physical RAM → Host Memory → VM Configured Memory → Guest Active Memory
```

### Memory States

| State | Description | Overhead Source |
|-------|-------------|-----------------|
| Configured | VM setting | None |
| Granted | Physical pages mapped | Base allocation |
| Active | Recently touched pages | Working set |
| Consumed | Host memory used by VM | Granted + overhead |

### Memory Overhead

Each VM requires additional memory beyond configured:
- **Video RAM**: Overhead for virtual display
- **VMX process**: ~50-100MB per VM
- **Device emulation**: Variable
- **vSphere features**: FT, vMotion buffers

**Rough estimate:**
```
Overhead ≈ 100MB + (VM_RAM_GB × 8MB) + Video_RAM
```

## Memory Reclamation Deep Dive

### Transparent Page Sharing (TPS)

**How it works:**
1. VMkernel hashes all guest pages
2. Identical pages share single physical page
3. Copy-on-write for modifications

**Security considerations:**
- Inter-VM TPS disabled by default (security patches 2014+)
- Intra-VM TPS still active (same VM's pages)
- Enable inter-VM TPS only if security is less critical than density

**TPS settings:**
```
Mem.ShareForceSalting = 2  # 0=inter-VM, 1=off, 2=intra-VM only
```

### Balloon Driver (vmmemctl)

**Operation sequence:**
1. VMkernel signals balloon driver target size
2. Balloon driver allocates memory in guest
3. Guest OS pages out less-used data
4. Balloon driver pins pages, VMkernel reclaims

**Requirements:**
- VMware Tools installed and running
- Guest OS has pagefile/swap configured
- Balloon target < configured RAM

**Monitoring:**
```bash
# In esxtop memory view
MCTLSZ: Balloon target (MB)
MCTL?: Balloon driver status (Y/N)
```

**Balloon limits:**
- Default max: 65% of VM configured RAM
- Can be adjusted per-VM: `sched.mem.maxmemctl`

### Memory Compression

**When triggered:**
- Memory state reaches Hard (2-4% free)
- Page candidates for swap are compressed first
- Achieved ratio determines if compression is used

**Compression cache:**
- Default: 10% of VM memory
- Stores compressed pages
- Faster than swap, slower than RAM (~10% overhead)

**Settings:**
```
Mem.MemZipEnable = 1  # Enable compression
Mem.MemZipMaxPct = 10  # Max compression cache %
```

### Host Swap

**Last resort mechanism:**
- Pages VM memory to .vswp file on datastore
- Severe performance impact (100-1000x latency)
- Configure on fast storage (SSD preferred)

**vswp file:**
- Location: VM's datastore
- Size: Configured RAM - Reservation
- To eliminate: Set reservation = configured memory

## Sizing Guidelines

### Production Workloads

**Conservative (recommended):**
```
Total VM Memory ≤ 80% × Physical RAM
```

Allows:
- ESXi overhead (~2-4GB)
- Headroom for no reclamation
- Burst capacity

### Memory Reservations

**When to use:**
- Critical workloads that can't tolerate ballooning
- Latency-sensitive applications
- Licensing tied to allocated memory

**Implications:**
- Guarantees physical RAM
- Reduces VM density
- Eliminates .vswp file for reserved amount
- Affects HA slot sizing

### Right-sizing VMs

**Identify oversized VMs:**
```
Active Memory / Configured Memory < 50% sustained
```

**Process:**
1. Monitor %ACTV in esxtop over time
2. Check guest OS memory utilization
3. Reduce configured RAM incrementally
4. Verify application performance

### Memory Shares

Similar to CPU, shares determine priority during contention:

| Level | Shares per MB |
|-------|---------------|
| Low | 5 |
| Normal | 10 |
| High | 20 |

## NUMA Memory Considerations

### NUMA Architecture Impact

- Each NUMA node has local memory
- Remote memory access: ~1.5-2x latency
- ESXi tries to keep VM memory on home NUMA node

### Wide VMs (Spanning NUMA Nodes)

VMs larger than single NUMA node:
- Memory split across nodes
- Some remote memory access inevitable
- Consider NUMA client size for VM sizing

**Check NUMA topology:**
```bash
esxcli hardware memory get
vsish -e cat /hardware/numa/node*/properties
```

### vNUMA (Virtual NUMA)

**When exposed:**
- VM > 8 vCPUs or memory > single NUMA node
- Helps guest OS optimize memory allocation

**Settings:**
```
numa.vcpu.min = 8  # Min vCPUs to expose vNUMA
numa.autosize = TRUE  # Auto-calculate topology
```

## Large Pages

ESXi supports multiple page sizes:

| Page Size | Use Case | Benefit |
|-----------|----------|---------|
| 4KB | Default, flexible | Fine-grained allocation |
| 2MB | Large memory VMs | Reduced TLB misses |
| 1GB | Monster VMs | Maximum TLB efficiency |

**Large page handling:**
- ESXi tries to back VMs with large pages
- Can be broken into small pages under pressure
- Monitor with `PSHRD` (pages shared) and page size metrics
