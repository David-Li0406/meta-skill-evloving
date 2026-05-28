package me

import (
	"database/sql"
	"fmt"
	"time"

	"github.com/google/uuid"
)

// Person represents a person in the database
type Person struct {
	ID             string
	CanonicalName  string
	DisplayName    *string
	IsMe           bool
	RelationType   *string
	CreatedAt      time.Time
	UpdatedAt      time.Time
}

// Identity represents an identity linked to a person
type Identity struct {
	ID         string
	PersonID   string
	Channel    string
	Identifier string
	CreatedAt  time.Time
}

// GetMePerson returns the person marked as "me", or nil if not set
func GetMePerson(db *sql.DB) (*Person, error) {
	row := db.QueryRow(`
		SELECT id, canonical_name, display_name, is_me, relationship_type, created_at, updated_at
		FROM persons
		WHERE is_me = 1
		LIMIT 1
	`)

	var p Person
	var displayName, relationType sql.NullString
	var createdAt, updatedAt int64

	err := row.Scan(&p.ID, &p.CanonicalName, &displayName, &p.IsMe, &relationType, &createdAt, &updatedAt)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get me person: %w", err)
	}

	if displayName.Valid {
		p.DisplayName = &displayName.String
	}
	if relationType.Valid {
		p.RelationType = &relationType.String
	}
	p.CreatedAt = time.Unix(createdAt, 0)
	p.UpdatedAt = time.Unix(updatedAt, 0)

	return &p, nil
}

// GetIdentities returns all identities for a person
func GetIdentities(db *sql.DB, personID string) ([]Identity, error) {
	rows, err := db.Query(`
		SELECT id, person_id, channel, identifier, created_at
		FROM identities
		WHERE person_id = ?
		ORDER BY channel, identifier
	`, personID)
	if err != nil {
		return nil, fmt.Errorf("failed to query identities: %w", err)
	}
	defer rows.Close()

	var identities []Identity
	for rows.Next() {
		var i Identity
		var createdAt int64
		if err := rows.Scan(&i.ID, &i.PersonID, &i.Channel, &i.Identifier, &createdAt); err != nil {
			return nil, fmt.Errorf("failed to scan identity: %w", err)
		}
		i.CreatedAt = time.Unix(createdAt, 0)
		identities = append(identities, i)
	}

	return identities, rows.Err()
}

// SetMeName sets or updates the "me" person's name
func SetMeName(db *sql.DB, name string) error {
	tx, err := db.Begin()
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %w", err)
	}
	defer tx.Rollback()

	now := time.Now().Unix()

	// Check if me person exists
	var existingID string
	err = tx.QueryRow("SELECT id FROM persons WHERE is_me = 1 LIMIT 1").Scan(&existingID)
	if err == sql.ErrNoRows {
		// Create new me person
		newID := uuid.New().String()
		_, err = tx.Exec(`
			INSERT INTO persons (id, canonical_name, is_me, created_at, updated_at)
			VALUES (?, ?, 1, ?, ?)
		`, newID, name, now, now)
		if err != nil {
			return fmt.Errorf("failed to create me person: %w", err)
		}
	} else if err != nil {
		return fmt.Errorf("failed to check existing me person: %w", err)
	} else {
		// Update existing me person
		_, err = tx.Exec(`
			UPDATE persons
			SET canonical_name = ?, updated_at = ?
			WHERE id = ?
		`, name, now, existingID)
		if err != nil {
			return fmt.Errorf("failed to update me person: %w", err)
		}
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("failed to commit transaction: %w", err)
	}

	return nil
}

// AddIdentity adds an identity to the me person
func AddIdentity(db *sql.DB, channel, identifier string) error {
	tx, err := db.Begin()
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %w", err)
	}
	defer tx.Rollback()

	// Get or create me person
	var meID string
	err = tx.QueryRow("SELECT id FROM persons WHERE is_me = 1 LIMIT 1").Scan(&meID)
	if err == sql.ErrNoRows {
		// Create me person with empty name (will be set later)
		meID = uuid.New().String()
		now := time.Now().Unix()
		_, err = tx.Exec(`
			INSERT INTO persons (id, canonical_name, is_me, created_at, updated_at)
			VALUES (?, '', 1, ?, ?)
		`, meID, now, now)
		if err != nil {
			return fmt.Errorf("failed to create me person: %w", err)
		}
	} else if err != nil {
		return fmt.Errorf("failed to get me person: %w", err)
	}

	// Check if identity already exists
	var existingID string
	err = tx.QueryRow(`
		SELECT id FROM identities WHERE channel = ? AND identifier = ?
	`, channel, identifier).Scan(&existingID)

	if err == nil {
		// Identity exists - check if it belongs to me
		var belongsToMe bool
		err = tx.QueryRow(`
			SELECT person_id = ? FROM identities WHERE id = ?
		`, meID, existingID).Scan(&belongsToMe)
		if err != nil {
			return fmt.Errorf("failed to check identity ownership: %w", err)
		}
		if belongsToMe {
			// Already belongs to me, nothing to do
			return tx.Commit()
		}
		return fmt.Errorf("identity %s:%s already belongs to another person", channel, identifier)
	} else if err != sql.ErrNoRows {
		return fmt.Errorf("failed to check existing identity: %w", err)
	}

	// Create new identity
	newID := uuid.New().String()
	now := time.Now().Unix()
	_, err = tx.Exec(`
		INSERT INTO identities (id, person_id, channel, identifier, created_at)
		VALUES (?, ?, ?, ?, ?)
	`, newID, meID, channel, identifier, now)
	if err != nil {
		return fmt.Errorf("failed to create identity: %w", err)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("failed to commit transaction: %w", err)
	}

	return nil
}
