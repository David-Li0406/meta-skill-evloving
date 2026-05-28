# Cloud-init Configuration Patterns

## Overview

Cloud-init is the industry-standard multi-distribution method for cross-platform cloud instance initialization. All major cloud providers (AWS, Azure, GCP, DigitalOcean, etc.) support cloud-init to automate VM configuration on first boot.

## Complete Examples

Ready-to-use cloud-init configurations are in the `examples/` directory:

| File | Purpose |
|------|---------|
| `bastion.yaml` | SSH bastion host with UFW + fail2ban |
| `proxy-http.yaml` | Nginx reverse proxy (HTTP) - **default** |
| `proxy-https.yaml` | Nginx reverse proxy with self-signed certificate |
| `proxy-https-letsencrypt.yaml` | Nginx reverse proxy with Let's Encrypt certificate |
| `static-files.yaml` | Nginx static file server |
| `flask.yaml` | Python/Flask application server |
| `nodejs.yaml` | Node.js application server |
| `java.yaml` | Java/Spring Boot application server |
| `dotnet.yaml` | .NET application server |

> **HTTPS Options:**
> - Use `proxy-http.yaml` by default (no SSL)
> - Use `proxy-https.yaml` for self-signed certificates (development/internal)
> - Use `proxy-https-letsencrypt.yaml` for trusted certificates (requires domain name)

## Basic Structure

### Minimal Cloud-init File

```yaml
#cloud-config
# This header is MANDATORY - must be first line with no leading whitespace

package_update: true
packages:
  - nginx
```

**Important:** The `#cloud-config` header is not a comment - it's a required file type identifier. Omitting it will cause cloud-init to ignore the file.

## Module Execution Order

Cloud-init modules execute in a specific order during boot:

1. **Network configuration** (automatic)
2. **Package management** (`package_update`, `package_upgrade`, `packages`)
3. **File creation** (`write_files`)
4. **User commands** (`runcmd`)

This order is critical for dependencies:
- Install packages before writing config files that reference them
- Write config files before running commands that use them
- Create users before setting file ownership

## Package Management

### Update and Upgrade

```yaml
# Update package lists (apt update)
package_update: true

# Upgrade all installed packages (apt upgrade)
package_upgrade: true
```

**Recommendation:** Always use `package_update: true` to ensure package lists are current before installing new packages.

### Installing Packages

```yaml
packages:
  - nginx              # Web server
  - python3            # Python interpreter
  - python3-pip        # Python package manager
  - python3-venv       # Virtual environment support
  - postgresql-client  # PostgreSQL command-line tools
  - fail2ban           # Intrusion prevention
  - ufw                # Firewall management
  - git                # Version control
```

**Package names:** Use exact Ubuntu package names as they appear in `apt search`.

## Writing Files

### Basic File Creation

```yaml
write_files:
  - path: /etc/myapp/config.yml
    content: |
      setting1: value1
      setting2: value2
```

**Note:** The pipe (`|`) after `content:` enables multi-line string literals. All subsequent indented lines become the file content.

### File Permissions and Ownership

```yaml
write_files:
  - path: /opt/app/config.ini
    owner: appuser:appgroup
    permissions: '0640'
    content: |
      [database]
      host=localhost
```

**Important:**
- Permissions MUST be quoted strings (`'0640'`), not integers
- Ownership format is `user:group`
- Default permissions are `0644` (rw-r--r--)
- Default owner is `root:root`

### Multiple Files

```yaml
write_files:
  # Systemd service file
  - path: /etc/systemd/system/myapp.service
    permissions: '0644'
    content: |
      [Unit]
      Description=My Application
      After=network.target

      [Service]
      Type=simple
      ExecStart=/usr/bin/myapp

      [Install]
      WantedBy=multi-user.target

  # Application configuration
  - path: /etc/myapp/settings.conf
    owner: root:myapp
    permissions: '0640'
    content: |
      PORT=5001
      DEBUG=false

  # Nginx site configuration
  - path: /etc/nginx/sites-available/myapp
    content: |
      server {
          listen 80;
          server_name _;
          location / {
              # Replace with backend IP/hostname:port
              proxy_pass http://localhost:5001;
          }
      }
```

## Running Commands

### Basic Commands

```yaml
runcmd:
  - echo "Hello from cloud-init"
  - mkdir -p /opt/myapp
  - systemctl restart nginx
```

**Note:** Each list item is a separate command. They execute sequentially.

### Multi-line Commands

```yaml
runcmd:
  # Long command split across lines using YAML list syntax
  - |
    openssl req -x509 -nodes -days 365 \
      -newkey rsa:2048 \
      -keyout /etc/ssl/private/nginx.key \
      -out /etc/ssl/certs/nginx.crt \
      -subj "/CN=localhost/O=Dev/C=US"
```

### Common Command Patterns

```yaml
runcmd:
  # Create directories
  - mkdir -p /opt/myapp
  - mkdir -p /etc/myapp

  # Create system user (non-interactive)
  - useradd --system --shell /usr/sbin/nologin --no-create-home myapp

  # Python virtual environment
  - python3 -m venv /opt/myapp/venv
  - /opt/myapp/venv/bin/pip install --upgrade pip

  # File permissions (deploy user owns, service group can read)
  # Replace 'adminuser' with your cloud provider's default SSH user
  - chown -R adminuser:myapp /opt/myapp
  - chmod 775 /opt/myapp
  - chmod 775 /opt/myapp/venv

  # Secure environment file
  - touch /etc/myapp/environment
  - chown root:myapp /etc/myapp/environment
  - chmod 640 /etc/myapp/environment

  # Systemd services (register but don't start - no app code yet)
  - systemctl daemon-reload

  # Nginx
  - ln -sf /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/myapp
  - rm -f /etc/nginx/sites-enabled/default
  - systemctl reload nginx
```

## Cloud-init Lifecycle

### When Cloud-init Runs

Cloud-init executes **only on first boot** by default. Subsequent reboots do NOT re-run cloud-init.

**To force cloud-init to run again:**
```bash
sudo cloud-init clean
sudo reboot
```

**Warning:** This will re-execute ALL cloud-init directives, potentially overwriting manual changes.

### Execution Timeline

| Time | Event |
|------|-------|
| 0:00 | VM starts booting |
| 0:10 | Cloud-init begins execution |
| 0:15 | Package updates start (if `package_update: true`) |
| 0:45 | Package upgrades start (if `package_upgrade: true`) |
| 1:30 | Packages installed |
| 1:35 | Files written |
| 1:40 | Commands executed |
| 2:00 | Cloud-init completes |
| 2:05 | SSH becomes available |

**Typical duration:** 2-3 minutes for basic configuration, 5+ minutes with package upgrades.

## Debugging Cloud-init

### Log Files

```bash
# Main execution log (all output from runcmd)
sudo cat /var/log/cloud-init-output.log

# Cloud-init internal logs
sudo cat /var/log/cloud-init.log

# Check for errors
sudo grep -i error /var/log/cloud-init-output.log
sudo grep -i fail /var/log/cloud-init-output.log
```

### Status Commands

```bash
# Check if cloud-init has finished
cloud-init status

# Detailed status with execution time
cloud-init status --long

# Wait for cloud-init to complete (blocks until done)
cloud-init status --wait
```

### Common Debug Workflow

> **See also:** `common-pitfalls.md` Issue #2 for timing-related deployment failures.

```bash
# 1. Check if cloud-init completed
cloud-init status

# 2. View execution log
sudo tail -100 /var/log/cloud-init-output.log

# 3. Search for errors
sudo grep -i error /var/log/cloud-init-output.log

# 4. Check service status (if configuring systemd service)
sudo systemctl status myapp.service

# 5. View service logs
sudo journalctl -u myapp.service -n 50
```

## Advanced Patterns

### Conditional Execution

```yaml
runcmd:
  # Only run if file doesn't exist
  - test -f /etc/myapp/initialized || echo "first run" > /etc/myapp/initialized

  # Only run if command succeeds
  - which nginx && systemctl restart nginx
```

### Error Handling

```yaml
runcmd:
  # Continue on error (|| true suppresses failure)
  - mkdir /opt/myapp || true

  # Stop on error (default behavior - next command won't run if this fails)
  - mkdir /opt/myapp
  - chown -R adminuser:myapp /opt/myapp
```

### Combining with Shell Scripts

```yaml
write_files:
  - path: /usr/local/bin/setup-app.sh
    permissions: '0755'
    content: |
      #!/bin/bash
      set -e  # Exit on error

      echo "Setting up application..."
      mkdir -p /opt/myapp
      python3 -m venv /opt/myapp/venv
      /opt/myapp/venv/bin/pip install flask
      echo "Setup complete"

runcmd:
  - /usr/local/bin/setup-app.sh
```

**Benefits:**
- Cleaner runcmd section
- Better error handling in shell script
- Reusable script for manual re-runs

## Integration with Infrastructure as Code

### Loading Cloud-init in Bicep (Azure)

```bicep
// Load cloud-init from external file
var cloudInitContent = loadTextContent('../cloud-init/app.yaml')

// Use in VM resource
resource vm 'Microsoft.Compute/virtualMachines@2023-03-01' = {
  name: 'vm-app'
  properties: {
    osProfile: {
      customData: base64(cloudInitContent)
    }
  }
}
```

**Benefits:**
- Separate files are easier to edit and test
- Syntax highlighting in YAML editors
- Can validate YAML independently
- Cleaner infrastructure code

### Cloud Provider Considerations

**Default SSH user:** Cloud providers create a default admin user for SSH access. Never use the `users:` directive in cloud-init, as it replaces this user and breaks SSH access. See `common-pitfalls.md` Issue #1 for details.

| Provider | Default SSH User |
|----------|------------------|
| AWS (Amazon Linux) | `ec2-user` |
| AWS (Ubuntu AMI) | `ubuntu` |
| Azure | `azureuser` |
| GCP | Your Google account username |
| DigitalOcean | `root` |

**Network configuration:** Cloud providers handle network setup automatically. Don't configure network interfaces in cloud-init.

**SSH keys:** Cloud providers inject SSH keys automatically via their APIs. Don't configure SSH keys in cloud-init.

### Cloud Provider Metadata Services

Cloud providers offer metadata services to retrieve instance information like public IP addresses. This is useful when generating SSL certificates that need the public IP as the Common Name (CN).

**Cloud-agnostic approach (recommended default):**
```bash
# Use external service - works on any cloud
PUBLIC_IP=$(curl -s --max-time 10 ifconfig.me 2>/dev/null)
```

**Provider-specific metadata services** (faster, no external dependency):

| Provider | Metadata Endpoint |
|----------|-------------------|
| Azure | `http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01&format=text` |
| AWS | `http://169.254.169.254/latest/meta-data/public-ipv4` |
| GCP | `http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip` |

**Azure example with fallback:**
```bash
# Try Azure IMDS first (requires -H "Metadata:true" header)
PUBLIC_IP=$(curl -s -H "Metadata:true" --max-time 5 \
  "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01&format=text" 2>/dev/null)

# Fall back to external service if IMDS returns empty
if [ -z "$PUBLIC_IP" ]; then
  PUBLIC_IP=$(curl -s --max-time 10 ifconfig.me 2>/dev/null)
fi

# Fall back to localhost as last resort
if [ -z "$PUBLIC_IP" ]; then
  PUBLIC_IP="localhost"
fi
```

**AWS example:**
```bash
# AWS metadata service (no special headers required)
PUBLIC_IP=$(curl -s --max-time 5 http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null)
```

**GCP example:**
```bash
# GCP metadata service (requires Metadata-Flavor header)
PUBLIC_IP=$(curl -s -H "Metadata-Flavor: Google" --max-time 5 \
  "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip" 2>/dev/null)
```

> **Note:** The `proxy-https.yaml` example uses `ifconfig.me` as the default (cloud-agnostic). For production deployments, consider using the provider-specific metadata service for faster, more reliable results.

## Best Practices

1. **Always use `package_update: true`** - Ensures latest package lists
2. **Test cloud-init files independently** - Use `cloud-init schema --config-file myfile.yaml` to validate syntax
3. **Use meaningful comments** - Explain WHY, not WHAT
4. **Prefer external files in IaC** - Use `loadTextContent()` or equivalent for maintainability
5. **Wait for cloud-init completion** - Check logs before assuming configuration is complete
6. **Use absolute paths** - Always use full paths in runcmd (e.g., `/usr/bin/python3`, not `python3`)
7. **Avoid inline comments in config files** - Especially systemd unit files (see common-pitfalls.md)
8. **Set explicit permissions** - Don't rely on defaults for security-sensitive files
