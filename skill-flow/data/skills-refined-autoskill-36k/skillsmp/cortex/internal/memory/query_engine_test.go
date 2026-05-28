package memory

import (
	"context"
	"database/sql"
	"testing"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

// setupQueryEngineTestDB creates a test database with required tables.
func setupQueryEngineTestDB(t *testing.T) *sql.DB {
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

		CREATE TABLE entity_aliases (
			id TEXT PRIMARY KEY,
			entity_id TEXT NOT NULL REFERENCES entities(id),
			alias TEXT NOT NULL,
			alias_type TEXT NOT NULL,
			normalized TEXT,
			is_shared BOOLEAN DEFAULT FALSE,
			created_at TEXT NOT NULL
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
	`
	if _, err := db.Exec(schema); err != nil {
		t.Fatalf("create schema: %v", err)
	}

	return db
}

// insertQueryEngineTestEntity inserts a test entity and returns its ID.
func insertQueryEngineTestEntity(t *testing.T, db *sql.DB, id, name string, entityTypeID int) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO entities (id, canonical_name, entity_type_id, origin, confidence, created_at, updated_at)
		VALUES (?, ?, ?, 'extracted', 1.0, ?, ?)
	`, id, name, entityTypeID, now, now)
	if err != nil {
		t.Fatalf("insert entity: %v", err)
	}
}

// insertQueryEngineTestRelationship inserts a test relationship.
func insertQueryEngineTestRelationship(t *testing.T, db *sql.DB, id, sourceID string, targetID *string, targetLiteral *string, relType, fact string, validAt, invalidAt *string) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO relationships (id, source_entity_id, target_entity_id, target_literal, relation_type, fact, valid_at, invalid_at, created_at, confidence)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1.0)
	`, id, sourceID, targetID, targetLiteral, relType, fact, validAt, invalidAt, now)
	if err != nil {
		t.Fatalf("insert relationship: %v", err)
	}
}

// insertQueryEngineTestAlias inserts a test alias.
func insertQueryEngineTestAlias(t *testing.T, db *sql.DB, id, entityID, alias, aliasType string, isShared bool) {
	now := time.Now().Format(time.RFC3339)
	normalized := normalizeAlias(alias)
	_, err := db.Exec(`
		INSERT INTO entity_aliases (id, entity_id, alias, alias_type, normalized, is_shared, created_at)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	`, id, entityID, alias, aliasType, normalized, isShared, now)
	if err != nil {
		t.Fatalf("insert alias: %v", err)
	}
}

func TestQueryEngine_GetRelatedEntities_Outgoing(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities: Tyler -> WORKS_AT -> Anthropic
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "anthropic-id", "Anthropic", EntityTypeCompany)

	// Create relationship
	anthropicID := "anthropic-id"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", &anthropicID, nil, "WORKS_AT", "Tyler works at Anthropic", nil, nil)

	// Query outgoing relationships from Tyler
	opts := DefaultQueryOptions()
	opts.Direction = DirectionOutgoing
	results, err := qe.GetRelatedEntities(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetRelatedEntities: %v", err)
	}

	if len(results) != 1 {
		t.Fatalf("expected 1 result, got %d", len(results))
	}

	if results[0].ID != "anthropic-id" {
		t.Errorf("expected anthropic-id, got %s", results[0].ID)
	}
	if results[0].CanonicalName != "Anthropic" {
		t.Errorf("expected Anthropic, got %s", results[0].CanonicalName)
	}
	if results[0].RelationType != "WORKS_AT" {
		t.Errorf("expected WORKS_AT, got %s", results[0].RelationType)
	}
	if results[0].Direction != "outgoing" {
		t.Errorf("expected outgoing, got %s", results[0].Direction)
	}
}

func TestQueryEngine_GetRelatedEntities_Incoming(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities: Tyler -> WORKS_AT -> Anthropic
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "anthropic-id", "Anthropic", EntityTypeCompany)

	// Create relationship
	anthropicID := "anthropic-id"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", &anthropicID, nil, "WORKS_AT", "Tyler works at Anthropic", nil, nil)

	// Query incoming relationships to Anthropic (who works there?)
	opts := DefaultQueryOptions()
	opts.Direction = DirectionIncoming
	results, err := qe.GetRelatedEntities(ctx, "anthropic-id", opts)
	if err != nil {
		t.Fatalf("GetRelatedEntities: %v", err)
	}

	if len(results) != 1 {
		t.Fatalf("expected 1 result, got %d", len(results))
	}

	if results[0].ID != "tyler-id" {
		t.Errorf("expected tyler-id, got %s", results[0].ID)
	}
	if results[0].Direction != "incoming" {
		t.Errorf("expected incoming, got %s", results[0].Direction)
	}
}

func TestQueryEngine_GetRelatedEntities_Bidirectional(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities: Tyler, Anthropic, Casey
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "anthropic-id", "Anthropic", EntityTypeCompany)
	insertQueryEngineTestEntity(t, db, "casey-id", "Casey", EntityTypePerson)

	// Tyler -> WORKS_AT -> Anthropic (outgoing from Tyler)
	anthropicID := "anthropic-id"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", &anthropicID, nil, "WORKS_AT", "Tyler works at Anthropic", nil, nil)

	// Casey -> KNOWS -> Tyler (incoming to Tyler)
	tylerID := "tyler-id"
	insertQueryEngineTestRelationship(t, db, "rel-2", "casey-id", &tylerID, nil, "KNOWS", "Casey knows Tyler", nil, nil)

	// Query both directions from Tyler
	opts := DefaultQueryOptions()
	opts.Direction = DirectionBoth
	results, err := qe.GetRelatedEntities(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetRelatedEntities: %v", err)
	}

	if len(results) != 2 {
		t.Fatalf("expected 2 results, got %d", len(results))
	}

	// Check we have both directions
	hasOutgoing := false
	hasIncoming := false
	for _, r := range results {
		if r.Direction == "outgoing" {
			hasOutgoing = true
		}
		if r.Direction == "incoming" {
			hasIncoming = true
		}
	}
	if !hasOutgoing || !hasIncoming {
		t.Errorf("expected both outgoing and incoming results")
	}
}

func TestQueryEngine_GetRelatedEntities_FilterByRelationType(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "anthropic-id", "Anthropic", EntityTypeCompany)
	insertQueryEngineTestEntity(t, db, "austin-id", "Austin", EntityTypeLocation)

	// Tyler -> WORKS_AT -> Anthropic
	anthropicID := "anthropic-id"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", &anthropicID, nil, "WORKS_AT", "Tyler works at Anthropic", nil, nil)

	// Tyler -> LIVES_IN -> Austin
	austinID := "austin-id"
	insertQueryEngineTestRelationship(t, db, "rel-2", "tyler-id", &austinID, nil, "LIVES_IN", "Tyler lives in Austin", nil, nil)

	// Query only WORKS_AT relationships
	opts := DefaultQueryOptions()
	opts.RelationTypes = []string{"WORKS_AT"}
	results, err := qe.GetRelatedEntities(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetRelatedEntities: %v", err)
	}

	if len(results) != 1 {
		t.Fatalf("expected 1 result, got %d", len(results))
	}

	if results[0].RelationType != "WORKS_AT" {
		t.Errorf("expected WORKS_AT, got %s", results[0].RelationType)
	}
}

func TestQueryEngine_GetRelatedEntities_TemporalFiltering(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "intent-id", "Intent Systems", EntityTypeCompany)
	insertQueryEngineTestEntity(t, db, "anthropic-id", "Anthropic", EntityTypeCompany)

	// Tyler -> WORKS_AT -> Intent Systems (invalidated - past job)
	intentID := "intent-id"
	validAtOld := "2020-01-01"
	invalidAt := "2025-12-01"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", &intentID, nil, "WORKS_AT", "Tyler works at Intent Systems", &validAtOld, &invalidAt)

	// Tyler -> WORKS_AT -> Anthropic (current job)
	anthropicID := "anthropic-id"
	validAtNew := "2026-01-01"
	insertQueryEngineTestRelationship(t, db, "rel-2", "tyler-id", &anthropicID, nil, "WORKS_AT", "Tyler works at Anthropic", &validAtNew, nil)

	// Query without invalidated - should only get current job
	opts := DefaultQueryOptions()
	opts.IncludeInvalidated = false
	results, err := qe.GetRelatedEntities(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetRelatedEntities: %v", err)
	}

	if len(results) != 1 {
		t.Fatalf("expected 1 result (current job only), got %d", len(results))
	}
	if results[0].ID != "anthropic-id" {
		t.Errorf("expected anthropic-id, got %s", results[0].ID)
	}

	// Query with invalidated - should get both jobs
	opts.IncludeInvalidated = true
	results, err = qe.GetRelatedEntities(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetRelatedEntities: %v", err)
	}

	if len(results) != 2 {
		t.Fatalf("expected 2 results (both jobs), got %d", len(results))
	}
}

func TestQueryEngine_GetRelatedEntities_ExcludesMergedEntities(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "casey-id", "Casey", EntityTypePerson)

	// Create relationship
	caseyID := "casey-id"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", &caseyID, nil, "KNOWS", "Tyler knows Casey", nil, nil)

	// Query should return Casey
	opts := DefaultQueryOptions()
	results, err := qe.GetRelatedEntities(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetRelatedEntities: %v", err)
	}
	if len(results) != 1 {
		t.Fatalf("expected 1 result, got %d", len(results))
	}

	// Now merge Casey into another entity
	now := time.Now().Format(time.RFC3339)
	_, err = db.Exec("UPDATE entities SET merged_into = ?, updated_at = ? WHERE id = ?", "some-other-id", now, "casey-id")
	if err != nil {
		t.Fatalf("update merged_into: %v", err)
	}

	// Query should return 0 results (Casey is merged)
	results, err = qe.GetRelatedEntities(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetRelatedEntities: %v", err)
	}
	if len(results) != 0 {
		t.Fatalf("expected 0 results (merged entity excluded), got %d", len(results))
	}
}

func TestQueryEngine_GetEntityRelationships_OutgoingWithLiteral(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)

	// Tyler -> BORN_ON -> 1990-05-15 (literal target)
	birthdate := "1990-05-15"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", nil, &birthdate, "BORN_ON", "Tyler was born on May 15, 1990", nil, nil)

	// Query outgoing relationships
	opts := DefaultQueryOptions()
	opts.Direction = DirectionOutgoing
	results, err := qe.GetEntityRelationships(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetEntityRelationships: %v", err)
	}

	if len(results) != 1 {
		t.Fatalf("expected 1 result, got %d", len(results))
	}

	if results[0].TargetLiteral == nil || *results[0].TargetLiteral != "1990-05-15" {
		t.Errorf("expected target_literal=1990-05-15, got %v", results[0].TargetLiteral)
	}
	if results[0].TargetEntityID != nil {
		t.Errorf("expected target_entity_id=nil, got %v", results[0].TargetEntityID)
	}
}

func TestQueryEngine_GetEntityRelationships_Bidirectional(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "anthropic-id", "Anthropic", EntityTypeCompany)
	insertQueryEngineTestEntity(t, db, "casey-id", "Casey", EntityTypePerson)

	// Outgoing: Tyler -> WORKS_AT -> Anthropic
	anthropicID := "anthropic-id"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", &anthropicID, nil, "WORKS_AT", "Tyler works at Anthropic", nil, nil)

	// Incoming: Casey -> KNOWS -> Tyler
	tylerID := "tyler-id"
	insertQueryEngineTestRelationship(t, db, "rel-2", "casey-id", &tylerID, nil, "KNOWS", "Casey knows Tyler", nil, nil)

	// Query all relationships for Tyler
	opts := DefaultQueryOptions()
	results, err := qe.GetEntityRelationships(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetEntityRelationships: %v", err)
	}

	if len(results) != 2 {
		t.Fatalf("expected 2 results, got %d", len(results))
	}

	// Check directions
	hasOutgoing := false
	hasIncoming := false
	for _, r := range results {
		if r.Direction == "outgoing" && r.RelationType == "WORKS_AT" {
			hasOutgoing = true
		}
		if r.Direction == "incoming" && r.RelationType == "KNOWS" {
			hasIncoming = true
		}
	}
	if !hasOutgoing || !hasIncoming {
		t.Errorf("expected both outgoing WORKS_AT and incoming KNOWS")
	}
}

func TestQueryEngine_GetEntity(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entity
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)

	// Query entity
	entity, err := qe.GetEntity(ctx, "tyler-id")
	if err != nil {
		t.Fatalf("GetEntity: %v", err)
	}

	if entity == nil {
		t.Fatal("expected entity, got nil")
	}
	if entity.CanonicalName != "Tyler" {
		t.Errorf("expected Tyler, got %s", entity.CanonicalName)
	}
	if entity.EntityTypeID != EntityTypePerson {
		t.Errorf("expected Person type, got %d", entity.EntityTypeID)
	}

	// Query non-existent entity
	entity, err = qe.GetEntity(ctx, "non-existent")
	if err != nil {
		t.Fatalf("GetEntity: %v", err)
	}
	if entity != nil {
		t.Errorf("expected nil for non-existent entity, got %+v", entity)
	}
}

func TestQueryEngine_FindEntitiesByName(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities
	insertQueryEngineTestEntity(t, db, "tyler-1", "Tyler Napathy", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "tyler-2", "Tyler Smith", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "casey-1", "Casey Jones", EntityTypePerson)

	// Search for Tyler
	results, err := qe.FindEntitiesByName(ctx, "Tyler", nil)
	if err != nil {
		t.Fatalf("FindEntitiesByName: %v", err)
	}

	if len(results) != 2 {
		t.Fatalf("expected 2 results, got %d", len(results))
	}

	// Search for specific type
	personType := EntityTypePerson
	results, err = qe.FindEntitiesByName(ctx, "Casey", &personType)
	if err != nil {
		t.Fatalf("FindEntitiesByName: %v", err)
	}

	if len(results) != 1 {
		t.Fatalf("expected 1 result, got %d", len(results))
	}
}

func TestQueryEngine_FindEntitiesByRelationType(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities
	insertQueryEngineTestEntity(t, db, "anthropic-id", "Anthropic", EntityTypeCompany)
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "casey-id", "Casey", EntityTypePerson)

	// Tyler -> WORKS_AT -> Anthropic
	anthropicID := "anthropic-id"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", &anthropicID, nil, "WORKS_AT", "Tyler works at Anthropic", nil, nil)

	// Casey -> WORKS_AT -> Anthropic
	insertQueryEngineTestRelationship(t, db, "rel-2", "casey-id", &anthropicID, nil, "WORKS_AT", "Casey works at Anthropic", nil, nil)

	// Query: "Who works at Anthropic?"
	opts := DefaultQueryOptions()
	results, err := qe.FindEntitiesByRelationType(ctx, "WORKS_AT", "anthropic-id", opts)
	if err != nil {
		t.Fatalf("FindEntitiesByRelationType: %v", err)
	}

	if len(results) != 2 {
		t.Fatalf("expected 2 results, got %d", len(results))
	}

	// Check we got Tyler and Casey
	names := make(map[string]bool)
	for _, r := range results {
		names[r.CanonicalName] = true
	}
	if !names["Tyler"] || !names["Casey"] {
		t.Errorf("expected Tyler and Casey, got %v", names)
	}
}

func TestQueryEngine_GetEntityAliases(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entity
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)

	// Create aliases
	insertQueryEngineTestAlias(t, db, "alias-1", "tyler-id", "tyler@example.com", "email", false)
	insertQueryEngineTestAlias(t, db, "alias-2", "tyler-id", "Tyler Napathy", "name", false)
	insertQueryEngineTestAlias(t, db, "alias-3", "tyler-id", "@tnapathy", "handle", false)

	// Query aliases
	aliases, err := qe.GetEntityAliases(ctx, "tyler-id")
	if err != nil {
		t.Fatalf("GetEntityAliases: %v", err)
	}

	if len(aliases) != 3 {
		t.Fatalf("expected 3 aliases, got %d", len(aliases))
	}
}

func TestQueryEngine_TemporalAsOfTime(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "intent-id", "Intent Systems", EntityTypeCompany)
	insertQueryEngineTestEntity(t, db, "anthropic-id", "Anthropic", EntityTypeCompany)

	// Tyler -> WORKS_AT -> Intent Systems (2020-01 to 2025-12)
	intentID := "intent-id"
	validAtOld := "2020-01-01"
	invalidAt := "2025-12-01"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", &intentID, nil, "WORKS_AT", "Tyler works at Intent Systems", &validAtOld, &invalidAt)

	// Tyler -> WORKS_AT -> Anthropic (2026-01 to current)
	anthropicID := "anthropic-id"
	validAtNew := "2026-01-01"
	insertQueryEngineTestRelationship(t, db, "rel-2", "tyler-id", &anthropicID, nil, "WORKS_AT", "Tyler works at Anthropic", &validAtNew, nil)

	// Query as of 2023 - should get Intent Systems
	asOf2023 := time.Date(2023, 6, 1, 0, 0, 0, 0, time.UTC)
	opts := QueryOptions{
		Direction:          DirectionBoth,
		AsOfTime:           &asOf2023,
		IncludeInvalidated: false,
	}
	results, err := qe.GetRelatedEntities(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetRelatedEntities: %v", err)
	}

	// At 2023, Intent Systems was valid (not yet invalidated at 2025-12)
	if len(results) != 1 {
		t.Fatalf("expected 1 result at 2023, got %d", len(results))
	}
	if results[0].ID != "intent-id" {
		t.Errorf("expected intent-id at 2023, got %s", results[0].ID)
	}
}

func TestQueryEngine_GetRelatedEntities_EmptyID(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	opts := DefaultQueryOptions()
	_, err := qe.GetRelatedEntities(ctx, "", opts)
	if err == nil {
		t.Fatal("expected error for empty entityID")
	}
}

func TestQueryEngine_Limit(t *testing.T) {
	db := setupQueryEngineTestDB(t)
	defer db.Close()

	ctx := context.Background()
	qe := NewQueryEngine(db)

	// Create entities
	insertQueryEngineTestEntity(t, db, "tyler-id", "Tyler", EntityTypePerson)
	insertQueryEngineTestEntity(t, db, "company-1", "Company1", EntityTypeCompany)
	insertQueryEngineTestEntity(t, db, "company-2", "Company2", EntityTypeCompany)
	insertQueryEngineTestEntity(t, db, "company-3", "Company3", EntityTypeCompany)

	// Create relationships
	c1 := "company-1"
	c2 := "company-2"
	c3 := "company-3"
	insertQueryEngineTestRelationship(t, db, "rel-1", "tyler-id", &c1, nil, "KNOWS_ABOUT", "Tyler knows about Company1", nil, nil)
	insertQueryEngineTestRelationship(t, db, "rel-2", "tyler-id", &c2, nil, "KNOWS_ABOUT", "Tyler knows about Company2", nil, nil)
	insertQueryEngineTestRelationship(t, db, "rel-3", "tyler-id", &c3, nil, "KNOWS_ABOUT", "Tyler knows about Company3", nil, nil)

	// Query with limit
	opts := DefaultQueryOptions()
	opts.Limit = 2
	results, err := qe.GetRelatedEntities(ctx, "tyler-id", opts)
	if err != nil {
		t.Fatalf("GetRelatedEntities: %v", err)
	}

	if len(results) != 2 {
		t.Errorf("expected 2 results with limit, got %d", len(results))
	}
}
