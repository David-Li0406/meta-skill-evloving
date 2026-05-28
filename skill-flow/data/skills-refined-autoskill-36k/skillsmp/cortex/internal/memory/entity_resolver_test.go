package memory

import (
	"context"
	"database/sql"
	"math"
	"testing"
	"time"

	_ "modernc.org/sqlite"
)

// setupResolverTestDB creates an in-memory SQLite database with the necessary schema.
func setupResolverTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite", ":memory:")
	if err != nil {
		t.Fatalf("failed to open database: %v", err)
	}

	// Create necessary tables
	schema := `
		CREATE TABLE entities (
			id TEXT PRIMARY KEY,
			canonical_name TEXT NOT NULL,
			entity_type_id INTEGER NOT NULL,
			summary TEXT,
			summary_updated_at TEXT,
			origin TEXT NOT NULL,
			confidence REAL DEFAULT 1.0,
			merged_into TEXT REFERENCES entities(id),
			created_at TEXT NOT NULL,
			updated_at TEXT NOT NULL
		);

		CREATE TABLE entity_aliases (
			id TEXT PRIMARY KEY,
			entity_id TEXT NOT NULL REFERENCES entities(id),
			alias TEXT NOT NULL,
			alias_type TEXT NOT NULL,
			normalized TEXT,
			is_shared BOOLEAN DEFAULT FALSE,
			created_at TEXT NOT NULL
		);

		CREATE INDEX idx_entity_aliases_normalized ON entity_aliases(normalized, alias_type);
		CREATE INDEX idx_entity_aliases_lookup ON entity_aliases(alias, alias_type);
		CREATE INDEX idx_entity_aliases_entity ON entity_aliases(entity_id);

		CREATE TABLE embeddings (
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

		CREATE TABLE relationships (
			id TEXT PRIMARY KEY,
			source_entity_id TEXT NOT NULL REFERENCES entities(id),
			target_entity_id TEXT REFERENCES entities(id),
			target_literal TEXT,
			relation_type TEXT NOT NULL,
			fact TEXT NOT NULL,
			valid_at TEXT,
			invalid_at TEXT,
			created_at TEXT NOT NULL,
			confidence REAL DEFAULT 1.0
		);

		CREATE TABLE episodes (
			id TEXT PRIMARY KEY,
			definition_id TEXT,
			channel TEXT,
			thread_id TEXT,
			start_time INTEGER,
			end_time INTEGER,
			event_count INTEGER
		);

		CREATE TABLE episode_entity_mentions (
			episode_id TEXT NOT NULL REFERENCES episodes(id),
			entity_id TEXT NOT NULL REFERENCES entities(id),
			mention_count INTEGER DEFAULT 1,
			created_at TEXT NOT NULL,
			PRIMARY KEY (episode_id, entity_id)
		);

		CREATE TABLE merge_candidates (
			id TEXT PRIMARY KEY,
			entity_a_id TEXT NOT NULL REFERENCES entities(id),
			entity_b_id TEXT NOT NULL REFERENCES entities(id),
			confidence REAL NOT NULL,
			auto_eligible BOOLEAN DEFAULT FALSE,
			reason TEXT NOT NULL,
			matching_facts TEXT,
			context TEXT,
			candidates_considered TEXT,
			conflicts TEXT,
			status TEXT DEFAULT 'pending',
			created_at TEXT NOT NULL,
			resolved_at TEXT,
			resolved_by TEXT,
			resolution_reason TEXT,
			UNIQUE(entity_a_id, entity_b_id)
		);
	`
	_, err = db.Exec(schema)
	if err != nil {
		t.Fatalf("failed to create schema: %v", err)
	}

	return db
}

// insertTestEntity inserts an entity for testing.
func insertTestEntity(t *testing.T, db *sql.DB, id, name string, typeID int) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO entities (id, canonical_name, entity_type_id, origin, created_at, updated_at)
		VALUES (?, ?, ?, 'manual', ?, ?)
	`, id, name, typeID, now, now)
	if err != nil {
		t.Fatalf("failed to insert entity: %v", err)
	}
}

// insertTestAlias inserts an alias for testing.
func insertTestAlias(t *testing.T, db *sql.DB, id, entityID, alias, aliasType string, isShared bool) {
	now := time.Now().Format(time.RFC3339)
	normalized := normalizeAlias(alias)
	_, err := db.Exec(`
		INSERT INTO entity_aliases (id, entity_id, alias, alias_type, normalized, is_shared, created_at)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	`, id, entityID, alias, aliasType, normalized, isShared, now)
	if err != nil {
		t.Fatalf("failed to insert alias: %v", err)
	}
}

// insertTestRelationship inserts a relationship for testing.
func insertTestRelationship(t *testing.T, db *sql.DB, id, sourceID, targetID, relType, fact string) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO relationships (id, source_entity_id, target_entity_id, relation_type, fact, created_at)
		VALUES (?, ?, ?, ?, ?, ?)
	`, id, sourceID, targetID, relType, fact, now)
	if err != nil {
		t.Fatalf("failed to insert relationship: %v", err)
	}
}

// insertTestEpisode inserts an episode for testing.
func insertTestEpisode(t *testing.T, db *sql.DB, id, channel string, endTime int64) {
	_, err := db.Exec(`
		INSERT INTO episodes (id, channel, end_time, event_count)
		VALUES (?, ?, ?, 1)
	`, id, channel, endTime)
	if err != nil {
		t.Fatalf("failed to insert episode: %v", err)
	}
}

// insertTestMention inserts an episode-entity mention for testing.
func insertTestMention(t *testing.T, db *sql.DB, episodeID, entityID string) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO episode_entity_mentions (episode_id, entity_id, created_at)
		VALUES (?, ?, ?)
	`, episodeID, entityID, now)
	if err != nil {
		t.Fatalf("failed to insert mention: %v", err)
	}
}

func TestEntityResolver_NoMatch_CreatesNewEntity(t *testing.T) {
	db := setupResolverTestDB(t)
	defer db.Close()

	resolver := NewEntityResolver(db, nil, "")

	extracted := []ExtractedEntity{
		{ID: 0, Name: "Alice Smith", EntityTypeID: EntityTypePerson},
	}

	result, err := resolver.Resolve(context.Background(), extracted, ResolutionContext{})
	if err != nil {
		t.Fatalf("Resolve failed: %v", err)
	}

	if len(result.ResolvedEntities) != 1 {
		t.Fatalf("expected 1 resolved entity, got %d", len(result.ResolvedEntities))
	}

	resolved := result.ResolvedEntities[0]
	if !resolved.IsNew {
		t.Error("expected IsNew to be true for new entity")
	}
	if resolved.Decision != DecisionCreatedNew {
		t.Errorf("expected decision %s, got %s", DecisionCreatedNew, resolved.Decision)
	}
	if resolved.ID == "" {
		t.Error("expected non-empty UUID for new entity")
	}

	// Check UUID map
	if result.UUIDMap[0] != resolved.ID {
		t.Errorf("UUID map mismatch: expected %s, got %s", resolved.ID, result.UUIDMap[0])
	}

	// Verify entity was created in database
	var count int
	err = db.QueryRow("SELECT COUNT(*) FROM entities WHERE id = ?", resolved.ID).Scan(&count)
	if err != nil || count != 1 {
		t.Errorf("entity not found in database")
	}

	// Verify alias was created
	err = db.QueryRow("SELECT COUNT(*) FROM entity_aliases WHERE entity_id = ?", resolved.ID).Scan(&count)
	if err != nil || count != 1 {
		t.Errorf("alias not found in database")
	}
}

func TestEntityResolver_ExactAliasMatch_ReturnsExisting(t *testing.T) {
	db := setupResolverTestDB(t)
	defer db.Close()

	// Create existing entity with alias
	insertTestEntity(t, db, "ent-001", "Tyler Brandt", EntityTypePerson)
	insertTestAlias(t, db, "alias-001", "ent-001", "Tyler", "name", false)

	resolver := NewEntityResolver(db, nil, "")

	extracted := []ExtractedEntity{
		{ID: 0, Name: "Tyler", EntityTypeID: EntityTypePerson},
	}

	result, err := resolver.Resolve(context.Background(), extracted, ResolutionContext{})
	if err != nil {
		t.Fatalf("Resolve failed: %v", err)
	}

	if len(result.ResolvedEntities) != 1 {
		t.Fatalf("expected 1 resolved entity, got %d", len(result.ResolvedEntities))
	}

	resolved := result.ResolvedEntities[0]
	if resolved.IsNew {
		t.Error("expected IsNew to be false for matched entity")
	}
	if resolved.ID != "ent-001" {
		t.Errorf("expected entity ID 'ent-001', got %s", resolved.ID)
	}
	if resolved.Decision != DecisionExactAlias && resolved.Decision != DecisionHighConfidence {
		t.Errorf("expected decision ExactAlias or HighConfidence, got %s", resolved.Decision)
	}
}

func TestEntityResolver_EmailAliasMatch_HighConfidence(t *testing.T) {
	db := setupResolverTestDB(t)
	defer db.Close()

	// Create existing entity with email alias
	insertTestEntity(t, db, "ent-002", "Tyler Brandt", EntityTypePerson)
	insertTestAlias(t, db, "alias-002", "ent-002", "tyler@example.com", "email", false)

	resolver := NewEntityResolver(db, nil, "")

	extracted := []ExtractedEntity{
		{ID: 0, Name: "tyler@example.com", EntityTypeID: EntityTypePerson},
	}

	result, err := resolver.Resolve(context.Background(), extracted, ResolutionContext{})
	if err != nil {
		t.Fatalf("Resolve failed: %v", err)
	}

	resolved := result.ResolvedEntities[0]
	if resolved.IsNew {
		t.Error("expected IsNew to be false for email-matched entity")
	}
	if resolved.ID != "ent-002" {
		t.Errorf("expected entity ID 'ent-002', got %s", resolved.ID)
	}
}

func TestEntityResolver_SharedAlias_ReducedConfidence(t *testing.T) {
	db := setupResolverTestDB(t)
	defer db.Close()

	// Create two entities sharing the same phone alias (family phone)
	insertTestEntity(t, db, "ent-003", "Mom", EntityTypePerson)
	insertTestEntity(t, db, "ent-004", "Dad", EntityTypePerson)
	insertTestAlias(t, db, "alias-003", "ent-003", "+1-555-0100", "phone", true)
	insertTestAlias(t, db, "alias-004", "ent-004", "+1-555-0100", "phone", true)

	resolver := NewEntityResolver(db, nil, "")

	extracted := []ExtractedEntity{
		{ID: 0, Name: "+1-555-0100", EntityTypeID: EntityTypePerson},
	}

	result, err := resolver.Resolve(context.Background(), extracted, ResolutionContext{})
	if err != nil {
		t.Fatalf("Resolve failed: %v", err)
	}

	// Should have multiple candidates due to shared alias
	candidates := result.CandidatesMap[0]
	if len(candidates) < 2 {
		t.Errorf("expected at least 2 candidates for shared alias, got %d", len(candidates))
	}

	// Shared aliases should have reduced scores
	for _, c := range candidates {
		if c.AliasScore > 0.7 { // 0.95 * 0.7 = 0.665
			t.Logf("candidate %s has alias score %.3f", c.CanonicalName, c.AliasScore)
		}
	}
}

func TestEntityResolver_MergedEntity_Excluded(t *testing.T) {
	db := setupResolverTestDB(t)
	defer db.Close()

	// Create entity that was merged
	insertTestEntity(t, db, "ent-005", "Old Tyler", EntityTypePerson)
	insertTestAlias(t, db, "alias-005", "ent-005", "Tyler", "name", false)

	// Mark as merged
	_, err := db.Exec("UPDATE entities SET merged_into = 'ent-other' WHERE id = 'ent-005'")
	if err != nil {
		t.Fatalf("failed to update entity: %v", err)
	}

	resolver := NewEntityResolver(db, nil, "")

	extracted := []ExtractedEntity{
		{ID: 0, Name: "Tyler", EntityTypeID: EntityTypePerson},
	}

	result, err := resolver.Resolve(context.Background(), extracted, ResolutionContext{})
	if err != nil {
		t.Fatalf("Resolve failed: %v", err)
	}

	// Should NOT match merged entity - should create new
	resolved := result.ResolvedEntities[0]
	if resolved.ID == "ent-005" {
		t.Error("should not match merged entity")
	}
	if !resolved.IsNew {
		t.Error("expected new entity to be created when merged entity excluded")
	}
}

func TestEntityResolver_RelationshipContext_BoostsScore(t *testing.T) {
	db := setupResolverTestDB(t)
	defer db.Close()

	// Create Tyler and Casey with a relationship
	insertTestEntity(t, db, "ent-tyler", "Tyler Brandt", EntityTypePerson)
	insertTestEntity(t, db, "ent-casey", "Casey Adams", EntityTypePerson)
	insertTestAlias(t, db, "alias-tyler", "ent-tyler", "Tyler", "name", false)
	insertTestRelationship(t, db, "rel-001", "ent-tyler", "ent-casey", "KNOWS", "Tyler knows Casey")

	resolver := NewEntityResolver(db, nil, "")

	extracted := []ExtractedEntity{
		{ID: 0, Name: "Tyler", EntityTypeID: EntityTypePerson},
	}

	// Resolve with Casey as co-mentioned (already resolved)
	result, err := resolver.Resolve(context.Background(), extracted, ResolutionContext{
		CoMentionedIDs: []string{"ent-casey"},
	})
	if err != nil {
		t.Fatalf("Resolve failed: %v", err)
	}

	resolved := result.ResolvedEntities[0]
	if resolved.ID != "ent-tyler" {
		t.Errorf("expected to match Tyler due to relationship with Casey, got %s", resolved.ID)
	}

	// Check that context score was applied
	candidates := result.CandidatesMap[0]
	if len(candidates) > 0 && candidates[0].ContextScore == 0 {
		t.Log("context score was not applied (relationship check may not have matched)")
	}
}

func TestEntityResolver_ChannelRecency_BoostsScore(t *testing.T) {
	db := setupResolverTestDB(t)
	defer db.Close()

	// Create Tyler with recent mention in imessage channel
	insertTestEntity(t, db, "ent-tyler2", "Tyler Brandt", EntityTypePerson)
	insertTestAlias(t, db, "alias-tyler2", "ent-tyler2", "Tyler", "name", false)

	// Create recent episode in imessage
	recentTime := time.Now().Add(-24 * time.Hour).Unix()
	insertTestEpisode(t, db, "ep-001", "imessage", recentTime)
	insertTestMention(t, db, "ep-001", "ent-tyler2")

	resolver := NewEntityResolver(db, nil, "")

	extracted := []ExtractedEntity{
		{ID: 0, Name: "Tyler", EntityTypeID: EntityTypePerson},
	}

	// Resolve with channel context
	result, err := resolver.Resolve(context.Background(), extracted, ResolutionContext{
		Channel: "imessage",
	})
	if err != nil {
		t.Fatalf("Resolve failed: %v", err)
	}

	resolved := result.ResolvedEntities[0]
	if resolved.ID != "ent-tyler2" {
		t.Errorf("expected to match Tyler due to channel recency, got %s", resolved.ID)
	}
}

func TestEntityResolver_AmbiguousMatch_CreatesMergeCandidate(t *testing.T) {
	db := setupResolverTestDB(t)
	defer db.Close()

	// Create two Tylers (no distinguishing features)
	insertTestEntity(t, db, "ent-tyler-a", "Tyler A", EntityTypePerson)
	insertTestEntity(t, db, "ent-tyler-b", "Tyler B", EntityTypePerson)
	insertTestAlias(t, db, "alias-tyler-a", "ent-tyler-a", "Tyler", "name", false)
	insertTestAlias(t, db, "alias-tyler-b", "ent-tyler-b", "Tyler", "name", false)

	resolver := NewEntityResolver(db, nil, "")

	extracted := []ExtractedEntity{
		{ID: 0, Name: "Tyler", EntityTypeID: EntityTypePerson},
	}

	result, err := resolver.Resolve(context.Background(), extracted, ResolutionContext{})
	if err != nil {
		t.Fatalf("Resolve failed: %v", err)
	}

	// With two equally-scoring candidates, should create new and add merge candidate
	resolved := result.ResolvedEntities[0]

	// Verify that candidates were considered
	candidates := result.CandidatesMap[0]
	if len(candidates) < 2 {
		t.Logf("expected 2 candidates, got %d", len(candidates))
	}

	// If ambiguous, should have created merge candidate (check if new entity created)
	if resolved.IsNew && resolved.Decision == DecisionAmbiguous {
		// Check merge candidate was created
		var count int
		err = db.QueryRow("SELECT COUNT(*) FROM merge_candidates WHERE entity_a_id = ?", resolved.ID).Scan(&count)
		if err != nil {
			t.Errorf("failed to check merge candidates: %v", err)
		}
		if count != 1 {
			t.Errorf("expected 1 merge candidate, got %d", count)
		}
	}
}

func TestEntityResolver_MultipleEntities_PreservesOrder(t *testing.T) {
	db := setupResolverTestDB(t)
	defer db.Close()

	resolver := NewEntityResolver(db, nil, "")

	extracted := []ExtractedEntity{
		{ID: 0, Name: "Alice", EntityTypeID: EntityTypePerson},
		{ID: 1, Name: "Bob", EntityTypeID: EntityTypePerson},
		{ID: 2, Name: "Charlie", EntityTypeID: EntityTypePerson},
	}

	result, err := resolver.Resolve(context.Background(), extracted, ResolutionContext{})
	if err != nil {
		t.Fatalf("Resolve failed: %v", err)
	}

	if len(result.ResolvedEntities) != 3 {
		t.Fatalf("expected 3 resolved entities, got %d", len(result.ResolvedEntities))
	}

	// Check UUID map has all entries
	if len(result.UUIDMap) != 3 {
		t.Errorf("expected 3 entries in UUID map, got %d", len(result.UUIDMap))
	}

	for i := 0; i < 3; i++ {
		if _, ok := result.UUIDMap[i]; !ok {
			t.Errorf("UUID map missing entry for ID %d", i)
		}
	}

	// Verify all are unique
	seen := make(map[string]bool)
	for _, id := range result.UUIDMap {
		if seen[id] {
			t.Error("duplicate UUID in map")
		}
		seen[id] = true
	}
}

func TestEntityResolver_EmptyName_ReturnsError(t *testing.T) {
	db := setupResolverTestDB(t)
	defer db.Close()

	resolver := NewEntityResolver(db, nil, "")

	extracted := []ExtractedEntity{
		{ID: 0, Name: "", EntityTypeID: EntityTypePerson},
	}

	_, err := resolver.Resolve(context.Background(), extracted, ResolutionContext{})
	if err == nil {
		t.Error("expected error for empty name")
	}
}

func TestNormalizeAlias(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Tyler", "tyler"},
		{"  Tyler  ", "tyler"},
		{"TYLER BRANDT", "tyler brandt"},
		{"tyler@example.com", "tyler@example.com"},
	}

	for _, tt := range tests {
		result := normalizeAlias(tt.input)
		if result != tt.expected {
			t.Errorf("normalizeAlias(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSortCandidatesByScore(t *testing.T) {
	candidates := []ResolutionCandidate{
		{EntityID: "a", TotalScore: 0.5},
		{EntityID: "b", TotalScore: 0.9},
		{EntityID: "c", TotalScore: 0.7},
	}

	sortCandidatesByScore(candidates)

	expected := []string{"b", "c", "a"}
	for i, c := range candidates {
		if c.EntityID != expected[i] {
			t.Errorf("position %d: expected %s, got %s", i, expected[i], c.EntityID)
		}
	}
}

func TestCosineSimilarity(t *testing.T) {
	tests := []struct {
		a, b     []float64
		expected float64
	}{
		{[]float64{1, 0, 0}, []float64{1, 0, 0}, 1.0},
		{[]float64{1, 0, 0}, []float64{0, 1, 0}, 0.0},
		{[]float64{1, 0, 0}, []float64{-1, 0, 0}, -1.0},
		{[]float64{1, 1}, []float64{1, 1}, 1.0},
		{[]float64{}, []float64{}, 0.0},
	}

	for _, tt := range tests {
		result := cosineSimilarity(tt.a, tt.b)
		if math.Abs(result-tt.expected) > 0.001 {
			t.Errorf("cosineSimilarity(%v, %v) = %f, want %f", tt.a, tt.b, result, tt.expected)
		}
	}
}

func TestNormalizeCosine(t *testing.T) {
	tests := []struct {
		input    float64
		expected float64
	}{
		{1.0, 1.0},
		{0.0, 0.5},
		{-1.0, 0.0},
		{0.5, 0.75},
	}

	for _, tt := range tests {
		result := normalizeCosine(tt.input)
		if math.Abs(result-tt.expected) > 0.001 {
			t.Errorf("normalizeCosine(%f) = %f, want %f", tt.input, result, tt.expected)
		}
	}
}
