package adapters

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"time"

	"github.com/Napageneral/cortex/internal/chunk"
	"github.com/google/uuid"
)

// AIXFacetExtractor extracts facets from AIX event metadata
type AIXFacetExtractor struct {
	db *sql.DB
}

// NewAIXFacetExtractor creates a new facet extractor
func NewAIXFacetExtractor(db *sql.DB) *AIXFacetExtractor {
	return &AIXFacetExtractor{db: db}
}

// aixMetadataFull represents the full structure of AIX message metadata for facet extraction
type aixMetadataFull struct {
	Type             int                    `json:"type"`
	IsAgentic        bool                   `json:"isAgentic"`
	RelevantFiles    []string               `json:"relevantFiles"`
	Lints            []interface{}          `json:"lints"`
	CapabilitiesRan  map[string][]int       `json:"capabilitiesRan"`
	CapabilityStatuses map[string][]int     `json:"capabilityStatuses"`
	ToolFormerData   *aixToolFormerData     `json:"toolFormerData"`
	SupportedTools   []int                  `json:"supportedTools"`
	WebReferences    []interface{}          `json:"webReferences"`
	DocsReferences   []interface{}          `json:"docsReferences"`
	TokenCount       *aixTokenCountFull     `json:"tokenCount"`
	CursorRules      []interface{}          `json:"cursorRules"`
}

type aixTokenCountFull struct {
	InputTokens  int `json:"inputTokens"`
	OutputTokens int `json:"outputTokens"`
}

// ExtractResult contains the results of facet extraction
type ExtractResult struct {
	EventsProcessed int
	FacetsCreated   int
	EpisodesCreated int
	Duration        time.Duration
}

// ExtractFacetsFromMetadata extracts facets from events with metadata_json
func (e *AIXFacetExtractor) ExtractFacetsFromMetadata(ctx context.Context, channel string, since int64) (ExtractResult, error) {
	start := time.Now()
	result := ExtractResult{}

	// Get or create the aix_metadata analysis type
	analysisTypeID, err := e.ensureAnalysisType(ctx)
	if err != nil {
		return result, fmt.Errorf("ensure analysis type: %w", err)
	}

	// Get or create episode definition for single-event AIX episodes
	episodeDefID, err := e.ensureEpisodeDefinition(ctx)
	if err != nil {
		return result, fmt.Errorf("ensure episode definition: %w", err)
	}

	// Query events with metadata that haven't been processed yet
	query := `
		SELECT e.id, e.timestamp, e.channel, e.thread_id, e.metadata_json
		FROM events e
		WHERE e.metadata_json IS NOT NULL
		  AND e.channel = ?
		  AND e.timestamp > ?
		  AND NOT EXISTS (
		    SELECT 1 FROM episode_events ee
		    JOIN episodes ep ON ep.id = ee.episode_id
		    WHERE ee.event_id = e.id AND ep.definition_id = ?
		  )
		ORDER BY e.timestamp ASC
		LIMIT 500
	`

	rows, err := e.db.QueryContext(ctx, query, channel, since, episodeDefID)
	if err != nil {
		return result, fmt.Errorf("query events: %w", err)
	}
	defer rows.Close()

	// Collect all events first, then batch insert
	type eventData struct {
		eventID      string
		timestamp    int64
		eventChannel string
		threadID     sql.NullString
		metadataJSON string
		meta         aixMetadataFull
	}
	var events []eventData

	for rows.Next() {
		var ed eventData
		if err := rows.Scan(&ed.eventID, &ed.timestamp, &ed.eventChannel, &ed.threadID, &ed.metadataJSON); err != nil {
			continue
		}
		if err := json.Unmarshal([]byte(ed.metadataJSON), &ed.meta); err != nil {
			continue
		}
		if !hasExtractableFacets(ed.meta) {
			continue
		}
		events = append(events, ed)
	}

	if len(events) == 0 {
		result.Duration = time.Since(start)
		return result, nil
	}

	// Batch insert in a single transaction
	tx, err := e.db.BeginTx(ctx, nil)
	if err != nil {
		return result, fmt.Errorf("begin tx: %w", err)
	}
	defer tx.Rollback()

	now := time.Now().Unix()

	stmtEpisode, err := tx.PrepareContext(ctx, `
		INSERT INTO episodes (id, definition_id, channel, thread_id, start_time, end_time, event_count, first_event_id, last_event_id, created_at)
		VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
	`)
	if err != nil {
		return result, fmt.Errorf("prepare episode stmt: %w", err)
	}
	defer stmtEpisode.Close()

	stmtEpisodeEvent, err := tx.PrepareContext(ctx, `
		INSERT INTO episode_events (episode_id, event_id, position) VALUES (?, ?, 1)
	`)
	if err != nil {
		return result, fmt.Errorf("prepare episode_event stmt: %w", err)
	}
	defer stmtEpisodeEvent.Close()

	stmtRun, err := tx.PrepareContext(ctx, `
		INSERT INTO analysis_runs (id, analysis_type_id, episode_id, status, started_at, completed_at, output_text, created_at)
		VALUES (?, ?, ?, 'completed', ?, ?, ?, ?)
	`)
	if err != nil {
		return result, fmt.Errorf("prepare run stmt: %w", err)
	}
	defer stmtRun.Close()

	stmtFacet, err := tx.PrepareContext(ctx, `
		INSERT INTO facets (id, analysis_run_id, episode_id, facet_type, value, confidence, metadata_json, created_at)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)
	`)
	if err != nil {
		return result, fmt.Errorf("prepare facet stmt: %w", err)
	}
	defer stmtFacet.Close()

	for _, ed := range events {
		episodeID := uuid.New().String()
		var threadIDVal interface{}
		if ed.threadID.Valid {
			threadIDVal = ed.threadID.String
		}

		_, err = stmtEpisode.ExecContext(ctx, episodeID, episodeDefID, ed.eventChannel, threadIDVal, ed.timestamp, ed.timestamp, ed.eventID, ed.eventID, now)
		if err != nil {
			continue
		}

		_, err = stmtEpisodeEvent.ExecContext(ctx, episodeID, ed.eventID)
		if err != nil {
			continue
		}
		result.EpisodesCreated++

		runID := uuid.New().String()
		_, err = stmtRun.ExecContext(ctx, runID, analysisTypeID, episodeID, now, now, ed.metadataJSON, now)
		if err != nil {
			continue
		}

		facets := extractFacetsFromMeta(ed.meta, runID, episodeID, now)
		for _, f := range facets {
			_, err = stmtFacet.ExecContext(ctx, f.ID, f.AnalysisRunID, f.EpisodeID, f.FacetType, f.Value, f.Confidence, f.MetadataJSON, f.CreatedAt)
			if err == nil {
				result.FacetsCreated++
			}
		}

		result.EventsProcessed++
	}

	if err := tx.Commit(); err != nil {
		return result, fmt.Errorf("commit tx: %w", err)
	}

	result.Duration = time.Since(start)
	return result, nil
}

type facetRow struct {
	ID            string
	AnalysisRunID string
	EpisodeID     string
	FacetType     string
	Value         string
	Confidence    float64
	MetadataJSON  interface{}
	CreatedAt     int64
}

func hasExtractableFacets(meta aixMetadataFull) bool {
	if len(meta.RelevantFiles) > 0 {
		return true
	}
	if meta.ToolFormerData != nil && meta.ToolFormerData.Name != "" {
		return true
	}
	if meta.IsAgentic {
		return true
	}
	if hasNonEmptyCaps(meta.CapabilitiesRan) || hasNonEmptyCaps(meta.CapabilityStatuses) {
		return true
	}
	if len(meta.WebReferences) > 0 || len(meta.DocsReferences) > 0 {
		return true
	}
	return false
}

func extractFacetsFromMeta(meta aixMetadataFull, runID, episodeID string, now int64) []facetRow {
	var facets []facetRow

	// Extract file references
	for _, file := range meta.RelevantFiles {
		if file == "" {
			continue
		}
		facets = append(facets, facetRow{
			ID:            uuid.New().String(),
			AnalysisRunID: runID,
			EpisodeID:     episodeID,
			FacetType:     "file_reference",
			Value:         file,
			Confidence:    1.0,
			CreatedAt:     now,
		})
	}

	// Extract tool usage
	if meta.ToolFormerData != nil && meta.ToolFormerData.Name != "" {
		toolMeta, _ := json.Marshal(map[string]interface{}{
			"status":  meta.ToolFormerData.Status,
			"call_id": meta.ToolFormerData.ToolCallID,
		})
		facets = append(facets, facetRow{
			ID:            uuid.New().String(),
			AnalysisRunID: runID,
			EpisodeID:     episodeID,
			FacetType:     "tool_invocation",
			Value:         meta.ToolFormerData.Name,
			Confidence:    1.0,
			MetadataJSON:  string(toolMeta),
			CreatedAt:     now,
		})
	}

	// Extract agentic mode
	if meta.IsAgentic {
		facets = append(facets, facetRow{
			ID:            uuid.New().String(),
			AnalysisRunID: runID,
			EpisodeID:     episodeID,
			FacetType:     "mode",
			Value:         "agentic",
			Confidence:    1.0,
			CreatedAt:     now,
		})
	}

	// Extract capabilities used
	seenCaps := map[string]struct{}{}
	addCap := func(capType string, count int) {
		if capType == "" {
			return
		}
		if _, ok := seenCaps[capType]; ok {
			return
		}
		seenCaps[capType] = struct{}{}
		facets = append(facets, facetRow{
			ID:            uuid.New().String(),
			AnalysisRunID: runID,
			EpisodeID:     episodeID,
			FacetType:     "capability",
			Value:         capType,
			Confidence:    1.0,
			MetadataJSON:  fmt.Sprintf(`{"count":%d}`, count),
			CreatedAt:     now,
		})
	}
	for capType, caps := range meta.CapabilitiesRan {
		if len(caps) > 0 {
			addCap(capType, len(caps))
		}
	}
	for capType, caps := range meta.CapabilityStatuses {
		if len(caps) > 0 {
			addCap(capType, len(caps))
		}
	}

	return facets
}

func hasNonEmptyCaps(values map[string][]int) bool {
	for _, v := range values {
		if len(v) > 0 {
			return true
		}
	}
	return false
}

func (e *AIXFacetExtractor) ensureAnalysisType(ctx context.Context) (string, error) {
	const analysisTypeName = "aix_metadata_direct"
	
	var id string
	err := e.db.QueryRowContext(ctx, `SELECT id FROM analysis_types WHERE name = ?`, analysisTypeName).Scan(&id)
	if err == nil {
		return id, nil
	}
	if err != sql.ErrNoRows {
		return "", err
	}

	// Create the analysis type
	id = uuid.New().String()
	now := time.Now().Unix()
	_, err = e.db.ExecContext(ctx, `
		INSERT INTO analysis_types (id, name, version, description, output_type, facets_config_json, prompt_template, created_at, updated_at)
		VALUES (?, ?, '1.0.0', 'Direct extraction of facets from AIX message metadata', 'structured', ?, 'N/A - no LLM', ?, ?)
	`, id, analysisTypeName, `{"mappings":[]}`, now, now)
	if err != nil {
		return "", fmt.Errorf("create analysis type: %w", err)
	}

	return id, nil
}

func (e *AIXFacetExtractor) ensureEpisodeDefinition(ctx context.Context) (string, error) {
	config := chunk.SingleEventConfig{}
	return chunk.CreateDefinition(
		ctx,
		e.db,
		"single_event",
		"",
		"single_event",
		config,
		"Single-event episodes (one episode per event)",
	)
}
