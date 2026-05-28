# Unifi MCP Server

Model Context Protocol server for managing Ubiquiti Unifi networks through Claude Code.

## Features

- **Device Management**: List, monitor, and restart access points, switches, and gateways
- **Client Monitoring**: View connected clients (wired and wireless) with connection details
- **Network Control**: Block/unblock clients, authorize guests with bandwidth limits
- **Health Monitoring**: Check network health, view alerts, and device statistics
- **Site Information**: Access controller and site configuration

## Installation

1. Install dependencies:
```bash
cd ~/claudesync/mcp-servers/unifi
pip install -e .
```

Or with uv (recommended):
```bash
cd ~/claudesync/mcp-servers/unifi
uv pip install -e .
```

## Configuration

### 1. Store Unifi Credentials

Use deep-env to securely store your Unifi controller credentials:

```bash
# Store required credentials
deep-env store UNIFI_HOST "your-controller-ip-or-hostname"
deep-env store UNIFI_USERNAME "your-username"
deep-env store UNIFI_PASSWORD "your-password"

# Optional: Store custom settings
deep-env store UNIFI_PORT "8443"  # Default: 8443
deep-env store UNIFI_SITE "default"  # Default: default
deep-env store UNIFI_VERSION "UDMP-unifiOS"  # Default: UDMP-unifiOS

# Sync to iCloud for other Macs
deep-env push
```

**Note**: UNIFI_VERSION options:
- `UDMP-unifiOS` - UDM Pro, UDM SE, or UXG devices (recommended for modern hardware)
- `unifiOS` - Cloud Key Gen2 Plus
- `v5` - Cloud Key Gen1 or older controllers
- `v4` - Legacy controllers

### 2. Add to Claude Code MCP Configuration

Add this to `~/claudesync/config.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "unifi": {
      "command": "python3",
      "args": ["~/claudesync/mcp-servers/unifi/server.py"],
      "env": {
        "UNIFI_HOST": "{{env.UNIFI_HOST}}",
        "UNIFI_USERNAME": "{{env.UNIFI_USERNAME}}",
        "UNIFI_PASSWORD": "{{env.UNIFI_PASSWORD}}",
        "UNIFI_PORT": "{{env.UNIFI_PORT}}",
        "UNIFI_SITE": "{{env.UNIFI_SITE}}",
        "UNIFI_VERSION": "{{env.UNIFI_VERSION}}"
      }
    }
  }
}
```

## Available Tools

### Monitoring Tools

- `list_devices(device_type?)` - List all network devices (APs, switches, gateways)
- `list_clients(connection_type?)` - List connected clients (wireless/wired)
- `get_device_stats(device_mac)` - Get detailed stats for a specific device
- `list_alerts(limit?)` - View recent network alerts
- `get_network_health()` - Overall network health status
- `get_site_info()` - Site and controller information

### Management Tools

- `restart_device(device_mac)` - Restart an AP, switch, or gateway
- `block_client(client_mac)` - Block a client from the network
- `unblock_client(client_mac)` - Unblock a previously blocked client
- `authorize_guest(guest_mac, minutes?, up_bandwidth_kbps?, down_bandwidth_kbps?)` - Authorize guest with time/bandwidth limits

## Usage Examples

Once configured, you can use natural language with Claude Code:

```
"What devices are on my network?"
"Show me all wireless clients"
"Restart the living room AP"
"Block the device with MAC aa:bb:cc:dd:ee:ff"
"Authorize guest with MAC xx:yy:zz:aa:bb:cc for 2 hours"
"What's the network health status?"
"Show me recent alerts"
```

## Troubleshooting

### Connection Issues

If you see SSL errors, ensure `ssl_verify=False` is set in server.py (it is by default for self-signed certificates).

### Authentication Errors

1. Verify credentials are stored correctly:
```bash
deep-env list | grep UNIFI
```

2. Check that your Unifi user has admin privileges

3. For UDM Pro, ensure you're using `UNIFI_VERSION=UDMP-unifiOS`

### Version Compatibility

If commands fail, try changing `UNIFI_VERSION`:
- UDM Pro/SE/UXG: `UDMP-unifiOS`
- Cloud Key Gen2+: `unifiOS`
- Older controllers: `v5` or `v4`

## Security Notes

- Credentials are stored in macOS Keychain via deep-env (encrypted)
- SSL certificate verification is disabled by default (self-signed certs)
- The MCP server only runs when Claude Code is active
- API calls use HTTPS (port 8443 by default)

## Future Enhancements

Potential additions:
- WebSocket support for real-time events
- Firewall rule management
- WLAN configuration
- Voucher generation
- Port profile management
- Historical bandwidth analytics
- Automatic backup/restore
