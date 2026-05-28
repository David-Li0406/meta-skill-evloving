package query

import (
	"database/sql"
	"fmt"
	"strings"
	"time"
)

// EventFilters holds all possible filters for querying events
type EventFilters struct {
	PersonName string    // Filter by person name (canonical or display)
	Channel    string    // Filter by channel
	Since      time.Time // Filter by start date
	Until      time.Time // Filter by end date
	Direction  string    // Filter by direction (sent, received, observed)
	Limit      int       // Limit number of results (default 100)
}

// Event represents a communication event with participant info
type Event struct {
	ID           string
	Timestamp    int64
	Channel      string
	ContentTypes string
	Content      string
	Direction    string
	ThreadID     *string
	ReplyTo      *string
	Participants []Participant
}

// Participant represents a person involved in an event
type Participant struct {
	PersonID string
	Name     string
	Role     string
}

// QueryEvents retrieves events matching the provided filters
func QueryEvents(db *sql.DB, filters EventFilters) ([]Event, error) {
	// Build query dynamically based on filters
	query := `
		SELECT DISTINCT
			e.id,
			e.timestamp,
			e.channel,
			e.content_types,
			e.content,
			e.direction,
			e.thread_id,
			e.reply_to
		FROM events e
	`

	var joins []string
	var conditions []string
	var args []interface{}
	argCount := 0

	// Join with event_participants if filtering by person
	if filters.PersonName != "" {
		joins = append(joins, `
			LEFT JOIN event_participants ep ON e.id = ep.event_id
			LEFT JOIN persons p ON ep.person_id = p.id
		`)
		conditions = append(conditions, "(LOWER(p.canonical_name) LIKE ? OR LOWER(p.display_name) LIKE ?)")
		searchTerm := "%" + strings.ToLower(filters.PersonName) + "%"
		args = append(args, searchTerm, searchTerm)
		argCount += 2
	}

	// Add joins to query
	if len(joins) > 0 {
		query += strings.Join(joins, " ")
	}

	// Build WHERE clause
	if filters.Channel != "" {
		conditions = append(conditions, "e.channel = ?")
		args = append(args, filters.Channel)
		argCount++
	}

	if !filters.Since.IsZero() {
		conditions = append(conditions, "e.timestamp >= ?")
		args = append(args, filters.Since.Unix())
		argCount++
	}

	if !filters.Until.IsZero() {
		conditions = append(conditions, "e.timestamp <= ?")
		args = append(args, filters.Until.Unix())
		argCount++
	}

	if filters.Direction != "" {
		conditions = append(conditions, "e.direction = ?")
		args = append(args, filters.Direction)
		argCount++
	}

	if len(conditions) > 0 {
		query += " WHERE " + strings.Join(conditions, " AND ")
	}

	// Order by timestamp descending (most recent first)
	query += " ORDER BY e.timestamp DESC"

	// Apply limit
	limit := filters.Limit
	if limit <= 0 {
		limit = 100 // Default limit
	}
	query += " LIMIT ?"
	args = append(args, limit)

	// Execute query
	rows, err := db.Query(query, args...)
	if err != nil {
		return nil, fmt.Errorf("failed to query events: %w", err)
	}
	defer rows.Close()

	var events []Event
	for rows.Next() {
		var e Event
		var threadID, replyTo sql.NullString

		err := rows.Scan(
			&e.ID,
			&e.Timestamp,
			&e.Channel,
			&e.ContentTypes,
			&e.Content,
			&e.Direction,
			&threadID,
			&replyTo,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan event: %w", err)
		}

		if threadID.Valid {
			e.ThreadID = &threadID.String
		}
		if replyTo.Valid {
			e.ReplyTo = &replyTo.String
		}

		events = append(events, e)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error iterating events: %w", err)
	}

	// Load participants for each event
	for i := range events {
		participants, err := getEventParticipants(db, events[i].ID)
		if err != nil {
			return nil, fmt.Errorf("failed to get participants for event %s: %w", events[i].ID, err)
		}
		events[i].Participants = participants
	}

	return events, nil
}

// getEventParticipants retrieves all participants for a given event
func getEventParticipants(db *sql.DB, eventID string) ([]Participant, error) {
	query := `
		SELECT
			ep.person_id,
			COALESCE(p.display_name, p.canonical_name) as name,
			ep.role
		FROM event_participants ep
		JOIN persons p ON ep.person_id = p.id
		WHERE ep.event_id = ?
		ORDER BY
			CASE ep.role
				WHEN 'sender' THEN 1
				WHEN 'recipient' THEN 2
				WHEN 'cc' THEN 3
				ELSE 4
			END
	`

	rows, err := db.Query(query, eventID)
	if err != nil {
		return nil, fmt.Errorf("failed to query participants: %w", err)
	}
	defer rows.Close()

	var participants []Participant
	for rows.Next() {
		var p Participant
		err := rows.Scan(&p.PersonID, &p.Name, &p.Role)
		if err != nil {
			return nil, fmt.Errorf("failed to scan participant: %w", err)
		}
		participants = append(participants, p)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error iterating participants: %w", err)
	}

	return participants, nil
}

// FormatTimestamp converts Unix timestamp to human-readable format
func FormatTimestamp(timestamp int64) string {
	t := time.Unix(timestamp, 0)
	return t.Format("2006-01-02 15:04:05")
}
