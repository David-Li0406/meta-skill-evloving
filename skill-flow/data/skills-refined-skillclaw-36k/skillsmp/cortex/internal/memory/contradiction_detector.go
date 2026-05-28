package memory

import (
	"context"
	"database/sql"
	"fmt"
	"time"
)

// ContradictionResult contains the output from contradiction detection.
type ContradictionResult struct {
	ContradictionsFound int      // Number of contradictions detected
	InvalidatedIDs      []string // IDs of relationships that were invalidated
}

// ContradictingRelationType defines how relationships contradict each other.
// Some relationships are "exclusive" - only one can be true at a time (WORKS_AT, LIVES_IN).
// When a new exclusive relationship is found, the old one is invalidated.
var ExclusiveRelationTypes = map[string]bool{
	// Employment - typically one primary employer at a time
	"WORKS_AT": true,

	// Residence - typically one primary residence at a time
	"LIVES_IN": true,

	// Marital status - mutually exclusive
	"SPOUSE_OF": true,
	"MARRIED_TO": true,

	// Dating - typically exclusive
	"DATING": true,

	// Attendance at institutions (e.g., which school you attend)
	// Note: ATTENDED can be multiple historical, but current attendance is singular
	// We handle this by checking valid_at/invalid_at
}

// ContradictionDetector finds and invalidates contradicted facts.
// When a new fact contradicts an existing fact, the old fact gets
// invalid_at set to mark it as no longer true.
type ContradictionDetector struct {
	db *sql.DB
}

// NewContradictionDetector creates a new ContradictionDetector.
func NewContradictionDetector(db *sql.DB) *ContradictionDetector {
	return &ContradictionDetector{db: db}
}

// Detect finds existing facts that are contradicted by new facts and invalidates them.
// For exclusive relationship types (WORKS_AT, LIVES_IN, etc.), having a new relationship
// implies the old one is no longer true.
//
// The invalidationTime is used as the invalid_at value when the new relationship
// doesn't have an explicit valid_at date.
//
// Returns the count of contradictions found and the IDs of invalidated relationships.
func (d *ContradictionDetector) Detect(ctx context.Context, newRelationshipIDs []string, invalidationTime time.Time) (*ContradictionResult, error) {
	result := &ContradictionResult{
		InvalidatedIDs: make([]string, 0),
	}

	for _, newRelID := range newRelationshipIDs {
		invalidated, err := d.detectForRelationship(ctx, newRelID, invalidationTime)
		if err != nil {
			return nil, fmt.Errorf("detect contradictions for relationship %s: %w", newRelID, err)
		}
		result.InvalidatedIDs = append(result.InvalidatedIDs, invalidated...)
		result.ContradictionsFound += len(invalidated)
	}

	return result, nil
}

// detectForRelationship checks if a new relationship contradicts any existing relationships.
func (d *ContradictionDetector) detectForRelationship(ctx context.Context, newRelID string, invalidationTime time.Time) ([]string, error) {
	// Get the new relationship's details
	var sourceEntityID, relationType string
	var targetEntityID, targetLiteral, validAt sql.NullString

	err := d.db.QueryRowContext(ctx, `
		SELECT source_entity_id, relation_type, target_entity_id, target_literal, valid_at
		FROM relationships
		WHERE id = ?
	`, newRelID).Scan(&sourceEntityID, &relationType, &targetEntityID, &targetLiteral, &validAt)

	if err != nil {
		if err == sql.ErrNoRows {
			return nil, nil // Relationship doesn't exist
		}
		return nil, fmt.Errorf("get relationship details: %w", err)
	}

	// Only check exclusive relationship types
	if !ExclusiveRelationTypes[relationType] {
		return nil, nil
	}

	// Find existing relationships that might be contradicted
	// A contradiction exists when:
	// 1. Same source entity
	// 2. Same relation type
	// 3. Different target (entity or literal)
	// 4. Old relationship is still "current" (invalid_at IS NULL)
	// 5. Old relationship's valid_at is before the new one (or both NULL)
	invalidated := make([]string, 0)

	if targetEntityID.Valid {
		// Entity-targeted relationship - find contradicting entity targets
		// Only invalidate relationships that are older than the new one:
		// - If new has valid_at: invalidate if old has NULL or earlier valid_at
		// - If new has no valid_at: invalidate if old also has no valid_at (same-episode fallback)
		var query string
		var args []interface{}
		if validAt.Valid {
			// New relationship has a date - only invalidate older ones
			query = `
				SELECT id FROM relationships
				WHERE source_entity_id = ?
				  AND relation_type = ?
				  AND target_entity_id IS NOT NULL
				  AND target_entity_id != ?
				  AND invalid_at IS NULL
				  AND id != ?
				  AND (valid_at IS NULL OR valid_at < ?)
			`
			args = []interface{}{sourceEntityID, relationType, targetEntityID.String, newRelID, validAt.String}
		} else {
			// New relationship has no date - only invalidate others without dates
			// This handles same-episode conflicts when neither has explicit dates
			query = `
				SELECT id FROM relationships
				WHERE source_entity_id = ?
				  AND relation_type = ?
				  AND target_entity_id IS NOT NULL
				  AND target_entity_id != ?
				  AND invalid_at IS NULL
				  AND id != ?
				  AND valid_at IS NULL
			`
			args = []interface{}{sourceEntityID, relationType, targetEntityID.String, newRelID}
		}
		rows, err := d.db.QueryContext(ctx, query, args...)

		if err != nil {
			return nil, fmt.Errorf("find entity contradictions: %w", err)
		}

		// Collect all IDs first before closing rows
		// (SQLite doesn't support concurrent queries on same connection)
		var oldIDs []string
		for rows.Next() {
			var oldID string
			if err := rows.Scan(&oldID); err != nil {
				rows.Close()
				return nil, err
			}
			oldIDs = append(oldIDs, oldID)
		}
		rows.Close()

		if err := rows.Err(); err != nil {
			return nil, err
		}

		// Now invalidate each relationship (after rows is closed)
		for _, oldID := range oldIDs {
			if err := d.invalidateRelationship(ctx, oldID, invalidationTime, validAt); err != nil {
				return nil, err
			}
			invalidated = append(invalidated, oldID)
		}
	} else if targetLiteral.Valid {
		// Literal-targeted relationship - find contradicting literal targets
		// Only invalidate relationships that are older than the new one:
		// - If new has valid_at: invalidate if old has NULL or earlier valid_at
		// - If new has no valid_at: invalidate if old also has no valid_at (same-episode fallback)
		var query string
		var args []interface{}
		if validAt.Valid {
			query = `
				SELECT id FROM relationships
				WHERE source_entity_id = ?
				  AND relation_type = ?
				  AND target_literal IS NOT NULL
				  AND target_literal != ?
				  AND invalid_at IS NULL
				  AND id != ?
				  AND (valid_at IS NULL OR valid_at < ?)
			`
			args = []interface{}{sourceEntityID, relationType, targetLiteral.String, newRelID, validAt.String}
		} else {
			query = `
				SELECT id FROM relationships
				WHERE source_entity_id = ?
				  AND relation_type = ?
				  AND target_literal IS NOT NULL
				  AND target_literal != ?
				  AND invalid_at IS NULL
				  AND id != ?
				  AND valid_at IS NULL
			`
			args = []interface{}{sourceEntityID, relationType, targetLiteral.String, newRelID}
		}
		rows, err := d.db.QueryContext(ctx, query, args...)

		if err != nil {
			return nil, fmt.Errorf("find literal contradictions: %w", err)
		}

		// Collect all IDs first before closing rows
		// (SQLite doesn't support concurrent queries on same connection)
		var oldIDs []string
		for rows.Next() {
			var oldID string
			if err := rows.Scan(&oldID); err != nil {
				rows.Close()
				return nil, err
			}
			oldIDs = append(oldIDs, oldID)
		}
		rows.Close()

		if err := rows.Err(); err != nil {
			return nil, err
		}

		// Now invalidate each relationship (after rows is closed)
		for _, oldID := range oldIDs {
			if err := d.invalidateRelationship(ctx, oldID, invalidationTime, validAt); err != nil {
				return nil, err
			}
			invalidated = append(invalidated, oldID)
		}
	}

	return invalidated, nil
}

// invalidateRelationship sets invalid_at on an old relationship.
// Uses the new relationship's valid_at if available, otherwise the invalidationTime.
func (d *ContradictionDetector) invalidateRelationship(ctx context.Context, oldRelID string, invalidationTime time.Time, newValidAt sql.NullString) error {
	var invalidAt string

	if newValidAt.Valid {
		// Use the new relationship's valid_at as the old one's invalid_at
		// This represents "the old fact stopped being true when the new fact became true"
		invalidAt = newValidAt.String
	} else {
		// Use the episode timestamp as fallback
		invalidAt = invalidationTime.Format(time.RFC3339)
	}

	_, err := d.db.ExecContext(ctx, `
		UPDATE relationships
		SET invalid_at = ?
		WHERE id = ?
		  AND invalid_at IS NULL
	`, invalidAt, oldRelID)

	if err != nil {
		return fmt.Errorf("update relationships: %w", err)
	}
	return nil
}

// DetectAndInvalidate is a convenience method that processes resolved relationships
// and detects contradictions. It should be called after EdgeResolver creates new relationships.
//
// The relationships slice contains the ExtractedRelationship objects, and newRelIDs
// contains the database IDs of the newly created relationships.
func (d *ContradictionDetector) DetectAndInvalidate(ctx context.Context, newRelIDs []string, episodeTime time.Time) (*ContradictionResult, error) {
	return d.Detect(ctx, newRelIDs, episodeTime)
}

// IsExclusiveRelationType returns true if the relation type is mutually exclusive
// (only one can be current at a time for a given source entity).
func IsExclusiveRelationType(relType string) bool {
	return ExclusiveRelationTypes[relType]
}

// GetContradictingRelationships finds existing relationships that would be contradicted
// by a new relationship (without actually invalidating them). Useful for preview/dry-run.
func (d *ContradictionDetector) GetContradictingRelationships(ctx context.Context, sourceEntityID, relationType string, targetEntityID, targetLiteral *string) ([]string, error) {
	if !ExclusiveRelationTypes[relationType] {
		return nil, nil
	}

	var rows *sql.Rows
	var err error

	if targetEntityID != nil {
		rows, err = d.db.QueryContext(ctx, `
			SELECT id FROM relationships
			WHERE source_entity_id = ?
			  AND relation_type = ?
			  AND target_entity_id IS NOT NULL
			  AND target_entity_id != ?
			  AND invalid_at IS NULL
		`, sourceEntityID, relationType, *targetEntityID)
	} else if targetLiteral != nil {
		rows, err = d.db.QueryContext(ctx, `
			SELECT id FROM relationships
			WHERE source_entity_id = ?
			  AND relation_type = ?
			  AND target_literal IS NOT NULL
			  AND target_literal != ?
			  AND invalid_at IS NULL
		`, sourceEntityID, relationType, *targetLiteral)
	} else {
		return nil, nil
	}

	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var ids []string
	for rows.Next() {
		var id string
		if err := rows.Scan(&id); err != nil {
			return nil, err
		}
		ids = append(ids, id)
	}

	return ids, rows.Err()
}
