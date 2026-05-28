# Common Ubuntu Configuration Pitfalls

## Overview

This document catalogs common mistakes to **avoid** when configuring Ubuntu servers. Read the prevention checklist before starting work to avoid these issues entirely.

## Prevention Checklist

Scan this list before writing cloud-init or systemd configurations:

### Cloud-init
- [ ] **DO NOT use `users:` directive** — Use `useradd` in `runcmd` instead
- [ ] **Quote permissions** — Write `'0640'` not `0640`
- [ ] **Wait for completion** — Run `cloud-init status --wait` before deploying

### systemd
- [ ] **NO inline comments** — Put comments on their own line, never after directives
- [ ] **Use absolute paths** — `/opt/app/venv/bin/python` not `python`
- [ ] **Run daemon-reload** — After any service file changes

### Permissions
- [ ] **Fix ownership after SCP** — Files retain local permissions when copied
- [ ] **App directories: 775** — Shared access for deploy user and service
- [ ] **Config files with secrets: 640** — Owned by `root:servicegroup`

### Python
- [ ] **Always use venv paths** — `/opt/app/venv/bin/pip` not `pip`

### Security
- [ ] **Never commit secrets** — Use `.gitignore` and example files

---

## Detailed Issue Reference

The sections below provide detailed explanations, symptoms, and solutions for each issue. Use these when diagnosing problems or understanding why a rule exists.

## Critical Cloud-init Issues

> **See also:** `cloud-init-patterns.md` for correct patterns and `examples/` for ready-to-use templates.

### Issue 1: Cloud-init `users:` Directive Replaces Default Users

**Severity:** Critical - Breaks SSH access

**Problem:** Using `users:` in cloud-init YAML completely replaces the default user list instead of adding to it. Cloud providers create a default SSH user for access:
- **AWS:** `ec2-user` (Amazon Linux) or `ubuntu` (Ubuntu AMI)
- **Azure:** `azureuser`
- **GCP:** Your Google account username

The `users:` directive deletes this default user, breaking SSH access.

**Symptom:**
```
Permission denied (publickey)
```

**Example of WRONG configuration:**
```yaml
#cloud-config
# DO NOT DO THIS ON CLOUD VMs!
users:
  - name: flask-app
    system: true
    shell: /usr/sbin/nologin
```

**Result:** Default SSH user is deleted, SSH access fails, VM becomes inaccessible.

**Solution:** Create service users in `runcmd` instead:
```yaml
runcmd:
  - useradd --system --shell /usr/sbin/nologin --no-create-home flask-app
```

**Key takeaway:** Never use `users:` directive on cloud VMs. Always use `useradd` in `runcmd`.

### Issue 2: Cloud-init Timing - Not Waiting for Completion

**Severity:** High - Causes deployment failures

**Problem:** Cloud-init takes 2-3 minutes to complete, but scripts often try to deploy immediately after VM creation.

**Symptom:**
- Files don't exist that should have been created by cloud-init
- Services aren't registered
- Directories haven't been created
- Package installations incomplete

**Solution:** Always wait for cloud-init completion before attempting deployment.

```bash
#!/bin/bash
# Wait for cloud-init to complete on all VMs

VMS=("vm-bastion" "vm-proxy" "vm-app")

for vm in "${VMS[@]}"; do
    echo "Waiting for cloud-init on $vm..."

    while true; do
        # Check cloud-init status via SSH
        STATUS=$(ssh azureuser@$vm "cloud-init status" 2>/dev/null)

        if echo "$STATUS" | grep -q "status: done"; then
            echo "✓ Cloud-init completed on $vm"
            break
        fi

        echo "  Still running..."
        sleep 10
    done
done
```

**Key takeaway:** Always verify cloud-init completion before deploying applications or running configuration scripts.

## systemd Service Issues

> **See also:** `systemd-patterns.md` for correct service file patterns and complete examples.

### Issue 3: Systemd Unit Files Do Not Support Inline Comments

**Severity:** Critical - Service fails to start

**Problem:** systemd does not support inline comments (comments after configuration directives on the same line). It interprets everything after the directive as part of the value.

**Symptom:**
```
Failed to enable unit: "#" is not a valid unit name
Job for flask-app.service failed because the control process exited with error code
```

**Example of WRONG configuration:**
```ini
[Unit]
Description=Flask App
After=network.target    # Start after network is available

[Service]
Type=simple             # Gunicorn runs in foreground
User=flask-app          # Run as dedicated user
```

**What systemd sees:**
- `After=network.target # Start after network is available` - Tries to start after targets named "network.target", "#", "Start", "after", "network", etc.
- `Type=simple #...` - Tries to set Type to "simple #..."

**Solution:** Move all comments to their own lines:
```ini
[Unit]
Description=Flask App
# Start after network is available
After=network.target

[Service]
# Gunicorn runs in foreground
Type=simple
# Run as dedicated user
User=flask-app
```

**Key takeaway:** In systemd unit files, comments MUST be on their own lines starting with `#` or `;`. Never place comments after directives on the same line.

### Issue 4: Service Can't Read Application Files - Permission Errors

**Severity:** High - Service fails to start

**Problem:** After SCP deployment, application files are owned by `azureuser:azureuser` with restrictive permissions (600). The service user (e.g., `flask-app`) cannot read them.

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: '/opt/flask-app/wsgi.py'
```

**Root cause:**
1. Local files have restrictive permissions (`rw-------`)
2. SCP preserves these permissions
3. Service user is not the owner and cannot read

**Example of problem:**
```bash
# After SCP
$ ls -la /opt/flask-app/wsgi.py
-rw------- 1 azureuser azureuser 256 Jan 15 10:30 wsgi.py

# Service runs as flask-app user
$ sudo -u flask-app cat /opt/flask-app/wsgi.py
cat: /opt/flask-app/wsgi.py: Permission denied
```

**Solution:** Set explicit ownership and permissions after copying files:
```bash
# Copy files via SCP
scp -r application/* azureuser@vm-app:/opt/flask-app/

# Fix permissions so service group can read
ssh azureuser@vm-app "sudo chown azureuser:flask-app /opt/flask-app/*.py"
ssh azureuser@vm-app "sudo chmod 640 /opt/flask-app/*.py"
```

**Correct permissions:**
```bash
$ ls -la /opt/flask-app/wsgi.py
-rw-r----- 1 azureuser flask-app 256 Jan 15 10:30 wsgi.py
```

**Key takeaway:** When deploying files to be run by a different user/group:
1. Always set explicit ownership after copying
2. Use `chown user:group` to set proper ownership
3. Use `chmod 640` (rw-r-----) so owner can write, group can read

## File Permission Patterns

### Issue 5: Incorrect Permission Syntax in Cloud-init

**Severity:** Medium - Files created with wrong permissions

**Problem:** Using numeric permissions without quotes in cloud-init `write_files`.

**Example of WRONG syntax:**
```yaml
write_files:
  - path: /etc/myapp/config.yml
    permissions: 0640    # WRONG - interpreted as decimal 640, not octal
```

**Result:** File gets decimal 640 permissions (octal 1200) which is invalid.

**Correct syntax:**
```yaml
write_files:
  - path: /etc/myapp/config.yml
    permissions: '0640'   # Correct - quoted octal string
```

**Key takeaway:** Always quote permissions in cloud-init: `'0640'`, never unquoted `0640`.

### Issue 6: Virtual Environment Permissions

**Severity:** Medium - Deployment or service failures

**Problem:** Python virtual environment not accessible to both deployment user and service user.

**Symptom:**
- Can't install packages during deployment
- Service can't import modules from venv

**Solution:** Set shared ownership with appropriate permissions:
```bash
# Virtual environment owned by deployment user, accessible to service group
chown -R azureuser:flask-app /opt/flask-app/venv
chmod 775 /opt/flask-app/venv

# Ensure deployment user is in service group
usermod -aG flask-app azureuser
```

**Permission breakdown:**
- **775** = rwxrwxr-x
  - Owner (azureuser): read, write, execute
  - Group (flask-app): read, write, execute
  - Others: read, execute

**Key takeaway:** Virtual environments need group write access (775) to allow both deployment and service access.

## SSH and Networking Issues

> **See also:** `../deploy-flask/references/ssh-patterns.md` for complete SSH patterns.

### Issue 7: SSH ProxyJump Host Key Verification Failures

**Severity:** Medium - Automation scripts fail or hang

**Problem:** When using `ssh -J` (ProxyJump), SSH options like `-o StrictHostKeyChecking=no` don't propagate to the proxy connection.

**Symptom:**
```
Host key verification failed
```
Or script hangs waiting for interactive confirmation.

**Example of problematic command:**
```bash
# Options don't apply to bastion connection
ssh -o StrictHostKeyChecking=no -J azureuser@bastion azureuser@vm-app "command"
```

**Solution:** Use explicit `ProxyCommand` instead of `-J`:
```bash
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"
PROXY_CMD="ssh $SSH_OPTS -W %h:%p azureuser@$BASTION_IP"

ssh $SSH_OPTS -o "ProxyCommand=$PROXY_CMD" azureuser@vm-app "command"
```

**Benefits:**
- SSH options apply to both connections
- No interactive prompts
- Clean log output

**Key takeaway:** For programmatic SSH through bastion, use `ProxyCommand` instead of `-J` to ensure options propagate correctly.

## Database Configuration Issues

### Issue 8: Database Not Created Automatically in Azure PostgreSQL

**Severity:** High - Application fails to connect

**Problem:** Provisioning an Azure PostgreSQL Flexible Server creates the server but doesn't create any databases within it.

**Symptom:**
```
FATAL: database "flask" does not exist
```

**Solution:** Explicitly create database resource in Bicep:
```bicep
resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: 'postgres-server'
  // ... server configuration
}

resource flaskDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  parent: postgresServer
  name: 'flask'
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}
```

**Key takeaway:** Azure PostgreSQL servers don't include default databases. Always create database resources explicitly.

## Python and Virtual Environment Issues

### Issue 9: Using System Python Instead of Virtual Environment

**Severity:** Medium - Dependency conflicts or missing packages

**Problem:** Running pip or python commands without using the virtual environment's executables.

**Example of WRONG approach:**
```bash
# Installs to system Python, not venv
pip install flask

# Uses system Python, can't find venv packages
python wsgi.py
```

**Correct approach:**
```bash
# Use venv's pip explicitly
/opt/flask-app/venv/bin/pip install flask

# Use venv's Python explicitly
/opt/flask-app/venv/bin/python wsgi.py

# Or use venv's gunicorn (which knows to use venv's Python)
/opt/flask-app/venv/bin/gunicorn wsgi:app
```

**systemd service configuration:**
```ini
[Service]
# Always use full path to venv executable
ExecStart=/opt/flask-app/venv/bin/gunicorn --bind 0.0.0.0:5001 wsgi:app
```

**Key takeaway:** Always use absolute paths to virtual environment executables. Never rely on PATH or assume activation.

### Issue 10: Virtual Environment Created by Root

**Severity:** Medium - Permission issues during deployment

**Problem:** If virtual environment is created by root (e.g., in cloud-init), deployment user can't install packages.

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: '/opt/flask-app/venv/lib/python3.11/site-packages/...'
```

**Solution:** Set proper ownership after creating venv:
```yaml
runcmd:
  # Create venv as root
  - python3 -m venv /opt/flask-app/venv

  # Fix ownership for deployment user
  - chown -R azureuser:flask-app /opt/flask-app/venv
  - chmod 775 /opt/flask-app/venv
```

**Key takeaway:** Virtual environments created during provisioning need ownership adjusted for deployment user.

## Environment Configuration Issues

### Issue 11: Environment File Syntax Errors

**Severity:** Medium - Environment variables not loaded

**Problem:** Incorrect syntax in .env files prevents systemd from loading variables.

**Example of WRONG syntax:**
```bash
# WRONG - spaces around equals
DATABASE_URL = postgresql://localhost/db

# WRONG - quotes interpreted literally
DATABASE_URL="postgresql://localhost/db"

# WRONG - shell variable expansion won't work
DATABASE_URL=$DB_HOST/db
```

**Correct syntax:**
```bash
# Correct - no spaces, no quotes, no expansion
DATABASE_URL=postgresql://localhost/db
SECRET_KEY=abc123xyz
DEBUG=false
```

**Key takeaway:** systemd EnvironmentFile format:
- No spaces around `=`
- No quotes (they become part of the value)
- No shell variable expansion
- One variable per line

### Issue 12: Environment File Not Readable by Service User

**Severity:** High - Service fails to start

**Problem:** Environment file has restrictive permissions that prevent service user from reading it.

**Symptom:**
```
Failed to load environment files: Permission denied
```

**Solution:** Set proper ownership and permissions:
```bash
# Environment file owned by root, readable by service group
chown root:flask-app /etc/flask-app/environment
chmod 640 /etc/flask-app/environment
```

**Permission breakdown:**
- **640** = rw-r-----
  - Owner (root): read, write
  - Group (flask-app): read
  - Others: no access

**Key takeaway:** Environment files with secrets should be 640 with root:servicegroup ownership.

## Deployment Script Issues

### Issue 13: Hardcoded File Lists in Deployment

**Severity:** Low - Maintenance burden

**Problem:** Deployment scripts list individual files to copy, requiring edits when adding new files.

**Example of brittle approach:**
```bash
scp app.py azureuser@vm-app:/opt/flask-app/
scp models.py azureuser@vm-app:/opt/flask-app/
scp wsgi.py azureuser@vm-app:/opt/flask-app/
# Must update script for every new file
```

**Better approach:**
```bash
# Copy entire directory recursively
scp -r application/* azureuser@vm-app:/opt/flask-app/
```

**Key takeaway:** Use recursive copy patterns instead of hardcoding file lists.

### Issue 14: Not Validating Prerequisites Before Deployment

**Severity:** Medium - Confusing error messages

**Problem:** Deployment scripts fail with cryptic errors when prerequisites aren't met.

**Example issues:**
- Azure CLI not logged in
- Resource group doesn't exist
- VM isn't running
- Cloud-init not complete

**Solution:** Validate prerequisites at start of script:
```bash
#!/bin/bash
set -e

# Check Azure CLI authentication
if ! az account show &>/dev/null; then
    echo "Error: Not logged in to Azure CLI"
    exit 1
fi

# Check resource group exists
if ! az group show -n "$RESOURCE_GROUP" &>/dev/null; then
    echo "Error: Resource group $RESOURCE_GROUP doesn't exist"
    exit 1
fi

# Check VM is running
STATE=$(az vm show -g "$RESOURCE_GROUP" -n "$VM_NAME" --query "powerState" -o tsv)
if [[ "$STATE" != "VM running" ]]; then
    echo "Error: VM is not running (current state: $STATE)"
    exit 1
fi

# Now proceed with deployment...
```

**Key takeaway:** Fail fast with clear error messages. Validate all prerequisites before attempting deployment.

## Security Issues

### Issue 15: Secrets in Git Repository

**Severity:** Critical - Security vulnerability

**Problem:** Database passwords, API keys, or other secrets committed to git.

**Common mistakes:**
- Hardcoded passwords in scripts
- Environment files with real credentials
- parameters.json with secrets

**Solution:** Use git ignore and example files:
```bash
# .gitignore
parameters.json
*.env
secrets/
```

**Provide templates instead:**
```bash
# parameters.example.json (committed)
{
  "adminPassword": "REPLACE_WITH_STRONG_PASSWORD",
  "databasePassword": "REPLACE_WITH_STRONG_PASSWORD"
}

# Generate real file locally (gitignored)
cp parameters.example.json parameters.json
# Edit parameters.json with real secrets
```

**Key takeaway:** Never commit secrets. Use example files and .gitignore.

## Bicep and Infrastructure Issues

### Issue 16: Bicep Linter Warnings for Literal Values

**Severity:** Low - Best practice violation

**Problem:** Bicep linter warns about hardcoded admin usernames.

**Warning:**
```
Warning adminusername-should-not-be-literal: Property 'adminUserName' should not use a literal value
```

**Example of warned code:**
```bicep
resource vm 'Microsoft.Compute/virtualMachines@2023-03-01' = {
  properties: {
    osProfile: {
      adminUsername: 'azureuser'  // Hardcoded literal
    }
  }
}
```

**Solution:** Use parameter with default:
```bicep
param adminUsername string = 'azureuser'

resource vm 'Microsoft.Compute/virtualMachines@2023-03-01' = {
  properties: {
    osProfile: {
      adminUsername: adminUsername  // Parameter reference
    }
  }
}
```

**Key takeaway:** Parameterize values that might change, even if you provide sensible defaults.

## Testing and Debugging

### Issue 17: Not Checking Logs When Services Fail

**Severity:** Medium - Wastes debugging time

**Problem:** Assuming why a service failed instead of checking logs.

**Proper debugging workflow:**
```bash
# 1. Check service status
sudo systemctl status flask-app.service

# 2. View recent logs
sudo journalctl -u flask-app.service -n 50

# 3. Follow logs in real-time while restarting
sudo journalctl -u flask-app.service -f &
sudo systemctl restart flask-app.service

# 4. Check for specific errors
sudo journalctl -u flask-app.service | grep -i error

# 5. View cloud-init output for provisioning issues
sudo cat /var/log/cloud-init-output.log
```

**Key takeaway:** Always check logs first. Don't guess at problems.

## Summary of Critical Rules

**Cloud-init:**
1. Never use `users:` directive on Azure VMs
2. Always wait for cloud-init completion before deployment
3. Quote permissions in write_files: `'0640'`

**systemd:**
4. Never use inline comments in unit files
5. Always use absolute paths in ExecStart
6. Always run `systemctl daemon-reload` after editing service files

**Permissions:**
7. Always set explicit ownership after SCP deployment
8. Virtual environments need 775 permissions
9. Environment files need 640 permissions with root:servicegroup ownership

**SSH:**
10. Use ProxyCommand instead of -J for scripted SSH through bastion

**Python:**
11. Always use full paths to venv executables
12. Never rely on PATH or assume venv activation

**Security:**
13. Never commit secrets to git
14. Use .gitignore and example files for sensitive configuration

**Debugging:**
15. Always check logs first (journalctl, cloud-init-output.log)
16. Validate prerequisites before deployment

## Quick Reference: Common Commands

**Check cloud-init status:**
```bash
cloud-init status
sudo cat /var/log/cloud-init-output.log
```

**Check service status:**
```bash
sudo systemctl status service-name
sudo journalctl -u service-name -f
```

**Fix permissions after deployment:**
```bash
sudo chown azureuser:flask-app /opt/flask-app/*.py
sudo chmod 640 /opt/flask-app/*.py
```

**Test SSH through bastion:**
```bash
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
PROXY_CMD="ssh $SSH_OPTS -W %h:%p azureuser@bastion-ip"
ssh $SSH_OPTS -o "ProxyCommand=$PROXY_CMD" azureuser@vm-app "hostname"
```

**Reload systemd after changes:**
```bash
sudo systemctl daemon-reload
sudo systemctl restart service-name
```
