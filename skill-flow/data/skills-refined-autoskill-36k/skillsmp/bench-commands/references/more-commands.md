# More Commands Reference

This file provides a brief overview of additional bench commands not covered in detail in other reference files. Use `bench <command> --help` to get detailed information about any command.

---

## User Management

### add-user
```bash
bench --site development.localhost add-user email@example.com --help
```
Add a new user to a site with specified role and permissions.

**Options:** `--first-name`, `--last-name`, `--password`, `--user-type`, `--add-role`, `--send-welcome-email`

### add-system-manager
```bash
bench --site development.localhost add-system-manager email@example.com --help
```
Add a new system manager (admin) user to a site.

**Options:** `--first-name`, `--last-name`, `--password`, `--send-welcome-email`

### disable-user
```bash
bench --site development.localhost disable-user email@example.com --help
```
Disable a user account, preventing login.

### set-last-active-for-user
```bash
bench --site development.localhost set-last-active-for-user --help
```
Update user's last active timestamp to current datetime.

**Options:** `--user TEXT`

### destroy-all-sessions
```bash
bench --site development.localhost destroy-all-sessions --help
```
Clear all user sessions (logs everyone out).

**Options:** `--reason TEXT`

---

## Site Operations

### use
```bash
bench use development.localhost
```
Set a default site for bench commands. After setting, you can omit `--site` flag.

### browse
```bash
bench --site development.localhost browse --help
```
Opens the site in your default web browser.

**Options:** `--user TEXT` (login as specific user), `--session-end TEXT`, `--user-for-audit TEXT`

### add-to-hosts
```bash
bench --site development.localhost add-to-hosts
```
Add the site to your `/etc/hosts` file (requires sudo).

### set-maintenance-mode
```bash
bench --site development.localhost set-maintenance-mode on
bench --site development.localhost set-maintenance-mode off
```
Put site in maintenance mode (shows maintenance page to users).

**Options:** `--site TEXT`

### ngrok
```bash
bench --site development.localhost ngrok --help
```
Start an ngrok tunnel to your local development server for external access.

**Options:** `--bind-tls`, `--use-default-authtoken`

---

## Data Operations

### export-fixtures
```bash
bench --site development.localhost export-fixtures --help
```
Export fixtures defined in app's `hooks.py` to JSON files.

**Options:** `--app TEXT` (export for specific app only)

### export-json
```bash
bench --site development.localhost export-json "DocType Name" output/path --help
```
Export DocType records as JSON files.

**Options:** `--name TEXT` (export specific document)

### export-csv
```bash
bench --site development.localhost export-csv "DocType Name" output.csv
```
Export data import template with existing data for a DocType.

### export-doc
```bash
bench --site development.localhost export-doc "DocType Name" "Document Name"
```
Export a single document to CSV format.

### import-doc
```bash
bench --site development.localhost import-doc path/to/file.json --help
```
Import document(s) from JSON file(s). If path is directory, imports all `.json` files.

### data-import
```bash
bench --site development.localhost data-import --help
```
Bulk import documents from CSV or XLSX file.

**Options:**
- `--file FILE` (required): Path to import file
- `--doctype TEXT` (required): Target DocType
- `--type [insert|update]`: Insert new or update existing
- `--submit-after-import`: Submit documents after import
- `--mute-emails`: Don't send emails during import

### bulk-rename
```bash
bench --site development.localhost bulk-rename "DocType Name" rename.csv
```
Rename multiple documents via CSV file (old_name,new_name format).

---

## Database Console Access

### postgres
```bash
bench --site development.localhost postgres [EXTRA_ARGS]...
```
Enter PostgreSQL console for the site (if using PostgreSQL).

### mariadb (covered in database-operations.md)
Access MariaDB console. See [database-operations.md](database-operations.md).

---

## Search and Indexing

### build-search-index
```bash
bench --site development.localhost build-search-index
```
Rebuild search index used by global search feature.

### rebuild-global-search
```bash
bench --site development.localhost rebuild-global-search --help
```
Setup help table for global search functionality.

**Options:** `--static-pages` (rebuild for static pages)

---

## DocType Operations

### reload-doc
```bash
bench --site development.localhost reload-doc "Module Name" "DocType" "DocType Name"
```
Reload schema for a specific DocType. More precise than `reload-doctype`.

**Example:**
```bash
bench --site development.localhost reload-doc "Selling" "DocType" "Sales Order"
```

### reload-doctype (covered in utilities.md)
Reload DocType schema. See [utilities.md](utilities.md).

### reset-perms
```bash
bench --site development.localhost reset-perms
```
Reset permissions for all doctypes to their default state.

---

## Bench Management

### init
```bash
bench init frappe-bench --help
```
Initialize a new bench instance.

**Key options:**
- `--frappe-branch TEXT`: Clone specific Frappe branch
- `--python TEXT`: Path to Python executable
- `--apps_path TEXT`: JSON file with apps to install
- `--frappe-path TEXT`: Path to local Frappe repo
- `--skip-assets`: Don't build assets
- `--install-app TEXT`: Install app after init

### find
```bash
bench find [LOCATION]
```
Recursively find bench instances from specified location.

### src
```bash
bench src
```
Prints bench source folder path. Useful for scripting: `cd $(bench src)`

### app-cache
```bash
bench app-cache --help
```
View or manage get-app cache.

**Options:**
- `--clear`: Remove all cached items
- `--remove-app TEXT`: Remove cache for specific app
- `--remove-key TEXT`: Remove specific cache key

---

## App Management Utilities

### exclude-app
```bash
bench exclude-app app_name
```
Exclude app from automatic updates via `bench update`.

### include-app
```bash
bench include-app app_name
```
Include previously excluded app in updates.

### remove-from-installed-apps
```bash
bench --site development.localhost remove-from-installed-apps app_name
```
Remove app from site's installed apps list without full uninstall.

### list-apps
```bash
bench --site development.localhost list-apps --help
```
List all apps installed on a site.

**Options:** `-f, --format [text|json]`

---

## Production and System

### disable-production
```bash
sudo bench disable-production
```
Disables production environment for the bench. Requires superuser privileges.

### install
```bash
sudo bench install
```
Install system dependencies for setting up Frappe/ERPNext. Requires superuser privileges.

### restart
```bash
bench restart --help
```
Restart supervisor processes or systemd units.

**Options:** `--web`, `--supervisor`, `--systemd`

### renew-lets-encrypt
```bash
sudo bench renew-lets-encrypt
```
Renew Let's Encrypt SSL certificates. Requires superuser privileges.

---

## Redis Configuration

### set-redis-cache-host
```bash
bench set-redis-cache-host localhost:6379
```
Set Redis cache host for bench.

### set-redis-queue-host
```bash
bench set-redis-queue-host localhost:6380
```
Set Redis queue host for bench.

### set-redis-socketio-host
```bash
bench set-redis-socketio-host localhost:6381
```
Set Redis socketio host for bench.

### create-rq-users
```bash
bench --site development.localhost create-rq-users --help
```
Create Redis Queue users with ACL authentication.

**Options:**
- `--set-admin-password`: Set new Redis admin password
- `--use-rq-auth`: Enable Redis authentication for sites

---

## NGINX and SSL

### set-nginx-port
```bash
bench set-nginx-port development.localhost 8080
```
Set NGINX port for a specific site.

### set-ssl-certificate
```bash
bench set-ssl-certificate development.localhost /path/to/cert.pem
```
Set SSL certificate path for site.

### set-ssl-key
```bash
bench set-ssl-key development.localhost /path/to/key.pem
```
Set SSL certificate private key path for site.

### set-url-root
```bash
bench set-url-root development.localhost https://example.com
```
Set URL root for a site.

---

## MariaDB Configuration

### set-mariadb-host
```bash
bench set-mariadb-host localhost
```
Set MariaDB host for bench.

---

## Advanced Development

### jupyter
```bash
bench --site development.localhost jupyter
```
Start an interactive Jupyter notebook with Frappe context.

### setup-chrome
```bash
bench --site development.localhost setup-chrome
```
Setup Chrome (server-side) for PDF generation.

### clear-website-cache
```bash
bench --site development.localhost clear-website-cache
```
Clear website-specific cache (separate from general cache).

### request
```bash
bench --site development.localhost request --help
```
Run a request as an admin user (for testing API endpoints).

**Options:**
- `--args TEXT`: Query string arguments
- `--path TEXT`: Path to JSON request file

---

## Frappe Recorder

### start-recording
```bash
bench --site development.localhost start-recording
```
Start Frappe Recorder for performance profiling.

### stop-recording
```bash
bench --site development.localhost stop-recording
```
Stop Frappe Recorder and save results.

**Usage:** Navigate to `/app/recorder` to view recorded requests and queries.

---

## Patch Management

### create-patch
```bash
bench --site development.localhost create-patch
```
Interactively create a new patch file for app.

---

## Email Queue

### add-to-email-queue
```bash
bench --site development.localhost add-to-email-queue /path/to/email.json
```
Add an email to the Email Queue for sending.

---

## Testing

### run-ui-tests
```bash
bench --site development.localhost run-ui-tests app_name --help
```
Run Cypress UI tests for an app.

**Options:**
- `--headless`: Run in headless mode
- `--parallel`: Run tests in parallel
- `--with-coverage`: Generate coverage report
- `--browser TEXT`: Browser to use
- `--ci-build-id TEXT`: CI build identifier

### run-parallel-tests
```bash
bench --site development.localhost run-parallel-tests --help
```
Run tests in parallel (typically used in CI/CD).

**Options:**
- `--app TEXT`: App to test
- `--build-number INTEGER`: Build number
- `--total-builds INTEGER`: Total number of builds
- `--with-coverage`: Generate coverage
- `--use-orchestrator`: Use test orchestrator
- `--dry-run`: Don't actually run tests

---

## Migration and Backup

### partial-restore
```bash
bench --site development.localhost partial-restore backup.sql.gz --help
```
Restore specific tables from a backup. See https://frappeframework.com/docs for details.

**Options:**
- `--verbose`: Verbose output
- `--encryption-key TEXT`: Backup encryption key

### ready-for-migration
```bash
bench --site development.localhost ready-for-migration --help
```
Check if site is ready for migration to another hosting provider.

---

## Environment Management

### migrate-env
```bash
bench migrate-env python3.11 --help
```
Migrate virtual environment to different Python version.

**Options:** `--no-backup`

---

## Update Operations

### retry-upgrade
```bash
bench retry-upgrade --help
```
Retry a failed bench upgrade operation.

**Options:** `--version INTEGER`

### switch-to-develop
Covered in [app-development.md](app-development.md) - Switch frappe and erpnext to develop branch.

---

## Bench Configuration

### config (subcommands)
Access configuration subcommands via `bench config <subcommand>`.

#### dns_multitenant
```bash
bench config dns_multitenant --help
```
Enable/disable bench multitenancy on production.

#### http_timeout
```bash
bench config http_timeout --help
```
Set HTTP timeout for bench operations.

#### rebase_on_pull
```bash
bench config rebase_on_pull --help
```
Enable/disable repository rebase on pull during update.

#### remove-common-config
```bash
bench config remove-common-config --help
```
Remove specific keys from current bench's common config.

#### restart_supervisor_on_update
```bash
bench config restart_supervisor_on_update --help
```
Enable/disable automatic supervisor restart after updates.

#### restart_systemd_on_update
```bash
bench config restart_systemd_on_update --help
```
Enable/disable automatic systemd restart after updates.

#### serve_default_site
```bash
bench config serve_default_site --help
```
Configure nginx to serve the default site on port 80.

#### set-common-config
```bash
bench config set-common-config --help
```
Set value in common config file.

---

## Setup Operations

### setup (subcommands)
Access setup subcommands via `bench setup <subcommand>`. Most are for production deployment.

#### add-domain
```bash
bench setup add-domain site.local custom.domain.com
```
Add a custom domain to a site.

#### remove-domain
```bash
bench setup remove-domain site.local custom.domain.com
```
Remove custom domain from a site.

#### backups
```bash
bench setup backups
```
Add cronjob for automatic bench backups.

#### config
```bash
bench setup config
```
Generate or overwrite `sites/common_site_config.json`.

#### env
```bash
bench setup env
```
Setup Python virtual environment for bench.

#### requirements
```bash
bench setup requirements --help
```
Install Python and Node.js dependencies for all apps.

#### procfile
```bash
bench setup procfile
```
Generate Procfile for `bench start`.

#### redis
```bash
bench setup redis
```
Generate Redis configuration files.

#### nginx
```bash
sudo bench setup nginx
```
Generate NGINX configuration files.

#### reload-nginx
```bash
sudo bench setup reload-nginx
```
Check NGINX config and reload service.

#### supervisor
```bash
sudo bench setup supervisor
```
Generate supervisor configuration for production.

#### systemd
```bash
sudo bench setup systemd
```
Generate systemd service files for production.

#### production
```bash
sudo bench setup production [USER]
```
Complete production environment setup (nginx, supervisor/systemd, etc.).

#### lets-encrypt
```bash
sudo bench setup lets-encrypt [EMAIL]
```
Setup Let's Encrypt SSL certificate for site.

#### wildcard-ssl
```bash
sudo bench setup wildcard-ssl [DOMAIN]
```
Setup wildcard SSL certificate for multi-tenant bench.

#### sync-domains
```bash
bench setup sync-domains
```
Check and sync any domain changes.

#### manager
```bash
bench setup manager
```
Setup bench-manager.local site with bench_manager app.

#### fail2ban
```bash
sudo bench setup fail2ban
```
Setup fail2ban intrusion prevention software.

#### firewall
```bash
sudo bench setup firewall
```
Setup firewall for system.

#### ssh-port
```bash
sudo bench setup ssh-port [PORT]
```
Set SSH port for system.

#### sudoers
```bash
sudo bench setup sudoers [USER]
```
Add commands to sudoers list for password-less execution.

#### fonts
```bash
sudo bench setup fonts
```
Add Frappe fonts to system.

#### role
```bash
bench setup role [ROLE]
```
Install dependencies via ansible roles.

#### socketio
```bash
bench setup socketio
```
**[DEPRECATED]** Setup node dependencies for socketio server.

---

## Bench Update

### update
```bash
bench update --help
```
Comprehensive update operation for bench.

**Options:**
- `--pull`: Pull updates for all apps
- `--apps TEXT`: Update specific apps only
- `--patch`: Run migrations/patches
- `--build`: Build JS/CSS assets
- `--requirements`: Update dependencies
- `--restart-supervisor`: Restart supervisor after update
- `--restart-systemd`: Restart systemd after update
- `--no-backup`: Skip backup (not recommended for production)
- `--force`: Force major version upgrades
- `--reset`: Hard reset git branches (discards local changes)

**Common usage:**
```bash
# Full update (default)
bench update

# Pull only
bench update --pull

# Pull and patch
bench update --pull --patch

# Pull, patch, and build
bench update --pull --patch --build

# Full update for specific apps
bench update --apps frappe,erpnext

# Force major upgrade
bench update --force
```

---

## Python Package Management

### pip
```bash
bench pip --help
```
Wrapper for pip commands in bench's virtual environment.

**Usage:**
```bash
# Install package
bench pip install package-name

# Uninstall package
bench pip uninstall package-name

# List installed packages
bench pip list

# Show package info
bench pip show package-name

# Install from requirements
bench pip install -r requirements.txt
```

---

## Remote Management (covered in app-development.md)

- `remote-urls`: Show app remote URLs
- `remote-set-url`: Set app remote URL
- `remote-reset-url`: Reset to frappe official URL

See [app-development.md](app-development.md) for details.

---

## Version Info

### version
Covered in [utilities.md](utilities.md) - Show versions of all installed apps.

---

## Notes

- Commands marked as requiring `sudo` need superuser privileges
- Production commands (`setup`, `install`, etc.) should be run on production servers only
- Most setup subcommands are for initial production deployment
- Use `bench <command> --help` for detailed information about any command
- Many commands support `--site` flag to specify target site
- Commands without site flag typically operate at bench level

---

## Getting More Help

For any command:
```bash
bench <command> --help
bench <command> <subcommand> --help
```

For Frappe framework documentation:
- https://frappeframework.com/docs
- https://discuss.frappe.io (Community forum)
