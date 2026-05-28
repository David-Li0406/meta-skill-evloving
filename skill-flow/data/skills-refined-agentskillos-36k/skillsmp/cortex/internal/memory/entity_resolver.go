package memory

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"math"
	"strings"
	"time"

	"github.com/Napageneral/cortex/internal/gemini"
	"github.com/google/uuid"
)

// Resolution confidence thresholds
const (
	HighConfidenceThreshold = 0.9   // Single candidate above this = auto-match
	AmbiguousGapThreshold   = 0.15  // Gap between top 2 candidates must exceed this
	EmbeddingMinScore       = 0.85  // Minimum embedding similarity to consider
	AliasExactMatchScore    = 1.0   // Score for exact alias matches (normalized match)
	AliasEmailMatchWeight   = 0.95  // Weight for email/phone alias matches
	AliasNameMatchWeight    = 0.85  // Weight for name-only alias matches
	MinMatchThreshold       = 0.35  // Minimum total score to consider matching (lower = more permissive)
)

// ResolutionDecision describes why a resolution was made
type ResolutionDecision string

const (
	DecisionExactAlias      ResolutionDecision = "exact_alias"       // Matched via alias lookup
	DecisionHighConfidence  ResolutionDecision = "high_confidence"   // Single high-confidence candidate
	DecisionClearWinner     ResolutionDecision = "clear_winner"      // Clear winner among candidates
	DecisionCreatedNew      ResolutionDecision = "created_new"       // No match found, created new
	DecisionAmbiguous       ResolutionDecision = "ambiguous"         // Ambiguous, created new + merge_candidate
)

// ResolvedEntity represents an entity after resolution.
type ResolvedEntity struct {
	ID              string             `json:"id"`               // Resolved UUID (existing or new)
	Name            string             `json:"name"`             // Canonical name
	EntityTypeID    int                `json:"entity_type_id"`   // Entity type
	IsNew           bool               `json:"is_new"`           // True if this is a newly created entity
	Decision        ResolutionDecision `json:"decision"`         // How the resolution was decided
	Confidence      float64            `json:"confidence"`       // Resolution confidence (0-1)
	CandidatesCount int                `json:"candidates_count"` // Number of candidates considered
}

// ResolutionCandidate represents a potential match for an extracted entity.
type ResolutionCandidate struct {
	EntityID       string  `json:"entity_id"`
	CanonicalName  string  `json:"canonical_name"`
	EntityTypeID   int     `json:"entity_type_id"`
	AliasScore     float64 `json:"alias_score"`     // Score from alias matching (0-1)
	EmbeddingScore float64 `json:"embedding_score"` // Score from embedding similarity (0-1)
	ContextScore   float64 `json:"context_score"`   // Score from context signals (0-1)
	TotalScore     float64 `json:"total_score"`     // Combined weighted score
	MatchedAlias   string  `json:"matched_alias,omitempty"`
	MatchReason    string  `json:"match_reason,omitempty"`
}

// ResolutionResult contains the output of entity resolution.
type ResolutionResult struct {
	ResolvedEntities []ResolvedEntity       `json:"resolved_entities"`
	UUIDMap          map[int]string         `json:"uuid_map"`           // Maps temp IDs to resolved UUIDs
	CandidatesMap    map[int][]ResolutionCandidate `json:"candidates_map"`  // Candidates considered per entity
}

// ResolutionContext provides context signals for disambiguation.
type ResolutionContext struct {
	EpisodeID      string   `json:"episode_id,omitempty"`
	Channel        string   `json:"channel,omitempty"`
	ThreadID       string   `json:"thread_id,omitempty"`
	CoMentionedIDs []string `json:"co_mentioned_ids,omitempty"` // Already-resolved entity IDs in this episode
}

// EntityResolver resolves extracted entities against the existing graph.
// It implements a conservative strategy: prefer duplicates over false merges.
type EntityResolver struct {
	db           *sql.DB
	geminiClient *gemini.Client
	model        string
}

// NewEntityResolver creates a new EntityResolver.
func NewEntityResolver(db *sql.DB, geminiClient *gemini.Client, model string) *EntityResolver {
	if model == "" {
		model = DefaultEmbeddingModel
	}
	return &EntityResolver{
		db:           db,
		geminiClient: geminiClient,
		model:        model,
	}
}

// Resolve resolves a list of extracted entities against the existing graph.
// Returns a ResolutionResult with resolved entities and a UUID map.
func (r *EntityResolver) Resolve(ctx context.Context, extracted []ExtractedEntity, resCtx ResolutionContext) (*ResolutionResult, error) {
	result := &ResolutionResult{
		ResolvedEntities: make([]ResolvedEntity, 0, len(extracted)),
		UUIDMap:          make(map[int]string),
		CandidatesMap:    make(map[int][]ResolutionCandidate),
	}

	for _, ext := range extracted {
		resolved, candidates, err := r.resolveOne(ctx, ext, resCtx)
		if err != nil {
			return nil, fmt.Errorf("resolve entity %q (id=%d): %w", ext.Name, ext.ID, err)
		}

		result.ResolvedEntities = append(result.ResolvedEntities, *resolved)
		result.UUIDMap[ext.ID] = resolved.ID
		result.CandidatesMap[ext.ID] = candidates

		// Add to co-mentioned IDs for subsequent resolutions
		if resolved.ID != "" {
			resCtx.CoMentionedIDs = append(resCtx.CoMentionedIDs, resolved.ID)
		}
	}

	return result, nil
}

// resolveOne resolves a single extracted entity.
func (r *EntityResolver) resolveOne(ctx context.Context, ext ExtractedEntity, resCtx ResolutionContext) (*ResolvedEntity, []ResolutionCandidate, error) {
	name := strings.TrimSpace(ext.Name)
	if name == "" {
		return nil, nil, fmt.Errorf("entity name is empty")
	}

	// Step 1: Exact alias match
	aliasCandidates, err := r.findAliasCandidates(ctx, name, ext.EntityTypeID)
	if err != nil {
		return nil, nil, fmt.Errorf("find alias candidates: %w", err)
	}

	// Step 2: Embedding similarity search (if we have candidates from alias or need to find more)
	embeddingCandidates, err := r.findEmbeddingCandidates(ctx, name, ext.EntityTypeID)
	if err != nil {
		return nil, nil, fmt.Errorf("find embedding candidates: %w", err)
	}

	// Merge candidates from both sources
	candidates := r.mergeCandidates(aliasCandidates, embeddingCandidates)

	// Step 3: Context scoring for each candidate
	for i := range candidates {
		candidates[i].ContextScore = r.computeContextScore(ctx, candidates[i], resCtx)
		candidates[i].TotalScore = r.computeTotalScore(candidates[i])
	}

	// Sort by total score descending
	sortCandidatesByScore(candidates)

	// Step 4: Decision logic
	return r.makeDecision(ctx, ext, candidates, resCtx)
}

// findAliasCandidates searches entity_aliases for matching aliases.
func (r *EntityResolver) findAliasCandidates(ctx context.Context, name string, entityTypeID int) ([]ResolutionCandidate, error) {
	normalized := normalizeAlias(name)

	rows, err := r.db.QueryContext(ctx, `
		SELECT ea.entity_id, e.canonical_name, e.entity_type_id,
		       ea.alias, ea.alias_type, ea.normalized, ea.is_shared
		FROM entity_aliases ea
		JOIN entities e ON ea.entity_id = e.id
		WHERE e.merged_into IS NULL
		  AND (ea.normalized = ? OR ea.alias = ?)
	`, normalized, name)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	candidateMap := make(map[string]*ResolutionCandidate)
	for rows.Next() {
		var (
			entityID      string
			canonicalName string
			entTypeID     int
			alias         string
			aliasType     string
			normalizedVal sql.NullString
			isShared      bool
		)
		if err := rows.Scan(&entityID, &canonicalName, &entTypeID, &alias, &aliasType, &normalizedVal, &isShared); err != nil {
			continue
		}

		// Calculate alias match score based on type
		score := AliasNameMatchWeight
		if aliasType == "email" || aliasType == "phone" {
			score = AliasEmailMatchWeight
		}
		if normalizedVal.Valid && normalizedVal.String == normalized {
			score = AliasExactMatchScore
		}

		// If shared alias, reduce confidence
		if isShared {
			score *= 0.7
		}

		// Update or add candidate
		if existing, ok := candidateMap[entityID]; ok {
			if score > existing.AliasScore {
				existing.AliasScore = score
				existing.MatchedAlias = alias
				existing.MatchReason = fmt.Sprintf("alias_match:%s", aliasType)
			}
		} else {
			candidateMap[entityID] = &ResolutionCandidate{
				EntityID:      entityID,
				CanonicalName: canonicalName,
				EntityTypeID:  entTypeID,
				AliasScore:    score,
				MatchedAlias:  alias,
				MatchReason:   fmt.Sprintf("alias_match:%s", aliasType),
			}
		}
	}

	candidates := make([]ResolutionCandidate, 0, len(candidateMap))
	for _, c := range candidateMap {
		candidates = append(candidates, *c)
	}
	return candidates, rows.Err()
}

// findEmbeddingCandidates searches entities by embedding similarity.
func (r *EntityResolver) findEmbeddingCandidates(ctx context.Context, name string, entityTypeID int) ([]ResolutionCandidate, error) {
	// Generate embedding for the query name
	queryEmbedding, err := r.generateEmbedding(ctx, name)
	if err != nil {
		// If embedding fails, return empty (alias matching will be used)
		return nil, nil
	}

	// Search entity embeddings
	rows, err := r.db.QueryContext(ctx, `
		SELECT e.id, e.canonical_name, e.entity_type_id,
		       emb.embedding_blob, emb.dimension
		FROM entities e
		JOIN embeddings emb ON emb.target_id = e.id AND emb.target_type = ?
		WHERE e.merged_into IS NULL
		  AND emb.model = ?
	`, TargetTypeEntity, r.model)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var candidates []ResolutionCandidate
	for rows.Next() {
		var (
			entityID      string
			canonicalName string
			entTypeID     int
			blob          []byte
			dimension     int
		)
		if err := rows.Scan(&entityID, &canonicalName, &entTypeID, &blob, &dimension); err != nil {
			continue
		}

		if dimension != len(queryEmbedding) {
			continue
		}

		entityEmbedding := blobToFloat64Slice(blob)
		if len(entityEmbedding) != len(queryEmbedding) {
			continue
		}

		similarity := normalizeCosine(cosineSimilarity(queryEmbedding, entityEmbedding))
		if similarity < EmbeddingMinScore {
			continue
		}

		candidates = append(candidates, ResolutionCandidate{
			EntityID:       entityID,
			CanonicalName:  canonicalName,
			EntityTypeID:   entTypeID,
			EmbeddingScore: similarity,
			MatchReason:    fmt.Sprintf("embedding:%.3f", similarity),
		})
	}

	return candidates, rows.Err()
}

// mergeCandidates merges candidates from alias and embedding searches.
func (r *EntityResolver) mergeCandidates(alias, embedding []ResolutionCandidate) []ResolutionCandidate {
	merged := make(map[string]*ResolutionCandidate)

	for _, c := range alias {
		merged[c.EntityID] = &ResolutionCandidate{
			EntityID:       c.EntityID,
			CanonicalName:  c.CanonicalName,
			EntityTypeID:   c.EntityTypeID,
			AliasScore:     c.AliasScore,
			EmbeddingScore: 0,
			MatchedAlias:   c.MatchedAlias,
			MatchReason:    c.MatchReason,
		}
	}

	for _, c := range embedding {
		if existing, ok := merged[c.EntityID]; ok {
			existing.EmbeddingScore = c.EmbeddingScore
			if existing.MatchReason != "" && c.MatchReason != "" {
				existing.MatchReason = existing.MatchReason + "+" + c.MatchReason
			}
		} else {
			merged[c.EntityID] = &ResolutionCandidate{
				EntityID:       c.EntityID,
				CanonicalName:  c.CanonicalName,
				EntityTypeID:   c.EntityTypeID,
				AliasScore:     0,
				EmbeddingScore: c.EmbeddingScore,
				MatchReason:    c.MatchReason,
			}
		}
	}

	result := make([]ResolutionCandidate, 0, len(merged))
	for _, c := range merged {
		result = append(result, *c)
	}
	return result
}

// computeContextScore computes a context-based score for a candidate.
func (r *EntityResolver) computeContextScore(ctx context.Context, candidate ResolutionCandidate, resCtx ResolutionContext) float64 {
	score := 0.0

	// Check if candidate has relationships with co-mentioned entities
	if len(resCtx.CoMentionedIDs) > 0 {
		relScore := r.checkRelationshipOverlap(ctx, candidate.EntityID, resCtx.CoMentionedIDs)
		score += relScore * 0.3 // Up to 0.3 for relationship overlap
	}

	// Check if candidate appears in same channel recently
	if resCtx.Channel != "" {
		channelScore := r.checkChannelRecency(ctx, candidate.EntityID, resCtx.Channel)
		score += channelScore * 0.2 // Up to 0.2 for channel recency
	}

	return score
}

// checkRelationshipOverlap checks if the candidate has relationships with co-mentioned entities.
func (r *EntityResolver) checkRelationshipOverlap(ctx context.Context, entityID string, coMentionedIDs []string) float64 {
	if len(coMentionedIDs) == 0 {
		return 0
	}

	// Build placeholder string for IN clause
	placeholders := make([]string, len(coMentionedIDs))
	args := make([]interface{}, len(coMentionedIDs)+1)
	args[0] = entityID
	for i, id := range coMentionedIDs {
		placeholders[i] = "?"
		args[i+1] = id
	}

	var count int
	query := fmt.Sprintf(`
		SELECT COUNT(*)
		FROM relationships
		WHERE (source_entity_id = ? AND target_entity_id IN (%s))
		   OR (target_entity_id = ? AND source_entity_id IN (%s))
	`, strings.Join(placeholders, ","), strings.Join(placeholders, ","))

	// Adjust args for both conditions
	fullArgs := append(args, args...)
	err := r.db.QueryRowContext(ctx, query, fullArgs...).Scan(&count)
	if err != nil {
		return 0
	}

	if count > 0 {
		return 1.0 // Has relationships with co-mentioned entities
	}
	return 0
}

// checkChannelRecency checks if the candidate has recent mentions in the same channel.
func (r *EntityResolver) checkChannelRecency(ctx context.Context, entityID, channel string) float64 {
	// Look for recent episode mentions in the same channel
	var count int
	err := r.db.QueryRowContext(ctx, `
		SELECT COUNT(*)
		FROM episode_entity_mentions eem
		JOIN episodes ep ON eem.episode_id = ep.id
		WHERE eem.entity_id = ?
		  AND ep.channel = ?
		  AND ep.end_time > ?
	`, entityID, channel, time.Now().Add(-7*24*time.Hour).Unix()).Scan(&count)
	if err != nil {
		return 0
	}

	if count > 0 {
		return 1.0 // Has recent mentions in same channel
	}
	return 0
}

// computeTotalScore computes the total weighted score for a candidate.
func (r *EntityResolver) computeTotalScore(c ResolutionCandidate) float64 {
	// Weighted combination:
	// - Alias match is most important (0.5 weight)
	// - Embedding similarity (0.3 weight)
	// - Context signals (0.2 weight)
	return c.AliasScore*0.5 + c.EmbeddingScore*0.3 + c.ContextScore*0.2
}

// makeDecision makes a resolution decision based on candidates.
func (r *EntityResolver) makeDecision(ctx context.Context, ext ExtractedEntity, candidates []ResolutionCandidate, resCtx ResolutionContext) (*ResolvedEntity, []ResolutionCandidate, error) {
	// No candidates - create new entity
	if len(candidates) == 0 {
		entity, err := r.createNewEntity(ctx, ext)
		if err != nil {
			return nil, nil, fmt.Errorf("create new entity: %w", err)
		}
		return &ResolvedEntity{
			ID:              entity.ID,
			Name:            entity.CanonicalName,
			EntityTypeID:    ext.EntityTypeID,
			IsNew:           true,
			Decision:        DecisionCreatedNew,
			Confidence:      1.0,
			CandidatesCount: 0,
		}, candidates, nil
	}

	topCandidate := candidates[0]

	// Single high-confidence candidate (based on raw alias/embedding scores, not weighted)
	if topCandidate.TotalScore >= HighConfidenceThreshold {
		return &ResolvedEntity{
			ID:              topCandidate.EntityID,
			Name:            topCandidate.CanonicalName,
			EntityTypeID:    topCandidate.EntityTypeID,
			IsNew:           false,
			Decision:        DecisionHighConfidence,
			Confidence:      topCandidate.TotalScore,
			CandidatesCount: len(candidates),
		}, candidates, nil
	}

	// Exact alias match (normalized) - high confidence match
	if topCandidate.AliasScore >= AliasExactMatchScore {
		return &ResolvedEntity{
			ID:              topCandidate.EntityID,
			Name:            topCandidate.CanonicalName,
			EntityTypeID:    topCandidate.EntityTypeID,
			IsNew:           false,
			Decision:        DecisionExactAlias,
			Confidence:      topCandidate.TotalScore,
			CandidatesCount: len(candidates),
		}, candidates, nil
	}

	// Check for clear winner (single candidate or gap between top 2)
	if len(candidates) == 1 && topCandidate.TotalScore >= MinMatchThreshold {
		return &ResolvedEntity{
			ID:              topCandidate.EntityID,
			Name:            topCandidate.CanonicalName,
			EntityTypeID:    topCandidate.EntityTypeID,
			IsNew:           false,
			Decision:        DecisionClearWinner,
			Confidence:      topCandidate.TotalScore,
			CandidatesCount: len(candidates),
		}, candidates, nil
	}

	if len(candidates) >= 2 {
		secondCandidate := candidates[1]
		gap := topCandidate.TotalScore - secondCandidate.TotalScore
		if gap >= AmbiguousGapThreshold && topCandidate.TotalScore >= MinMatchThreshold {
			return &ResolvedEntity{
				ID:              topCandidate.EntityID,
				Name:            topCandidate.CanonicalName,
				EntityTypeID:    topCandidate.EntityTypeID,
				IsNew:           false,
				Decision:        DecisionClearWinner,
				Confidence:      topCandidate.TotalScore,
				CandidatesCount: len(candidates),
			}, candidates, nil
		}
	}

	// Ambiguous - create new entity and merge_candidate
	// CRITICAL: When in doubt, create new entity. Duplicates are recoverable; false merges corrupt data.
	entity, err := r.createNewEntity(ctx, ext)
	if err != nil {
		return nil, nil, fmt.Errorf("create new entity for ambiguous case: %w", err)
	}

	// Create merge candidate for human review
	if err := r.createMergeCandidate(ctx, entity.ID, topCandidate, ext.Name, candidates); err != nil {
		// Log but don't fail - the entity was created
		_ = err
	}

	return &ResolvedEntity{
		ID:              entity.ID,
		Name:            entity.CanonicalName,
		EntityTypeID:    ext.EntityTypeID,
		IsNew:           true,
		Decision:        DecisionAmbiguous,
		Confidence:      topCandidate.TotalScore,
		CandidatesCount: len(candidates),
	}, candidates, nil
}

// createNewEntity creates a new entity in the database.
func (r *EntityResolver) createNewEntity(ctx context.Context, ext ExtractedEntity) (*Entity, error) {
	id := uuid.New().String()
	now := time.Now().Format(time.RFC3339)

	_, err := r.db.ExecContext(ctx, `
		INSERT INTO entities (id, canonical_name, entity_type_id, origin, confidence, created_at, updated_at)
		VALUES (?, ?, ?, 'extracted', 1.0, ?, ?)
	`, id, ext.Name, ext.EntityTypeID, now, now)
	if err != nil {
		return nil, err
	}

	// Also create a name alias for the new entity
	aliasID := uuid.New().String()
	_, err = r.db.ExecContext(ctx, `
		INSERT INTO entity_aliases (id, entity_id, alias, alias_type, normalized, is_shared, created_at)
		VALUES (?, ?, ?, 'name', ?, FALSE, ?)
	`, aliasID, id, ext.Name, normalizeAlias(ext.Name), now)
	if err != nil {
		// Log but don't fail - entity was created
		_ = err
	}

	return &Entity{
		ID:            id,
		CanonicalName: ext.Name,
	}, nil
}

// createMergeCandidate creates a merge candidate for human review.
func (r *EntityResolver) createMergeCandidate(ctx context.Context, newEntityID string, candidate ResolutionCandidate, extractedName string, allCandidates []ResolutionCandidate) error {
	id := uuid.New().String()
	now := time.Now().Format(time.RFC3339)

	context := map[string]interface{}{
		"extracted_name":    extractedName,
		"candidate_name":    candidate.CanonicalName,
		"alias_score":       candidate.AliasScore,
		"embedding_score":   candidate.EmbeddingScore,
		"context_score":     candidate.ContextScore,
		"total_score":       candidate.TotalScore,
		"matched_alias":     candidate.MatchedAlias,
		"match_reason":      candidate.MatchReason,
	}
	contextJSON, _ := json.Marshal(context)

	// Track all candidates considered for debugging
	candidatesConsidered := make([]map[string]interface{}, 0, len(allCandidates))
	for _, c := range allCandidates {
		candidatesConsidered = append(candidatesConsidered, map[string]interface{}{
			"entity_id":   c.EntityID,
			"name":        c.CanonicalName,
			"total_score": c.TotalScore,
		})
	}
	candidatesJSON, _ := json.Marshal(candidatesConsidered)

	_, err := r.db.ExecContext(ctx, `
		INSERT INTO merge_candidates (id, entity_a_id, entity_b_id, confidence, auto_eligible, reason, context, candidates_considered, status, created_at)
		VALUES (?, ?, ?, ?, FALSE, 'ambiguous_resolution', ?, ?, 'pending', ?)
		ON CONFLICT(entity_a_id, entity_b_id) DO UPDATE SET
			confidence = excluded.confidence,
			context = excluded.context,
			candidates_considered = excluded.candidates_considered
	`, id, newEntityID, candidate.EntityID, candidate.TotalScore, string(contextJSON), string(candidatesJSON), now)

	return err
}

// generateEmbedding generates an embedding for the given text.
func (r *EntityResolver) generateEmbedding(ctx context.Context, text string) ([]float64, error) {
	if r.geminiClient == nil {
		return nil, fmt.Errorf("gemini client not configured")
	}

	resp, err := r.geminiClient.EmbedContent(ctx, &gemini.EmbedContentRequest{
		Model: r.model,
		Content: gemini.Content{
			Parts: []gemini.Part{{Text: text}},
		},
	})
	if err != nil {
		return nil, err
	}
	if resp.Embedding == nil || len(resp.Embedding.Values) == 0 {
		return nil, fmt.Errorf("empty embedding response")
	}
	return resp.Embedding.Values, nil
}

// normalizeAlias normalizes an alias for matching.
func normalizeAlias(alias string) string {
	return strings.ToLower(strings.TrimSpace(alias))
}

// sortCandidatesByScore sorts candidates by total score descending.
func sortCandidatesByScore(candidates []ResolutionCandidate) {
	for i := 0; i < len(candidates)-1; i++ {
		for j := i + 1; j < len(candidates); j++ {
			if candidates[j].TotalScore > candidates[i].TotalScore {
				candidates[i], candidates[j] = candidates[j], candidates[i]
			}
		}
	}
}

// Utility functions (duplicated from search package to avoid circular imports)

func cosineSimilarity(a, b []float64) float64 {
	if len(a) != len(b) || len(a) == 0 {
		return 0
	}
	var dotProduct, normA, normB float64
	for i := range a {
		dotProduct += a[i] * b[i]
		normA += a[i] * a[i]
		normB += b[i] * b[i]
	}
	if normA == 0 || normB == 0 {
		return 0
	}
	return dotProduct / (math.Sqrt(normA) * math.Sqrt(normB))
}

func normalizeCosine(score float64) float64 {
	if score < -1 {
		score = -1
	} else if score > 1 {
		score = 1
	}
	return (score + 1) / 2
}

func blobToFloat64Slice(blob []byte) []float64 {
	if len(blob)%8 != 0 {
		return nil
	}
	values := make([]float64, len(blob)/8)
	for i := 0; i < len(values); i++ {
		bits := uint64(0)
		for j := 0; j < 8; j++ {
			bits |= uint64(blob[i*8+j]) << (j * 8)
		}
		values[i] = math.Float64frombits(bits)
	}
	return values
}
