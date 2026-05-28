package chunk

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/google/uuid"
)

// Chunker defines the interface for episode chunking strategies
type Chunker interface {
	// Chunk creates episodes based on the strategy
	Chunk(ctx context.Context, db *sql.DB, definitionID string) (ChunkResult, error)
}

// ChunkResult tracks the outcome of a chunking operation
type ChunkResult struct {
	EpisodesCreated int
	EventsProcessed int
	Duration        time.Duration
}

// Event represents a minimal event for chunking
type Event struct {
	ID        string
	Timestamp int64
	ThreadID  string
	Channel   string
}

// TimeGapConfig defines configuration for time-gap chunking
type TimeGapConfig struct {
	GapSeconds int64  `json:"gap_seconds"` // Time gap in seconds
	Scope      string `json:"scope"`       // "thread" or "channel"
}

// TimeGapChunker implements time-gap based episode chunking
type TimeGapChunker struct {
	config TimeGapConfig
}

// NewTimeGapChunker creates a new time-gap chunker
func NewTimeGapChunker(config TimeGapConfig) *TimeGapChunker {
	return &TimeGapChunker{config: config}
}

// Chunk implements the Chunker interface for time-gap chunking
func (c *TimeGapChunker) Chunk(ctx context.Context, db *sql.DB, definitionID string) (ChunkResult, error) {
	startTime := time.Now()
	result := ChunkResult{}

	// Get definition details to determine scope
	var defName, channel string
	err := db.QueryRowContext(ctx, `
		SELECT name, channel FROM episode_definitions WHERE id = ?
	`, definitionID).Scan(&defName, &channel)
	if err != nil {
		return result, fmt.Errorf("failed to fetch definition: %w", err)
	}

	// Query events based on scope
	var query string
	var args []interface{}

	if c.config.Scope == "thread" {
		// Group by thread_id
		if channel != "" {
			query = `
				SELECT id, timestamp, thread_id, channel
				FROM events
				WHERE channel = ? AND thread_id IS NOT NULL
				ORDER BY thread_id, timestamp ASC
			`
			args = []interface{}{channel}
		} else {
			query = `
				SELECT id, timestamp, thread_id, channel
				FROM events
				WHERE thread_id IS NOT NULL
				ORDER BY thread_id, timestamp ASC
			`
		}
	} else {
		// Group by channel only
		if channel != "" {
			query = `
				SELECT id, timestamp, thread_id, channel
				FROM events
				WHERE channel = ?
				ORDER BY timestamp ASC
			`
			args = []interface{}{channel}
		} else {
			query = `
				SELECT id, timestamp, thread_id, channel
				FROM events
				ORDER BY timestamp ASC
			`
		}
	}

	rows, err := db.QueryContext(ctx, query, args...)
	if err != nil {
		return result, fmt.Errorf("failed to query events: %w", err)
	}
	defer rows.Close()

	// Group events by thread (or globally if scope is channel)
	eventsByGroup := make(map[string][]Event)

	for rows.Next() {
		var e Event
		var threadID sql.NullString

		err := rows.Scan(&e.ID, &e.Timestamp, &threadID, &e.Channel)
		if err != nil {
			return result, fmt.Errorf("failed to scan event: %w", err)
		}

		if threadID.Valid {
			e.ThreadID = threadID.String
		}

		// Group key depends on scope
		groupKey := "global"
		if c.config.Scope == "thread" && e.ThreadID != "" {
			groupKey = e.ThreadID
		} else if c.config.Scope == "channel" {
			groupKey = e.Channel
		}

		eventsByGroup[groupKey] = append(eventsByGroup[groupKey], e)
		result.EventsProcessed++
	}

	if err := rows.Err(); err != nil {
		return result, fmt.Errorf("error iterating events: %w", err)
	}

	// Process each group and create episodes based on time gaps
	for groupKey, events := range eventsByGroup {
		if len(events) == 0 {
			continue
		}

		// Split events into episodes based on time gaps
		episodes := c.splitByTimeGap(events)

		// Insert episodes into database
		for _, ep := range episodes {
			err := c.insertEpisode(ctx, db, definitionID, groupKey, ep, channel)
			if err != nil {
				return result, fmt.Errorf("failed to insert episode: %w", err)
			}
			result.EpisodesCreated++
		}
	}

	result.Duration = time.Since(startTime)
	return result, nil
}

// episode represents a chunked group of events
type episode struct {
	events    []Event
	startTime int64
	endTime   int64
	threadID  string
	channel   string
}

// splitByTimeGap splits events into episodes based on time gaps
func (c *TimeGapChunker) splitByTimeGap(events []Event) []episode {
	if len(events) == 0 {
		return nil
	}

	episodes := []episode{}
	currentEp := episode{
		events:    []Event{events[0]},
		startTime: events[0].Timestamp,
		endTime:   events[0].Timestamp,
		threadID:  events[0].ThreadID,
		channel:   events[0].Channel,
	}

	for i := 1; i < len(events); i++ {
		timeSinceLastEvent := events[i].Timestamp - currentEp.endTime

		if timeSinceLastEvent > c.config.GapSeconds {
			// Gap exceeded, finalize current episode and start new one
			episodes = append(episodes, currentEp)
			currentEp = episode{
				events:    []Event{events[i]},
				startTime: events[i].Timestamp,
				endTime:   events[i].Timestamp,
				threadID:  events[i].ThreadID,
				channel:   events[i].Channel,
			}
		} else {
			// Continue current episode
			currentEp.events = append(currentEp.events, events[i])
			currentEp.endTime = events[i].Timestamp
		}
	}

	// Don't forget the last episode
	episodes = append(episodes, currentEp)
	return episodes
}

// insertEpisode inserts an episode and its event mappings
func (c *TimeGapChunker) insertEpisode(ctx context.Context, db *sql.DB, definitionID, groupKey string, ep episode, scopeChannel string) error {
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %w", err)
	}
	defer tx.Rollback()

	episodeID := uuid.New().String()
	now := time.Now().Unix()

	// Determine thread_id and channel values for the episode record
	var threadIDValue interface{} = nil
	if ep.threadID != "" && c.config.Scope == "thread" {
		threadIDValue = ep.threadID
	}

	var channelValue interface{} = nil
	if scopeChannel != "" {
		channelValue = scopeChannel
	} else if ep.channel != "" {
		channelValue = ep.channel
	}

	// Insert episode
	_, err = tx.ExecContext(ctx, `
		INSERT INTO episodes (
			id, definition_id, channel, thread_id,
			start_time, end_time, event_count,
			first_event_id, last_event_id, created_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`, episodeID, definitionID, channelValue, threadIDValue,
		ep.startTime, ep.endTime, len(ep.events),
		ep.events[0].ID, ep.events[len(ep.events)-1].ID, now)

	if err != nil {
		return fmt.Errorf("failed to insert episode: %w", err)
	}

	// Insert episode_events mappings
	for position, event := range ep.events {
		_, err = tx.ExecContext(ctx, `
			INSERT INTO episode_events (episode_id, event_id, position)
			VALUES (?, ?, ?)
		`, episodeID, event.ID, position+1) // position is 1-indexed

		if err != nil {
			return fmt.Errorf("failed to insert episode_event mapping: %w", err)
		}
	}

	return tx.Commit()
}

// CreateDefinition creates an episode definition in the database
func CreateDefinition(ctx context.Context, db *sql.DB, name, channel, strategy string, config interface{}, description string) (string, error) {
	// Check if definition already exists
	var existingID string
	err := db.QueryRowContext(ctx, "SELECT id FROM episode_definitions WHERE name = ?", name).Scan(&existingID)
	if err == nil {
		// Definition already exists
		return existingID, nil
	}
	if err != sql.ErrNoRows {
		return "", fmt.Errorf("failed to check for existing definition: %w", err)
	}

	configJSON, err := json.Marshal(config)
	if err != nil {
		return "", fmt.Errorf("failed to marshal config: %w", err)
	}

	definitionID := uuid.New().String()
	now := time.Now().Unix()

	var channelValue interface{} = nil
	if channel != "" {
		channelValue = channel
	}

	_, err = db.ExecContext(ctx, `
		INSERT INTO episode_definitions (
			id, name, channel, strategy, config_json, description, created_at, updated_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
	`, definitionID, name, channelValue, strategy, string(configJSON), description, now, now)

	if err != nil {
		return "", fmt.Errorf("failed to insert definition: %w", err)
	}

	return definitionID, nil
}

// ThreadConfig defines configuration for thread-based chunking
type ThreadConfig struct {
	// No additional config needed - one episode per thread_id
}

// ThreadChunker implements thread-based episode chunking
// Each unique thread_id becomes one episode
type ThreadChunker struct {
	config ThreadConfig
}

// NewThreadChunker creates a new thread-based chunker
func NewThreadChunker(config ThreadConfig) *ThreadChunker {
	return &ThreadChunker{config: config}
}

// Chunk implements the Chunker interface for thread-based chunking
func (c *ThreadChunker) Chunk(ctx context.Context, db *sql.DB, definitionID string) (ChunkResult, error) {
	startTime := time.Now()
	result := ChunkResult{}

	// Get definition details
	var defName, channel string
	err := db.QueryRowContext(ctx, `
		SELECT name, channel FROM episode_definitions WHERE id = ?
	`, definitionID).Scan(&defName, &channel)
	if err != nil {
		return result, fmt.Errorf("failed to fetch definition: %w", err)
	}

	// Query events based on channel scope
	var query string
	var args []interface{}

	if channel != "" {
		query = `
			SELECT id, timestamp, thread_id, channel
			FROM events
			WHERE channel = ? AND thread_id IS NOT NULL
			ORDER BY thread_id, timestamp ASC
		`
		args = []interface{}{channel}
	} else {
		query = `
			SELECT id, timestamp, thread_id, channel
			FROM events
			WHERE thread_id IS NOT NULL
			ORDER BY thread_id, timestamp ASC
		`
	}

	rows, err := db.QueryContext(ctx, query, args...)
	if err != nil {
		return result, fmt.Errorf("failed to query events: %w", err)
	}
	defer rows.Close()

	// Group events by thread_id
	eventsByThread := make(map[string][]Event)

	for rows.Next() {
		var e Event
		var threadID sql.NullString

		err := rows.Scan(&e.ID, &e.Timestamp, &threadID, &e.Channel)
		if err != nil {
			return result, fmt.Errorf("failed to scan event: %w", err)
		}

		if threadID.Valid {
			e.ThreadID = threadID.String
		}

		if e.ThreadID != "" {
			eventsByThread[e.ThreadID] = append(eventsByThread[e.ThreadID], e)
			result.EventsProcessed++
		}
	}

	if err := rows.Err(); err != nil {
		return result, fmt.Errorf("error iterating events: %w", err)
	}

	// Create one episode per thread
	existingThreads := make(map[string]struct{})
	existingRows, err := db.QueryContext(ctx, `
		SELECT thread_id FROM episodes
		WHERE definition_id = ? AND thread_id IS NOT NULL
	`, definitionID)
	if err != nil {
		return result, fmt.Errorf("failed to query existing episodes: %w", err)
	}
	for existingRows.Next() {
		var tid sql.NullString
		if err := existingRows.Scan(&tid); err != nil {
			existingRows.Close()
			return result, fmt.Errorf("failed to scan existing episode: %w", err)
		}
		if tid.Valid && tid.String != "" {
			existingThreads[tid.String] = struct{}{}
		}
	}
	if err := existingRows.Err(); err != nil {
		existingRows.Close()
		return result, fmt.Errorf("error iterating existing episodes: %w", err)
	}
	existingRows.Close()

	for threadID, events := range eventsByThread {
		if len(events) == 0 {
			continue
		}
		if _, ok := existingThreads[threadID]; ok {
			continue
		}

		ep := episode{
			events:    events,
			startTime: events[0].Timestamp,
			endTime:   events[len(events)-1].Timestamp,
			threadID:  threadID,
			channel:   events[0].Channel,
		}

		err := c.insertEpisode(ctx, db, definitionID, threadID, ep, channel)
		if err != nil {
			return result, fmt.Errorf("failed to insert episode: %w", err)
		}
		result.EpisodesCreated++
	}

	result.Duration = time.Since(startTime)
	return result, nil
}

// insertEpisode inserts an episode and its event mappings
func (c *ThreadChunker) insertEpisode(ctx context.Context, db *sql.DB, definitionID, threadID string, ep episode, scopeChannel string) error {
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %w", err)
	}
	defer tx.Rollback()

	episodeID := uuid.New().String()
	now := time.Now().Unix()

	// Thread-based chunking always has a thread_id
	var channelValue interface{} = nil
	if scopeChannel != "" {
		channelValue = scopeChannel
	} else if ep.channel != "" {
		channelValue = ep.channel
	}

	// Insert episode
	_, err = tx.ExecContext(ctx, `
		INSERT INTO episodes (
			id, definition_id, channel, thread_id,
			start_time, end_time, event_count,
			first_event_id, last_event_id, created_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`, episodeID, definitionID, channelValue, threadID,
		ep.startTime, ep.endTime, len(ep.events),
		ep.events[0].ID, ep.events[len(ep.events)-1].ID, now)

	if err != nil {
		return fmt.Errorf("failed to insert episode: %w", err)
	}

	// Insert episode_events mappings
	for position, event := range ep.events {
		_, err = tx.ExecContext(ctx, `
			INSERT INTO episode_events (episode_id, event_id, position)
			VALUES (?, ?, ?)
		`, episodeID, event.ID, position+1) // position is 1-indexed

		if err != nil {
			return fmt.Errorf("failed to insert episode_event mapping: %w", err)
		}
	}

	return tx.Commit()
}

// SingleEventConfig defines configuration for single-event chunking
type SingleEventConfig struct {
	SourceAdapter string `json:"source_adapter,omitempty"`
}

// SingleEventChunker implements single-event episode chunking
// Each event becomes its own episode.
type SingleEventChunker struct {
	config SingleEventConfig
}

// NewSingleEventChunker creates a new single-event chunker
func NewSingleEventChunker(config SingleEventConfig) *SingleEventChunker {
	return &SingleEventChunker{config: config}
}

// Chunk implements the Chunker interface for single-event chunking
func (c *SingleEventChunker) Chunk(ctx context.Context, db *sql.DB, definitionID string) (ChunkResult, error) {
	startTime := time.Now()
	result := ChunkResult{}

	// Get definition details
	var channel string
	err := db.QueryRowContext(ctx, `
		SELECT channel FROM episode_definitions WHERE id = ?
	`, definitionID).Scan(&channel)
	if err != nil {
		return result, fmt.Errorf("failed to fetch definition: %w", err)
	}

	existing, err := loadExistingEventIDs(ctx, db, definitionID)
	if err != nil {
		return result, fmt.Errorf("failed to load existing episodes: %w", err)
	}

	query := `
		SELECT id, timestamp, thread_id, channel
		FROM events
	`
	args := []interface{}{}
	clauses := []string{}
	if channel != "" {
		clauses = append(clauses, "channel = ?")
		args = append(args, channel)
	}
	if c.config.SourceAdapter != "" {
		clauses = append(clauses, "source_adapter = ?")
		args = append(args, c.config.SourceAdapter)
	}
	if len(clauses) > 0 {
		query += " WHERE " + strings.Join(clauses, " AND ")
	}
	query += " ORDER BY timestamp ASC"

	rows, err := db.QueryContext(ctx, query, args...)
	if err != nil {
		return result, fmt.Errorf("failed to query events: %w", err)
	}
	defer rows.Close()

	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return result, fmt.Errorf("failed to begin transaction: %w", err)
	}
	defer tx.Rollback()

	stmtInsertEpisode, err := tx.PrepareContext(ctx, `
		INSERT INTO episodes (
			id, definition_id, channel, thread_id,
			start_time, end_time, event_count,
			first_event_id, last_event_id, created_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`)
	if err != nil {
		return result, fmt.Errorf("prepare insert episode: %w", err)
	}
	defer stmtInsertEpisode.Close()

	stmtInsertEvent, err := tx.PrepareContext(ctx, `
		INSERT INTO episode_events (episode_id, event_id, position)
		VALUES (?, ?, ?)
	`)
	if err != nil {
		return result, fmt.Errorf("prepare insert episode_event: %w", err)
	}
	defer stmtInsertEvent.Close()

	now := time.Now().Unix()
	for rows.Next() {
		var e Event
		var threadID sql.NullString
		if err := rows.Scan(&e.ID, &e.Timestamp, &threadID, &e.Channel); err != nil {
			return result, fmt.Errorf("failed to scan event: %w", err)
		}
		if _, ok := existing[e.ID]; ok {
			continue
		}
		if threadID.Valid {
			e.ThreadID = threadID.String
		}

		episodeID := uuid.New().String()
		var threadIDValue interface{} = nil
		if e.ThreadID != "" {
			threadIDValue = e.ThreadID
		}
		var channelValue interface{} = nil
		if channel != "" {
			channelValue = channel
		} else if e.Channel != "" {
			channelValue = e.Channel
		}

		if _, err := stmtInsertEpisode.Exec(
			episodeID,
			definitionID,
			channelValue,
			threadIDValue,
			e.Timestamp,
			e.Timestamp,
			1,
			e.ID,
			e.ID,
			now,
		); err != nil {
			return result, fmt.Errorf("insert episode: %w", err)
		}

		if _, err := stmtInsertEvent.Exec(episodeID, e.ID, 1); err != nil {
			return result, fmt.Errorf("insert episode_event: %w", err)
		}

		existing[e.ID] = struct{}{}
		result.EpisodesCreated++
		result.EventsProcessed++
	}
	if err := rows.Err(); err != nil {
		return result, fmt.Errorf("error iterating events: %w", err)
	}

	if err := tx.Commit(); err != nil {
		return result, fmt.Errorf("commit episodes: %w", err)
	}

	result.Duration = time.Since(startTime)
	return result, nil
}

// TurnPairConfig defines configuration for turn-pair chunking
type TurnPairConfig struct {
	IncludeTools bool `json:"include_tools"`
}

// TurnPairChunker groups a user message with following assistant responses.
type TurnPairChunker struct {
	config TurnPairConfig
}

// NewTurnPairChunker creates a new turn-pair chunker.
func NewTurnPairChunker(config TurnPairConfig) *TurnPairChunker {
	return &TurnPairChunker{config: config}
}

type turnEvent struct {
	ID           string
	Timestamp    int64
	ThreadID     string
	Channel      string
	Direction    string
	SourceAdapter string
}

// Chunk implements the Chunker interface for turn-pair chunking
func (c *TurnPairChunker) Chunk(ctx context.Context, db *sql.DB, definitionID string) (ChunkResult, error) {
	startTime := time.Now()
	result := ChunkResult{}

	var channel string
	err := db.QueryRowContext(ctx, `
		SELECT channel FROM episode_definitions WHERE id = ?
	`, definitionID).Scan(&channel)
	if err != nil {
		return result, fmt.Errorf("failed to fetch definition: %w", err)
	}

	existing, err := loadExistingEventIDs(ctx, db, definitionID)
	if err != nil {
		return result, fmt.Errorf("failed to load existing episodes: %w", err)
	}

	query := `
		SELECT id, timestamp, thread_id, channel, direction, source_adapter
		FROM events
		WHERE thread_id IS NOT NULL
	`
	args := []interface{}{}
	if channel != "" {
		query += " AND channel = ?"
		args = append(args, channel)
	}
	query += " ORDER BY thread_id, timestamp ASC"

	rows, err := db.QueryContext(ctx, query, args...)
	if err != nil {
		return result, fmt.Errorf("failed to query events: %w", err)
	}
	defer rows.Close()

	eventsByThread := make(map[string][]turnEvent)
	for rows.Next() {
		var ev turnEvent
		var threadID sql.NullString
		if err := rows.Scan(&ev.ID, &ev.Timestamp, &threadID, &ev.Channel, &ev.Direction, &ev.SourceAdapter); err != nil {
			return result, fmt.Errorf("failed to scan event: %w", err)
		}
		if !threadID.Valid || threadID.String == "" {
			continue
		}
		ev.ThreadID = threadID.String
		eventsByThread[ev.ThreadID] = append(eventsByThread[ev.ThreadID], ev)
		result.EventsProcessed++
	}
	if err := rows.Err(); err != nil {
		return result, fmt.Errorf("error iterating events: %w", err)
	}

	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return result, fmt.Errorf("failed to begin transaction: %w", err)
	}
	defer tx.Rollback()

	stmtInsertEpisode, err := tx.PrepareContext(ctx, `
		INSERT INTO episodes (
			id, definition_id, channel, thread_id,
			start_time, end_time, event_count,
			first_event_id, last_event_id, created_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`)
	if err != nil {
		return result, fmt.Errorf("prepare insert episode: %w", err)
	}
	defer stmtInsertEpisode.Close()

	stmtInsertEvent, err := tx.PrepareContext(ctx, `
		INSERT INTO episode_events (episode_id, event_id, position)
		VALUES (?, ?, ?)
	`)
	if err != nil {
		return result, fmt.Errorf("prepare insert episode_event: %w", err)
	}
	defer stmtInsertEvent.Close()

	now := time.Now().Unix()
	for threadID, events := range eventsByThread {
		if len(events) == 0 {
			continue
		}

		var current []turnEvent
		flush := func() error {
			if len(current) == 0 {
				return nil
			}
			first := current[0]
			if _, ok := existing[first.ID]; ok {
				current = nil
				return nil
			}

			episodeID := uuid.New().String()
			channelValue := interface{}(first.Channel)
			if channel != "" {
				channelValue = channel
			}

			if _, err := stmtInsertEpisode.Exec(
				episodeID,
				definitionID,
				channelValue,
				threadID,
				current[0].Timestamp,
				current[len(current)-1].Timestamp,
				len(current),
				current[0].ID,
				current[len(current)-1].ID,
				now,
			); err != nil {
				return fmt.Errorf("insert episode: %w", err)
			}

			for idx, ev := range current {
				if _, err := stmtInsertEvent.Exec(episodeID, ev.ID, idx+1); err != nil {
					return fmt.Errorf("insert episode_event: %w", err)
				}
				existing[ev.ID] = struct{}{}
			}

			result.EpisodesCreated++
			current = nil
			return nil
		}

		for _, ev := range events {
			switch ev.Direction {
			case "sent":
				if err := flush(); err != nil {
					return result, err
				}
				current = []turnEvent{ev}
			case "received":
				if len(current) == 0 {
					continue
				}
				current = append(current, ev)
			default:
				if !c.config.IncludeTools {
					continue
				}
				if len(current) == 0 {
					continue
				}
				current = append(current, ev)
			}
		}

		if err := flush(); err != nil {
			return result, err
		}
	}

	if err := tx.Commit(); err != nil {
		return result, fmt.Errorf("commit episodes: %w", err)
	}

	result.Duration = time.Since(startTime)
	return result, nil
}

// GetChunkerForDefinition creates a chunker instance for a given definition
func GetChunkerForDefinition(ctx context.Context, db *sql.DB, definitionID string) (Chunker, error) {
	var strategy, configJSON string
	err := db.QueryRowContext(ctx, `
		SELECT strategy, config_json FROM episode_definitions WHERE id = ?
	`, definitionID).Scan(&strategy, &configJSON)

	if err != nil {
		return nil, fmt.Errorf("failed to fetch definition: %w", err)
	}

	switch strategy {
	case "time_gap":
		var config TimeGapConfig
		if err := json.Unmarshal([]byte(configJSON), &config); err != nil {
			return nil, fmt.Errorf("failed to unmarshal time_gap config: %w", err)
		}
		return NewTimeGapChunker(config), nil
	case "thread":
		var config ThreadConfig
		if err := json.Unmarshal([]byte(configJSON), &config); err != nil {
			return nil, fmt.Errorf("failed to unmarshal thread config: %w", err)
		}
		return NewThreadChunker(config), nil
	case "single_event":
		var config SingleEventConfig
		if err := json.Unmarshal([]byte(configJSON), &config); err != nil {
			return nil, fmt.Errorf("failed to unmarshal single_event config: %w", err)
		}
		return NewSingleEventChunker(config), nil
	case "turn_pair":
		var config TurnPairConfig
		if err := json.Unmarshal([]byte(configJSON), &config); err != nil {
			return nil, fmt.Errorf("failed to unmarshal turn_pair config: %w", err)
		}
		return NewTurnPairChunker(config), nil
	default:
		return nil, fmt.Errorf("unsupported strategy: %s", strategy)
	}
}

func loadExistingEventIDs(ctx context.Context, db *sql.DB, definitionID string) (map[string]struct{}, error) {
	rows, err := db.QueryContext(ctx, `
		SELECT ee.event_id
		FROM episode_events ee
		JOIN episodes e ON ee.episode_id = e.id
		WHERE e.definition_id = ?
	`, definitionID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	existing := make(map[string]struct{})
	for rows.Next() {
		var eventID string
		if err := rows.Scan(&eventID); err != nil {
			return nil, err
		}
		existing[eventID] = struct{}{}
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return existing, nil
}

// ListDefinitions lists all episode definitions
func ListDefinitions(ctx context.Context, db *sql.DB) ([]Definition, error) {
	rows, err := db.QueryContext(ctx, `
		SELECT id, name, channel, strategy, config_json, description, created_at, updated_at
		FROM episode_definitions
		ORDER BY name
	`)
	if err != nil {
		return nil, fmt.Errorf("failed to query definitions: %w", err)
	}
	defer rows.Close()

	definitions := []Definition{}
	for rows.Next() {
		var d Definition
		var channel sql.NullString

		err := rows.Scan(&d.ID, &d.Name, &channel, &d.Strategy, &d.ConfigJSON, &d.Description, &d.CreatedAt, &d.UpdatedAt)
		if err != nil {
			return nil, fmt.Errorf("failed to scan definition: %w", err)
		}

		if channel.Valid {
			d.Channel = channel.String
		}

		definitions = append(definitions, d)
	}

	return definitions, rows.Err()
}

// Definition represents an episode definition
type Definition struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	Channel     string `json:"channel,omitempty"`
	Strategy    string `json:"strategy"`
	ConfigJSON  string `json:"config_json"`
	Description string `json:"description,omitempty"`
	CreatedAt   int64  `json:"created_at"`
	UpdatedAt   int64  `json:"updated_at"`
}
