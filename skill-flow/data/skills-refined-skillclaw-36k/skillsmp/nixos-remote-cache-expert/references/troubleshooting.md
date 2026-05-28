# Troubleshooting Guide

Comprehensive troubleshooting guide for NixOS remote cache servers. Organized by symptom → diagnosis → solution.

## Table of Contents
- [Cache Server Not Starting](#cache-server-not-starting)
- [Clients Can't Reach Cache](#clients-cant-reach-cache)
- [Poor Performance](#poor-performance)
- [Build Failures](#build-failures)
- [Storage Issues](#storage-issues)
- [Network Problems](#network-problems)

## Cache Server Not Starting

### Symptom: `systemctl status nix-serve` shows failed/inactive

**Diagnosis:**
```bash
journalctl -u nix-serve -n 50
```

**Common causes & solutions:**

1. **Missing secret key**
   ```
   Error: /var/cache-priv-key.pem not found
   ```
   
   **Solution:**
   ```bash
   sudo nix-store --generate-binary-cache-key cache-key /var/cache-priv-key.pem cache-pub-key.pem
   sudo chown nix-serve:nix-serve /var/cache-priv-key.pem
   sudo chmod 600 /var/cache-priv-key.pem
   ```

2. **Port already in use**
   ```
   Error: Address already in use (port 5000)
   ```
   
   **Solution:**
   ```bash
   # Check what's using the port
   sudo ss -tlnp | grep :5000
   
   # Either kill that process or change nix-serve port
   services.nix-serve.port = 5001;  # In configuration.nix
   ```

3. **Permissions issue**
   ```
   Error: Permission denied
   ```
   
   **Solution:**
   ```bash
   # Fix ownership of key file
   sudo chown nix-serve:nix-serve /var/cache-priv-key.pem
   
   # Ensure nix-serve user exists
   id nix-serve  # Should return user info
   ```

## Clients Can't Reach Cache

### Symptom: Client shows "unable to reach cache server"

**Quick diagnosis:**
```bash
# From client machine
ping 10.255.255.1  # Test basic connectivity
curl http://10.255.255.1:5000/nix-cache-info  # Test cache endpoint
```

**Troubleshooting tree:**

1. **No ping response**
   
   Problem: Network layer issue
   
   **Check on server:**
   ```bash
   ip addr show  # Verify IP configured
   ping 10.255.255.2  # Try reverse ping
   ```
   
   **Check on client:**
   ```bash
   ip addr show  # Verify client IP
   ip route  # Check routing table
   ```
   
   **Common fixes:**
   - Cable not connected properly (check both ends)
   - Wrong network interface configured
   - IP addresses in wrong subnet
   
   **Nuclear option:**
   ```bash
   # On server
   sudo ip addr add 10.255.255.1/24 dev eth0
   sudo ip link set eth0 up
   
   # On client
   sudo ip addr add 10.255.255.2/24 dev eth0
   sudo ip link set eth0 up
   ```

2. **Ping works, but curl fails**
   
   Problem: Firewall or service issue
   
   **Check firewall (server):**
   ```bash
   sudo iptables -L -n | grep 5000  # Should show ACCEPT rule
   sudo nft list ruleset | grep 5000  # For nftables
   ```
   
   **Check service:**
   ```bash
   systemctl status nix-serve
   ss -tlnp | grep :5000  # Should show LISTEN
   ```
   
   **Fix firewall:**
   ```nix
   # In configuration.nix
   networking.firewall.allowedTCPPorts = [ 5000 ];
   ```

3. **Curl works, but Nix doesn't use cache**
   
   Problem: Client configuration
   
   **Check client config:**
   ```bash
   nix show-config | grep substituters
   ```
   
   Should include: `http://10.255.255.1:5000`
   
   **Fix:**
   ```nix
   # In configuration.nix
   nix.settings.substituters = [
     "http://10.255.255.1:5000"
     "https://cache.nixos.org"
   ];
   ```
   
   **Test manually:**
   ```bash
   nix-store --realise /nix/store/some-path --option substituters http://10.255.255.1:5000
   ```

## Poor Performance

### Symptom: Slow cache serving or builds

**Diagnosis checklist:**

1. **Check system resources**
   ```bash
   htop  # Overall system load
   iotop  # Disk I/O
   iftop  # Network usage (or use scripts/monitor_performance.sh)
   ```

2. **Check cache hit rate**
   ```bash
   # Monitor nix-daemon logs for cache hits vs misses
   journalctl -u nix-daemon -f | grep -E "copying|fetching|building"
   ```

**Performance issues by symptom:**

### Slow network transfers

**Diagnosis:**
```bash
# Test network speed
iperf3 -s  # On server
iperf3 -c 10.255.255.1  # On client

# Expected: 900+ Mbps for gigabit connection
```

**If slow (<100 Mbps):**
- Check cable quality (cat5e or better)
- Verify gigabit link speed:
  ```bash
  ethtool eth0 | grep Speed
  # Should show: Speed: 1000Mb/s
  ```
- Check for autonegotiation issues:
  ```bash
  sudo ethtool -s eth0 speed 1000 duplex full autoneg off
  ```

**If moderate (100-500 Mbps):**
- CPU bottleneck on old hardware
- Apply kernel tuning from hardware-optimization.md
- Check for high CPU usage during transfers

### Slow builds

**Diagnosis:**
```bash
# Check what's building
nix-store --query --deriver /nix/store/*-building

# Monitor build progress
tail -f /nix/var/log/nix/drvs/*/*.log
```

**Common causes:**

1. **Memory pressure**
   ```bash
   free -h  # Check available RAM
   dmesg | grep -i "out of memory"  # Check for OOM
   ```
   
   **Fix:** Reduce max-jobs, enable zram

2. **CPU saturation**
   ```bash
   mpstat 1  # All cores at 100%?
   ```
   
   **Fix:** Reduce max-jobs × cores

3. **Disk I/O bottleneck**
   ```bash
   iostat -x 1  # Check %util
   ```
   
   **Fix:** Upgrade to SSD, reduce concurrent builds

### High latency (cache hits still slow)

**Diagnosis:**
```bash
# Measure actual latency
time curl -s http://10.255.255.1:5000/nix-cache-info > /dev/null

# Should be < 10ms for local network
```

**If high (>50ms):**
- Check for network congestion
- Verify direct connection (not going through router)
- Check DNS resolution (should use IP, not hostname)

## Build Failures

### Symptom: Builds fail with "killed" or "error 137"

**Cause:** Out of memory

**Solution:**
```nix
nix.settings.max-jobs = 1;  # Reduce parallelism
```

**Temporary fix:**
```bash
# Add swap immediately
sudo dd if=/dev/zero of=/swapfile bs=1M count=4096
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Symptom: "error: unable to start build process"

**Cause:** nix-daemon issues

**Solution:**
```bash
sudo systemctl restart nix-daemon
# Check logs
journalctl -u nix-daemon -n 50
```

### Symptom: Builds succeed on other machines but fail on cache server

**Cause:** Hardware limitations or missing dependencies

**Workaround:**
Build on more capable machine and copy to cache:
```bash
# On capable machine
nix-build some-package
nix copy --to http://10.255.255.1:5000 ./result
```

## Storage Issues

### Symptom: "no space left on device"

**Immediate fix:**
```bash
# Emergency garbage collection
sudo nix-collect-garbage -d

# Free up space immediately
sudo nix-store --gc --max-freed 10G
```

**Diagnosis:**
```bash
df -h /
du -sh /nix/store
```

**Long-term solution:**
```nix
# Aggressive garbage collection
nix.gc = {
  automatic = true;
  dates = "daily";
  options = "--delete-older-than 7d";
};

# Set storage limits
nix.settings = {
  min-free = ${10 * 1024 * 1024 * 1024};
  max-free = ${25 * 1024 * 1024 * 1024};
};
```

### Symptom: /nix/store growing rapidly

**Diagnosis:**
```bash
# Find largest store paths
du -sh /nix/store/* | sort -h | tail -20
```

**Solutions:**
1. Reduce cache retention period
2. Enable auto-optimise-store
3. Consider dedicated partition for /nix

## Network Problems

### Symptom: Intermittent connectivity

**Diagnosis:**
```bash
# Long-term ping test
ping -i 0.2 10.255.255.1 | ts  # Timestamp each ping

# Check for packet loss
ping -c 1000 10.255.255.1 | tail -2
```

**Common causes:**
1. **Bad cable:** Replace with known-good cable
2. **Interface flapping:**
   ```bash
   dmesg | grep eth0  # Look for link up/down messages
   ```
3. **Autonegotiation issues:**
   ```bash
   sudo ethtool -s eth0 autoneg off speed 1000 duplex full
   ```

### Symptom: Connection drops under load

**Diagnosis:**
```bash
# Stress test network
iperf3 -c 10.255.255.1 -t 300  # 5-minute test
```

**If drops occur:**
- Check cable quality (use cat6 or better)
- Verify both NICs support gigabit
- Check for overheating (touch NIC)
- Test with different NIC or port

## Emergency Recovery

### Cache server completely unresponsive

**Recovery procedure:**

1. **Physical access to server**
   - Check if machine is running (LEDs, fans)
   - Try keyboard input (Ctrl+Alt+F2 for console)

2. **If frozen:**
   ```bash
   # Magic SysRq keys (if enabled)
   Alt+SysRq+R  # Take back keyboard
   Alt+SysRq+E  # Terminate all processes
   Alt+SysRq+I  # Kill all processes
   Alt+SysRq+S  # Sync disks
   Alt+SysRq+U  # Unmount filesystems
   Alt+SysRq+B  # Reboot
   ```

3. **After reboot:**
   ```bash
   # Check system logs
   journalctl -b -1  # Previous boot
   dmesg  # Hardware errors
   
   # Check filesystem
   sudo fsck -y /dev/sda1  # If needed
   ```

### Corrupted Nix store

**Verification:**
```bash
sudo nix-store --verify --check-contents
```

**Repair:**
```bash
# Repair store
sudo nix-store --repair --verify --check-contents

# If severe corruption, rebuild from scratch
sudo rm -rf /nix/store/*
sudo nixos-rebuild switch
```

## Diagnostic Commands Cheatsheet

```bash
# System health
htop                    # CPU, RAM, processes
iostat -x 1            # Disk I/O
iftop                  # Network traffic
dmesg                  # Kernel messages

# Network
ip addr show           # IP configuration
ip route               # Routing table
ss -tlnp               # Listening ports
ping <ip>              # Connectivity
traceroute <ip>        # Network path
ethtool eth0           # Interface details

# Nix
nix-store --verify     # Store integrity
nix-store --gc         # Garbage collection
journalctl -u nix-daemon  # Daemon logs
nix show-config        # Current configuration

# Cache server
systemctl status nix-serve
journalctl -u nix-serve
curl http://localhost:5000/nix-cache-info

# Storage
df -h                  # Disk usage
du -sh /nix/store     # Store size
ncdu /nix/store       # Interactive disk usage
```

## When to Give Up (Realistic Assessment)

Some limitations can't be overcome with configuration:

**Hardware is too limited:**
- <2GB RAM: Can't build most packages reliably
- Single-core CPU: Builds will be painfully slow
- <50GB storage: Not enough for useful cache

**Solution:** Accept limitations and:
1. Use as simple proxy/cache only
2. Build on another machine, copy to cache
3. Prioritize Black Friday upgrade

**Network is fundamentally broken:**
- WiFi with constant interference
- 10/100 Mbps old switch in path
- Physical damage to NIC

**Solution:** Direct cable connection or new hardware

**Remember:** It's okay to say "this hardware can't do X" and propose alternatives. Being realistic prevents wasted time and frustration.
