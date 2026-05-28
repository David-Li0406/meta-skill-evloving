# System Packs

This document describes packs in the `system` category.

## Packs in this Category

- [Disk Operations](#systemdisk)
- [Permissions](#systempermissions)
- [Services](#systemservices)

---

## Disk Operations

**Pack ID:** `system.disk`

Protects against destructive disk operations like dd to devices, mkfs, and partition table modifications

### Keywords

Commands containing these keywords are checked against this pack:

- `dd`
- `fdisk`
- `mkfs`
- `parted`
- `mount`
- `wipefs`
- `/dev/`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `dd-file-out` | `dd\s+.*of=[^/\s]+\.` |
| `dd-discard` | `dd\s+.*of=/dev/(?:null\|zero\|full)(?:\s\|$)` |
| `lsblk` | `\blsblk\b` |
| `fdisk-list` | `fdisk\s+-l` |
| `parted-print` | `parted\s+.*print` |
| `blkid` | `\bblkid\b` |
| `df` | `\bdf\b` |
| `mount-list` | `\bmount\s*$` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `dd-device` | dd to a block device will OVERWRITE all data on that device. Extremely dangerous! | high |
| `dd-wipe` | dd from /dev/zero or /dev/urandom to a device will WIPE all data! | high |
| `fdisk-edit` | fdisk can modify partition tables and cause data loss. | high |
| `parted-modify` | parted can modify partition tables and cause data loss. | high |
| `mkfs` | mkfs formats a partition/device and ERASES all existing data. | high |
| `wipefs` | wipefs removes filesystem signatures. Use with extreme caution. | high |
| `mount-bind-root` | mount --bind to root directory can have system-wide effects. | high |
| `umount-force` | umount -f force unmounts which may cause data loss if device is in use. | high |
| `losetup-device` | losetup modifies loop device associations. Verify before proceeding. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "system.disk:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "system.disk:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Permissions

**Pack ID:** `system.permissions`

Protects against dangerous permission changes like chmod 777, recursive chmod/chown on system directories

### Keywords

Commands containing these keywords are checked against this pack:

- `chmod`
- `chown`
- `chgrp`
- `setfacl`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `chmod-non-recursive` | `chmod\s+(?!-[rR])(?:\d{3,4}\|[ugoa][+-][rwxXst]+)\s+[^/]` |
| `stat` | `\bstat\b` |
| `ls-perms` | `ls\s+.*-[a-zA-Z]*l` |
| `getfacl` | `\bgetfacl\b` |
| `namei` | `\bnamei\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `chmod-777` | chmod 777 makes files world-writable. This is a security risk. | high |
| `chmod-recursive-root` | chmod -R on system directories can break system permissions. | high |
| `chown-recursive-root` | chown -R on system directories can break system ownership. | high |
| `chmod-setuid` | Setting setuid bit (chmod u+s) is a security-sensitive operation. | high |
| `chmod-setgid` | Setting setgid bit (chmod g+s) is a security-sensitive operation. | high |
| `chown-to-root` | Changing ownership to root should be done carefully. | high |
| `setfacl-all` | setfacl -R on system directories can modify access control across the filesystem. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "system.permissions:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "system.permissions:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Services

**Pack ID:** `system.services`

Protects against dangerous service operations like stopping critical services and modifying init configuration

### Keywords

Commands containing these keywords are checked against this pack:

- `systemctl`
- `service`
- `init`
- `upstart`
- `shutdown`
- `reboot`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `systemctl-status` | `systemctl\s+status` |
| `service-status` | `service\s+\S+\s+status` |
| `systemctl-list` | `systemctl\s+list-(?:units\|unit-files\|sockets\|timers)` |
| `systemctl-show` | `systemctl\s+show` |
| `systemctl-is` | `systemctl\s+is-(?:active\|enabled\|failed)` |
| `systemctl-reload` | `systemctl\s+daemon-reload` |
| `systemctl-cat` | `systemctl\s+cat` |
| `journalctl` | `\bjournalctl\b` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `systemctl-stop-critical` | Stopping/disabling critical services can cause system access loss or outage. | high |
| `systemctl-stop` | systemctl stop/disable/mask affects service availability. Verify service name. | high |
| `service-stop-critical` | Stopping critical services can cause system access loss. | high |
| `systemctl-isolate` | systemctl isolate changes the system state significantly. | high |
| `systemctl-power` | systemctl poweroff/reboot/halt will shut down or restart the system. | high |
| `shutdown` | shutdown will power off or restart the system. | high |
| `reboot` | reboot will restart the system. | high |
| `init-level` | init 0 shuts down, init 6 reboots the system. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "system.services:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "system.services:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

