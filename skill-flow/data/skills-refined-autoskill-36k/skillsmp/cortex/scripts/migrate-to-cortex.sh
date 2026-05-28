#!/bin/bash
set -euo pipefail

# Migration script: comms -> cortex
# This script migrates your existing comms data to the new cortex format:
# 1. Moves config directory from ~/.config/comms -> ~/.config/cortex
# 2. Moves data directory from ~/Library/Application Support/Comms -> ~/Library/Application Support/Cortex
# 3. Renames database from comms.db to cortex.db
# 4. Applies schema migrations (conversations -> segments, drops checkpoints, adds metadata_json)

echo "=== Cortex Migration Script ==="
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OLD_DATA_DIR="$HOME/Library/Application Support/Comms"
    NEW_DATA_DIR="$HOME/Library/Application Support/Cortex"
else
    OLD_DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/comms"
    NEW_DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/cortex"
fi

OLD_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/comms"
NEW_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/cortex"

OLD_DB_PATH="$OLD_DATA_DIR/comms.db"
NEW_DB_PATH="$NEW_DATA_DIR/cortex.db"

# Check if migration is needed
if [[ ! -d "$OLD_DATA_DIR" ]] && [[ ! -d "$OLD_CONFIG_DIR" ]]; then
    echo "No existing comms installation found. Nothing to migrate."
    exit 0
fi

if [[ -f "$NEW_DB_PATH" ]]; then
    echo "WARNING: cortex.db already exists at $NEW_DB_PATH"
    echo "This migration would overwrite it."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Migration aborted."
        exit 1
    fi
fi

echo "Migration plan:"
echo "  Config: $OLD_CONFIG_DIR -> $NEW_CONFIG_DIR"
echo "  Data:   $OLD_DATA_DIR -> $NEW_DATA_DIR"
echo "  DB:     comms.db -> cortex.db (with schema changes)"
echo ""
read -p "Proceed with migration? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Migration aborted."
    exit 1
fi

# Step 1: Move config directory
if [[ -d "$OLD_CONFIG_DIR" ]]; then
    echo "Moving config directory..."
    mkdir -p "$(dirname "$NEW_CONFIG_DIR")"
    if [[ -d "$NEW_CONFIG_DIR" ]]; then
        echo "  Merging into existing cortex config..."
        cp -rn "$OLD_CONFIG_DIR"/* "$NEW_CONFIG_DIR"/ 2>/dev/null || true
    else
        mv "$OLD_CONFIG_DIR" "$NEW_CONFIG_DIR"
    fi
    echo "  Done."
fi

# Step 2: Move data directory  
if [[ -d "$OLD_DATA_DIR" ]]; then
    echo "Moving data directory..."
    mkdir -p "$NEW_DATA_DIR"
    
    # Move all files except the database (we'll handle that specially)
    for f in "$OLD_DATA_DIR"/*; do
        if [[ "$f" != "$OLD_DB_PATH" ]] && [[ -e "$f" ]]; then
            mv "$f" "$NEW_DATA_DIR/" 2>/dev/null || true
        fi
    done
    echo "  Done."
fi

# Step 3: Migrate database schema and rename
if [[ -f "$OLD_DB_PATH" ]]; then
    echo "Migrating database schema..."
    
    # Create backup
    BACKUP_PATH="$OLD_DB_PATH.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$OLD_DB_PATH" "$BACKUP_PATH"
    echo "  Backup created: $BACKUP_PATH"
    
    # Apply schema migrations using sqlite3
    # Main transaction for table renames
    sqlite3 "$OLD_DB_PATH" << 'EOF'
BEGIN TRANSACTION;

-- Step 1: Rename conversation_definitions -> segment_definitions
ALTER TABLE conversation_definitions RENAME TO segment_definitions;

-- Step 2: Rename conversations -> segments  
ALTER TABLE conversations RENAME TO segments;

-- Step 3: Rename conversation_events -> segment_events
ALTER TABLE conversation_events RENAME TO segment_events;

-- Step 4: Drop indexes that reference old names
DROP INDEX IF EXISTS idx_conversations_definition;
DROP INDEX IF EXISTS idx_conversations_channel;
DROP INDEX IF EXISTS idx_conversations_thread;
DROP INDEX IF EXISTS idx_conversations_time;
DROP INDEX IF EXISTS idx_conversation_events_event;

-- Step 5: Create new indexes with correct names
CREATE INDEX IF NOT EXISTS idx_segments_definition ON segments(definition_id);
CREATE INDEX IF NOT EXISTS idx_segments_channel ON segments(channel);
CREATE INDEX IF NOT EXISTS idx_segments_thread ON segments(thread_id);
CREATE INDEX IF NOT EXISTS idx_segments_time ON segments(start_time, end_time);
CREATE INDEX IF NOT EXISTS idx_segment_events_event ON segment_events(event_id);

-- Step 6: Drop checkpoint tables (no longer needed)
DROP TABLE IF EXISTS checkpoint_quality;
DROP TABLE IF EXISTS turn_facets;
DROP TABLE IF EXISTS checkpoints;

-- Step 7: Update schema version
INSERT OR REPLACE INTO schema_version (version, applied_at) VALUES (12, strftime('%s', 'now'));

COMMIT;
EOF

    if [[ $? -ne 0 ]]; then
        echo "  ERROR: Table migration failed!"
        echo "  Restoring from backup..."
        cp "$BACKUP_PATH" "$OLD_DB_PATH"
        exit 1
    fi
    
    # Add metadata_json column (separate statement, may fail if exists - that's ok)
    sqlite3 "$OLD_DB_PATH" "ALTER TABLE events ADD COLUMN metadata_json TEXT;" 2>/dev/null || true
    
    # Create FTS5 index if not exists
    sqlite3 "$OLD_DB_PATH" << 'FTS_EOF'
-- Create FTS5 table for event search
CREATE VIRTUAL TABLE IF NOT EXISTS events_fts USING fts5(
    event_id UNINDEXED,
    channel UNINDEXED,
    content,
    tokenize='porter unicode61'
);

-- Populate FTS index from existing events
INSERT OR IGNORE INTO events_fts(event_id, channel, content)
SELECT id, channel, COALESCE(content, '') FROM events;

-- Create triggers for future updates
CREATE TRIGGER IF NOT EXISTS events_fts_insert AFTER INSERT ON events BEGIN
    INSERT INTO events_fts(event_id, channel, content)
    VALUES (new.id, new.channel, COALESCE(new.content, ''));
END;

CREATE TRIGGER IF NOT EXISTS events_fts_update AFTER UPDATE ON events BEGIN
    DELETE FROM events_fts WHERE event_id = old.id;
    INSERT INTO events_fts(event_id, channel, content)
    VALUES (new.id, new.channel, COALESCE(new.content, ''));
END;

CREATE TRIGGER IF NOT EXISTS events_fts_delete AFTER DELETE ON events BEGIN
    DELETE FROM events_fts WHERE event_id = old.id;
END;
FTS_EOF
    
    echo "  Schema migrated successfully."
    
    # Move and rename database
    mv "$OLD_DB_PATH" "$NEW_DB_PATH"
    echo "  Database moved to: $NEW_DB_PATH"
    
    # Also move WAL and SHM files if they exist
    [[ -f "$OLD_DB_PATH-wal" ]] && mv "$OLD_DB_PATH-wal" "$NEW_DB_PATH-wal"
    [[ -f "$OLD_DB_PATH-shm" ]] && mv "$OLD_DB_PATH-shm" "$NEW_DB_PATH-shm"
fi

# Step 4: Clean up empty old directories
rmdir "$OLD_DATA_DIR" 2>/dev/null || true
rmdir "$OLD_CONFIG_DIR" 2>/dev/null || true

echo ""
echo "=== Migration Complete ==="
echo ""
echo "Your data has been migrated to:"
echo "  Config: $NEW_CONFIG_DIR"
echo "  Data:   $NEW_DATA_DIR"
echo "  DB:     $NEW_DB_PATH"
echo ""
echo "Backup of original database: $BACKUP_PATH"
echo ""
echo "You can now use 'cortex' instead of 'comms'."
