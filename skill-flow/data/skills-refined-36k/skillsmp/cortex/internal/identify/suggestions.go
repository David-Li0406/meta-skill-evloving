package identify

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/google/uuid"
)

// MergeSuggestion represents a proposed merge for user review
type MergeSuggestion struct {
	ID                string  `json:"id"`
	Person1ID         string  `json:"person1_id"`
	Person2ID         string  `json:"person2_id"`
	Person1Name       string  `json:"person1_name"`
	Person2Name       string  `json:"person2_name"`
	EvidenceType      string  `json:"evidence_type"`
	Evidence          any     `json:"evidence"`
	Confidence        float64 `json:"confidence"`
	Person1EventCount int     `json:"person1_event_count"`
	Person2EventCount int     `json:"person2_event_count"`
	Status            string  `json:"status"`
	CreatedAt         int64   `json:"created_at"`
	ReviewedAt        *int64  `json:"reviewed_at,omitempty"`
}

// SuggestionOptions controls suggestion generation
type SuggestionOptions struct {
	MinEventCount   int     // only suggest for persons with >= this many events (default 5)
	MinConfidence   float64 // minimum confidence to create suggestion (default 0.5)
	MaxSuggestions  int     // limit number of suggestions created per run (default 100)
	NameSimilarity  bool    // check name similarity (default true)
	SharedDomain    bool    // check shared email domains (default true)
	CoOccurrence    bool    // check frequent co-occurrence in threads (default false, expensive)
}

func (o SuggestionOptions) withDefaults() SuggestionOptions {
	if o.MinEventCount <= 0 {
		o.MinEventCount = 5
	}
	if o.MinConfidence <= 0 {
		o.MinConfidence = 0.5
	}
	if o.MaxSuggestions <= 0 {
		o.MaxSuggestions = 100
	}
	// Defaults: name similarity and shared domain on, co-occurrence off
	if !o.NameSimilarity && !o.SharedDomain && !o.CoOccurrence {
		o.NameSimilarity = true
		o.SharedDomain = true
	}
	return o
}

// EnsureSuggestionsTable creates the merge_suggestions table if needed
func EnsureSuggestionsTable(db *sql.DB) error {
	_, err := db.Exec(`
		CREATE TABLE IF NOT EXISTS merge_suggestions (
			id TEXT PRIMARY KEY,
			person1_id TEXT NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
			person2_id TEXT NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
			evidence_type TEXT NOT NULL,
			evidence_json TEXT,
			confidence REAL NOT NULL,
			person1_event_count INTEGER,
			person2_event_count INTEGER,
			status TEXT NOT NULL DEFAULT 'pending',
			created_at INTEGER NOT NULL,
			reviewed_at INTEGER,
			UNIQUE(person1_id, person2_id)
		)
	`)
	return err
}

// GenerateSuggestions analyzes the identity graph and creates merge suggestions
// for persons that might be the same but lack deterministic evidence.
func GenerateSuggestions(db *sql.DB, opts SuggestionOptions) (int, error) {
	opts = opts.withDefaults()
	if err := EnsureSuggestionsTable(db); err != nil {
		return 0, err
	}

	// Get persons with event counts above threshold (these are "important")
	rows, err := db.Query(`
		SELECT p.id, p.canonical_name, p.display_name, COUNT(DISTINCT ep.event_id) as event_count
		FROM persons p
		JOIN event_participants ep ON p.id = ep.person_id
		WHERE p.is_me = 0
		GROUP BY p.id
		HAVING event_count >= ?
		ORDER BY event_count DESC
	`, opts.MinEventCount)
	if err != nil {
		return 0, fmt.Errorf("failed to query persons: %w", err)
	}
	defer rows.Close()

	type personInfo struct {
		id          string
		canonical   string
		display     string
		eventCount  int
		emails      []string
		phones      []string
	}

	var persons []personInfo
	for rows.Next() {
		var p personInfo
		var display sql.NullString
		if err := rows.Scan(&p.id, &p.canonical, &display, &p.eventCount); err != nil {
			return 0, err
		}
		if display.Valid {
			p.display = display.String
		}
		persons = append(persons, p)
	}
	if err := rows.Err(); err != nil {
		return 0, err
	}

	// Load identities for each person
	for i := range persons {
		idRows, err := db.Query(`
			SELECT channel, identifier FROM identities WHERE person_id = ?
		`, persons[i].id)
		if err != nil {
			return 0, err
		}
		for idRows.Next() {
			var ch, ident string
			if err := idRows.Scan(&ch, &ident); err != nil {
				idRows.Close()
				return 0, err
			}
			switch ch {
			case "email":
				persons[i].emails = append(persons[i].emails, strings.ToLower(ident))
			case "phone":
				persons[i].phones = append(persons[i].phones, ident)
			}
		}
		idRows.Close()
	}

	// Get existing pending suggestions to avoid duplicates
	existing := make(map[string]struct{})
	exRows, err := db.Query(`
		SELECT person1_id, person2_id FROM merge_suggestions WHERE status = 'pending'
	`)
	if err != nil {
		return 0, err
	}
	for exRows.Next() {
		var p1, p2 string
		if err := exRows.Scan(&p1, &p2); err != nil {
			exRows.Close()
			return 0, err
		}
		existing[p1+":"+p2] = struct{}{}
		existing[p2+":"+p1] = struct{}{}
	}
	exRows.Close()

	// Generate suggestions
	suggestions := make([]MergeSuggestion, 0)
	now := time.Now().Unix()

	for i := 0; i < len(persons) && len(suggestions) < opts.MaxSuggestions; i++ {
		for j := i + 1; j < len(persons) && len(suggestions) < opts.MaxSuggestions; j++ {
			p1, p2 := persons[i], persons[j]

			// Skip if already suggested
			if _, ok := existing[p1.id+":"+p2.id]; ok {
				continue
			}

			var suggestion *MergeSuggestion

			// Check name similarity
			if opts.NameSimilarity {
				if s := checkNameSimilarity(p1.id, p1.canonical, p1.display, p2.id, p2.canonical, p2.display, p1.eventCount, p2.eventCount); s != nil && s.Confidence >= opts.MinConfidence {
					suggestion = s
				}
			}

			// Check shared domain (work emails)
			if suggestion == nil && opts.SharedDomain {
				if s := checkSharedDomain(p1.id, p1.emails, p2.id, p2.emails, p1.eventCount, p2.eventCount); s != nil && s.Confidence >= opts.MinConfidence {
					suggestion = s
				}
			}

			if suggestion != nil {
				suggestion.ID = uuid.New().String()
				suggestion.CreatedAt = now
				suggestion.Status = "pending"
				suggestions = append(suggestions, *suggestion)
				existing[p1.id+":"+p2.id] = struct{}{}
			}
		}
	}

	// Insert suggestions
	for _, s := range suggestions {
		evidenceJSON, _ := json.Marshal(s.Evidence)
		_, err := db.Exec(`
			INSERT INTO merge_suggestions (id, person1_id, person2_id, evidence_type, evidence_json, confidence, person1_event_count, person2_event_count, status, created_at)
			VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
			ON CONFLICT(person1_id, person2_id) DO NOTHING
		`, s.ID, s.Person1ID, s.Person2ID, s.EvidenceType, string(evidenceJSON), s.Confidence, s.Person1EventCount, s.Person2EventCount, s.Status, s.CreatedAt)
		if err != nil {
			return 0, fmt.Errorf("failed to insert suggestion: %w", err)
		}
	}

	return len(suggestions), nil
}

// checkNameSimilarity checks if two persons have similar names
func checkNameSimilarity(p1ID, p1Canonical, p1Display, p2ID, p2Canonical, p2Display string, p1Events, p2Events int) *MergeSuggestion {
	// Normalize names for comparison
	names1 := []string{normalizeForComparison(p1Canonical)}
	if p1Display != "" {
		names1 = append(names1, normalizeForComparison(p1Display))
	}
	names2 := []string{normalizeForComparison(p2Canonical)}
	if p2Display != "" {
		names2 = append(names2, normalizeForComparison(p2Display))
	}

	// Check for matches
	for _, n1 := range names1 {
		if n1 == "" || len(n1) < 3 {
			continue
		}
		// Skip if looks like email/phone
		if strings.Contains(n1, "@") || strings.HasPrefix(n1, "+") {
			continue
		}
		for _, n2 := range names2 {
			if n2 == "" || len(n2) < 3 {
				continue
			}
			if strings.Contains(n2, "@") || strings.HasPrefix(n2, "+") {
				continue
			}

			// Exact match after normalization
			if n1 == n2 {
				return &MergeSuggestion{
					Person1ID:         p1ID,
					Person2ID:         p2ID,
					EvidenceType:      "name_similarity",
					Evidence:          map[string]string{"name1": n1, "name2": n2, "match": "exact"},
					Confidence:        0.8,
					Person1EventCount: p1Events,
					Person2EventCount: p2Events,
				}
			}

			// One name contains the other (e.g., "John" vs "John Smith")
			if strings.Contains(n1, n2) || strings.Contains(n2, n1) {
				longer, shorter := n1, n2
				if len(n2) > len(n1) {
					longer, shorter = n2, n1
				}
				// Only if shorter is substantial
				if len(shorter) >= 4 && float64(len(shorter))/float64(len(longer)) > 0.5 {
					return &MergeSuggestion{
						Person1ID:         p1ID,
						Person2ID:         p2ID,
						EvidenceType:      "name_similarity",
						Evidence:          map[string]string{"name1": n1, "name2": n2, "match": "substring"},
						Confidence:        0.6,
						Person1EventCount: p1Events,
						Person2EventCount: p2Events,
					}
				}
			}
		}
	}
	return nil
}

// checkSharedDomain checks if two persons share an email domain (suggests same org)
func checkSharedDomain(p1ID string, p1Emails []string, p2ID string, p2Emails []string, p1Events, p2Events int) *MergeSuggestion {
	// Extract domains (skip common public domains)
	publicDomains := map[string]bool{
		"gmail.com": true, "yahoo.com": true, "hotmail.com": true, "outlook.com": true,
		"icloud.com": true, "aol.com": true, "proton.me": true, "protonmail.com": true,
		"live.com": true, "msn.com": true, "me.com": true, "mac.com": true,
	}

	getDomains := func(emails []string) []string {
		seen := make(map[string]bool)
		var out []string
		for _, e := range emails {
			parts := strings.Split(e, "@")
			if len(parts) != 2 {
				continue
			}
			d := strings.ToLower(parts[1])
			if publicDomains[d] || seen[d] {
				continue
			}
			seen[d] = true
			out = append(out, d)
		}
		return out
	}

	d1 := getDomains(p1Emails)
	d2 := getDomains(p2Emails)

	for _, dom1 := range d1 {
		for _, dom2 := range d2 {
			if dom1 == dom2 {
				return &MergeSuggestion{
					Person1ID:         p1ID,
					Person2ID:         p2ID,
					EvidenceType:      "shared_domain",
					Evidence:          map[string]string{"domain": dom1},
					Confidence:        0.5, // weak signal alone
					Person1EventCount: p1Events,
					Person2EventCount: p2Events,
				}
			}
		}
	}
	return nil
}

func normalizeForComparison(s string) string {
	s = strings.ToLower(strings.TrimSpace(s))
	// Remove common suffixes/prefixes
	s = strings.TrimSuffix(s, " jr")
	s = strings.TrimSuffix(s, " sr")
	s = strings.TrimSuffix(s, " ii")
	s = strings.TrimSuffix(s, " iii")
	// Collapse whitespace
	parts := strings.Fields(s)
	return strings.Join(parts, " ")
}

// ListSuggestions returns pending merge suggestions ordered by importance
func ListSuggestions(db *sql.DB, status string, limit int) ([]MergeSuggestion, error) {
	if err := EnsureSuggestionsTable(db); err != nil {
		return nil, err
	}
	if limit <= 0 {
		limit = 50
	}
	if status == "" {
		status = "pending"
	}

	rows, err := db.Query(`
		SELECT s.id, s.person1_id, s.person2_id, s.evidence_type, s.evidence_json,
		       s.confidence, s.person1_event_count, s.person2_event_count, s.status, s.created_at, s.reviewed_at,
		       p1.canonical_name, p2.canonical_name
		FROM merge_suggestions s
		JOIN persons p1 ON s.person1_id = p1.id
		JOIN persons p2 ON s.person2_id = p2.id
		WHERE s.status = ?
		ORDER BY (s.person1_event_count + s.person2_event_count) DESC, s.confidence DESC
		LIMIT ?
	`, status, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var out []MergeSuggestion
	for rows.Next() {
		var s MergeSuggestion
		var evidenceJSON sql.NullString
		var reviewedAt sql.NullInt64
		if err := rows.Scan(&s.ID, &s.Person1ID, &s.Person2ID, &s.EvidenceType, &evidenceJSON,
			&s.Confidence, &s.Person1EventCount, &s.Person2EventCount, &s.Status, &s.CreatedAt, &reviewedAt,
			&s.Person1Name, &s.Person2Name); err != nil {
			return nil, err
		}
		if evidenceJSON.Valid {
			_ = json.Unmarshal([]byte(evidenceJSON.String), &s.Evidence)
		}
		if reviewedAt.Valid {
			s.ReviewedAt = &reviewedAt.Int64
		}
		out = append(out, s)
	}
	return out, rows.Err()
}

// AcceptSuggestion merges the two persons and marks the suggestion accepted
func AcceptSuggestion(db *sql.DB, suggestionID string) error {
	if err := EnsureSuggestionsTable(db); err != nil {
		return err
	}

	var p1, p2 string
	err := db.QueryRow(`SELECT person1_id, person2_id FROM merge_suggestions WHERE id = ? AND status = 'pending'`, suggestionID).Scan(&p1, &p2)
	if err == sql.ErrNoRows {
		return fmt.Errorf("suggestion not found or not pending")
	}
	if err != nil {
		return err
	}

	// Perform the merge (person2 into person1)
	if err := Merge(db, p1, p2); err != nil {
		return fmt.Errorf("merge failed: %w", err)
	}

	// Mark accepted
	now := time.Now().Unix()
	_, err = db.Exec(`UPDATE merge_suggestions SET status = 'accepted', reviewed_at = ? WHERE id = ?`, now, suggestionID)
	return err
}

// RejectSuggestion marks the suggestion as rejected
func RejectSuggestion(db *sql.DB, suggestionID string) error {
	if err := EnsureSuggestionsTable(db); err != nil {
		return err
	}
	now := time.Now().Unix()
	res, err := db.Exec(`UPDATE merge_suggestions SET status = 'rejected', reviewed_at = ? WHERE id = ? AND status = 'pending'`, now, suggestionID)
	if err != nil {
		return err
	}
	if n, _ := res.RowsAffected(); n == 0 {
		return fmt.Errorf("suggestion not found or not pending")
	}
	return nil
}

// CleanupExpiredSuggestions removes suggestions where one or both persons no longer exist
func CleanupExpiredSuggestions(db *sql.DB) (int, error) {
	if err := EnsureSuggestionsTable(db); err != nil {
		return 0, err
	}
	now := time.Now().Unix()
	res, err := db.Exec(`
		UPDATE merge_suggestions SET status = 'expired', reviewed_at = ?
		WHERE status = 'pending' AND (
			person1_id NOT IN (SELECT id FROM persons) OR
			person2_id NOT IN (SELECT id FROM persons)
		)
	`, now)
	if err != nil {
		return 0, err
	}
	n, _ := res.RowsAffected()
	return int(n), nil
}
