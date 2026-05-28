---
name: metasploit-framework
description: Use this skill when you need to leverage the Metasploit Framework for penetration testing, including exploiting vulnerabilities, creating payloads, and performing post-exploitation activities.
---

# Skill body

## Purpose

Leverage the Metasploit Framework for comprehensive penetration testing, from initial exploitation through post-exploitation activities. Metasploit provides a unified platform for vulnerability exploitation, payload generation, auxiliary scanning, and maintaining access to compromised systems during authorized security assessments.

## Prerequisites

### Required Tools
```bash
# Metasploit comes pre-installed on Kali Linux
# For other systems:
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall

# Start PostgreSQL for database support
sudo systemctl start postgresql
sudo msfdb init
```

### Required Knowledge
- Network and system fundamentals
- Understanding of vulnerabilities and exploits
- Basic programming concepts
- Target enumeration techniques

### Required Access
- Written authorization for testing
- Network access to target systems
- Understanding of scope and rules of engagement

## Outputs and Deliverables

1. **Exploitation Evidence** - Screenshots and logs of successful compromises
2. **Session Logs** - Command history and extracted data
3. **Vulnerability Mapping** - Exploited vulnerabilities with CVE references
4. **Post-Exploitation Artifacts** - Credentials, files, and system information

## Core Workflow

### Phase 1: MSFConsole Basics

Launch and navigate the Metasploit console:

```bash
# Start msfconsole
msfconsole

# Quiet mode (skip banner)
msfconsole -q

# Basic navigation commands
msf6 > help                    # Show all commands
msf6 > search [term]           # Search modules
msf6 > use [module]            # Select module
msf6 > info                    # Show module details
msf6 > show options            # Display required options
msf6 > set [OPTION] [value]    # Configure option
msf6 > run / exploit           # Execute module
msf6 > back                    # Return to main console
msf6 > exit                    # Exit msfconsole
```

### Phase 2: Module Types

(Additional details on module types and usage can be added here as needed.)