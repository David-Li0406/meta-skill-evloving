package identify

import (
	"database/sql"
	"fmt"
	"strings"
	"time"

	"github.com/google/uuid"
)

// PersonWithIdentities represents a person with their identities
type PersonWithIdentities struct {
	ID             string
	CanonicalName  string
	DisplayName    *string
	IsMe           bool
	RelationType   *string
	Identities     []IdentityInfo
	EventCount     int
	LastEventAt    *time.Time
}

// IdentityInfo represents an identity
type IdentityInfo struct {
	ID         string
	Channel    string
	Identifier string
	CreatedAt  time.Time
}

// ListAll returns all persons with their identities
func ListAll(db *sql.DB) ([]PersonWithIdentities, error) {
	rows, err := db.Query(`
		SELECT
			p.id, p.canonical_name, p.display_name, p.is_me, p.relationship_type,
			COALESCE(COUNT(DISTINCT ep.event_id), 0) as event_count,
			MAX(e.timestamp) as last_event_at
		FROM persons p
		LEFT JOIN event_participants ep ON p.id = ep.person_id
		LEFT JOIN events e ON ep.event_id = e.id
		GROUP BY p.id
		ORDER BY event_count DESC, p.canonical_name
	`)
	if err != nil {
		return nil, fmt.Errorf("failed to query persons: %w", err)
	}
	defer rows.Close()

	var persons []PersonWithIdentities
	for rows.Next() {
		var p PersonWithIdentities
		var displayName, relationType sql.NullString
		var lastEventAt sql.NullInt64

		if err := rows.Scan(&p.ID, &p.CanonicalName, &displayName, &p.IsMe, &relationType, &p.EventCount, &lastEventAt); err != nil {
			return nil, fmt.Errorf("failed to scan person: %w", err)
		}

		if displayName.Valid {
			p.DisplayName = &displayName.String
		}
		if relationType.Valid {
			p.RelationType = &relationType.String
		}
		if lastEventAt.Valid {
			t := time.Unix(lastEventAt.Int64, 0)
			p.LastEventAt = &t
		}

		// Get identities for this person
		identities, err := getIdentitiesForPerson(db, p.ID)
		if err != nil {
			return nil, fmt.Errorf("failed to get identities for person %s: %w", p.ID, err)
		}
		p.Identities = identities

		persons = append(persons, p)
	}

	return persons, rows.Err()
}

// Search finds persons matching a search string
func Search(db *sql.DB, searchTerm string) ([]PersonWithIdentities, error) {
	searchPattern := "%" + strings.ToLower(searchTerm) + "%"

	rows, err := db.Query(`
		SELECT DISTINCT
			p.id, p.canonical_name, p.display_name, p.is_me, p.relationship_type,
			COALESCE(COUNT(DISTINCT ep.event_id), 0) as event_count,
			MAX(e.timestamp) as last_event_at
		FROM persons p
		LEFT JOIN identities i ON p.id = i.person_id
		LEFT JOIN event_participants ep ON p.id = ep.person_id
		LEFT JOIN events e ON ep.event_id = e.id
		WHERE LOWER(p.canonical_name) LIKE ?
		   OR LOWER(p.display_name) LIKE ?
		   OR LOWER(i.identifier) LIKE ?
		GROUP BY p.id
		ORDER BY event_count DESC, p.canonical_name
	`, searchPattern, searchPattern, searchPattern)
	if err != nil {
		return nil, fmt.Errorf("failed to search persons: %w", err)
	}
	defer rows.Close()

	var persons []PersonWithIdentities
	for rows.Next() {
		var p PersonWithIdentities
		var displayName, relationType sql.NullString
		var lastEventAt sql.NullInt64

		if err := rows.Scan(&p.ID, &p.CanonicalName, &displayName, &p.IsMe, &relationType, &p.EventCount, &lastEventAt); err != nil {
			return nil, fmt.Errorf("failed to scan person: %w", err)
		}

		if displayName.Valid {
			p.DisplayName = &displayName.String
		}
		if relationType.Valid {
			p.RelationType = &relationType.String
		}
		if lastEventAt.Valid {
			t := time.Unix(lastEventAt.Int64, 0)
			p.LastEventAt = &t
		}

		// Get identities for this person
		identities, err := getIdentitiesForPerson(db, p.ID)
		if err != nil {
			return nil, fmt.Errorf("failed to get identities for person %s: %w", p.ID, err)
		}
		p.Identities = identities

		persons = append(persons, p)
	}

	return persons, rows.Err()
}

// Merge merges person2 into person1 (union-find operation)
// All identities and event_participants for person2 are transferred to person1
// person2 is then deleted
func Merge(db *sql.DB, person1ID, person2ID string) error {
	tx, err := db.Begin()
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %w", err)
	}
	defer tx.Rollback()

	// Verify both persons exist
	var count int
	err = tx.QueryRow("SELECT COUNT(*) FROM persons WHERE id IN (?, ?)", person1ID, person2ID).Scan(&count)
	if err != nil {
		return fmt.Errorf("failed to verify persons: %w", err)
	}
	if count != 2 {
		return fmt.Errorf("one or both persons not found")
	}

	// Check if trying to merge with "me" person
	var person1IsMe, person2IsMe bool
	err = tx.QueryRow("SELECT is_me FROM persons WHERE id = ?", person1ID).Scan(&person1IsMe)
	if err != nil {
		return fmt.Errorf("failed to check person1: %w", err)
	}
	err = tx.QueryRow("SELECT is_me FROM persons WHERE id = ?", person2ID).Scan(&person2IsMe)
	if err != nil {
		return fmt.Errorf("failed to check person2: %w", err)
	}

	if person2IsMe {
		return fmt.Errorf("cannot merge 'me' person into another person - swap the order")
	}

	// Update all identities from person2 to person1
	_, err = tx.Exec("UPDATE identities SET person_id = ? WHERE person_id = ?", person1ID, person2ID)
	if err != nil {
		return fmt.Errorf("failed to transfer identities: %w", err)
	}

	// Update all event_participants from person2 to person1
	// Handle potential duplicates with ON CONFLICT
	_, err = tx.Exec(`
		INSERT INTO event_participants (event_id, person_id, role)
		SELECT event_id, ?, role FROM event_participants WHERE person_id = ?
		ON CONFLICT(event_id, person_id, role) DO NOTHING
	`, person1ID, person2ID)
	if err != nil {
		return fmt.Errorf("failed to transfer event participants: %w", err)
	}

	// Delete old event_participants for person2
	_, err = tx.Exec("DELETE FROM event_participants WHERE person_id = ?", person2ID)
	if err != nil {
		return fmt.Errorf("failed to delete old event participants: %w", err)
	}

	// Delete person2
	_, err = tx.Exec("DELETE FROM persons WHERE id = ?", person2ID)
	if err != nil {
		return fmt.Errorf("failed to delete person2: %w", err)
	}

	// Update person1's updated_at timestamp
	now := time.Now().Unix()
	_, err = tx.Exec("UPDATE persons SET updated_at = ? WHERE id = ?", now, person1ID)
	if err != nil {
		return fmt.Errorf("failed to update person1 timestamp: %w", err)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("failed to commit transaction: %w", err)
	}

	return nil
}

// AddIdentityToPerson adds a new identity to an existing person
func AddIdentityToPerson(db *sql.DB, personID, channel, identifier string) error {
	tx, err := db.Begin()
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %w", err)
	}
	defer tx.Rollback()

	// Verify person exists
	var exists bool
	err = tx.QueryRow("SELECT EXISTS(SELECT 1 FROM persons WHERE id = ?)", personID).Scan(&exists)
	if err != nil {
		return fmt.Errorf("failed to verify person: %w", err)
	}
	if !exists {
		return fmt.Errorf("person not found")
	}

	// Check if identity already exists
	var existingPersonID string
	err = tx.QueryRow(`
		SELECT person_id FROM identities WHERE channel = ? AND identifier = ?
	`, channel, identifier).Scan(&existingPersonID)

	if err == nil {
		// Identity exists - check if it belongs to this person
		if existingPersonID == personID {
			// Already belongs to this person, nothing to do
			return tx.Commit()
		}
		return fmt.Errorf("identity %s:%s already belongs to another person (ID: %s)", channel, identifier, existingPersonID)
	} else if err != sql.ErrNoRows {
		return fmt.Errorf("failed to check existing identity: %w", err)
	}

	// Create new identity
	newID := uuid.New().String()
	now := time.Now().Unix()
	_, err = tx.Exec(`
		INSERT INTO identities (id, person_id, channel, identifier, created_at)
		VALUES (?, ?, ?, ?, ?)
	`, newID, personID, channel, identifier, now)
	if err != nil {
		return fmt.Errorf("failed to create identity: %w", err)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("failed to commit transaction: %w", err)
	}

	return nil
}

// GetPersonByName finds a person by canonical or display name (exact match)
func GetPersonByName(db *sql.DB, name string) (*PersonWithIdentities, error) {
	var p PersonWithIdentities
	var displayName, relationType sql.NullString
	var lastEventAt sql.NullInt64

	err := db.QueryRow(`
		SELECT
			p.id, p.canonical_name, p.display_name, p.is_me, p.relationship_type,
			COALESCE(COUNT(DISTINCT ep.event_id), 0) as event_count,
			MAX(e.timestamp) as last_event_at
		FROM persons p
		LEFT JOIN event_participants ep ON p.id = ep.person_id
		LEFT JOIN events e ON ep.event_id = e.id
		WHERE p.canonical_name = ? OR p.display_name = ?
		GROUP BY p.id
	`, name, name).Scan(&p.ID, &p.CanonicalName, &displayName, &p.IsMe, &relationType, &p.EventCount, &lastEventAt)

	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("failed to query person: %w", err)
	}

	if displayName.Valid {
		p.DisplayName = &displayName.String
	}
	if relationType.Valid {
		p.RelationType = &relationType.String
	}
	if lastEventAt.Valid {
		t := time.Unix(lastEventAt.Int64, 0)
		p.LastEventAt = &t
	}

	// Get identities for this person
	identities, err := getIdentitiesForPerson(db, p.ID)
	if err != nil {
		return nil, fmt.Errorf("failed to get identities for person %s: %w", p.ID, err)
	}
	p.Identities = identities

	return &p, nil
}

// getIdentitiesForPerson is a helper to fetch identities for a person
func getIdentitiesForPerson(db *sql.DB, personID string) ([]IdentityInfo, error) {
	rows, err := db.Query(`
		SELECT id, channel, identifier, created_at
		FROM identities
		WHERE person_id = ?
		ORDER BY channel, identifier
	`, personID)
	if err != nil {
		return nil, fmt.Errorf("failed to query identities: %w", err)
	}
	defer rows.Close()

	var identities []IdentityInfo
	for rows.Next() {
		var i IdentityInfo
		var createdAt int64
		if err := rows.Scan(&i.ID, &i.Channel, &i.Identifier, &createdAt); err != nil {
			return nil, fmt.Errorf("failed to scan identity: %w", err)
		}
		i.CreatedAt = time.Unix(createdAt, 0)
		identities = append(identities, i)
	}

	return identities, rows.Err()
}
