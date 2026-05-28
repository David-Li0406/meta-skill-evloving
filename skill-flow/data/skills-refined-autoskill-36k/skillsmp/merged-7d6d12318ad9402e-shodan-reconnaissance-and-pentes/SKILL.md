---
name: shodan-reconnaissance-and-pentesting
description: Use this skill when you need to search for exposed devices on the internet, perform Shodan reconnaissance, find vulnerable services, scan IP ranges, or discover IoT devices and open ports.
---

# Shodan Reconnaissance and Pentesting

## Purpose

Provide systematic methodologies for leveraging Shodan as a reconnaissance tool during penetration testing engagements. This skill covers the Shodan web interface, command-line interface (CLI), REST API, search filters, on-demand scanning, and network monitoring capabilities for discovering exposed services, vulnerable systems, and IoT devices.

## Inputs / Prerequisites

- **Shodan Account**: Free or paid account at shodan.io
- **API Key**: Obtained from Shodan account dashboard
- **Target Information**: IP addresses, domains, or network ranges to investigate
- **Shodan CLI**: Python-based command-line tool installed
- **Authorization**: Written permission for reconnaissance on target networks

## Outputs / Deliverables

- **Asset Inventory**: List of discovered hosts, ports, and services
- **Vulnerability Report**: Identified CVEs and exposed vulnerable services
- **Banner Data**: Service banners revealing software versions
- **Network Mapping**: Geographic and organizational distribution of assets
- **Screenshot Gallery**: Visual reconnaissance of exposed interfaces
- **Exported Data**: JSON/CSV files for further analysis

## Core Workflow

### 1. Setup and Configuration

#### Install Shodan CLI
```bash
# Using pip
pip install shodan

# Or easy_install
easy_install shodan

# On BlackArch/Arch Linux
sudo pacman -S python-shodan
```

#### Initialize API Key
```bash
# Set your API key
shodan init YOUR_API_KEY

# Verify setup
shodan info
```

#### Check Account Status
```bash
# View credits and plan info
shodan info

# Check your external IP
shodan myip

# Check CLI version
shodan version
```

### 2. Basic Host Reconnaissance

#### Query Single Host
```bash
# Get all information about an IP
shodan host <ip_address>
```

#### Check if Host is Honeypot
```bash
# Get honeypot probability score
shodan honeyscore <ip_address>
```

### 3. Search Queries

#### Basic Search (Free)
```bash
# Simple keyword search (no credits consumed)
shodan search <keyword>
```

#### Filtered Search (1 Credit)
```bash
# Product-specific search
shodan search product:<product_name>

# Search with multiple filters
shodan search product:<product_name> country:<country_code> city:<city_name>
```

#### Count Results
```bash
# Get result count without consuming credits
shodan count <query>
```

#### Download Results
```bash
# Download results
shodan download <filename.json.gz> "<query>"
```

#### Parse Downloaded Data
```bash
# Extract specific fields from downloaded data
shodan parse --fields <fields> <filename.json.gz>
```

### 4. Search Filters Reference

#### Network Filters
```
ip:<ip_address>                  # Specific IP address
net:<network_range>              # Network range (CIDR)
hostname:<hostname>              # Hostname contains
port:<port_number>               # Specific port
asn:<asn_number>                 # Autonomous System Number
```

#### Geographic Filters
```
country:<country_code>           # Two-letter country code
city:<city_name>                 # City name
state:<state_code>               # State/region
```

#### Organization Filters
```
org:<organization_name>          # Organization name
```

#### Service/Product Filters
```
product:<product_name>           # Software product
version:<version_number>         # Software version
```

#### Vulnerability Filters
```
vuln:<CVE_ID>                    # Specific CVE
```

#### Screenshot Filters
```
has_screenshot:true              # Has screenshot available
```

### 5. On-Demand Scanning

#### Submit Scan
```bash
# Scan single IP (1 credit per IP)
shodan scan submit <ip_address>
```

#### Monitor Scan Status
```bash
# List recent scans
shodan scan list

# Check specific scan status
shodan scan status <SCAN_ID>
```

### 6. Statistics and Analysis

#### Get Search Statistics
```bash
# Default statistics (top 10 countries, orgs)
shodan stats <query>
```

### 7. Network Monitoring

#### Setup Alerts (Web Interface)
```
1. Navigate to Monitor Dashboard
2. Add IP, range, or domain to monitor
3. Configure notification service (email, Slack, webhook)
4. Select trigger events (new service, vulnerability, etc.)
5. View dashboard for exposed services
```

### 8. REST API Usage

#### Direct API Calls
```bash
# Get API info
curl -s "https://api.shodan.io/api-info?key=YOUR_KEY" | jq

# Host lookup
curl -s "https://api.shodan.io/shodan/host/<ip_address>?key=YOUR_KEY" | jq

# Search query
curl -s "https://api.shodan.io/shodan/host/search?key=YOUR_KEY&query=<query>" | jq
```

#### Python Library
```python
import shodan

api = shodan.Shodan('YOUR_API_KEY')

# Search
results = api.search('<query>')
print(f'Results found: {results["total"]}')
for result in results['matches']:
    print(f'IP: {result["ip_str"]}')

# Host lookup
host = api.host('<ip_address>')
print(f'IP: {host["ip_str"]}')
```

## Quick Reference

### Essential CLI Commands

| Command | Description | Credits |
|---------|-------------|---------|
| `shodan init KEY` | Initialize API key | 0 |
| `shodan info` | Show account info | 0 |
| `shodan myip` | Show your IP | 0 |
| `shodan host IP` | Host details | 0 |
| `shodan count QUERY` | Result count | 0 |
| `shodan search QUERY` | Basic search | 0* |
| `shodan download FILE QUERY` | Save results | 1/100 results |
| `shodan parse FILE` | Extract data | 0 |
| `shodan stats QUERY` | Statistics | 1 |
| `shodan scan submit IP` | On-demand scan | 1/IP |
| `shodan honeyscore IP` | Honeypot check | 0 |

*Filters consume 1 credit per query

### Common Search Queries

| Purpose | Query |
|---------|-------|
| Find webcams | `webcam has_screenshot:true` |
| MongoDB databases | `product:mongodb` |
| Vulnerable RDP | `port:3389 vuln:CVE-2019-0708` |

### Credit System

| Action | Credit Type | Cost |
|--------|-------------|------|
| Basic search | Query | 0 (no filters) |
| Filtered search | Query | 1 |
| Download 100 results | Query | 1 |
| Scan 1 IP | Scan | 1 |

## Constraints and Limitations

### Operational Boundaries
- Rate limited to 1 request per second
- Scan results not immediate (asynchronous)
- Free accounts have limited credits

### Legal Requirements
- Only perform reconnaissance on authorized targets
- Document all reconnaissance activities

## Examples

### Example 1: Organization Reconnaissance
```bash
# Find all hosts belonging to target organization
shodan search 'org:"Target Company"'
```

### Example 2: Vulnerable Service Discovery
```bash
# Find hosts vulnerable to BlueKeep (RDP CVE)
shodan search 'vuln:CVE-2019-0708 country:US'
```

### Example 3: IoT Device Discovery
```bash
# Find exposed webcams
shodan search 'webcam has_screenshot:true country:US'
```

### Example 4: SSL/TLS Certificate Analysis
```bash
# Find hosts with specific SSL cert
shodan search 'ssl.cert.subject.cn:*.example.com'
```

### Example 5: Python Automation Script
```python
#!/usr/bin/env python3
import shodan

API_KEY = 'YOUR_API_KEY'
api = shodan.Shodan(API_KEY)

def recon_organization(org_name):
    """Perform reconnaissance on an organization"""
    try:
        query = f'org:"{org_name}"'
        results = api.search(query)
        print(f"[*] Found {results['total']} hosts for {org_name}")
    except shodan.APIError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    recon_organization("Target Company")
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No API Key Configured | Key not initialized | Run `shodan init YOUR_API_KEY` |
| Query Credits Exhausted | Monthly credits consumed | Use credit-free queries (no filters) |
| Rate Limit Exceeded | >1 request/second | Add `time.sleep(1)` between API requests |