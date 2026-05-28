<?php
/**
 * Import History Helper Functions
 *
 * Functions for tracking imports and enabling rollback functionality
 */

/**
 * Start a new import session
 *
 * @param object $db Database connection
 * @param string $importType Type of import (riders, results, events, clubs, uci, other)
 * @param string $filename Original filename
 * @param int $fileSize File size in bytes
 * @param string $importedBy Username of who initiated the import
 * @return int Import ID
 */
function startImportHistory($db, $importType, $filename, $fileSize, $importedBy = 'admin') {
    $data = [
        'import_type' => $importType,
        'filename' => basename($filename),
        'file_size' => $fileSize,
        'status' => 'completed',
        'imported_by' => $importedBy
    ];

    return $db->insert('import_history', $data);
}

/**
 * Update import history with final statistics
 *
 * @param object $db Database connection
 * @param int $importId Import history ID
 * @param array $stats Statistics array with keys: total, success, updated, failed, skipped
 * @param array $errors Array of error messages
 * @param string $status Status (completed, failed)
 */
function updateImportHistory($db, $importId, $stats, $errors = [], $status = 'completed') {
    $errorSummary = null;
    if (!empty($errors)) {
        // Limit to first 100 errors
        $errorSummary = implode("\n", array_slice($errors, 0, 100));
        if (count($errors) > 100) {
            $errorSummary .= "\n... and " . (count($errors) - 100) . " more errors";
        }
    }

    $data = [
        'status' => $status,
        'total_records' => $stats['total'] ?? 0,
        'success_count' => $stats['success'] ?? 0,
        'updated_count' => $stats['updated'] ?? 0,
        'failed_count' => $stats['failed'] ?? 0,
        'skipped_count' => $stats['skipped'] ?? 0,
        'error_summary' => $errorSummary
    ];

    $db->update('import_history', $data, 'id = ?', [$importId]);
}

/**
 * Track a record that was created during import
 *
 * @param object $db Database connection
 * @param int $importId Import history ID
 * @param string $recordType Type of record (rider, result, event, club)
 * @param int $recordId ID of the created/updated record
 * @param string $action Action performed (created, updated)
 * @param array $oldData Old data before update (for rollback, optional)
 */
function trackImportRecord($db, $importId, $recordType, $recordId, $action = 'created', $oldData = null) {
    $data = [
        'import_id' => $importId,
        'record_type' => $recordType,
        'record_id' => $recordId,
        'action' => $action,
        'old_data' => $oldData ? json_encode($oldData) : null
    ];

    try {
        $db->insert('import_records', $data);
    } catch (Exception $e) {
        // Log error but don't fail the import
        error_log("Failed to track import record: " . $e->getMessage());
    }
}

/**
 * Rollback an import by deleting/restoring all affected records
 *
 * @param object $db Database connection
 * @param int $importId Import history ID
 * @param string $rolledBackBy Username of who initiated the rollback
 * @return array Result with success status and message
 */
function rollbackImport($db, $importId, $rolledBackBy = 'admin') {
    try {
        // Get import history
        $import = $db->getRow("SELECT * FROM import_history WHERE id = ?", [$importId]);

        if (!$import) {
            return ['success' => false, 'message' => 'Import hittades inte'];
        }

        // Get all records from this import
        $records = $db->getAll("SELECT * FROM import_records WHERE import_id = ? ORDER BY id DESC", [$importId]);

        if (empty($records)) {
            return ['success' => false, 'message' => 'Inga poster att återställa'];
        }

        $deletedCount = 0;
        $restoredCount = 0;
        $errors = [];

        // Process each record
        foreach ($records as $record) {
            try {
                if ($record['action'] === 'created') {
                    // Delete created records
                    $table = getTableName($record['record_type']);
                    $db->delete($table, 'id = ?', [$record['record_id']]);
                    $deletedCount++;
                } elseif ($record['action'] === 'updated' && $record['old_data']) {
                    // Restore old data
                    $table = getTableName($record['record_type']);
                    $oldData = json_decode($record['old_data'], true);
                    if ($oldData) {
                        unset($oldData['id']); // Don't update ID
                        $db->update($table, $oldData, 'id = ?', [$record['record_id']]);
                        $restoredCount++;
                    }
                }
            } catch (Exception $e) {
                $errors[] = "Record {$record['record_type']} #{$record['record_id']}: " . $e->getMessage();
            }
        }

        // Delete all import records
        $db->delete('import_records', 'import_id = ?', [$importId]);

        // Delete import history (remove from list completely)
        $db->delete('import_history', 'id = ?', [$importId]);

        $message = "Import återställd och raderad! $deletedCount poster raderade, $restoredCount återställda.";
        if (!empty($errors)) {
            $message .= " " . count($errors) . " fel uppstod.";
        }

        return [
            'success' => true,
            'message' => $message,
            'deleted' => $deletedCount,
            'restored' => $restoredCount,
            'errors' => $errors
        ];

    } catch (Exception $e) {
        return ['success' => false, 'message' => 'Rollback misslyckades: ' . $e->getMessage()];
    }
}

/**
 * Get table name from record type
 */
function getTableName($recordType) {
    $map = [
        'rider' => 'riders',
        'result' => 'results',
        'event' => 'events',
        'club' => 'clubs',
        'class' => 'classes'
    ];

    return $map[$recordType] ?? $recordType . 's';
}

/**
 * Get import history with statistics
 *
 * @param object $db Database connection
 * @param int $limit Number of records to return
 * @param string $type Filter by import type (optional)
 * @return array Array of import history records
 */
function getImportHistory($db, $limit = 50, $type = null) {
    $where = [];
    $params = [];

    if ($type) {
        $where[] = "import_type = ?";
        $params[] = $type;
    }

    $whereClause = $where ? 'WHERE ' . implode(' AND ', $where) : '';

    $sql = "SELECT
                ih.*,
                COUNT(DISTINCT ir.id) as records_count
            FROM import_history ih
            LEFT JOIN import_records ir ON ih.id = ir.import_id
            $whereClause
            GROUP BY ih.id
            ORDER BY ih.imported_at DESC
            LIMIT ?";

    $params[] = $limit;

    return $db->getAll($sql, $params);
}

/**
 * Get detailed records for a specific import
 *
 * @param object $db Database connection
 * @param int $importId Import history ID
 * @return array Array of import records
 */
function getImportRecords($db, $importId) {
    return $db->getAll("SELECT * FROM import_records WHERE import_id = ? ORDER BY id", [$importId]);
}

/**
 * Delete import history entry (without rollback)
 *
 * @param object $db Database connection
 * @param int $importId Import history ID
 * @return array Result with success status and message
 */
function deleteImportHistory($db, $importId) {
    try {
        // Get import history
        $import = $db->getRow("SELECT * FROM import_history WHERE id = ?", [$importId]);

        if (!$import) {
            return ['success' => false, 'message' => 'Import hittades inte'];
        }

        // Delete all import records first (foreign key)
        $db->delete('import_records', 'import_id = ?', [$importId]);

        // Delete import history
        $db->delete('import_history', 'id = ?', [$importId]);

        return [
            'success' => true,
            'message' => 'Importhistorik raderad'
        ];

    } catch (Exception $e) {
        return ['success' => false, 'message' => 'Radering misslyckades: ' . $e->getMessage()];
    }
}
