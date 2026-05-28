package memory

import (
	"context"
	"database/sql"
	"testing"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

// setupContradictionTestDB creates an in-memory SQLite database with the required schema
func setupContradictionTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatalf("Failed to open database: %v", err)
	}

	// Create minimal schema for testing (simplified - no CHECK constraint)
	schema := `
		CREATE TABLE entities (
			id TEXT PRIMARY KEY,
			canonical_name TEXT NOT NULL,
			entity_type_id INTEGER DEFAULT 0,
			summary TEXT,
			summary_updated_at TEXT,
			origin TEXT,
			confidence REAL DEFAULT 1.0,
			merged_into TEXT,
			created_at TEXT NOT NULL,
			updated_at TEXT NOT NULL
		);

		CREATE TABLE relationships (
			id TEXT PRIMARY KEY,
			source_entity_id TEXT NOT NULL,
			target_entity_id TEXT,
			target_literal TEXT,
			relation_type TEXT NOT NULL,
			fact TEXT,
			valid_at TEXT,
			invalid_at TEXT,
			created_at TEXT NOT NULL,
			confidence REAL DEFAULT 1.0
		);
	`

	if _, err := db.Exec(schema); err != nil {
		t.Fatalf("Failed to create schema: %v", err)
	}

	return db
}

// Helper to insert test entities
func insertContradictionTestEntity(t *testing.T, db *sql.DB, id, name string, typeID int) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO entities (id, canonical_name, entity_type_id, created_at, updated_at)
		VALUES (?, ?, ?, ?, ?)
	`, id, name, typeID, now, now)
	if err != nil {
		t.Fatalf("Failed to insert entity: %v", err)
	}
}

// Helper to insert test relationships with entity target
func insertContradictionTestRelWithEntity(t *testing.T, db *sql.DB, id, sourceID, targetID, relType string, validAt, invalidAt *string) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO relationships (id, source_entity_id, target_entity_id, relation_type, fact, valid_at, invalid_at, created_at)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)
	`, id, sourceID, targetID, relType, "Test fact", validAt, invalidAt, now)
	if err != nil {
		t.Fatalf("Failed to insert relationship: %v", err)
	}
}

// Helper to insert test relationships with literal target
func insertContradictionTestRelWithLiteral(t *testing.T, db *sql.DB, id, sourceID, targetLiteral, relType string, validAt, invalidAt *string) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO relationships (id, source_entity_id, target_literal, relation_type, fact, valid_at, invalid_at, created_at)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)
	`, id, sourceID, targetLiteral, relType, "Test fact", validAt, invalidAt, now)
	if err != nil {
		t.Fatalf("Failed to insert relationship: %v", err)
	}
}

// Helper to get relationship's invalid_at value
func getRelationshipInvalidAt(t *testing.T, db *sql.DB, id string) *string {
	var invalidAt sql.NullString
	err := db.QueryRow("SELECT invalid_at FROM relationships WHERE id = ?", id).Scan(&invalidAt)
	if err != nil {
		t.Fatalf("Failed to get relationship: %v", err)
	}
	if !invalidAt.Valid {
		return nil
	}
	return &invalidAt.String
}

func TestContradictionDetector_NewDetector(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	if detector == nil {
		t.Fatal("NewContradictionDetector returned nil")
	}
	if detector.db != db {
		t.Error("Expected db to be set")
	}
}

func TestContradictionDetector_NoContradictionForNonExclusiveTypes(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "person-2", "Casey", EntityTypePerson)
	insertContradictionTestEntity(t, db, "person-3", "Alex", EntityTypePerson)

	// Create first KNOWS relationship
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "person-2", "KNOWS", nil, nil)

	// Create second KNOWS relationship (to different person) - should NOT contradict
	insertContradictionTestRelWithEntity(t, db, "rel-2", "person-1", "person-3", "KNOWS", nil, nil)

	// Detect contradictions
	result, err := detector.Detect(ctx, []string{"rel-2"}, time.Now())
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	if result.ContradictionsFound != 0 {
		t.Errorf("Expected 0 contradictions, got %d", result.ContradictionsFound)
	}

	// First relationship should still be valid (invalid_at = NULL)
	invalidAt := getRelationshipInvalidAt(t, db, "rel-1")
	if invalidAt != nil {
		t.Errorf("Expected rel-1 to remain valid, but invalid_at = %s", *invalidAt)
	}
}

func TestContradictionDetector_ContradictionForWorksAt(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "company-1", "Intent Systems", EntityTypeCompany)
	insertContradictionTestEntity(t, db, "company-2", "Anthropic", EntityTypeCompany)

	// Tyler works at Intent Systems
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "company-1", "WORKS_AT", nil, nil)

	// Tyler now works at Anthropic - should contradict
	insertContradictionTestRelWithEntity(t, db, "rel-2", "person-1", "company-2", "WORKS_AT", nil, nil)

	invalidationTime := time.Now()
	result, err := detector.Detect(ctx, []string{"rel-2"}, invalidationTime)
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	if result.ContradictionsFound != 1 {
		t.Errorf("Expected 1 contradiction, got %d", result.ContradictionsFound)
	}

	// First relationship should be invalidated
	invalidAt := getRelationshipInvalidAt(t, db, "rel-1")
	if invalidAt == nil {
		t.Error("Expected rel-1 to be invalidated, but invalid_at is NULL")
	}

	// Second relationship should remain valid
	invalidAt = getRelationshipInvalidAt(t, db, "rel-2")
	if invalidAt != nil {
		t.Errorf("Expected rel-2 to remain valid, but invalid_at = %s", *invalidAt)
	}
}

func TestContradictionDetector_ContradictionForLivesIn(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "location-1", "Austin", EntityTypeLocation)
	insertContradictionTestEntity(t, db, "location-2", "San Francisco", EntityTypeLocation)

	// Tyler lives in Austin
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "location-1", "LIVES_IN", nil, nil)

	// Tyler now lives in San Francisco - should contradict
	insertContradictionTestRelWithEntity(t, db, "rel-2", "person-1", "location-2", "LIVES_IN", nil, nil)

	result, err := detector.Detect(ctx, []string{"rel-2"}, time.Now())
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	if result.ContradictionsFound != 1 {
		t.Errorf("Expected 1 contradiction, got %d", result.ContradictionsFound)
	}

	// First relationship should be invalidated
	invalidAt := getRelationshipInvalidAt(t, db, "rel-1")
	if invalidAt == nil {
		t.Error("Expected rel-1 to be invalidated")
	}
}

func TestContradictionDetector_UsesValidAtAsInvalidAt(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "company-1", "Intent", EntityTypeCompany)
	insertContradictionTestEntity(t, db, "company-2", "Anthropic", EntityTypeCompany)

	// Tyler worked at Intent (no specific valid_at)
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "company-1", "WORKS_AT", nil, nil)

	// Tyler works at Anthropic starting 2026-01
	validAt := "2026-01"
	insertContradictionTestRelWithEntity(t, db, "rel-2", "person-1", "company-2", "WORKS_AT", &validAt, nil)

	result, err := detector.Detect(ctx, []string{"rel-2"}, time.Now())
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	if result.ContradictionsFound != 1 {
		t.Errorf("Expected 1 contradiction, got %d", result.ContradictionsFound)
	}

	// First relationship should have invalid_at = "2026-01" (from new relationship's valid_at)
	invalidAt := getRelationshipInvalidAt(t, db, "rel-1")
	if invalidAt == nil {
		t.Error("Expected rel-1 to be invalidated")
	} else if *invalidAt != "2026-01" {
		t.Errorf("Expected invalid_at = '2026-01', got '%s'", *invalidAt)
	}
}

func TestContradictionDetector_UsesFallbackTimeWhenNoValidAt(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "company-1", "Intent", EntityTypeCompany)
	insertContradictionTestEntity(t, db, "company-2", "Anthropic", EntityTypeCompany)

	// Tyler worked at Intent
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "company-1", "WORKS_AT", nil, nil)

	// Tyler works at Anthropic (no explicit valid_at)
	insertContradictionTestRelWithEntity(t, db, "rel-2", "person-1", "company-2", "WORKS_AT", nil, nil)

	invalidationTime := time.Date(2026, 1, 21, 10, 30, 0, 0, time.UTC)
	result, err := detector.Detect(ctx, []string{"rel-2"}, invalidationTime)
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	if result.ContradictionsFound != 1 {
		t.Errorf("Expected 1 contradiction, got %d", result.ContradictionsFound)
	}

	// First relationship should have invalid_at from fallback time
	invalidAt := getRelationshipInvalidAt(t, db, "rel-1")
	if invalidAt == nil {
		t.Error("Expected rel-1 to be invalidated")
	} else {
		expected := invalidationTime.Format(time.RFC3339)
		if *invalidAt != expected {
			t.Errorf("Expected invalid_at = '%s', got '%s'", expected, *invalidAt)
		}
	}
}

func TestContradictionDetector_DoesNotInvalidateAlreadyInvalidated(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "company-1", "Google", EntityTypeCompany)
	insertContradictionTestEntity(t, db, "company-2", "Intent", EntityTypeCompany)
	insertContradictionTestEntity(t, db, "company-3", "Anthropic", EntityTypeCompany)

	// Tyler worked at Google (already invalidated)
	existingInvalidAt := "2020-01"
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "company-1", "WORKS_AT", nil, &existingInvalidAt)

	// Tyler worked at Intent (current)
	insertContradictionTestRelWithEntity(t, db, "rel-2", "person-1", "company-2", "WORKS_AT", nil, nil)

	// Tyler now works at Anthropic
	insertContradictionTestRelWithEntity(t, db, "rel-3", "person-1", "company-3", "WORKS_AT", nil, nil)

	result, err := detector.Detect(ctx, []string{"rel-3"}, time.Now())
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	// Should only invalidate rel-2, not rel-1 (which is already invalidated)
	if result.ContradictionsFound != 1 {
		t.Errorf("Expected 1 contradiction, got %d", result.ContradictionsFound)
	}

	// rel-1 should still have original invalid_at
	invalidAt := getRelationshipInvalidAt(t, db, "rel-1")
	if invalidAt == nil || *invalidAt != "2020-01" {
		t.Errorf("Expected rel-1 to keep original invalid_at='2020-01', got %v", invalidAt)
	}

	// rel-2 should be invalidated
	invalidAt = getRelationshipInvalidAt(t, db, "rel-2")
	if invalidAt == nil {
		t.Error("Expected rel-2 to be invalidated")
	}
}

func TestContradictionDetector_SameTargetNoContradiction(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "company-1", "Anthropic", EntityTypeCompany)

	// Tyler works at Anthropic
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "company-1", "WORKS_AT", nil, nil)

	// Another mention of Tyler working at Anthropic (same target)
	insertContradictionTestRelWithEntity(t, db, "rel-2", "person-1", "company-1", "WORKS_AT", nil, nil)

	result, err := detector.Detect(ctx, []string{"rel-2"}, time.Now())
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	// No contradiction - same target
	if result.ContradictionsFound != 0 {
		t.Errorf("Expected 0 contradictions, got %d", result.ContradictionsFound)
	}

	// First relationship should remain valid
	invalidAt := getRelationshipInvalidAt(t, db, "rel-1")
	if invalidAt != nil {
		t.Errorf("Expected rel-1 to remain valid, but invalid_at = %s", *invalidAt)
	}
}

func TestContradictionDetector_MultipleContradictions(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "company-1", "Google", EntityTypeCompany)
	insertContradictionTestEntity(t, db, "company-2", "Meta", EntityTypeCompany)
	insertContradictionTestEntity(t, db, "location-1", "Austin", EntityTypeLocation)
	insertContradictionTestEntity(t, db, "location-2", "SF", EntityTypeLocation)
	insertContradictionTestEntity(t, db, "company-3", "Anthropic", EntityTypeCompany)

	// Tyler works at Google (to be contradicted)
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "company-1", "WORKS_AT", nil, nil)

	// Tyler also works at Meta (to be contradicted - should this be possible? Yes for testing)
	insertContradictionTestRelWithEntity(t, db, "rel-2", "person-1", "company-2", "WORKS_AT", nil, nil)

	// Tyler lives in Austin (to be contradicted)
	insertContradictionTestRelWithEntity(t, db, "rel-3", "person-1", "location-1", "LIVES_IN", nil, nil)

	// Tyler now works at Anthropic
	insertContradictionTestRelWithEntity(t, db, "rel-4", "person-1", "company-3", "WORKS_AT", nil, nil)

	// Tyler now lives in SF
	insertContradictionTestRelWithEntity(t, db, "rel-5", "person-1", "location-2", "LIVES_IN", nil, nil)

	result, err := detector.Detect(ctx, []string{"rel-4", "rel-5"}, time.Now())
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	// Should find 3 contradictions: rel-1, rel-2 (WORKS_AT), rel-3 (LIVES_IN)
	if result.ContradictionsFound != 3 {
		t.Errorf("Expected 3 contradictions, got %d", result.ContradictionsFound)
	}
}

func TestContradictionDetector_DifferentSourceEntities(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "person-2", "Casey", EntityTypePerson)
	insertContradictionTestEntity(t, db, "company-1", "Anthropic", EntityTypeCompany)
	insertContradictionTestEntity(t, db, "company-2", "Google", EntityTypeCompany)

	// Tyler works at Anthropic
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "company-1", "WORKS_AT", nil, nil)

	// Casey works at Google - different source entity, should NOT contradict Tyler's relationship
	insertContradictionTestRelWithEntity(t, db, "rel-2", "person-2", "company-2", "WORKS_AT", nil, nil)

	result, err := detector.Detect(ctx, []string{"rel-2"}, time.Now())
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	if result.ContradictionsFound != 0 {
		t.Errorf("Expected 0 contradictions, got %d", result.ContradictionsFound)
	}

	// Tyler's relationship should remain valid
	invalidAt := getRelationshipInvalidAt(t, db, "rel-1")
	if invalidAt != nil {
		t.Errorf("Expected rel-1 to remain valid, but invalid_at = %s", *invalidAt)
	}
}

func TestContradictionDetector_SpouseOfContradiction(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "person-2", "Alex", EntityTypePerson)
	insertContradictionTestEntity(t, db, "person-3", "Casey", EntityTypePerson)

	// Tyler is spouse of Alex
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "person-2", "SPOUSE_OF", nil, nil)

	// Tyler is now spouse of Casey - contradicts previous marriage
	insertContradictionTestRelWithEntity(t, db, "rel-2", "person-1", "person-3", "SPOUSE_OF", nil, nil)

	result, err := detector.Detect(ctx, []string{"rel-2"}, time.Now())
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	if result.ContradictionsFound != 1 {
		t.Errorf("Expected 1 contradiction, got %d", result.ContradictionsFound)
	}

	// First relationship should be invalidated
	invalidAt := getRelationshipInvalidAt(t, db, "rel-1")
	if invalidAt == nil {
		t.Error("Expected rel-1 to be invalidated")
	}
}

func TestContradictionDetector_GetContradictingRelationships(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Create entities
	insertContradictionTestEntity(t, db, "person-1", "Tyler", EntityTypePerson)
	insertContradictionTestEntity(t, db, "company-1", "Intent", EntityTypeCompany)
	insertContradictionTestEntity(t, db, "company-2", "Anthropic", EntityTypeCompany)

	// Tyler works at Intent
	insertContradictionTestRelWithEntity(t, db, "rel-1", "person-1", "company-1", "WORKS_AT", nil, nil)

	// Check what would be contradicted by Tyler working at Anthropic
	targetID := "company-2"
	contradicting, err := detector.GetContradictingRelationships(ctx, "person-1", "WORKS_AT", &targetID, nil)
	if err != nil {
		t.Fatalf("GetContradictingRelationships failed: %v", err)
	}

	if len(contradicting) != 1 {
		t.Errorf("Expected 1 contradicting relationship, got %d", len(contradicting))
	}
	if len(contradicting) > 0 && contradicting[0] != "rel-1" {
		t.Errorf("Expected rel-1, got %s", contradicting[0])
	}
}

func TestIsExclusiveRelationType(t *testing.T) {
	exclusiveTypes := []string{"WORKS_AT", "LIVES_IN", "SPOUSE_OF", "MARRIED_TO", "DATING"}
	for _, relType := range exclusiveTypes {
		if !IsExclusiveRelationType(relType) {
			t.Errorf("Expected %s to be exclusive", relType)
		}
	}

	nonExclusiveTypes := []string{"KNOWS", "FRIEND_OF", "PARENT_OF", "ATTENDED", "CREATED", "HAS_EMAIL"}
	for _, relType := range nonExclusiveTypes {
		if IsExclusiveRelationType(relType) {
			t.Errorf("Expected %s to NOT be exclusive", relType)
		}
	}
}

func TestContradictionDetector_NonexistentRelationship(t *testing.T) {
	db := setupContradictionTestDB(t)
	defer db.Close()

	detector := NewContradictionDetector(db)
	ctx := context.Background()

	// Detect contradictions for a relationship that doesn't exist
	result, err := detector.Detect(ctx, []string{"nonexistent-rel"}, time.Now())
	if err != nil {
		t.Fatalf("Detect failed: %v", err)
	}

	if result.ContradictionsFound != 0 {
		t.Errorf("Expected 0 contradictions, got %d", result.ContradictionsFound)
	}
}
