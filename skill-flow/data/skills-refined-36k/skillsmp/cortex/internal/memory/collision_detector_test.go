package memory

import (
	"context"
	"database/sql"
	"testing"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

// setupCollisionTestDB creates an in-memory SQLite database with the required schema
func setupCollisionTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatalf("Failed to open database: %v", err)
	}

	// Create minimal schema for testing
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

		CREATE TABLE entity_aliases (
			id TEXT PRIMARY KEY,
			entity_id TEXT NOT NULL,
			alias TEXT NOT NULL,
			alias_type TEXT NOT NULL,
			normalized TEXT,
			is_shared BOOLEAN DEFAULT FALSE,
			created_at TEXT NOT NULL
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

		CREATE TABLE merge_candidates (
			id TEXT PRIMARY KEY,
			entity_a_id TEXT NOT NULL,
			entity_b_id TEXT NOT NULL,
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

	if _, err := db.Exec(schema); err != nil {
		t.Fatalf("Failed to create schema: %v", err)
	}

	return db
}

// Helper to insert test entities
func insertCollisionTestEntity(t *testing.T, db *sql.DB, id, name string, typeID int) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO entities (id, canonical_name, entity_type_id, created_at, updated_at)
		VALUES (?, ?, ?, ?, ?)
	`, id, name, typeID, now, now)
	if err != nil {
		t.Fatalf("Failed to insert entity: %v", err)
	}
}

// Helper to insert test aliases
func insertCollisionTestAlias(t *testing.T, db *sql.DB, id, entityID, alias, aliasType, normalized string, isShared bool) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO entity_aliases (id, entity_id, alias, alias_type, normalized, is_shared, created_at)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	`, id, entityID, alias, aliasType, normalized, isShared, now)
	if err != nil {
		t.Fatalf("Failed to insert alias: %v", err)
	}
}

// Helper to insert test relationships with entity target
func insertCollisionTestRelWithEntity(t *testing.T, db *sql.DB, id, sourceID, targetID, relType string) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO relationships (id, source_entity_id, target_entity_id, relation_type, fact, created_at)
		VALUES (?, ?, ?, ?, ?, ?)
	`, id, sourceID, targetID, relType, "Test fact", now)
	if err != nil {
		t.Fatalf("Failed to insert relationship: %v", err)
	}
}

// Helper to insert test relationships with literal target
func insertCollisionTestRelWithLiteral(t *testing.T, db *sql.DB, id, sourceID, targetLiteral, relType string) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO relationships (id, source_entity_id, target_literal, relation_type, fact, created_at)
		VALUES (?, ?, ?, ?, ?, ?)
	`, id, sourceID, targetLiteral, relType, "Test fact", now)
	if err != nil {
		t.Fatalf("Failed to insert relationship: %v", err)
	}
}

func TestCollisionDetector_HardIdentifierCollision_Email(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create two entities with the same email
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "J. Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "john@example.com", "email", "john@example.com", false)

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	if len(result.Collisions) != 1 {
		t.Errorf("Expected 1 collision, got %d", len(result.Collisions))
	}

	c := result.Collisions[0]
	if c.Confidence != HardIdentifierConfidence {
		t.Errorf("Expected confidence %f, got %f", HardIdentifierConfidence, c.Confidence)
	}
	if c.Reason != ReasonHardIdentifier {
		t.Errorf("Expected reason %s, got %s", ReasonHardIdentifier, c.Reason)
	}
	if !c.AutoEligible {
		t.Error("Expected auto_eligible to be true for hard identifier match")
	}
}

func TestCollisionDetector_HardIdentifierCollision_Phone(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create two entities with the same phone
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "Johnny Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "+1-555-123-4567", "phone", "+15551234567", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "+15551234567", "phone", "+15551234567", false)

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	if len(result.Collisions) != 1 {
		t.Errorf("Expected 1 collision, got %d", len(result.Collisions))
	}

	if result.Collisions[0].Reason != ReasonHardIdentifier {
		t.Errorf("Expected reason %s, got %s", ReasonHardIdentifier, result.Collisions[0].Reason)
	}
}

func TestCollisionDetector_SharedAliasNoCollision(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create two entities with the same phone, but marked as shared (family phone)
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "Jane Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "+1-555-123-4567", "phone", "+15551234567", true)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "+15551234567", "phone", "+15551234567", true)

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	// Shared aliases should NOT trigger collisions
	if len(result.Collisions) != 0 {
		t.Errorf("Expected 0 collisions for shared aliases, got %d", len(result.Collisions))
	}
}

func TestCollisionDetector_MultipleHardIdentifiers(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create two entities with both same email AND same phone
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "J. Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1a", "entity-1", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-1b", "entity-1", "+15551234567", "phone", "+15551234567", false)
	insertCollisionTestAlias(t, db, "alias-2a", "entity-2", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-2b", "entity-2", "+15551234567", "phone", "+15551234567", false)

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	// Should be upgraded to multiple hard identifiers
	if len(result.Collisions) != 1 {
		t.Errorf("Expected 1 collision (deduplicated), got %d", len(result.Collisions))
	}

	c := result.Collisions[0]
	if c.Confidence != MultipleHardIDConfidence {
		t.Errorf("Expected confidence %f for multiple hard IDs, got %f", MultipleHardIDConfidence, c.Confidence)
	}
	if c.Reason != ReasonMultipleHardIDs {
		t.Errorf("Expected reason %s, got %s", ReasonMultipleHardIDs, c.Reason)
	}
	if len(c.MatchingFacts) != 2 {
		t.Errorf("Expected 2 matching facts, got %d", len(c.MatchingFacts))
	}
}

func TestCollisionDetector_MergedEntityExcluded(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create two entities, one merged into another
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "J. Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "john@example.com", "email", "john@example.com", false)

	// Mark entity-2 as merged
	_, err := db.Exec("UPDATE entities SET merged_into = 'entity-1' WHERE id = 'entity-2'")
	if err != nil {
		t.Fatalf("Failed to update entity: %v", err)
	}

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	// Merged entities should NOT be included in collision detection
	if len(result.Collisions) != 0 {
		t.Errorf("Expected 0 collisions (merged entity excluded), got %d", len(result.Collisions))
	}
}

func TestCollisionDetector_CompoundNameBirthdate(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create two entities with same name and birthdate
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "John Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "John Smith", "name", "john smith", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "John Smith", "name", "john smith", false)
	insertCollisionTestRelWithLiteral(t, db, "rel-1", "entity-1", "1990-05-15", "BORN_ON")
	insertCollisionTestRelWithLiteral(t, db, "rel-2", "entity-2", "1990-05-15", "BORN_ON")

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	if len(result.Collisions) != 1 {
		t.Errorf("Expected 1 collision, got %d", len(result.Collisions))
	}

	c := result.Collisions[0]
	if c.Confidence != CompoundNameBirthdateConf {
		t.Errorf("Expected confidence %f, got %f", CompoundNameBirthdateConf, c.Confidence)
	}
	if c.Reason != ReasonCompound {
		t.Errorf("Expected reason %s, got %s", ReasonCompound, c.Reason)
	}
	if !c.AutoEligible {
		t.Error("Expected auto_eligible to be true for name+birthdate match")
	}
}

func TestCollisionDetector_CompoundNameEmployer(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create company entity
	insertCollisionTestEntity(t, db, "company-1", "Acme Corp", 2)

	// Create two person entities with same name working at same company
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "John Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "John Smith", "name", "john smith", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "John Smith", "name", "john smith", false)
	insertCollisionTestRelWithEntity(t, db, "rel-1", "entity-1", "company-1", "WORKS_AT")
	insertCollisionTestRelWithEntity(t, db, "rel-2", "entity-2", "company-1", "WORKS_AT")

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	if len(result.Collisions) != 1 {
		t.Errorf("Expected 1 collision, got %d", len(result.Collisions))
	}

	c := result.Collisions[0]
	if c.Confidence != CompoundNameEmployerCityConf {
		t.Errorf("Expected confidence %f, got %f", CompoundNameEmployerCityConf, c.Confidence)
	}
	if c.Reason != ReasonCompound {
		t.Errorf("Expected reason %s, got %s", ReasonCompound, c.Reason)
	}
	if c.AutoEligible {
		t.Error("Expected auto_eligible to be false for name+employer match (needs review)")
	}
}

func TestCollisionDetector_DifferentNameNoBirthdate(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create two entities with different names but same birthdate
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "Jane Doe", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "John Smith", "name", "john smith", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "Jane Doe", "name", "jane doe", false)
	insertCollisionTestRelWithLiteral(t, db, "rel-1", "entity-1", "1990-05-15", "BORN_ON")
	insertCollisionTestRelWithLiteral(t, db, "rel-2", "entity-2", "1990-05-15", "BORN_ON")

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	// Different names = no compound match
	if len(result.Collisions) != 0 {
		t.Errorf("Expected 0 collisions for different names, got %d", len(result.Collisions))
	}
}

func TestCollisionDetector_CreateMergeCandidates(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create two entities with the same email
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "J. Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "john@example.com", "email", "john@example.com", false)

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), true) // createCandidates = true
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	if result.CandidatesCreated != 1 {
		t.Errorf("Expected 1 candidate created, got %d", result.CandidatesCreated)
	}

	// Verify the merge_candidate was created
	var count int
	err = db.QueryRow("SELECT COUNT(*) FROM merge_candidates WHERE status = 'pending'").Scan(&count)
	if err != nil {
		t.Fatalf("Failed to count merge_candidates: %v", err)
	}
	if count != 1 {
		t.Errorf("Expected 1 merge_candidate in DB, got %d", count)
	}
}

func TestCollisionDetector_DetectCollisionsForEntity(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create three entities - two with same email as entity-1
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "J. Smith", 1)
	insertCollisionTestEntity(t, db, "entity-3", "Jane Doe", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-3", "entity-3", "jane@example.com", "email", "jane@example.com", false)

	detector := NewCollisionDetector(db)

	// Detect collisions only for entity-1
	result, err := detector.DetectCollisionsForEntity(context.Background(), "entity-1", false)
	if err != nil {
		t.Fatalf("DetectCollisionsForEntity failed: %v", err)
	}

	// Should find collision with entity-2, not entity-3
	if len(result.Collisions) != 1 {
		t.Errorf("Expected 1 collision, got %d", len(result.Collisions))
	}

	c := result.Collisions[0]
	if c.EntityAID != "entity-1" || c.EntityBID != "entity-2" {
		t.Errorf("Expected collision between entity-1 and entity-2, got %s and %s", c.EntityAID, c.EntityBID)
	}
}

func TestCollisionDetector_ThreeWayCollision(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create three entities with the same email
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "J. Smith", 1)
	insertCollisionTestEntity(t, db, "entity-3", "Johnny Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-3", "entity-3", "john@example.com", "email", "john@example.com", false)

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	// 3 entities sharing same email = 3 pairs: (1,2), (1,3), (2,3)
	if len(result.Collisions) != 3 {
		t.Errorf("Expected 3 collisions for 3-way match, got %d", len(result.Collisions))
	}
}

func TestCollisionDetector_HandleMatchNotCollision(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create two entities with the same handle
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "J. Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "@johnsmith", "handle", "@johnsmith", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "@johnsmith", "handle", "@johnsmith", false)

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	if len(result.Collisions) != 1 {
		t.Errorf("Expected 1 collision for handle match, got %d", len(result.Collisions))
	}
}

func TestCollisionDetector_GetPendingMergeCandidates(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create entities and collision
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "J. Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "john@example.com", "email", "john@example.com", false)

	detector := NewCollisionDetector(db)
	_, err := detector.DetectCollisions(context.Background(), true)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	// Get pending candidates
	candidates, err := detector.GetPendingMergeCandidates(context.Background(), 10)
	if err != nil {
		t.Fatalf("GetPendingMergeCandidates failed: %v", err)
	}

	if len(candidates) != 1 {
		t.Errorf("Expected 1 pending candidate, got %d", len(candidates))
	}
}

func TestCollisionDetector_GetAutoEligibleCandidates(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create email collision (auto-eligible)
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "J. Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "john@example.com", "email", "john@example.com", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "john@example.com", "email", "john@example.com", false)

	// Create name+employer collision (not auto-eligible)
	insertCollisionTestEntity(t, db, "company-1", "Acme Corp", 2)
	insertCollisionTestEntity(t, db, "entity-3", "Jane Doe", 1)
	insertCollisionTestEntity(t, db, "entity-4", "Jane Doe", 1)
	insertCollisionTestAlias(t, db, "alias-3", "entity-3", "Jane Doe", "name", "jane doe", false)
	insertCollisionTestAlias(t, db, "alias-4", "entity-4", "Jane Doe", "name", "jane doe", false)
	insertCollisionTestRelWithEntity(t, db, "rel-1", "entity-3", "company-1", "WORKS_AT")
	insertCollisionTestRelWithEntity(t, db, "rel-2", "entity-4", "company-1", "WORKS_AT")

	detector := NewCollisionDetector(db)
	_, err := detector.DetectCollisions(context.Background(), true)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	// Get auto-eligible candidates only
	candidates, err := detector.GetAutoEligibleCandidates(context.Background())
	if err != nil {
		t.Fatalf("GetAutoEligibleCandidates failed: %v", err)
	}

	// Only the email collision should be auto-eligible
	if len(candidates) != 1 {
		t.Errorf("Expected 1 auto-eligible candidate, got %d", len(candidates))
	}

	if len(candidates) > 0 && candidates[0].Reason != ReasonHardIdentifier {
		t.Errorf("Expected hard_identifier reason, got %s", candidates[0].Reason)
	}
}

func TestCollisionDetector_InvalidatedRelationshipExcluded(t *testing.T) {
	db := setupCollisionTestDB(t)
	defer db.Close()

	// Create two entities with same name and same birthdate, but one is invalidated
	insertCollisionTestEntity(t, db, "entity-1", "John Smith", 1)
	insertCollisionTestEntity(t, db, "entity-2", "John Smith", 1)
	insertCollisionTestAlias(t, db, "alias-1", "entity-1", "John Smith", "name", "john smith", false)
	insertCollisionTestAlias(t, db, "alias-2", "entity-2", "John Smith", "name", "john smith", false)

	now := time.Now().Format(time.RFC3339)
	// Entity-1 has valid birthdate
	_, err := db.Exec(`
		INSERT INTO relationships (id, source_entity_id, target_literal, relation_type, fact, created_at, invalid_at)
		VALUES (?, ?, ?, ?, ?, ?, NULL)
	`, "rel-1", "entity-1", "1990-05-15", "BORN_ON", "Test fact", now)
	if err != nil {
		t.Fatalf("Failed to insert relationship: %v", err)
	}

	// Entity-2 has invalidated birthdate
	_, err = db.Exec(`
		INSERT INTO relationships (id, source_entity_id, target_literal, relation_type, fact, created_at, invalid_at)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	`, "rel-2", "entity-2", "1990-05-15", "BORN_ON", "Test fact", now, now)
	if err != nil {
		t.Fatalf("Failed to insert relationship: %v", err)
	}

	detector := NewCollisionDetector(db)
	result, err := detector.DetectCollisions(context.Background(), false)
	if err != nil {
		t.Fatalf("DetectCollisions failed: %v", err)
	}

	// Invalidated relationships should NOT contribute to compound matches
	if len(result.Collisions) != 0 {
		t.Errorf("Expected 0 collisions (invalidated relationship excluded), got %d", len(result.Collisions))
	}
}

func TestSplitCSV(t *testing.T) {
	tests := []struct {
		input    string
		expected []string
	}{
		{"a,b,c", []string{"a", "b", "c"}},
		{"a, b, c", []string{"a", "b", "c"}},
		{"single", []string{"single"}},
		{"", nil},
		{"a,,b", []string{"a", "b"}},
	}

	for _, tt := range tests {
		result := splitCSV(tt.input)
		if len(result) != len(tt.expected) {
			t.Errorf("splitCSV(%q) = %v, expected %v", tt.input, result, tt.expected)
			continue
		}
		for i, v := range result {
			if v != tt.expected[i] {
				t.Errorf("splitCSV(%q)[%d] = %q, expected %q", tt.input, i, v, tt.expected[i])
			}
		}
	}
}
