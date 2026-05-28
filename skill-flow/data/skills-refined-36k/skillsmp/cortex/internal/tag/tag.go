package tag

import (
	"database/sql"
	"fmt"
	"time"

	"github.com/google/uuid"
)

// Tag represents a tag on an event
type Tag struct {
	ID         string
	EventID    string
	TagType    string
	Value      string
	Confidence *float64
	Source     string
	CreatedAt  time.Time
}

// TagWithEvent includes event details for display
type TagWithEvent struct {
	Tag
	EventTimestamp int64
	EventChannel   string
	EventContent   string
}

// ListAll returns all tags in the database
func ListAll(db *sql.DB) ([]TagWithEvent, error) {
	query := `
		SELECT
			t.id, t.event_id, t.tag_type, t.value, t.confidence, t.source, t.created_at,
			e.timestamp, e.channel, e.content
		FROM tags t
		JOIN events e ON t.event_id = e.id
		ORDER BY t.created_at DESC
	`

	rows, err := db.Query(query)
	if err != nil {
		return nil, fmt.Errorf("query tags: %w", err)
	}
	defer rows.Close()

	var tags []TagWithEvent
	for rows.Next() {
		var t TagWithEvent
		var confidence sql.NullFloat64

		err := rows.Scan(
			&t.ID, &t.EventID, &t.TagType, &t.Value, &confidence, &t.Source, &t.CreatedAt,
			&t.EventTimestamp, &t.EventChannel, &t.EventContent,
		)
		if err != nil {
			return nil, fmt.Errorf("scan tag: %w", err)
		}

		if confidence.Valid {
			t.Confidence = &confidence.Float64
		}

		tags = append(tags, t)
	}

	return tags, nil
}

// ListByEvent returns all tags for a specific event
func ListByEvent(db *sql.DB, eventID string) ([]Tag, error) {
	query := `
		SELECT id, event_id, tag_type, value, confidence, source, created_at
		FROM tags
		WHERE event_id = ?
		ORDER BY created_at DESC
	`

	rows, err := db.Query(query, eventID)
	if err != nil {
		return nil, fmt.Errorf("query tags: %w", err)
	}
	defer rows.Close()

	var tags []Tag
	for rows.Next() {
		var t Tag
		var confidence sql.NullFloat64

		err := rows.Scan(&t.ID, &t.EventID, &t.TagType, &t.Value, &confidence, &t.Source, &t.CreatedAt)
		if err != nil {
			return nil, fmt.Errorf("scan tag: %w", err)
		}

		if confidence.Valid {
			t.Confidence = &confidence.Float64
		}

		tags = append(tags, t)
	}

	return tags, nil
}

// ListByType returns all tags of a specific type
func ListByType(db *sql.DB, tagType string) ([]TagWithEvent, error) {
	query := `
		SELECT
			t.id, t.event_id, t.tag_type, t.value, t.confidence, t.source, t.created_at,
			e.timestamp, e.channel, e.content
		FROM tags t
		JOIN events e ON t.event_id = e.id
		WHERE t.tag_type = ?
		ORDER BY t.created_at DESC
	`

	rows, err := db.Query(query, tagType)
	if err != nil {
		return nil, fmt.Errorf("query tags: %w", err)
	}
	defer rows.Close()

	var tags []TagWithEvent
	for rows.Next() {
		var t TagWithEvent
		var confidence sql.NullFloat64

		err := rows.Scan(
			&t.ID, &t.EventID, &t.TagType, &t.Value, &confidence, &t.Source, &t.CreatedAt,
			&t.EventTimestamp, &t.EventChannel, &t.EventContent,
		)
		if err != nil {
			return nil, fmt.Errorf("scan tag: %w", err)
		}

		if confidence.Valid {
			t.Confidence = &confidence.Float64
		}

		tags = append(tags, t)
	}

	return tags, nil
}

// Add adds a tag to an event
func Add(db *sql.DB, eventID string, tagType string, value string, confidence *float64, source string) error {
	// Validate tag type
	validTypes := map[string]bool{
		"topic":   true,
		"entity":  true,
		"emotion": true,
		"project": true,
		"context": true,
	}

	if !validTypes[tagType] {
		return fmt.Errorf("invalid tag type '%s'. Must be one of: topic, entity, emotion, project, context", tagType)
	}

	// Check if event exists
	var exists bool
	err := db.QueryRow("SELECT EXISTS(SELECT 1 FROM events WHERE id = ?)", eventID).Scan(&exists)
	if err != nil {
		return fmt.Errorf("check event exists: %w", err)
	}
	if !exists {
		return fmt.Errorf("event '%s' not found", eventID)
	}

	// Check for duplicate tag
	var dupExists bool
	err = db.QueryRow(
		"SELECT EXISTS(SELECT 1 FROM tags WHERE event_id = ? AND tag_type = ? AND value = ?)",
		eventID, tagType, value,
	).Scan(&dupExists)
	if err != nil {
		return fmt.Errorf("check duplicate tag: %w", err)
	}
	if dupExists {
		return fmt.Errorf("tag '%s:%s' already exists on event '%s'", tagType, value, eventID)
	}

	// Insert tag
	tagID := uuid.New().String()
	createdAt := time.Now().Unix()

	query := `
		INSERT INTO tags (id, event_id, tag_type, value, confidence, source, created_at)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	`

	_, err = db.Exec(query, tagID, eventID, tagType, value, confidence, source, createdAt)
	if err != nil {
		return fmt.Errorf("insert tag: %w", err)
	}

	return nil
}

// AddBulk adds a tag to multiple events matching the filter
// Returns the number of events tagged
func AddBulk(db *sql.DB, filter EventFilter, tagType string, value string, confidence *float64, source string) (int, error) {
	// Validate tag type
	validTypes := map[string]bool{
		"topic":   true,
		"entity":  true,
		"emotion": true,
		"project": true,
		"context": true,
	}

	if !validTypes[tagType] {
		return 0, fmt.Errorf("invalid tag type '%s'. Must be one of: topic, entity, emotion, project, context", tagType)
	}

	// Build query to find matching events
	query, args := buildEventFilterQuery(filter)

	rows, err := db.Query(query, args...)
	if err != nil {
		return 0, fmt.Errorf("query events: %w", err)
	}
	defer rows.Close()

	// Collect event IDs
	var eventIDs []string
	for rows.Next() {
		var eventID string
		if err := rows.Scan(&eventID); err != nil {
			return 0, fmt.Errorf("scan event ID: %w", err)
		}
		eventIDs = append(eventIDs, eventID)
	}

	if len(eventIDs) == 0 {
		return 0, fmt.Errorf("no events match the specified filter")
	}

	// Add tag to each event (skip duplicates)
	tagged := 0
	for _, eventID := range eventIDs {
		// Check for duplicate tag
		var dupExists bool
		err = db.QueryRow(
			"SELECT EXISTS(SELECT 1 FROM tags WHERE event_id = ? AND tag_type = ? AND value = ?)",
			eventID, tagType, value,
		).Scan(&dupExists)
		if err != nil {
			return tagged, fmt.Errorf("check duplicate tag: %w", err)
		}
		if dupExists {
			continue // Skip duplicate
		}

		// Insert tag
		tagID := uuid.New().String()
		createdAt := time.Now().Unix()

		insertQuery := `
			INSERT INTO tags (id, event_id, tag_type, value, confidence, source, created_at)
			VALUES (?, ?, ?, ?, ?, ?, ?)
		`

		_, err = db.Exec(insertQuery, tagID, eventID, tagType, value, confidence, source, createdAt)
		if err != nil {
			return tagged, fmt.Errorf("insert tag: %w", err)
		}

		tagged++
	}

	return tagged, nil
}

// EventFilter defines filters for bulk tagging
type EventFilter struct {
	PersonName string
	Channel    string
	Since      *time.Time
	Until      *time.Time
}

// buildEventFilterQuery builds a SQL query to find events matching the filter
func buildEventFilterQuery(filter EventFilter) (string, []interface{}) {
	query := "SELECT DISTINCT e.id FROM events e"
	var args []interface{}
	var conditions []string

	// Join with event_participants if filtering by person
	if filter.PersonName != "" {
		query += `
			JOIN event_participants ep ON e.id = ep.event_id
			JOIN persons p ON ep.person_id = p.id
		`
		conditions = append(conditions, "(p.canonical_name LIKE ? OR p.display_name LIKE ?)")
		searchTerm := "%" + filter.PersonName + "%"
		args = append(args, searchTerm, searchTerm)
	}

	// Channel filter
	if filter.Channel != "" {
		conditions = append(conditions, "e.channel = ?")
		args = append(args, filter.Channel)
	}

	// Time range filters
	if filter.Since != nil {
		conditions = append(conditions, "e.timestamp >= ?")
		args = append(args, filter.Since.Unix())
	}

	if filter.Until != nil {
		conditions = append(conditions, "e.timestamp <= ?")
		args = append(args, filter.Until.Unix())
	}

	// Add WHERE clause if we have conditions
	if len(conditions) > 0 {
		query += " WHERE " + conditions[0]
		for i := 1; i < len(conditions); i++ {
			query += " AND " + conditions[i]
		}
	}

	return query, args
}

// Delete removes a tag from an event
func Delete(db *sql.DB, tagID string) error {
	result, err := db.Exec("DELETE FROM tags WHERE id = ?", tagID)
	if err != nil {
		return fmt.Errorf("delete tag: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("check rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return fmt.Errorf("tag '%s' not found", tagID)
	}

	return nil
}
