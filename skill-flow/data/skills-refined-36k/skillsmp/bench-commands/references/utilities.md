# Utilities

## Configuration Management

### Set Configuration Value
```bash
bench --site development.localhost set-config key value
```

Sets a configuration value in site_config.json.

**Examples:**
```bash
# Enable developer mode
bench --site development.localhost set-config developer_mode 1

# Set encryption key
bench --site development.localhost set-config encryption_key "your-key-here"

# Set custom config
bench --site development.localhost set-config max_file_size 10485760
```

### Get Configuration Value
```bash
bench --site development.localhost get-config key
```

Retrieves a configuration value.

**Example:**
```bash
bench --site development.localhost get-config developer_mode
```

### View All Configuration

**Using show-config command:**
```bash
# View as text
bench --site development.localhost show-config

# View as JSON
bench --site development.localhost show-config --format json
```

**Using cat:**
```bash
cat sites/development.localhost/site_config.json
```

Shows complete site configuration file.

**Common configurations:**
- `developer_mode`: Enable developer mode (1 = on, 0 = off)
- `encryption_key`: Site encryption key
- `db_name`: Database name
- `db_password`: Database password
- `redis_cache`, `redis_queue`, `redis_socketio`: Redis connection strings
- `mail_server`, `mail_port`, `mail_login`, `mail_password`: Email settings

## Scheduler Management

### Enable Scheduler
```bash
bench --site development.localhost enable-scheduler
```

Enables background scheduled jobs (hourly, daily, weekly, etc.).

**Scheduled jobs run for:**
- Email sending
- Report generation
- Automated workflows
- Maintenance tasks

### Disable Scheduler
```bash
bench --site development.localhost disable-scheduler
```

Disables scheduled jobs. Useful during development to prevent:
- Unwanted emails
- Background task interference
- Resource consumption

### Check Scheduler Status
```bash
bench --site development.localhost doctor
```

Shows site health including scheduler status.

## DocType Operations

### Reload DocType
```bash
bench --site development.localhost reload-doctype "DocType Name"
```

Reloads a DocType definition from its JSON file.

**Use when:**
- JSON changes not reflecting
- DocType appears corrupted
- After manual JSON edits

### Rebuild DocType
```bash
bench --site development.localhost rebuild-doctype "DocType Name"
```

Completely rebuilds a DocType including database schema.

**Warning:** More aggressive than reload. Use carefully.

## Password Management

### Reset Admin Password
```bash
bench --site development.localhost set-admin-password admin
```

Resets Administrator user password to "admin".

**Options:**
```bash
# Set specific password
bench --site development.localhost set-admin-password "new_secure_password"

# Log out all sessions when changing password
bench --site development.localhost set-admin-password admin --logout-all-sessions
```

**Use when:**
- Forgot admin password
- After restoring backup
- Initial setup
- Security incident requiring password reset

### Set User Password

**Using set-password command:**
```bash
# Interactive prompt for password
bench --site development.localhost set-password user@example.com

# Specify password directly
bench --site development.localhost set-password user@example.com "new_password"

# Log out all user sessions when changing password
bench --site development.localhost set-password user@example.com "new_password" --logout-all-sessions
```

**Using console (alternative method):**
```bash
bench --site development.localhost console
>>> from frappe.utils.password import update_password
>>> update_password("user@example.com", "new_password")
>>> frappe.db.commit()
```

**Security best practices:**
- Always use `--logout-all-sessions` when changing passwords after security incidents
- Use strong passwords (mix of letters, numbers, symbols)
- Never commit passwords to git repositories
- Use environment variables for production passwords

## Version Information

### Check Bench Version
```bash
bench --version
```

Shows bench utility version.

### Check Frappe Version
```bash
bench version
```

Shows version of all installed apps.

**Output example:**
```
erpnext 15.0.0
frappe 15.0.0
soldamundo 1.0.0
tweaks 1.0.0
```

### Check App Version
```bash
cd apps/soldamundo && git describe --tags
```

Shows git tag/version for specific app.

## Update Operations

### Update Specific App
```bash
bench update --apps soldamundo
```

Pulls latest code and runs migrations for the specified app.

**Steps performed:**
1. Git pull latest code
2. Install dependencies (requirements.txt, package.json)
3. Run migrations
4. Build assets

### Update All Apps
```bash
bench update
```

Updates all apps in bench.

**Warning:** Can break things. Test in development first.

### Pull Without Migrate
```bash
bench update --pull
```

Only pulls code without running migrations.

**Use when:**
- Want to review changes first
- Manually control migration timing
- Debugging issues

### Update Bench
```bash
bench update --bench
```

Updates the bench tool itself.

## Maintenance Operations

### Clear Website Cache
```bash
bench --site development.localhost clear-website-cache
```

Clears website/portal cache specifically.

### Clear Global Search
```bash
bench --site development.localhost build-search-index
```

Rebuilds the global search index.

**Use when:**
- Search not finding documents
- After bulk data import
- Search results stale

### Optimize Tables
```bash
bench --site development.localhost mariadb
```

Then in MariaDB:
```sql
OPTIMIZE TABLE `tabDocType`;
```

Optimizes database table performance.

## Permission Management

### Setup Requirements
```bash
bench setup requirements
```

Reinstalls Python dependencies from requirements.txt files.

**Use when:**
- Python packages not found
- After requirements.txt changes
- Fixing dependency issues

### Setup SocketIO
```bash
bench setup socketio
```

Reinstalls SocketIO dependencies.

**Use when:**
- Real-time updates not working
- SocketIO connection errors

## Node.js Dependencies

### Install Node Dependencies
```bash
cd apps/soldamundo && yarn install
cd apps/frappe && yarn install
```

Installs/updates JavaScript dependencies.

**Use when:**
- After package.json changes
- Build errors
- Missing JavaScript packages

### Clean Install
```bash
cd apps/soldamundo
rm -rf node_modules
yarn install
```

Complete clean reinstall of node_modules.

## RQ Job Queue Management

### Purge Jobs

```bash
# Purge all pending jobs for all queues
bench --site development.localhost purge-jobs

# Purge specific queue
bench --site development.localhost purge-jobs --queue default
bench --site development.localhost purge-jobs --queue short
bench --site development.localhost purge-jobs --queue long

# Purge specific scheduled event type
bench --site development.localhost purge-jobs --event daily
bench --site development.localhost purge-jobs --event hourly
bench --site development.localhost purge-jobs --event weekly
bench --site development.localhost purge-jobs --event monthly
bench --site development.localhost purge-jobs --event daily_long
bench --site development.localhost purge-jobs --event weekly_long

# Purge all scheduled events
bench --site development.localhost purge-jobs --event all

# Purge for specific site
bench --site production.example.com purge-jobs --event all
```

**What it does:**
- Removes pending periodic/scheduled tasks from queues
- Clears stuck or old jobs
- Helps reset job queue state
- Does NOT affect running jobs

**Use cases:**
- Queue backed up with old jobs
- Testing scheduler without old jobs running
- After configuration changes
- Clearing jobs before maintenance
- Development/testing cleanup

**Queue types:**
- `short` - Quick tasks (< 5 minutes)
- `default` - Standard background jobs (5-30 minutes)
- `long` - Long-running tasks (> 30 minutes)

**Event types:**
- `all` - All scheduled events
- `hourly` - Jobs scheduled every hour (e.g., email digest)
- `daily` - Jobs scheduled daily (e.g., daily reports)
- `weekly` - Jobs scheduled weekly (e.g., weekly reports)
- `monthly` - Jobs scheduled monthly (e.g., monthly cleanup)
- `daily_long` - Long-running daily jobs
- `weekly_long` - Long-running weekly jobs

**Warning:**
- Purging removes jobs that haven't run yet
- Consider consequences before purging in production
- Some jobs may be important (emails, reports, etc.)

### Check Queue Status

See [job-queue.md](job-queue.md) for detailed queue management.

## Bench Doctor

### Run Comprehensive Diagnostics
```bash
# Full diagnostics for specific site
bench --site development.localhost doctor

# Check specific site (alternative syntax)
bench doctor --site development.localhost
```

**What it checks:**
1. **Site Health:**
   - Site exists and is accessible
   - Database connectivity
   - Redis connectivity (cache, queue, socketio)

2. **Scheduler Status:**
   - Enabled/disabled state
   - Last execution time
   - Pending scheduled events

3. **Worker Status:**
   - Active workers per queue
   - Queue depths (short, default, long)
   - Failed job counts

4. **Queue Statistics:**
   - Pending jobs in each queue
   - Currently processing jobs
   - Failed jobs requiring attention

5. **System Resources:**
   - Memory usage
   - Disk space
   - Database size

6. **Configuration Issues:**
   - Missing configuration values
   - Invalid settings
   - Potential problems

**Example output:**
```
Site: development.localhost
Status: Active ✓

Database:
  Status: Connected ✓
  Size: 245 MB

Redis:
  Cache: Connected ✓
  Queue: Connected ✓
  SocketIO: Connected ✓

Scheduler:
  Status: Enabled ✓
  Last run: 2 minutes ago
  Pending events: 0

Workers:
  short queue: 1 active ✓
  default queue: 2 active ✓
  long queue: 1 active ✓

Queues:
  short: 0 pending
  default: 3 pending
  long: 0 pending

Failed Jobs: 0 ✓

Disk Space:
  Available: 45 GB / 100 GB (45% used)

Memory:
  Available: 2.1 GB / 4 GB (47% used)
```

**Use cases:**
- Troubleshooting performance issues
- Checking worker/scheduler status
- Verifying queue health
- System health monitoring
- Pre-deployment checks

### Interpreting Doctor Results

**Healthy system indicators:**
- All connections show "Connected ✓"
- Scheduler is "Enabled ✓" and recently ran
- Workers are active for all queues
- Failed jobs count is 0 or low
- Queue depths are reasonable (< 100 pending)

**Problem indicators:**
- "Connection failed" for Redis/Database
- Scheduler shows "Disabled" or "Not running"
- No active workers
- High failed job count (> 10)
- Queue depth growing (> 500 pending)
- Low disk space (< 10% available)

## Helpful Shortcuts

### List All Sites
```bash
bench --site all list
```

Shows all sites in the bench.

### Switch Branch
```bash
cd apps/soldamundo
git checkout develop
cd ../..
bench update --apps soldamundo
```

Switches app to different branch and updates.

### Backup Before Risky Operation
```bash
bench --site development.localhost backup --backup-path "backups/before-risky-change"
# ... perform risky operation ...
```

Always backup before potentially destructive operations.
