---
name: atuin-guide
description: Atuin shell history management with SQLite database, fuzzy search, metadata tracking, and SQL query examples for history analysis
---

# Atuin

[Atuin](https://github.com/atuinsh/atuin) is a powerful shell history tool that replaces the default shell history with a SQLite database. It provides enhanced history search, synchronization across machines, and rich metadata for each command.

## Features

- **SQLite-based history**: All command history is stored in a SQLite database
- **Rich metadata**: Stores timestamp, duration, exit code, working directory, hostname, and session info
- **Fuzzy search**: Powerful fuzzy search with vim-style keybindings
- **Privacy-focused**: Auto-sync disabled by default in this configuration

## Configuration

The configuration is managed in `home-manager/atuin/default.nix`:

- **Database location**: `~/.local/share/atuin/history.db`
- **Search mode**: Fuzzy search with vim-normal keymap
- **Filter mode**: Host-based filtering
- **Auto-sync**: Disabled (can be enabled if needed)

## Accessing the History Database

Atuin stores all command history in a SQLite database at `~/.local/share/atuin/history.db`. You can query this database directly using the `sqlite3` command.

### Database Schema

The main table is `history` with the following structure:

```sql
CREATE TABLE history (
    id text primary key,
    timestamp integer not null,
    duration integer not null,
    exit integer not null,
    command text not null,
    cwd text not null,
    session text not null,
    hostname text not null,
    deleted_at integer
);
```

### Useful SQL Queries

#### 1. View Recent Commands

```bash
sqlite3 -column -header ~/.local/share/atuin/history.db \
  "SELECT
     datetime(timestamp/1000000000, 'unixepoch', 'localtime') as time,
     command,
     exit,
     duration/1000000 as duration_ms
   FROM history
   WHERE deleted_at IS NULL
   ORDER BY timestamp DESC
   LIMIT 20"
```

#### 2. Most Frequently Used Commands

```bash
sqlite3 -column -header ~/.local/share/atuin/history.db \
  "SELECT
     command,
     count(*) as count
   FROM history
   WHERE deleted_at IS NULL
   GROUP BY command
   ORDER BY count DESC
   LIMIT 20"
```

#### 3. Commands by Directory

```bash
sqlite3 -column -header ~/.local/share/atuin/history.db \
  "SELECT
     datetime(timestamp/1000000000, 'unixepoch', 'localtime') as time,
     command,
     cwd
   FROM history
   WHERE cwd LIKE '%your-directory%'
     AND deleted_at IS NULL
   ORDER BY timestamp DESC
   LIMIT 20"
```

#### 4. Failed Commands (non-zero exit codes)

```bash
sqlite3 -column -header ~/.local/share/atuin/history.db \
  "SELECT
     datetime(timestamp/1000000000, 'unixepoch', 'localtime') as time,
     command,
     exit,
     cwd
   FROM history
   WHERE exit != 0
     AND deleted_at IS NULL
   ORDER BY timestamp DESC
   LIMIT 20"
```

#### 5. Longest Running Commands

```bash
sqlite3 -column -header ~/.local/share/atuin/history.db \
  "SELECT
     command,
     duration/1000000000.0 as duration_sec,
     datetime(timestamp/1000000000, 'unixepoch', 'localtime') as time
   FROM history
   WHERE deleted_at IS NULL
   ORDER BY duration DESC
   LIMIT 20"
```

#### 6. Total Command Count

```bash
sqlite3 ~/.local/share/atuin/history.db \
  "SELECT count(*) as total_commands
   FROM history
   WHERE deleted_at IS NULL"
```

#### 7. Command Statistics by Hour

```bash
sqlite3 -column -header ~/.local/share/atuin/history.db \
  "SELECT
     strftime('%H', datetime(timestamp/1000000000, 'unixepoch', 'localtime')) as hour,
     count(*) as count
   FROM history
   WHERE deleted_at IS NULL
   GROUP BY hour
   ORDER BY hour"
```

### Interactive SQLite Mode

For more exploratory analysis, you can enter interactive mode:

```bash
sqlite3 ~/.local/share/atuin/history.db
```

Useful commands in interactive mode:

```sql
.tables                -- List all tables
.schema history        -- Show table structure
.mode column          -- Enable column display mode
.headers on           -- Show column headers
.quit                 -- Exit interactive mode
```

### Example Analysis Session

```bash
# Enter interactive mode
sqlite3 ~/.local/share/atuin/history.db

# Set display options
.mode column
.headers on

# Run custom queries
SELECT
  strftime('%Y-%m-%d', datetime(timestamp/1000000000, 'unixepoch', 'localtime')) as date,
  count(*) as commands
FROM history
WHERE deleted_at IS NULL
GROUP BY date
ORDER BY date DESC
LIMIT 30;

# Exit
.quit
```

## Tips

1. **Backup your history**: The database is stored locally and is not synced by default
   ```bash
   cp ~/.local/share/atuin/history.db ~/.local/share/atuin/history.db.backup
   ```

2. **Export to CSV**: You can export query results to CSV format
   ```bash
   sqlite3 -header -csv ~/.local/share/atuin/history.db \
     "SELECT * FROM history WHERE deleted_at IS NULL LIMIT 100" > history.csv
   ```

3. **Database size**: Check the database file size
   ```bash
   ls -lh ~/.local/share/atuin/history.db
   ```

4. **Vacuum database**: Optimize database size by removing deleted entries
   ```bash
   sqlite3 ~/.local/share/atuin/history.db "VACUUM;"
   ```

## Related Documentation

- [Shell configuration](docs/20_nix.md)
- [Development tools](docs/50_npm_tools.md)
