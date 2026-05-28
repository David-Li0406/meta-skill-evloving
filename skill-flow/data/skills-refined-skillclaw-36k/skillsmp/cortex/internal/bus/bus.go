package bus

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"time"

	"github.com/google/uuid"
)

type Event struct {
	Seq        int64   `json:"seq"`
	ID         string  `json:"id"`
	Type       string  `json:"type"`
	Adapter    *string `json:"adapter,omitempty"`
	CommsEvent *string `json:"cortex_event_id,omitempty"`
	CreatedAt  int64   `json:"created_at"`
	Payload    *string `json:"payload_json,omitempty"`
}

func ensureTable(db *sql.DB) error {
	_, err := db.Exec(`
		CREATE TABLE IF NOT EXISTS bus_events (
			seq INTEGER PRIMARY KEY AUTOINCREMENT,
			id TEXT NOT NULL UNIQUE,
			type TEXT NOT NULL,
			adapter TEXT,
			cortex_event_id TEXT,
			created_at INTEGER NOT NULL,
			payload_json TEXT
		)
	`)
	if err != nil {
		return fmt.Errorf("failed to ensure bus_events table: %w", err)
	}
	return nil
}

func Emit(db *sql.DB, typ string, adapter string, cortexEventID string, payload any) error {
	if typ == "" {
		return fmt.Errorf("type is required")
	}
	if err := ensureTable(db); err != nil {
		return err
	}
	now := time.Now().Unix()
	id := uuid.New().String()

	var adapterVal any
	if adapter != "" {
		adapterVal = adapter
	}
	var eventVal any
	if cortexEventID != "" {
		eventVal = cortexEventID
	}
	var payloadVal any
	if payload != nil {
		b, err := json.Marshal(payload)
		if err != nil {
			return fmt.Errorf("failed to marshal payload: %w", err)
		}
		payloadVal = string(b)
	}

	_, err := db.Exec(`
		INSERT INTO bus_events (id, type, adapter, cortex_event_id, created_at, payload_json)
		VALUES (?, ?, ?, ?, ?, ?)
	`, id, typ, adapterVal, eventVal, now, payloadVal)
	if err != nil {
		return fmt.Errorf("failed to insert bus event: %w", err)
	}
	return nil
}

func List(db *sql.DB, afterSeq int64, limit int) ([]Event, error) {
	if err := ensureTable(db); err != nil {
		return nil, err
	}
	if limit <= 0 {
		limit = 100
	}
	rows, err := db.Query(`
		SELECT seq, id, type, adapter, cortex_event_id, created_at, payload_json
		FROM bus_events
		WHERE seq > ?
		ORDER BY seq ASC
		LIMIT ?
	`, afterSeq, limit)
	if err != nil {
		return nil, fmt.Errorf("failed to query bus events: %w", err)
	}
	defer rows.Close()

	var out []Event
	for rows.Next() {
		var e Event
		var adapter sql.NullString
		var cortexEvent sql.NullString
		var payload sql.NullString
		if err := rows.Scan(&e.Seq, &e.ID, &e.Type, &adapter, &cortexEvent, &e.CreatedAt, &payload); err != nil {
			return nil, fmt.Errorf("failed to scan bus event: %w", err)
		}
		if adapter.Valid {
			e.Adapter = &adapter.String
		}
		if cortexEvent.Valid {
			e.CommsEvent = &cortexEvent.String
		}
		if payload.Valid {
			e.Payload = &payload.String
		}
		out = append(out, e)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("failed iterating bus events: %w", err)
	}
	return out, nil
}
