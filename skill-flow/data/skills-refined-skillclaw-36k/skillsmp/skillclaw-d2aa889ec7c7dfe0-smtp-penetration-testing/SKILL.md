---
name: smtp-penetration-testing
description: Use this skill when you need to perform SMTP penetration testing, including user enumeration, testing for open mail relays, grabbing SMTP banners, brute forcing email credentials, or assessing mail server security.
---

# SMTP Penetration Testing

## Purpose

Conduct comprehensive security assessments of SMTP (Simple Mail Transfer Protocol) servers to identify vulnerabilities including open relays, user enumeration, weak authentication, and misconfiguration. This skill covers banner grabbing, user enumeration techniques, relay testing, brute force attacks, and security hardening recommendations.

## Prerequisites

### Required Tools
```bash
# Nmap with SMTP scripts
sudo apt-get install nmap

# Netcat
sudo apt-get install netcat

# Hydra for brute force
sudo apt-get install hydra

# SMTP user enumeration tool
sudo apt-get install smtp-user-enum

# Metasploit Framework
msfconsole
```

### Required Knowledge
- SMTP protocol fundamentals
- Email architecture (MTA, MDA, MUA)
- DNS and MX records
- Network protocols

### Required Access
- Target SMTP server IP/hostname
- Written authorization for testing
- Wordlists for enumeration and brute force

## Outputs and Deliverables

1. **SMTP Security Assessment Report** - Comprehensive vulnerability findings
2. **User Enumeration Results** - Valid email addresses discovered
3. **Relay Test Results** - Open relay status and exploitation potential
4. **Remediation Recommendations** - Security hardening guidance

## Core Workflow

### Phase 1: SMTP Architecture Understanding

```
Components: MTA (transfer) → MDA (delivery) → MUA (client)

Ports: 25 (SMTP), 465 (SMTPS), 587 (submission), 2525 (alternative)

Workflow: Sender MUA → Sender MTA → DNS/MX → Recipient MTA → MDA → Recipient MUA
```

### Phase 2: SMTP Service Discovery

Identify SMTP servers and versions:

```bash
# Discover SMTP ports
nmap -p 25,465,587,2525 -sV TARGET_IP

# Aggressive service detection
nmap -sV -sC -p 25 TARGET_IP

# SMTP-specific scripts
nmap --script=smtp-* -p 25 TARGET_IP

# Discover MX records for domain
dig MX target.com
nslookup -type=mx target.com
host -t mx target.com
```

### Phase 3: Banner Grabbing

Retrieve SMTP server information:

```bash
# Using Telnet
telnet TARGET_IP 25
# Response: 220 mail.target.com ESMTP Postfix

# Using Netcat
nc TARGET_IP 25
# Response: 220 mail.target.com ESMTP
```