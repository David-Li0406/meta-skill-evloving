package memory

import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	"time"
)

// QueryDirection specifies the direction of relationship traversal.
type QueryDirection string

const (
	DirectionOutgoing QueryDirection = "outgoing" // Entity is the source
	DirectionIncoming QueryDirection = "incoming" // Entity is the target
	DirectionBoth     QueryDirection = "both"     // Either direction
)

// RelatedEntity represents an entity found via relationship traversal.
type RelatedEntity struct {
	ID            string  `json:"id"`
	CanonicalName string  `json:"canonical_name"`
	EntityTypeID  int     `json:"entity_type_id"`
	RelationType  string  `json:"relation_type"`  // The relationship type that connects them
	Direction     string  `json:"direction"`      // "outgoing" or "incoming"
	ValidAt       *string `json:"valid_at,omitempty"`
	InvalidAt     *string `json:"invalid_at,omitempty"`
	Fact          string  `json:"fact,omitempty"` // The natural language fact
}

// EntityRelationship represents a relationship from the graph.
type EntityRelationship struct {
	ID              string  `json:"id"`
	SourceEntityID  string  `json:"source_entity_id"`
	SourceName      string  `json:"source_name"`
	TargetEntityID  *string `json:"target_entity_id,omitempty"` // nil if target_literal
	TargetName      *string `json:"target_name,omitempty"`      // nil if target_literal
	TargetLiteral   *string `json:"target_literal,omitempty"`   // nil if target_entity_id
	RelationType    string  `json:"relation_type"`
	Fact            string  `json:"fact"`
	ValidAt         *string `json:"valid_at,omitempty"`
	InvalidAt       *string `json:"invalid_at,omitempty"`
	CreatedAt       string  `json:"created_at"`
	Confidence      float64 `json:"confidence"`
	Direction       string  `json:"direction"` // "outgoing" or "incoming" relative to queried entity
}

// QueryOptions configures graph traversal queries.
type QueryOptions struct {
	// Direction specifies which relationships to traverse
	Direction QueryDirection `json:"direction,omitempty"`

	// RelationTypes filters to specific relationship types (nil = all)
	RelationTypes []string `json:"relation_types,omitempty"`

	// IncludeInvalidated includes relationships with invalid_at set
	IncludeInvalidated bool `json:"include_invalidated,omitempty"`

	// AsOfTime queries relationships valid at a specific time (nil = now)
	// Format: RFC3339 or ISO8601 date
	AsOfTime *time.Time `json:"as_of_time,omitempty"`

	// Limit caps the number of results (0 = no limit)
	Limit int `json:"limit,omitempty"`
}

// DefaultQueryOptions returns sensible defaults for queries.
func DefaultQueryOptions() QueryOptions {
	return QueryOptions{
		Direction:          DirectionBoth,
		RelationTypes:      nil, // All types
		IncludeInvalidated: false,
		AsOfTime:           nil, // Now
		Limit:              0,   // No limit
	}
}

// QueryEngine provides graph traversal queries for the memory system.
type QueryEngine struct {
	db *sql.DB
}

// NewQueryEngine creates a new QueryEngine.
func NewQueryEngine(db *sql.DB) *QueryEngine {
	return &QueryEngine{db: db}
}

// GetRelatedEntities returns entities related to the given entity via specified relationship types.
// If relationTypes is nil or empty, all relationship types are included.
// Respects temporal bounds: only returns valid relationships (invalid_at IS NULL OR invalid_at > now).
func (q *QueryEngine) GetRelatedEntities(ctx context.Context, entityID string, opts QueryOptions) ([]RelatedEntity, error) {
	if entityID == "" {
		return nil, fmt.Errorf("entityID is required")
	}

	// Determine time for temporal filtering
	asOf := time.Now()
	if opts.AsOfTime != nil {
		asOf = *opts.AsOfTime
	}
	asOfStr := asOf.Format(time.RFC3339)

	var results []RelatedEntity
	var err error

	// Query outgoing relationships (entity is source)
	if opts.Direction == DirectionOutgoing || opts.Direction == DirectionBoth || opts.Direction == "" {
		outgoing, err := q.getOutgoingRelatedEntities(ctx, entityID, opts, asOfStr)
		if err != nil {
			return nil, fmt.Errorf("get outgoing: %w", err)
		}
		results = append(results, outgoing...)
	}

	// Query incoming relationships (entity is target)
	if opts.Direction == DirectionIncoming || opts.Direction == DirectionBoth || opts.Direction == "" {
		incoming, err := q.getIncomingRelatedEntities(ctx, entityID, opts, asOfStr)
		if err != nil {
			return nil, fmt.Errorf("get incoming: %w", err)
		}
		results = append(results, incoming...)
	}

	// Apply limit if specified
	if opts.Limit > 0 && len(results) > opts.Limit {
		results = results[:opts.Limit]
	}

	return results, err
}

// getOutgoingRelatedEntities finds entities where the given entity is the source.
func (q *QueryEngine) getOutgoingRelatedEntities(ctx context.Context, entityID string, opts QueryOptions, asOfStr string) ([]RelatedEntity, error) {
	query := `
		SELECT e.id, e.canonical_name, e.entity_type_id, r.relation_type, r.valid_at, r.invalid_at, r.fact
		FROM relationships r
		JOIN entities e ON r.target_entity_id = e.id
		WHERE r.source_entity_id = ?
		  AND e.merged_into IS NULL
		  AND r.target_entity_id IS NOT NULL
	`
	args := []interface{}{entityID}

	// Add temporal filter
	// When AsOfTime is set, include relationships that were valid at that time:
	// - valid_at <= asOf (or valid_at is NULL - unknown start time)
	// - invalid_at > asOf (or invalid_at is NULL - still valid)
	if !opts.IncludeInvalidated {
		query += " AND (r.invalid_at IS NULL OR r.invalid_at > ?)"
		args = append(args, asOfStr)
	}
	if opts.AsOfTime != nil {
		query += " AND (r.valid_at IS NULL OR r.valid_at <= ?)"
		args = append(args, asOfStr)
	}

	// Add relation type filter
	if len(opts.RelationTypes) > 0 {
		placeholders := make([]string, len(opts.RelationTypes))
		for i, rt := range opts.RelationTypes {
			placeholders[i] = "?"
			args = append(args, rt)
		}
		query += fmt.Sprintf(" AND r.relation_type IN (%s)", strings.Join(placeholders, ","))
	}

	rows, err := q.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []RelatedEntity
	for rows.Next() {
		var (
			id          string
			name        string
			typeID      int
			relType     string
			validAt     sql.NullString
			invalidAt   sql.NullString
			fact        string
		)
		if err := rows.Scan(&id, &name, &typeID, &relType, &validAt, &invalidAt, &fact); err != nil {
			return nil, err
		}

		rel := RelatedEntity{
			ID:            id,
			CanonicalName: name,
			EntityTypeID:  typeID,
			RelationType:  relType,
			Direction:     "outgoing",
			Fact:          fact,
		}
		if validAt.Valid {
			rel.ValidAt = &validAt.String
		}
		if invalidAt.Valid {
			rel.InvalidAt = &invalidAt.String
		}
		results = append(results, rel)
	}

	return results, rows.Err()
}

// getIncomingRelatedEntities finds entities where the given entity is the target.
func (q *QueryEngine) getIncomingRelatedEntities(ctx context.Context, entityID string, opts QueryOptions, asOfStr string) ([]RelatedEntity, error) {
	query := `
		SELECT e.id, e.canonical_name, e.entity_type_id, r.relation_type, r.valid_at, r.invalid_at, r.fact
		FROM relationships r
		JOIN entities e ON r.source_entity_id = e.id
		WHERE r.target_entity_id = ?
		  AND e.merged_into IS NULL
	`
	args := []interface{}{entityID}

	// Add temporal filter
	if !opts.IncludeInvalidated {
		query += " AND (r.invalid_at IS NULL OR r.invalid_at > ?)"
		args = append(args, asOfStr)
	}
	if opts.AsOfTime != nil {
		query += " AND (r.valid_at IS NULL OR r.valid_at <= ?)"
		args = append(args, asOfStr)
	}

	// Add relation type filter
	if len(opts.RelationTypes) > 0 {
		placeholders := make([]string, len(opts.RelationTypes))
		for i, rt := range opts.RelationTypes {
			placeholders[i] = "?"
			args = append(args, rt)
		}
		query += fmt.Sprintf(" AND r.relation_type IN (%s)", strings.Join(placeholders, ","))
	}

	rows, err := q.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []RelatedEntity
	for rows.Next() {
		var (
			id          string
			name        string
			typeID      int
			relType     string
			validAt     sql.NullString
			invalidAt   sql.NullString
			fact        string
		)
		if err := rows.Scan(&id, &name, &typeID, &relType, &validAt, &invalidAt, &fact); err != nil {
			return nil, err
		}

		rel := RelatedEntity{
			ID:            id,
			CanonicalName: name,
			EntityTypeID:  typeID,
			RelationType:  relType,
			Direction:     "incoming",
			Fact:          fact,
		}
		if validAt.Valid {
			rel.ValidAt = &validAt.String
		}
		if invalidAt.Valid {
			rel.InvalidAt = &invalidAt.String
		}
		results = append(results, rel)
	}

	return results, rows.Err()
}

// GetEntityRelationships returns all relationships for a given entity (as source or target).
// Respects temporal bounds by default.
func (q *QueryEngine) GetEntityRelationships(ctx context.Context, entityID string, opts QueryOptions) ([]EntityRelationship, error) {
	if entityID == "" {
		return nil, fmt.Errorf("entityID is required")
	}

	// Determine time for temporal filtering
	asOf := time.Now()
	if opts.AsOfTime != nil {
		asOf = *opts.AsOfTime
	}
	asOfStr := asOf.Format(time.RFC3339)

	var results []EntityRelationship

	// Query outgoing relationships (entity is source)
	if opts.Direction == DirectionOutgoing || opts.Direction == DirectionBoth || opts.Direction == "" {
		outgoing, err := q.getOutgoingRelationships(ctx, entityID, opts, asOfStr)
		if err != nil {
			return nil, fmt.Errorf("get outgoing relationships: %w", err)
		}
		results = append(results, outgoing...)
	}

	// Query incoming relationships (entity is target)
	if opts.Direction == DirectionIncoming || opts.Direction == DirectionBoth || opts.Direction == "" {
		incoming, err := q.getIncomingRelationships(ctx, entityID, opts, asOfStr)
		if err != nil {
			return nil, fmt.Errorf("get incoming relationships: %w", err)
		}
		results = append(results, incoming...)
	}

	// Apply limit if specified
	if opts.Limit > 0 && len(results) > opts.Limit {
		results = results[:opts.Limit]
	}

	return results, nil
}

// getOutgoingRelationships returns relationships where the entity is the source.
func (q *QueryEngine) getOutgoingRelationships(ctx context.Context, entityID string, opts QueryOptions, asOfStr string) ([]EntityRelationship, error) {
	// Query with LEFT JOIN to handle both entity targets and literal targets
	query := `
		SELECT r.id, r.source_entity_id, src.canonical_name as source_name,
		       r.target_entity_id, tgt.canonical_name as target_name, r.target_literal,
		       r.relation_type, r.fact, r.valid_at, r.invalid_at, r.created_at, r.confidence
		FROM relationships r
		JOIN entities src ON r.source_entity_id = src.id
		LEFT JOIN entities tgt ON r.target_entity_id = tgt.id AND tgt.merged_into IS NULL
		WHERE r.source_entity_id = ?
	`
	args := []interface{}{entityID}

	// Add temporal filter
	if !opts.IncludeInvalidated {
		query += " AND (r.invalid_at IS NULL OR r.invalid_at > ?)"
		args = append(args, asOfStr)
	}
	if opts.AsOfTime != nil {
		query += " AND (r.valid_at IS NULL OR r.valid_at <= ?)"
		args = append(args, asOfStr)
	}

	// Add relation type filter
	if len(opts.RelationTypes) > 0 {
		placeholders := make([]string, len(opts.RelationTypes))
		for i, rt := range opts.RelationTypes {
			placeholders[i] = "?"
			args = append(args, rt)
		}
		query += fmt.Sprintf(" AND r.relation_type IN (%s)", strings.Join(placeholders, ","))
	}

	query += " ORDER BY r.created_at DESC"

	rows, err := q.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []EntityRelationship
	for rows.Next() {
		var (
			id             string
			sourceID       string
			sourceName     string
			targetID       sql.NullString
			targetName     sql.NullString
			targetLiteral  sql.NullString
			relType        string
			fact           string
			validAt        sql.NullString
			invalidAt      sql.NullString
			createdAt      string
			confidence     float64
		)
		if err := rows.Scan(&id, &sourceID, &sourceName, &targetID, &targetName, &targetLiteral,
			&relType, &fact, &validAt, &invalidAt, &createdAt, &confidence); err != nil {
			return nil, err
		}

		rel := EntityRelationship{
			ID:             id,
			SourceEntityID: sourceID,
			SourceName:     sourceName,
			RelationType:   relType,
			Fact:           fact,
			CreatedAt:      createdAt,
			Confidence:     confidence,
			Direction:      "outgoing",
		}
		if targetID.Valid {
			rel.TargetEntityID = &targetID.String
		}
		if targetName.Valid {
			rel.TargetName = &targetName.String
		}
		if targetLiteral.Valid {
			rel.TargetLiteral = &targetLiteral.String
		}
		if validAt.Valid {
			rel.ValidAt = &validAt.String
		}
		if invalidAt.Valid {
			rel.InvalidAt = &invalidAt.String
		}
		results = append(results, rel)
	}

	return results, rows.Err()
}

// getIncomingRelationships returns relationships where the entity is the target.
func (q *QueryEngine) getIncomingRelationships(ctx context.Context, entityID string, opts QueryOptions, asOfStr string) ([]EntityRelationship, error) {
	query := `
		SELECT r.id, r.source_entity_id, src.canonical_name as source_name,
		       r.target_entity_id, tgt.canonical_name as target_name, r.target_literal,
		       r.relation_type, r.fact, r.valid_at, r.invalid_at, r.created_at, r.confidence
		FROM relationships r
		JOIN entities src ON r.source_entity_id = src.id AND src.merged_into IS NULL
		JOIN entities tgt ON r.target_entity_id = tgt.id
		WHERE r.target_entity_id = ?
	`
	args := []interface{}{entityID}

	// Add temporal filter
	if !opts.IncludeInvalidated {
		query += " AND (r.invalid_at IS NULL OR r.invalid_at > ?)"
		args = append(args, asOfStr)
	}
	if opts.AsOfTime != nil {
		query += " AND (r.valid_at IS NULL OR r.valid_at <= ?)"
		args = append(args, asOfStr)
	}

	// Add relation type filter
	if len(opts.RelationTypes) > 0 {
		placeholders := make([]string, len(opts.RelationTypes))
		for i, rt := range opts.RelationTypes {
			placeholders[i] = "?"
			args = append(args, rt)
		}
		query += fmt.Sprintf(" AND r.relation_type IN (%s)", strings.Join(placeholders, ","))
	}

	query += " ORDER BY r.created_at DESC"

	rows, err := q.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []EntityRelationship
	for rows.Next() {
		var (
			id             string
			sourceID       string
			sourceName     string
			targetID       sql.NullString
			targetName     sql.NullString
			targetLiteral  sql.NullString
			relType        string
			fact           string
			validAt        sql.NullString
			invalidAt      sql.NullString
			createdAt      string
			confidence     float64
		)
		if err := rows.Scan(&id, &sourceID, &sourceName, &targetID, &targetName, &targetLiteral,
			&relType, &fact, &validAt, &invalidAt, &createdAt, &confidence); err != nil {
			return nil, err
		}

		rel := EntityRelationship{
			ID:             id,
			SourceEntityID: sourceID,
			SourceName:     sourceName,
			RelationType:   relType,
			Fact:           fact,
			CreatedAt:      createdAt,
			Confidence:     confidence,
			Direction:      "incoming",
		}
		if targetID.Valid {
			rel.TargetEntityID = &targetID.String
		}
		if targetName.Valid {
			rel.TargetName = &targetName.String
		}
		if targetLiteral.Valid {
			rel.TargetLiteral = &targetLiteral.String
		}
		if validAt.Valid {
			rel.ValidAt = &validAt.String
		}
		if invalidAt.Valid {
			rel.InvalidAt = &invalidAt.String
		}
		results = append(results, rel)
	}

	return results, rows.Err()
}

// GetEntity retrieves a single entity by ID.
func (q *QueryEngine) GetEntity(ctx context.Context, entityID string) (*Entity, error) {
	if entityID == "" {
		return nil, fmt.Errorf("entityID is required")
	}

	var entity Entity
	var mergedInto sql.NullString
	err := q.db.QueryRowContext(ctx, `
		SELECT id, canonical_name, entity_type_id, summary, origin, confidence, merged_into, created_at, updated_at
		FROM entities
		WHERE id = ?
	`, entityID).Scan(
		&entity.ID, &entity.CanonicalName, &entity.EntityTypeID,
		&entity.Summary, &entity.Origin, &entity.Confidence,
		&mergedInto, &entity.CreatedAt, &entity.UpdatedAt,
	)
	if err == sql.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	if mergedInto.Valid {
		entity.MergedInto = &mergedInto.String
	}

	return &entity, nil
}

// FindEntitiesByName searches for entities by canonical name (case-insensitive partial match).
func (q *QueryEngine) FindEntitiesByName(ctx context.Context, name string, entityTypeID *int) ([]Entity, error) {
	query := `
		SELECT id, canonical_name, entity_type_id, summary, origin, confidence, merged_into, created_at, updated_at
		FROM entities
		WHERE merged_into IS NULL
		  AND LOWER(canonical_name) LIKE LOWER(?)
	`
	args := []interface{}{"%" + name + "%"}

	if entityTypeID != nil {
		query += " AND entity_type_id = ?"
		args = append(args, *entityTypeID)
	}

	query += " ORDER BY canonical_name"

	rows, err := q.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var entities []Entity
	for rows.Next() {
		var entity Entity
		var mergedInto sql.NullString
		if err := rows.Scan(
			&entity.ID, &entity.CanonicalName, &entity.EntityTypeID,
			&entity.Summary, &entity.Origin, &entity.Confidence,
			&mergedInto, &entity.CreatedAt, &entity.UpdatedAt,
		); err != nil {
			return nil, err
		}
		if mergedInto.Valid {
			entity.MergedInto = &mergedInto.String
		}
		entities = append(entities, entity)
	}

	return entities, rows.Err()
}

// FindEntitiesByRelationType finds all entities that have a specific relationship type (as source or target).
// For example: "Who works at Anthropic?" - find people with WORKS_AT relationship to Anthropic.
func (q *QueryEngine) FindEntitiesByRelationType(ctx context.Context, relationType string, targetEntityID string, opts QueryOptions) ([]RelatedEntity, error) {
	// Determine time for temporal filtering
	asOf := time.Now()
	if opts.AsOfTime != nil {
		asOf = *opts.AsOfTime
	}
	asOfStr := asOf.Format(time.RFC3339)

	query := `
		SELECT e.id, e.canonical_name, e.entity_type_id, r.relation_type, r.valid_at, r.invalid_at, r.fact
		FROM relationships r
		JOIN entities e ON r.source_entity_id = e.id
		WHERE r.target_entity_id = ?
		  AND r.relation_type = ?
		  AND e.merged_into IS NULL
	`
	args := []interface{}{targetEntityID, relationType}

	// Add temporal filter
	if !opts.IncludeInvalidated {
		query += " AND (r.invalid_at IS NULL OR r.invalid_at > ?)"
		args = append(args, asOfStr)
	}

	query += " ORDER BY e.canonical_name"

	rows, err := q.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []RelatedEntity
	for rows.Next() {
		var (
			id          string
			name        string
			typeID      int
			relType     string
			validAt     sql.NullString
			invalidAt   sql.NullString
			fact        string
		)
		if err := rows.Scan(&id, &name, &typeID, &relType, &validAt, &invalidAt, &fact); err != nil {
			return nil, err
		}

		rel := RelatedEntity{
			ID:            id,
			CanonicalName: name,
			EntityTypeID:  typeID,
			RelationType:  relType,
			Direction:     "incoming", // They point TO the target
			Fact:          fact,
		}
		if validAt.Valid {
			rel.ValidAt = &validAt.String
		}
		if invalidAt.Valid {
			rel.InvalidAt = &invalidAt.String
		}
		results = append(results, rel)
	}

	return results, rows.Err()
}

// GetEntityAliases retrieves all aliases for an entity.
func (q *QueryEngine) GetEntityAliases(ctx context.Context, entityID string) ([]EntityAlias, error) {
	rows, err := q.db.QueryContext(ctx, `
		SELECT id, entity_id, alias, alias_type, normalized, is_shared, created_at
		FROM entity_aliases
		WHERE entity_id = ?
		ORDER BY alias_type, alias
	`, entityID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var aliases []EntityAlias
	for rows.Next() {
		var alias EntityAlias
		var normalized sql.NullString
		if err := rows.Scan(&alias.ID, &alias.EntityID, &alias.Alias, &alias.AliasType,
			&normalized, &alias.IsShared, &alias.CreatedAt); err != nil {
			return nil, err
		}
		if normalized.Valid {
			alias.Normalized = normalized.String
		}
		aliases = append(aliases, alias)
	}

	return aliases, rows.Err()
}

// EntityAlias represents an alias for an entity.
type EntityAlias struct {
	ID         string `json:"id"`
	EntityID   string `json:"entity_id"`
	Alias      string `json:"alias"`
	AliasType  string `json:"alias_type"`
	Normalized string `json:"normalized,omitempty"`
	IsShared   bool   `json:"is_shared"`
	CreatedAt  string `json:"created_at"`
}
