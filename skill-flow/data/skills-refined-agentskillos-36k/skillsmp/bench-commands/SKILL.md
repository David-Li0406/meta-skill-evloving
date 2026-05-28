---
name: bench-commands
description: Comprehensive reference for Frappe bench CLI commands including site management, app installation, backup/restore, database operations, migrations, and development workflows. Use when users ask about bench commands, site setup, database operations, backup/restore procedures, MariaDB configuration, or common development workflows in Frappe.
---

# Bench Commands

## Overview

This skill provides comprehensive guidance for using the Frappe bench command-line interface in development environments, covering all aspects from site creation to production backup restoration.

## Environment Constants

When working with bench commands, use these standard development environment values:

- **Site Name**: `development.localhost`
- **Database Root Password**: `123`
- **Admin Password**: `admin`
- **Bench Path**: `/workspace/development/frappe-bench`

All commands assume execution from the bench directory unless otherwise specified.

## Command Categories

Commands are organized by functional area. See the corresponding reference file for detailed information:

### Site Management
See [references/site-management.md](references/site-management.md) for:
- Creating new sites
- Dropping sites (with automatic backup)
- Reinstalling sites
- Site configuration

### App Management
See [references/app-management.md](references/app-management.md) for:
- Installing apps to sites
- Uninstalling apps from sites
- Getting apps from repositories
- Managing multiple apps

### App Development
See [references/app-development.md](references/app-development.md) for:
- Creating new Frappe apps
- Managing app remotes
- Branch switching and management
- Dependency validation
- App development workflows

### Backup and Restore
See [references/backup-restore.md](references/backup-restore.md) for:
- Creating full or database-only backups
- Restoring from production backups
- Handling encryption keys
- Backup file management

### Database Operations
See [references/database-operations.md](references/database-operations.md) for:
- Running migrations
- Executing specific patches
- Accessing database consoles
- MariaDB runtime configuration (memory limits, packet sizes)
- Performance tuning for large operations

### Database Maintenance
See [references/database-maintenance.md](references/database-maintenance.md) for:
- Removing deleted DocType tables and columns
- Table analysis and statistics
- Index management
- Database optimization

### Development Operations
See [references/development-operations.md](references/development-operations.md) for:
- Starting/stopping the development server
- Building assets
- Watching for changes
- Clearing caches
- Managing developer mode

### Testing and Debugging
See [references/testing-debugging.md](references/testing-debugging.md) for:
- Running test suites
- Running specific tests
- Using the Python console
- Executing Python code
- Code coverage

### Job Queue Management
See [references/job-queue.md](references/job-queue.md) for:
- Starting and managing workers
- Scheduler control
- Viewing pending jobs
- Queue diagnostics and troubleshooting

### Translation Operations
See [references/translation-operations.md](references/translation-operations.md) for:
- Complete translation workflow (POT/PO/MO)
- CSV to PO migration
- Translation compilation
- Managing translations for multiple locales

### Utilities
See [references/utilities.md](references/utilities.md) for:
- Setting/getting configuration values
- Managing the scheduler
- RQ job queue management (clearing jobs, purging queues)
- Reloading doctypes
- Resetting passwords
- Version checking
- System diagnostics

### More Commands
See [references/more-commands.md](references/more-commands.md) for:
- User management commands
- Data import/export operations
- Search and indexing
- Production setup commands
- NGINX and SSL configuration
- And many more specialized commands

## Common Workflows

For complete step-by-step workflows, see [references/workflows.md](references/workflows.md):
- **Fresh Install**: Complete setup from scratch
- **Restore from Production**: Migrating production backups to development
- **Quick Reinstall**: Reinstalling apps without dropping the site
- **Large Database Restore**: Configuring MariaDB for large backups

## Usage

When a user asks about bench commands or needs help with Frappe development operations:

1. **Identify the category** of their request (site management, backup, database, etc.)
2. **Reference the appropriate section** from references/ directory
3. **Provide the specific commands** with the correct environment constants
4. **Include important notes** about prerequisites or side effects

Always ensure commands use the correct site name (`development.localhost`) and include necessary flags like `--db-root-password` when required.

## Key Principles

- **Always specify site name**: Most commands require `--site development.localhost`
- **Database root access**: Use `--db-root-password 123` for operations requiring database root access
- **Developer mode**: Enable for development work with `bench --site development.localhost set-config developer_mode 1`
- **Cache clearing**: After code or configuration changes, run `bench clear-cache`
- **Migration after changes**: Run `bench --site development.localhost migrate` after app installations or updates

## Important Notes

- Backups are automatically created in `./sites/development.localhost/private/backups/` unless specified otherwise
- Runtime MariaDB settings (memory limits) are lost on container restart - add to docker-compose.yml to persist
- **Database users are lost on MariaDB container restart** - if you get "Access denied" errors, recreate the database user (see [database-operations.md](references/database-operations.md#access-denied-for-user-after-container-restart))
- When recreating a site, always set the encryption_key from backup before restoring data
- Use `--skip-search-index` flag with migrate for faster migrations during development
