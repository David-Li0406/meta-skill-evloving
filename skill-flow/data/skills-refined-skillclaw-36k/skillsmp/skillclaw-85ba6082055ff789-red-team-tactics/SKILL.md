---
name: red-team-tactics
description: Use this skill when you need to understand and apply red team tactics based on the MITRE ATT&CK framework for adversary simulation.
---

# Red Team Tactics

> Adversary simulation principles based on the MITRE ATT&CK framework.

## 1. MITRE ATT&CK Phases

### Attack Lifecycle

```
RECONNAISSANCE → INITIAL ACCESS → EXECUTION → PERSISTENCE
       ↓              ↓              ↓            ↓
   PRIVILEGE ESC → DEFENSE EVASION → CRED ACCESS → DISCOVERY
       ↓              ↓              ↓            ↓
LATERAL MOVEMENT → COLLECTION → C2 → EXFILTRATION → IMPACT
```

### Phase Objectives

| Phase                    | Objective                |
| ------------------------ | ------------------------ |
| **Recon**                | Map attack surface       |
| **Initial Access**       | Get first foothold       |
| **Execution**            | Run code on target       |
| **Persistence**          | Survive reboots          |
| **Privilege Escalation** | Get admin/root           |
| **Defense Evasion**      | Avoid detection          |
| **Credential Access**    | Harvest credentials      |
| **Discovery**            | Map internal network     |
| **Lateral Movement**     | Spread to other systems  |
| **Collection**           | Gather target data       |
| **C2**                   | Maintain command channel |
| **Exfiltration**         | Extract data             |

## 2. Reconnaissance Principles

### Passive vs Active

| Type        | Trade-off                           |
| ----------- | ----------------------------------- |
| **Passive** | No target contact, limited info     |
| **Active**  | Direct contact, more detection risk |

### Information Targets

| Category         | Value                   |
| ---------------- | ----------------------- |
| Technology stack | Attack vector selection |
| Employee info    | Social engineering      |
| Network ranges   | Scanning scope          |
| Third parties    | Supply chain attack     |

## 3. Initial Access Vectors

### Selection Criteria

| Vector                | When to Use                 |
| --------------------- | --------------------------- |
| **Phishing**          | Human target, email access  |
| **Public exploits**   | Vulnerable services exposed  |
| **Valid credentials** | Leaked or cracked           |
| **Supply chain**      | Third-party access          |

## 4. Privilege Escalation Principles

### Windows Targets

| Check                    | Opportunity                |
|------------------------- |--------------------------- |
| Unquoted service paths   | Write to path              |
| Weak service permissions  | Modify service             |
| Token privileges          | Abuse SeDebug, etc.       |
| Stored credentials        | Harvest                    |

### Linux Targets

| Check                    | Opportunity                |
|------------------------- |--------------------------- |
| SUID binaries            | Execute as owner           |
| Sudo misconfiguration     | Command execution          |
| Kernel vulnerabilities    | Kernel exploits            |
| Cron jobs                | Writable scripts           |

## 5. Defense Evasion Principles

### Key Techniques

| Technique | Purpose |
|-----------|---------|
| ...       | ...     |