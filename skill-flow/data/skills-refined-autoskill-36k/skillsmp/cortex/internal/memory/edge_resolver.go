package memory

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	"github.com/google/uuid"
)

// EdgeResolverResult contains the output from edge resolution.
type EdgeResolverResult struct {
	NewRelationships     int // Number of new relationships created
	ExistingRelationships int // Number of relationships that already existed
	MentionsCreated      int // Number of episode_relationship_mentions created
}

// ResolvedRelationship represents a relationship with resolved entity UUIDs.
type ResolvedRelationship struct {
	SourceEntityID string  // UUID of source entity
	TargetEntityID *string // UUID of target entity (for entity targets)
	TargetLiteral  *string // Literal value (for identity/temporal targets)
	RelationType   string  // SCREAMING_SNAKE_CASE
	Fact           string  // Natural language description
	SourceType     string  // 'self_disclosed', 'mentioned', 'inferred'
	ValidAt        *string // ISO 8601 date when became true (optional)
	InvalidAt      *string // ISO 8601 date when stopped being true (optional)
	Confidence     float64 // 0.0-1.0
}

// EdgeResolver handles relationship deduplication.
// It checks if a relationship already exists before inserting a new one.
// Same relationship mentioned in multiple episodes creates multiple mentions
// but only one relationship row.
type EdgeResolver struct {
	db *sql.DB
}

// NewEdgeResolver creates a new EdgeResolver.
func NewEdgeResolver(db *sql.DB) *EdgeResolver {
	return &EdgeResolver{db: db}
}

// Resolve processes extracted relationships and deduplicates them against existing edges.
// For each relationship:
// - If exists: create episode_relationship_mentions only
// - If new: create relationship row + episode_relationship_mentions
//
// The relationships should already have resolved entity UUIDs (from entity resolution).
func (r *EdgeResolver) Resolve(ctx context.Context, episodeID string, relationships []ExtractedRelationship, resolvedEntities []ResolvedEntity) (*EdgeResolverResult, error) {
	result := &EdgeResolverResult{}

	for _, rel := range relationships {
		// Skip identity relationships - those are handled by IdentityPromoter
		if IsIdentityRelationType(rel.RelationType) {
			continue
		}

		// Convert to resolved relationship with UUIDs
		resolved, err := r.toResolvedRelationship(rel, resolvedEntities)
		if err != nil {
			// Skip invalid relationships
			continue
		}

		// Check if relationship already exists
		existingID, err := r.findExisting(ctx, resolved)
		if err != nil {
			return nil, fmt.Errorf("find existing relationship: %w", err)
		}

		var relationshipID string
		if existingID != "" {
			// Relationship already exists - just create mention
			relationshipID = existingID
			result.ExistingRelationships++
		} else {
			// New relationship - create it
			relationshipID, err = r.createRelationship(ctx, resolved)
			if err != nil {
				return nil, fmt.Errorf("create relationship: %w", err)
			}
			result.NewRelationships++
		}

		// Create episode_relationship_mentions for provenance
		err = r.createMention(ctx, episodeID, relationshipID, rel)
		if err != nil {
			return nil, fmt.Errorf("create mention: %w", err)
		}
		result.MentionsCreated++
	}

	return result, nil
}

// toResolvedRelationship converts an ExtractedRelationship to a ResolvedRelationship with UUIDs.
func (r *EdgeResolver) toResolvedRelationship(rel ExtractedRelationship, entities []ResolvedEntity) (*ResolvedRelationship, error) {
	// Get source entity UUID
	sourceUUID := GetSourceEntityUUID(rel, entities)
	if sourceUUID == "" {
		return nil, fmt.Errorf("invalid source entity ID: %d", rel.SourceEntityID)
	}

	resolved := &ResolvedRelationship{
		SourceEntityID: sourceUUID,
		RelationType:   rel.RelationType,
		Fact:           rel.Fact,
		SourceType:     rel.SourceType,
		ValidAt:        rel.ValidAt,
		InvalidAt:      rel.InvalidAt,
		Confidence:     1.0, // Default confidence
	}

	// Handle target - either entity ID or literal
	if rel.TargetEntityID != nil {
		targetUUID := GetTargetEntityUUID(rel, entities)
		if targetUUID == "" {
			return nil, fmt.Errorf("invalid target entity ID: %d", *rel.TargetEntityID)
		}
		resolved.TargetEntityID = &targetUUID
	} else if rel.TargetLiteral != nil {
		resolved.TargetLiteral = rel.TargetLiteral
	} else {
		return nil, fmt.Errorf("relationship has no target")
	}

	return resolved, nil
}

// findExisting checks if a relationship already exists in the database.
// Matches on: source_entity_id, target (entity_id or literal), relation_type, valid_at.
// Returns the existing relationship ID if found, empty string otherwise.
func (r *EdgeResolver) findExisting(ctx context.Context, rel *ResolvedRelationship) (string, error) {
	var existingID string

	if rel.TargetEntityID != nil {
		// Match against entity target
		err := r.db.QueryRowContext(ctx, `
			SELECT id FROM relationships
			WHERE source_entity_id = ?
			  AND target_entity_id = ?
			  AND relation_type = ?
			  AND (valid_at IS NULL AND ? IS NULL OR valid_at = ?)
		`, rel.SourceEntityID, *rel.TargetEntityID, rel.RelationType, rel.ValidAt, rel.ValidAt).Scan(&existingID)

		if err == sql.ErrNoRows {
			return "", nil
		}
		if err != nil {
			return "", err
		}
	} else if rel.TargetLiteral != nil {
		// Match against literal target
		err := r.db.QueryRowContext(ctx, `
			SELECT id FROM relationships
			WHERE source_entity_id = ?
			  AND target_literal = ?
			  AND relation_type = ?
			  AND (valid_at IS NULL AND ? IS NULL OR valid_at = ?)
		`, rel.SourceEntityID, *rel.TargetLiteral, rel.RelationType, rel.ValidAt, rel.ValidAt).Scan(&existingID)

		if err == sql.ErrNoRows {
			return "", nil
		}
		if err != nil {
			return "", err
		}
	}

	return existingID, nil
}

// createRelationship creates a new relationship row.
func (r *EdgeResolver) createRelationship(ctx context.Context, rel *ResolvedRelationship) (string, error) {
	id := uuid.New().String()
	now := time.Now().Format(time.RFC3339)

	_, err := r.db.ExecContext(ctx, `
		INSERT INTO relationships (
			id, source_entity_id, target_entity_id, target_literal,
			relation_type, fact, valid_at, invalid_at, created_at, confidence
		)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	`, id, rel.SourceEntityID, rel.TargetEntityID, rel.TargetLiteral,
		rel.RelationType, rel.Fact, rel.ValidAt, rel.InvalidAt, now, rel.Confidence)

	if err != nil {
		return "", err
	}
	return id, nil
}

// createMention creates an episode_relationship_mentions record for provenance.
func (r *EdgeResolver) createMention(ctx context.Context, episodeID, relationshipID string, rel ExtractedRelationship) error {
	id := uuid.New().String()
	now := time.Now().Format(time.RFC3339)

	// Get target literal if present (for temporal relationships)
	var targetLiteral *string
	if rel.TargetLiteral != nil {
		targetLiteral = rel.TargetLiteral
	}

	_, err := r.db.ExecContext(ctx, `
		INSERT INTO episode_relationship_mentions (
			id, episode_id, relationship_id, extracted_fact,
			asserted_by_entity_id, source_type, target_literal, alias_id, confidence, created_at
		)
		VALUES (?, ?, ?, ?, NULL, ?, ?, NULL, ?, ?)
	`, id, episodeID, relationshipID, rel.Fact, rel.SourceType, targetLiteral, 1.0, now)

	return err
}

// ResolveWithAssertedBy processes relationships with speaker attribution.
// asserted_by_entity_id tracks who made the statement (for third-party claims).
func (r *EdgeResolver) ResolveWithAssertedBy(ctx context.Context, episodeID string, relationships []ExtractedRelationship, resolvedEntities []ResolvedEntity, assertedByEntityID *string) (*EdgeResolverResult, error) {
	result := &EdgeResolverResult{}

	for _, rel := range relationships {
		// Skip identity relationships - those are handled by IdentityPromoter
		if IsIdentityRelationType(rel.RelationType) {
			continue
		}

		// Convert to resolved relationship with UUIDs
		resolved, err := r.toResolvedRelationship(rel, resolvedEntities)
		if err != nil {
			// Skip invalid relationships
			continue
		}

		// Check if relationship already exists
		existingID, err := r.findExisting(ctx, resolved)
		if err != nil {
			return nil, fmt.Errorf("find existing relationship: %w", err)
		}

		var relationshipID string
		if existingID != "" {
			// Relationship already exists - just create mention
			relationshipID = existingID
			result.ExistingRelationships++
		} else {
			// New relationship - create it
			relationshipID, err = r.createRelationship(ctx, resolved)
			if err != nil {
				return nil, fmt.Errorf("create relationship: %w", err)
			}
			result.NewRelationships++
		}

		// Create episode_relationship_mentions with speaker attribution
		err = r.createMentionWithAssertedBy(ctx, episodeID, relationshipID, rel, assertedByEntityID)
		if err != nil {
			return nil, fmt.Errorf("create mention: %w", err)
		}
		result.MentionsCreated++
	}

	return result, nil
}

// createMentionWithAssertedBy creates a mention with optional speaker attribution.
func (r *EdgeResolver) createMentionWithAssertedBy(ctx context.Context, episodeID, relationshipID string, rel ExtractedRelationship, assertedByEntityID *string) error {
	id := uuid.New().String()
	now := time.Now().Format(time.RFC3339)

	var targetLiteral *string
	if rel.TargetLiteral != nil {
		targetLiteral = rel.TargetLiteral
	}

	_, err := r.db.ExecContext(ctx, `
		INSERT INTO episode_relationship_mentions (
			id, episode_id, relationship_id, extracted_fact,
			asserted_by_entity_id, source_type, target_literal, alias_id, confidence, created_at
		)
		VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?)
	`, id, episodeID, relationshipID, rel.Fact, assertedByEntityID, rel.SourceType, targetLiteral, 1.0, now)

	return err
}
