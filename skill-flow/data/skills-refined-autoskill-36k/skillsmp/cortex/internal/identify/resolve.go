package identify

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"time"

	"github.com/google/uuid"
)

// MergeEvent represents a proposed or executed identity merge
type MergeEvent struct {
	ID              string
	SourcePersonID  string
	TargetPersonID  string
	MergeType       string  // hard_identifier, compound, soft_accumulation, manual
	TriggeringFacts []TriggeringFact
	SimilarityScore float64
	Status          string // pending, accepted, rejected, executed
	AutoEligible    bool
	CreatedAt       time.Time
	ResolvedAt      *time.Time
	ResolvedBy      *string
}

// TriggeringFact captures the fact that triggered a merge suggestion
type TriggeringFact struct {
	FactType  string `json:"fact_type"`
	FactValue string `json:"fact_value"`
}

// ResolutionResult holds the results of running the resolution algorithm
type ResolutionResult struct {
	HardCollisions      int
	CompoundMatches     int
	SoftAccumulations   int
	MergeSuggestionsCreated int
	AutoMergesExecuted  int
	Errors              int
}

// DetectHardIDCollisions finds person pairs sharing hard identifiers
// Uses GROUP BY fact_value HAVING COUNT > 1 pattern (O(F) not O(P²))
func DetectHardIDCollisions(db *sql.DB) ([]FactCollision, error) {
	return FindAllHardIdentifierCollisions(db)
}

// DetectTier1IDCollisions finds collisions for Tier 1 identifiers only
func DetectTier1IDCollisions(db *sql.DB) ([]FactCollision, error) {
	return FindTier1IdentifierCollisions(db)
}
// DetectHardIDCollisionsByType finds collisions for a specific hard identifier type
func DetectHardIDCollisionsByType(db *sql.DB, factType string) ([]FactCollision, error) {
	return FindFactCollisions(db, factType)
}

// CompoundMatch represents a match based on multiple facts
type CompoundMatch struct {
	Person1ID      string
	Person2ID      string
	MatchingFacts  []TriggeringFact
	CompoundType   string  // "name_birthdate", "name_employer_city", etc.
	Confidence     float64
}

// DetectCompoundMatches finds persons matching compound identifiers
// Compound matches: name+birthdate, name+employer+city, name+spouse+children
func DetectCompoundMatches(db *sql.DB) ([]CompoundMatch, error) {
	var matches []CompoundMatch

	// 1. Name + Birthdate match
	rows, err := db.Query(`
		SELECT pf1.person_id, pf2.person_id, pf1.fact_value as name, pf3.fact_value as birthdate
		FROM person_facts pf1
		JOIN person_facts pf2 ON pf1.fact_type = pf2.fact_type 
			AND pf1.fact_value = pf2.fact_value 
			AND pf1.person_id < pf2.person_id
		JOIN person_facts pf3 ON pf1.person_id = pf3.person_id AND pf3.fact_type = ?
		JOIN person_facts pf4 ON pf2.person_id = pf4.person_id AND pf4.fact_type = ?
			AND pf3.fact_value = pf4.fact_value
		WHERE pf1.fact_type = ?
	`, FactTypeBirthdate, FactTypeBirthdate, FactTypeFullLegalName)
	if err != nil {
		return nil, fmt.Errorf("name+birthdate query: %w", err)
	}

	for rows.Next() {
		var p1, p2, name, birthdate string
		if err := rows.Scan(&p1, &p2, &name, &birthdate); err != nil {
			rows.Close()
			return nil, err
		}
		matches = append(matches, CompoundMatch{
			Person1ID:     p1,
			Person2ID:     p2,
			CompoundType:  "name_birthdate",
			Confidence:    0.90,
			MatchingFacts: []TriggeringFact{
				{FactType: FactTypeFullLegalName, FactValue: name},
				{FactType: FactTypeBirthdate, FactValue: birthdate},
			},
		})
	}
	rows.Close()

	// 2. Name + Employer + Location match
	rows, err = db.Query(`
		SELECT DISTINCT pf_name1.person_id, pf_name2.person_id, 
			pf_name1.fact_value as name, 
			pf_emp1.fact_value as employer,
			pf_loc1.fact_value as location
		FROM person_facts pf_name1
		JOIN person_facts pf_name2 ON pf_name1.fact_type = pf_name2.fact_type 
			AND pf_name1.fact_value = pf_name2.fact_value 
			AND pf_name1.person_id < pf_name2.person_id
		JOIN person_facts pf_emp1 ON pf_name1.person_id = pf_emp1.person_id 
			AND pf_emp1.fact_type = ?
		JOIN person_facts pf_emp2 ON pf_name2.person_id = pf_emp2.person_id 
			AND pf_emp2.fact_type = ? 
			AND pf_emp1.fact_value = pf_emp2.fact_value
		JOIN person_facts pf_loc1 ON pf_name1.person_id = pf_loc1.person_id 
			AND pf_loc1.fact_type = ?
		JOIN person_facts pf_loc2 ON pf_name2.person_id = pf_loc2.person_id 
			AND pf_loc2.fact_type = ? 
			AND pf_loc1.fact_value = pf_loc2.fact_value
		WHERE pf_name1.fact_type IN (?, ?)
	`, FactTypeEmployerCurrent, FactTypeEmployerCurrent,
		FactTypeLocationCurrent, FactTypeLocationCurrent,
		FactTypeFullLegalName, FactTypeGivenName)
	if err != nil {
		return nil, fmt.Errorf("name+employer+city query: %w", err)
	}

	for rows.Next() {
		var p1, p2, name, employer, location string
		if err := rows.Scan(&p1, &p2, &name, &employer, &location); err != nil {
			rows.Close()
			return nil, err
		}
		matches = append(matches, CompoundMatch{
			Person1ID:     p1,
			Person2ID:     p2,
			CompoundType:  "name_employer_city",
			Confidence:    0.85,
			MatchingFacts: []TriggeringFact{
				{FactType: "name", FactValue: name},
				{FactType: FactTypeEmployerCurrent, FactValue: employer},
				{FactType: FactTypeLocationCurrent, FactValue: location},
			},
		})
	}
	rows.Close()

	return matches, nil
}

// SoftIdentifierScore represents similarity between two persons based on soft identifiers
type SoftIdentifierScore struct {
	Person1ID      string
	Person2ID      string
	Score          float64
	MatchingFacts  []TriggeringFact
}

// ScoreSoftIdentifiers calculates similarity scores between persons
// Uses weighted soft identifiers, iterates through facts O(F), not person pairs O(P²)
func ScoreSoftIdentifiers(db *sql.DB) ([]SoftIdentifierScore, error) {
	// Cap pair explosion for overly common values (e.g., "Austin", "Engineer").
	// These are too ambiguous to be useful and can blow up runtime.
	const maxSoftGroupSize = 50

	// Map of (person1, person2) -> accumulated score and matching facts
	type pairKey struct{ p1, p2 string }
	scores := make(map[pairKey]*SoftIdentifierScore)

	for factType, weight := range SoftIdentifierWeights {
		collisions, err := FindFactCollisions(db, factType)
		if err != nil {
			continue
		}

		for _, collision := range collisions {
			if len(collision.PersonIDs) > maxSoftGroupSize {
				continue
			}
			// For each collision, update scores for all person pairs
			for i := 0; i < len(collision.PersonIDs); i++ {
				for j := i + 1; j < len(collision.PersonIDs); j++ {
					p1, p2 := collision.PersonIDs[i], collision.PersonIDs[j]
					// Ensure consistent ordering
					if p1 > p2 {
						p1, p2 = p2, p1
					}

					key := pairKey{p1, p2}
					if scores[key] == nil {
						scores[key] = &SoftIdentifierScore{
							Person1ID: p1,
							Person2ID: p2,
						}
					}
					scores[key].Score += weight
					scores[key].MatchingFacts = append(scores[key].MatchingFacts, TriggeringFact{
						FactType:  factType,
						FactValue: collision.FactValue,
					})
				}
			}
		}
	}

	// Convert map to slice and filter by threshold
	var results []SoftIdentifierScore
	for _, score := range scores {
		if score.Score >= 0.4 { // Keep scores above threshold for potential suggestions
			results = append(results, *score)
		}
	}

	return results, nil
}

// GenerateMergeSuggestions creates merge_events from collision detection results
func GenerateMergeSuggestions(db *sql.DB, includeSoft bool, tier1Only bool) (*ResolutionResult, error) {
	result := &ResolutionResult{}
	now := time.Now().Unix()

	// Cache existing merge pairs to avoid per-pair DB lookups.
	type pairKey struct{ p1, p2 string }
	existing := make(map[pairKey]struct{})
	rows, err := db.Query(`
		SELECT source_person_id, target_person_id
		FROM merge_events
	`)
	if err == nil {
		for rows.Next() {
			var p1, p2 string
			if err := rows.Scan(&p1, &p2); err != nil {
				continue
			}
			if p1 > p2 {
				p1, p2 = p2, p1
			}
			existing[pairKey{p1, p2}] = struct{}{}
		}
		rows.Close()
	}

	// Phase 1: Tier 1 (or hard) identifier collisions
	const maxHardGroupSize = 50
	var hardCollisions []FactCollision
	if tier1Only {
		hardCollisions, err = DetectTier1IDCollisions(db)
	} else {
		hardCollisions, err = DetectHardIDCollisions(db)
	}
	if err != nil {
		return nil, fmt.Errorf("detect hard collisions: %w", err)
	}

	for _, collision := range hardCollisions {
		if len(collision.PersonIDs) > maxHardGroupSize {
			continue
		}
		result.HardCollisions++
		for i := 0; i < len(collision.PersonIDs); i++ {
			for j := i + 1; j < len(collision.PersonIDs); j++ {
				p1, p2 := collision.PersonIDs[i], collision.PersonIDs[j]
				if p1 > p2 {
					p1, p2 = p2, p1
				}

				if _, ok := existing[pairKey{p1, p2}]; ok {
					continue
				}

				triggeringFacts := []TriggeringFact{{
					FactType:  collision.FactType,
					FactValue: collision.FactValue,
				}}
				factsJSON, _ := json.Marshal(triggeringFacts)

				// High confidence hard ID match - auto eligible if confidence >= 0.8
				autoEligible := collision.Confidence >= 0.8

				_, err := db.Exec(`
					INSERT INTO merge_events (id, source_person_id, target_person_id, merge_type,
						triggering_facts, similarity_score, status, auto_eligible, created_at)
					VALUES (?, ?, ?, 'hard_identifier', ?, ?, 'pending', ?, ?)
				`, uuid.New().String(), p1, p2, string(factsJSON), collision.Confidence,
					boolToInt(autoEligible), now)
				if err == nil {
					result.MergeSuggestionsCreated++
					existing[pairKey{p1, p2}] = struct{}{}
				}
			}
		}
	}

	// Phase 2: Compound matches (Tier 2)
	if !tier1Only {
		compoundMatches, err := DetectCompoundMatches(db)
		if err != nil {
			return nil, fmt.Errorf("detect compound matches: %w", err)
		}

		for _, match := range compoundMatches {
			result.CompoundMatches++
			p1, p2 := match.Person1ID, match.Person2ID
			if p1 > p2 {
				p1, p2 = p2, p1
			}

			if _, ok := existing[pairKey{p1, p2}]; ok {
				continue
			}

			factsJSON, _ := json.Marshal(match.MatchingFacts)

			_, err := db.Exec(`
				INSERT INTO merge_events (id, source_person_id, target_person_id, merge_type,
					triggering_facts, similarity_score, status, auto_eligible, created_at)
				VALUES (?, ?, ?, 'compound', ?, ?, 'pending', 1, ?)
			`, uuid.New().String(), p1, p2, string(factsJSON), match.Confidence, now)
			if err == nil {
				result.MergeSuggestionsCreated++
				existing[pairKey{p1, p2}] = struct{}{}
			}
		}
	}

	// Phase 3: Soft identifier accumulation (Tier 2)
	if includeSoft && !tier1Only {
		softScores, err := ScoreSoftIdentifiers(db)
		if err != nil {
			return nil, fmt.Errorf("score soft identifiers: %w", err)
		}

		for _, score := range softScores {
			if score.Score < 0.6 {
				continue // Only create suggestions for score >= 0.6
			}
			result.SoftAccumulations++

			p1, p2 := score.Person1ID, score.Person2ID
			if p1 > p2 {
				p1, p2 = p2, p1
			}

			if _, ok := existing[pairKey{p1, p2}]; ok {
				continue
			}

			factsJSON, _ := json.Marshal(score.MatchingFacts)

			// Soft accumulation - generally not auto-eligible
			_, err := db.Exec(`
				INSERT INTO merge_events (id, source_person_id, target_person_id, merge_type,
					triggering_facts, similarity_score, status, auto_eligible, created_at)
				VALUES (?, ?, ?, 'soft_accumulation', ?, ?, 'pending', 0, ?)
			`, uuid.New().String(), p1, p2, string(factsJSON), score.Score, now)
			if err == nil {
				result.MergeSuggestionsCreated++
				existing[pairKey{p1, p2}] = struct{}{}
			}
		}
	}

	return result, nil
}

// ExecuteAutoMerges executes all auto-eligible pending merges
func ExecuteAutoMerges(db *sql.DB) (int, error) {
	// Get all auto-eligible pending merges
	rows, err := db.Query(`
		SELECT id, source_person_id, target_person_id
		FROM merge_events
		WHERE status = 'pending' AND auto_eligible = 1
	`)
	if err != nil {
		return 0, fmt.Errorf("query auto merges: %w", err)
	}

	var merges []struct {
		ID       string
		SourceID string
		TargetID string
	}
	for rows.Next() {
		var m struct {
			ID       string
			SourceID string
			TargetID string
		}
		if err := rows.Scan(&m.ID, &m.SourceID, &m.TargetID); err != nil {
			rows.Close()
			return 0, err
		}
		merges = append(merges, m)
	}
	rows.Close()

	executed := 0
	for _, m := range merges {
		err := ExecuteMerge(db, m.ID, m.SourceID, m.TargetID)
		if err != nil {
			continue
		}
		executed++
	}

	return executed, nil
}

// ExecuteMerge performs the actual merge operation
func ExecuteMerge(db *sql.DB, mergeEventID, sourcePersonID, targetPersonID string) error {
	// Check for conflicting facts before merge
	hasConflict, err := hasConflictingFacts(db, sourcePersonID, targetPersonID)
	if err != nil {
		return fmt.Errorf("check conflicts: %w", err)
	}

	now := time.Now().Unix()

	if hasConflict {
		// Downgrade to manual review
		_, err := db.Exec(`
			UPDATE merge_events 
			SET auto_eligible = 0, status = 'pending'
			WHERE id = ?
		`, mergeEventID)
		return err
	}

	// Execute merge in transaction
	tx, err := db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// Move facts from source to target
	_, err = tx.Exec(`
		UPDATE person_facts 
		SET person_id = ?
		WHERE person_id = ?
	`, targetPersonID, sourcePersonID)
	if err != nil {
		return fmt.Errorf("move facts: %w", err)
	}

	// Move identities from source to target
	_, err = tx.Exec(`
		UPDATE identities 
		SET person_id = ?
		WHERE person_id = ?
	`, targetPersonID, sourcePersonID)
	if err != nil {
		return fmt.Errorf("move identities: %w", err)
	}

	// Update event_participants to point to target
	_, err = tx.Exec(`
		UPDATE OR IGNORE event_participants 
		SET person_id = ?
		WHERE person_id = ?
	`, targetPersonID, sourcePersonID)
	if err != nil {
		return fmt.Errorf("update participants: %w", err)
	}

	// Mark source person as merged (if persons table has merged_into column)
	// Note: Using UPDATE since column may not exist
	tx.Exec(`
		UPDATE persons 
		SET canonical_name = canonical_name || ' [MERGED→' || ? || ']'
		WHERE id = ?
	`, targetPersonID[:8], sourcePersonID)

	// Update merge event status
	_, err = tx.Exec(`
		UPDATE merge_events 
		SET status = 'executed', resolved_at = ?, resolved_by = 'auto'
		WHERE id = ?
	`, now, mergeEventID)
	if err != nil {
		return fmt.Errorf("update merge event: %w", err)
	}

	return tx.Commit()
}

// hasConflictingFacts checks if two persons have conflicting facts
// (e.g., different birthdates, different SSNs)
func hasConflictingFacts(db *sql.DB, person1ID, person2ID string) (bool, error) {
	// Check for conflicting unique facts (birthdate, SSN, etc.)
	conflictTypes := []string{
		FactTypeBirthdate,
		FactTypeSSN,
		FactTypePassportNumber,
		FactTypeDriversLicense,
	}

	for _, factType := range conflictTypes {
		var val1, val2 sql.NullString
		db.QueryRow(`
			SELECT fact_value FROM person_facts 
			WHERE person_id = ? AND fact_type = ?
		`, person1ID, factType).Scan(&val1)
		db.QueryRow(`
			SELECT fact_value FROM person_facts 
			WHERE person_id = ? AND fact_type = ?
		`, person2ID, factType).Scan(&val2)

		if val1.Valid && val2.Valid && val1.String != val2.String {
			return true, nil
		}
	}

	return false, nil
}

// RunFullResolution runs the complete identity resolution pipeline
func RunFullResolution(db *sql.DB, autoMerge bool, includeSoft bool, tier1Only bool) (*ResolutionResult, error) {
	// Generate all merge suggestions
	result, err := GenerateMergeSuggestions(db, includeSoft, tier1Only)
	if err != nil {
		return nil, err
	}

	// Optionally execute auto-merges
	if autoMerge {
		executed, err := ExecuteAutoMerges(db)
		if err != nil {
			return nil, fmt.Errorf("execute auto merges: %w", err)
		}
		result.AutoMergesExecuted = executed
	}

	return result, nil
}

// ListPendingMerges returns all pending merge events
func ListPendingMerges(db *sql.DB, status string, limit int) ([]MergeEvent, error) {
	query := `
		SELECT id, source_person_id, target_person_id, merge_type,
			triggering_facts, similarity_score, status, auto_eligible, created_at
		FROM merge_events
		WHERE status = ?
		ORDER BY similarity_score DESC
		LIMIT ?
	`

	rows, err := db.Query(query, status, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var merges []MergeEvent
	for rows.Next() {
		var m MergeEvent
		var factsJSON string
		var autoEligible int
		var createdAt int64

		err := rows.Scan(&m.ID, &m.SourcePersonID, &m.TargetPersonID, &m.MergeType,
			&factsJSON, &m.SimilarityScore, &m.Status, &autoEligible, &createdAt)
		if err != nil {
			return nil, err
		}

		json.Unmarshal([]byte(factsJSON), &m.TriggeringFacts)
		m.AutoEligible = autoEligible == 1
		m.CreatedAt = time.Unix(createdAt, 0)

		merges = append(merges, m)
	}

	return merges, rows.Err()
}

// AcceptMergeEvent accepts a merge suggestion and executes it
func AcceptMergeEvent(db *sql.DB, mergeEventID string) error {
	var sourceID, targetID string
	err := db.QueryRow(`
		SELECT source_person_id, target_person_id FROM merge_events WHERE id = ?
	`, mergeEventID).Scan(&sourceID, &targetID)
	if err != nil {
		return fmt.Errorf("get merge event: %w", err)
	}

	return ExecuteMerge(db, mergeEventID, sourceID, targetID)
}

// RejectMergeEvent rejects a merge suggestion
func RejectMergeEvent(db *sql.DB, mergeEventID string) error {
	now := time.Now().Unix()
	_, err := db.Exec(`
		UPDATE merge_events 
		SET status = 'rejected', resolved_at = ?, resolved_by = 'user'
		WHERE id = ?
	`, now, mergeEventID)
	return err
}

// GetResolutionStats returns statistics about the identity resolution state
type ResolutionStats struct {
	ActivePersons       int
	MergedPersons       int
	TotalFacts          int
	HardIdentifiers     int
	PendingMerges       int
	AutoEligibleMerges  int
	UnresolvedFacts     int
	CrossChannelLinked  int
}

func GetResolutionStats(db *sql.DB) (*ResolutionStats, error) {
	stats := &ResolutionStats{}

	db.QueryRow(`SELECT COUNT(*) FROM persons WHERE canonical_name NOT LIKE '%[MERGED%'`).Scan(&stats.ActivePersons)
	db.QueryRow(`SELECT COUNT(*) FROM persons WHERE canonical_name LIKE '%[MERGED%'`).Scan(&stats.MergedPersons)
	db.QueryRow(`SELECT COUNT(*) FROM person_facts`).Scan(&stats.TotalFacts)
	db.QueryRow(`SELECT COUNT(*) FROM person_facts WHERE is_hard_identifier = 1`).Scan(&stats.HardIdentifiers)
	db.QueryRow(`SELECT COUNT(*) FROM merge_events WHERE status = 'pending'`).Scan(&stats.PendingMerges)
	db.QueryRow(`SELECT COUNT(*) FROM merge_events WHERE status = 'pending' AND auto_eligible = 1`).Scan(&stats.AutoEligibleMerges)
	db.QueryRow(`SELECT COUNT(*) FROM unattributed_facts WHERE resolved_to_person_id IS NULL`).Scan(&stats.UnresolvedFacts)

	// Cross-channel linkage: persons with facts from multiple channels
	db.QueryRow(`
		SELECT COUNT(DISTINCT person_id) FROM (
			SELECT person_id, COUNT(DISTINCT source_channel) as channel_count
			FROM person_facts
			WHERE source_channel IS NOT NULL
			GROUP BY person_id
			HAVING channel_count >= 2
		)
	`).Scan(&stats.CrossChannelLinked)

	return stats, nil
}
