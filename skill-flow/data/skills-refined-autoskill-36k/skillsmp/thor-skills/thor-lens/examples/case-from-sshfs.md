# Case from SSHFS

Scan remote systems that can't run THOR directly by mounting their filesystem via SSHFS.

## Use Cases

- Network appliances with no shell access
- IoT devices or embedded systems
- Systems with unsupported architectures
- Quick triage of remote Linux/Unix systems

## Prerequisites

- THOR v11 installed locally
- THOR Lens built locally
- SSH access to remote system
- SSHFS installed locally

### Install SSHFS

```bash
# Debian/Ubuntu
sudo apt install sshfs

# RHEL/Fedora
sudo dnf install sshfs

# macOS (requires macFUSE)
brew install sshfs
```

## Step 1: Mount Remote System

### Basic Mount

```bash
mkdir -p /mnt/remote
sshfs root@remote-host:/ /mnt/remote -o ro
```

### With SSH Key

```bash
sshfs root@host:/ /mnt/remote -o ro,IdentityFile=~/.ssh/id_rsa
```

### Via Jump Host

```bash
sshfs -o ProxyJump=bastion-host root@internal-host:/ /mnt/remote
```

### Performance Options

```bash
sshfs root@host:/ /mnt/remote -o ro,cache=yes,kernel_cache,compression=no
```

### Verify Mount

```bash
ls /mnt/remote/
# Should show remote filesystem
```

## Step 2: Identify Remote Hostname

```bash
cat /mnt/remote/etc/hostname
```

## Step 3: Run THOR v11 Scan

```bash
./thor-linux-64 --lab \
  -p /mnt/remote \
  --virtual-map /mnt/remote:/ \
  -j remote-hostname \
  --audit-trail /cases/remote-hostname_audit.jsonl \
  -e /cases/reports
```

### For Quick Triage

```bash
./thor-linux-64 --lab --quick \
  -p /mnt/remote \
  --virtual-map /mnt/remote:/ \
  -j remote-hostname \
  --audit-trail /cases/remote-hostname_audit.jsonl \
  -e /cases/reports
```

### Scan Specific Directories Only

```bash
./thor-linux-64 --lab \
  -p /mnt/remote/etc \
  -p /mnt/remote/var/log \
  --virtual-map /mnt/remote:/ \
  -j remote-hostname \
  --audit-trail /cases/remote-hostname_audit.jsonl \
  -e /cases/reports
```

## Step 4: Unmount

```bash
# Linux
fusermount -u /mnt/remote

# macOS
umount /mnt/remote
```

## Step 5: Import into THOR Lens

```bash
cd /path/to/thor-lens

./thorlens import \
  --log /cases/remote-hostname_audit.jsonl \
  --case remote-hostname

# Verify
cat ./cases/remote-hostname/meta.json | jq '.event_count'
```

## Step 6: Analyze

```bash
./thorlens serve --case ./cases/remote-hostname --port 8080
```

Open **http://127.0.0.1:8080**

## Example: Scanning a Firewall

```bash
# Mount firewall filesystem
mkdir -p /mnt/firewall
sshfs admin@firewall-01:/ /mnt/firewall -o ro

# Quick scan of config and logs
./thor-linux-64 --lab --quick \
  -p /mnt/firewall/etc \
  -p /mnt/firewall/var/log \
  --virtual-map /mnt/firewall:/ \
  -j firewall-01 \
  --audit-trail /cases/firewall-01_audit.jsonl \
  -e /cases/reports

# Unmount
fusermount -u /mnt/firewall

# Import and analyze
./thorlens import --log /cases/firewall-01_audit.jsonl --case firewall-01
./thorlens serve --case ./cases/firewall-01 --port 8080
```

## Troubleshooting

### Connection Drops

Add reconnection options:

```bash
sshfs user@host:/ /mnt/target -o ro,reconnect,ServerAliveInterval=15
```

### Permission Issues

```bash
sshfs root@host:/ /mnt/target -o ro,allow_other,default_permissions
```

### Slow Performance

1. Use `--quick` mode for initial triage
2. Target specific directories instead of full filesystem
3. Disable compression on fast networks: `-o compression=no`
4. Run multiple targeted scans in parallel

### Mount Fails

```bash
# Check SSH works
ssh root@host "ls /"

# Check SSHFS is installed
which sshfs

# Try with debug
sshfs -d root@host:/ /mnt/target -o ro
```

## Limitations

- Slower than local scanning (network I/O bound)
- No process memory scanning (remote system not running THOR)
- Large filesystems take longer to scan
- Connection stability affects scan reliability

## Quick Reference

```bash
# Mount
sshfs root@host:/ /mnt/remote -o ro

# Scan
./thor-linux-64 --lab -p /mnt/remote --virtual-map /mnt/remote:/ -j hostname --audit-trail audit.jsonl

# Unmount
fusermount -u /mnt/remote

# Import
./thorlens import --log audit.jsonl --case hostname

# Serve
./thorlens serve --case ./cases/hostname --port 8080
```
