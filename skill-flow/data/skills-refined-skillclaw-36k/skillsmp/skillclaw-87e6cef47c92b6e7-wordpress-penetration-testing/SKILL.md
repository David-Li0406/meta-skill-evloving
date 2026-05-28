---
name: wordpress-penetration-testing
description: Use this skill when you need to conduct security assessments on WordPress installations, including vulnerability scanning, user enumeration, and exploitation techniques.
---

# Skill body

## Purpose

Conduct comprehensive security assessments of WordPress installations, including enumeration of users, themes, and plugins, vulnerability scanning, credential attacks, and exploitation techniques. WordPress powers approximately 35% of websites, making it a critical target for security testing.

## Prerequisites

### Required Tools
- WPScan (pre-installed in Kali Linux)
- Metasploit Framework
- Burp Suite or OWASP ZAP
- Nmap for initial discovery
- cURL or wget

### Required Knowledge
- WordPress architecture and structure
- Web application testing fundamentals
- HTTP protocol understanding
- Common web vulnerabilities (OWASP Top 10)

## Outputs and Deliverables

1. **WordPress Enumeration Report** - Version, themes, plugins, users
2. **Vulnerability Assessment** - Identified CVEs and misconfigurations
3. **Credential Assessment** - Weak password findings
4. **Exploitation Proof** - Shell access documentation

## Core Workflow

### Phase 1: WordPress Discovery

Identify WordPress installations:

```bash
# Check for WordPress indicators
curl -s http://target.com | grep -i wordpress
curl -s http://target.com | grep -i "wp-content"
curl -s http://target.com | grep -i "wp-includes"

# Check common WordPress paths
curl -I http://target.com/wp-login.php
curl -I http://target.com/wp-admin/
curl -I http://target.com/wp-content/
curl -I http://target.com/xmlrpc.php

# Check meta generator tag
curl -s http://target.com | grep "generator"

# Nmap WordPress detection
nmap -p 80,443 --script http-wordpress-enum target.com
```

Key WordPress files and directories:
- `/wp-admin/` - Admin dashboard
- `/wp-login.php` - Login page
- `/wp-content/` - Themes, plugins, uploads
- `/wp-includes/` - Core files
- `/xmlrpc.php` - XML-RPC interface
- `/wp-config.php` - Configuration (not accessible if secure)
- `/readme.html` - Version information

### Phase 2: Basic WPScan Enumeration

Comprehensive WordPress scanning with WPScan:

```bash
# Basic scan
wpscan --url http://target.com/wordpress/

# With API token (for vulnerability data)
wpscan --url http://target.com --api-token YOUR_API_TOKEN
```

### Phase 3: Vulnerability Scanning and Exploitation

Conduct vulnerability scanning and attempt exploitation based on findings. Document all steps and results for reporting.

```bash
# Example of exploiting a known vulnerability
# (Insert specific exploitation commands here)
```