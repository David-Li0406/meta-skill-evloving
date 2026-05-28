---
name: unifi
description: Manage Ubiquiti UniFi networks - monitor devices, clients, health status, restart APs, block/unblock clients. Use when user mentions UniFi, network management, or WiFi issues.
triggers:
  - UniFi network management
  - WiFi client monitoring
  - Network device control
  - Access point management
  - Network health check
---

# UniFi MCP Server

Manage Ubiquiti UniFi networks from Claude Code via MCP.

## When to Use

Use this skill when:
- User asks about network devices or clients
- User wants to check network health or status
- User needs to restart an access point or device
- User wants to block/unblock network clients
- User mentions "UniFi", "WiFi", "network", or related terms

## Available MCP Tools

### Monitoring Tools

| Tool | Description |
|------|-------------|
| `list_devices(device_type?)` | List network devices (APs, switches, gateways) |
| `list_clients(connection_type?)` | List connected clients (wireless/wired) |
| `get_device_stats(device_mac)` | Get detailed stats for a device |
| `list_alerts(limit?)` | View recent network alerts |
| `get_network_health()` | Overall network health status |
| `get_site_info()` | Site and controller information |

### Management Tools

| Tool | Description |
|------|-------------|
| `restart_device(device_mac)` | Restart an AP, switch, or gateway |
| `block_client(client_mac)` | Block a client from the network |
| `unblock_client(client_mac)` | Unblock a previously blocked client |
| `authorize_guest(guest_mac, minutes?, up?, down?)` | Authorize guest with limits |

## Common Workflows

### Check Network Health
```
1. Use get_network_health() for overall status
2. Use list_alerts() to see recent issues
3. Use list_devices() to check device states
```

### Find and Manage Clients
```
1. Use list_clients() to see all connected devices
2. Filter by "wireless" or "wired" if needed
3. Use block_client(mac) to block a problematic device
```

### Troubleshoot an AP
```
1. Use list_devices("ap") to see access points
2. Use get_device_stats(mac) for detailed info
3. Use restart_device(mac) if restart is needed
```

### Authorize Guest
```
1. Get guest's MAC address
2. Use authorize_guest(mac, minutes, up_kbps, down_kbps)
3. Default is unlimited if no limits specified
```

## Version Selection

The UNIFI_VERSION setting depends on your hardware:

| Hardware | UNIFI_VERSION |
|----------|---------------|
| UDM Pro, UDM SE, UXG | `UDMP-unifiOS` (recommended) |
| Cloud Key Gen2+ | `unifiOS` |
| Cloud Key Gen1 | `v5` |
| Legacy controllers | `v4` |

## Troubleshooting

### SSL Errors
Self-signed certificate errors are handled automatically (ssl_verify=False).

### Authentication Errors
1. Verify credentials: `deep-env list | grep UNIFI`
2. Ensure UniFi user has admin privileges
3. Try changing UNIFI_VERSION if commands fail

### Commands Failing
If commands fail silently, try a different UNIFI_VERSION setting.

## Setup

Store credentials via deep-env:
```bash
deep-env store UNIFI_HOST "your-controller-ip"
deep-env store UNIFI_USERNAME "your-username"
deep-env store UNIFI_PASSWORD "your-password"
deep-env store UNIFI_VERSION "UDMP-unifiOS"
```

## Example Usage

**Check devices:**
"What devices are on my network?"

**See wireless clients:**
"Show me all wireless clients"

**Restart an AP:**
"Restart the living room AP"

**Block a device:**
"Block the device with MAC aa:bb:cc:dd:ee:ff"

**Network health:**
"What's the network health status?"
