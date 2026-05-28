# Best Practices for NixOS Cache Servers

Production-grade best practices for running NixOS cache servers, from home labs to small business deployments.

## Table of Contents
- [Security](#security)
- [Monitoring & Observability](#monitoring--observability)
- [Backup & Recovery](#backup--recovery)
- [Performance Tuning](#performance-tuning)
- [Maintenance](#maintenance)
- [Documentation](#documentation)

## Security

### 1. Cache Signing Keys

**Critical:** Always use signed caches to prevent malicious package injection.

**Key generation:**
```bash
sudo nix-store --generate-binary-cache-key cache-key \
  /var/cache-priv-key.pem \
  cache-pub-key.pem
```

**Best practices:**
- Store private key with restrictive permissions (600)
- Keep backup of private key in secure location
- Share public key with clients via secure channel
- Rotate keys annually or after suspected compromise

**Key storage:**
```bash
# Server
-rw------- 1 nix-serve nix-serve  /var/cache-priv-key.pem

# Client (in configuration.nix)
nix.settings.trusted-public-keys = [
  "cache-key-1:BASE64_ENCODED_PUBLIC_KEY"
];
```

### 2. Network Isolation

**For direct RJ45 connections:**
- Use dedicated subnet (e.g., 10.255.255.0/24)
- No default gateway on cache interface
- Separate from internet-facing networks

**Configuration:**
```nix
networking.interfaces.eth0 = {
  ipv4.addresses = [{
    address = "10.255.255.1";
    prefixLength = 24;
  }];
  # No default gateway - isolated network
};
```

### 3. Firewall Configuration

**Principle:** Minimum exposure, explicit allows.

```nix
networking.firewall = {
  enable = true;
  
  # Default deny
  allowedTCPPorts = [];
  
  # Per-interface rules
  interfaces.eth0 = {
    allowedTCPPorts = [ 5000 ];  # nix-serve only
  };
  
  # Optional: restrict source IPs
  extraCommands = ''
    iptables -A nixos-fw -i eth0 -p tcp --dport 5000 \
      -s 10.255.255.2 -j ACCEPT
    iptables -A nixos-fw -i eth0 -p tcp --dport 5000 -j DROP
  '';
};
```

### 4. Service Hardening

**Systemd security:**
```nix
systemd.services.nix-serve = {
  serviceConfig = {
    # Filesystem isolation
    PrivateTmp = true;
    ProtectSystem = "strict";
    ProtectHome = true;
    ReadWritePaths = [ "/nix/store" ];
    
    # Network isolation
    RestrictAddressFamilies = [ "AF_INET" "AF_INET6" ];
    
    # Privilege restriction
    NoNewPrivileges = true;
    PrivateDevices = true;
    
    # Resource limits
    MemoryMax = "2G";
    TasksMax = 50;
  };
};
```

## Monitoring & Observability

### 1. Essential Metrics

**What to monitor:**
- Cache hit rate (% of requests served from cache)
- Storage usage (% full, growth rate)
- Memory usage (identify leaks or pressure)
- CPU usage (identify bottlenecks)
- Network throughput (detect issues)
- Build success rate (% of successful builds)

### 2. Prometheus + Node Exporter

**Setup:**
```nix
services.prometheus = {
  enable = true;
  
  exporters = {
    node = {
      enable = true;
      enabledCollectors = [ 
        "systemd" 
        "processes"
        "filesystem"
        "netdev"
      ];
      port = 9100;
    };
  };
  
  scrapeConfigs = [{
    job_name = "cache-server";
    static_configs = [{
      targets = [ "localhost:9100" ];
    }];
  }];
};
```

**Query examples:**
```promql
# Disk usage percentage
(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100

# Network throughput
rate(node_network_receive_bytes_total{device="eth0"}[5m])
```

### 3. Logging Strategy

**Centralized logging:**
```nix
services.journald.extraConfig = ''
  Storage=persistent
  MaxRetentionSec=2week
  MaxFileSec=1day
'';
```

**Key logs to monitor:**
```bash
# Build failures
journalctl -u nix-daemon | grep -i "error\|failed"

# Cache serving
journalctl -u nix-serve -f

# System errors
journalctl -p err -b
```

### 4. Alerting (Simple)

**Disk space alert:**
```bash
#!/usr/bin/env bash
# /etc/cron.hourly/check-disk

THRESHOLD=85
USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "WARNING: Disk usage at ${USAGE}%" | \
      mail -s "Cache Server Alert" admin@example.com
fi
```

## Backup & Recovery

### 1. What to Back Up

**Critical:**
- Private signing key (`/var/cache-priv-key.pem`)
- NixOS configuration (`/etc/nixos/`)

**Optional:**
- `/nix/store` (can be rebuilt, but expensive)
- Build logs (`/nix/var/log/nix/`)

### 2. Configuration Backup

**Automated git backup:**
```nix
# /etc/nixos/backup.sh
#!/usr/bin/env bash
cd /etc/nixos
git add -A
git commit -m "Auto backup $(date +%Y-%m-%d)"
git push origin main
```

**Systemd timer:**
```nix
systemd.timers.config-backup = {
  wantedBy = [ "timers.target" ];
  timerConfig = {
    OnCalendar = "daily";
    Persistent = true;
  };
};

systemd.services.config-backup = {
  script = "/etc/nixos/backup.sh";
  serviceConfig.Type = "oneshot";
};
```

### 3. Recovery Plan

**Document the recovery procedure:**

```markdown
## Emergency Recovery Procedure

1. Boot from NixOS ISO
2. Mount existing partition: `mount /dev/sda1 /mnt`
3. Restore configuration: `git clone <repo> /mnt/etc/nixos`
4. Restore signing key: `cp backup/cache-priv-key.pem /mnt/var/`
5. Rebuild: `nixos-install --root /mnt`
6. Reboot

Time estimate: 30 minutes
```

### 4. Disaster Scenarios

**Lost signing key:**
- Impact: Clients won't trust cache
- Recovery: Generate new keys, distribute to all clients
- Prevention: Offline backup of key

**Corrupted /nix/store:**
- Impact: Cache invalidated
- Recovery: `nix-store --verify --repair`
- Prevention: Regular `auto-optimise-store`, BTRFS snapshots

**Hardware failure:**
- Impact: Service downtime
- Recovery: Restore config on new hardware
- Prevention: Keep spare hardware, regular backups

## Performance Tuning

### 1. Baseline Performance

**Measure before optimizing:**
```bash
# Cache hit latency
time curl -s http://localhost:5000/nix-cache-info

# Network throughput
iperf3 -s  # On server
iperf3 -c 10.255.255.1  # On client

# Build time (reference package)
time nix-build '<nixpkgs>' -A hello
```

**Document baselines:**
- Cache hit: < 50ms
- Network: > 900 Mbps
- Hello build: < 30s

### 2. Iterative Optimization

**Process:**
1. Measure baseline
2. Change one parameter
3. Measure again
4. Keep if improved, revert if worse
5. Document results

**Example tuning log:**
```
Date: 2024-10-25
Changed: nix.settings.max-jobs from 2 to 3
Before: Firefox build 45min
After: Firefox build 38min
Result: Kept, 15% improvement
Notes: RAM usage increased 500MB, still acceptable
```

### 3. Performance Profiles

**Quick profiles by use case:**

**Single heavy user (dev workstation):**
```nix
nix.settings = {
  max-jobs = 4;
  cores = 2;
  http-connections = 50;
};
```

**Multiple light users (office):**
```nix
nix.settings = {
  max-jobs = 2;
  cores = 1;
  http-connections = 25;
  keep-outputs = false;  # Reduce storage
};
```

**CI/CD server:**
```nix
nix.settings = {
  max-jobs = 8;
  cores = 4;
  keep-outputs = true;
  keep-derivations = true;
};
```

## Maintenance

### 1. Regular Tasks

**Daily (automated):**
- Garbage collection (via `nix.gc.automatic`)
- Log rotation (via `services.journald`)
- Backup configuration (via systemd timer)

**Weekly (manual):**
- Review disk usage: `df -h / && du -sh /nix/store`
- Check for build failures: `journalctl -u nix-daemon --since "1 week ago" | grep failed`
- Verify cache serving: `curl http://localhost:5000/nix-cache-info`

**Monthly (manual):**
- Review system logs: `journalctl -p err --since "1 month ago"`
- Check for updates: `nixos-rebuild dry-build`
- Test disaster recovery (every 6 months)
- Review and update documentation

### 2. Update Strategy

**NixOS channel updates:**
```bash
# Check current channel
nix-channel --list

# Update and test
sudo nix-channel --update
sudo nixos-rebuild test

# If stable, apply
sudo nixos-rebuild switch

# If issues, rollback
sudo nixos-rebuild --rollback switch
```

**Best practices:**
- Test updates on dev/staging first
- Schedule during low-usage windows
- Keep previous generation available for rollback
- Document changes and observations

### 3. Capacity Planning

**Monitor growth trends:**
```bash
# Store size history
du -sh /nix/store | ts >> /var/log/store-size.log

# Analyze growth
awk '{print $2, $1}' /var/log/store-size.log | \
  gnuplot -e "set terminal dumb; plot '-' using 1:2 with lines"
```

**Predict storage needs:**
- Linear growth: Extrapolate from 3-month trend
- Plan upgrade when approaching 70% full
- Black Friday is ideal upgrade window

## Documentation

### 1. Living Documentation

**Maintain a knowledge base:**

```
docs/
├── architecture.md       # System design, network topology
├── runbook.md           # Common operations, troubleshooting
├── decisions.md         # ADRs (Architecture Decision Records)
└── postmortems/         # Incident reports and learnings
```

**Example ADR:**
```markdown
# ADR-001: Use Direct RJ45 Connection

Date: 2024-10-25
Status: Accepted

## Context
Cache server and client are physically adjacent. Could use
existing network switch or direct cable connection.

## Decision
Use direct RJ45 cable connection (10.255.255.0/24 subnet).

## Consequences
+ Reduced latency (0.3ms vs 2ms)
+ Dedicated bandwidth, no contention
+ Network isolation
- Requires manual IP configuration
- Not easily scalable to >2 machines

## Alternatives Considered
- WiFi: Too unreliable for critical service
- Switch: Unnecessary complexity and latency
```

### 2. Operational Playbooks

**Example: "Adding New Client" playbook:**
```markdown
## Add New Cache Client

Prerequisites:
- Physical RJ45 cable
- Client has free ethernet port

Steps:
1. Connect cable between server eth0 and client eth1
2. On client, configure network:
   [configuration snippet]
3. Configure Nix substituters:
   [configuration snippet]
4. Test connectivity:
   `ping 10.255.255.1`
5. Test cache:
   `nix-build '<nixpkgs>' -A hello`
6. Update documentation with new client details

Time estimate: 15 minutes
```

### 3. Configuration as Documentation

**Self-documenting configs:**
```nix
{
  # Cache server optimized for:
  # - 4GB RAM (can handle 2 concurrent builds)
  # - 100GB storage (7-day cache retention)
  # - Direct network connection (10.255.255.0/24)
  
  services.nix-serve = {
    enable = true;
    secretKeyFile = "/var/cache-priv-key.pem";
    port = 5000;
  };
  
  nix.settings = {
    # Build parallelism: 2 jobs × 1 core = 2 threads
    # Rationale: Limited RAM, avoid OOM
    max-jobs = 2;
    cores = 1;
    
    # Storage management: Keep 10-25GB free
    # Rationale: Small partition, aggressive GC needed
    max-free = ${25 * 1024 * 1024 * 1024};
    min-free = ${10 * 1024 * 1024 * 1024};
  };
  
  # Garbage collection: Daily, 7-day retention
  # Rationale: Limited storage, frequent cleanup needed
  nix.gc = {
    automatic = true;
    dates = "daily";
    options = "--delete-older-than 7d";
  };
}
```

## Anti-Patterns to Avoid

### 1. Over-Engineering

**Don't:**
- Set up Kubernetes for single cache server
- Use enterprise monitoring (Grafana, etc.) for home lab
- Implement complex HA for non-critical service

**Do:**
- Start simple, add complexity only when needed
- Use built-in tools (journalctl, systemctl)
- Accept single point of failure for dev/test

### 2. Under-Specification

**Don't:**
- Assume infinite storage/RAM
- Ignore garbage collection
- Skip monitoring completely

**Do:**
- Set realistic resource limits
- Enable automatic GC from day one
- Monitor at least disk usage and service status

### 3. Premature Optimization

**Don't:**
- Tune kernel parameters before measuring
- Max out all settings hoping for better performance
- Copy random configs from internet without understanding

**Do:**
- Measure baseline performance first
- Change one thing at a time
- Understand what each setting does

## Advanced Topics

### 1. Distributed Builds

For extremely limited cache server, offload builds to more powerful machine:

```nix
# On cache server
nix.buildMachines = [{
  hostName = "build-server.local";
  system = "x86_64-linux";
  maxJobs = 4;
  speedFactor = 2;
  supportedFeatures = [ "nixos-test" "benchmark" "big-parallel" ];
  mandatoryFeatures = [];
}];

nix.distributedBuilds = true;
```

### 2. Multi-Tier Caching

**Architecture:**
```
Client → Local Cache (4GB RAM) → Remote Cache (Powerful) → cache.nixos.org
```

**Configuration:**
```nix
# Local cache (server)
services.nix-serve.enable = true;

nix.settings.substituters = [
  "http://remote-cache.local:5000"
  "https://cache.nixos.org"
];

# Client
nix.settings.substituters = [
  "http://10.255.255.1:5000"      # Try local first
  "http://remote-cache.local:5000"  # Then remote
  "https://cache.nixos.org"        # Finally official
];
```

### 3. BTRFS Snapshots (Optional)

**For /nix partition:**
```nix
fileSystems."/nix" = {
  device = "/dev/sda2";
  fsType = "btrfs";
  options = [ "compress=zstd" "noatime" ];
};

# Automatic snapshots before upgrades
system.activationScripts.snapshotNix = ''
  btrfs subvolume snapshot /nix /nix-snapshots/pre-upgrade-$(date +%Y%m%d)
  # Keep only last 5 snapshots
  ls -t /nix-snapshots | tail -n +6 | xargs -I {} btrfs subvolume delete /nix-snapshots/{}
'';
```

## Summary Checklist

**Essential best practices:**
- [ ] Signed cache with secure key storage
- [ ] Automatic garbage collection configured
- [ ] Firewall enabled with minimal exposure
- [ ] Basic monitoring (disk space, service status)
- [ ] Configuration backed up
- [ ] Disaster recovery plan documented
- [ ] Performance baseline measured

**Advanced (optional):**
- [ ] Prometheus monitoring
- [ ] Systemd service hardening
- [ ] BTRFS snapshots
- [ ] Distributed builds
- [ ] Multi-tier caching
