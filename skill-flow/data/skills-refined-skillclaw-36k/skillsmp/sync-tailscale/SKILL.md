---
name: sync-tailscale
description: Sync Tailscale IP addresses from API to inventory.yaml
---

# Sync Tailscale IPs

Fetch Tailscale device IPs and update inventory.yaml with tailscale_address attributes.

## Task

1. Fetch devices from Tailscale API:
```bash
curl -H "Authorization: Bearer {{ tailscale_api_key }}" \
  https://api.tailscale.com/api/v2/tailnet/-/devices | jq .
```

2. Extract hostname → IPv4 mapping from the devices array

3. Update inventory.yaml with tailscale_address attributes for matching hosts

## Inventory Structure

File: `inventory.yaml`

Format:
```yaml
groupname:
  hosts:
    hostname:
      ansible_host: 192.168.x.x
      tailscale_address: 100.x.x.x  # Add or update this
      exporter_port: 9100
```

## Rules

- Match on hostname (case-insensitive)
- Use IPv4 address (not IPv6)
- Add tailscale_address after ansible_host if missing
- Update existing tailscale_address if IP changed
- Preserve YAML formatting and structure
- Report what was added/updated

## API Key

The API key is stored encrypted in `secrets.yml` as `tailscale_api_key`. Decrypt with:
```bash
ansible-vault view secrets.yml | grep -A 5 tailscale_api_key
```
