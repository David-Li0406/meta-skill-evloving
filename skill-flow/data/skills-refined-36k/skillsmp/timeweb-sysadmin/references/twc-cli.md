# TWC CLI Reference

Timeweb Cloud CLI quick reference. Full docs: https://github.com/timeweb-cloud/twc

## Server Commands

```bash
# List servers
twc server list
twc server list -o json  # JSON output

# Get server info
twc server get <SERVER_ID>

# Power management
twc server boot <SERVER_ID>      # Start
twc server shutdown <SERVER_ID>  # Stop
twc server reboot <SERVER_ID>    # Restart

# Open VNC console
twc server vnc <SERVER_ID>

# Open dashboard in browser
twc server dash <SERVER_ID>
```

## Backup Commands

```bash
# List backups for a disk
twc server backup list <DISK_ID>

# Create backup
twc server backup create <DISK_ID>
twc server backup create <DISK_ID> --comment "Before upgrade"

# Restore backup
twc server backup restore <DISK_ID> <BACKUP_ID>

# Configure automated backups
twc server backup schedule <DISK_ID> --enable --keep 7 --interval day

# Mount backup as external drive
twc server backup mount <DISK_ID> <BACKUP_ID>
twc server backup unmount <DISK_ID> <BACKUP_ID>
```

## S3 Storage Commands

```bash
# List buckets
twc storage list

# Create bucket
twc storage mb <BUCKET_NAME>

# Remove bucket
twc storage rb <BUCKET_NAME>

# Generate S3 client config (for s3cmd, rclone, etc.)
twc storage genconfig
```

## Apps Commands

```bash
# List apps
twc apps list

# Get app details
twc apps get <APP_ID>

# Delete app
twc apps delete <APP_ID>
```

## Domain Commands

```bash
# List domains
twc domain list

# Get domain info
twc domain info <DOMAIN>

# List DNS records
twc domain record list <DOMAIN>

# Add DNS record
twc domain record add <DOMAIN> --type A --name www --value 1.2.3.4
```

## Firewall Commands

```bash
# List firewall groups
twc firewall group list

# Show firewall rules
twc firewall show <GROUP_ID>

# Link firewall to server
twc firewall link <GROUP_ID> --server <SERVER_ID>
```

## Account Commands

```bash
# Check account
twc whoami

# Account finances
twc account finances

# Account status
twc account status
```

## Config Commands

```bash
# Initialize config
twc config init

# Edit config
twc config edit

# Show config file path
twc config file

# List profiles
twc config profiles
```

## Common Options

| Option | Description |
|--------|-------------|
| `-o json` | JSON output |
| `-o yaml` | YAML output |
| `-v` | Verbose mode |
| `-y` | Auto-confirm (no prompt) |
| `-p <profile>` | Use specific profile |
