# Sysadmin Quality Checklist

## 🚨 Document Persistence (MANDATORY)

> [!CAUTION]
> **BEFORE handing off to another skill, you MUST:**

- [ ] **Final document exists in `docs/`** at the path defined in Artifact Ownership
- [ ] **AGENTS.md updated** with status ✅ Done and Last Updated date
- [ ] **Artifact synced** — if you used an artifact, copy final content to `docs/`

**Why?** Artifacts don't persist between sessions. Without `docs/` file, the next skill cannot continue.

Use this checklist when performing server administration tasks.

## 1. Security
- [ ] **SSH**: Key-only access enabled, password auth disabled?
- [ ] **Firewall**: UFW/iptables configured with minimal open ports?
- [ ] **fail2ban**: Installed and active for SSH?
- [ ] **Updates**: `apt update && apt upgrade` run recently?
- [ ] **Users**: No unnecessary root access? Proper sudo setup?

## 2. Backups (S3 Cold Storage)
> We use custom scripts with private S3 cold storage, NOT official TWC backups!

- [ ] **Scripts**: Backup/restore scripts in `examples/` adapted for site?
- [ ] **Cron**: Backup cron jobs configured on servers?
- [ ] **S3 Bucket**: Private cold storage bucket exists?
- [ ] **Rotation**: 7 daily + 4 weekly backups?
- [ ] **Tested**: Restoration tested in last quarter?
- [ ] **Credentials**: S3 access keys in environment (not hardcoded)?

## 3. Performance
- [ ] **Swap**: Configured on low-memory servers?
- [ ] **OPcache**: Enabled for PHP servers?
- [ ] **Object Cache**: Redis/Memcached configured where needed?
- [ ] **PHP-FPM**: Proper pool sizes for traffic?
- [ ] **Logs**: Log rotation configured?

## 4. Monitoring
- [ ] **Disk space**: Adequate free space (>20%)?
- [ ] **Memory**: Not swapping excessively?
- [ ] **Load average**: Normal for server capacity?

## 5. Timeweb Cloud
- [ ] **twc CLI**: Working and configured?
- [ ] **Billing**: Account in good standing?
- [ ] **DNS**: Records correct and propagated?

## 6. Documentation
- [ ] **Server purpose**: Documented in SKILL.md mappings?
- [ ] **Access**: SSH keys documented?
- [ ] **Config changes**: Logged with date and reason?

## Quick Commands

```bash
# Check server status
twc server list
ssh root@<IP> "uptime && df -h && free -h"

# S3 backup check
aws s3 ls s3://backups-cold/<SITE>/daily/ --endpoint-url=https://s3.twcstorage.ru

# Manual backup
./examples/backup-wordpress.sh truesharing 45.8.96.209

# Security check
ssh root@<IP> "fail2ban-client status sshd"
```
