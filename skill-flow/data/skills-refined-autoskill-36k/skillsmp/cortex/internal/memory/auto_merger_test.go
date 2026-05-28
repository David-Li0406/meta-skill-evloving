package memory

import (
	"context"
	"database/sql"
	"encoding/json"
	"testing"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

// setupAutoMergerTestDB creates a test database with the required tables.
func setupAutoMergerTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatalf("failed to open database: %v", err)
	}

	// Create required tables
	_, err = db.Exec(`
		CREATE TABLE entities (
			id TEXT PRIMARY KEY,
			canonical_name TEXT NOT NULL,
			entity_type_id INTEGER NOT NULL,
			summary TEXT,
			summary_updated_at TEXT,
			origin TEXT,
			confidence REAL,
			merged_into TEXT REFERENCES entities(id),
			created_at TEXT NOT NULL,
			updated_at TEXT NOT NULL
		);

		CREATE TABLE entity_aliases (
			id TEXT PRIMARY KEY,
			entity_id TEXT NOT NULL REFERENCES entities(id),
			alias TEXT NOT NULL,
			alias_type TEXT NOT NULL,
			normalized TEXT NOT NULL,
			is_shared BOOLEAN DEFAULT FALSE,
			created_at TEXT NOT NULL
		);

		CREATE TABLE relationships (
			id TEXT PRIMARY KEY,
			source_entity_id TEXT NOT NULL REFERENCES entities(id),
			target_entity_id TEXT REFERENCES entities(id),
			target_literal TEXT,
			relation_type TEXT NOT NULL,
			fact TEXT,
			valid_at TEXT,
			invalid_at TEXT,
			created_at TEXT NOT NULL,
			confidence REAL
		);

		CREATE TABLE episodes (
			id TEXT PRIMARY KEY,
			definition_id TEXT,
			channel TEXT,
			start_time INTEGER NOT NULL,
			end_time INTEGER NOT NULL,
			event_count INTEGER DEFAULT 0,
			content TEXT,
			created_at INTEGER NOT NULL
		);

		CREATE TABLE episode_entity_mentions (
			episode_id TEXT NOT NULL,
			entity_id TEXT NOT NULL,
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
			source_entity_id TEXT NOT NULL REFERENCES entities(id),
			target_entity_id TEXT NOT NULL REFERENCES entities(id),
			merge_type TEXT NOT NULL,
			triggering_facts TEXT,
			similarity_score REAL,
			created_at TEXT NOT NULL,
			resolved_by TEXT
		);
	`)
	if err != nil {
		t.Fatalf("failed to create tables: %v", err)
	}

	return db
}

// createTestEntity creates a test entity and returns its ID.
func createTestEntity(t *testing.T, db *sql.DB, id, name string, entityTypeID int) string {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO entities (id, canonical_name, entity_type_id, created_at, updated_at)
		VALUES (?, ?, ?, ?, ?)
	`, id, name, entityTypeID, now, now)
	if err != nil {
		t.Fatalf("failed to create entity: %v", err)
	}
	return id
}

// createTestAlias creates a test alias for an entity.
func createTestAlias(t *testing.T, db *sql.DB, entityID, alias, aliasType, normalized string, isShared bool) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO entity_aliases (id, entity_id, alias, alias_type, normalized, is_shared, created_at)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	`, "alias-"+alias+"-"+entityID, entityID, alias, aliasType, normalized, isShared, now)
	if err != nil {
		t.Fatalf("failed to create alias: %v", err)
	}
}

// createTestRelationship creates a test relationship.
func createTestRelationship(t *testing.T, db *sql.DB, sourceID, relationType string, targetEntityID *string, targetLiteral *string) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO relationships (id, source_entity_id, target_entity_id, target_literal, relation_type, created_at)
		VALUES (?, ?, ?, ?, ?, ?)
	`, "rel-"+sourceID+"-"+relationType, sourceID, targetEntityID, targetLiteral, relationType, now)
	if err != nil {
		t.Fatalf("failed to create relationship: %v", err)
	}
}

// createTestMergeCandidate creates a test merge candidate.
func createTestMergeCandidate(t *testing.T, db *sql.DB, entityAID, entityBID string, confidence float64, autoEligible bool, reason string) string {
	now := time.Now().Format(time.RFC3339)
	id := "mc-" + entityAID + "-" + entityBID
	facts := []map[string]interface{}{{"type": "email", "value": "test@example.com"}}
	factsJSON, _ := json.Marshal(facts)

	_, err := db.Exec(`
		INSERT INTO merge_candidates (id, entity_a_id, entity_b_id, confidence, auto_eligible, reason, matching_facts, status, created_at)
		VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
	`, id, entityAID, entityBID, confidence, autoEligible, reason, string(factsJSON), now)
	if err != nil {
		t.Fatalf("failed to create merge candidate: %v", err)
	}
	return id
}

// createTestEpisodeMention creates a test episode entity mention.
func createTestEpisodeMention(t *testing.T, db *sql.DB, episodeID, entityID string, mentionCount int) {
	now := time.Now().Format(time.RFC3339)
	_, err := db.Exec(`
		INSERT INTO episode_entity_mentions (episode_id, entity_id, mention_count, created_at)
		VALUES (?, ?, ?, ?)
	`, episodeID, entityID, mentionCount, now)
	if err != nil {
		t.Fatalf("failed to create episode mention: %v", err)
	}
}

// createTestEpisode creates a test episode.
func createTestEpisode(t *testing.T, db *sql.DB, id string) {
	now := time.Now().Unix()
	_, err := db.Exec(`
		INSERT INTO episodes (id, channel, start_time, end_time, created_at)
		VALUES (?, 'test', ?, ?, ?)
	`, id, now-3600, now, now)
	if err != nil {
		t.Fatalf("failed to create episode: %v", err)
	}
}

func TestDetectConflicts_NoConflicts(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create two entities with no conflicting data
	createTestEntity(t, db, "entity-a", "Tyler", 1)
	createTestEntity(t, db, "entity-b", "Tyler B", 1)

	merger := NewAutoMerger(db)
	conflicts, err := merger.DetectConflicts(context.Background(), "entity-a", "entity-b")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(conflicts) != 0 {
		t.Errorf("expected no conflicts, got %d", len(conflicts))
	}
}

func TestDetectConflicts_DifferentPhones(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create two entities with different phone numbers
	createTestEntity(t, db, "entity-a", "Tyler", 1)
	createTestEntity(t, db, "entity-b", "Tyler B", 1)
	createTestAlias(t, db, "entity-a", "+1-555-111-1111", "phone", "+15551111111", false)
	createTestAlias(t, db, "entity-b", "+1-555-222-2222", "phone", "+15552222222", false)

	merger := NewAutoMerger(db)
	conflicts, err := merger.DetectConflicts(context.Background(), "entity-a", "entity-b")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(conflicts) != 1 {
		t.Fatalf("expected 1 conflict, got %d", len(conflicts))
	}

	if conflicts[0].Type != "different_phones" {
		t.Errorf("expected conflict type 'different_phones', got '%s'", conflicts[0].Type)
	}
}

func TestDetectConflicts_SamePhone(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create two entities with the same phone number (no conflict)
	createTestEntity(t, db, "entity-a", "Tyler", 1)
	createTestEntity(t, db, "entity-b", "Tyler B", 1)
	createTestAlias(t, db, "entity-a", "+1-555-111-1111", "phone", "+15551111111", false)
	createTestAlias(t, db, "entity-b", "+1-555-111-1111", "phone", "+15551111111", false)

	merger := NewAutoMerger(db)
	conflicts, err := merger.DetectConflicts(context.Background(), "entity-a", "entity-b")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(conflicts) != 0 {
		t.Errorf("expected no conflicts (same phone), got %d", len(conflicts))
	}
}

func TestDetectConflicts_DifferentEmails(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create two entities with different emails
	createTestEntity(t, db, "entity-a", "Tyler", 1)
	createTestEntity(t, db, "entity-b", "Tyler B", 1)
	createTestAlias(t, db, "entity-a", "tyler@work.com", "email", "tyler@work.com", false)
	createTestAlias(t, db, "entity-b", "tyler@personal.com", "email", "tyler@personal.com", false)

	merger := NewAutoMerger(db)
	conflicts, err := merger.DetectConflicts(context.Background(), "entity-a", "entity-b")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(conflicts) != 1 {
		t.Fatalf("expected 1 conflict, got %d", len(conflicts))
	}

	if conflicts[0].Type != "different_emails" {
		t.Errorf("expected conflict type 'different_emails', got '%s'", conflicts[0].Type)
	}
}

func TestDetectConflicts_DifferentBirthdates(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create two entities with different birthdates
	createTestEntity(t, db, "entity-a", "Tyler", 1)
	createTestEntity(t, db, "entity-b", "Tyler B", 1)

	bday1 := "1990-01-15"
	bday2 := "1985-06-20"
	createTestRelationship(t, db, "entity-a", "BORN_ON", nil, &bday1)
	createTestRelationship(t, db, "entity-b", "BORN_ON", nil, &bday2)

	merger := NewAutoMerger(db)
	conflicts, err := merger.DetectConflicts(context.Background(), "entity-a", "entity-b")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(conflicts) != 1 {
		t.Fatalf("expected 1 conflict, got %d", len(conflicts))
	}

	if conflicts[0].Type != "different_birthdates" {
		t.Errorf("expected conflict type 'different_birthdates', got '%s'", conflicts[0].Type)
	}
}

func TestDetectConflicts_SameBirthdate(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create two entities with the same birthdate (no conflict)
	createTestEntity(t, db, "entity-a", "Tyler", 1)
	createTestEntity(t, db, "entity-b", "Tyler B", 1)

	bday := "1990-01-15"
	createTestRelationship(t, db, "entity-a", "BORN_ON", nil, &bday)
	createTestRelationship(t, db, "entity-b", "BORN_ON", nil, &bday)

	merger := NewAutoMerger(db)
	conflicts, err := merger.DetectConflicts(context.Background(), "entity-a", "entity-b")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(conflicts) != 0 {
		t.Errorf("expected no conflicts (same birthdate), got %d", len(conflicts))
	}
}

func TestDetectConflicts_MultipleConflicts(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create two entities with multiple conflicts
	createTestEntity(t, db, "entity-a", "Tyler", 1)
	createTestEntity(t, db, "entity-b", "Tyler B", 1)

	// Different phones
	createTestAlias(t, db, "entity-a", "+1-555-111-1111", "phone", "+15551111111", false)
	createTestAlias(t, db, "entity-b", "+1-555-222-2222", "phone", "+15552222222", false)

	// Different emails
	createTestAlias(t, db, "entity-a", "tyler@work.com", "email", "tyler@work.com", false)
	createTestAlias(t, db, "entity-b", "tyler@personal.com", "email", "tyler@personal.com", false)

	// Different birthdates
	bday1 := "1990-01-15"
	bday2 := "1985-06-20"
	createTestRelationship(t, db, "entity-a", "BORN_ON", nil, &bday1)
	createTestRelationship(t, db, "entity-b", "BORN_ON", nil, &bday2)

	merger := NewAutoMerger(db)
	conflicts, err := merger.DetectConflicts(context.Background(), "entity-a", "entity-b")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(conflicts) != 3 {
		t.Errorf("expected 3 conflicts, got %d", len(conflicts))
	}
}

func TestShouldAutoMerge_HardIdentifierHighConfidence(t *testing.T) {
	merger := &AutoMerger{}

	candidate := &MergeCandidate{
		Confidence:   0.95,
		Reason:       "hard_identifier",
		MatchingFacts: []map[string]interface{}{
			{"type": "email", "value": "tyler@example.com"},
		},
		Conflicts: nil,
	}

	if !merger.ShouldAutoMerge(candidate) {
		t.Error("expected should auto-merge for hard identifier with 0.95 confidence")
	}
}

func TestShouldAutoMerge_HardIdentifierWithConflicts(t *testing.T) {
	merger := &AutoMerger{}

	candidate := &MergeCandidate{
		Confidence:   0.95,
		Reason:       "hard_identifier",
		MatchingFacts: []map[string]interface{}{
			{"type": "email", "value": "tyler@example.com"},
		},
		Conflicts: []Conflict{
			{Type: "different_phones"},
		},
	}

	if merger.ShouldAutoMerge(candidate) {
		t.Error("expected should NOT auto-merge when conflicts exist")
	}
}

func TestShouldAutoMerge_MultipleHardIdentifiers(t *testing.T) {
	merger := &AutoMerger{}

	candidate := &MergeCandidate{
		Confidence:   0.99,
		Reason:       "multiple_hard_identifiers",
		MatchingFacts: []map[string]interface{}{
			{"type": "email", "value": "tyler@example.com"},
			{"type": "phone", "value": "+15551234567"},
		},
		Conflicts: nil,
	}

	if !merger.ShouldAutoMerge(candidate) {
		t.Error("expected should auto-merge for multiple hard identifiers")
	}
}

func TestShouldAutoMerge_CompoundNameBirthdate(t *testing.T) {
	merger := &AutoMerger{}

	candidate := &MergeCandidate{
		Confidence: 0.90,
		Reason:     "compound",
		MatchingFacts: []map[string]interface{}{
			{"type": "name", "value": "tyler"},
			{"type": "birthdate", "value": "1990-01-15"},
		},
		Context: map[string]interface{}{
			"compound_type": "name_birthdate",
		},
		Conflicts: nil,
	}

	if !merger.ShouldAutoMerge(candidate) {
		t.Error("expected should auto-merge for name+birthdate compound match")
	}
}

func TestShouldAutoMerge_LowConfidence(t *testing.T) {
	merger := &AutoMerger{}

	candidate := &MergeCandidate{
		Confidence: 0.80,
		Reason:     "hard_identifier",
		MatchingFacts: []map[string]interface{}{
			{"type": "email", "value": "tyler@example.com"},
		},
		Conflicts: nil,
	}

	if merger.ShouldAutoMerge(candidate) {
		t.Error("expected should NOT auto-merge for low confidence")
	}
}

func TestExecuteMerge_MovesAliases(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create source and target entities
	createTestEntity(t, db, "entity-source", "Tyler Source", 1)
	createTestEntity(t, db, "entity-target", "Tyler Target", 1)

	// Create aliases on source
	createTestAlias(t, db, "entity-source", "tyler@example.com", "email", "tyler@example.com", false)
	createTestAlias(t, db, "entity-source", "+1-555-1234", "phone", "+15551234", false)

	// Create merge candidate
	candidateID := createTestMergeCandidate(t, db, "entity-source", "entity-target", 0.95, true, "hard_identifier")

	merger := NewAutoMerger(db)
	candidate, _ := merger.GetCandidateByID(context.Background(), candidateID)

	result, err := merger.ExecuteMerge(context.Background(), candidate, "auto")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if result.AliasesMoved != 2 {
		t.Errorf("expected 2 aliases moved, got %d", result.AliasesMoved)
	}

	// Verify aliases are now on target
	var count int
	db.QueryRow(`SELECT COUNT(*) FROM entity_aliases WHERE entity_id = 'entity-target'`).Scan(&count)
	if count != 2 {
		t.Errorf("expected 2 aliases on target, got %d", count)
	}
}

func TestExecuteMerge_MovesRelationships(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create entities
	createTestEntity(t, db, "entity-source", "Tyler Source", 1)
	createTestEntity(t, db, "entity-target", "Tyler Target", 1)
	createTestEntity(t, db, "entity-company", "Acme Corp", 2)

	// Create relationships on source
	companyID := "entity-company"
	createTestRelationship(t, db, "entity-source", "WORKS_AT", &companyID, nil)

	// Also create a relationship where source is the target
	createTestRelationship(t, db, "entity-company", "EMPLOYS", strPtr("entity-source"), nil)

	// Create merge candidate
	candidateID := createTestMergeCandidate(t, db, "entity-source", "entity-target", 0.95, true, "hard_identifier")

	merger := NewAutoMerger(db)
	candidate, _ := merger.GetCandidateByID(context.Background(), candidateID)

	result, err := merger.ExecuteMerge(context.Background(), candidate, "auto")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if result.RelationsMoved != 2 {
		t.Errorf("expected 2 relationships moved, got %d", result.RelationsMoved)
	}

	// Verify source relationship moved
	var targetID string
	db.QueryRow(`SELECT source_entity_id FROM relationships WHERE relation_type = 'WORKS_AT'`).Scan(&targetID)
	if targetID != "entity-target" {
		t.Errorf("expected WORKS_AT source to be entity-target, got %s", targetID)
	}

	// Verify relationship where source was target
	db.QueryRow(`SELECT target_entity_id FROM relationships WHERE relation_type = 'EMPLOYS'`).Scan(&targetID)
	if targetID != "entity-target" {
		t.Errorf("expected EMPLOYS target to be entity-target, got %s", targetID)
	}
}

func TestExecuteMerge_MovesMentions(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create entities
	createTestEntity(t, db, "entity-source", "Tyler Source", 1)
	createTestEntity(t, db, "entity-target", "Tyler Target", 1)

	// Create episodes and mentions
	createTestEpisode(t, db, "episode-1")
	createTestEpisode(t, db, "episode-2")
	createTestEpisodeMention(t, db, "episode-1", "entity-source", 3)
	createTestEpisodeMention(t, db, "episode-2", "entity-source", 2)

	// Create merge candidate
	candidateID := createTestMergeCandidate(t, db, "entity-source", "entity-target", 0.95, true, "hard_identifier")

	merger := NewAutoMerger(db)
	candidate, _ := merger.GetCandidateByID(context.Background(), candidateID)

	_, err := merger.ExecuteMerge(context.Background(), candidate, "auto")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	// Verify mentions are now on target
	var count int
	db.QueryRow(`SELECT COUNT(*) FROM episode_entity_mentions WHERE entity_id = 'entity-target'`).Scan(&count)
	if count != 2 {
		t.Errorf("expected 2 mentions on target, got %d", count)
	}

	// Verify no mentions remain on source
	db.QueryRow(`SELECT COUNT(*) FROM episode_entity_mentions WHERE entity_id = 'entity-source'`).Scan(&count)
	if count != 0 {
		t.Errorf("expected 0 mentions on source, got %d", count)
	}
}

func TestExecuteMerge_MergesMentionCounts(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create entities
	createTestEntity(t, db, "entity-source", "Tyler Source", 1)
	createTestEntity(t, db, "entity-target", "Tyler Target", 1)

	// Create episode with mentions for BOTH entities
	createTestEpisode(t, db, "episode-1")
	createTestEpisodeMention(t, db, "episode-1", "entity-source", 3)
	createTestEpisodeMention(t, db, "episode-1", "entity-target", 2)

	// Create merge candidate
	candidateID := createTestMergeCandidate(t, db, "entity-source", "entity-target", 0.95, true, "hard_identifier")

	merger := NewAutoMerger(db)
	candidate, _ := merger.GetCandidateByID(context.Background(), candidateID)

	_, err := merger.ExecuteMerge(context.Background(), candidate, "auto")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	// Verify mention counts are merged
	var mentionCount int
	db.QueryRow(`SELECT mention_count FROM episode_entity_mentions WHERE entity_id = 'entity-target' AND episode_id = 'episode-1'`).Scan(&mentionCount)
	if mentionCount != 5 { // 3 + 2
		t.Errorf("expected merged mention count 5, got %d", mentionCount)
	}
}

func TestExecuteMerge_MarksSourceAsMerged(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create entities
	createTestEntity(t, db, "entity-source", "Tyler Source", 1)
	createTestEntity(t, db, "entity-target", "Tyler Target", 1)

	// Create merge candidate
	candidateID := createTestMergeCandidate(t, db, "entity-source", "entity-target", 0.95, true, "hard_identifier")

	merger := NewAutoMerger(db)
	candidate, _ := merger.GetCandidateByID(context.Background(), candidateID)

	_, err := merger.ExecuteMerge(context.Background(), candidate, "auto")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	// Verify source is marked as merged
	var mergedInto sql.NullString
	var canonicalName string
	db.QueryRow(`SELECT merged_into, canonical_name FROM entities WHERE id = 'entity-source'`).Scan(&mergedInto, &canonicalName)

	if !mergedInto.Valid || mergedInto.String != "entity-target" {
		t.Errorf("expected source merged_into to be 'entity-target', got '%v'", mergedInto.String)
	}

	if !containsString(canonicalName, "[MERGED→") {
		t.Errorf("expected canonical name to contain merge marker, got '%s'", canonicalName)
	}
}

func TestExecuteMerge_CreatesMergeEvent(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create entities
	createTestEntity(t, db, "entity-source", "Tyler Source", 1)
	createTestEntity(t, db, "entity-target", "Tyler Target", 1)

	// Create merge candidate
	candidateID := createTestMergeCandidate(t, db, "entity-source", "entity-target", 0.95, true, "hard_identifier")

	merger := NewAutoMerger(db)
	candidate, _ := merger.GetCandidateByID(context.Background(), candidateID)

	result, err := merger.ExecuteMerge(context.Background(), candidate, "auto")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if result.MergeEventID == "" {
		t.Error("expected merge event ID to be set")
	}

	// Verify merge event was created
	var count int
	db.QueryRow(`SELECT COUNT(*) FROM entity_merge_events WHERE id = ?`, result.MergeEventID).Scan(&count)
	if count != 1 {
		t.Error("expected merge event to be created")
	}
}

func TestExecuteMerge_UpdatesCandidateStatus(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create entities
	createTestEntity(t, db, "entity-source", "Tyler Source", 1)
	createTestEntity(t, db, "entity-target", "Tyler Target", 1)

	// Create merge candidate
	candidateID := createTestMergeCandidate(t, db, "entity-source", "entity-target", 0.95, true, "hard_identifier")

	merger := NewAutoMerger(db)
	candidate, _ := merger.GetCandidateByID(context.Background(), candidateID)

	_, err := merger.ExecuteMerge(context.Background(), candidate, "auto")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	// Verify candidate status is updated
	var status string
	var resolvedBy sql.NullString
	db.QueryRow(`SELECT status, resolved_by FROM merge_candidates WHERE id = ?`, candidateID).Scan(&status, &resolvedBy)

	if status != "merged" {
		t.Errorf("expected status 'merged', got '%s'", status)
	}
	if !resolvedBy.Valid || resolvedBy.String != "auto" {
		t.Errorf("expected resolved_by 'auto', got '%v'", resolvedBy.String)
	}
}

func TestProcessMergeCandidates_AutoMerges(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create entities
	createTestEntity(t, db, "entity-a", "Tyler A", 1)
	createTestEntity(t, db, "entity-b", "Tyler B", 1)

	// Create merge candidate (auto-eligible, no conflicts)
	createTestMergeCandidate(t, db, "entity-a", "entity-b", 0.95, true, "hard_identifier")

	merger := NewAutoMerger(db)
	result, err := merger.ProcessMergeCandidates(context.Background())
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if result.Processed != 1 {
		t.Errorf("expected 1 processed, got %d", result.Processed)
	}
	if result.AutoMerged != 1 {
		t.Errorf("expected 1 auto-merged, got %d", result.AutoMerged)
	}
}

func TestProcessMergeCandidates_DetectsConflicts(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create entities with conflicting phones
	createTestEntity(t, db, "entity-a", "Tyler A", 1)
	createTestEntity(t, db, "entity-b", "Tyler B", 1)
	createTestAlias(t, db, "entity-a", "+1-555-111-1111", "phone", "+15551111111", false)
	createTestAlias(t, db, "entity-b", "+1-555-222-2222", "phone", "+15552222222", false)

	// Create merge candidate
	createTestMergeCandidate(t, db, "entity-a", "entity-b", 0.95, true, "hard_identifier")

	merger := NewAutoMerger(db)
	result, err := merger.ProcessMergeCandidates(context.Background())
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if result.Conflicts != 1 {
		t.Errorf("expected 1 conflict, got %d", result.Conflicts)
	}
	if result.AutoMerged != 0 {
		t.Errorf("expected 0 auto-merged (due to conflict), got %d", result.AutoMerged)
	}
}

func TestIsBetterName(t *testing.T) {
	merger := &AutoMerger{}

	tests := []struct {
		source   string
		target   string
		expected bool
	}{
		{"Tyler Brandt", "TYLER", true},      // Title case better than ALL CAPS
		{"TYLER", "Tyler Brandt", false},     // ALL CAPS worse than title case
		{"Tyler Brandt", "Tyler", true},      // Longer name better
		{"T", "Tyler", false},                // Too short not better
		{"", "Tyler", false},                 // Empty not better
		{"Tyler", "", true},                  // Something better than empty
		{"Tyler", "Tyler", false},            // Same name not better
	}

	for _, tt := range tests {
		result := merger.isBetterName(tt.source, tt.target)
		if result != tt.expected {
			t.Errorf("isBetterName(%q, %q) = %v, expected %v", tt.source, tt.target, result, tt.expected)
		}
	}
}

func TestRejectCandidate(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create entities and candidate
	createTestEntity(t, db, "entity-a", "Tyler A", 1)
	createTestEntity(t, db, "entity-b", "Tyler B", 1)
	candidateID := createTestMergeCandidate(t, db, "entity-a", "entity-b", 0.80, false, "compound")

	merger := NewAutoMerger(db)
	err := merger.RejectCandidate(context.Background(), candidateID, "user:tyler", "Not the same person")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	// Verify status
	var status, resolvedBy, reason string
	db.QueryRow(`SELECT status, resolved_by, resolution_reason FROM merge_candidates WHERE id = ?`, candidateID).Scan(&status, &resolvedBy, &reason)

	if status != "rejected" {
		t.Errorf("expected status 'rejected', got '%s'", status)
	}
	if resolvedBy != "user:tyler" {
		t.Errorf("expected resolved_by 'user:tyler', got '%s'", resolvedBy)
	}
	if reason != "Not the same person" {
		t.Errorf("expected reason 'Not the same person', got '%s'", reason)
	}
}

func TestGetMergeHistory(t *testing.T) {
	db := setupAutoMergerTestDB(t)
	defer db.Close()

	// Create entities
	createTestEntity(t, db, "entity-source1", "Tyler S1", 1)
	createTestEntity(t, db, "entity-source2", "Tyler S2", 1)
	createTestEntity(t, db, "entity-target", "Tyler Target", 1)

	// Create merge events
	now := time.Now().Format(time.RFC3339)
	db.Exec(`INSERT INTO entity_merge_events (id, source_entity_id, target_entity_id, merge_type, created_at, resolved_by) VALUES (?, ?, ?, ?, ?, ?)`,
		"event-1", "entity-source1", "entity-target", "hard_identifier", now, "auto")
	db.Exec(`INSERT INTO entity_merge_events (id, source_entity_id, target_entity_id, merge_type, created_at, resolved_by) VALUES (?, ?, ?, ?, ?, ?)`,
		"event-2", "entity-source2", "entity-target", "manual", now, "user:tyler")

	merger := NewAutoMerger(db)
	events, err := merger.GetMergeHistory(context.Background(), "entity-target")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(events) != 2 {
		t.Errorf("expected 2 merge events, got %d", len(events))
	}
}

// Helper to check if a string contains a substring
func containsString(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > 0 && containsStringHelper(s, substr))
}

func containsStringHelper(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

// Helper to create a string pointer
func strPtr(s string) *string {
	return &s
}
