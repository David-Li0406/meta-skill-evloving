# Infrastructure Inventory

This file contains the authoritative list of infrastructure IPs and paths. Update here if infrastructure changes.

## Network Layout

```
Internet
    │
    ▼
Cloudflare (DNS + Tunnel)
    │ *.lakehouse.wtf
    ▼
┌─────────────────────────────────────┐
│ AdGuard DNS (Internal Override)     │
│ *.internal.lakehouse.wtf → Traefik  │
└─────────────────────────────────────┘
    │
    ▼
Traefik Reverse Proxy (192.168.1.110)
    │ TLS termination, routing
    ▼
Backend Services (LXC or Standalone)
```

## Proxmox HA Cluster

| Node | IP | Hostname |
|------|-----|----------|
| Primary | 192.168.1.137 | proxmox |
| Secondary | 192.168.1.125 | proxmox2 |
| Tertiary | 192.168.1.126 | proxmox3 |

**Web UI:** https://proxmox.internal.lakehouse.wtf:8006

```bash
# Check cluster status
ssh root@192.168.1.137 "pvecm status"

# Check node resources
for node in 192.168.1.137 192.168.1.125 192.168.1.126; do
  echo "=== $node ===" 
  ssh root@$node "pct list | wc -l && free -h | grep Mem"
done
```

## DHCP - Kea (HA Pair)

| Role | IP | Config Path |
|------|-----|-------------|
| Primary | 192.168.1.133 | `/etc/kea/kea-dhcp4.conf` |
| Secondary | 192.168.1.134 | `/etc/kea/kea-dhcp4.conf` |

**Service name:** `isc-kea-dhcp4-server`

**Reservation JSON format:**
```json
{
  "hw-address": "XX:XX:XX:XX:XX:XX",
  "ip-address": "192.168.1.XXX",
  "hostname": "service-name"
}
```

**Location in config:** `Dhcp4.subnet4[].reservations` array (find the 192.168.1.0/24 subnet)

```bash
# View current reservations
ssh root@192.168.1.133 "jq '.Dhcp4.subnet4[0].reservations' /etc/kea/kea-dhcp4.conf"

# Validate config syntax
ssh root@192.168.1.133 "kea-dhcp4 -t /etc/kea/kea-dhcp4.conf"

# Reload after changes (both servers!)
ssh root@192.168.1.133 "systemctl reload isc-kea-dhcp4-server"
ssh root@192.168.1.134 "systemctl reload isc-kea-dhcp4-server"
```

## DNS - AdGuard Home (HA Pair)

| Role | IP | Config Path |
|------|-----|-------------|
| Primary | 192.168.1.253 | `/opt/AdGuardHome/AdGuardHome.yaml` |
| Secondary | 192.168.1.224 | `/opt/AdGuardHome/AdGuardHome.yaml` |

**Web UIs:**
- Primary: http://192.168.1.253:3000
- Secondary: http://192.168.1.224:3000

**Rewrite YAML format:**
```yaml
rewrites:
  - domain: service.internal.lakehouse.wtf
    answer: 192.168.1.110
```

**Note:** Rewrites point to Traefik (192.168.1.110) for services proxied through Traefik. For standalone hardware bypassing Traefik, point directly to the hardware IP.

```bash
# View current rewrites
ssh root@192.168.1.253 "grep -A 200 'rewrites:' /opt/AdGuardHome/AdGuardHome.yaml | head -100"

# Test DNS resolution
dig +short service.internal.lakehouse.wtf @192.168.1.253

# Restart after changes (both servers!)
ssh root@192.168.1.253 "systemctl restart AdGuardHome"
ssh root@192.168.1.224 "systemctl restart AdGuardHome"
```

## Reverse Proxy - Traefik

| Property | Value |
|----------|-------|
| LXC ID | 110 |
| IP | 192.168.1.110 |
| Version | 3.0.0 |
| Dashboard | https://traefik.internal.lakehouse.wtf |

**Configuration Files:**
| File | Purpose |
|------|---------|
| `/etc/traefik/traefik.yml` | Static config (entrypoints, providers) |
| `/etc/traefik/dynamic/routers.yml` | HTTP routers (Host rules) |
| `/etc/traefik/dynamic/services.yml` | Backend services (URLs) |
| `/etc/traefik/dynamic/middlewares.yml` | Middleware chains |
| `/var/log/traefik/traefik.log` | Logs |

```bash
# Reload config (no restart needed for dynamic files)
ssh root@192.168.1.110 "systemctl reload traefik"

# Check config validity
ssh root@192.168.1.110 "traefik healthcheck"

# View logs
ssh root@192.168.1.110 "tail -f /var/log/traefik/traefik.log"

# List all routers via API
curl -sk https://traefik.internal.lakehouse.wtf/api/http/routers | jq '.[].name'

# List all services via API
curl -sk https://traefik.internal.lakehouse.wtf/api/http/services | jq '.[].name'

# Check specific service health
curl -sk https://traefik.internal.lakehouse.wtf/api/http/services | jq '.[] | select(.name | contains("SERVICE_NAME"))'
```

## Monitoring - Uptime Kuma

| Property | Value |
|----------|-------|
| LXC ID | 132 |
| IP | 192.168.1.132 |
| URL | https://uptime.internal.lakehouse.wtf |

**Monitor Types:** HTTP(s), TCP, Ping, DNS, Docker, and more

**Standard settings for new monitors:**
- Type: HTTP(s)
- Interval: 60 seconds
- Retries: 3
- Timeout: 30 seconds

## Dashboard - Homepage

| Property | Value |
|----------|-------|
| LXC ID | 150 |
| IP | 192.168.1.45 |
| Config Dir | `/home/homepage/homepage/config/` |

**Key files:**
- `services.yaml` - Service links
- `settings.yaml` - Dashboard settings
- `widgets.yaml` - Widget config

```bash
# Edit services
ssh root@192.168.1.45 "vim /home/homepage/homepage/config/services.yaml"

# Restart to apply changes
ssh root@192.168.1.45 "cd /home/homepage/homepage && docker compose restart"
```

## Existing Services Reference

| Service | LXC ID | IP | Port | Health Path |
|---------|--------|-----|------|-------------|
| Traefik | 110 | 192.168.1.110 | 443 | /ping |
| Uptime Kuma | 132 | 192.168.1.132 | 3001 | / |
| Homepage | 150 | 192.168.1.45 | 3000 | / |
| Grafana | - | 192.168.1.140 | 3000 | /api/health |
| Memos | - | 192.168.1.144 | 9030 | / |
| Hoarder | - | 192.168.1.102 | 3000 | / |
| Tandoor | 108 | 192.168.1.108 | 8002 | / |
| NetBox | - | 192.168.1.xxx | 8000 | /api/ |
| Wiki.js | - | 192.168.1.xxx | 3000 | / |
| ESPHome | - | 192.168.1.xxx | 6052 | / |
| Zigbee2MQTT | - | 192.168.1.xxx | 8080 | / |

## IP Address Ranges

| Range | Purpose |
|-------|---------|
| 192.168.1.1-99 | Network infrastructure, IoT |
| 192.168.1.100-149 | LXC containers (services) |
| 192.168.1.150-199 | Reserved / future expansion |
| 192.168.1.200-254 | Standalone hardware, DHCP pool |
