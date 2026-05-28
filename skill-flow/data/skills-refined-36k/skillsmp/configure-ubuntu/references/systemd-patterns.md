# systemd Service Configuration Patterns

## Overview

systemd is the system and service manager for Ubuntu 24.04 LTS. It manages system services, handles dependencies, and provides automatic restart capabilities.

## Service Unit File Structure

### Basic Service File

systemd service files use INI-style configuration with sections denoted by `[Section]`.

```ini
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/my-command

[Install]
WantedBy=multi-user.target
```

**Location:** `/etc/systemd/system/service-name.service`

## Critical Rules for systemd Unit Files

### NO Inline Comments

**CRITICAL:** systemd does NOT support inline comments. Comments must be on their own lines.

```ini
# WRONG - causes "Failed to enable unit" errors
After=network.target    # This breaks everything

# CORRECT - comments on their own lines
# Start after network is available
After=network.target
```

> **See also:** `common-pitfalls.md` Issue #3 for detailed explanation and symptoms.

## Service File Sections

### [Unit] Section

Defines metadata and dependencies.

```ini
[Unit]
# Human-readable description (appears in systemctl status)
Description=Flask Contact Form Application

# Optional longer description
Documentation=https://github.com/myorg/myapp

# Start service after these targets
After=network.target

# Require these units (service fails if they fail)
Requires=postgresql.service

# Prefer to start with these units (but don't fail if they're not available)
Wants=network-online.target
```

**Common After= targets:**
- `network.target` - Basic network is configured
- `network-online.target` - Network is fully online
- `multi-user.target` - Multi-user system is ready

### [Service] Section

Defines how the service runs.

```ini
[Service]
# Service type
Type=simple

# User and group to run as
User=flask-app
Group=flask-app

# Working directory
WorkingDirectory=/opt/flask-app

# Environment variables
Environment="PORT=5001"
Environment="DEBUG=false"

# Load environment from file
EnvironmentFile=/etc/flask-app/environment

# Command to start service
ExecStart=/opt/flask-app/venv/bin/gunicorn --bind 0.0.0.0:5001 wsgi:app

# Restart behavior
Restart=always
RestartSec=5

# Resource limits
MemoryMax=512M
CPUQuota=50%
```

### [Install] Section

Defines when the service should start.

```ini
[Install]
# Start in normal multi-user mode
WantedBy=multi-user.target
```

**Common WantedBy= targets:**
- `multi-user.target` - Normal boot (no GUI)
- `graphical.target` - Graphical desktop environment
- `default.target` - System default target

## Service Types

### Type=simple

**Most common.** Process specified in ExecStart is the main process.

```ini
[Service]
Type=simple
ExecStart=/usr/bin/my-daemon
```

**Use when:** Your application runs in the foreground (doesn't fork/daemonize).

**Examples:** Gunicorn, Flask development server, most Python applications.

### Type=forking

Process specified in ExecStart forks and the parent exits.

```ini
[Service]
Type=forking
PIDFile=/var/run/myapp.pid
ExecStart=/usr/bin/my-daemon --daemonize
```

**Use when:** Application daemonizes itself (old-style Unix daemons).

### Type=oneshot

For tasks that execute and exit (not long-running services).

```ini
[Service]
Type=oneshot
ExecStart=/usr/local/bin/setup-task.sh
RemainAfterExit=yes
```

**Use when:** Running initialization scripts or one-time tasks.

## Environment Configuration

### Inline Environment Variables

```ini
[Service]
Environment="DATABASE_URL=postgresql://localhost/mydb"
Environment="SECRET_KEY=abc123"
Environment="PORT=5001"
```

**Use when:** Few variables, no sensitive data.

### Environment File

```ini
[Service]
EnvironmentFile=/etc/flask-app/environment
```

**environment file contents:**
```bash
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key
DEBUG=false
```

**Use when:** Multiple variables or sensitive credentials.

**Best practice:** Set file permissions to 640 (rw-r-----) and owner to root:appgroup.

```bash
sudo chown root:flask-app /etc/flask-app/environment
sudo chmod 640 /etc/flask-app/environment
```

## Restart Behavior

### Restart Policies

```ini
[Service]
# Never restart (default)
Restart=no

# Restart unless stopped manually
Restart=on-failure

# Always restart (except if stopped manually)
Restart=always

# Restart only on successful exit
Restart=on-success
```

### Restart Timing

```ini
[Service]
Restart=always

# Wait 5 seconds before restarting
RestartSec=5

# Give up after 3 restart attempts in 30 seconds
StartLimitBurst=3
StartLimitIntervalSec=30
```

**Recommendation:** Use `Restart=always` with `RestartSec=5` for production services.

## User and Group Configuration

### Running as Non-Root User

```ini
[Service]
User=flask-app
Group=flask-app
```

**Prerequisites:**
1. User must exist (create in cloud-init runcmd)
2. User must have read access to application files
3. User must have execute permission on application directory

**Creating service user:**
```bash
sudo useradd --system --shell /usr/sbin/nologin --no-create-home flask-app
```

**Flags explained:**
- `--system` - System user (UID < 1000, no password aging)
- `--shell /usr/sbin/nologin` - Prevent interactive login
- `--no-create-home` - No home directory needed

### File Permissions for Service User

```bash
# Application owned by deployment user, readable by service group
sudo chown -R azureuser:flask-app /opt/flask-app
sudo chmod 775 /opt/flask-app

# Application files readable by group
sudo chmod 640 /opt/flask-app/*.py

# Virtual environment accessible by group
sudo chmod 775 /opt/flask-app/venv
```

## Complete Working Examples

### Example 1: Flask Application with Gunicorn

```ini
[Unit]
Description=Flask Application
After=network.target

[Service]
# Run in foreground
Type=simple

# Run as dedicated service user
User=flask-app
Group=flask-app

# Application directory
WorkingDirectory=/opt/flask-app

# Load database credentials from file
EnvironmentFile=/etc/flask-app/environment

# Start Gunicorn WSGI server
# Use venv Python to ensure correct dependencies
ExecStart=/opt/flask-app/venv/bin/gunicorn --bind 0.0.0.0:5001 wsgi:app

# Restart on any exit (crash recovery)
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Cloud-init integration:** See `examples/flask.yaml` for complete cloud-init configuration.

### Example 2: Background Worker Service

```ini
[Unit]
Description=Background Task Worker
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=worker
Group=worker
WorkingDirectory=/opt/worker
EnvironmentFile=/etc/worker/environment

# Run Celery worker
ExecStart=/opt/worker/venv/bin/celery -A tasks worker --loglevel=info

# Restart on failure
Restart=on-failure
RestartSec=10

# Resource limits
MemoryMax=1G
CPUQuota=80%

[Install]
WantedBy=multi-user.target
```

### Example 3: Initialization Service (One-shot)

```ini
[Unit]
Description=Initialize Application Database
After=postgresql.service
Requires=postgresql.service

[Service]
Type=oneshot
User=flask-app
Group=flask-app
WorkingDirectory=/opt/flask-app
EnvironmentFile=/etc/flask-app/environment

# Run database migrations
ExecStart=/opt/flask-app/venv/bin/flask db upgrade

# Service is considered active after script completes
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

## Managing Services

### Essential Commands

```bash
# Reload systemd after creating/editing service files
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable flask-app.service

# Disable service from starting on boot
sudo systemctl disable flask-app.service

# Start service immediately
sudo systemctl start flask-app.service

# Stop service
sudo systemctl stop flask-app.service

# Restart service
sudo systemctl restart flask-app.service

# Reload service configuration (if supported)
sudo systemctl reload flask-app.service

# Check service status
sudo systemctl status flask-app.service

# Check if service is enabled
sudo systemctl is-enabled flask-app.service

# Check if service is running
sudo systemctl is-active flask-app.service
```

### Viewing Logs

```bash
# View all logs for service
sudo journalctl -u flask-app.service

# View last 50 lines
sudo journalctl -u flask-app.service -n 50

# Follow logs in real-time
sudo journalctl -u flask-app.service -f

# View logs since boot
sudo journalctl -u flask-app.service -b

# View logs for date range
sudo journalctl -u flask-app.service --since "2024-01-01" --until "2024-01-02"

# View logs with timestamps
sudo journalctl -u flask-app.service -o short-iso
```

### Debugging Failed Services

```bash
# 1. Check service status and recent logs
sudo systemctl status flask-app.service
sudo journalctl -u flask-app.service -n 50

# 2. Verify service file syntax
sudo systemd-analyze verify /etc/systemd/system/flask-app.service

# 3. View service dependencies
sudo systemctl list-dependencies flask-app.service
```

> **See also:** `common-pitfalls.md` Issue #17 for complete debugging workflow.

## Troubleshooting

For common issues and their solutions, see `common-pitfalls.md`:
- Issue #1: Service permission errors
- Issue #3: Inline comments breaking unit files
- Issue #4: Environment file problems

## Best Practices

1. **Use Type=simple for most applications** - Simplest and most reliable
2. **Always set User= and Group=** - Never run services as root unless absolutely necessary
3. **Use EnvironmentFile for secrets** - Don't hardcode credentials in service files
4. **Set Restart=always for production** - Automatic recovery from crashes
5. **Add After=network.target** - Ensure network is available before starting
6. **Use absolute paths** - ExecStart should use full paths to executables
7. **Comments on separate lines** - Never use inline comments in unit files
8. **Reload after changes** - Always run `systemctl daemon-reload` after editing service files
9. **Test with systemd-analyze verify** - Validate syntax before deploying
10. **Monitor with journalctl** - Use journalctl for log analysis, not custom log files

## Resource Limits

### Memory Limits

```ini
[Service]
# Hard limit (OOM killer terminates if exceeded)
MemoryMax=512M

# Soft limit (cgroup memory accounting)
MemoryHigh=400M
```

### CPU Limits

```ini
[Service]
# Limit to 50% of one CPU core
CPUQuota=50%

# Assign to specific CPU cores
CPUAffinity=0 1
```

### File Descriptor Limits

```ini
[Service]
# Maximum number of open files
LimitNOFILE=4096
```

### Process Limits

```ini
[Service]
# Maximum number of processes
LimitNPROC=512
```

## Advanced Patterns

### Service with Pre-Start Check

```ini
[Service]
# Check database connectivity before starting application
ExecStartPre=/usr/local/bin/check-database.sh
ExecStart=/opt/flask-app/venv/bin/gunicorn --bind 0.0.0.0:5001 wsgi:app
```

### Service with Cleanup on Stop

```ini
[Service]
ExecStart=/opt/flask-app/venv/bin/gunicorn --bind 0.0.0.0:5001 wsgi:app

# Run cleanup script when stopping
ExecStopPost=/usr/local/bin/cleanup.sh
```

### Service with Graceful Shutdown

```ini
[Service]
ExecStart=/opt/flask-app/venv/bin/gunicorn --bind 0.0.0.0:5001 wsgi:app

# Send SIGTERM, wait 30 seconds, then send SIGKILL
KillMode=mixed
TimeoutStopSec=30
```

## Systemd Timers (Scheduled Tasks)

Systemd timers are the modern replacement for cron jobs. They offer better logging, dependency management, and integration with systemd services.

### Timer Structure

A timer requires two files:
1. **Service file** (`.service`) - Defines what to run
2. **Timer file** (`.timer`) - Defines when to run it

### Example: Daily Backup Timer

**Service file:** `/etc/systemd/system/backup.service`
```ini
[Unit]
Description=Daily Backup Task

[Service]
Type=oneshot
User=backup
Group=backup
ExecStart=/usr/local/bin/backup.sh

[Install]
WantedBy=multi-user.target
```

**Timer file:** `/etc/systemd/system/backup.timer`
```ini
[Unit]
Description=Run backup daily at 2:00 AM

[Timer]
# Run daily at 2:00 AM
OnCalendar=*-*-* 02:00:00

# Run immediately if last scheduled run was missed
Persistent=true

# Add random delay up to 5 minutes to avoid thundering herd
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

### Timer Schedule Formats

```ini
[Timer]
# Specific time daily
OnCalendar=*-*-* 02:00:00

# Every hour
OnCalendar=hourly

# Every day at midnight
OnCalendar=daily

# Every week on Sunday at 3:00 AM
OnCalendar=Sun *-*-* 03:00:00

# Every 15 minutes
OnCalendar=*:0/15

# First day of month at 6:00 AM
OnCalendar=*-*-01 06:00:00
```

### Alternative: Interval-Based Timers

```ini
[Timer]
# Run 10 minutes after boot
OnBootSec=10min

# Run every 6 hours after activation
OnUnitActiveSec=6h

# Run 5 minutes after last completion
OnUnitInactiveSec=5min
```

### Managing Timers

```bash
# Enable and start timer
sudo systemctl enable backup.timer
sudo systemctl start backup.timer

# List all timers
sudo systemctl list-timers

# Check timer status
sudo systemctl status backup.timer

# View timer logs
sudo journalctl -u backup.service

# Run service manually (test)
sudo systemctl start backup.service
```

### Cloud-init Example: Scheduled Cleanup Task

```yaml
write_files:
  # Cleanup service
  - path: /etc/systemd/system/cleanup.service
    content: |
      [Unit]
      Description=Clean up temporary files

      [Service]
      Type=oneshot
      ExecStart=/usr/bin/find /tmp -type f -mtime +7 -delete

  # Timer to run cleanup weekly
  - path: /etc/systemd/system/cleanup.timer
    content: |
      [Unit]
      Description=Weekly cleanup timer

      [Timer]
      OnCalendar=weekly
      Persistent=true

      [Install]
      WantedBy=timers.target

runcmd:
  - systemctl daemon-reload
  - systemctl enable cleanup.timer
  - systemctl start cleanup.timer
```

## Integration with Cloud-init

For complete cloud-init configurations that include systemd services, see the `examples/` directory:

- `examples/flask.yaml` - Python/Flask with Gunicorn
- `examples/nodejs.yaml` - Node.js application
- `examples/java.yaml` - Java/Spring Boot
- `examples/dotnet.yaml` - .NET application

**Note:** Cloud-init creates the service file and registers it with `systemctl daemon-reload`, but typically does NOT start the service because application code hasn't been deployed yet. A separate deployment script starts the service after copying application files.

## References

- [systemd.service man page](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [systemd.timer man page](https://www.freedesktop.org/software/systemd/man/systemd.timer.html)
- [systemd.unit man page](https://www.freedesktop.org/software/systemd/man/systemd.unit.html)
