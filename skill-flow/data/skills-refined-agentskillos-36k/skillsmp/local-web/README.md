# Networks Module

Cross-platform networking utilities with automatic WSL2 port forwarding, firewall management, LAN accessibility, and browser automation for AI agents.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Local Web Access](#local-web-access)
- [CLI Usage](#cli-usage)
- [Python API](#python-api)
- [Real-World Examples](#real-world-examples)
- [WSL2 Deep Dive](#wsl2-deep-dive)
- [Platform Support](#platform-support)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)

## Features

- **Cross-platform IP detection** - Works on Windows, Linux, WSL2, Android/Termux
- **WSL2 port forwarding** - Automatically configure Windows → WSL2 port forwarding
- **Firewall management** - Add firewall rules on Windows, Linux (ufw/firewalld)
- **LAN accessibility** - Make your applications accessible on the local network
- **Network information** - Get comprehensive network details
- **Port checking** - Verify if ports are open locally or remotely
- **Local web access** - Fetch/screenshot LAN URLs that cloud AI can't reach
- **Browser automation** - Click, type, scroll, crawl pages with headless Firefox/Chromium
- **CLI tools** - Easy command-line access to all features

## Installation

```bash
cd ~/scripts
pip install -e modules/networks/
```

Verify installation:
```bash
networks --help
networks ip
```

## Quick Start

### CLI Quick Start

```bash
# Get your LAN IP address
networks ip
# Output: 192.168.50.100

# Make port 3000 accessible on LAN (handles everything automatically)
networks ensure -p 3000 -n myapp

# Check if it worked
networks check -H $(networks ip) -p 3000
# Output: ✓ 192.168.50.100:3000 is OPEN

# View all network information
networks info
```

### Python Quick Start

```python
from networks import ensure_port_accessible, get_lan_ip

# Make your web app accessible on LAN
port = 3000
success, msg = ensure_port_accessible(port, name='webapp')
print(msg)

# Get IP to share with others
ip = get_lan_ip()
print(f"\n✓ Share this URL: http://{ip}:{port}")
```

## Local Web Access

Cloud AI agents (Claude, Codex, etc.) cannot access private network URLs because their requests go through cloud servers. The local-web commands run locally and can access any URL your machine can reach.

### Installation for Browser Features

```bash
# Install base module
pip install -e modules/networks/

# For browser automation (screenshots, interact, crawl, list)
pip install playwright
playwright install firefox  # or chromium
```

### Commands

```bash
# Fetch HTML from local URL
networks web-fetch http://localhost:3000/ --json

# Check if URL is accessible
networks web-check http://192.168.1.100:8080/

# Take a screenshot
networks web-screenshot http://localhost:3000/ -o screenshot.png

# List all buttons on a page
networks web-list http://localhost:3000/ --element-type button

# Click a button and capture before/after screenshots
networks web-interact http://localhost:3000/ --action click --selector "Submit"

# Crawl a site with screenshots
networks web-crawl http://localhost:3000/ --max-pages 10 -o ./crawl_output/
```

### Browser Choice

All browser commands support `--browser firefox|chromium|webkit` (default: firefox):

```bash
# Use Chromium instead of Firefox
networks web-screenshot http://localhost:3000/ -o shot.png --browser chromium
```

### See Also

See [SKILL.md](SKILL.md) for the full Agent Skills documentation.

## CLI Usage

### `networks ip` - Get LAN IP

Get the primary LAN-accessible IP address.

```bash
# Basic usage
networks ip
# Output: 192.168.50.100

# Use in scripts
IP=$(networks ip)
echo "Server running at http://$IP:3000"

# Use with other commands
curl http://$(networks ip):8000/api/status
```

### `networks info` - Network Information

Show comprehensive network information.

```bash
# Human-readable output
networks info
# Output:
# LAN IP:     192.168.50.100
# Hostname:   Xeres
# Is WSL2:    True
# Host IP:    172.21.192.1
#
# All interfaces:
#   lo              127.0.0.1
#   eth0            172.21.207.214

# JSON output (for scripts)
networks info --json
# Output: {"lan_ip": "192.168.50.100", ...}

# Use in scripts
INFO=$(networks info --json)
LAN_IP=$(echo $INFO | jq -r '.lan_ip')
```

### `networks ensure` - Make Port Accessible

Ensure a port is accessible on the LAN (handles WSL2 port forwarding and firewall rules).

```bash
# Make port 3000 accessible
networks ensure -p 3000 -n myapp
# Output:
# ✓ Port forwarding: Windows:0.0.0.0:3000 → WSL2:172.21.207.214:3000
# ✓ Firewall rule added: WSL2_myapp_3000
#
# ✓ Access from LAN: http://192.168.50.100:3000

# Different port
networks ensure -p 8080 -n api-server

# UDP port (for games, DNS, etc.)
networks ensure -p 5353 -t udp -n mdns

# Custom name for firewall rule
networks ensure -p 3001 -n "Knowledge Manager Web UI"
```

### `networks check` - Check if Port is Open

Check if a port is open on a host.

```bash
# Check local port
networks check -H localhost -p 3000
# Output: ✓ localhost:3000 is OPEN

# Check LAN IP
networks check -H 192.168.50.100 -p 3000
# Output: ✓ 192.168.50.100:3000 is OPEN

# Check remote server
networks check -H google.com -p 443
# Output: ✓ google.com:443 is OPEN

# With custom timeout
networks check -H 10.0.0.50 -p 22 -t 5.0
# Output: ✗ 10.0.0.50:22 is CLOSED

# Use in scripts (exit code indicates success)
if networks check -H $(networks ip) -p 3000; then
    echo "Server is accessible!"
else
    echo "Server is not accessible"
fi
```

### `networks wsl-host` - Get WSL2 Host IP

Get the Windows host IP from WSL2.

```bash
# Get Windows host IP
networks wsl-host
# Output: 172.21.192.1

# Use to access Windows services from WSL2
curl http://$(networks wsl-host):5000/api
```

## Python API

### Basic Network Information

```python
from networks import get_lan_ip, get_all_ips, get_network_info

# Get LAN IP
ip = get_lan_ip()
print(f"LAN IP: {ip}")
# Output: LAN IP: 192.168.50.100

# Get all network interfaces
interfaces = get_all_ips()
for iface in interfaces:
    print(f"{iface['interface']:15} {iface['ip']}")
# Output:
# lo              127.0.0.1
# eth0            172.21.207.214

# Get comprehensive network info
info = get_network_info()
print(f"Hostname: {info['hostname']}")
print(f"Running in WSL2: {info['is_wsl']}")
if info['is_wsl']:
    print(f"Windows Host IP: {info['wsl_host_ip']}")
```

### Making Ports Accessible

```python
from networks import ensure_port_accessible

# Basic usage
success, message = ensure_port_accessible(3000)
if success:
    print("✓ Port 3000 is accessible")
    print(message)
else:
    print(f"✗ Failed: {message}")

# With custom name
success, msg = ensure_port_accessible(8080, name='api-server')

# UDP port
success, msg = ensure_port_accessible(5353, protocol='udp', name='mdns')
```

### Port Checking

```python
from networks import check_port_open

# Check if local port is open
if check_port_open('localhost', 3000):
    print("Server is running")
else:
    print("Server is not running")

# Check remote server
if check_port_open('google.com', 443, timeout=5.0):
    print("Internet connection is working")

# Check LAN device
if check_port_open('192.168.1.50', 22):
    print("SSH is available")
```

### WSL2 Utilities

```python
from networks import get_wsl2_host_ip, get_network_info

# Check if running in WSL2
info = get_network_info()
if info['is_wsl']:
    print("Running in WSL2")
    print(f"Windows host: {info['wsl_host_ip']}")

    # Access Windows services from WSL2
    host_ip = get_wsl2_host_ip()
    windows_service = f"http://{host_ip}:5000"
    print(f"Windows service: {windows_service}")
```

## Real-World Examples

### Example 1: Flask Web App on WSL2

```python
# app.py
from flask import Flask
from networks import ensure_port_accessible, get_lan_ip

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from WSL2!'

if __name__ == '__main__':
    port = 5000

    # Make port accessible on LAN
    success, msg = ensure_port_accessible(port, name='flask-app')
    print(msg)

    # Get LAN IP
    lan_ip = get_lan_ip()

    print(f"\n{'='*60}")
    print(f"Flask app starting on port {port}")
    print(f"Access from this computer: http://localhost:{port}")
    print(f"Access from LAN:          http://{lan_ip}:{port}")
    print(f"Access from phone/tablet: http://{lan_ip}:{port}")
    print(f"{'='*60}\n")

    app.run(host='0.0.0.0', port=port)
```

### Example 2: FastAPI with Auto-Configuration

```python
# main.py
import uvicorn
from fastapi import FastAPI
from networks import ensure_port_accessible, get_lan_ip, get_network_info

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on WSL2!"}

@app.get("/network")
def network_info():
    """Endpoint to show network information"""
    return get_network_info()

def main():
    port = 8000

    # Setup LAN accessibility
    print("Configuring network accessibility...")
    success, msg = ensure_port_accessible(port, name='fastapi-app')
    print(msg)

    # Show access URLs
    lan_ip = get_lan_ip()
    info = get_network_info()

    print(f"\n{'='*70}")
    print(f"FastAPI server starting")
    print(f"")
    print(f"Local access:     http://localhost:{port}")
    print(f"LAN access:       http://{lan_ip}:{port}")
    print(f"API docs:         http://{lan_ip}:{port}/docs")
    print(f"Network info:     http://{lan_ip}:{port}/network")
    print(f"")
    if info['is_wsl']:
        print(f"WSL2 detected - Port forwarding configured")
        print(f"Windows host IP: {info['wsl_host_ip']}")
    print(f"{'='*70}\n")

    # Run server
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
```

### Example 3: Development Server with Health Check

```python
# dev_server.py
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from networks import ensure_port_accessible, get_lan_ip, check_port_open

def start_server(port=8000):
    # Setup network
    print(f"Setting up port {port} for LAN access...")
    success, msg = ensure_port_accessible(port, name='dev-server')
    print(msg)

    # Start server
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)

    # Wait for server to be ready
    time.sleep(1)

    # Verify server is accessible
    lan_ip = get_lan_ip()
    if check_port_open(lan_ip, port):
        print(f"\n✓ Server is accessible at http://{lan_ip}:{port}")
    else:
        print(f"\n✗ Warning: Server may not be accessible from LAN")

    print(f"\nServing HTTP on 0.0.0.0 port {port}")
    print(f"Press Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        server.shutdown()

if __name__ == '__main__':
    start_server(8000)
```

### Example 4: Network Monitor Script

```bash
#!/bin/bash
# network_monitor.sh - Monitor network accessibility

PORT=${1:-3000}
APP_NAME=${2:-"app"}

# Setup port forwarding
echo "Configuring port $PORT for LAN access..."
networks ensure -p $PORT -n $APP_NAME

# Get LAN IP
LAN_IP=$(networks ip)

echo ""
echo "Monitoring $APP_NAME on port $PORT"
echo "LAN URL: http://$LAN_IP:$PORT"
echo ""

# Continuous monitoring
while true; do
    if networks check -H $LAN_IP -p $PORT -t 1; then
        echo "$(date '+%H:%M:%S') - ✓ Service is UP"
    else
        echo "$(date '+%H:%M:%S') - ✗ Service is DOWN"
    fi
    sleep 5
done
```

### Example 5: Integration with koweb

```python
# In koweb's main.py startup
from networks import ensure_port_accessible, get_lan_ip, get_network_info
import logging

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    port = config.PORT

    # Setup LAN accessibility
    success, msg = ensure_port_accessible(port, name='koweb')
    if success:
        logger.info(msg)

        # Get network info
        lan_ip = get_lan_ip()
        info = get_network_info()

        logger.info("="*60)
        logger.info("Orchestrator Web Viewer Starting")
        logger.info(f"Local:  http://localhost:{port}")
        logger.info(f"LAN:    http://{lan_ip}:{port}")

        if info['is_wsl']:
            logger.info(f"WSL2:   Port forwarding configured")
            logger.info(f"Host:   {info['wsl_host_ip']}")

        logger.info("="*60)
    else:
        logger.warning(f"LAN setup failed: {msg}")
        logger.warning(f"Server will only be accessible locally")
```

## WSL2 Deep Dive

### How WSL2 Networking Works

WSL2 uses a virtualized network adapter with NAT. This means:
- WSL2 has its own IP address (e.g., `172.21.207.214`)
- Windows host has a different IP (e.g., `192.168.50.100`)
- Traffic from LAN goes to Windows, not directly to WSL2

### What `ensure_port_accessible()` Does on WSL2

1. **Detects WSL2 environment**
   ```python
   if sys_utils.is_wsl2():
       # Special WSL2 handling
   ```

2. **Gets WSL2 IP address**
   ```bash
   hostname -I  # Returns 172.21.207.214
   ```

3. **Creates port forwarding rule on Windows**
   ```powershell
   # Executed via powershell.exe from WSL2
   netsh interface portproxy add v4tov4 \
       listenport=3000 listenaddress=0.0.0.0 \
       connectport=3000 connectaddress=172.21.207.214
   ```
   This forwards traffic from `Windows:0.0.0.0:3000` → `WSL2:172.21.207.214:3000`

4. **Adds Windows Firewall rule**
   ```powershell
   New-NetFirewallRule -DisplayName "WSL2_koweb_3000" \
       -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
   ```

5. **Result**: LAN devices can access `192.168.50.100:3000` which gets forwarded to WSL2

### Manual WSL2 Setup (if needed)

If you need to do this manually:

```powershell
# On Windows PowerShell (as Administrator)

# Get WSL2 IP
wsl hostname -I

# Add port forwarding (replace 172.21.207.214 with your WSL2 IP)
netsh interface portproxy add v4tov4 listenport=3000 listenaddress=0.0.0.0 connectport=3000 connectaddress=172.21.207.214

# Add firewall rule
New-NetFirewallRule -DisplayName "WSL2_Port_3000" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow

# View existing port forwards
netsh interface portproxy show all

# Delete a port forward
netsh interface portproxy delete v4tov4 listenport=3000 listenaddress=0.0.0.0
```

### WSL2 Gotchas

1. **WSL2 IP changes on restart**
   - The `172.21.207.214` IP changes when WSL2 restarts
   - `networks ensure` detects the new IP and updates the forwarding
   - Run it every time you start your server

2. **Port forwarding persists across WSL2 restarts**
   - Windows port forwarding rules stay active
   - But they point to the old WSL2 IP
   - Solution: Re-run `networks ensure` after WSL2 restart

3. **Firewall rules are permanent**
   - Firewall rules stay even after reboot
   - You only need to create them once per port
   - `networks ensure` deletes old rules before creating new ones

## Platform Support

### WSL2 (Ubuntu on Windows 11)
- ✅ Port forwarding (requires PowerShell access)
- ✅ Windows Firewall rules (may require admin)
- ✅ LAN IP detection
- ✅ All CLI commands

**Requirements:**
- PowerShell accessible from WSL2 (default in WSL2)
- Administrator rights for firewall rules (optional, shows warning if fails)

### Windows 11 (Native)
- ✅ Firewall rules
- ✅ LAN IP detection
- ✅ All CLI commands

**Requirements:**
- Administrator rights for firewall rules (optional)

### Linux (Ubuntu, Debian, etc.)
- ✅ UFW firewall support
- ✅ firewalld support
- ✅ LAN IP detection
- ✅ All CLI commands

**Requirements:**
- `sudo` access for firewall configuration (optional)

### Android/Termux
- ✅ LAN IP detection
- ✅ Network information
- ✅ Port checking
- ℹ️ No firewall configuration (not needed)

## Troubleshooting

### WSL2: "Failed to add port forwarding"

**Cause:** Can't access PowerShell from WSL2

**Solution:**
```bash
# Test if PowerShell is accessible
powershell.exe -Command "Write-Host 'Hello'"

# If it fails, check if powershell.exe is in PATH
which powershell.exe

# Add to PATH if needed (in ~/.bashrc or ~/.zshrc)
export PATH="$PATH:/mnt/c/Windows/System32/WindowsPowerShell/v1.0"
```

### WSL2: "Firewall rule failed (may need admin)"

**Cause:** Creating firewall rules requires Administrator privileges

**Solution 1:** Run PowerShell as Administrator and manually add rule:
```powershell
# On Windows PowerShell (as Administrator)
New-NetFirewallRule -DisplayName "WSL2_myapp_3000" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
```

**Solution 2:** The port forwarding still works! The firewall warning is informational. Test if it's accessible:
```bash
networks check -H $(networks ip) -p 3000
```

### Can't Access from Android/Phone

**Checklist:**
1. ✅ Are both devices on the same WiFi network?
   ```bash
   # Check your network
   networks info
   ```

2. ✅ Is the server bound to `0.0.0.0` (not `127.0.0.1`)?
   ```python
   # Good
   app.run(host='0.0.0.0', port=3000)

   # Bad (only accessible locally)
   app.run(host='127.0.0.1', port=3000)
   ```

3. ✅ Is port forwarding configured (WSL2 only)?
   ```bash
   networks ensure -p 3000 -n myapp
   ```

4. ✅ Is the port actually open?
   ```bash
   networks check -H $(networks ip) -p 3000
   ```

5. ✅ Windows Firewall blocking? (Windows/WSL2)
   ```powershell
   # Check firewall rules (Windows PowerShell)
   Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*WSL2*" }
   ```

### Port Check Says Closed But Server is Running

**Cause:** Server might be bound to `127.0.0.1` instead of `0.0.0.0`

**Solution:**
```bash
# Check what the server is bound to
ss -tlnp | grep :3000

# Good output (listening on all interfaces):
# 0.0.0.0:3000

# Bad output (only localhost):
# 127.0.0.1:3000
```

### Get More Debug Info

```python
from networks import get_network_info
import json

# Get all network details
info = get_network_info()
print(json.dumps(info, indent=2, default=str))
```

```bash
# CLI version
networks info --json | jq .
```

## API Reference

### Functions

#### `get_lan_ip() -> Optional[str]`

Get the primary LAN-accessible IP address.

**Returns:** IP address string (e.g., `"192.168.50.100"`) or `None` if not found

**Example:**
```python
ip = get_lan_ip()
print(f"Server at: http://{ip}:3000")
```

---

#### `get_all_ips() -> List[Dict[str, str]]`

Get all network interfaces and their IP addresses.

**Returns:** List of dicts with `'interface'` and `'ip'` keys

**Example:**
```python
for iface in get_all_ips():
    print(f"{iface['interface']}: {iface['ip']}")
```

---

#### `get_network_info() -> Dict[str, Any]`

Get comprehensive network information.

**Returns:** Dict with keys:
- `lan_ip` (str): Primary LAN IP
- `all_ips` (List[Dict]): All interfaces
- `hostname` (str): System hostname
- `is_wsl` (bool): True if WSL2
- `wsl_host_ip` (Optional[str]): Windows host IP (WSL2 only)

**Example:**
```python
info = get_network_info()
if info['is_wsl']:
    print(f"WSL2 - Windows host: {info['wsl_host_ip']}")
```

---

#### `ensure_port_accessible(port: int, protocol: str = 'tcp', name: Optional[str] = None) -> Tuple[bool, str]`

Ensure a port is accessible on the LAN.

Handles platform-specific requirements:
- **WSL2**: Port forwarding + Windows Firewall
- **Windows**: Firewall rule
- **Linux**: ufw/firewalld configuration

**Args:**
- `port` (int): Port number
- `protocol` (str): `'tcp'` or `'udp'` (default: `'tcp'`)
- `name` (Optional[str]): Name for firewall rule

**Returns:** `(success: bool, message: str)`

**Example:**
```python
success, msg = ensure_port_accessible(3000, name='webapp')
if success:
    print(msg)
else:
    print(f"Failed: {msg}")
```

---

#### `check_port_open(host: str, port: int, timeout: float = 2.0) -> bool`

Check if a port is open on a host.

**Args:**
- `host` (str): Hostname or IP address
- `port` (int): Port number
- `timeout` (float): Connection timeout in seconds

**Returns:** `True` if port is open, `False` otherwise

**Example:**
```python
if check_port_open('192.168.1.100', 3000):
    print("Server is accessible")
```

---

#### `get_wsl2_host_ip() -> Optional[str]`

Get the Windows host IP address from WSL2.

**Returns:** Windows host IP or `None` if not in WSL2

**Example:**
```python
if get_wsl2_host_ip():
    print("Running in WSL2")
    print(f"Windows host: {get_wsl2_host_ip()}")
```

### CLI Commands

All CLI commands are available via `networks` or `netinfo`:

```bash
networks ip                               # Get LAN IP
networks info [--json]                    # Show network info
networks ensure -p PORT -n NAME [-t tcp]  # Make port accessible
networks check -H HOST -p PORT [-t 2.0]   # Check if port is open
networks wsl-host                         # Get WSL2 Windows host IP
```

## Dependencies

- **cross_platform** module (for OS detection)
- **Python 3.8+**
- **WSL2**: PowerShell access (included by default)
- **Linux**: Optional: `ufw` or `firewalld` for firewall management

## License

Part of the scripts repository.

## See Also

- [cross_platform module](../cross_platform/README.md) - OS detection and utilities
- [orchestrator_web_viewer](../orchestrator_web_viewer/README.md) - Web UI that uses networks module
