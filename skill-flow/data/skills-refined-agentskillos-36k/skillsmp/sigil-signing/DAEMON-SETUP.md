# Sigil Daemon Setup Guide

Complete guide for installing and configuring the Sigil signing daemon.

## Prerequisites

- Linux system with floppy drive support (USB floppy drives work)
- Rust toolchain (1.70+)
- udev (for automatic disk detection)

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/chippr-robotics/sigil.git
cd sigil

# Build release binaries
cargo build --release

# Install binaries
sudo cp target/release/sigil-daemon /usr/local/bin/
sudo cp target/release/sigil-cli /usr/local/bin/

# Install udev rules
sudo cp scripts/99-sigil.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
```

### Using Install Script

```bash
./scripts/install.sh
```

## Configuration

### Daemon Configuration

Create `/etc/sigil/daemon.json`:

```json
{
  "agent_store_path": "/var/lib/sigil/agent_store",
  "ipc_socket_path": "/tmp/sigil.sock",
  "enable_zkvm_proving": false,
  "disk_mount_pattern": "/media/*/SIGIL*",
  "signing_timeout_secs": 60,
  "dev_mode": false
}
```

**Configuration Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `agent_store_path` | `/var/lib/sigil/agent_store` | Where agent shares are stored |
| `ipc_socket_path` | `/tmp/sigil.sock` | Unix socket path |
| `enable_zkvm_proving` | `false` | Enable SP1 proof generation |
| `disk_mount_pattern` | `/media/*/SIGIL*` | Glob pattern for disk detection |
| `signing_timeout_secs` | `60` | Timeout for signing operations |
| `dev_mode` | `false` | Enable development features |

### Create Required Directories

```bash
sudo mkdir -p /etc/sigil
sudo mkdir -p /var/lib/sigil/agent_store
sudo chown $USER:$USER /var/lib/sigil/agent_store
```

## Running the Daemon

### Manual Start

```bash
# Foreground (for debugging)
sigil-daemon

# Background
sigil-daemon &

# With custom config
sigil-daemon --config /path/to/config.json
```

### Systemd Service

Create `/etc/systemd/system/sigil-daemon.service`:

```ini
[Unit]
Description=Sigil MPC Signing Daemon
After=network.target

[Service]
Type=simple
User=sigil
Group=sigil
ExecStart=/usr/local/bin/sigil-daemon
Restart=on-failure
RestartSec=5

# Security hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/sigil /tmp

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable sigil-daemon
sudo systemctl start sigil-daemon
```

### Check Status

```bash
# Via systemctl
sudo systemctl status sigil-daemon

# Via CLI
sigil-cli check-disk

# Via socket directly
echo '{"type":"Ping"}' | nc -U /tmp/sigil.sock
```

## Disk Detection

### udev Rules

The daemon uses udev for automatic disk detection. Rules in `/etc/udev/rules.d/99-sigil.rules`:

```
# Mount Sigil disks automatically
SUBSYSTEM=="block", KERNEL=="fd*", ACTION=="add", \
  RUN+="/usr/local/bin/sigil-mount %k"

SUBSYSTEM=="block", KERNEL=="fd*", ACTION=="remove", \
  RUN+="/usr/local/bin/sigil-unmount %k"

# Also handle USB floppy drives
SUBSYSTEM=="block", ATTRS{idVendor}=="*", ATTRS{idProduct}=="*", \
  ENV{ID_TYPE}=="floppy", ACTION=="add", \
  RUN+="/usr/local/bin/sigil-mount %k"
```

Reload rules:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Manual Mount

If udev rules aren't working:

```bash
# Create mount point
sudo mkdir -p /media/sigil

# Mount with proper flags
sudo mount -o noexec,nosuid,nodev,umask=077 /dev/fd0 /media/sigil

# Verify
ls -la /media/sigil/
```

## Agent Store Setup

The daemon stores the "agent half" of presignatures locally.

### Initialize Agent Store

When you first pair with a mother device:

```bash
# The mother device will provide the agent shares
sigil-cli import-shares --file agent_shares.json

# Verify import
sigil-cli list-children
```

### Backup Agent Store

Critical: Without agent shares, presigs on disk are useless.

```bash
# Create encrypted backup
tar czf - /var/lib/sigil/agent_store | \
  gpg --symmetric --cipher-algo AES256 > agent_store_backup.tar.gz.gpg

# Restore
gpg --decrypt agent_store_backup.tar.gz.gpg | \
  tar xzf - -C /
```

## Troubleshooting

### Daemon Won't Start

```bash
# Check if socket exists from previous run
rm -f /tmp/sigil.sock

# Check permissions
ls -la /var/lib/sigil/

# Run with debug logging
RUST_LOG=debug sigil-daemon
```

### Disk Not Detected

```bash
# Check if disk is mounted
mount | grep -i floppy

# Check udev events
udevadm monitor --subsystem-match=block

# Manual detection test
ls /media/*/SIGIL* 2>/dev/null || echo "No disk found"
```

### Signing Fails

```bash
# Check disk status
sigil-cli check-disk --json

# Verify agent store has matching shares
sigil-cli list-children

# Check daemon logs
journalctl -u sigil-daemon -f
```

### Socket Permission Denied

```bash
# Check socket permissions
ls -la /tmp/sigil.sock

# Ensure user is in correct group
sudo usermod -aG sigil $USER

# Or set permissive socket mode (dev only)
# In daemon.json: "socket_mode": "0666"
```

## Security Recommendations

### Production Deployment

1. **Run as dedicated user**: Create a `sigil` user with minimal privileges
2. **Encrypt agent store**: Use LUKS or similar for `/var/lib/sigil`
3. **Network isolation**: Daemon should not have network access
4. **Audit logging**: Enable syslog forwarding
5. **Regular backups**: Automate encrypted backups of agent store

### Physical Security

1. Store signing disks in secure location
2. Limit physical access to the machine running the daemon
3. Use tamper-evident seals on disk storage
4. Consider using multiple disks with different expiry dates

### Operational Security

1. Rotate disks regularly (recommended: every 30 days)
2. Monitor presig consumption rates
3. Review usage logs periodically
4. Test recovery procedures

## Development Mode

For testing without physical disks:

```json
{
  "dev_mode": true,
  "virtual_disk_path": "/tmp/sigil_virtual_disk"
}
```

Create a virtual disk:

```bash
sigil-cli create-virtual-disk --presigs 100 --output /tmp/sigil_virtual_disk
```

**Warning**: Never use dev mode in production.
