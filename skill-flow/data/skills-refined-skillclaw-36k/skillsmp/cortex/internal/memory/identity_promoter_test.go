package memory

import (
	"context"
	"database/sql"
	"testing"
	"time"

	_ "modernc.org/sqlite"
)

// setupIdentityPromoterTestDB creates an in-memory SQLite database with the necessary schema.
func setupIdentityPromoterTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite", ":memory:")
	if err != nil {
		t.Fatalf("failed to open database: %v", err)
	}

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

		CREATE TABLE episodes (
			id TEXT PRIMARY KEY,
			definition_id TEXT,
			channel TEXT,
			thread_id TEXT,
			start_time INTEGER,
			end_time INTEGER,
			event_count INTEGER
		);

		CREATE TABLE episode_relationship_mentions (
			id TEXT PRIMARY KEY,
			episode_id TEXT NOT NULL REFERENCES episodes(id),
			relationship_id TEXT,
			extracted_fact TEXT NOT NULL,
			asserted_by_entity_id TEXT,
			source_type TEXT,
			target_literal TEXT,
			alias_id TEXT,
			confidence REAL,
			created_at TEXT NOT NULL
		);
	`
	_, err = db.Exec(schema)
	if err != nil {
		t.Fatalf("failed to create schema: %v", err)
	}

	return db
}

// insertIdentityTestEntity inserts an entity for testing.
func insertIdentityTestEntity(t *testing.T, db *sql.DB, id, name string, typeID int) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO entities (id, canonical_name, entity_type_id, origin, created_at, updated_at)
		VALUES (?, ?, ?, 'manual', ?, ?)
	`, id, name, typeID, now, now)
	if err != nil {
		t.Fatalf("failed to insert entity: %v", err)
	}
}

// insertIdentityTestEpisode inserts an episode for testing.
func insertIdentityTestEpisode(t *testing.T, db *sql.DB, id, channel string) {
	_, err := db.Exec(`
		INSERT INTO episodes (id, channel, event_count)
		VALUES (?, ?, 1)
	`, id, channel)
	if err != nil {
		t.Fatalf("failed to insert episode: %v", err)
	}
}

func TestIdentityPromoter_Promote_SelfDisclosedEmail(t *testing.T) {
	db := setupIdentityPromoterTestDB(t)
	defer db.Close()

	ctx := context.Background()
	promoter := NewIdentityPromoter(db)

	// Setup test data
	entityID := "entity-123"
	episodeID := "episode-456"
	insertIdentityTestEntity(t, db, entityID, "Tyler", 1)
	insertIdentityTestEpisode(t, db, episodeID, "test-channel")

	email := "tyler@example.com"
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0, // Maps to resolvedEntities[0]
			RelationType:   "HAS_EMAIL",
			TargetLiteral:  &email,
			Fact:           "Tyler's email is tyler@example.com",
			SourceType:     "self_disclosed",
		},
	}
	resolvedEntities := []ResolvedEntity{
		{ID: entityID, Name: "Tyler", EntityTypeID: 1},
	}

	result, err := promoter.Promote(ctx, episodeID, relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Promote: %v", err)
	}

	// Should have one promoted identity
	if len(result.PromotedIdentities) != 1 {
		t.Errorf("expected 1 promoted identity, got %d", len(result.PromotedIdentities))
	}

	// Should have no non-identity relationships
	if len(result.NonIdentityRels) != 0 {
		t.Errorf("expected 0 non-identity rels, got %d", len(result.NonIdentityRels))
	}

	// Verify the promoted identity
	promoted := result.PromotedIdentities[0]
	if promoted.SourceEntityID != entityID {
		t.Errorf("expected source entity %s, got %s", entityID, promoted.SourceEntityID)
	}
	if promoted.AliasType != "email" {
		t.Errorf("expected alias type 'email', got %s", promoted.AliasType)
	}
	if promoted.TargetLiteral != email {
		t.Errorf("expected target literal %s, got %s", email, promoted.TargetLiteral)
	}
	if promoted.AliasID == "" {
		t.Error("expected alias ID to be set")
	}

	// Verify alias was created in database
	var aliasCount int
	err = db.QueryRow(`SELECT COUNT(*) FROM entity_aliases WHERE entity_id = ? AND alias_type = 'email'`, entityID).Scan(&aliasCount)
	if err != nil {
		t.Fatalf("query alias count: %v", err)
	}
	if aliasCount != 1 {
		t.Errorf("expected 1 alias, got %d", aliasCount)
	}

	// Verify episode_relationship_mentions was created
	var mentionCount int
	err = db.QueryRow(`SELECT COUNT(*) FROM episode_relationship_mentions WHERE episode_id = ?`, episodeID).Scan(&mentionCount)
	if err != nil {
		t.Fatalf("query mention count: %v", err)
	}
	if mentionCount != 1 {
		t.Errorf("expected 1 mention, got %d", mentionCount)
	}

	// Verify mention has correct fields
	var mentionTargetLiteral, mentionSourceType string
	var mentionAliasID sql.NullString
	err = db.QueryRow(`
		SELECT target_literal, source_type, alias_id
		FROM episode_relationship_mentions
		WHERE episode_id = ?
	`, episodeID).Scan(&mentionTargetLiteral, &mentionSourceType, &mentionAliasID)
	if err != nil {
		t.Fatalf("query mention: %v", err)
	}
	if mentionTargetLiteral != email {
		t.Errorf("expected mention target_literal %s, got %s", email, mentionTargetLiteral)
	}
	if mentionSourceType != "self_disclosed" {
		t.Errorf("expected mention source_type 'self_disclosed', got %s", mentionSourceType)
	}
	if !mentionAliasID.Valid || mentionAliasID.String != promoted.AliasID {
		t.Errorf("expected mention alias_id %s, got %v", promoted.AliasID, mentionAliasID)
	}
}

func TestIdentityPromoter_Promote_MentionedSource_NoAlias(t *testing.T) {
	db := setupIdentityPromoterTestDB(t)
	defer db.Close()

	ctx := context.Background()
	promoter := NewIdentityPromoter(db)

	// Setup test data
	entityID := "entity-123"
	episodeID := "episode-456"
	insertIdentityTestEntity(t, db, entityID, "Tyler", 1)
	insertIdentityTestEpisode(t, db, episodeID, "test-channel")

	email := "tyler@example.com"
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "HAS_EMAIL",
			TargetLiteral:  &email,
			Fact:           "I heard Tyler's email is tyler@example.com",
			SourceType:     "mentioned", // Not self_disclosed
		},
	}
	resolvedEntities := []ResolvedEntity{
		{ID: entityID, Name: "Tyler", EntityTypeID: 1},
	}

	result, err := promoter.Promote(ctx, episodeID, relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Promote: %v", err)
	}

	// Should still have one promoted identity for tracking
	if len(result.PromotedIdentities) != 1 {
		t.Errorf("expected 1 promoted identity, got %d", len(result.PromotedIdentities))
	}

	// But alias should NOT be created (source_type != self_disclosed)
	var aliasCount int
	err = db.QueryRow(`SELECT COUNT(*) FROM entity_aliases WHERE entity_id = ?`, entityID).Scan(&aliasCount)
	if err != nil {
		t.Fatalf("query alias count: %v", err)
	}
	if aliasCount != 0 {
		t.Errorf("expected 0 aliases (non-self_disclosed), got %d", aliasCount)
	}

	// Alias ID should be empty for the promoted identity
	if result.PromotedIdentities[0].AliasID != "" {
		t.Errorf("expected empty alias ID for non-self_disclosed, got %s", result.PromotedIdentities[0].AliasID)
	}

	// But episode_relationship_mentions should still be created for provenance
	var mentionCount int
	err = db.QueryRow(`SELECT COUNT(*) FROM episode_relationship_mentions WHERE episode_id = ?`, episodeID).Scan(&mentionCount)
	if err != nil {
		t.Fatalf("query mention count: %v", err)
	}
	if mentionCount != 1 {
		t.Errorf("expected 1 mention for provenance, got %d", mentionCount)
	}
}

func TestIdentityPromoter_Promote_NonIdentityRelationship(t *testing.T) {
	db := setupIdentityPromoterTestDB(t)
	defer db.Close()

	ctx := context.Background()
	promoter := NewIdentityPromoter(db)

	// Setup test data
	entityID := "entity-123"
	companyID := "company-456"
	episodeID := "episode-789"
	insertIdentityTestEntity(t, db, entityID, "Tyler", 1)
	insertIdentityTestEntity(t, db, companyID, "Acme Corp", 2)
	insertIdentityTestEpisode(t, db, episodeID, "test-channel")

	targetID := 1 // Index for companyID
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "WORKS_AT",
			TargetEntityID: &targetID,
			Fact:           "Tyler works at Acme Corp",
			SourceType:     "self_disclosed",
		},
	}
	resolvedEntities := []ResolvedEntity{
		{ID: entityID, Name: "Tyler", EntityTypeID: 1},
		{ID: companyID, Name: "Acme Corp", EntityTypeID: 2},
	}

	result, err := promoter.Promote(ctx, episodeID, relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Promote: %v", err)
	}

	// Should have no promoted identities
	if len(result.PromotedIdentities) != 0 {
		t.Errorf("expected 0 promoted identities, got %d", len(result.PromotedIdentities))
	}

	// Should pass through the non-identity relationship
	if len(result.NonIdentityRels) != 1 {
		t.Errorf("expected 1 non-identity rel, got %d", len(result.NonIdentityRels))
	}

	// Verify no aliases created
	var aliasCount int
	err = db.QueryRow(`SELECT COUNT(*) FROM entity_aliases`).Scan(&aliasCount)
	if err != nil {
		t.Fatalf("query alias count: %v", err)
	}
	if aliasCount != 0 {
		t.Errorf("expected 0 aliases, got %d", aliasCount)
	}
}

func TestIdentityPromoter_Promote_SharedAlias(t *testing.T) {
	db := setupIdentityPromoterTestDB(t)
	defer db.Close()

	ctx := context.Background()
	promoter := NewIdentityPromoter(db)

	// Setup test data - two people (Dad and Mom) will share a phone number
	dadID := "entity-dad"
	momID := "entity-mom"
	episodeID := "episode-456"
	insertIdentityTestEntity(t, db, dadID, "Dad", 1)
	insertIdentityTestEntity(t, db, momID, "Mom", 1)
	insertIdentityTestEpisode(t, db, episodeID, "test-channel")

	phone := "555-1234"

	// First, Dad discloses the phone number
	relationships1 := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "HAS_PHONE",
			TargetLiteral:  &phone,
			Fact:           "Dad's phone number is 555-1234",
			SourceType:     "self_disclosed",
		},
	}
	resolvedEntities1 := []ResolvedEntity{
		{ID: dadID, Name: "Dad", EntityTypeID: 1},
	}

	result1, err := promoter.Promote(ctx, episodeID, relationships1, resolvedEntities1)
	if err != nil {
		t.Fatalf("Promote (Dad): %v", err)
	}

	// Dad's alias should NOT be shared yet
	if result1.PromotedIdentities[0].IsShared {
		t.Error("Dad's alias should not be shared yet")
	}

	// Now, Mom discloses the same phone number
	relationships2 := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "HAS_PHONE",
			TargetLiteral:  &phone,
			Fact:           "Mom's phone number is 555-1234",
			SourceType:     "self_disclosed",
		},
	}
	resolvedEntities2 := []ResolvedEntity{
		{ID: momID, Name: "Mom", EntityTypeID: 1},
	}

	result2, err := promoter.Promote(ctx, episodeID, relationships2, resolvedEntities2)
	if err != nil {
		t.Fatalf("Promote (Mom): %v", err)
	}

	// Mom's alias should be marked as shared
	if !result2.PromotedIdentities[0].IsShared {
		t.Error("Mom's alias should be marked as shared")
	}

	// Both aliases should now be marked as shared in the database
	var sharedCount int
	err = db.QueryRow(`SELECT COUNT(*) FROM entity_aliases WHERE is_shared = TRUE`).Scan(&sharedCount)
	if err != nil {
		t.Fatalf("query shared count: %v", err)
	}
	if sharedCount != 2 {
		t.Errorf("expected 2 shared aliases, got %d", sharedCount)
	}
}

func TestIdentityPromoter_Promote_DuplicateIdentity(t *testing.T) {
	db := setupIdentityPromoterTestDB(t)
	defer db.Close()

	ctx := context.Background()
	promoter := NewIdentityPromoter(db)

	// Setup test data
	entityID := "entity-123"
	episodeID1 := "episode-1"
	episodeID2 := "episode-2"
	insertIdentityTestEntity(t, db, entityID, "Tyler", 1)
	insertIdentityTestEpisode(t, db, episodeID1, "test-channel")
	insertIdentityTestEpisode(t, db, episodeID2, "test-channel")

	email := "tyler@example.com"
	relationships := []ExtractedRelationship{
		{
			SourceEntityID: 0,
			RelationType:   "HAS_EMAIL",
			TargetLiteral:  &email,
			Fact:           "Tyler's email is tyler@example.com",
			SourceType:     "self_disclosed",
		},
	}
	resolvedEntities := []ResolvedEntity{
		{ID: entityID, Name: "Tyler", EntityTypeID: 1},
	}

	// First promotion
	_, err := promoter.Promote(ctx, episodeID1, relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Promote (first): %v", err)
	}

	// Second promotion of same identity from different episode
	result2, err := promoter.Promote(ctx, episodeID2, relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Promote (second): %v", err)
	}

	// Should still have one promoted identity
	if len(result2.PromotedIdentities) != 1 {
		t.Errorf("expected 1 promoted identity, got %d", len(result2.PromotedIdentities))
	}

	// Should only have ONE alias (deduped)
	var aliasCount int
	err = db.QueryRow(`SELECT COUNT(*) FROM entity_aliases WHERE entity_id = ?`, entityID).Scan(&aliasCount)
	if err != nil {
		t.Fatalf("query alias count: %v", err)
	}
	if aliasCount != 1 {
		t.Errorf("expected 1 alias (deduplicated), got %d", aliasCount)
	}

	// Should have TWO mentions (provenance from each episode)
	var mentionCount int
	err = db.QueryRow(`SELECT COUNT(*) FROM episode_relationship_mentions`).Scan(&mentionCount)
	if err != nil {
		t.Fatalf("query mention count: %v", err)
	}
	if mentionCount != 2 {
		t.Errorf("expected 2 mentions, got %d", mentionCount)
	}
}

func TestIdentityPromoter_Promote_AllIdentityTypes(t *testing.T) {
	db := setupIdentityPromoterTestDB(t)
	defer db.Close()

	ctx := context.Background()
	promoter := NewIdentityPromoter(db)

	// Setup test data
	entityID := "entity-123"
	episodeID := "episode-456"
	insertIdentityTestEntity(t, db, entityID, "Tyler", 1)
	insertIdentityTestEpisode(t, db, episodeID, "test-channel")

	email := "tyler@example.com"
	phone := "+1-555-123-4567"
	handle := "@tnapathy"
	username := "tnapathy"
	nickname := "T"

	relationships := []ExtractedRelationship{
		{SourceEntityID: 0, RelationType: "HAS_EMAIL", TargetLiteral: &email, Fact: "email", SourceType: "self_disclosed"},
		{SourceEntityID: 0, RelationType: "HAS_PHONE", TargetLiteral: &phone, Fact: "phone", SourceType: "self_disclosed"},
		{SourceEntityID: 0, RelationType: "HAS_HANDLE", TargetLiteral: &handle, Fact: "handle", SourceType: "self_disclosed"},
		{SourceEntityID: 0, RelationType: "HAS_USERNAME", TargetLiteral: &username, Fact: "username", SourceType: "self_disclosed"},
		{SourceEntityID: 0, RelationType: "ALSO_KNOWN_AS", TargetLiteral: &nickname, Fact: "nickname", SourceType: "self_disclosed"},
	}
	resolvedEntities := []ResolvedEntity{
		{ID: entityID, Name: "Tyler", EntityTypeID: 1},
	}

	result, err := promoter.Promote(ctx, episodeID, relationships, resolvedEntities)
	if err != nil {
		t.Fatalf("Promote: %v", err)
	}

	// Should have all 5 promoted identities
	if len(result.PromotedIdentities) != 5 {
		t.Errorf("expected 5 promoted identities, got %d", len(result.PromotedIdentities))
	}

	// Verify all alias types were created
	expectedTypes := map[string]bool{"email": true, "phone": true, "handle": true, "username": true, "nickname": true}
	for _, promoted := range result.PromotedIdentities {
		if !expectedTypes[promoted.AliasType] {
			t.Errorf("unexpected alias type: %s", promoted.AliasType)
		}
		delete(expectedTypes, promoted.AliasType)
	}
	if len(expectedTypes) > 0 {
		t.Errorf("missing alias types: %v", expectedTypes)
	}

	// Verify all 5 aliases were created in database
	var aliasCount int
	err = db.QueryRow(`SELECT COUNT(*) FROM entity_aliases WHERE entity_id = ?`, entityID).Scan(&aliasCount)
	if err != nil {
		t.Fatalf("query alias count: %v", err)
	}
	if aliasCount != 5 {
		t.Errorf("expected 5 aliases, got %d", aliasCount)
	}
}

func TestNormalizeIdentityValue(t *testing.T) {
	tests := []struct {
		value     string
		aliasType string
		expected  string
	}{
		{"Tyler@Example.COM", "email", "tyler@example.com"},
		{"+1-555-123-4567", "phone", "+15551234567"},
		{"(555) 123-4567", "phone", "5551234567"},
		{"@TylerB", "handle", "@tylerb"},
		{"TylerB", "username", "tylerb"},
		{"  T-Man  ", "nickname", "t-man"},
	}

	for _, tt := range tests {
		t.Run(tt.aliasType+":"+tt.value, func(t *testing.T) {
			result := normalizeIdentityValue(tt.value, tt.aliasType)
			if result != tt.expected {
				t.Errorf("normalizeIdentityValue(%q, %q) = %q, want %q", tt.value, tt.aliasType, result, tt.expected)
			}
		})
	}
}

func TestIdentityPromoter_IsIdentityRelationType(t *testing.T) {
	identityTypes := []string{"HAS_EMAIL", "HAS_PHONE", "HAS_HANDLE", "HAS_USERNAME", "ALSO_KNOWN_AS"}
	nonIdentityTypes := []string{"WORKS_AT", "KNOWS", "BORN_ON", "LIVES_IN"}

	for _, relType := range identityTypes {
		if !IsIdentityRelationType(relType) {
			t.Errorf("expected %s to be identity type", relType)
		}
	}

	for _, relType := range nonIdentityTypes {
		if IsIdentityRelationType(relType) {
			t.Errorf("expected %s to NOT be identity type", relType)
		}
	}
}

func TestGetAliasTypeForRelation(t *testing.T) {
	tests := []struct {
		relType  string
		expected string
	}{
		{"HAS_EMAIL", "email"},
		{"HAS_PHONE", "phone"},
		{"HAS_HANDLE", "handle"},
		{"HAS_USERNAME", "username"},
		{"ALSO_KNOWN_AS", "nickname"},
		{"WORKS_AT", ""},
		{"KNOWS", ""},
	}

	for _, tt := range tests {
		t.Run(tt.relType, func(t *testing.T) {
			result := GetAliasTypeForRelation(tt.relType)
			if result != tt.expected {
				t.Errorf("GetAliasTypeForRelation(%q) = %q, want %q", tt.relType, result, tt.expected)
			}
		})
	}
}
