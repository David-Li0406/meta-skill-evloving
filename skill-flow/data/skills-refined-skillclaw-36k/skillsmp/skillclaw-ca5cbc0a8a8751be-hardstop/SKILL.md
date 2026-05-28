---
name: hardstop
description: Use this skill to protect users from executing dangerous shell commands or reading sensitive files by implementing a pre-execution safety protocol.
---

# Hardstop Skill v1.3

> **Note:** This skill complements the Hardstop plugin. The plugin provides deterministic protection via hooks; this skill provides LLM-level awareness for platforms without hook support.

**Purpose:** Protect users from dangerous AI-initiated actions. The mechanical brake for AI-generated commands.

**Core Question:** "If this action goes wrong, can the user recover?"

---

## MANDATORY: Pre-Execution Protocol

**BEFORE executing ANY shell command, ALWAYS run this checklist:**

```
[ ] 1. INSTANT BLOCK check (see list below)
[ ] 2. Risk level assessment (SAFE/RISKY/DANGEROUS)
[ ] 3. Signal confidence BEFORE action
[ ] 4. If RISKY or DANGEROUS -> Explain -> Wait for confirmation
```

**NEVER skip this protocol. NEVER proceed on DANGEROUS without explicit user approval.**

---

## 1. INSTANT BLOCK List

**These patterns require IMMEDIATE STOP. No exceptions. No "let me just..."**

### Unix/Linux/macOS

| Pattern | Why |
|---------|-----|
| `rm -rf ~/` or `rm -rf ~/*` | Deletes entire home directory |
| `rm -rf /` | Destroys entire system |
| `:(){ :\|:& };:` | Fork bomb, crashes system |
| `bash -i >& /dev/tcp/` | Reverse shell, attacker access |
| `nc -e /bin/sh` | Reverse shell variant |
| `curl/wget ... \| bash` | Executes untrusted remote code |
| `curl -d @~/.ssh/` | Exfiltrates SSH keys |
| `dd of=/dev/sd*` | Overwrites disk |
| `mkfs` on system drives | Formats drives |
| `> /dev/sda` | Destroys disk |
| `sudo rm -rf /` | Privileged system destruction |
| `chmod -R 777 /` | World-writable system |

#### Package Manager Force Operations

| Pattern | Why |
|---------|-----|
| `dpkg --purge --force-*` | Overrides package safety checks |
| `dpkg --remove --force-*` | Overrides package safety checks |
| `dpkg --force-remove-reinstreq` | Forces removal of broken package (can break system) |
| `dpkg --force-depends` | Ignores dependency checks |
| `dpkg --force-all` | Nuclear option - ignores all safety |
| `apt-get remove --force-*` | Overrides package safety checks |

#### Shell Wrappers

| Pattern | Why |
|---------|-----|
| `bash -c "rm -rf ..."` | Hides recursive delete in shell wrapper |
| `sh -c "... | bash"` | Executes untrusted code through a shell wrapper |

---

## 2. Risk Level Assessment

- **SAFE:** Command is safe to execute.
- **RISKY:** Command may have unintended consequences; explain risks and wait for user confirmation.
- **DANGEROUS:** Command poses a high risk of data loss or system damage; require explicit user approval before proceeding.

---

## 3. Signal Confidence

Always communicate your confidence level in the safety of the command before execution.

---

## 4. User Confirmation

If the command is assessed as RISKY or DANGEROUS, provide a detailed explanation of the risks involved and wait for user confirmation before proceeding.