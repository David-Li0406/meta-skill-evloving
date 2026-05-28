# Hardware Optimization Reference

This document provides detailed optimization strategies for NixOS cache servers across different hardware profiles.

## Table of Contents
- [Hardware Profiles](#hardware-profiles)
- [RAM Optimization](#ram-optimization)
- [CPU Optimization](#cpu-optimization)
- [Storage Optimization](#storage-optimization)
- [Network Optimization](#network-optimization)
- [Black Friday Upgrade Planning](#black-friday-upgrade-planning)

## Hardware Profiles

### Profile: Minimal (< 4GB RAM, 2 cores)
**Reality Check:** This is tight but workable for a local cache server serving 1-2 clients.

**Critical Optimizations:**
- `nix.settings.max-jobs = 1` - Only one build at a time
- `nix.settings.cores = 1` - Single-threaded builds
- Enable zram compression (50% of RAM)
- Aggressive garbage collection (7-day retention)
- `vm.swappiness = 10` - Minimize swap usage
- Consider tmpfs for /tmp with size limit

**Expected Performance:**
- Cache hits: Excellent (network-bound, not CPU)
- Cache misses: Slow (single-threaded builds)
- Concurrent clients: 2-3 maximum

### Profile: Low-End (4-6GB RAM, 2-4 cores)
**Reality Check:** This is your current setup - very reasonable for home use.

**Optimizations:**
- `nix.settings.max-jobs = 2` - Two concurrent builds
- `nix.settings.cores = 1-2` - Balance between jobs
- Optional zram (25% of RAM)
- 14-day cache retention
- `vm.swappiness = 5`
- BBR congestion control for network

**Expected Performance:**
- Cache hits: Excellent
- Cache misses: Moderate (parallel builds help)
- Concurrent clients: 4-6 comfortable

### Profile: Mid-Range (8-16GB RAM, 4-8 cores)
**Reality Check:** Ideal sweet spot for home/small office cache server.

**Optimizations:**
- `nix.settings.max-jobs = 4-6`
- `nix.settings.cores = 2`
- No zram needed
- 30-day cache retention
- `vm.swappiness = 1`
- Consider NVMe for /nix/store if available

**Expected Performance:**
- Cache hits: Excellent
- Cache misses: Fast (parallel builds)
- Concurrent clients: 10+ no problem

### Profile: High-End (16GB+ RAM, 8+ cores)
**Reality Check:** Overkill for home use, but enables advanced workflows.

**Optimizations:**
- `nix.settings.max-jobs = auto` - Let Nix decide
- `nix.settings.cores = 4`
- 60-day cache retention
- Consider distributed builds
- Enable Nix build sandboxing
- Consider dedicated cache partition

**Expected Performance:**
- Cache hits: Excellent
- Cache misses: Very fast
- Concurrent clients: Effectively unlimited

## RAM Optimization

### Understanding Nix Memory Usage

**Build-time memory:**
- Average package: 500MB - 1GB
- Large packages (Firefox, Chromium): 4GB - 8GB
- Kernel builds: 2GB - 4GB

**Cache-serving memory:**
- nix-serve daemon: ~50MB base
- Per-connection overhead: ~10MB
- Total for serving: Usually < 500MB

### Low Memory Strategies

1. **ZRAM Compression**
```nix
zramSwap = {
  enable = true;
  memoryPercent = 50;  # Compress up to 50% of RAM
  algorithm = "zstd";  # Fast, good compression ratio
};
```

**Real-world impact:**
- 4GB physical RAM → ~6GB effective RAM
- CPU overhead: 5-10%
- Worth it for systems < 8GB

2. **Build Job Limiting**
```nix
nix.settings = {
  max-jobs = 1;  # Prevent OOM during builds
  cores = 1;     # Single-threaded builds use less memory
};
```

3. **Swap Configuration**
```nix
swapDevices = [{
  device = "/swapfile";
  size = 8192;  # 8GB swap for 4GB RAM system
}];

boot.kernel.sysctl = {
  "vm.swappiness" = 10;  # Use swap only when critical
  "vm.vfs_cache_pressure" = 50;  # Keep cache aggressive
};
```

### Memory Monitoring

**Warning signs:**
- `free -h` shows < 500MB available consistently
- `journalctl -u nix-daemon` shows OOM kills
- Builds failing with "killed" status

**Commands:**
```bash
# Real-time memory pressure
watch -n 1 'free -h'

# Track which builds use most memory
journalctl -u nix-daemon | grep "killed"

# Check for OOM events
dmesg | grep -i "out of memory"
```

## CPU Optimization

### Understanding Build Parallelism

**max-jobs vs cores:**
- `max-jobs`: How many packages to build simultaneously
- `cores`: Threads per package build

**Rule of thumb:**
- Total threads = max-jobs × cores
- Keep < total CPU cores to avoid thrashing

### Strategies by Core Count

**2 cores:**
```nix
max-jobs = 1;
cores = 2;  # Let single build use both cores
```

**4 cores:**
```nix
max-jobs = 2;
cores = 2;  # Two builds, each with 2 threads
```

**8+ cores:**
```nix
max-jobs = 4;
cores = 2;  # Four builds with 2 threads each
```

### CPU Affinity (Advanced)

For dedicated cache servers, pin nix-daemon to specific cores:

```nix
systemd.services.nix-daemon = {
  serviceConfig = {
    CPUAffinity = "0-3";  # Use first 4 cores only
  };
};
```

This leaves remaining cores for cache serving and system tasks.

## Storage Optimization

### Auto-Optimization
```nix
nix.settings.auto-optimise-store = true;
```

**What it does:**
- Hardlinks identical files in /nix/store
- Typical savings: 20-30% on well-used systems
- CPU cost: Minimal (runs during builds)

### Garbage Collection

**Aggressive (< 100GB storage):**
```nix
nix.gc = {
  automatic = true;
  dates = "daily";
  options = "--delete-older-than 7d";
};

nix.settings = {
  min-free = ${10 * 1024 * 1024 * 1024};  # Keep 10GB free
  max-free = ${25 * 1024 * 1024 * 1024};  # GC when > 25GB used
};
```

**Moderate (100-250GB):**
```nix
nix.gc = {
  automatic = true;
  dates = "weekly";
  options = "--delete-older-than 14d";
};
```

**Conservative (> 250GB):**
```nix
nix.gc = {
  automatic = true;
  dates = "monthly";
  options = "--delete-older-than 30d";
};
```

### Storage Performance

**Filesystem considerations:**
- ext4: Solid default, proven
- btrfs: Compression can help (compress=zstd)
- xfs: Better for very large stores (> 1TB)

**Mount options:**
```nix
fileSystems."/nix" = {
  options = [ "noatime" "nodiratime" ];  # Reduce write overhead
};
```

## Network Optimization

### Direct Connection (RJ45) - HIGHLY RECOMMENDED

**Advantages:**
- Latency: 0.1-0.3ms (vs 1-5ms via switch)
- Bandwidth: Full link speed, no contention
- Isolation: No interference from other network traffic
- Simplicity: Fewer failure points

**Setup:**
```nix
# Server: 10.255.255.1/24
# Client: 10.255.255.2/24
```

### Kernel Network Tuning

```nix
boot.kernel.sysctl = {
  # TCP buffer sizes (important for large transfers)
  "net.core.rmem_max" = 134217728;  # 128MB receive buffer
  "net.core.wmem_max" = 134217728;  # 128MB send buffer
  
  # TCP window scaling
  "net.ipv4.tcp_rmem" = "4096 87380 67108864";  # min, default, max
  "net.ipv4.tcp_wmem" = "4096 65536 67108864";
  
  # Congestion control (BBR is superior for local networks)
  "net.ipv4.tcp_congestion_control" = "bbr";
  "net.core.default_qdisc" = "fq";
  
  # Connection tracking (increase for multiple clients)
  "net.netfilter.nf_conntrack_max" = 131072;
};
```

**Why BBR?**
- Better throughput on local networks
- More efficient than default CUBIC
- Especially good for cache transfers (bursty traffic)

### HTTP Connection Pooling

```nix
nix.settings.http-connections = 25;  # Default is 25, good for local
```

For gigabit direct connection, can increase to 50.

## Black Friday Upgrade Planning

### Priority Matrix

**Highest Impact:**
1. **RAM upgrade** (4GB → 8GB or 16GB)
   - Cost: $30-60
   - Impact: Massive - enables parallel builds
   - ROI: Excellent

2. **SSD upgrade** (if using HDD)
   - Cost: $40-80 for 500GB
   - Impact: 5-10x faster store operations
   - ROI: Excellent

**Medium Impact:**
3. **CPU upgrade** (if motherboard supports)
   - Cost: Varies ($50-150)
   - Impact: Faster builds, more parallelism
   - ROI: Good if RAM is already adequate

**Lower Impact:**
4. **Network card** (if doing WiFi currently)
   - Cost: $15-30 for gigabit NIC
   - Impact: Stable, faster transfers
   - ROI: Good, but direct cable is sufficient

### Recommended Upgrades by Budget

**$50 budget:**
- 8GB RAM stick (single)
- Direct RJ45 cable (cat6)

**$100 budget:**
- 16GB RAM (2x8GB if dual-channel)
- 500GB SSD for /nix/store

**$150+ budget:**
- 16GB RAM
- 1TB NVMe SSD
- Better CPU if motherboard compatible

### Benchmark Targets

**Current setup (4GB RAM, Pentium):**
- Cache hit serve: < 1s for typical package
- Small package build: 5-10 min
- Large package build: 30-60 min

**After upgrade (16GB RAM, modern CPU):**
- Cache hit serve: < 0.5s
- Small package build: 2-5 min
- Large package build: 10-20 min

### Future-Proofing

**Consider:**
- Motherboard with expansion options
- M.2 slot for future NVMe
- Dual-channel RAM support
- At least 4 SATA ports for storage expansion

**Don't overkill:**
- RGB lighting (zero performance benefit)
- High-end CPU (diminishing returns for cache server)
- More than 32GB RAM (unnecessary for home use)
