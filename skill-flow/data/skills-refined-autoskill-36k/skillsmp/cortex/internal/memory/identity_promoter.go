package memory

import (
	"context"
	"database/sql"
	"fmt"
	"regexp"
	"strings"
	"time"

	"github.com/google/uuid"
)

// IdentityRelationTypes are relationship types that use target_literal and get promoted to aliases.
var IdentityRelationTypes = map[string]string{
	"HAS_EMAIL":     "email",
	"HAS_PHONE":     "phone",
	"HAS_HANDLE":    "handle",
	"HAS_USERNAME":  "username",
	"ALSO_KNOWN_AS": "nickname",
}

// PromotedIdentity represents an identity relationship that was promoted to an alias.
type PromotedIdentity struct {
	SourceEntityID string // UUID of the entity
	RelationType   string // HAS_EMAIL, HAS_PHONE, etc.
	TargetLiteral  string // The literal value (email, phone, etc.)
	AliasID        string // UUID of the created alias
	AliasType      string // email, phone, handle, username, nickname
	IsShared       bool   // Whether this alias is shared across entities
	Fact           string // Natural language description
	SourceType     string // self_disclosed, mentioned, inferred
}

// IdentityPromotionResult contains the output of identity promotion.
type IdentityPromotionResult struct {
	PromotedIdentities []PromotedIdentity       // Identities that were promoted to aliases
	NonIdentityRels    []ExtractedRelationship  // Relationships that are NOT identity types
	MentionsCreated    int                      // Number of episode_relationship_mentions created
}

// IdentityPromoter processes identity relationships and promotes them to aliases.
// Identity relationships (HAS_EMAIL, HAS_PHONE, HAS_HANDLE, HAS_USERNAME, ALSO_KNOWN_AS)
// use target_literal and go to entity_aliases, NOT the relationships table.
type IdentityPromoter struct {
	db *sql.DB
}

// NewIdentityPromoter creates a new IdentityPromoter.
func NewIdentityPromoter(db *sql.DB) *IdentityPromoter {
	return &IdentityPromoter{db: db}
}

// Promote processes extracted relationships and promotes identity relationships to aliases.
// It separates identity relationships from non-identity relationships:
// - Identity relationships → entity_aliases + episode_relationship_mentions
// - Non-identity relationships → returned for EdgeResolver to handle
//
// Only promotes when source_type = 'self_disclosed' (high confidence).
// Other source_types still create episode_relationship_mentions for provenance.
func (p *IdentityPromoter) Promote(ctx context.Context, episodeID string, relationships []ExtractedRelationship, resolvedEntities []ResolvedEntity) (*IdentityPromotionResult, error) {
	result := &IdentityPromotionResult{
		PromotedIdentities: make([]PromotedIdentity, 0),
		NonIdentityRels:    make([]ExtractedRelationship, 0, len(relationships)),
	}

	for _, rel := range relationships {
		aliasType, isIdentity := IdentityRelationTypes[rel.RelationType]
		if !isIdentity {
			// Not an identity relationship - pass through for EdgeResolver
			result.NonIdentityRels = append(result.NonIdentityRels, rel)
			continue
		}

		// Identity relationship - needs target_literal
		if rel.TargetLiteral == nil || *rel.TargetLiteral == "" {
			// Invalid identity relationship - skip
			continue
		}

		// Get source entity UUID
		sourceUUID := GetSourceEntityUUID(rel, resolvedEntities)
		if sourceUUID == "" {
			// Invalid source entity - skip
			continue
		}

		promoted, err := p.promoteOne(ctx, episodeID, sourceUUID, rel, aliasType)
		if err != nil {
			return nil, fmt.Errorf("promote identity relationship: %w", err)
		}

		if promoted != nil {
			result.PromotedIdentities = append(result.PromotedIdentities, *promoted)
			result.MentionsCreated++
		}
	}

	return result, nil
}

// promoteOne promotes a single identity relationship to an alias.
func (p *IdentityPromoter) promoteOne(ctx context.Context, episodeID, sourceEntityID string, rel ExtractedRelationship, aliasType string) (*PromotedIdentity, error) {
	targetLiteral := *rel.TargetLiteral

	// Validate phone numbers before promotion
	if aliasType == "phone" && !isValidPhoneNumber(targetLiteral) {
		// Reject invalid phone - skip alias creation and episode_relationship_mention
		return nil, nil
	}

	normalized := normalizeIdentityValue(targetLiteral, aliasType)
	now := time.Now().Format(time.RFC3339)

	var aliasID string
	var isShared bool

	// Only create/update alias when source_type = 'self_disclosed'
	// This is the highest confidence - the entity directly stated this about themselves
	if rel.SourceType == "self_disclosed" {
		// Check if this alias already exists for this entity
		var existingAliasID string
		err := p.db.QueryRowContext(ctx, `
			SELECT id FROM entity_aliases
			WHERE entity_id = ? AND normalized = ? AND alias_type = ?
		`, sourceEntityID, normalized, aliasType).Scan(&existingAliasID)

		if err == sql.ErrNoRows {
			// New alias for this entity - create it
			aliasID = uuid.New().String()
			_, err = p.db.ExecContext(ctx, `
				INSERT INTO entity_aliases (id, entity_id, alias, alias_type, normalized, is_shared, created_at)
				VALUES (?, ?, ?, ?, ?, FALSE, ?)
			`, aliasID, sourceEntityID, targetLiteral, aliasType, normalized, now)
			if err != nil {
				return nil, fmt.Errorf("insert alias: %w", err)
			}
		} else if err != nil {
			return nil, fmt.Errorf("check existing alias: %w", err)
		} else {
			// Alias already exists for this entity
			aliasID = existingAliasID
		}

		// Check for shared aliases (same normalized value, different entities)
		isShared, err = p.detectAndMarkSharedAlias(ctx, aliasID, normalized, aliasType)
		if err != nil {
			// Log but don't fail
			_ = err
		}
	} else {
		// Non-self_disclosed: Find existing alias if any (for provenance link)
		_ = p.db.QueryRowContext(ctx, `
			SELECT id FROM entity_aliases
			WHERE entity_id = ? AND normalized = ? AND alias_type = ?
		`, sourceEntityID, normalized, aliasType).Scan(&aliasID)
		// aliasID may be empty if no existing alias - that's OK for provenance
	}

	// Create episode_relationship_mentions for provenance
	// This records WHERE the identity info came from
	mentionID := uuid.New().String()
	var nullableAliasID *string
	if aliasID != "" {
		nullableAliasID = &aliasID
	}

	_, err := p.db.ExecContext(ctx, `
		INSERT INTO episode_relationship_mentions (
			id, episode_id, relationship_id, extracted_fact,
			asserted_by_entity_id, source_type, target_literal, alias_id, confidence, created_at
		)
		VALUES (?, ?, NULL, ?, NULL, ?, ?, ?, ?, ?)
	`, mentionID, episodeID, rel.Fact, rel.SourceType, targetLiteral, nullableAliasID, 1.0, now)
	if err != nil {
		return nil, fmt.Errorf("insert episode_relationship_mentions: %w", err)
	}

	return &PromotedIdentity{
		SourceEntityID: sourceEntityID,
		RelationType:   rel.RelationType,
		TargetLiteral:  targetLiteral,
		AliasID:        aliasID,
		AliasType:      aliasType,
		IsShared:       isShared,
		Fact:           rel.Fact,
		SourceType:     rel.SourceType,
	}, nil
}

// detectAndMarkSharedAlias checks if the alias is shared and marks all related aliases.
// Returns true if the alias is shared across multiple entities.
func (p *IdentityPromoter) detectAndMarkSharedAlias(ctx context.Context, currentAliasID, normalized, aliasType string) (bool, error) {
	// Find all entities with this normalized alias
	rows, err := p.db.QueryContext(ctx, `
		SELECT id, entity_id FROM entity_aliases
		WHERE normalized = ? AND alias_type = ?
	`, normalized, aliasType)
	if err != nil {
		return false, err
	}
	defer rows.Close()

	type aliasRecord struct {
		id       string
		entityID string
	}
	var aliases []aliasRecord
	entities := make(map[string]bool)

	for rows.Next() {
		var rec aliasRecord
		if err := rows.Scan(&rec.id, &rec.entityID); err != nil {
			continue
		}
		aliases = append(aliases, rec)
		entities[rec.entityID] = true
	}
	if err := rows.Err(); err != nil {
		return false, err
	}

	// If multiple distinct entities have this alias, mark all as shared
	if len(entities) > 1 {
		for _, alias := range aliases {
			_, err := p.db.ExecContext(ctx, `
				UPDATE entity_aliases SET is_shared = TRUE WHERE id = ?
			`, alias.id)
			if err != nil {
				// Log but continue
				_ = err
			}
		}
		return true, nil
	}

	return false, nil
}

// normalizeIdentityValue normalizes an identity value based on its type.
func normalizeIdentityValue(value, aliasType string) string {
	value = strings.TrimSpace(value)

	switch aliasType {
	case "email":
		// Lowercase for email
		return strings.ToLower(value)
	case "phone":
		// Remove spaces and dashes, keep + for international
		normalized := strings.ReplaceAll(value, " ", "")
		normalized = strings.ReplaceAll(normalized, "-", "")
		normalized = strings.ReplaceAll(normalized, "(", "")
		normalized = strings.ReplaceAll(normalized, ")", "")
		return normalized
	case "handle":
		// Lowercase, keep @ prefix if present
		return strings.ToLower(value)
	case "username":
		// Lowercase
		return strings.ToLower(value)
	case "nickname":
		// Lowercase for matching
		return strings.ToLower(value)
	default:
		return strings.ToLower(value)
	}
}

// IsIdentityRelationType returns true if the relation type is an identity relationship.
// Exported for use by other packages.
func IsIdentityRelationType(relType string) bool {
	_, ok := IdentityRelationTypes[relType]
	return ok
}

// GetAliasTypeForRelation returns the alias type for an identity relation type.
// Returns empty string if not an identity relation.
func GetAliasTypeForRelation(relType string) string {
	return IdentityRelationTypes[relType]
}

// isValidPhoneNumber validates that a phone number has 10-15 digits,
// allowing leading + and common formatting characters.
func isValidPhoneNumber(phone string) bool {
	// Remove formatting characters (spaces, dashes, parentheses, dots)
	cleaned := regexp.MustCompile(`[\s\-\(\)\.]`).ReplaceAllString(phone, "")
	
	// Allow leading + for international format
	if strings.HasPrefix(cleaned, "+") {
		cleaned = cleaned[1:]
	}
	
	// Check if remaining string contains only digits
	if !regexp.MustCompile(`^\d+$`).MatchString(cleaned) {
		return false
	}
	
	// Validate length: 10-15 digits
	digitCount := len(cleaned)
	return digitCount >= 10 && digitCount <= 15
}
