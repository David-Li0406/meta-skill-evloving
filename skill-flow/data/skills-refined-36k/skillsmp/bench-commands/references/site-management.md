# Site Management

## Create a New Site

```bash
bench new-site development.localhost --admin-password admin --db-root-password 123
```

Creates a new Frappe site with the specified credentials.

**Parameters:**
- `--admin-password admin`: Sets the Administrator user password
- `--db-root-password 123`: MariaDB root password for creating the database

## Drop a Site

```bash
bench drop-site development.localhost --db-root-password 123
```

Drops (deletes) a site completely. This command:
- Automatically creates a backup before dropping
- Moves the site to `archived/sites/` directory
- Removes the site's database
- Cleans up site files

**Warning:** This is destructive. Always ensure you have recent backups.

## Reinstall a Site (Drop and Recreate)

```bash
bench drop-site development.localhost --db-root-password 123
bench new-site development.localhost --admin-password admin --db-root-password 123
```

Complete site reinstallation. Use this when you need a fresh start.

**After reinstalling, remember to:**
1. Install your apps again
2. Run migrations
3. Re-enable developer mode if needed
4. Restore data if needed
