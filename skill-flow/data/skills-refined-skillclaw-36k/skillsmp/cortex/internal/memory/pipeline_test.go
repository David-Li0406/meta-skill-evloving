package memory

import (
	"context"
	"database/sql"
	"testing"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

// setupPipelineTestDB creates an in-memory SQLite database with the required schema.
func setupPipelineTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatalf("Failed to open database: %v", err)
	}

	// Create minimal schema for testing
	schema := `
		CREATE TABLE IF NOT EXISTS episodes (
			id TEXT PRIMARY KEY,
			definition_id TEXT NOT NULL,
			channel TEXT,
			thread_id TEXT,
			start_time INTEGER NOT NULL,
			end_time INTEGER NOT NULL,
			event_count INTEGER DEFAULT 0,
			summary TEXT,
			created_at INTEGER NOT NULL
		);

		CREATE TABLE IF NOT EXISTS events (
			id TEXT PRIMARY KEY,
			timestamp INTEGER NOT NULL,
			channel TEXT NOT NULL,
			content_types TEXT NOT NULL,
			content TEXT,
			direction TEXT NOT NULL,
			thread_id TEXT,
			reply_to TEXT,
			source_adapter TEXT NOT NULL,
			source_id TEXT NOT NULL,
			content_hash TEXT,
			metadata_json TEXT
		);

		CREATE TABLE IF NOT EXISTS episode_events (
			episode_id TEXT NOT NULL,
			event_id TEXT NOT NULL,
			position INTEGER NOT NULL,
			PRIMARY KEY (episode_id, event_id)
		);

		CREATE TABLE IF NOT EXISTS entities (
			id TEXT PRIMARY KEY,
			canonical_name TEXT NOT NULL,
			entity_type_id INTEGER NOT NULL,
			summary TEXT,
			summary_updated_at TEXT,
			origin TEXT NOT NULL,
			confidence REAL DEFAULT 1.0,
			merged_into TEXT,
			created_at TEXT NOT NULL,
			updated_at TEXT NOT NULL
		);

		CREATE TABLE IF NOT EXISTS entity_aliases (
			id TEXT PRIMARY KEY,
			entity_id TEXT NOT NULL,
			alias TEXT NOT NULL,
			alias_type TEXT NOT NULL,
			normalized TEXT,
			is_shared BOOLEAN DEFAULT FALSE,
			created_at TEXT NOT NULL
		);

		CREATE INDEX IF NOT EXISTS idx_entity_aliases_lookup ON entity_aliases(alias, alias_type);
		CREATE INDEX IF NOT EXISTS idx_entity_aliases_normalized ON entity_aliases(normalized, alias_type);
		CREATE INDEX IF NOT EXISTS idx_entity_aliases_entity ON entity_aliases(entity_id);

		CREATE TABLE IF NOT EXISTS relationships (
			id TEXT PRIMARY KEY,
			source_entity_id TEXT NOT NULL,
			target_entity_id TEXT,
			target_literal TEXT,
			relation_type TEXT NOT NULL,
			fact TEXT NOT NULL,
			valid_at TEXT,
			invalid_at TEXT,
			created_at TEXT NOT NULL,
			confidence REAL DEFAULT 1.0,
			CHECK ((target_entity_id IS NOT NULL AND target_literal IS NULL) OR
			       (target_entity_id IS NULL AND target_literal IS NOT NULL))
		);

		CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_entity_id);
		CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_entity_id);

		CREATE TABLE IF NOT EXISTS episode_entity_mentions (
			episode_id TEXT NOT NULL,
			entity_id TEXT NOT NULL,
			mention_count INTEGER DEFAULT 1,
			created_at TEXT NOT NULL,
			PRIMARY KEY (episode_id, entity_id)
		);

		CREATE INDEX IF NOT EXISTS idx_episode_entity_mentions_entity ON episode_entity_mentions(entity_id);

		CREATE TABLE IF NOT EXISTS episode_relationship_mentions (
			id TEXT PRIMARY KEY,
			episode_id TEXT NOT NULL,
			relationship_id TEXT,
			extracted_fact TEXT NOT NULL,
			asserted_by_entity_id TEXT,
			source_type TEXT,
			target_literal TEXT,
			alias_id TEXT,
			confidence REAL,
			created_at TEXT NOT NULL
		);

		CREATE INDEX IF NOT EXISTS idx_episode_rel_mentions_episode ON episode_relationship_mentions(episode_id);
		CREATE INDEX IF NOT EXISTS idx_episode_rel_mentions_relationship ON episode_relationship_mentions(relationship_id);

		CREATE TABLE IF NOT EXISTS merge_candidates (
			id TEXT PRIMARY KEY,
			entity_a_id TEXT NOT NULL,
			entity_b_id TEXT NOT NULL,
			confidence REAL NOT NULL,
			auto_eligible BOOLEAN DEFAULT FALSE,
			reason TEXT NOT NULL,
			context TEXT,
			matching_facts TEXT,
			candidates_considered TEXT,
			status TEXT DEFAULT 'pending',
			created_at TEXT NOT NULL,
			resolved_at TEXT,
			resolved_by TEXT,
			UNIQUE(entity_a_id, entity_b_id)
		);

		CREATE TABLE IF NOT EXISTS embeddings (
			id TEXT PRIMARY KEY,
			target_type TEXT NOT NULL,
			target_id TEXT NOT NULL,
			model TEXT NOT NULL,
			embedding_blob BLOB NOT NULL,
			dimension INTEGER NOT NULL,
			source_text_hash TEXT,
			created_at INTEGER NOT NULL,
			UNIQUE(target_type, target_id, model)
		);

		CREATE INDEX IF NOT EXISTS idx_embeddings_target ON embeddings(target_type, target_id);
	`

	_, err = db.Exec(schema)
	if err != nil {
		t.Fatalf("Failed to create schema: %v", err)
	}

	return db
}

// TestNewMemoryPipeline tests pipeline creation.
func TestNewMemoryPipeline(t *testing.T) {
	db := setupPipelineTestDB(t)
	defer db.Close()

	// Test with nil config (should use defaults)
	pipeline := NewMemoryPipeline(db, nil, nil)
	if pipeline == nil {
		t.Fatal("Expected non-nil pipeline")
	}
	if pipeline.entityExtractor == nil {
		t.Error("Expected entity extractor to be initialized")
	}
	if pipeline.entityResolver == nil {
		t.Error("Expected entity resolver to be initialized")
	}

	// Test with custom config
	config := &PipelineConfig{
		ExtractionModel:  "test-model",
		EmbeddingModel:   "test-embed",
		SkipEmbeddings:   true,
		LookbackEpisodes: 2,
	}
	pipeline2 := NewMemoryPipeline(db, nil, config)
	if pipeline2 == nil {
		t.Fatal("Expected non-nil pipeline")
	}
}

// TestDefaultPipelineConfig tests default configuration.
func TestDefaultPipelineConfig(t *testing.T) {
	config := DefaultPipelineConfig()

	if config.ExtractionModel != "gemini-2.0-flash" {
		t.Errorf("Expected extraction model 'gemini-2.0-flash', got '%s'", config.ExtractionModel)
	}
	if config.EmbeddingModel != DefaultEmbeddingModel {
		t.Errorf("Expected embedding model '%s', got '%s'", DefaultEmbeddingModel, config.EmbeddingModel)
	}
	if config.SkipEmbeddings {
		t.Error("Expected SkipEmbeddings to be false by default")
	}
	if config.LookbackEpisodes != 0 {
		t.Errorf("Expected LookbackEpisodes to be 0, got %d", config.LookbackEpisodes)
	}
}

// TestProcessEmptyContent tests processing an episode with empty content.
func TestProcessEmptyContent(t *testing.T) {
	db := setupPipelineTestDB(t)
	defer db.Close()

	config := &PipelineConfig{SkipEmbeddings: true}
	pipeline := NewMemoryPipeline(db, nil, config)

	ctx := context.Background()
	episode := EpisodeInput{
		ID:        "ep-001",
		Channel:   "test",
		Content:   "", // Empty content
		StartTime: time.Now(),
	}

	result, err := pipeline.Process(ctx, episode)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(result.ExtractedEntities) != 0 {
		t.Errorf("Expected 0 entities for empty content, got %d", len(result.ExtractedEntities))
	}
	if result.NewEntities != 0 {
		t.Errorf("Expected 0 new entities, got %d", result.NewEntities)
	}
}

// TestProcessMissingEpisodeID tests processing an episode without an ID.
func TestProcessMissingEpisodeID(t *testing.T) {
	db := setupPipelineTestDB(t)
	defer db.Close()

	config := &PipelineConfig{SkipEmbeddings: true}
	pipeline := NewMemoryPipeline(db, nil, config)

	ctx := context.Background()
	episode := EpisodeInput{
		ID:        "", // Missing ID
		Channel:   "test",
		Content:   "Hello world",
		StartTime: time.Now(),
	}

	_, err := pipeline.Process(ctx, episode)
	if err == nil {
		t.Error("Expected error for missing episode ID")
	}
}

// TestIsEpisodeProcessed tests the idempotency check.
func TestIsEpisodeProcessed(t *testing.T) {
	db := setupPipelineTestDB(t)
	defer db.Close()

	config := &PipelineConfig{SkipEmbeddings: true}
	pipeline := NewMemoryPipeline(db, nil, config)

	ctx := context.Background()
	episodeID := "ep-test-001"

	// Initially should not be processed
	processed, err := pipeline.isEpisodeProcessed(ctx, episodeID)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if processed {
		t.Error("Expected episode to not be processed initially")
	}

	// Insert an entity mention
	now := time.Now().Format(time.RFC3339)
	_, err = db.ExecContext(ctx, `
		INSERT INTO entities (id, canonical_name, entity_type_id, origin, created_at, updated_at)
		VALUES ('ent-001', 'Test Entity', 1, 'extracted', ?, ?)
	`, now, now)
	if err != nil {
		t.Fatalf("Failed to insert entity: %v", err)
	}

	_, err = db.ExecContext(ctx, `
		INSERT INTO episode_entity_mentions (episode_id, entity_id, mention_count, created_at)
		VALUES (?, 'ent-001', 1, ?)
	`, episodeID, now)
	if err != nil {
		t.Fatalf("Failed to insert mention: %v", err)
	}

	// Now should be processed
	processed, err = pipeline.isEpisodeProcessed(ctx, episodeID)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if !processed {
		t.Error("Expected episode to be processed after adding mention")
	}
}

// TestCreateEntityMentions tests creation of episode_entity_mentions.
func TestCreateEntityMentions(t *testing.T) {
	db := setupPipelineTestDB(t)
	defer db.Close()

	config := &PipelineConfig{SkipEmbeddings: true}
	pipeline := NewMemoryPipeline(db, nil, config)

	ctx := context.Background()
	episodeID := "ep-test-002"

	// Create entities first
	now := time.Now().Format(time.RFC3339)
	_, err := db.ExecContext(ctx, `
		INSERT INTO entities (id, canonical_name, entity_type_id, origin, created_at, updated_at)
		VALUES ('ent-001', 'Alice', 1, 'extracted', ?, ?),
		       ('ent-002', 'Bob', 1, 'extracted', ?, ?)
	`, now, now, now, now)
	if err != nil {
		t.Fatalf("Failed to insert entities: %v", err)
	}

	entities := []ResolvedEntity{
		{ID: "ent-001", Name: "Alice", EntityTypeID: 1, IsNew: true},
		{ID: "ent-002", Name: "Bob", EntityTypeID: 1, IsNew: false},
	}

	count, err := pipeline.createEntityMentions(ctx, episodeID, entities)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if count != 2 {
		t.Errorf("Expected 2 mentions created, got %d", count)
	}

	// Verify mentions were created
	var mentionCount int
	err = db.QueryRowContext(ctx, `
		SELECT COUNT(*) FROM episode_entity_mentions WHERE episode_id = ?
	`, episodeID).Scan(&mentionCount)
	if err != nil {
		t.Fatalf("Failed to count mentions: %v", err)
	}
	if mentionCount != 2 {
		t.Errorf("Expected 2 mentions in DB, got %d", mentionCount)
	}

	// Test idempotency - creating same mentions again should increment count
	count2, err := pipeline.createEntityMentions(ctx, episodeID, entities)
	if err != nil {
		t.Fatalf("Unexpected error on second call: %v", err)
	}
	if count2 != 2 {
		t.Errorf("Expected 2 mentions processed on second call, got %d", count2)
	}

	// Check mention counts were incremented
	var ent1Count int
	err = db.QueryRowContext(ctx, `
		SELECT mention_count FROM episode_entity_mentions
		WHERE episode_id = ? AND entity_id = 'ent-001'
	`, episodeID).Scan(&ent1Count)
	if err != nil {
		t.Fatalf("Failed to get mention count: %v", err)
	}
	if ent1Count != 2 {
		t.Errorf("Expected mention_count to be 2 after second call, got %d", ent1Count)
	}
}

// TestGetStats tests aggregate statistics.
func TestGetStats(t *testing.T) {
	db := setupPipelineTestDB(t)
	defer db.Close()

	config := &PipelineConfig{SkipEmbeddings: true}
	pipeline := NewMemoryPipeline(db, nil, config)

	ctx := context.Background()
	now := time.Now().Format(time.RFC3339)

	// Insert test data
	_, err := db.ExecContext(ctx, `
		INSERT INTO entities (id, canonical_name, entity_type_id, origin, created_at, updated_at)
		VALUES ('ent-001', 'Alice', 1, 'extracted', ?, ?),
		       ('ent-002', 'Bob', 1, 'extracted', ?, ?),
		       ('ent-003', 'MergedEntity', 1, 'extracted', ?, ?)
	`, now, now, now, now, now, now)
	if err != nil {
		t.Fatalf("Failed to insert entities: %v", err)
	}

	// Mark one as merged
	_, err = db.ExecContext(ctx, `UPDATE entities SET merged_into = 'ent-001' WHERE id = 'ent-003'`)
	if err != nil {
		t.Fatalf("Failed to mark entity merged: %v", err)
	}

	// Insert aliases
	_, err = db.ExecContext(ctx, `
		INSERT INTO entity_aliases (id, entity_id, alias, alias_type, normalized, created_at)
		VALUES ('alias-001', 'ent-001', 'alice@test.com', 'email', 'alice@test.com', ?),
		       ('alias-002', 'ent-002', 'bob@test.com', 'email', 'bob@test.com', ?)
	`, now, now)
	if err != nil {
		t.Fatalf("Failed to insert aliases: %v", err)
	}

	// Insert relationships
	_, err = db.ExecContext(ctx, `
		INSERT INTO relationships (id, source_entity_id, target_entity_id, relation_type, fact, created_at)
		VALUES ('rel-001', 'ent-001', 'ent-002', 'KNOWS', 'Alice knows Bob', ?),
		       ('rel-002', 'ent-002', 'ent-001', 'KNOWS', 'Bob knows Alice', ?)
	`, now, now)
	if err != nil {
		t.Fatalf("Failed to insert relationships: %v", err)
	}

	// Mark one relationship as invalidated
	_, err = db.ExecContext(ctx, `UPDATE relationships SET invalid_at = ? WHERE id = 'rel-002'`, now)
	if err != nil {
		t.Fatalf("Failed to invalidate relationship: %v", err)
	}

	// Insert mentions
	_, err = db.ExecContext(ctx, `
		INSERT INTO episode_entity_mentions (episode_id, entity_id, mention_count, created_at)
		VALUES ('ep-001', 'ent-001', 3, ?),
		       ('ep-001', 'ent-002', 2, ?)
	`, now, now)
	if err != nil {
		t.Fatalf("Failed to insert mentions: %v", err)
	}

	// Get stats
	stats, err := pipeline.GetStats(ctx)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	// Verify stats
	if stats.TotalEntities != 2 { // Excludes merged entity
		t.Errorf("Expected 2 entities, got %d", stats.TotalEntities)
	}
	if stats.TotalRelationships != 1 { // Excludes invalidated
		t.Errorf("Expected 1 valid relationship, got %d", stats.TotalRelationships)
	}
	if stats.TotalAliases != 2 {
		t.Errorf("Expected 2 aliases, got %d", stats.TotalAliases)
	}
	if stats.TotalMentions != 5 { // 3 + 2
		t.Errorf("Expected 5 total mentions, got %d", stats.TotalMentions)
	}
	if stats.TotalContradictions != 1 {
		t.Errorf("Expected 1 contradiction, got %d", stats.TotalContradictions)
	}
}

// TestFilterNewEntities tests the helper function.
func TestFilterNewEntities(t *testing.T) {
	entities := []ResolvedEntity{
		{ID: "ent-001", Name: "Alice", IsNew: true},
		{ID: "ent-002", Name: "Bob", IsNew: false},
		{ID: "ent-003", Name: "Charlie", IsNew: true},
	}

	newEntities := filterNewEntities(entities)

	if len(newEntities) != 2 {
		t.Errorf("Expected 2 new entities, got %d", len(newEntities))
	}

	// Verify the correct entities
	found := make(map[string]bool)
	for _, e := range newEntities {
		found[e.ID] = true
	}
	if !found["ent-001"] {
		t.Error("Expected ent-001 in new entities")
	}
	if !found["ent-003"] {
		t.Error("Expected ent-003 in new entities")
	}
}

// TestCountNewAliases tests the helper function.
func TestCountNewAliases(t *testing.T) {
	promoted := []PromotedIdentity{
		{AliasID: "alias-001", SourceType: "self_disclosed"},
		{AliasID: "alias-002", SourceType: "mentioned"}, // Not counted
		{AliasID: "", SourceType: "self_disclosed"},      // Not counted (no alias)
		{AliasID: "alias-003", SourceType: "self_disclosed"},
	}

	count := countNewAliases(promoted)

	if count != 2 {
		t.Errorf("Expected 2 new aliases, got %d", count)
	}
}

// TestGetPreviousEpisodes tests episode lookback.
func TestGetPreviousEpisodes(t *testing.T) {
	db := setupPipelineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	now := time.Now()

	// Insert test episodes
	_, err := db.ExecContext(ctx, `
		INSERT INTO episodes (id, definition_id, channel, start_time, end_time, created_at)
		VALUES
			('ep-001', 'def-1', 'test', ?, ?, ?),
			('ep-002', 'def-1', 'test', ?, ?, ?),
			('ep-003', 'def-1', 'other', ?, ?, ?)
	`, now.Add(-3*time.Hour).Unix(), now.Add(-2*time.Hour).Unix(), now.Unix(),
		now.Add(-1*time.Hour).Unix(), now.Unix(), now.Unix(),
		now.Add(-30*time.Minute).Unix(), now.Unix(), now.Unix())
	if err != nil {
		t.Fatalf("Failed to insert episodes: %v", err)
	}

	// Insert events for ep-001
	_, err = db.ExecContext(ctx, `
		INSERT INTO events (id, timestamp, channel, content_types, content, direction, source_adapter, source_id)
		VALUES ('evt-001', ?, 'test', '["text"]', 'Previous content', 'received', 'test', 'src-001')
	`, now.Add(-3*time.Hour).Unix())
	if err != nil {
		t.Fatalf("Failed to insert event: %v", err)
	}

	// Link event to episode
	_, err = db.ExecContext(ctx, `
		INSERT INTO episode_events (episode_id, event_id, position)
		VALUES ('ep-001', 'evt-001', 1)
	`)
	if err != nil {
		t.Fatalf("Failed to link event: %v", err)
	}

	config := &PipelineConfig{SkipEmbeddings: true, LookbackEpisodes: 2}
	pipeline := NewMemoryPipeline(db, nil, config)

	episode := EpisodeInput{
		ID:        "ep-current",
		Channel:   "test",
		StartTime: now,
	}

	previous, err := pipeline.getPreviousEpisodes(ctx, episode)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	// Should find 2 episodes in the same channel before current time
	// But only ep-001 has content
	if len(previous) != 1 {
		t.Errorf("Expected 1 previous episode with content, got %d", len(previous))
	}

	if len(previous) > 0 && previous[0] != "Previous content" {
		t.Errorf("Expected 'Previous content', got '%s'", previous[0])
	}
}

// TestProcessBatch tests batch processing.
func TestProcessBatch(t *testing.T) {
	db := setupPipelineTestDB(t)
	defer db.Close()

	config := &PipelineConfig{SkipEmbeddings: true}
	pipeline := NewMemoryPipeline(db, nil, config)

	ctx := context.Background()
	episodes := []EpisodeInput{
		{ID: "ep-001", Channel: "test", Content: "", StartTime: time.Now()},
		{ID: "ep-002", Channel: "test", Content: "", StartTime: time.Now()},
	}

	results, err := pipeline.ProcessBatch(ctx, episodes)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(results) != 2 {
		t.Errorf("Expected 2 results, got %d", len(results))
	}
}

// TestIdempotency tests that reprocessing is idempotent.
func TestIdempotency(t *testing.T) {
	db := setupPipelineTestDB(t)
	defer db.Close()

	config := &PipelineConfig{SkipEmbeddings: true}
	pipeline := NewMemoryPipeline(db, nil, config)

	ctx := context.Background()
	episodeID := "ep-idempotent"
	now := time.Now().Format(time.RFC3339)

	// Create an entity and mention (simulate previous processing)
	_, err := db.ExecContext(ctx, `
		INSERT INTO entities (id, canonical_name, entity_type_id, origin, created_at, updated_at)
		VALUES ('ent-001', 'Test', 1, 'extracted', ?, ?)
	`, now, now)
	if err != nil {
		t.Fatalf("Failed to insert entity: %v", err)
	}

	_, err = db.ExecContext(ctx, `
		INSERT INTO episode_entity_mentions (episode_id, entity_id, mention_count, created_at)
		VALUES (?, 'ent-001', 1, ?)
	`, episodeID, now)
	if err != nil {
		t.Fatalf("Failed to insert mention: %v", err)
	}

	// Process should skip
	episode := EpisodeInput{
		ID:        episodeID,
		Channel:   "test",
		Content:   "Some content that would normally be processed",
		StartTime: time.Now(),
	}

	result, err := pipeline.Process(ctx, episode)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if !result.Skipped {
		t.Error("Expected episode to be skipped (already processed)")
	}
	if result.NewEntities != 0 {
		t.Errorf("Expected 0 new entities when skipped, got %d", result.NewEntities)
	}
}
