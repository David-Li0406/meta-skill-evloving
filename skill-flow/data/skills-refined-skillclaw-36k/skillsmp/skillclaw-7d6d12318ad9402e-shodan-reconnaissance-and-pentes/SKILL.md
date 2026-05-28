---
name: shodan-reconnaissance-and-pentesting
description: Use this skill when you need to search for exposed devices on the internet, perform Shodan reconnaissance, find vulnerable services, scan IP ranges, or discover IoT devices and open ports.
---

# Skill body

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
# Output: Query credits available: 100
#         Scan credits available: 100
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
shodan host 1.1.1.1

# Example output:
# 1.1.1.1
# Hostnames: one.one.one.one
# Country: Australia
# Organization: Mountain View Communications
# Number of open ports: 3
# Ports:
#   53/udp
#   80/tcp
#   443/tcp
```