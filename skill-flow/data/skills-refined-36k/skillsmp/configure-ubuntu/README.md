# Configure Ubuntu Skill

## Overview

This skill provides comprehensive guidance for configuring Ubuntu 24.04 LTS servers, with emphasis on cloud-init automation for Azure VM provisioning. It documents patterns, best practices, and common pitfalls discovered during the stage-iaas-flask reference implementation.

## Skill Contents

### SKILL.md (10KB)

Main skill documentation covering:
- When to use this skill
- Cloud-init overview and structure
- Common configuration patterns (bastion, proxy, app server)
- systemd service patterns
- File permissions reference
- Testing and verification procedures

**Start here** for quick reference and common patterns.

### references/cloud-init-patterns.md (13KB)

Detailed cloud-init documentation:
- Basic structure and syntax
- Module execution order
- Package management
- File creation with permissions
- Running commands (runcmd)
- Complete working examples
- Debugging cloud-init
- Integration with Azure Bicep

**Use for** understanding cloud-init deeply or troubleshooting configuration issues.

### references/systemd-patterns.md (15KB)

Comprehensive systemd service documentation:
- Service unit file structure
- Service types (simple, forking, oneshot)
- Environment configuration
- Restart policies
- User and group configuration
- Complete working examples
- Managing services (enable, start, status)
- Debugging failed services

**Use for** creating or troubleshooting systemd services.

### references/common-pitfalls.md (17KB)

Catalog of common mistakes and solutions:
- Critical cloud-init issues
- systemd service problems
- File permission errors
- SSH and networking issues
- Database configuration problems
- Python virtual environment gotchas
- Security issues

**Use for** preventing common mistakes or debugging known issues.

## Quick Start

### Creating a Cloud-init Configuration

1. Start with the `#cloud-config` header
2. Update and install packages
3. Write configuration files
4. Run setup commands

**Example:**
```yaml
#cloud-config
package_update: true
packages:
  - nginx
  - python3-venv

write_files:
  - path: /etc/systemd/system/myapp.service
    content: |
      [Unit]
      Description=My Application
      After=network.target

      [Service]
      Type=simple
      ExecStart=/usr/bin/myapp

      [Install]
      WantedBy=multi-user.target

runcmd:
  - systemctl daemon-reload
  - systemctl enable myapp
```

### Creating a systemd Service

1. Create service file in `/etc/systemd/system/`
2. Define Unit, Service, and Install sections
3. Use absolute paths in ExecStart
4. Never use inline comments
5. Reload systemd and enable service

**Example:**
```ini
[Unit]
Description=Flask App
After=network.target

[Service]
Type=simple
User=flask-app
WorkingDirectory=/opt/flask-app
ExecStart=/opt/flask-app/venv/bin/gunicorn wsgi:app

[Install]
WantedBy=multi-user.target
```

## Critical Rules to Remember

**Cloud-init:**
- Never use `users:` directive on Azure VMs (deletes azureuser)
- Always wait for cloud-init completion (2-3 minutes)
- Quote permissions: `'0640'`, not `0640`

**systemd:**
- No inline comments in unit files (comments must be on separate lines)
- Use absolute paths in ExecStart
- Always run `systemctl daemon-reload` after editing files

**Permissions:**
- Set explicit ownership after SCP: `chown user:group`
- Virtual environments: 775 (rwxrwxr-x)
- Environment files: 640 (rw-r-----) with root:servicegroup

**Python:**
- Always use full paths to venv executables
- Never rely on PATH or assume venv activation

## Debugging Checklist

**Cloud-init not working:**
```bash
cloud-init status
sudo cat /var/log/cloud-init-output.log | grep -i error
```

**Service won't start:**
```bash
sudo systemctl status service-name
sudo journalctl -u service-name -n 50
```

**Permission errors:**
```bash
ls -la /opt/flask-app/
sudo -u service-user cat /opt/flask-app/file.py
```

## Reference Implementation

See complete working examples in:
- `/Users/lasse/Developer/IPL_Development/IPL25-Hugo-Site/reference/stage-iaas-flask/infrastructure/cloud-init/`
  - `bastion.yaml` - SSH bastion with fail2ban
  - `proxy.yaml` - Nginx reverse proxy with SSL
  - `app.yaml` - Flask app server with systemd service

## Related Skills

- **revealjs-skill** - Create presentations about infrastructure
- **create-exercise** - Turn these patterns into student exercises
- **student-technical-writer** - Document Ubuntu configuration for students

## Maintenance

This skill is extracted from:
- stage-iaas-flask cloud-init files (primary source)
- stage-iaas-flask IMPLEMENTATION-PLAN.md (lessons learned)

**Update trigger:** When stage-iaas-flask cloud-init configurations are updated or new pitfalls discovered.

## Skill Statistics

- **Total documentation:** 55KB across 4 files
- **Working examples:** 12 complete configurations
- **Common pitfalls documented:** 17 critical issues
- **Code examples:** 100+ snippets
- **Debugging procedures:** 15+ workflows

## License and Attribution

Created for IPL25 DevOps Project Management course.

Source material: stage-iaas-flask reference implementation
Skill author: Claude Code (via extraction and documentation)
