package sync

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"time"
)

type JobStatus struct {
	Adapter     string                 `json:"adapter"`
	Status      string                 `json:"status"`
	Phase       string                 `json:"phase"`
	Cursor      *string                `json:"cursor,omitempty"`
	StartedAt   *int64                 `json:"started_at,omitempty"`
	UpdatedAt   int64                  `json:"updated_at"`
	LastError   *string                `json:"last_error,omitempty"`
	Progress    map[string]interface{} `json:"progress,omitempty"`
	ProgressRaw *string                `json:"-"`
}

func ensureSyncJobsTable(db *sql.DB) error {
	// Keep this defensive: existing installs may not have re-run init/schema.
	_, err := db.Exec(`
		CREATE TABLE IF NOT EXISTS sync_jobs (
			adapter TEXT PRIMARY KEY,
			status TEXT NOT NULL,
			phase TEXT NOT NULL,
			cursor TEXT,
			started_at INTEGER,
			updated_at INTEGER NOT NULL,
			last_error TEXT,
			progress_json TEXT
		)
	`)
	if err != nil {
		return fmt.Errorf("failed to ensure sync_jobs table: %w", err)
	}
	return nil
}

func StartJob(db *sql.DB, adapter string) error {
	if err := ensureSyncJobsTable(db); err != nil {
		return err
	}
	now := time.Now().Unix()
	_, err := db.Exec(`
		INSERT INTO sync_jobs (adapter, status, phase, cursor, started_at, updated_at, last_error, progress_json)
		VALUES (?, 'running', 'sync', NULL, ?, ?, NULL, NULL)
		ON CONFLICT(adapter) DO UPDATE SET
			status = 'running',
			phase = 'sync',
			cursor = NULL,
			started_at = excluded.started_at,
			updated_at = excluded.updated_at,
			last_error = NULL
	`, adapter, now, now)
	if err != nil {
		return fmt.Errorf("failed to start job: %w", err)
	}
	return nil
}

func UpdateJob(db *sql.DB, adapter string, phase string, cursor *string, progress any) error {
	if err := ensureSyncJobsTable(db); err != nil {
		return err
	}
	now := time.Now().Unix()
	var progressJSON *string
	if progress != nil {
		b, err := json.Marshal(progress)
		if err != nil {
			return fmt.Errorf("failed to marshal progress json: %w", err)
		}
		s := string(b)
		progressJSON = &s
	}
	_, err := db.Exec(`
		INSERT INTO sync_jobs (adapter, status, phase, cursor, started_at, updated_at, last_error, progress_json)
		VALUES (?, 'running', ?, ?, NULL, ?, NULL, ?)
		ON CONFLICT(adapter) DO UPDATE SET
			status = 'running',
			phase = excluded.phase,
			cursor = excluded.cursor,
			updated_at = excluded.updated_at,
			last_error = NULL,
			progress_json = excluded.progress_json
	`, adapter, phase, cursor, now, progressJSON)
	if err != nil {
		return fmt.Errorf("failed to update job: %w", err)
	}
	return nil
}

func FinishJobSuccess(db *sql.DB, adapter string, phase string, cursor *string, progress any) error {
	if err := ensureSyncJobsTable(db); err != nil {
		return err
	}
	now := time.Now().Unix()
	var progressJSON *string
	if progress != nil {
		b, err := json.Marshal(progress)
		if err != nil {
			return fmt.Errorf("failed to marshal progress json: %w", err)
		}
		s := string(b)
		progressJSON = &s
	}
	_, err := db.Exec(`
		INSERT INTO sync_jobs (adapter, status, phase, cursor, started_at, updated_at, last_error, progress_json)
		VALUES (?, 'success', ?, ?, NULL, ?, NULL, ?)
		ON CONFLICT(adapter) DO UPDATE SET
			status = 'success',
			phase = excluded.phase,
			cursor = excluded.cursor,
			updated_at = excluded.updated_at,
			last_error = NULL,
			progress_json = excluded.progress_json
	`, adapter, phase, cursor, now, progressJSON)
	if err != nil {
		return fmt.Errorf("failed to finish job: %w", err)
	}
	return nil
}

func FinishJobError(db *sql.DB, adapter string, phase string, cursor *string, errMsg string, progress any) error {
	if err := ensureSyncJobsTable(db); err != nil {
		return err
	}
	now := time.Now().Unix()
	var progressJSON *string
	if progress != nil {
		b, err := json.Marshal(progress)
		if err != nil {
			return fmt.Errorf("failed to marshal progress json: %w", err)
		}
		s := string(b)
		progressJSON = &s
	}
	_, err := db.Exec(`
		INSERT INTO sync_jobs (adapter, status, phase, cursor, started_at, updated_at, last_error, progress_json)
		VALUES (?, 'error', ?, ?, NULL, ?, ?, ?)
		ON CONFLICT(adapter) DO UPDATE SET
			status = 'error',
			phase = excluded.phase,
			cursor = excluded.cursor,
			updated_at = excluded.updated_at,
			last_error = excluded.last_error,
			progress_json = excluded.progress_json
	`, adapter, phase, cursor, now, errMsg, progressJSON)
	if err != nil {
		return fmt.Errorf("failed to finish job with error: %w", err)
	}
	return nil
}

func ListJobs(db *sql.DB) ([]JobStatus, error) {
	if err := ensureSyncJobsTable(db); err != nil {
		return nil, err
	}
	rows, err := db.Query(`
		SELECT adapter, status, phase, cursor, started_at, updated_at, last_error, progress_json
		FROM sync_jobs
		ORDER BY updated_at DESC
	`)
	if err != nil {
		return nil, fmt.Errorf("failed to query jobs: %w", err)
	}
	defer rows.Close()

	var out []JobStatus
	for rows.Next() {
		var adapter, status, phase string
		var cursor sql.NullString
		var startedAt sql.NullInt64
		var updatedAt int64
		var lastErr sql.NullString
		var progressJSON sql.NullString
		if err := rows.Scan(&adapter, &status, &phase, &cursor, &startedAt, &updatedAt, &lastErr, &progressJSON); err != nil {
			return nil, fmt.Errorf("failed to scan job row: %w", err)
		}

		js := JobStatus{
			Adapter:   adapter,
			Status:    status,
			Phase:     phase,
			UpdatedAt: updatedAt,
		}
		if cursor.Valid {
			js.Cursor = &cursor.String
		}
		if startedAt.Valid {
			v := startedAt.Int64
			js.StartedAt = &v
		}
		if lastErr.Valid {
			js.LastError = &lastErr.String
		}
		if progressJSON.Valid && progressJSON.String != "" {
			raw := progressJSON.String
			js.ProgressRaw = &raw
			var m map[string]interface{}
			if err := json.Unmarshal([]byte(raw), &m); err == nil {
				js.Progress = m
			}
		}

		out = append(out, js)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed iterating job rows: %w", err)
	}
	return out, nil
}
