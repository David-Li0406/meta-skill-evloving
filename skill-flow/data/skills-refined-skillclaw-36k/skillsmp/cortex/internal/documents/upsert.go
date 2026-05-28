package documents

import (
	"context"
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"
)

const defaultSourceAdapter = "documents"

// UpsertDocument stores a document as an immutable event and updates document_heads.
// If the content hash hasn't changed, the upsert is skipped.
func UpsertDocument(ctx context.Context, db *sql.DB, input DocumentInput) (DocumentResult, error) {
	if db == nil {
		return DocumentResult{}, errors.New("documents: db is nil")
	}
	if input.DocKey == "" {
		return DocumentResult{}, errors.New("documents: docKey is required")
	}
	if input.Channel == "" {
		return DocumentResult{}, errors.New("documents: channel is required")
	}
	if input.Content == "" {
		return DocumentResult{}, errors.New("documents: content is required")
	}

	sourceAdapter := input.SourceAdapter
	if sourceAdapter == "" {
		sourceAdapter = defaultSourceAdapter
	}

	timestamp := input.Timestamp
	if timestamp == 0 {
		timestamp = time.Now().Unix()
	}

	contentHash := hashContent(input.Content)
	metadataJSON, err := marshalMetadata(input.Metadata)
	if err != nil {
		return DocumentResult{}, fmt.Errorf("documents: marshal metadata: %w", err)
	}

	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return DocumentResult{}, fmt.Errorf("documents: begin tx: %w", err)
	}
	defer tx.Rollback()

	var previousEventID sql.NullString
	var previousHash sql.NullString
	row := tx.QueryRowContext(ctx, `
		SELECT current_event_id, content_hash
		FROM document_heads
		WHERE doc_key = ?
	`, input.DocKey)
	if err := row.Scan(&previousEventID, &previousHash); err != nil && err != sql.ErrNoRows {
		return DocumentResult{}, fmt.Errorf("documents: query head: %w", err)
	}

	if previousHash.Valid && previousHash.String == contentHash {
		return DocumentResult{
			DocKey:      input.DocKey,
			ContentHash: contentHash,
			Skipped:     true,
			Reason:      "content unchanged",
		}, nil
	}

	eventID := uuid.NewString()
	direction := "created"
	if previousEventID.Valid {
		direction = "updated"
	}

	contentTypes, err := json.Marshal([]string{"document", input.Channel})
	if err != nil {
		return DocumentResult{}, fmt.Errorf("documents: marshal content types: %w", err)
	}

	sourceID := fmt.Sprintf("%s@%s", input.DocKey, contentHash)
	var replyTo any = nil
	if previousEventID.Valid {
		replyTo = previousEventID.String
	}

	_, err = tx.ExecContext(ctx, `
		INSERT INTO events (
			id, timestamp, channel, content_types, content,
			direction, thread_id, reply_to, source_adapter, source_id
		) VALUES (?, ?, ?, ?, ?, ?, NULL, ?, ?, ?)
	`, eventID, timestamp, input.Channel, string(contentTypes), input.Content, direction, replyTo, sourceAdapter, sourceID)
	if err != nil {
		return DocumentResult{}, fmt.Errorf("documents: insert event: %w", err)
	}

	_, err = tx.ExecContext(ctx, `
		INSERT INTO document_heads (
			doc_key, channel, current_event_id, content_hash,
			title, description, metadata_json, updated_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(doc_key) DO UPDATE SET
			channel = excluded.channel,
			current_event_id = excluded.current_event_id,
			content_hash = excluded.content_hash,
			title = excluded.title,
			description = excluded.description,
			metadata_json = excluded.metadata_json,
			updated_at = excluded.updated_at
	`, input.DocKey, input.Channel, eventID, contentHash, nullIfEmpty(input.Title), nullIfEmpty(input.Description), metadataJSON, timestamp)
	if err != nil {
		return DocumentResult{}, fmt.Errorf("documents: upsert head: %w", err)
	}

	if err := tx.Commit(); err != nil {
		return DocumentResult{}, fmt.Errorf("documents: commit: %w", err)
	}

	return DocumentResult{
		DocKey:          input.DocKey,
		EventID:         eventID,
		ContentHash:     contentHash,
		Created:         !previousEventID.Valid,
		Updated:         previousEventID.Valid,
		PreviousEventID: previousEventID.String,
	}, nil
}

func hashContent(content string) string {
	sum := sha256.Sum256([]byte(content))
	return hex.EncodeToString(sum[:])
}

func marshalMetadata(metadata map[string]any) (any, error) {
	if len(metadata) == 0 {
		return nil, nil
	}
	raw, err := json.Marshal(metadata)
	if err != nil {
		return nil, err
	}
	return string(raw), nil
}

func nullIfEmpty(value string) any {
	if value == "" {
		return nil
	}
	return value
}
