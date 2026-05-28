package memory

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/google/uuid"
)

// Conflict represents a reason why two entities might NOT be the same.
type Conflict struct {
	Type    string   `json:"type"`     // e.g., "different_phones", "different_birthdates"
	ValuesA []string `json:"values_a"` // Values for entity A
	ValuesB []string `json:"values_b"` // Values for entity B
}

// MergeCandidate represents a pending merge candidate from the database.
type MergeCandidate struct {
	ID               string                   `json:"id"`
	EntityAID        string                   `json:"entity_a_id"`
	EntityBID        string                   `json:"entity_b_id"`
	Confidence       float64                  `json:"confidence"`
	AutoEligible     bool                     `json:"auto_eligible"`
	Reason           string                   `json:"reason"`
	MatchingFacts    []map[string]interface{} `json:"matching_facts,omitempty"`
	Context          map[string]interface{}   `json:"context,omitempty"`
	Conflicts        []Conflict               `json:"conflicts,omitempty"`
	Status           string                   `json:"status"`
	CreatedAt        string                   `json:"created_at"`
	ResolvedAt       *string                  `json:"resolved_at,omitempty"`
	ResolvedBy       *string                  `json:"resolved_by,omitempty"`
	ResolutionReason *string                  `json:"resolution_reason,omitempty"`
}

// MergeResult contains the result of a merge operation.
type MergeResult struct {
	SourceEntityID string `json:"source_entity_id"` // Entity that was merged into target
	TargetEntityID string `json:"target_entity_id"` // Entity that remains
	MergeEventID   string `json:"merge_event_id"`
	AliasesMoved   int    `json:"aliases_moved"`
	RelationsMoved int    `json:"relations_moved"`
	MentionsMoved  int    `json:"mentions_moved"`
}

// ProcessMergeCandidatesResult contains the result of processing merge candidates.
type ProcessMergeCandidatesResult struct {
	Processed     int            `json:"processed"`
	AutoMerged    int            `json:"auto_merged"`
	Conflicts     int            `json:"conflicts"`
	NeedsReview   int            `json:"needs_review"`
	MergeResults  []*MergeResult `json:"merge_results,omitempty"`
}

// AutoMerger evaluates merge candidates and executes auto-merges when appropriate.
// It is conservative - false positives (wrongly merging different people) are much
// worse than duplicates (keeping them separate).
type AutoMerger struct {
	db *sql.DB
}

// NewAutoMerger creates a new AutoMerger.
func NewAutoMerger(db *sql.DB) *AutoMerger {
	return &AutoMerger{db: db}
}

// DetectConflicts checks for conflicts between two entities that would prevent merging.
// Conflicts include:
// - Different hard identifiers of the same type (both have phones, but different phones)
// - Different birthdates
func (m *AutoMerger) DetectConflicts(ctx context.Context, entityAID, entityBID string) ([]Conflict, error) {
	var conflicts []Conflict

	// Check for different hard identifiers (phone, email)
	for _, aliasType := range []string{"phone", "email"} {
		conflict, err := m.checkDifferentAliases(ctx, entityAID, entityBID, aliasType)
		if err != nil {
			return nil, fmt.Errorf("check different %ss: %w", aliasType, err)
		}
		if conflict != nil {
			conflicts = append(conflicts, *conflict)
		}
	}

	// Check for different birthdates
	birthdateConflict, err := m.checkDifferentBirthdates(ctx, entityAID, entityBID)
	if err != nil {
		return nil, fmt.Errorf("check different birthdates: %w", err)
	}
	if birthdateConflict != nil {
		conflicts = append(conflicts, *birthdateConflict)
	}

	return conflicts, nil
}

// checkDifferentAliases checks if both entities have aliases of the same type
// but with different values (no overlap).
func (m *AutoMerger) checkDifferentAliases(ctx context.Context, entityAID, entityBID, aliasType string) (*Conflict, error) {
	// Get aliases for entity A
	aliasesA, err := m.getEntityAliases(ctx, entityAID, aliasType)
	if err != nil {
		return nil, err
	}

	// Get aliases for entity B
	aliasesB, err := m.getEntityAliases(ctx, entityBID, aliasType)
	if err != nil {
		return nil, err
	}

	// Both must have aliases of this type for a conflict
	if len(aliasesA) == 0 || len(aliasesB) == 0 {
		return nil, nil
	}

	// Check if there's any overlap
	setA := make(map[string]bool)
	for _, a := range aliasesA {
		setA[a] = true
	}

	hasOverlap := false
	for _, b := range aliasesB {
		if setA[b] {
			hasOverlap = true
			break
		}
	}

	// If both have aliases but no overlap, that's a conflict
	if !hasOverlap {
		return &Conflict{
			Type:    fmt.Sprintf("different_%ss", aliasType),
			ValuesA: aliasesA,
			ValuesB: aliasesB,
		}, nil
	}

	return nil, nil
}

// getEntityAliases returns all aliases of a given type for an entity.
func (m *AutoMerger) getEntityAliases(ctx context.Context, entityID, aliasType string) ([]string, error) {
	rows, err := m.db.QueryContext(ctx, `
		SELECT normalized
		FROM entity_aliases
		WHERE entity_id = ? AND alias_type = ?
	`, entityID, aliasType)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var aliases []string
	for rows.Next() {
		var alias string
		if err := rows.Scan(&alias); err != nil {
			continue
		}
		aliases = append(aliases, alias)
	}

	return aliases, rows.Err()
}

// checkDifferentBirthdates checks if both entities have BORN_ON relationships
// with different dates.
func (m *AutoMerger) checkDifferentBirthdates(ctx context.Context, entityAID, entityBID string) (*Conflict, error) {
	birthdateA, err := m.getRelationshipTargetLiteral(ctx, entityAID, "BORN_ON")
	if err != nil {
		return nil, err
	}

	birthdateB, err := m.getRelationshipTargetLiteral(ctx, entityBID, "BORN_ON")
	if err != nil {
		return nil, err
	}

	// Both must have birthdates for a conflict
	if birthdateA == nil || birthdateB == nil {
		return nil, nil
	}

	// Different birthdates = conflict
	if *birthdateA != *birthdateB {
		return &Conflict{
			Type:    "different_birthdates",
			ValuesA: []string{*birthdateA},
			ValuesB: []string{*birthdateB},
		}, nil
	}

	return nil, nil
}

// getRelationshipTargetLiteral returns the target_literal for a specific relationship type.
// Returns nil if no such relationship exists.
func (m *AutoMerger) getRelationshipTargetLiteral(ctx context.Context, entityID, relationType string) (*string, error) {
	var literal sql.NullString
	err := m.db.QueryRowContext(ctx, `
		SELECT target_literal
		FROM relationships
		WHERE source_entity_id = ?
		  AND relation_type = ?
		  AND target_literal IS NOT NULL
		  AND invalid_at IS NULL
		ORDER BY created_at DESC
		LIMIT 1
	`, entityID, relationType).Scan(&literal)

	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}

	if literal.Valid {
		return &literal.String, nil
	}
	return nil, nil
}

// ShouldAutoMerge determines if a merge candidate should be auto-merged.
// Returns true only when confidence is high and there are no conflicts.
func (m *AutoMerger) ShouldAutoMerge(candidate *MergeCandidate) bool {
	// Rule 1: Must have no conflicts
	if len(candidate.Conflicts) > 0 {
		return false
	}

	// Rule 2: Hard identifier with high confidence (≥0.95)
	if candidate.Reason == string(ReasonHardIdentifier) || candidate.Reason == string(ReasonMultipleHardIDs) {
		if candidate.Confidence >= 0.95 {
			return true
		}
	}

	// Rule 3: Multiple hard identifiers match (any confidence, since confidence is already 0.99)
	hardMatches := m.countHardIdentifierMatches(candidate.MatchingFacts)
	if hardMatches >= 2 {
		return true
	}

	// Rule 4: Name + birthdate compound match (0.90 confidence)
	if candidate.Reason == string(ReasonCompound) {
		if ctx, ok := candidate.Context["compound_type"]; ok && ctx == "name_birthdate" {
			if candidate.Confidence >= 0.90 {
				return true
			}
		}
	}

	// Default: Don't auto-merge (require human review)
	return false
}

// countHardIdentifierMatches counts how many hard identifier matches are in the matching facts.
func (m *AutoMerger) countHardIdentifierMatches(facts []map[string]interface{}) int {
	count := 0
	for _, fact := range facts {
		if factType, ok := fact["type"].(string); ok {
			for _, hardType := range HardIdentifierTypes {
				if factType == hardType {
					count++
					break
				}
			}
		}
	}
	return count
}

// ExecuteMerge merges entity A into entity B (A is source, B is target).
// Source entity is marked as merged_into target; target entity remains active.
func (m *AutoMerger) ExecuteMerge(ctx context.Context, candidate *MergeCandidate, resolvedBy string) (*MergeResult, error) {
	sourceID := candidate.EntityAID // Will be merged into target
	targetID := candidate.EntityBID // Will remain

	result := &MergeResult{
		SourceEntityID: sourceID,
		TargetEntityID: targetID,
	}

	// Start transaction
	tx, err := m.db.BeginTx(ctx, nil)
	if err != nil {
		return nil, fmt.Errorf("begin transaction: %w", err)
	}
	defer tx.Rollback()

	// 1. Move all aliases from source to target
	aliasesMoved, err := m.moveAliases(ctx, tx, sourceID, targetID)
	if err != nil {
		return nil, fmt.Errorf("move aliases: %w", err)
	}
	result.AliasesMoved = aliasesMoved

	// 2. Update all relationships to point to target
	relationsMoved, err := m.moveRelationships(ctx, tx, sourceID, targetID)
	if err != nil {
		return nil, fmt.Errorf("move relationships: %w", err)
	}
	result.RelationsMoved = relationsMoved

	// 3. Move episode mentions
	mentionsMoved, err := m.moveMentions(ctx, tx, sourceID, targetID)
	if err != nil {
		return nil, fmt.Errorf("move mentions: %w", err)
	}
	result.MentionsMoved = mentionsMoved

	// 4. Update canonical name if source has a better name
	err = m.maybeUpdateCanonicalName(ctx, tx, sourceID, targetID)
	if err != nil {
		return nil, fmt.Errorf("update canonical name: %w", err)
	}

	// 5. Mark source as merged (don't delete for audit trail)
	targetName, err := m.getEntityCanonicalName(ctx, tx, targetID)
	if err != nil {
		return nil, fmt.Errorf("get target name: %w", err)
	}

	_, err = tx.ExecContext(ctx, `
		UPDATE entities
		SET merged_into = ?,
		    canonical_name = canonical_name || ' [MERGED→' || ? || ']',
		    updated_at = ?
		WHERE id = ?
	`, targetID, targetName, time.Now().Format(time.RFC3339), sourceID)
	if err != nil {
		return nil, fmt.Errorf("mark entity as merged: %w", err)
	}

	// 6. Log the merge event
	mergeEventID := uuid.New().String()
	triggeringFactsJSON, _ := json.Marshal(candidate.MatchingFacts)

	_, err = tx.ExecContext(ctx, `
		INSERT INTO entity_merge_events (
			id, source_entity_id, target_entity_id, merge_type,
			triggering_facts, similarity_score, created_at, resolved_by
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
	`, mergeEventID, sourceID, targetID, candidate.Reason,
		string(triggeringFactsJSON), candidate.Confidence,
		time.Now().Format(time.RFC3339), resolvedBy)
	if err != nil {
		return nil, fmt.Errorf("create merge event: %w", err)
	}
	result.MergeEventID = mergeEventID

	// 7. Update candidate status
	now := time.Now().Format(time.RFC3339)
	_, err = tx.ExecContext(ctx, `
		UPDATE merge_candidates
		SET status = 'merged',
		    resolved_at = ?,
		    resolved_by = ?
		WHERE id = ?
	`, now, resolvedBy, candidate.ID)
	if err != nil {
		return nil, fmt.Errorf("update candidate status: %w", err)
	}

	// Commit transaction
	if err := tx.Commit(); err != nil {
		return nil, fmt.Errorf("commit transaction: %w", err)
	}

	return result, nil
}

// moveAliases moves all aliases from source entity to target entity.
func (m *AutoMerger) moveAliases(ctx context.Context, tx *sql.Tx, sourceID, targetID string) (int, error) {
	res, err := tx.ExecContext(ctx, `
		UPDATE entity_aliases
		SET entity_id = ?
		WHERE entity_id = ?
	`, targetID, sourceID)
	if err != nil {
		return 0, err
	}

	rows, _ := res.RowsAffected()
	return int(rows), nil
}

// moveRelationships updates all relationships to point to target instead of source.
func (m *AutoMerger) moveRelationships(ctx context.Context, tx *sql.Tx, sourceID, targetID string) (int, error) {
	total := 0

	// Update source relationships
	res, err := tx.ExecContext(ctx, `
		UPDATE relationships
		SET source_entity_id = ?
		WHERE source_entity_id = ?
	`, targetID, sourceID)
	if err != nil {
		return 0, err
	}
	rows, _ := res.RowsAffected()
	total += int(rows)

	// Update target relationships
	res, err = tx.ExecContext(ctx, `
		UPDATE relationships
		SET target_entity_id = ?
		WHERE target_entity_id = ?
	`, targetID, sourceID)
	if err != nil {
		return 0, err
	}
	rows, _ = res.RowsAffected()
	total += int(rows)

	return total, nil
}

// moveMentions moves episode_entity_mentions from source to target.
// Uses INSERT OR REPLACE to handle cases where both entities are mentioned in same episode.
func (m *AutoMerger) moveMentions(ctx context.Context, tx *sql.Tx, sourceID, targetID string) (int, error) {
	// First, merge mentions where both entities appear in the same episode
	// (add mention counts together)
	_, err := tx.ExecContext(ctx, `
		INSERT OR REPLACE INTO episode_entity_mentions (episode_id, entity_id, mention_count, created_at)
		SELECT
			eem1.episode_id,
			? as entity_id,
			COALESCE(eem1.mention_count, 0) + COALESCE(eem2.mention_count, 0) as mention_count,
			MIN(eem1.created_at, COALESCE(eem2.created_at, eem1.created_at)) as created_at
		FROM episode_entity_mentions eem1
		LEFT JOIN episode_entity_mentions eem2
			ON eem1.episode_id = eem2.episode_id AND eem2.entity_id = ?
		WHERE eem1.entity_id = ?
	`, targetID, targetID, sourceID)
	if err != nil {
		return 0, err
	}

	// Then delete source mentions (we've already moved/merged them)
	res, err := tx.ExecContext(ctx, `
		DELETE FROM episode_entity_mentions
		WHERE entity_id = ?
	`, sourceID)
	if err != nil {
		return 0, err
	}

	rows, _ := res.RowsAffected()
	return int(rows), nil
}

// maybeUpdateCanonicalName updates the target's canonical name if source has a better name.
// "Better" means: more complete (longer but not excessively), or title-cased vs all-caps.
func (m *AutoMerger) maybeUpdateCanonicalName(ctx context.Context, tx *sql.Tx, sourceID, targetID string) error {
	sourceName, err := m.getEntityCanonicalNameTx(ctx, tx, sourceID)
	if err != nil {
		return err
	}

	targetName, err := m.getEntityCanonicalNameTx(ctx, tx, targetID)
	if err != nil {
		return err
	}

	if m.isBetterName(sourceName, targetName) {
		_, err = tx.ExecContext(ctx, `
			UPDATE entities
			SET canonical_name = ?, updated_at = ?
			WHERE id = ?
		`, sourceName, time.Now().Format(time.RFC3339), targetID)
		return err
	}

	return nil
}

// getEntityCanonicalName returns the canonical name for an entity.
func (m *AutoMerger) getEntityCanonicalName(ctx context.Context, tx *sql.Tx, entityID string) (string, error) {
	var name string
	err := tx.QueryRowContext(ctx, `
		SELECT canonical_name FROM entities WHERE id = ?
	`, entityID).Scan(&name)
	return name, err
}

// getEntityCanonicalNameTx returns the canonical name for an entity within a transaction.
func (m *AutoMerger) getEntityCanonicalNameTx(ctx context.Context, tx *sql.Tx, entityID string) (string, error) {
	var name string
	err := tx.QueryRowContext(ctx, `
		SELECT canonical_name FROM entities WHERE id = ?
	`, entityID).Scan(&name)
	return name, err
}

// isBetterName returns true if sourceName is "better" than targetName.
// Heuristics:
// - Title case is better than ALL CAPS
// - Full names are better than nicknames (Tyler > T)
// - Moderate length is better than too short or too long
func (m *AutoMerger) isBetterName(source, target string) bool {
	// Source is empty - target wins
	if source == "" {
		return false
	}

	// Target is empty - source wins
	if target == "" {
		return true
	}

	// Check for all caps (worse)
	sourceIsAllCaps := source == strings.ToUpper(source) && len(source) > 1
	targetIsAllCaps := target == strings.ToUpper(target) && len(target) > 1

	if !sourceIsAllCaps && targetIsAllCaps {
		return true
	}
	if sourceIsAllCaps && !targetIsAllCaps {
		return false
	}

	// Check length - prefer longer names (up to a point)
	// But not if they're way longer (might be a title or something)
	if len(source) > len(target) && len(source) < 50 && len(source) < len(target)*3 {
		return true
	}

	return false
}

// ProcessMergeCandidates processes all pending merge candidates.
// For each candidate:
// 1. Detect conflicts
// 2. Update candidate with conflict information
// 3. Auto-merge if eligible, otherwise leave for human review
func (m *AutoMerger) ProcessMergeCandidates(ctx context.Context) (*ProcessMergeCandidatesResult, error) {
	result := &ProcessMergeCandidatesResult{
		MergeResults: make([]*MergeResult, 0),
	}

	// Get all pending candidates
	candidates, err := m.GetPendingCandidates(ctx)
	if err != nil {
		return nil, fmt.Errorf("get pending candidates: %w", err)
	}

	for _, candidate := range candidates {
		result.Processed++

		// Detect conflicts for this pair
		conflicts, err := m.DetectConflicts(ctx, candidate.EntityAID, candidate.EntityBID)
		if err != nil {
			// Log but continue
			continue
		}
		candidate.Conflicts = conflicts

		// Update candidate with conflicts
		if len(conflicts) > 0 {
			err = m.updateCandidateConflicts(ctx, &candidate)
			if err != nil {
				// Log but continue
				continue
			}
			result.Conflicts++
			continue
		}

		// Check if should auto-merge
		if m.ShouldAutoMerge(&candidate) {
			mergeResult, err := m.ExecuteMerge(ctx, &candidate, "auto")
			if err != nil {
				// Log but continue
				continue
			}
			result.AutoMerged++
			result.MergeResults = append(result.MergeResults, mergeResult)
		} else {
			result.NeedsReview++
		}
	}

	return result, nil
}

// GetPendingCandidates returns all pending merge candidates.
func (m *AutoMerger) GetPendingCandidates(ctx context.Context) ([]MergeCandidate, error) {
	rows, err := m.db.QueryContext(ctx, `
		SELECT id, entity_a_id, entity_b_id, confidence, auto_eligible,
		       reason, matching_facts, context, conflicts, status, created_at,
		       resolved_at, resolved_by, resolution_reason
		FROM merge_candidates
		WHERE status = 'pending'
		ORDER BY confidence DESC, created_at ASC
	`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var candidates []MergeCandidate
	for rows.Next() {
		var c MergeCandidate
		var matchingFactsJSON, contextJSON, conflictsJSON sql.NullString
		var resolvedAt, resolvedBy, resolutionReason sql.NullString

		err := rows.Scan(
			&c.ID, &c.EntityAID, &c.EntityBID, &c.Confidence, &c.AutoEligible,
			&c.Reason, &matchingFactsJSON, &contextJSON, &conflictsJSON, &c.Status, &c.CreatedAt,
			&resolvedAt, &resolvedBy, &resolutionReason,
		)
		if err != nil {
			continue
		}

		if matchingFactsJSON.Valid {
			_ = json.Unmarshal([]byte(matchingFactsJSON.String), &c.MatchingFacts)
		}
		if contextJSON.Valid {
			_ = json.Unmarshal([]byte(contextJSON.String), &c.Context)
		}
		if conflictsJSON.Valid {
			_ = json.Unmarshal([]byte(conflictsJSON.String), &c.Conflicts)
		}
		if resolvedAt.Valid {
			c.ResolvedAt = &resolvedAt.String
		}
		if resolvedBy.Valid {
			c.ResolvedBy = &resolvedBy.String
		}
		if resolutionReason.Valid {
			c.ResolutionReason = &resolutionReason.String
		}

		candidates = append(candidates, c)
	}

	return candidates, rows.Err()
}

// updateCandidateConflicts updates a merge candidate with detected conflicts.
func (m *AutoMerger) updateCandidateConflicts(ctx context.Context, candidate *MergeCandidate) error {
	conflictsJSON, _ := json.Marshal(candidate.Conflicts)

	_, err := m.db.ExecContext(ctx, `
		UPDATE merge_candidates
		SET conflicts = ?,
		    auto_eligible = FALSE
		WHERE id = ?
	`, string(conflictsJSON), candidate.ID)

	return err
}

// RejectCandidate marks a merge candidate as rejected.
func (m *AutoMerger) RejectCandidate(ctx context.Context, candidateID, resolvedBy, reason string) error {
	now := time.Now().Format(time.RFC3339)
	_, err := m.db.ExecContext(ctx, `
		UPDATE merge_candidates
		SET status = 'rejected',
		    resolved_at = ?,
		    resolved_by = ?,
		    resolution_reason = ?
		WHERE id = ?
	`, now, resolvedBy, reason, candidateID)
	return err
}

// DeferCandidate marks a merge candidate as deferred (needs more information).
func (m *AutoMerger) DeferCandidate(ctx context.Context, candidateID, resolvedBy, reason string) error {
	now := time.Now().Format(time.RFC3339)
	_, err := m.db.ExecContext(ctx, `
		UPDATE merge_candidates
		SET status = 'deferred',
		    resolved_at = ?,
		    resolved_by = ?,
		    resolution_reason = ?
		WHERE id = ?
	`, now, resolvedBy, reason, candidateID)
	return err
}

// GetCandidateByID returns a merge candidate by ID.
func (m *AutoMerger) GetCandidateByID(ctx context.Context, candidateID string) (*MergeCandidate, error) {
	var c MergeCandidate
	var matchingFactsJSON, contextJSON, conflictsJSON sql.NullString
	var resolvedAt, resolvedBy, resolutionReason sql.NullString

	err := m.db.QueryRowContext(ctx, `
		SELECT id, entity_a_id, entity_b_id, confidence, auto_eligible,
		       reason, matching_facts, context, conflicts, status, created_at,
		       resolved_at, resolved_by, resolution_reason
		FROM merge_candidates
		WHERE id = ?
	`, candidateID).Scan(
		&c.ID, &c.EntityAID, &c.EntityBID, &c.Confidence, &c.AutoEligible,
		&c.Reason, &matchingFactsJSON, &contextJSON, &conflictsJSON, &c.Status, &c.CreatedAt,
		&resolvedAt, &resolvedBy, &resolutionReason,
	)
	if err != nil {
		return nil, err
	}

	if matchingFactsJSON.Valid {
		_ = json.Unmarshal([]byte(matchingFactsJSON.String), &c.MatchingFacts)
	}
	if contextJSON.Valid {
		_ = json.Unmarshal([]byte(contextJSON.String), &c.Context)
	}
	if conflictsJSON.Valid {
		_ = json.Unmarshal([]byte(conflictsJSON.String), &c.Conflicts)
	}
	if resolvedAt.Valid {
		c.ResolvedAt = &resolvedAt.String
	}
	if resolvedBy.Valid {
		c.ResolvedBy = &resolvedBy.String
	}
	if resolutionReason.Valid {
		c.ResolutionReason = &resolutionReason.String
	}

	return &c, nil
}

// GetMergeHistory returns the merge events for a given target entity.
func (m *AutoMerger) GetMergeHistory(ctx context.Context, targetEntityID string) ([]map[string]interface{}, error) {
	rows, err := m.db.QueryContext(ctx, `
		SELECT id, source_entity_id, target_entity_id, merge_type,
		       triggering_facts, similarity_score, created_at, resolved_by
		FROM entity_merge_events
		WHERE target_entity_id = ?
		ORDER BY created_at DESC
	`, targetEntityID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var events []map[string]interface{}
	for rows.Next() {
		var id, sourceID, targetID, mergeType string
		var triggeringFactsJSON sql.NullString
		var similarityScore sql.NullFloat64
		var createdAt string
		var resolvedBy sql.NullString

		err := rows.Scan(&id, &sourceID, &targetID, &mergeType,
			&triggeringFactsJSON, &similarityScore, &createdAt, &resolvedBy)
		if err != nil {
			continue
		}

		event := map[string]interface{}{
			"id":               id,
			"source_entity_id": sourceID,
			"target_entity_id": targetID,
			"merge_type":       mergeType,
			"created_at":       createdAt,
		}

		if triggeringFactsJSON.Valid {
			var facts interface{}
			if json.Unmarshal([]byte(triggeringFactsJSON.String), &facts) == nil {
				event["triggering_facts"] = facts
			}
		}
		if similarityScore.Valid {
			event["similarity_score"] = similarityScore.Float64
		}
		if resolvedBy.Valid {
			event["resolved_by"] = resolvedBy.String
		}

		events = append(events, event)
	}

	return events, rows.Err()
}
