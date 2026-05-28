package memory

import (
	"context"
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"fmt"
	"math"
	"strings"
	"time"

	"github.com/Napageneral/cortex/internal/gemini"
	"github.com/google/uuid"
)

const (
	// DefaultEmbeddingModel is the default model used for entity embeddings
	DefaultEmbeddingModel = "gemini-embedding-001"

	// TargetTypeEntity is the target_type value for entity embeddings
	TargetTypeEntity = "entity"
)

// EntityEmbedder generates and stores embeddings for entity canonical names.
// Embeddings enable similarity search for entity resolution.
type EntityEmbedder struct {
	db           *sql.DB
	geminiClient *gemini.Client
	model        string
}

// NewEntityEmbedder creates a new EntityEmbedder.
func NewEntityEmbedder(db *sql.DB, geminiClient *gemini.Client, model string) *EntityEmbedder {
	if model == "" {
		model = DefaultEmbeddingModel
	}
	return &EntityEmbedder{
		db:           db,
		geminiClient: geminiClient,
		model:        model,
	}
}

// EmbedEntity generates and stores an embedding for an entity's canonical name.
// Returns true if an embedding was generated, false if skipped (already exists with same name).
func (e *EntityEmbedder) EmbedEntity(ctx context.Context, entityID string, canonicalName string) (bool, error) {
	if entityID == "" {
		return false, fmt.Errorf("entityID is required")
	}
	if canonicalName == "" {
		return false, fmt.Errorf("canonicalName is required")
	}

	// Normalize the name for embedding
	text := strings.TrimSpace(canonicalName)
	if text == "" {
		return false, nil // Skip empty names
	}

	// Check if embedding already exists with the same source text hash
	sourceHash := hashText(text)
	exists, err := e.embeddingExists(ctx, entityID, sourceHash)
	if err != nil {
		return false, fmt.Errorf("check existing embedding: %w", err)
	}
	if exists {
		return false, nil // Skip - embedding is up to date
	}

	// Generate embedding via Gemini
	embedding, err := e.generateEmbedding(ctx, text)
	if err != nil {
		return false, fmt.Errorf("generate embedding: %w", err)
	}

	if len(embedding) == 0 {
		return false, fmt.Errorf("empty embedding response")
	}

	// Store the embedding
	if err := e.storeEmbedding(ctx, entityID, embedding, sourceHash); err != nil {
		return false, fmt.Errorf("store embedding: %w", err)
	}

	return true, nil
}

// EmbedEntities generates embeddings for multiple entities.
// Returns the number of embeddings generated (skips existing up-to-date embeddings).
func (e *EntityEmbedder) EmbedEntities(ctx context.Context, entities []Entity) (int, error) {
	count := 0
	for _, entity := range entities {
		generated, err := e.EmbedEntity(ctx, entity.ID, entity.CanonicalName)
		if err != nil {
			return count, fmt.Errorf("embed entity %s: %w", entity.ID, err)
		}
		if generated {
			count++
		}
	}
	return count, nil
}

// Entity represents an entity in the graph.
type Entity struct {
	ID            string  `json:"id"`
	CanonicalName string  `json:"canonical_name"`
	EntityTypeID  int     `json:"entity_type_id"`
	Summary       *string `json:"summary,omitempty"`
	Origin        string  `json:"origin"`
	Confidence    float64 `json:"confidence"`
	MergedInto    *string `json:"merged_into,omitempty"`
	CreatedAt     string  `json:"created_at"`
	UpdatedAt     string  `json:"updated_at"`
}

// embeddingExists checks if an up-to-date embedding exists for the entity.
func (e *EntityEmbedder) embeddingExists(ctx context.Context, entityID, sourceHash string) (bool, error) {
	var count int
	err := e.db.QueryRowContext(ctx, `
		SELECT COUNT(*)
		FROM embeddings
		WHERE target_type = ?
		  AND target_id = ?
		  AND model = ?
		  AND source_text_hash = ?
	`, TargetTypeEntity, entityID, e.model, sourceHash).Scan(&count)
	if err != nil {
		return false, err
	}
	return count > 0, nil
}

// generateEmbedding generates an embedding for the given text.
func (e *EntityEmbedder) generateEmbedding(ctx context.Context, text string) ([]float64, error) {
	resp, err := e.geminiClient.EmbedContent(ctx, &gemini.EmbedContentRequest{
		Model: e.model,
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

// storeEmbedding stores an embedding in the database.
func (e *EntityEmbedder) storeEmbedding(ctx context.Context, entityID string, embedding []float64, sourceHash string) error {
	blob := float64SliceToBlob(embedding)
	embID := uuid.New().String()
	now := time.Now().Unix()
	dimension := len(embedding)

	_, err := e.db.ExecContext(ctx, `
		INSERT INTO embeddings (
			id, target_type, target_id, model,
			embedding_blob, dimension, source_text_hash, created_at
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
		ON CONFLICT(target_type, target_id, model) DO UPDATE SET
			embedding_blob = excluded.embedding_blob,
			dimension = excluded.dimension,
			source_text_hash = excluded.source_text_hash
	`, embID, TargetTypeEntity, entityID, e.model, blob, dimension, sourceHash, now)

	return err
}

// GetEntitiesNeedingEmbeddings returns entities that need embeddings generated.
// This includes entities without embeddings or with outdated embeddings (name changed).
func (e *EntityEmbedder) GetEntitiesNeedingEmbeddings(ctx context.Context) ([]Entity, error) {
	// Query entities that either:
	// 1. Have no embedding for this model
	// 2. Have an embedding but the source_text_hash doesn't match current canonical_name
	rows, err := e.db.QueryContext(ctx, `
		SELECT ent.id, ent.canonical_name
		FROM entities ent
		LEFT JOIN embeddings emb
		  ON emb.target_type = ?
		 AND emb.target_id = ent.id
		 AND emb.model = ?
		WHERE ent.merged_into IS NULL
		  AND (
		    emb.id IS NULL
		    OR emb.source_text_hash IS NULL
		    OR emb.source_text_hash != ?
		  )
	`, TargetTypeEntity, e.model, "PLACEHOLDER")
	if err != nil {
		return nil, fmt.Errorf("query entities: %w", err)
	}
	defer rows.Close()

	// Since we can't compute hash in SQL easily, we'll filter in Go
	var candidates []Entity
	for rows.Next() {
		var e Entity
		if err := rows.Scan(&e.ID, &e.CanonicalName); err != nil {
			return nil, fmt.Errorf("scan entity: %w", err)
		}
		candidates = append(candidates, e)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("iterate entities: %w", err)
	}

	// Filter to only those needing updates
	var needsEmbedding []Entity
	for _, ent := range candidates {
		sourceHash := hashText(strings.TrimSpace(ent.CanonicalName))
		exists, err := e.embeddingExists(ctx, ent.ID, sourceHash)
		if err != nil {
			return nil, fmt.Errorf("check embedding for %s: %w", ent.ID, err)
		}
		if !exists {
			needsEmbedding = append(needsEmbedding, ent)
		}
	}

	return needsEmbedding, nil
}

// hashText computes a SHA-256 hash of the text for change detection.
func hashText(text string) string {
	sum := sha256.Sum256([]byte(text))
	return hex.EncodeToString(sum[:])
}

// float64SliceToBlob converts a slice of float64 to a binary blob (little-endian).
func float64SliceToBlob(values []float64) []byte {
	blob := make([]byte, len(values)*8)
	for i, v := range values {
		bits := math.Float64bits(v)
		for j := 0; j < 8; j++ {
			blob[i*8+j] = byte(bits >> (j * 8))
		}
	}
	return blob
}
