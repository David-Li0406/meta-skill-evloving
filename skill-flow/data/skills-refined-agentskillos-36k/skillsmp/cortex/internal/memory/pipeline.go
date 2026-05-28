package memory

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	"github.com/Napageneral/cortex/internal/gemini"
)

// PipelineConfig holds configuration for the memory extraction pipeline.
type PipelineConfig struct {
	// LLM model for entity/relationship extraction (default: gemini-2.0-flash)
	ExtractionModel string
	// Embedding model for entity embeddings (default: gemini-embedding-001)
	EmbeddingModel string
	// Whether to skip embedding generation (useful for testing)
	SkipEmbeddings bool
	// Optional custom instructions for extraction
	CustomInstructions string
	// Number of previous episodes to include for context (default: 0)
	LookbackEpisodes int
}

// DefaultPipelineConfig returns a default pipeline configuration.
func DefaultPipelineConfig() *PipelineConfig {
	return &PipelineConfig{
		ExtractionModel:  "gemini-2.0-flash",
		EmbeddingModel:   DefaultEmbeddingModel,
		SkipEmbeddings:   false,
		LookbackEpisodes: 0,
	}
}

// EpisodeInput represents the input episode to process.
type EpisodeInput struct {
	ID            string        // Episode UUID
	Channel       string        // Channel (e.g., "imessage", "gmail", "aix")
	ThreadID      *string       // Thread ID if applicable
	Content       string        // The episode content to process
	StartTime     time.Time     // Episode start time (used for contradiction detection)
	ReferenceTime string        // ISO 8601 timestamp for temporal reference in extraction
	KnownEntities []KnownEntity // Optional: entities we already know about (e.g., thread participants)
}

// PipelineResult contains the results of pipeline processing.
type PipelineResult struct {
	// Entity extraction
	ExtractedEntities []ExtractedEntity `json:"extracted_entities"`
	ResolvedEntities  []ResolvedEntity  `json:"resolved_entities"`
	NewEntities       int               `json:"new_entities"`
	ExistingEntities  int               `json:"existing_entities"`

	// Relationship extraction
	ExtractedRelationships []ExtractedRelationship `json:"extracted_relationships"`
	NewRelationships       int                     `json:"new_relationships"`
	ExistingRelationships  int                     `json:"existing_relationships"`

	// Identity promotion
	PromotedIdentities int `json:"promoted_identities"`
	AliasesCreated     int `json:"aliases_created"`

	// Contradiction detection
	ContradictionsFound int `json:"contradictions_found"`

	// Embeddings
	EmbeddingsGenerated int `json:"embeddings_generated"`

	// Episode mentions
	EntityMentionsCreated       int `json:"entity_mentions_created"`
	RelationshipMentionsCreated int `json:"relationship_mentions_created"`

	// Processing metadata
	ProcessedAt time.Time     `json:"processed_at"`
	Duration    time.Duration `json:"duration"`
	Skipped     bool          `json:"skipped"` // True if episode was already processed
}

// MemoryPipeline orchestrates the full memory extraction pipeline.
// It follows the flow: extract entities → resolve → extract relationships →
// promote identity → resolve edges → detect contradictions → generate embeddings → save
type MemoryPipeline struct {
	db           *sql.DB
	geminiClient *gemini.Client
	config       *PipelineConfig

	// Pipeline components
	entityExtractor       *EntityExtractor
	entityResolver        *EntityResolver
	relationshipExtractor *RelationshipExtractor
	identityPromoter      *IdentityPromoter
	edgeResolver          *EdgeResolver
	contradictionDetector *ContradictionDetector
	entityEmbedder        *EntityEmbedder
}

// NewMemoryPipeline creates a new MemoryPipeline.
func NewMemoryPipeline(db *sql.DB, geminiClient *gemini.Client, config *PipelineConfig) *MemoryPipeline {
	if config == nil {
		config = DefaultPipelineConfig()
	}

	return &MemoryPipeline{
		db:                    db,
		geminiClient:          geminiClient,
		config:                config,
		entityExtractor:       NewEntityExtractor(geminiClient, config.ExtractionModel),
		entityResolver:        NewEntityResolver(db, geminiClient, config.EmbeddingModel),
		relationshipExtractor: NewRelationshipExtractor(geminiClient, config.ExtractionModel),
		identityPromoter:      NewIdentityPromoter(db),
		edgeResolver:          NewEdgeResolver(db),
		contradictionDetector: NewContradictionDetector(db),
		entityEmbedder:        NewEntityEmbedder(db, geminiClient, config.EmbeddingModel),
	}
}

// Process runs the full memory extraction pipeline for an episode.
// Returns a PipelineResult with counts of entities/relationships created.
//
// The pipeline is idempotent: reprocessing the same episode yields no new
// entities/relationships (existing ones are reused via deduplication).
func (p *MemoryPipeline) Process(ctx context.Context, episode EpisodeInput) (*PipelineResult, error) {
	startTime := time.Now()
	result := &PipelineResult{
		ProcessedAt: startTime,
	}

	// Validate input
	if episode.ID == "" {
		return nil, fmt.Errorf("episode ID is required")
	}
	if episode.Content == "" {
		result.Duration = time.Since(startTime)
		return result, nil // Empty content - nothing to process
	}

	// Check if episode was already processed (idempotency)
	processed, err := p.isEpisodeProcessed(ctx, episode.ID)
	if err != nil {
		return nil, fmt.Errorf("check if episode processed: %w", err)
	}
	if processed {
		result.Skipped = true
		result.Duration = time.Since(startTime)
		return result, nil
	}

	// Get previous episodes for context (if configured)
	var previousEpisodes []string
	if p.config.LookbackEpisodes > 0 {
		previousEpisodes, err = p.getPreviousEpisodes(ctx, episode)
		if err != nil {
			// Non-fatal - continue without context
			previousEpisodes = nil
		}
	}

	// Step 1: Extract entities (graph-independent)
	entityInput := EntityExtractionInput{
		EpisodeContent:     episode.Content,
		ReferenceTime:      episode.ReferenceTime,
		PreviousEpisodes:   previousEpisodes,
		KnownEntities:      episode.KnownEntities,
		CustomInstructions: p.config.CustomInstructions,
	}

	entityResult, err := p.entityExtractor.Extract(ctx, entityInput)
	if err != nil {
		return nil, fmt.Errorf("extract entities: %w", err)
	}
	result.ExtractedEntities = entityResult.ExtractedEntities

	// If no entities extracted, we're done (no relationships possible)
	if len(entityResult.ExtractedEntities) == 0 {
		result.Duration = time.Since(startTime)
		return result, nil
	}

	// Step 2: Resolve entities (with graph context)
	resolutionCtx := ResolutionContext{
		EpisodeID: episode.ID,
		Channel:   episode.Channel,
	}
	if episode.ThreadID != nil {
		resolutionCtx.ThreadID = *episode.ThreadID
	}

	resolutionResult, err := p.entityResolver.Resolve(ctx, entityResult.ExtractedEntities, resolutionCtx)
	if err != nil {
		return nil, fmt.Errorf("resolve entities: %w", err)
	}
	result.ResolvedEntities = resolutionResult.ResolvedEntities

	// Count new vs existing entities
	for _, ent := range resolutionResult.ResolvedEntities {
		if ent.IsNew {
			result.NewEntities++
		} else {
			result.ExistingEntities++
		}
	}

	// Step 3: Extract relationships (graph-independent)
	relInput := RelationshipExtractionInput{
		EpisodeContent:   episode.Content,
		ResolvedEntities: resolutionResult.ResolvedEntities,
		ReferenceTime:    episode.ReferenceTime,
		PreviousEpisodes: previousEpisodes,
		CustomInstructions: p.config.CustomInstructions,
	}

	relResult, err := p.relationshipExtractor.Extract(ctx, relInput)
	if err != nil {
		return nil, fmt.Errorf("extract relationships: %w", err)
	}
	result.ExtractedRelationships = relResult.ExtractedRelationships

	// Step 4: Promote identity relationships (HAS_EMAIL, HAS_PHONE, etc.)
	identityResult, err := p.identityPromoter.Promote(ctx, episode.ID, relResult.ExtractedRelationships, resolutionResult.ResolvedEntities)
	if err != nil {
		return nil, fmt.Errorf("promote identity relationships: %w", err)
	}
	result.PromotedIdentities = len(identityResult.PromotedIdentities)
	result.AliasesCreated = countNewAliases(identityResult.PromotedIdentities)
	result.RelationshipMentionsCreated += identityResult.MentionsCreated

	// Step 5: Resolve edges (deduplicate relationships)
	edgeResult, err := p.edgeResolver.Resolve(ctx, episode.ID, identityResult.NonIdentityRels, resolutionResult.ResolvedEntities)
	if err != nil {
		return nil, fmt.Errorf("resolve edges: %w", err)
	}
	result.NewRelationships = edgeResult.NewRelationships
	result.ExistingRelationships = edgeResult.ExistingRelationships
	result.RelationshipMentionsCreated += edgeResult.MentionsCreated

	// Step 6: Detect contradictions
	if edgeResult.NewRelationships > 0 {
		// Get IDs of newly created relationships for contradiction detection
		newRelIDs, err := p.getRecentlyCreatedRelationshipIDs(ctx, episode.ID)
		if err != nil {
			// Non-fatal - continue without contradiction detection
			_ = err
		} else if len(newRelIDs) > 0 {
			contradictionResult, err := p.contradictionDetector.Detect(ctx, newRelIDs, episode.StartTime)
			if err != nil {
				// Non-fatal - continue
				_ = err
			} else {
				result.ContradictionsFound = contradictionResult.ContradictionsFound
			}
		}
	}

	// Step 7: Generate embeddings for new entities
	if !p.config.SkipEmbeddings && result.NewEntities > 0 {
		newEntities := filterNewEntities(resolutionResult.ResolvedEntities)
		embeddingsGenerated, err := p.entityEmbedder.EmbedEntities(ctx, newEntities)
		if err != nil {
			// Non-fatal - continue without embeddings
			_ = err
		} else {
			result.EmbeddingsGenerated = embeddingsGenerated
		}
	}

	// Step 8: Create episode_entity_mentions
	mentionsCreated, err := p.createEntityMentions(ctx, episode.ID, resolutionResult.ResolvedEntities)
	if err != nil {
		return nil, fmt.Errorf("create entity mentions: %w", err)
	}
	result.EntityMentionsCreated = mentionsCreated

	result.Duration = time.Since(startTime)
	return result, nil
}

// isEpisodeProcessed checks if an episode has already been processed.
// We consider an episode processed if it has any entity mentions.
func (p *MemoryPipeline) isEpisodeProcessed(ctx context.Context, episodeID string) (bool, error) {
	var count int
	err := p.db.QueryRowContext(ctx, `
		SELECT COUNT(*) FROM episode_entity_mentions WHERE episode_id = ?
	`, episodeID).Scan(&count)
	if err != nil {
		return false, err
	}
	return count > 0, nil
}

// getPreviousEpisodes retrieves content from previous episodes for context.
func (p *MemoryPipeline) getPreviousEpisodes(ctx context.Context, episode EpisodeInput) ([]string, error) {
	// Find episodes in the same channel before this one
	rows, err := p.db.QueryContext(ctx, `
		SELECT e.id
		FROM episodes e
		WHERE e.channel = ?
		  AND e.start_time < ?
		ORDER BY e.start_time DESC
		LIMIT ?
	`, episode.Channel, episode.StartTime.Unix(), p.config.LookbackEpisodes)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var episodeIDs []string
	for rows.Next() {
		var id string
		if err := rows.Scan(&id); err != nil {
			continue
		}
		episodeIDs = append(episodeIDs, id)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}

	// For each episode, get its content from events
	var contents []string
	for _, id := range episodeIDs {
		content, err := p.getEpisodeContent(ctx, id)
		if err != nil {
			continue
		}
		if content != "" {
			contents = append(contents, content)
		}
	}

	return contents, nil
}

// getEpisodeContent retrieves the concatenated content of an episode's events.
func (p *MemoryPipeline) getEpisodeContent(ctx context.Context, episodeID string) (string, error) {
	rows, err := p.db.QueryContext(ctx, `
		SELECT ev.content
		FROM episode_events ee
		JOIN events ev ON ee.event_id = ev.id
		WHERE ee.episode_id = ?
		ORDER BY ee.position
	`, episodeID)
	if err != nil {
		return "", err
	}
	defer rows.Close()

	var contents []string
	for rows.Next() {
		var content sql.NullString
		if err := rows.Scan(&content); err != nil {
			continue
		}
		if content.Valid && content.String != "" {
			contents = append(contents, content.String)
		}
	}

	if len(contents) == 0 {
		return "", nil
	}

	// Join with newlines
	result := ""
	for i, c := range contents {
		if i > 0 {
			result += "\n"
		}
		result += c
	}
	return result, nil
}

// getRecentlyCreatedRelationshipIDs returns IDs of relationships created from a specific episode.
func (p *MemoryPipeline) getRecentlyCreatedRelationshipIDs(ctx context.Context, episodeID string) ([]string, error) {
	rows, err := p.db.QueryContext(ctx, `
		SELECT DISTINCT erm.relationship_id
		FROM episode_relationship_mentions erm
		WHERE erm.episode_id = ?
		  AND erm.relationship_id IS NOT NULL
	`, episodeID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var ids []string
	for rows.Next() {
		var id string
		if err := rows.Scan(&id); err != nil {
			continue
		}
		ids = append(ids, id)
	}

	return ids, rows.Err()
}

// createEntityMentions creates episode_entity_mentions records for all resolved entities.
func (p *MemoryPipeline) createEntityMentions(ctx context.Context, episodeID string, entities []ResolvedEntity) (int, error) {
	now := time.Now().Format(time.RFC3339)
	count := 0

	for _, ent := range entities {
		_, err := p.db.ExecContext(ctx, `
			INSERT INTO episode_entity_mentions (episode_id, entity_id, mention_count, created_at)
			VALUES (?, ?, 1, ?)
			ON CONFLICT(episode_id, entity_id) DO UPDATE SET
				mention_count = episode_entity_mentions.mention_count + 1
		`, episodeID, ent.ID, now)
		if err != nil {
			return count, fmt.Errorf("insert entity mention for %s: %w", ent.ID, err)
		}
		count++
	}

	return count, nil
}

// filterNewEntities returns only newly created entities from the resolution result.
func filterNewEntities(entities []ResolvedEntity) []Entity {
	var newEntities []Entity
	for _, e := range entities {
		if e.IsNew {
			newEntities = append(newEntities, Entity{
				ID:            e.ID,
				CanonicalName: e.Name,
			})
		}
	}
	return newEntities
}

// countNewAliases counts how many promoted identities resulted in new aliases.
func countNewAliases(promoted []PromotedIdentity) int {
	count := 0
	for _, p := range promoted {
		if p.AliasID != "" && p.SourceType == "self_disclosed" {
			count++
		}
	}
	return count
}

// ProcessBatch processes multiple episodes in sequence.
// Returns a slice of results, one per episode.
func (p *MemoryPipeline) ProcessBatch(ctx context.Context, episodes []EpisodeInput) ([]*PipelineResult, error) {
	results := make([]*PipelineResult, 0, len(episodes))

	for _, ep := range episodes {
		result, err := p.Process(ctx, ep)
		if err != nil {
			return results, fmt.Errorf("process episode %s: %w", ep.ID, err)
		}
		results = append(results, result)
	}

	return results, nil
}

// GetEpisodeStats returns statistics about processed episodes.
type EpisodeStats struct {
	TotalEntities       int
	TotalRelationships  int
	TotalAliases        int
	TotalMentions       int
	TotalContradictions int
}

// GetStats returns aggregate statistics about the memory graph.
func (p *MemoryPipeline) GetStats(ctx context.Context) (*EpisodeStats, error) {
	stats := &EpisodeStats{}

	// Count entities (excluding merged)
	err := p.db.QueryRowContext(ctx, `
		SELECT COUNT(*) FROM entities WHERE merged_into IS NULL
	`).Scan(&stats.TotalEntities)
	if err != nil {
		return nil, fmt.Errorf("count entities: %w", err)
	}

	// Count relationships (excluding invalidated)
	err = p.db.QueryRowContext(ctx, `
		SELECT COUNT(*) FROM relationships WHERE invalid_at IS NULL
	`).Scan(&stats.TotalRelationships)
	if err != nil {
		return nil, fmt.Errorf("count relationships: %w", err)
	}

	// Count aliases
	err = p.db.QueryRowContext(ctx, `
		SELECT COUNT(*) FROM entity_aliases
	`).Scan(&stats.TotalAliases)
	if err != nil {
		return nil, fmt.Errorf("count aliases: %w", err)
	}

	// Count entity mentions
	err = p.db.QueryRowContext(ctx, `
		SELECT COALESCE(SUM(mention_count), 0) FROM episode_entity_mentions
	`).Scan(&stats.TotalMentions)
	if err != nil {
		return nil, fmt.Errorf("count mentions: %w", err)
	}

	// Count invalidated relationships (contradictions)
	err = p.db.QueryRowContext(ctx, `
		SELECT COUNT(*) FROM relationships WHERE invalid_at IS NOT NULL
	`).Scan(&stats.TotalContradictions)
	if err != nil {
		return nil, fmt.Errorf("count contradictions: %w", err)
	}

	return stats, nil
}
