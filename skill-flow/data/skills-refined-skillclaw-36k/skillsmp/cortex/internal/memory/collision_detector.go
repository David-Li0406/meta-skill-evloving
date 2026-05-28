package memory

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"time"

	"github.com/google/uuid"
)

// Collision confidence thresholds
const (
	HardIdentifierConfidence     = 0.95 // Single hard identifier match (email, phone, handle)
	MultipleHardIDConfidence     = 0.99 // Multiple hard identifiers match
	CompoundNameBirthdateConf    = 0.90 // Name + birthdate match
	CompoundNameEmployerCityConf = 0.85 // Name + employer + city match
	SoftAccumulationMinConf      = 0.60 // Minimum for soft accumulation
)

// Hard identifier types for collision detection (not including shared aliases)
var HardIdentifierTypes = []string{"email", "phone", "handle"}

// CollisionReason describes why a collision was detected
type CollisionReason string

const (
	ReasonHardIdentifier    CollisionReason = "hard_identifier"
	ReasonMultipleHardIDs   CollisionReason = "multiple_hard_identifiers"
	ReasonCompound          CollisionReason = "compound"
	ReasonSoftAccumulation  CollisionReason = "soft_accumulation"
)

// Collision represents a detected collision between entities
type Collision struct {
	EntityAID     string                   `json:"entity_a_id"`
	EntityBID     string                   `json:"entity_b_id"`
	Confidence    float64                  `json:"confidence"`
	AutoEligible  bool                     `json:"auto_eligible"`
	Reason        CollisionReason          `json:"reason"`
	MatchingFacts []map[string]interface{} `json:"matching_facts"`
	Context       map[string]interface{}   `json:"context,omitempty"`
}

// CollisionDetectionResult contains the output of collision detection
type CollisionDetectionResult struct {
	Collisions       []Collision `json:"collisions"`
	CandidatesCreated int        `json:"candidates_created"`
	CandidatesUpdated int        `json:"candidates_updated"`
}

// CollisionDetector detects potential entity duplicates using an O(F) algorithm.
// It iterates through facts (aliases, relationships) rather than entity pairs,
// making it efficient for large entity sets.
type CollisionDetector struct {
	db *sql.DB
}

// NewCollisionDetector creates a new CollisionDetector.
func NewCollisionDetector(db *sql.DB) *CollisionDetector {
	return &CollisionDetector{db: db}
}

// DetectCollisions runs the full collision detection algorithm.
// Returns detected collisions and optionally creates merge_candidates.
func (d *CollisionDetector) DetectCollisions(ctx context.Context, createCandidates bool) (*CollisionDetectionResult, error) {
	result := &CollisionDetectionResult{
		Collisions: make([]Collision, 0),
	}

	// Phase 1: Hard identifier collisions (email, phone, handle)
	hardCollisions, err := d.detectHardIdentifierCollisions(ctx)
	if err != nil {
		return nil, fmt.Errorf("detect hard identifier collisions: %w", err)
	}
	result.Collisions = append(result.Collisions, hardCollisions...)

	// Phase 2: Compound matching (name + birthdate, name + employer)
	compoundCollisions, err := d.detectCompoundMatches(ctx)
	if err != nil {
		return nil, fmt.Errorf("detect compound matches: %w", err)
	}
	result.Collisions = append(result.Collisions, compoundCollisions...)

	// Deduplicate collisions (same entity pair may be detected multiple times)
	result.Collisions = d.deduplicateCollisions(result.Collisions)

	// Create merge candidates if requested
	if createCandidates {
		created, updated, err := d.createMergeCandidates(ctx, result.Collisions)
		if err != nil {
			return nil, fmt.Errorf("create merge candidates: %w", err)
		}
		result.CandidatesCreated = created
		result.CandidatesUpdated = updated
	}

	return result, nil
}

// detectHardIdentifierCollisions finds entities sharing the same hard identifiers.
// Uses O(F) algorithm: group aliases by value, find groups with multiple entities.
// CRITICAL: Shared aliases (is_shared=TRUE) do NOT trigger collisions.
func (d *CollisionDetector) detectHardIdentifierCollisions(ctx context.Context) ([]Collision, error) {
	var collisions []Collision

	for _, aliasType := range HardIdentifierTypes {
		// Find all aliases of this type where multiple non-merged entities share the same value
		// EXCLUDING shared aliases (they're intentional, e.g., family phone)
		rows, err := d.db.QueryContext(ctx, `
			SELECT ea.normalized, GROUP_CONCAT(DISTINCT ea.entity_id) as entity_ids
			FROM entity_aliases ea
			JOIN entities e ON ea.entity_id = e.id
			WHERE ea.alias_type = ?
			  AND ea.is_shared = FALSE
			  AND e.merged_into IS NULL
			GROUP BY ea.normalized
			HAVING COUNT(DISTINCT ea.entity_id) > 1
		`, aliasType)
		if err != nil {
			return nil, err
		}

		// Collect all collision data first (SQLite concurrent query limitation)
		type collisionData struct {
			normalized string
			entityIDs  string
		}
		var collisionRows []collisionData
		for rows.Next() {
			var cd collisionData
			if err := rows.Scan(&cd.normalized, &cd.entityIDs); err != nil {
				rows.Close()
				return nil, err
			}
			collisionRows = append(collisionRows, cd)
		}
		rows.Close()

		// Process collected data
		for _, cd := range collisionRows {
			entityIDs := splitCSV(cd.entityIDs)
			if len(entityIDs) < 2 {
				continue
			}

			// Create collision for each pair of entities
			// For efficiency, we create one candidate per pair (not all permutations)
			for i := 0; i < len(entityIDs)-1; i++ {
				for j := i + 1; j < len(entityIDs); j++ {
					collision := Collision{
						EntityAID:    entityIDs[i],
						EntityBID:    entityIDs[j],
						Confidence:   HardIdentifierConfidence,
						AutoEligible: true, // Hard identifier match = auto-eligible
						Reason:       ReasonHardIdentifier,
						MatchingFacts: []map[string]interface{}{
							{
								"type":  aliasType,
								"value": cd.normalized,
							},
						},
					}
					collisions = append(collisions, collision)
				}
			}
		}
	}

	// Upgrade confidence for entities with multiple hard identifier matches
	collisions = d.upgradeMultipleMatches(collisions)

	return collisions, nil
}

// upgradeMultipleMatches upgrades confidence for entity pairs with multiple hard identifier matches.
func (d *CollisionDetector) upgradeMultipleMatches(collisions []Collision) []Collision {
	// Count matches per entity pair
	pairFacts := make(map[string][]map[string]interface{})
	for _, c := range collisions {
		key := d.pairKey(c.EntityAID, c.EntityBID)
		pairFacts[key] = append(pairFacts[key], c.MatchingFacts...)
	}

	// Deduplicate and upgrade
	result := make([]Collision, 0)
	seen := make(map[string]bool)

	for _, c := range collisions {
		key := d.pairKey(c.EntityAID, c.EntityBID)
		if seen[key] {
			continue
		}
		seen[key] = true

		facts := pairFacts[key]
		if len(facts) > 1 {
			// Multiple hard identifiers match - upgrade to higher confidence
			c.Confidence = MultipleHardIDConfidence
			c.Reason = ReasonMultipleHardIDs
			c.MatchingFacts = facts
		}
		result = append(result, c)
	}

	return result
}

// detectCompoundMatches finds entities with compound identifier matches.
// Compound match types:
// - Name + birthdate (0.90 confidence)
// - Name + employer + city (0.85 confidence)
func (d *CollisionDetector) detectCompoundMatches(ctx context.Context) ([]Collision, error) {
	var collisions []Collision

	// Compound match 1: Name + birthdate
	nameBirthdateCollisions, err := d.detectNameBirthdateMatches(ctx)
	if err != nil {
		return nil, fmt.Errorf("detect name+birthdate matches: %w", err)
	}
	collisions = append(collisions, nameBirthdateCollisions...)

	// Compound match 2: Name + employer
	nameEmployerCollisions, err := d.detectNameEmployerMatches(ctx)
	if err != nil {
		return nil, fmt.Errorf("detect name+employer matches: %w", err)
	}
	collisions = append(collisions, nameEmployerCollisions...)

	return collisions, nil
}

// detectNameBirthdateMatches finds entities with matching name AND birthdate.
func (d *CollisionDetector) detectNameBirthdateMatches(ctx context.Context) ([]Collision, error) {
	// Find entities that share the same name (via aliases) AND have the same BORN_ON relationship
	rows, err := d.db.QueryContext(ctx, `
		SELECT
			ea1.entity_id as entity_a,
			ea2.entity_id as entity_b,
			ea1.normalized as name,
			r1.target_literal as birthdate
		FROM entity_aliases ea1
		JOIN entity_aliases ea2 ON ea1.normalized = ea2.normalized
			AND ea1.alias_type = ea2.alias_type
			AND ea1.entity_id < ea2.entity_id
		JOIN entities e1 ON ea1.entity_id = e1.id
		JOIN entities e2 ON ea2.entity_id = e2.id
		JOIN relationships r1 ON r1.source_entity_id = ea1.entity_id AND r1.relation_type = 'BORN_ON'
		JOIN relationships r2 ON r2.source_entity_id = ea2.entity_id AND r2.relation_type = 'BORN_ON'
		WHERE ea1.alias_type = 'name'
		  AND e1.merged_into IS NULL
		  AND e2.merged_into IS NULL
		  AND r1.target_literal = r2.target_literal
		  AND r1.target_literal IS NOT NULL
		  AND r1.invalid_at IS NULL
		  AND r2.invalid_at IS NULL
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var collisions []Collision
	for rows.Next() {
		var entityA, entityB, name, birthdate string
		if err := rows.Scan(&entityA, &entityB, &name, &birthdate); err != nil {
			continue
		}

		collisions = append(collisions, Collision{
			EntityAID:    entityA,
			EntityBID:    entityB,
			Confidence:   CompoundNameBirthdateConf,
			AutoEligible: true, // Name + birthdate is high confidence
			Reason:       ReasonCompound,
			MatchingFacts: []map[string]interface{}{
				{"type": "name", "value": name},
				{"type": "birthdate", "value": birthdate},
			},
			Context: map[string]interface{}{
				"compound_type": "name_birthdate",
			},
		})
	}

	return collisions, rows.Err()
}

// detectNameEmployerMatches finds entities with matching name AND employer.
func (d *CollisionDetector) detectNameEmployerMatches(ctx context.Context) ([]Collision, error) {
	// Find entities that share the same name AND work at the same company
	rows, err := d.db.QueryContext(ctx, `
		SELECT
			ea1.entity_id as entity_a,
			ea2.entity_id as entity_b,
			ea1.normalized as name,
			r1.target_entity_id as employer_id
		FROM entity_aliases ea1
		JOIN entity_aliases ea2 ON ea1.normalized = ea2.normalized
			AND ea1.alias_type = ea2.alias_type
			AND ea1.entity_id < ea2.entity_id
		JOIN entities e1 ON ea1.entity_id = e1.id
		JOIN entities e2 ON ea2.entity_id = e2.id
		JOIN relationships r1 ON r1.source_entity_id = ea1.entity_id AND r1.relation_type = 'WORKS_AT'
		JOIN relationships r2 ON r2.source_entity_id = ea2.entity_id AND r2.relation_type = 'WORKS_AT'
		WHERE ea1.alias_type = 'name'
		  AND e1.merged_into IS NULL
		  AND e2.merged_into IS NULL
		  AND r1.target_entity_id = r2.target_entity_id
		  AND r1.target_entity_id IS NOT NULL
		  AND r1.invalid_at IS NULL
		  AND r2.invalid_at IS NULL
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var collisions []Collision
	for rows.Next() {
		var entityA, entityB, name, employerID string
		if err := rows.Scan(&entityA, &entityB, &name, &employerID); err != nil {
			continue
		}

		collisions = append(collisions, Collision{
			EntityAID:    entityA,
			EntityBID:    entityB,
			Confidence:   CompoundNameEmployerCityConf,
			AutoEligible: false, // Name + employer needs review
			Reason:       ReasonCompound,
			MatchingFacts: []map[string]interface{}{
				{"type": "name", "value": name},
				{"type": "employer", "value": employerID},
			},
			Context: map[string]interface{}{
				"compound_type": "name_employer",
			},
		})
	}

	return collisions, rows.Err()
}

// deduplicateCollisions removes duplicate collisions for the same entity pair.
// Keeps the highest confidence collision for each pair.
func (d *CollisionDetector) deduplicateCollisions(collisions []Collision) []Collision {
	best := make(map[string]*Collision)

	for i := range collisions {
		c := &collisions[i]
		key := d.pairKey(c.EntityAID, c.EntityBID)

		if existing, ok := best[key]; ok {
			// Keep the one with higher confidence
			if c.Confidence > existing.Confidence {
				best[key] = c
			} else if c.Confidence == existing.Confidence {
				// Same confidence - merge matching facts
				existing.MatchingFacts = append(existing.MatchingFacts, c.MatchingFacts...)
			}
		} else {
			best[key] = c
		}
	}

	result := make([]Collision, 0, len(best))
	for _, c := range best {
		result = append(result, *c)
	}
	return result
}

// createMergeCandidates creates or updates merge_candidates records.
func (d *CollisionDetector) createMergeCandidates(ctx context.Context, collisions []Collision) (created, updated int, err error) {
	now := time.Now().Format(time.RFC3339)

	for _, c := range collisions {
		factsJSON, _ := json.Marshal(c.MatchingFacts)
		contextJSON, _ := json.Marshal(c.Context)

		// Check if candidate already exists
		var existingID string
		err := d.db.QueryRowContext(ctx, `
			SELECT id FROM merge_candidates
			WHERE (entity_a_id = ? AND entity_b_id = ?)
			   OR (entity_a_id = ? AND entity_b_id = ?)
		`, c.EntityAID, c.EntityBID, c.EntityBID, c.EntityAID).Scan(&existingID)

		if err == sql.ErrNoRows {
			// Create new candidate
			id := uuid.New().String()
			_, err = d.db.ExecContext(ctx, `
				INSERT INTO merge_candidates (
					id, entity_a_id, entity_b_id, confidence, auto_eligible,
					reason, matching_facts, context, status, created_at
				) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
			`, id, c.EntityAID, c.EntityBID, c.Confidence, c.AutoEligible,
				string(c.Reason), string(factsJSON), string(contextJSON), now)
			if err != nil {
				return created, updated, fmt.Errorf("insert merge_candidate: %w", err)
			}
			created++
		} else if err == nil {
			// Update existing candidate if new confidence is higher
			res, err := d.db.ExecContext(ctx, `
				UPDATE merge_candidates
				SET confidence = MAX(confidence, ?),
				    auto_eligible = auto_eligible OR ?,
				    matching_facts = ?,
				    context = ?,
				    reason = CASE WHEN ? > confidence THEN ? ELSE reason END
				WHERE id = ?
				  AND status = 'pending'
			`, c.Confidence, c.AutoEligible, string(factsJSON), string(contextJSON),
				c.Confidence, string(c.Reason), existingID)
			if err != nil {
				return created, updated, fmt.Errorf("update merge_candidate: %w", err)
			}
			if rows, _ := res.RowsAffected(); rows > 0 {
				updated++
			}
		} else {
			return created, updated, fmt.Errorf("check existing candidate: %w", err)
		}
	}

	return created, updated, nil
}

// pairKey creates a canonical key for an entity pair (order-independent)
func (d *CollisionDetector) pairKey(entityA, entityB string) string {
	if entityA < entityB {
		return entityA + "|" + entityB
	}
	return entityB + "|" + entityA
}

// DetectCollisionsForEntity detects collisions involving a specific entity.
// Useful for incremental detection after entity resolution.
func (d *CollisionDetector) DetectCollisionsForEntity(ctx context.Context, entityID string, createCandidates bool) (*CollisionDetectionResult, error) {
	result := &CollisionDetectionResult{
		Collisions: make([]Collision, 0),
	}

	// Phase 1: Check hard identifiers for this entity
	hardCollisions, err := d.detectHardIdentifierCollisionsForEntity(ctx, entityID)
	if err != nil {
		return nil, fmt.Errorf("detect hard identifier collisions for entity: %w", err)
	}
	result.Collisions = append(result.Collisions, hardCollisions...)

	// Phase 2: Check compound matches for this entity
	compoundCollisions, err := d.detectCompoundMatchesForEntity(ctx, entityID)
	if err != nil {
		return nil, fmt.Errorf("detect compound matches for entity: %w", err)
	}
	result.Collisions = append(result.Collisions, compoundCollisions...)

	// Deduplicate
	result.Collisions = d.deduplicateCollisions(result.Collisions)

	// Create merge candidates if requested
	if createCandidates {
		created, updated, err := d.createMergeCandidates(ctx, result.Collisions)
		if err != nil {
			return nil, fmt.Errorf("create merge candidates: %w", err)
		}
		result.CandidatesCreated = created
		result.CandidatesUpdated = updated
	}

	return result, nil
}

// detectHardIdentifierCollisionsForEntity finds hard identifier collisions for a specific entity.
func (d *CollisionDetector) detectHardIdentifierCollisionsForEntity(ctx context.Context, entityID string) ([]Collision, error) {
	var collisions []Collision

	for _, aliasType := range HardIdentifierTypes {
		// Find other entities with same alias values (excluding shared)
		rows, err := d.db.QueryContext(ctx, `
			SELECT ea2.entity_id, ea1.normalized
			FROM entity_aliases ea1
			JOIN entity_aliases ea2 ON ea1.normalized = ea2.normalized AND ea1.alias_type = ea2.alias_type
			JOIN entities e2 ON ea2.entity_id = e2.id
			WHERE ea1.entity_id = ?
			  AND ea1.alias_type = ?
			  AND ea1.is_shared = FALSE
			  AND ea2.is_shared = FALSE
			  AND ea2.entity_id != ?
			  AND e2.merged_into IS NULL
		`, entityID, aliasType, entityID)
		if err != nil {
			return nil, err
		}

		// Collect results first
		type match struct {
			otherEntityID string
			normalized    string
		}
		var matches []match
		for rows.Next() {
			var m match
			if err := rows.Scan(&m.otherEntityID, &m.normalized); err != nil {
				rows.Close()
				return nil, err
			}
			matches = append(matches, m)
		}
		rows.Close()

		// Create collisions
		for _, m := range matches {
			collisions = append(collisions, Collision{
				EntityAID:    entityID,
				EntityBID:    m.otherEntityID,
				Confidence:   HardIdentifierConfidence,
				AutoEligible: true,
				Reason:       ReasonHardIdentifier,
				MatchingFacts: []map[string]interface{}{
					{"type": aliasType, "value": m.normalized},
				},
			})
		}
	}

	// Upgrade for multiple matches
	return d.upgradeMultipleMatches(collisions), nil
}

// detectCompoundMatchesForEntity finds compound matches for a specific entity.
func (d *CollisionDetector) detectCompoundMatchesForEntity(ctx context.Context, entityID string) ([]Collision, error) {
	var collisions []Collision

	// Check name + birthdate
	nameBirthdateCollisions, err := d.detectNameBirthdateMatchesForEntity(ctx, entityID)
	if err != nil {
		return nil, err
	}
	collisions = append(collisions, nameBirthdateCollisions...)

	// Check name + employer
	nameEmployerCollisions, err := d.detectNameEmployerMatchesForEntity(ctx, entityID)
	if err != nil {
		return nil, err
	}
	collisions = append(collisions, nameEmployerCollisions...)

	return collisions, nil
}

// detectNameBirthdateMatchesForEntity finds name+birthdate matches for a specific entity.
func (d *CollisionDetector) detectNameBirthdateMatchesForEntity(ctx context.Context, entityID string) ([]Collision, error) {
	rows, err := d.db.QueryContext(ctx, `
		SELECT
			ea2.entity_id as other_entity,
			ea1.normalized as name,
			r1.target_literal as birthdate
		FROM entity_aliases ea1
		JOIN entity_aliases ea2 ON ea1.normalized = ea2.normalized
			AND ea1.alias_type = ea2.alias_type
		JOIN entities e2 ON ea2.entity_id = e2.id
		JOIN relationships r1 ON r1.source_entity_id = ea1.entity_id AND r1.relation_type = 'BORN_ON'
		JOIN relationships r2 ON r2.source_entity_id = ea2.entity_id AND r2.relation_type = 'BORN_ON'
		WHERE ea1.entity_id = ?
		  AND ea1.alias_type = 'name'
		  AND ea2.entity_id != ?
		  AND e2.merged_into IS NULL
		  AND r1.target_literal = r2.target_literal
		  AND r1.target_literal IS NOT NULL
		  AND r1.invalid_at IS NULL
		  AND r2.invalid_at IS NULL
	`, entityID, entityID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var collisions []Collision
	for rows.Next() {
		var otherEntity, name, birthdate string
		if err := rows.Scan(&otherEntity, &name, &birthdate); err != nil {
			continue
		}

		collisions = append(collisions, Collision{
			EntityAID:    entityID,
			EntityBID:    otherEntity,
			Confidence:   CompoundNameBirthdateConf,
			AutoEligible: true,
			Reason:       ReasonCompound,
			MatchingFacts: []map[string]interface{}{
				{"type": "name", "value": name},
				{"type": "birthdate", "value": birthdate},
			},
			Context: map[string]interface{}{
				"compound_type": "name_birthdate",
			},
		})
	}

	return collisions, rows.Err()
}

// detectNameEmployerMatchesForEntity finds name+employer matches for a specific entity.
func (d *CollisionDetector) detectNameEmployerMatchesForEntity(ctx context.Context, entityID string) ([]Collision, error) {
	rows, err := d.db.QueryContext(ctx, `
		SELECT
			ea2.entity_id as other_entity,
			ea1.normalized as name,
			r1.target_entity_id as employer_id
		FROM entity_aliases ea1
		JOIN entity_aliases ea2 ON ea1.normalized = ea2.normalized
			AND ea1.alias_type = ea2.alias_type
		JOIN entities e2 ON ea2.entity_id = e2.id
		JOIN relationships r1 ON r1.source_entity_id = ea1.entity_id AND r1.relation_type = 'WORKS_AT'
		JOIN relationships r2 ON r2.source_entity_id = ea2.entity_id AND r2.relation_type = 'WORKS_AT'
		WHERE ea1.entity_id = ?
		  AND ea1.alias_type = 'name'
		  AND ea2.entity_id != ?
		  AND e2.merged_into IS NULL
		  AND r1.target_entity_id = r2.target_entity_id
		  AND r1.target_entity_id IS NOT NULL
		  AND r1.invalid_at IS NULL
		  AND r2.invalid_at IS NULL
	`, entityID, entityID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var collisions []Collision
	for rows.Next() {
		var otherEntity, name, employerID string
		if err := rows.Scan(&otherEntity, &name, &employerID); err != nil {
			continue
		}

		collisions = append(collisions, Collision{
			EntityAID:    entityID,
			EntityBID:    otherEntity,
			Confidence:   CompoundNameEmployerCityConf,
			AutoEligible: false,
			Reason:       ReasonCompound,
			MatchingFacts: []map[string]interface{}{
				{"type": "name", "value": name},
				{"type": "employer", "value": employerID},
			},
			Context: map[string]interface{}{
				"compound_type": "name_employer",
			},
		})
	}

	return collisions, rows.Err()
}

// GetPendingMergeCandidates returns pending merge candidates ordered by confidence.
func (d *CollisionDetector) GetPendingMergeCandidates(ctx context.Context, limit int) ([]Collision, error) {
	if limit <= 0 {
		limit = 100
	}

	rows, err := d.db.QueryContext(ctx, `
		SELECT entity_a_id, entity_b_id, confidence, auto_eligible, reason, matching_facts, context
		FROM merge_candidates
		WHERE status = 'pending'
		ORDER BY confidence DESC, created_at ASC
		LIMIT ?
	`, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var collisions []Collision
	for rows.Next() {
		var c Collision
		var factsJSON, contextJSON sql.NullString
		var reasonStr string

		if err := rows.Scan(&c.EntityAID, &c.EntityBID, &c.Confidence, &c.AutoEligible,
			&reasonStr, &factsJSON, &contextJSON); err != nil {
			continue
		}

		c.Reason = CollisionReason(reasonStr)
		if factsJSON.Valid {
			_ = json.Unmarshal([]byte(factsJSON.String), &c.MatchingFacts)
		}
		if contextJSON.Valid {
			_ = json.Unmarshal([]byte(contextJSON.String), &c.Context)
		}

		collisions = append(collisions, c)
	}

	return collisions, rows.Err()
}

// GetAutoEligibleCandidates returns merge candidates that are eligible for automatic merging.
func (d *CollisionDetector) GetAutoEligibleCandidates(ctx context.Context) ([]Collision, error) {
	rows, err := d.db.QueryContext(ctx, `
		SELECT entity_a_id, entity_b_id, confidence, auto_eligible, reason, matching_facts, context
		FROM merge_candidates
		WHERE status = 'pending' AND auto_eligible = TRUE
		ORDER BY confidence DESC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var collisions []Collision
	for rows.Next() {
		var c Collision
		var factsJSON, contextJSON sql.NullString
		var reasonStr string

		if err := rows.Scan(&c.EntityAID, &c.EntityBID, &c.Confidence, &c.AutoEligible,
			&reasonStr, &factsJSON, &contextJSON); err != nil {
			continue
		}

		c.Reason = CollisionReason(reasonStr)
		if factsJSON.Valid {
			_ = json.Unmarshal([]byte(factsJSON.String), &c.MatchingFacts)
		}
		if contextJSON.Valid {
			_ = json.Unmarshal([]byte(contextJSON.String), &c.Context)
		}

		collisions = append(collisions, c)
	}

	return collisions, rows.Err()
}

// splitCSV splits a comma-separated string into a slice.
func splitCSV(s string) []string {
	if s == "" {
		return nil
	}
	var result []string
	for _, part := range stringsSplit(s, ",") {
		trimmed := stringsTrimSpace(part)
		if trimmed != "" {
			result = append(result, trimmed)
		}
	}
	return result
}

// Helper functions to avoid importing strings package multiple times
func stringsSplit(s, sep string) []string {
	var result []string
	start := 0
	for i := 0; i < len(s); i++ {
		if i+len(sep) <= len(s) && s[i:i+len(sep)] == sep {
			result = append(result, s[start:i])
			start = i + len(sep)
			i += len(sep) - 1
		}
	}
	result = append(result, s[start:])
	return result
}

func stringsTrimSpace(s string) string {
	start := 0
	end := len(s)
	for start < end && (s[start] == ' ' || s[start] == '\t' || s[start] == '\n' || s[start] == '\r') {
		start++
	}
	for end > start && (s[end-1] == ' ' || s[end-1] == '\t' || s[end-1] == '\n' || s[end-1] == '\r') {
		end--
	}
	return s[start:end]
}
