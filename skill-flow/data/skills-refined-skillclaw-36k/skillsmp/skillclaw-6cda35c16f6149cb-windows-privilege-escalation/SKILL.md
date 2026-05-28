---
name: windows-privilege-escalation
description: Use this skill when you need to escalate privileges on Windows systems, find privilege escalation vectors, or exploit misconfigurations during penetration testing.
---

# Skill body

## Purpose

Provide systematic methodologies for discovering and exploiting privilege escalation vulnerabilities on Windows systems during penetration testing engagements. This skill covers system enumeration, credential harvesting, service exploitation, token impersonation, kernel exploits, and various misconfigurations that enable escalation from standard user to Administrator or SYSTEM privileges.

## Inputs / Prerequisites

- **Initial Access**: Shell or RDP access as standard user on Windows system
- **Enumeration Tools**: WinPEAS, PowerUp, Seatbelt, or manual commands
- **Exploit Binaries**: Pre-compiled exploits or ability to transfer tools
- **Knowledge**: Understanding of Windows security model and privileges
- **Authorization**: Written permission for penetration testing activities

## Outputs / Deliverables

- **Privilege Escalation Path**: Identified vector to higher privileges
- **Credential Dump**: Harvested passwords, hashes, or tokens
- **Elevated Shell**: Command execution as Administrator or SYSTEM
- **Vulnerability Report**: Documentation of misconfigurations and exploits
- **Remediation Recommendations**: Fixes for identified weaknesses

## Core Workflow

### 1. System Enumeration

#### Basic System Information
```powershell
# OS version and patches
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
wmic qfe

# Architecture
wmic os get osarchitecture
echo %PROCESSOR_ARCHITECTURE%

# Environment variables
set
Get-ChildItem Env: | ft Key,Value

# List drives
wmic logicaldisk get caption,description,providername
```

#### User Enumeration
```powershell
# Current user
whoami
echo %USERNAME%

# User privileges
whoami /priv
whoami /groups
whoami /all

# All users
net user
Get-LocalUser | ft Name,Enabled,LastLogon

# User details
net user administrator
net user %USERNAME%

# Local groups
net localgroup
net localgroup administrators
Get-LocalGroupMember Administrators | ft Name,PrincipalSource
```

#### Network Enumeration
```powershell
# Network interfaces
ipconfig /all
Get-NetIPConf
```