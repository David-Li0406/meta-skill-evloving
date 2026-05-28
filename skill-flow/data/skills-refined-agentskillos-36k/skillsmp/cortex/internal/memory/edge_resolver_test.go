package memory

import (
	"context"
	"database/sql"
	"testing"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

// setupEdgeResolverTestDB creates a test database with required tables.
func setupEdgeResolverTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatalf("open db: %v", err)
	}

	// Create minimal schema for testing
	schema := `
		CREATE TABLE entities (
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

		CREATE TABLE episodes (
			id TEXT PRIMARY KEY,
			definition_id TEXT NOT NULL,
			channel TEXT,
			start_time INTEGER NOT NULL,
			end_time INTEGER NOT NULL,
			event_count INTEGER NOT NULL,
			created_at INTEGER NOT NULL
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
			confidence REAL DEFAULT 1.0,
			CHECK (
				(target_entity_id IS NOT NULL AND target_literal IS NULL) OR
				(target_entity_id IS NULL AND target_literal IS NOT NULL)
			)
		);

		CREATE TABLE episode_relationship_mentions (
			id TEXT PRIMARY KEY,
			episode_id TEXT NOT NULL REFERENCES episodes(id),
			relationship_id TEXT REFERENCES relationships(id),
			extracted_fact TEXT NOT NULL,
			asserted_by_entity_id TEXT,
			source_type TEXT,
			target_literal TEXT,
			alias_id TEXT,
			confidence REAL,
			created_at TEXT NOT NULL
		);
	`
	if _, err := db.Exec(schema); err != nil {
		t.Fatalf("create schema: %v", err)
	}

	return db
}

// insertEdgeResolverTestEntity inserts a test entity and returns its ID.
func insertEdgeResolverTestEntity(t *testing.T, db *sql.DB, id, name string, entityTypeID int) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO entities (id, canonical_name, entity_type_id, origin, created_at, updated_at)
		VALUES (?, ?, ?, 'extracted', ?, ?)
	`, id, name, entityTypeID, now, now)
	if err != nil {
		t.Fatalf("insert entity: %v", err)
	}
}

// insertEdgeResolverTestEpisode inserts a test episode.
func insertEdgeResolverTestEpisode(t *testing.T, db *sql.DB, id string) {
	now := time.Now().Unix()
	_, err := db.Exec(`
		INSERT INTO episodes (id, definition_id, start_time, end_time, event_count, created_at)
		VALUES (?, 'test-def', ?, ?, 1, ?)
	`, id, now, now, now)
	if err != nil {
		t.Fatalf("insert episode: %v", err)
	}
}

func TestEdgeResolver_NewRelationship(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEntity(t, db, "entity-anthropic", "Anthropic", EntityTypeCompany)
	insertEdgeResolverTestEpisode(t, db, "episode-1")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
		{ID: "entity-anthropic", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
	}

	targetID := 1
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Tyler works at Anthropic",
			SourceType:     "mentioned",
		},
	}

	result, err := resolver.Resolve(context.Background(), "episode-1", relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Resolve error: %v", err)
	}

	if result.NewRelationships != 1 {
		t.Errorf("NewRelationships = %d, want 1", result.NewRelationships)
	}
	if result.ExistingRelationships != 0 {
		t.Errorf("ExistingRelationships = %d, want 0", result.ExistingRelationships)
	}
	if result.MentionsCreated != 1 {
		t.Errorf("MentionsCreated = %d, want 1", result.MentionsCreated)
	}

	// Verify relationship was created
	var count int
	err = db.QueryRow(`SELECT COUNT(*) FROM relationships`).Scan(&count)
	if err != nil {
		t.Fatalf("count relationships: %v", err)
	}
	if count != 1 {
		t.Errorf("relationship count = %d, want 1", count)
	}

	// Verify mention was created
	err = db.QueryRow(`SELECT COUNT(*) FROM episode_relationship_mentions`).Scan(&count)
	if err != nil {
		t.Fatalf("count mentions: %v", err)
	}
	if count != 1 {
		t.Errorf("mention count = %d, want 1", count)
	}
}

func TestEdgeResolver_DuplicateRelationship_SingleRow(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEntity(t, db, "entity-anthropic", "Anthropic", EntityTypeCompany)
	insertEdgeResolverTestEpisode(t, db, "episode-1")
	insertEdgeResolverTestEpisode(t, db, "episode-2")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
		{ID: "entity-anthropic", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
	}

	targetID := 1
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Tyler works at Anthropic",
			SourceType:     "mentioned",
		},
	}

	// First extraction from episode-1
	result1, err := resolver.Resolve(context.Background(), "episode-1", relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Resolve 1 error: %v", err)
	}
	if result1.NewRelationships != 1 {
		t.Errorf("First extraction: NewRelationships = %d, want 1", result1.NewRelationships)
	}

	// Second extraction from episode-2 with same relationship
	result2, err := resolver.Resolve(context.Background(), "episode-2", relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Resolve 2 error: %v", err)
	}
	if result2.NewRelationships != 0 {
		t.Errorf("Second extraction: NewRelationships = %d, want 0", result2.NewRelationships)
	}
	if result2.ExistingRelationships != 1 {
		t.Errorf("Second extraction: ExistingRelationships = %d, want 1", result2.ExistingRelationships)
	}

	// Verify: 1 relationship row, 2 mentions
	var relCount, mentionCount int
	db.QueryRow(`SELECT COUNT(*) FROM relationships`).Scan(&relCount)
	db.QueryRow(`SELECT COUNT(*) FROM episode_relationship_mentions`).Scan(&mentionCount)

	if relCount != 1 {
		t.Errorf("relationship count = %d, want 1", relCount)
	}
	if mentionCount != 2 {
		t.Errorf("mention count = %d, want 2", mentionCount)
	}
}

func TestEdgeResolver_DifferentValidAt_DistinctRows(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEntity(t, db, "entity-anthropic", "Anthropic", EntityTypeCompany)
	insertEdgeResolverTestEpisode(t, db, "episode-1")
	insertEdgeResolverTestEpisode(t, db, "episode-2")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
		{ID: "entity-anthropic", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
	}

	targetID := 1
	validAt2024 := "2024-01"
	validAt2025 := "2025-01"

	// First job stint
	rel1 := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Tyler worked at Anthropic in 2024",
			SourceType:     "mentioned",
			ValidAt:        &validAt2024,
		},
	}

	// Second job stint (came back!)
	rel2 := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Tyler works at Anthropic again in 2025",
			SourceType:     "mentioned",
			ValidAt:        &validAt2025,
		},
	}

	result1, err := resolver.Resolve(context.Background(), "episode-1", rel1, resolvedEntities)
	if err != nil {
		t.Fatalf("Resolve 1 error: %v", err)
	}
	if result1.NewRelationships != 1 {
		t.Errorf("First stint: NewRelationships = %d, want 1", result1.NewRelationships)
	}

	result2, err := resolver.Resolve(context.Background(), "episode-2", rel2, resolvedEntities)
	if err != nil {
		t.Fatalf("Resolve 2 error: %v", err)
	}
	if result2.NewRelationships != 1 {
		t.Errorf("Second stint: NewRelationships = %d, want 1", result2.NewRelationships)
	}

	// Verify: 2 distinct relationship rows (different valid_at)
	var relCount int
	db.QueryRow(`SELECT COUNT(*) FROM relationships`).Scan(&relCount)

	if relCount != 2 {
		t.Errorf("relationship count = %d, want 2 (different valid_at should create distinct rows)", relCount)
	}
}

func TestEdgeResolver_TemporalRelationship_LiteralTarget(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEpisode(t, db, "episode-1")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
	}

	birthdate := "1990-05-15"
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "BORN_ON",
			TargetLiteral:  &birthdate,
			Fact:           "Tyler was born on May 15, 1990",
			SourceType:     "self_disclosed",
		},
	}

	result, err := resolver.Resolve(context.Background(), "episode-1", relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Resolve error: %v", err)
	}

	if result.NewRelationships != 1 {
		t.Errorf("NewRelationships = %d, want 1", result.NewRelationships)
	}

	// Verify relationship uses target_literal
	var targetEntityID *string
	var targetLiteral string
	err = db.QueryRow(`
		SELECT target_entity_id, target_literal FROM relationships
	`).Scan(&targetEntityID, &targetLiteral)
	if err != nil {
		t.Fatalf("query relationship: %v", err)
	}

	if targetEntityID != nil {
		t.Errorf("target_entity_id should be NULL for temporal relationships")
	}
	if targetLiteral != "1990-05-15" {
		t.Errorf("target_literal = %q, want %q", targetLiteral, "1990-05-15")
	}
}

func TestEdgeResolver_SkipsIdentityRelationships(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEpisode(t, db, "episode-1")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
	}

	email := "tyler@example.com"
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "HAS_EMAIL", // Identity relationship - should be skipped
			TargetLiteral:  &email,
			Fact:           "Tyler's email is tyler@example.com",
			SourceType:     "self_disclosed",
		},
	}

	result, err := resolver.Resolve(context.Background(), "episode-1", relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Resolve error: %v", err)
	}

	// Identity relationships should be skipped (handled by IdentityPromoter)
	if result.NewRelationships != 0 {
		t.Errorf("NewRelationships = %d, want 0 (identity relationships should be skipped)", result.NewRelationships)
	}
	if result.MentionsCreated != 0 {
		t.Errorf("MentionsCreated = %d, want 0 (identity relationships should be skipped)", result.MentionsCreated)
	}
}

func TestEdgeResolver_MentionIncludesSourceType(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEntity(t, db, "entity-anthropic", "Anthropic", EntityTypeCompany)
	insertEdgeResolverTestEpisode(t, db, "episode-1")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
		{ID: "entity-anthropic", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
	}

	targetID := 1
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Tyler works at Anthropic",
			SourceType:     "self_disclosed",
		},
	}

	_, err := resolver.Resolve(context.Background(), "episode-1", relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Resolve error: %v", err)
	}

	// Verify mention has correct source_type
	var sourceType string
	err = db.QueryRow(`SELECT source_type FROM episode_relationship_mentions`).Scan(&sourceType)
	if err != nil {
		t.Fatalf("query mention: %v", err)
	}

	if sourceType != "self_disclosed" {
		t.Errorf("source_type = %q, want %q", sourceType, "self_disclosed")
	}
}

func TestEdgeResolver_MentionIncludesExtractedFact(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEntity(t, db, "entity-anthropic", "Anthropic", EntityTypeCompany)
	insertEdgeResolverTestEpisode(t, db, "episode-1")
	insertEdgeResolverTestEpisode(t, db, "episode-2")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
		{ID: "entity-anthropic", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
	}

	targetID := 1

	// Same relationship, different phrasings
	rel1 := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Tyler is employed at Anthropic",
			SourceType:     "mentioned",
		},
	}

	rel2 := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Tyler works for Anthropic on AI safety",
			SourceType:     "mentioned",
		},
	}

	resolver.Resolve(context.Background(), "episode-1", rel1, resolvedEntities)
	resolver.Resolve(context.Background(), "episode-2", rel2, resolvedEntities)

	// Verify both phrasings are preserved in mentions
	rows, err := db.Query(`SELECT extracted_fact FROM episode_relationship_mentions ORDER BY created_at`)
	if err != nil {
		t.Fatalf("query mentions: %v", err)
	}
	defer rows.Close()

	var facts []string
	for rows.Next() {
		var fact string
		rows.Scan(&fact)
		facts = append(facts, fact)
	}

	if len(facts) != 2 {
		t.Fatalf("got %d facts, want 2", len(facts))
	}
	if facts[0] != "Tyler is employed at Anthropic" {
		t.Errorf("first fact = %q, want %q", facts[0], "Tyler is employed at Anthropic")
	}
	if facts[1] != "Tyler works for Anthropic on AI safety" {
		t.Errorf("second fact = %q, want %q", facts[1], "Tyler works for Anthropic on AI safety")
	}
}

func TestEdgeResolver_NullValidAt_MatchesCorrectly(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEntity(t, db, "entity-anthropic", "Anthropic", EntityTypeCompany)
	insertEdgeResolverTestEpisode(t, db, "episode-1")
	insertEdgeResolverTestEpisode(t, db, "episode-2")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
		{ID: "entity-anthropic", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
	}

	targetID := 1

	// Relationship with NULL valid_at
	rel := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Tyler works at Anthropic",
			SourceType:     "mentioned",
			ValidAt:        nil, // NULL valid_at
		},
	}

	// First insertion
	result1, _ := resolver.Resolve(context.Background(), "episode-1", rel, resolvedEntities)
	if result1.NewRelationships != 1 {
		t.Errorf("First: NewRelationships = %d, want 1", result1.NewRelationships)
	}

	// Second insertion should find existing (both have NULL valid_at)
	result2, _ := resolver.Resolve(context.Background(), "episode-2", rel, resolvedEntities)
	if result2.ExistingRelationships != 1 {
		t.Errorf("Second: ExistingRelationships = %d, want 1 (NULL valid_at should match)", result2.ExistingRelationships)
	}
	if result2.NewRelationships != 0 {
		t.Errorf("Second: NewRelationships = %d, want 0", result2.NewRelationships)
	}
}

func TestEdgeResolver_WithAssertedBy(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEntity(t, db, "entity-anthropic", "Anthropic", EntityTypeCompany)
	insertEdgeResolverTestEntity(t, db, "entity-casey", "Casey", EntityTypePerson)
	insertEdgeResolverTestEpisode(t, db, "episode-1")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
		{ID: "entity-anthropic", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
	}

	targetID := 1
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Tyler works at Anthropic",
			SourceType:     "mentioned", // Casey mentioned this about Tyler
		},
	}

	// Casey said this
	assertedBy := "entity-casey"
	_, err := resolver.ResolveWithAssertedBy(context.Background(), "episode-1", relationships, resolvedEntities, &assertedBy)
	if err != nil {
		t.Fatalf("ResolveWithAssertedBy error: %v", err)
	}

	// Verify asserted_by_entity_id is set
	var assertedByID *string
	err = db.QueryRow(`SELECT asserted_by_entity_id FROM episode_relationship_mentions`).Scan(&assertedByID)
	if err != nil {
		t.Fatalf("query mention: %v", err)
	}

	if assertedByID == nil || *assertedByID != "entity-casey" {
		t.Errorf("asserted_by_entity_id = %v, want %q", assertedByID, "entity-casey")
	}
}

func TestEdgeResolver_InvalidSourceEntity_Skipped(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEpisode(t, db, "episode-1")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
	}

	targetID := 1
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 99, // Invalid - out of range
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Invalid source",
			SourceType:     "mentioned",
		},
	}

	result, err := resolver.Resolve(context.Background(), "episode-1", relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Resolve error: %v", err)
	}

	// Invalid source should be skipped
	if result.NewRelationships != 0 {
		t.Errorf("NewRelationships = %d, want 0 (invalid source should be skipped)", result.NewRelationships)
	}
}

func TestEdgeResolver_InvalidTargetEntity_Skipped(t *testing.T) {
	db := setupEdgeResolverTestDB(t)
	defer db.Close()

	// Setup test data
	insertEdgeResolverTestEntity(t, db, "entity-tyler", "Tyler", EntityTypePerson)
	insertEdgeResolverTestEpisode(t, db, "episode-1")

	resolver := NewEdgeResolver(db)

	resolvedEntities := []ResolvedEntity{
		{ID: "entity-tyler", Name: "Tyler", EntityTypeID: EntityTypePerson},
	}

	invalidTargetID := 99 // Out of range
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &invalidTargetID,
			Fact:           "Invalid target",
			SourceType:     "mentioned",
		},
	}

	result, err := resolver.Resolve(context.Background(), "episode-1", relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Resolve error: %v", err)
	}

	// Invalid target should be skipped
	if result.NewRelationships != 0 {
		t.Errorf("NewRelationships = %d, want 0 (invalid target should be skipped)", result.NewRelationships)
	}
}
