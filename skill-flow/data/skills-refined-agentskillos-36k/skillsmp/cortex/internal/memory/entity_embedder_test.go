package memory

import (
	"context"
	"database/sql"
	"testing"

	_ "github.com/mattn/go-sqlite3"
)

func setupTestDB(t *testing.T) *sql.DB {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatalf("open db: %v", err)
	}

	// Create minimal schema for testing
	_, err = db.Exec(`
		CREATE TABLE entities (
			id TEXT PRIMARY KEY,
			canonical_name TEXT NOT NULL,
			entity_type_id INTEGER NOT NULL,
			summary TEXT,
			summary_updated_at TEXT,
			origin TEXT NOT NULL,
			confidence REAL DEFAULT 1.0,
			merged_into TEXT,
			created_at TEXT NOT NULL,
			updated_at TEXT NOT NULL
		);

		CREATE TABLE embeddings (
			id TEXT PRIMARY KEY,
			target_type TEXT NOT NULL,
			target_id TEXT NOT NULL,
			model TEXT NOT NULL,
			embedding_blob BLOB NOT NULL,
			dimension INTEGER NOT NULL,
			source_text_hash TEXT,
			created_at INTEGER NOT NULL,
			UNIQUE(target_type, target_id, model)
		);

		CREATE INDEX idx_embeddings_target ON embeddings(target_type, target_id);
	`)
	if err != nil {
		t.Fatalf("create schema: %v", err)
	}

	return db
}

func TestHashText(t *testing.T) {
	// Test that hashText produces consistent results
	hash1 := hashText("Tyler Brandt")
	hash2 := hashText("Tyler Brandt")
	hash3 := hashText("Tyler")

	if hash1 != hash2 {
		t.Error("same input should produce same hash")
	}
	if hash1 == hash3 {
		t.Error("different input should produce different hash")
	}
	if len(hash1) != 64 {
		t.Errorf("expected 64 char hex hash, got %d", len(hash1))
	}
}

func TestFloat64SliceToBlob(t *testing.T) {
	values := []float64{1.0, 2.5, 3.14159}
	blob := float64SliceToBlob(values)

	if len(blob) != len(values)*8 {
		t.Errorf("expected %d bytes, got %d", len(values)*8, len(blob))
	}
}

func TestEmbeddingExists(t *testing.T) {
	db := setupTestDB(t)
	defer db.Close()

	// Create embedder with nil client (we won't call Gemini in this test)
	embedder := NewEntityEmbedder(db, nil, "test-model")

	ctx := context.Background()

	// Initially no embedding exists
	exists, err := embedder.embeddingExists(ctx, "entity-1", "hash123")
	if err != nil {
		t.Fatalf("check exists: %v", err)
	}
	if exists {
		t.Error("expected no embedding to exist")
	}

	// Insert an embedding manually
	_, err = db.Exec(`
		INSERT INTO embeddings (id, target_type, target_id, model, embedding_blob, dimension, source_text_hash, created_at)
		VALUES ('emb-1', 'entity', 'entity-1', 'test-model', X'00', 1, 'hash123', 1234567890)
	`)
	if err != nil {
		t.Fatalf("insert embedding: %v", err)
	}

	// Now embedding should exist with matching hash
	exists, err = embedder.embeddingExists(ctx, "entity-1", "hash123")
	if err != nil {
		t.Fatalf("check exists: %v", err)
	}
	if !exists {
		t.Error("expected embedding to exist")
	}

	// Different hash should not match
	exists, err = embedder.embeddingExists(ctx, "entity-1", "different-hash")
	if err != nil {
		t.Fatalf("check exists: %v", err)
	}
	if exists {
		t.Error("expected no match with different hash")
	}
}

func TestStoreEmbedding(t *testing.T) {
	db := setupTestDB(t)
	defer db.Close()

	embedder := NewEntityEmbedder(db, nil, "test-model")
	ctx := context.Background()

	embedding := []float64{0.1, 0.2, 0.3}
	err := embedder.storeEmbedding(ctx, "entity-1", embedding, "test-hash")
	if err != nil {
		t.Fatalf("store embedding: %v", err)
	}

	// Verify it was stored
	var targetType, targetID, model, sourceHash string
	var dimension int
	err = db.QueryRow(`
		SELECT target_type, target_id, model, dimension, source_text_hash
		FROM embeddings
		WHERE target_id = 'entity-1'
	`).Scan(&targetType, &targetID, &model, &dimension, &sourceHash)
	if err != nil {
		t.Fatalf("query embedding: %v", err)
	}

	if targetType != "entity" {
		t.Errorf("expected target_type 'entity', got %q", targetType)
	}
	if targetID != "entity-1" {
		t.Errorf("expected target_id 'entity-1', got %q", targetID)
	}
	if model != "test-model" {
		t.Errorf("expected model 'test-model', got %q", model)
	}
	if dimension != 3 {
		t.Errorf("expected dimension 3, got %d", dimension)
	}
	if sourceHash != "test-hash" {
		t.Errorf("expected source_text_hash 'test-hash', got %q", sourceHash)
	}

	// Test update on conflict
	newEmbedding := []float64{0.4, 0.5, 0.6, 0.7}
	err = embedder.storeEmbedding(ctx, "entity-1", newEmbedding, "new-hash")
	if err != nil {
		t.Fatalf("update embedding: %v", err)
	}

	err = db.QueryRow(`
		SELECT dimension, source_text_hash FROM embeddings WHERE target_id = 'entity-1'
	`).Scan(&dimension, &sourceHash)
	if err != nil {
		t.Fatalf("query updated embedding: %v", err)
	}

	if dimension != 4 {
		t.Errorf("expected updated dimension 4, got %d", dimension)
	}
	if sourceHash != "new-hash" {
		t.Errorf("expected updated hash 'new-hash', got %q", sourceHash)
	}
}

func TestGetEntitiesNeedingEmbeddings(t *testing.T) {
	db := setupTestDB(t)
	defer db.Close()

	embedder := NewEntityEmbedder(db, nil, "test-model")
	ctx := context.Background()

	// Insert some entities
	_, err := db.Exec(`
		INSERT INTO entities (id, canonical_name, entity_type_id, origin, created_at, updated_at)
		VALUES
			('ent-1', 'Tyler Brandt', 1, 'extracted', '2024-01-01', '2024-01-01'),
			('ent-2', 'Casey Adams', 1, 'extracted', '2024-01-01', '2024-01-01'),
			('ent-3', 'Merged Entity', 1, 'extracted', '2024-01-01', '2024-01-01')
	`)
	if err != nil {
		t.Fatalf("insert entities: %v", err)
	}

	// Mark ent-3 as merged (should be excluded)
	_, err = db.Exec(`UPDATE entities SET merged_into = 'ent-1' WHERE id = 'ent-3'`)
	if err != nil {
		t.Fatalf("update merged_into: %v", err)
	}

	// Insert an up-to-date embedding for ent-1
	hash := hashText("Tyler Brandt")
	_, err = db.Exec(`
		INSERT INTO embeddings (id, target_type, target_id, model, embedding_blob, dimension, source_text_hash, created_at)
		VALUES ('emb-1', 'entity', 'ent-1', 'test-model', X'00', 1, ?, 1234567890)
	`, hash)
	if err != nil {
		t.Fatalf("insert embedding: %v", err)
	}

	// Get entities needing embeddings
	entities, err := embedder.GetEntitiesNeedingEmbeddings(ctx)
	if err != nil {
		t.Fatalf("get entities: %v", err)
	}

	// Should only return ent-2 (ent-1 has embedding, ent-3 is merged)
	if len(entities) != 1 {
		t.Fatalf("expected 1 entity, got %d", len(entities))
	}
	if entities[0].ID != "ent-2" {
		t.Errorf("expected ent-2, got %s", entities[0].ID)
	}
	if entities[0].CanonicalName != "Casey Adams" {
		t.Errorf("expected 'Casey Adams', got %q", entities[0].CanonicalName)
	}
}

func TestEmbedEntity_Validation(t *testing.T) {
	db := setupTestDB(t)
	defer db.Close()

	embedder := NewEntityEmbedder(db, nil, "test-model")
	ctx := context.Background()

	// Test empty entityID
	_, err := embedder.EmbedEntity(ctx, "", "Name")
	if err == nil {
		t.Error("expected error for empty entityID")
	}

	// Test empty canonicalName
	_, err = embedder.EmbedEntity(ctx, "ent-1", "")
	if err == nil {
		t.Error("expected error for empty canonicalName")
	}

	// Test whitespace-only name (should return false, no error)
	generated, err := embedder.EmbedEntity(ctx, "ent-1", "   ")
	if err != nil {
		t.Errorf("unexpected error for whitespace name: %v", err)
	}
	if generated {
		t.Error("expected no embedding for whitespace-only name")
	}
}

func TestDefaultEmbeddingModel(t *testing.T) {
	db := setupTestDB(t)
	defer db.Close()

	// Empty model should use default
	embedder := NewEntityEmbedder(db, nil, "")
	if embedder.model != DefaultEmbeddingModel {
		t.Errorf("expected default model %q, got %q", DefaultEmbeddingModel, embedder.model)
	}

	// Custom model should be used
	embedder2 := NewEntityEmbedder(db, nil, "custom-model")
	if embedder2.model != "custom-model" {
		t.Errorf("expected 'custom-model', got %q", embedder2.model)
	}
}
