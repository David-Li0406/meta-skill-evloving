# SSHFS Remote Scanning

Scan remote systems that don't support running THOR directly (appliances, embedded devices, unusual architectures) by mounting their filesystem via SSHFS.

## When to Use This

- Network appliances with no shell access
- IoT devices or embedded systems
- Systems with unsupported architectures
- Situations where you can't deploy THOR binaries
- Quick triage of remote Linux/Unix systems

## Prerequisites

```bash
# Install sshfs
sudo apt install sshfs  # Debian/Ubuntu
sudo dnf install sshfs  # RHEL/Fedora
brew install sshfs      # macOS (requires macFUSE)
```

## Basic Remote Scan

```bash
# Create mount point
mkdir -p /mnt/remote_host

# Mount remote filesystem via SSHFS
sshfs root@remote-host:/ /mnt/remote_host -o ro

# Run THOR scan
./thor-linux-64 --lab \
  -p /mnt/remote_host \
  --virtual-map /mnt/remote_host:/ \
  -j remote-host \
  -e /cases/remote-host/reports

# Unmount when done
fusermount -u /mnt/remote_host  # Linux
umount /mnt/remote_host         # macOS
```

## Read-Only Mount (Recommended)

Always mount with read-only to avoid accidental modifications:

```bash
sshfs user@host:/ /mnt/target -o ro,allow_other
```

## SSH Key Authentication

```bash
sshfs root@host:/ /mnt/target -o ro,IdentityFile=~/.ssh/id_rsa
```

## Jump Host (Bastion)

For hosts only accessible through a jump box:

```bash
sshfs -o ProxyJump=bastion-host root@internal-host:/ /mnt/target
```

## Performance Tuning

SSHFS can be slow for large filesystems. Optimize with:

```bash
sshfs root@host:/ /mnt/target -o ro,cache=yes,kernel_cache,compression=no
```

For THOR, consider:
```bash
./thor-linux-64 --lab --quick \
  -p /mnt/remote_host \
  --virtual-map /mnt/remote_host:/ \
  -j remote-host \
  -e /reports
```

## Partial Scans

For large remote systems, scan specific directories:

```bash
# Mount specific directory
sshfs root@host:/var/log /mnt/remote_logs -o ro

# Scan just logs
./thor-linux-64 --lab \
  -p /mnt/remote_logs \
  --virtual-map /mnt/remote_logs:/var/log \
  -j remote-host \
  -e /reports
```

## Scanning Network Appliances

Example for a firewall or router with SSH access:

```bash
# Mount appliance filesystem
sshfs admin@firewall-01:/ /mnt/firewall -o ro

# Quick scan focusing on configuration and logs
./thor-linux-64 --lab --quick \
  -p /mnt/firewall/etc \
  -p /mnt/firewall/var/log \
  --virtual-map /mnt/firewall:/ \
  -j firewall-01 \
  -e /cases/firewall-01/reports
```

## Troubleshooting

### Connection Drops

Add reconnection options:
```bash
sshfs user@host:/ /mnt/target -o ro,reconnect,ServerAliveInterval=15
```

### Permission Issues

If files appear inaccessible:
```bash
sshfs root@host:/ /mnt/target -o ro,allow_other,default_permissions
```

### Slow Performance

1. Use `--quick` mode for initial triage
2. Target specific directories instead of full filesystem
3. Disable compression if on fast network: `-o compression=no`
4. Run multiple targeted scans in parallel

## Limitations

- Slower than local scanning (network I/O bound)
- No process memory scanning (remote system not running THOR)
- Registry hives must be exported/copied for Windows over SSH
- Some file metadata may not be preserved
