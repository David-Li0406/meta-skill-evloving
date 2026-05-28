package memory

import (
	"context"
	"database/sql"
	"os"
	"path/filepath"
	"testing"

	_ "github.com/mattn/go-sqlite3"
)

func setupVerifyTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatalf("Failed to open test database: %v", err)
	}

	schema := `
		CREATE TABLE events (
			id TEXT PRIMARY KEY,
			channel TEXT NOT NULL,
			timestamp INTEGER NOT NULL,
			content TEXT,
			sender TEXT,
			metadata TEXT,
			created_at TEXT DEFAULT (datetime('now'))
		);

		CREATE TABLE episodes (
			id TEXT PRIMARY KEY,
			channel TEXT NOT NULL,
			thread_id TEXT,
			start_time INTEGER,
			end_time INTEGER,
			event_count INTEGER DEFAULT 0,
			metadata TEXT,
			created_at TEXT DEFAULT (datetime('now'))
		);

		CREATE TABLE episode_events (
			episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
			event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
			position INTEGER NOT NULL,
			PRIMARY KEY (episode_id, event_id)
		);

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

		CREATE TABLE entities (
			id TEXT PRIMARY KEY,
			canonical_name TEXT NOT NULL,
			entity_type_id INTEGER NOT NULL,
			summary TEXT,
			summary_updated_at TEXT,
			origin TEXT,
			confidence REAL DEFAULT 1.0,
			merged_into TEXT REFERENCES entities(id),
			created_at TEXT DEFAULT (datetime('now')),
			updated_at TEXT DEFAULT (datetime('now'))
		);

		CREATE TABLE entity_aliases (
			id TEXT PRIMARY KEY,
			entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
			alias TEXT NOT NULL,
			alias_type TEXT NOT NULL,
			normalized TEXT NOT NULL,
			is_shared INTEGER DEFAULT 0,
			created_at TEXT DEFAULT (datetime('now'))
		);

		CREATE TABLE relationships (
			id TEXT PRIMARY KEY,
			source_entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
			target_entity_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
			target_literal TEXT,
			relation_type TEXT NOT NULL,
			fact TEXT,
			valid_at TEXT,
			invalid_at TEXT,
			created_at TEXT DEFAULT (datetime('now')),
			confidence REAL DEFAULT 1.0,
			CHECK ((target_entity_id IS NULL) != (target_literal IS NULL))
		);

		CREATE TABLE episode_entity_mentions (
			episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
			entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
			mention_count INTEGER DEFAULT 1,
			created_at TEXT DEFAULT (datetime('now')),
			PRIMARY KEY (episode_id, entity_id)
		);

		CREATE TABLE episode_relationship_mentions (
			id TEXT PRIMARY KEY,
			episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
			relationship_id TEXT REFERENCES relationships(id) ON DELETE CASCADE,
			extracted_fact TEXT,
			asserted_by_entity_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
			source_type TEXT,
			target_literal TEXT,
			alias_id TEXT REFERENCES entity_aliases(id) ON DELETE SET NULL,
			confidence REAL DEFAULT 1.0,
			created_at TEXT DEFAULT (datetime('now'))
		);

		CREATE TABLE merge_candidates (
			id TEXT PRIMARY KEY,
			entity_a_id TEXT NOT NULL REFERENCES entities(id),
			entity_b_id TEXT NOT NULL REFERENCES entities(id),
			confidence REAL NOT NULL,
			auto_eligible INTEGER DEFAULT 0,
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

		CREATE TABLE entity_merge_events (
			id TEXT PRIMARY KEY,
			source_entity_id TEXT NOT NULL,
			target_entity_id TEXT NOT NULL,
			merge_type TEXT,
			triggering_facts TEXT,
			similarity_score REAL,
			created_at TEXT DEFAULT (datetime('now')),
			resolved_by TEXT
		);
	`
	_, err = db.Exec(schema)
	if err != nil {
		t.Fatalf("Failed to create schema: %v", err)
	}

	return db
}

func TestMatchLikePattern(t *testing.T) {
	tests := []struct {
		value   string
		pattern string
		want    bool
	}{
		// Exact match
		{"hello", "hello", true},
		{"hello", "world", false},

		// Prefix match (suffix wildcard)
		{"hello world", "hello%", true},
		{"hello world", "world%", false},
		{"2023-01-15", "2023%", true},
		{"2024-01-15", "2023%", false},

		// Suffix match (prefix wildcard)
		{"hello world", "%world", true},
		{"hello world", "%hello", false},

		// Contains (both wildcards)
		{"hello world", "%wor%", true},
		{"hello world", "%xyz%", false},

		// Match everything
		{"anything", "%", true},
	}

	for _, tt := range tests {
		t.Run(tt.pattern, func(t *testing.T) {
			got := matchLikePattern(tt.value, tt.pattern)
			if got != tt.want {
				t.Errorf("matchLikePattern(%q, %q) = %v, want %v", tt.value, tt.pattern, got, tt.want)
			}
		})
	}
}

func TestEntityMatches(t *testing.T) {
	h := &VerificationHarness{}

	entity := VerifyEntity{
		ID:            "ent-1",
		CanonicalName: "Tyler Adams",
		EntityTypeID:  1,
		EntityType:    "Person",
	}

	tests := []struct {
		name     string
		expected map[string]interface{}
		want     bool
	}{
		{
			name:     "exact name match",
			expected: map[string]interface{}{"name": "Tyler Adams"},
			want:     true,
		},
		{
			name:     "exact name no match",
			expected: map[string]interface{}{"name": "Casey Adams"},
			want:     false,
		},
		{
			name:     "name_contains match",
			expected: map[string]interface{}{"name_contains": "Tyler"},
			want:     true,
		},
		{
			name:     "name_contains case insensitive",
			expected: map[string]interface{}{"name_contains": "tyler"},
			want:     true,
		},
		{
			name:     "name_contains no match",
			expected: map[string]interface{}{"name_contains": "Casey"},
			want:     false,
		},
		{
			name:     "entity_type match",
			expected: map[string]interface{}{"entity_type": "Person"},
			want:     true,
		},
		{
			name:     "entity_type case insensitive",
			expected: map[string]interface{}{"entity_type": "person"},
			want:     true,
		},
		{
			name:     "entity_type any matches anything",
			expected: map[string]interface{}{"entity_type": "any"},
			want:     true,
		},
		{
			name:     "entity_type no match",
			expected: map[string]interface{}{"entity_type": "Company"},
			want:     false,
		},
		{
			name:     "combined match",
			expected: map[string]interface{}{"name_contains": "Tyler", "entity_type": "Person"},
			want:     true,
		},
		{
			name:     "combined partial match",
			expected: map[string]interface{}{"name_contains": "Tyler", "entity_type": "Company"},
			want:     false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := h.entityMatches(tt.expected, entity)
			if got != tt.want {
				t.Errorf("entityMatches() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestRelationshipMatches(t *testing.T) {
	h := &VerificationHarness{}

	validAt := "2023-01"
	targetName := "Anthropic"

	relationship := VerifyRelationship{
		ID:               "rel-1",
		SourceEntityID:   "ent-1",
		SourceEntityName: "Tyler Adams",
		RelationType:     "WORKS_AT",
		TargetEntityID:   verifyStrPtr("ent-2"),
		TargetEntityName: &targetName,
		ValidAt:          &validAt,
	}

	tests := []struct {
		name     string
		expected map[string]interface{}
		want     bool
	}{
		{
			name:     "relation_type match",
			expected: map[string]interface{}{"relation_type": "WORKS_AT"},
			want:     true,
		},
		{
			name:     "relation_type no match",
			expected: map[string]interface{}{"relation_type": "LIVES_IN"},
			want:     false,
		},
		{
			name:     "source_entity_name_contains match",
			expected: map[string]interface{}{"source_entity_name_contains": "Tyler"},
			want:     true,
		},
		{
			name:     "target_entity_name_contains match",
			expected: map[string]interface{}{"target_entity_name_contains": "Anthropic"},
			want:     true,
		},
		{
			name:     "target shorthand match",
			expected: map[string]interface{}{"target": "Anthropic"},
			want:     true,
		},
		{
			name:     "valid_at match",
			expected: map[string]interface{}{"valid_at": "2023-01"},
			want:     true,
		},
		{
			name:     "valid_at_like match",
			expected: map[string]interface{}{"valid_at_like": "2023%"},
			want:     true,
		},
		{
			name:     "valid_at_like no match",
			expected: map[string]interface{}{"valid_at_like": "2024%"},
			want:     false,
		},
		{
			name:     "combined match",
			expected: map[string]interface{}{"relation_type": "WORKS_AT", "target_entity_name_contains": "Anthropic"},
			want:     true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := h.relationshipMatches(tt.expected, relationship)
			if got != tt.want {
				t.Errorf("relationshipMatches() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestRelationshipMatchesLiteral(t *testing.T) {
	h := &VerificationHarness{}

	literal := "1990-08-15"
	relationship := VerifyRelationship{
		ID:               "rel-1",
		SourceEntityID:   "ent-1",
		SourceEntityName: "Tyler",
		RelationType:     "BORN_ON",
		TargetLiteral:    &literal,
	}

	tests := []struct {
		name     string
		expected map[string]interface{}
		want     bool
	}{
		{
			name:     "target_literal exact match",
			expected: map[string]interface{}{"target_literal": "1990-08-15"},
			want:     true,
		},
		{
			name:     "target_literal_like match",
			expected: map[string]interface{}{"target_literal_like": "1990-08%"},
			want:     true,
		},
		{
			name:     "target_literal_like no match",
			expected: map[string]interface{}{"target_literal_like": "1991%"},
			want:     false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := h.relationshipMatches(tt.expected, relationship)
			if got != tt.want {
				t.Errorf("relationshipMatches() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestAliasMatches(t *testing.T) {
	h := &VerificationHarness{}

	alias := VerifyAlias{
		ID:         "alias-1",
		EntityID:   "ent-1",
		EntityName: "Casey Adams",
		Alias:      "casey@example.com",
		AliasType:  "email",
		Normalized: "casey@example.com",
		IsShared:   false,
	}

	tests := []struct {
		name     string
		expected map[string]interface{}
		want     bool
	}{
		{
			name:     "entity_name_contains match",
			expected: map[string]interface{}{"entity_name_contains": "Casey"},
			want:     true,
		},
		{
			name:     "alias exact match",
			expected: map[string]interface{}{"alias": "casey@example.com"},
			want:     true,
		},
		{
			name:     "alias_type match",
			expected: map[string]interface{}{"alias_type": "email"},
			want:     true,
		},
		{
			name:     "is_shared match false",
			expected: map[string]interface{}{"is_shared": false},
			want:     true,
		},
		{
			name:     "is_shared no match",
			expected: map[string]interface{}{"is_shared": true},
			want:     false,
		},
		{
			name:     "combined match",
			expected: map[string]interface{}{"entity_name_contains": "Casey", "alias_type": "email"},
			want:     true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := h.aliasMatches(tt.expected, alias)
			if got != tt.want {
				t.Errorf("aliasMatches() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestRelMentionMatches(t *testing.T) {
	h := &VerificationHarness{}

	targetLiteral := "casey@example.com"
	mention := VerifyRelMention{
		ID:             "rm-1",
		EpisodeID:      "ep-1",
		RelationshipID: nil, // NULL for identity-only
		ExtractedFact:  "Casey shared their email address",
		SourceType:     "self_disclosed",
		TargetLiteral:  &targetLiteral,
	}

	tests := []struct {
		name     string
		expected map[string]interface{}
		want     bool
	}{
		{
			name:     "extracted_fact_contains match",
			expected: map[string]interface{}{"extracted_fact_contains": "email"},
			want:     true,
		},
		{
			name:     "source_type match",
			expected: map[string]interface{}{"source_type": "self_disclosed"},
			want:     true,
		},
		{
			name:     "target_literal match",
			expected: map[string]interface{}{"target_literal": "casey@example.com"},
			want:     true,
		},
		{
			name:     "relationship_id null match",
			expected: map[string]interface{}{"relationship_id": nil},
			want:     true,
		},
		{
			name:     "combined match",
			expected: map[string]interface{}{"source_type": "self_disclosed", "extracted_fact_contains": "email"},
			want:     true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := h.relMentionMatches(tt.expected, mention)
			if got != tt.want {
				t.Errorf("relMentionMatches() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestVerifyEntityExpectations(t *testing.T) {
	h := &VerificationHarness{}

	entities := []VerifyEntity{
		{ID: "ent-1", CanonicalName: "Tyler Adams", EntityTypeID: 1, EntityType: "Person"},
		{ID: "ent-2", CanonicalName: "Anthropic", EntityTypeID: 2, EntityType: "Company"},
	}

	t.Run("must_have passes when entity found", func(t *testing.T) {
		result := &VerificationResult{Passed: true}
		group := ExpectationGroup{
			MustHave: []map[string]interface{}{
				{"name_contains": "Tyler", "entity_type": "Person"},
			},
		}

		h.verifyEntityExpectations(result, group, entities)

		if !result.Passed {
			t.Errorf("Expected pass, got failures: %v", result.Failures)
		}
	})

	t.Run("must_have fails when entity not found", func(t *testing.T) {
		result := &VerificationResult{Passed: true}
		group := ExpectationGroup{
			MustHave: []map[string]interface{}{
				{"name_contains": "Casey", "entity_type": "Person"},
			},
		}

		h.verifyEntityExpectations(result, group, entities)

		if result.Passed {
			t.Errorf("Expected failure, but passed")
		}
		if len(result.Failures) == 0 {
			t.Errorf("Expected failure to be recorded")
		}
	})

	t.Run("must_not_have passes when entity not found", func(t *testing.T) {
		result := &VerificationResult{Passed: true}
		group := ExpectationGroup{
			MustNotHave: []map[string]interface{}{
				{"name_contains": "Claude", "entity_type": "any"},
			},
		}

		h.verifyEntityExpectations(result, group, entities)

		if !result.Passed {
			t.Errorf("Expected pass, got failures: %v", result.Failures)
		}
	})

	t.Run("must_not_have fails when forbidden entity found", func(t *testing.T) {
		result := &VerificationResult{Passed: true}
		group := ExpectationGroup{
			MustNotHave: []map[string]interface{}{
				{"name_contains": "Tyler", "entity_type": "Person"},
			},
		}

		h.verifyEntityExpectations(result, group, entities)

		if result.Passed {
			t.Errorf("Expected failure, but passed")
		}
	})
}

func TestCollectEntities(t *testing.T) {
	db := setupVerifyTestDB(t)
	defer db.Close()

	// Insert test data
	_, err := db.Exec(`
		INSERT INTO episodes (id, channel) VALUES ('ep-1', 'test');
		INSERT INTO entities (id, canonical_name, entity_type_id) VALUES
			('ent-1', 'Tyler', 1),
			('ent-2', 'Anthropic', 2),
			('ent-3', 'Merged Entity', 1);
		UPDATE entities SET merged_into = 'ent-1' WHERE id = 'ent-3';
		INSERT INTO episode_entity_mentions (episode_id, entity_id) VALUES
			('ep-1', 'ent-1'),
			('ep-1', 'ent-2'),
			('ep-1', 'ent-3');
	`)
	if err != nil {
		t.Fatalf("Failed to insert test data: %v", err)
	}

	h := &VerificationHarness{db: db}
	ctx := context.Background()

	entities, err := h.collectEntities(ctx, "ep-1")
	if err != nil {
		t.Fatalf("collectEntities failed: %v", err)
	}

	// Should only return 2 entities (merged entity excluded)
	if len(entities) != 2 {
		t.Errorf("Expected 2 entities, got %d", len(entities))
	}

	// Verify entity data
	foundTyler := false
	foundAnthropic := false
	for _, e := range entities {
		if e.CanonicalName == "Tyler" {
			foundTyler = true
			if e.EntityType != "Person" {
				t.Errorf("Expected Tyler to be Person, got %s", e.EntityType)
			}
		}
		if e.CanonicalName == "Anthropic" {
			foundAnthropic = true
			if e.EntityType != "Company" {
				t.Errorf("Expected Anthropic to be Company, got %s", e.EntityType)
			}
		}
	}

	if !foundTyler {
		t.Error("Tyler not found in entities")
	}
	if !foundAnthropic {
		t.Error("Anthropic not found in entities")
	}
}

func TestCollectRelationships(t *testing.T) {
	db := setupVerifyTestDB(t)
	defer db.Close()

	// Insert test data
	_, err := db.Exec(`
		INSERT INTO episodes (id, channel) VALUES ('ep-1', 'test');
		INSERT INTO entities (id, canonical_name, entity_type_id) VALUES
			('ent-1', 'Tyler', 1),
			('ent-2', 'Anthropic', 2);
		INSERT INTO relationships (id, source_entity_id, target_entity_id, relation_type, fact, valid_at)
			VALUES ('rel-1', 'ent-1', 'ent-2', 'WORKS_AT', 'Tyler works at Anthropic', '2023-01');
		INSERT INTO episode_relationship_mentions (id, episode_id, relationship_id, extracted_fact, source_type)
			VALUES ('rm-1', 'ep-1', 'rel-1', 'Tyler works at Anthropic', 'self_disclosed');
	`)
	if err != nil {
		t.Fatalf("Failed to insert test data: %v", err)
	}

	h := &VerificationHarness{db: db}
	ctx := context.Background()

	relationships, err := h.collectRelationships(ctx, "ep-1")
	if err != nil {
		t.Fatalf("collectRelationships failed: %v", err)
	}

	if len(relationships) != 1 {
		t.Fatalf("Expected 1 relationship, got %d", len(relationships))
	}

	rel := relationships[0]
	if rel.SourceEntityName != "Tyler" {
		t.Errorf("Expected source Tyler, got %s", rel.SourceEntityName)
	}
	if rel.RelationType != "WORKS_AT" {
		t.Errorf("Expected WORKS_AT, got %s", rel.RelationType)
	}
	if rel.TargetEntityName == nil || *rel.TargetEntityName != "Anthropic" {
		t.Errorf("Expected target Anthropic, got %v", rel.TargetEntityName)
	}
	if rel.ValidAt == nil || *rel.ValidAt != "2023-01" {
		t.Errorf("Expected valid_at 2023-01, got %v", rel.ValidAt)
	}
}

func TestCollectAliases(t *testing.T) {
	db := setupVerifyTestDB(t)
	defer db.Close()

	// Insert test data
	_, err := db.Exec(`
		INSERT INTO episodes (id, channel) VALUES ('ep-1', 'test');
		INSERT INTO entities (id, canonical_name, entity_type_id) VALUES ('ent-1', 'Casey', 1);
		INSERT INTO entity_aliases (id, entity_id, alias, alias_type, normalized, is_shared)
			VALUES ('alias-1', 'ent-1', 'casey@example.com', 'email', 'casey@example.com', 0);
		INSERT INTO episode_entity_mentions (episode_id, entity_id) VALUES ('ep-1', 'ent-1');
	`)
	if err != nil {
		t.Fatalf("Failed to insert test data: %v", err)
	}

	h := &VerificationHarness{db: db}
	ctx := context.Background()

	aliases, err := h.collectAliases(ctx, "ep-1")
	if err != nil {
		t.Fatalf("collectAliases failed: %v", err)
	}

	if len(aliases) != 1 {
		t.Fatalf("Expected 1 alias, got %d", len(aliases))
	}

	alias := aliases[0]
	if alias.EntityName != "Casey" {
		t.Errorf("Expected entity name Casey, got %s", alias.EntityName)
	}
	if alias.Alias != "casey@example.com" {
		t.Errorf("Expected alias casey@example.com, got %s", alias.Alias)
	}
	if alias.AliasType != "email" {
		t.Errorf("Expected alias_type email, got %s", alias.AliasType)
	}
}

func TestBuildEpisodeContent(t *testing.T) {
	h := &VerificationHarness{}

	episode := FixtureEpisode{
		ID:     "test-1",
		Source: "imessage",
		Events: []FixtureEvent{
			{ID: "e1", Sender: "Tyler", Content: "Hey, what's up?"},
			{ID: "e2", Sender: "Casey", Content: "Not much, you?"},
			{ID: "e3", Sender: "Tyler", Content: "Just working on the memory system"},
		},
	}

	content := h.buildEpisodeContent(episode)

	expected := "Tyler: Hey, what's up?\nCasey: Not much, you?\nTyler: Just working on the memory system"
	if content != expected {
		t.Errorf("buildEpisodeContent() = %q, want %q", content, expected)
	}
}

func TestLoadFixture(t *testing.T) {
	// Create a temporary fixture directory
	tmpDir, err := os.MkdirTemp("", "verify-test")
	if err != nil {
		t.Fatalf("Failed to create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpDir)

	// Create fixture structure
	fixtureDir := filepath.Join(tmpDir, "imessage", "test-fixture")
	if err := os.MkdirAll(fixtureDir, 0755); err != nil {
		t.Fatalf("Failed to create fixture dir: %v", err)
	}

	// Write episode.json
	episodeJSON := `{
		"id": "test-fixture-1",
		"source": "imessage",
		"channel": "imessage",
		"reference_time": "2026-01-22T10:00:00Z",
		"events": [
			{"id": "e1", "timestamp": "2026-01-22T10:00:00Z", "sender": "Tyler", "content": "Hello"}
		]
	}`
	if err := os.WriteFile(filepath.Join(fixtureDir, "episode.json"), []byte(episodeJSON), 0644); err != nil {
		t.Fatalf("Failed to write episode.json: %v", err)
	}

	// Write expectations.yaml
	expectationsYAML := `
description: "Test fixture"
entities:
  must_have:
    - name_contains: "Tyler"
      entity_type: Person
`
	if err := os.WriteFile(filepath.Join(fixtureDir, "expectations.yaml"), []byte(expectationsYAML), 0644); err != nil {
		t.Fatalf("Failed to write expectations.yaml: %v", err)
	}

	h := NewVerificationHarness(nil, tmpDir, nil)
	fixture, err := h.LoadFixture(fixtureDir)
	if err != nil {
		t.Fatalf("LoadFixture failed: %v", err)
	}

	if fixture.Name != "test-fixture" {
		t.Errorf("Expected name 'test-fixture', got %q", fixture.Name)
	}
	if fixture.Source != "imessage" {
		t.Errorf("Expected source 'imessage', got %q", fixture.Source)
	}
	if fixture.Episode.ID != "test-fixture-1" {
		t.Errorf("Expected episode ID 'test-fixture-1', got %q", fixture.Episode.ID)
	}
	if len(fixture.Episode.Events) != 1 {
		t.Errorf("Expected 1 event, got %d", len(fixture.Episode.Events))
	}
	if fixture.Expectations.Description != "Test fixture" {
		t.Errorf("Expected description 'Test fixture', got %q", fixture.Expectations.Description)
	}
	if len(fixture.Expectations.Entities.MustHave) != 1 {
		t.Errorf("Expected 1 must_have entity, got %d", len(fixture.Expectations.Entities.MustHave))
	}
}

func TestFormatResult(t *testing.T) {
	result := &VerificationResult{
		Fixture: &Fixture{
			Source: "imessage",
			Name:   "test-fixture",
		},
		Passed: false,
		Failures: []VerificationFailure{
			{
				Category:    "entities",
				Type:        "must_have",
				Expectation: map[string]interface{}{"name_contains": "Tyler"},
				Message:     "Expected entity not found",
			},
		},
	}

	output := FormatResult(result)

	if !contains(output, "[FAIL]") {
		t.Error("Expected [FAIL] in output")
	}
	if !contains(output, "imessage/test-fixture") {
		t.Error("Expected fixture path in output")
	}
	if !contains(output, "Expected entity not found") {
		t.Error("Expected failure message in output")
	}
}

func TestFormatSummary(t *testing.T) {
	results := []*VerificationResult{
		{
			Fixture: &Fixture{Source: "imessage", Name: "fixture-1"},
			Passed:  true,
		},
		{
			Fixture: &Fixture{Source: "imessage", Name: "fixture-2"},
			Passed:  false,
			Failures: []VerificationFailure{{Message: "test failure"}},
		},
	}

	output := FormatSummary(results)

	if !contains(output, "1 passed") {
		t.Error("Expected '1 passed' in output")
	}
	if !contains(output, "1 failed") {
		t.Error("Expected '1 failed' in output")
	}
	if !contains(output, "2 total") {
		t.Error("Expected '2 total' in output")
	}
}

// Helper function for tests - renamed to avoid collision with auto_merger_test.go
func verifyStrPtr(s string) *string {
	return &s
}
