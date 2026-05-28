---
name: security-scanning-tools
description: Use this skill when you need to perform vulnerability scanning, assess web application security, scan networks for open ports, or evaluate system compliance.
---

# Security Scanning Tools

## Purpose

Master essential security scanning tools for network discovery, vulnerability assessment, web application testing, wireless security, and compliance validation. This skill covers tool selection, configuration, and practical usage across different scanning categories.

## Prerequisites

### Required Environment
- Linux-based system (Kali Linux recommended)
- Network access to target systems
- Proper authorization for scanning activities

### Required Knowledge
- Basic networking concepts (TCP/IP, ports, protocols)
- Understanding of common vulnerabilities
- Familiarity with command-line interfaces

## Outputs and Deliverables

1. **Network Discovery Reports** - Identified hosts, ports, and services
2. **Vulnerability Assessment Reports** - CVEs, misconfigurations, risk ratings
3. **Web Application Security Reports** - OWASP Top 10 findings
4. **Compliance Reports** - CIS benchmarks, PCI-DSS, HIPAA checks

## Core Workflow

### Phase 1: Network Scanning Tools

#### Nmap (Network Mapper)

Primary tool for network discovery and security auditing:

```bash
# Host discovery
nmap -sn 192.168.1.0/24              # Ping scan (no port scan)
nmap -sL 192.168.1.0/24              # List scan (DNS resolution)
nmap -Pn 192.168.1.100               # Skip host discovery

# Port scanning techniques
nmap -sS 192.168.1.100               # TCP SYN scan (stealth)
nmap -sT 192.168.1.100               # TCP connect scan
nmap -sU 192.168.1.100               # UDP scan
nmap -sA 192.168.1.100               # ACK scan (firewall detection)

# Port specification
nmap -p 80,443 192.168.1.100         # Specific ports
nmap -p- 192.168.1.100               # All 65535 ports
nmap -p 1-1000 192.168.1.100         # Port range
nmap --top-ports 100 192.168.1.100   # Top 100 common ports

# Service and OS detection
nmap -sV 192.168.1.100               # Service version detection
nmap -O 192.168.1.100                # OS detection
nmap -A 192.168.1.100                # Aggressive (OS, version, scripts)

# Timing and performance
nmap -T0 192.168.1.100               # Paranoid (slowest)
```