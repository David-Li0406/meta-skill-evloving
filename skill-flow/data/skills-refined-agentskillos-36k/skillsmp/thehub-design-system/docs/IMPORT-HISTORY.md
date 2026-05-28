# Import History & Rollback System

## Overview

TheHUB includes a comprehensive import history and rollback system that tracks all data imports and allows administrators to undo imports if needed.

## Features

- **Complete Import Tracking**: Every import operation is logged with full statistics
- **Granular Record Tracking**: Individual records (created/updated) are tracked for precise rollback
- **Full Rollback Capability**: Undo an entire import by deleting created records and restoring updated records
- **Import History UI**: View all imports with detailed statistics and error logs
- **Error Logging**: Failed imports and individual record errors are captured

## Database Schema

### import_history Table

Tracks each import operation:

```sql
CREATE TABLE import_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    import_type ENUM('riders', 'results', 'events', 'clubs', 'uci', 'other'),
    filename VARCHAR(255),
    file_size INT,
    status ENUM('completed', 'failed', 'rolled_back'),
    total_records INT,
    success_count INT,
    updated_count INT,
    failed_count INT,
    skipped_count INT,
    error_summary TEXT,
    imported_by VARCHAR(100),
    imported_at TIMESTAMP,
    rolled_back_at TIMESTAMP NULL,
    rolled_back_by VARCHAR(100) NULL,
    notes TEXT
);
```

### import_records Table

Tracks individual records affected by imports:

```sql
CREATE TABLE import_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    import_id INT NOT NULL,
    record_type ENUM('rider', 'result', 'event', 'club'),
    record_id INT NOT NULL,
    action ENUM('created', 'updated'),
    old_data JSON NULL,
    created_at TIMESTAMP
);
```

## Usage

### 1. Integrating Import History into Import Scripts

```php
// Load helper functions
require_once __DIR__ . '/../includes/import-history.php';

// Start import tracking
$importId = startImportHistory(
    $db,
    'uci',                          // Import type
    $file['name'],                   // Filename
    $file['size'],                   // File size
    $current_admin['username']       // Username
);

// Perform your import...
$result = importData($filepath, $db, $importId);

// Update with final statistics
updateImportHistory($db, $importId, $stats, $errors, 'completed');

// Track individual records
if ($action === 'created') {
    trackImportRecord($db, $importId, 'rider', $riderId, 'created');
} else {
    // Get old data before updating
    $oldData = $db->getRow("SELECT * FROM riders WHERE id = ?", [$riderId]);
    trackImportRecord($db, $importId, 'rider', $riderId, 'updated', $oldData);
}
```

### 2. Viewing Import History

Navigate to: **Admin → Import History**

URL: `/admin/import-history.php`

Features:
- Filter by import type (UCI, Riders, Results, Events, Clubs)
- View detailed statistics for each import
- See error summaries
- Access rollback functionality

### 3. Rolling Back an Import

1. Go to Import History page
2. Find the import you want to rollback
3. Click "Rollback" button
4. Confirm the action (WARNING: This cannot be undone!)

**What happens during rollback:**
- All records created during the import are **deleted**
- All records updated during the import are **restored** to their previous values
- Import status is marked as "rolled_back"

## Helper Functions

### startImportHistory()
Starts a new import session and returns an import ID.

### updateImportHistory()
Updates import history with final statistics and error summary.

### trackImportRecord()
Tracks an individual record that was created or updated.

### rollbackImport()
Performs a full rollback of an import, deleting/restoring all affected records.

### getImportHistory()
Retrieves import history records with optional filtering.

### getImportRecords()
Gets detailed records for a specific import.

## Best Practices

1. **Always use import history**: Integrate tracking into all import scripts
2. **Track old data for updates**: Store old record data before updating for accurate rollback
3. **Test rollback**: Verify rollback works correctly with test data before production use
4. **Limit error storage**: Only store first 100 errors to prevent excessive database growth
5. **Clean up old imports**: Consider archiving or deleting old import history periodically

## Files

- **Migration**: `/database/migrations/003_import_history.sql`
- **Helper Functions**: `/includes/import-history.php`
- **Admin UI**: `/admin/import-history.php`
- **Example Integration**: `/admin/import-uci.php`

## Security

- All import operations require admin authentication
- CSRF tokens protect rollback actions
- Only the original importer or other admins can rollback imports
- Rollback actions are logged with username and timestamp

## Limitations

- Rollback cannot undo cascading deletes from foreign key constraints
- JSON data storage for old records may have size limitations
- Rollback is all-or-nothing (cannot selectively undo specific records)
- Once rolled back, an import cannot be "re-applied" (would need to re-import)

## Future Enhancements

Potential improvements for the import history system:

1. **Partial Rollback**: Allow selective rollback of specific records
2. **Import Preview**: Show what would be imported before committing
3. **Scheduled Imports**: Automatic imports with history tracking
4. **Export History**: Download import logs as CSV/Excel
5. **Import Diff**: Compare two imports to see changes
6. **Audit Trail**: Extended logging of who viewed/modified what
