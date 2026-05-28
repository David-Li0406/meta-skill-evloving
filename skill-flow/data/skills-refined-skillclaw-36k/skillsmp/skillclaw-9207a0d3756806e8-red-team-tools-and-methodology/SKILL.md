---
name: red-team-tools-and-methodology
description: Use this skill when you need to implement proven methodologies and workflows for effective reconnaissance, vulnerability discovery, and bug bounty hunting.
---

# Skill body

## Purpose

Implement proven methodologies and tool workflows from top security researchers for effective reconnaissance, vulnerability discovery, and bug bounty hunting. Automate common tasks while maintaining thorough coverage of attack surfaces.

## Inputs/Prerequisites

- Target scope definition (domains, IP ranges, applications)
- Linux-based attack machine (Kali, Ubuntu)
- Bug bounty program rules and scope
- Tool dependencies installed (Go, Python, Ruby)
- API keys for various services (Shodan, Censys, etc.)

## Outputs/Deliverables

- Comprehensive subdomain enumeration
- Live host discovery and technology fingerprinting
- Identified vulnerabilities and attack vectors
- Automated recon pipeline outputs
- Documented findings for reporting

## Core Workflow

### 1. Project Tracking and Acquisitions

Set up reconnaissance tracking:

```bash
# Create project structure
mkdir -p target/{recon,vulns,reports}
cd target

# Find acquisitions using Crunchbase
# Search manually for subsidiary companies

# Get ASN for targets
amass intel -org "Target Company" -src

# Alternative ASN lookup
curl -s "https://bgp.he.net/search?search=targetcompany&commit=Search"
```

### 2. Subdomain Enumeration

Comprehensive subdomain discovery:

```bash
# Create wildcards file
echo "target.com" > wildcards

# Run Amass passively
amass enum -passive -d target.com -src -o amass_passive.txt

# Run Amass actively
amass enum -active -d target.com -src -o amass_active.txt

# Use Subfinder
subfinder -d target.com -silent -o subfinder.txt

# Asset discovery
cat wildcards | assetfinder --subs-only | anew domains.txt

# Alternative subdomain tools
findomain -t target.com -o

# Generate permutations with dnsgen
cat domains.txt | dnsgen - | httprobe > permuted.txt

# Combine all sources
cat amass_*.txt subfinder.txt | sort -u > all_subs.txt
```

### 3. Live Host Discovery

Identify responding hosts:

```bash
# Check which hosts are live with httprobe
cat domains.txt | httprobe -c 80 --prefer-https | anew hosts.txt

# Use httpx for more details
cat domains.txt | httpx -title -tech-detect -status-code -o live_hosts.txt
```