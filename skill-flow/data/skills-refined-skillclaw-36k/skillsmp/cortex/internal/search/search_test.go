package search

import (
	"context"
	"database/sql"
	"math"
	"testing"
	"time"

	"github.com/Napageneral/cortex/internal/documents"
	"github.com/Napageneral/cortex/internal/testutil"
	"github.com/google/uuid"
)

func TestSearchDocumentsLexical(t *testing.T) {
	db := testutil.OpenTestDB(t)
	defer db.Close()

	ctx := context.Background()
	_, err := documents.UpsertDocument(ctx, db, documents.DocumentInput{
		DocKey:      "skill:gog",
		Channel:     "skill",
		Title:       "gog",
		Description: "Send email via Gmail",
		Content:     "Use this skill to send email and manage calendar.",
		Timestamp:   1000,
	})
	if err != nil {
		t.Fatalf("upsert gog: %v", err)
	}
	_, err = documents.UpsertDocument(ctx, db, documents.DocumentInput{
		DocKey:      "doc:routing",
		Channel:     "doc",
		Title:       "Semantic Routing Spec",
		Description: "Routing checkpoints",
		Content:     "Spec for semantic agent routing.",
		Timestamp:   1100,
	})
	if err != nil {
		t.Fatalf("upsert routing: %v", err)
	}

	searcher := NewSearcher(db, nil)
	resp, err := searcher.SearchDocuments(ctx, DocumentSearchRequest{
		Query:          "send email",
		UseEmbeddings:  false,
		UseLexical:     true,
		TrackRetrieval: true,
	})
	if err != nil {
		t.Fatalf("search: %v", err)
	}
	if len(resp.Results) == 0 {
		t.Fatalf("expected results")
	}
	if resp.Results[0].DocKey != "skill:gog" {
		t.Fatalf("expected skill:gog, got %s", resp.Results[0].DocKey)
	}

	var count int
	if err := db.QueryRow(`SELECT retrieval_count FROM document_heads WHERE doc_key = ?`, "skill:gog").Scan(&count); err != nil {
		t.Fatalf("query retrieval_count: %v", err)
	}
	if count == 0 {
		t.Fatalf("expected retrieval_count increment")
	}
}

func TestSearchDocumentsVector(t *testing.T) {
	db := testutil.OpenTestDB(t)
	defer db.Close()

	ctx := context.Background()
	_, err := documents.UpsertDocument(ctx, db, documents.DocumentInput{
		DocKey:    "skill:gog",
		Channel:   "skill",
		Content:   "Email and calendar",
		Timestamp: 1000,
	})
	if err != nil {
		t.Fatalf("upsert gog: %v", err)
	}
	_, err = documents.UpsertDocument(ctx, db, documents.DocumentInput{
		DocKey:    "doc:router",
		Channel:   "doc",
		Content:   "Routing spec",
		Timestamp: 1100,
	})
	if err != nil {
		t.Fatalf("upsert router: %v", err)
	}

	model := "test-model"
	err = insertEmbedding(db, "skill:gog", model, []float64{1, 0}, "hash-gog")
	if err != nil {
		t.Fatalf("insert embedding gog: %v", err)
	}
	err = insertEmbedding(db, "doc:router", model, []float64{0, 1}, "hash-router")
	if err != nil {
		t.Fatalf("insert embedding router: %v", err)
	}

	searcher := NewSearcher(db, nil)
	resp, err := searcher.SearchDocuments(ctx, DocumentSearchRequest{
		Query:          "email",
		QueryEmbedding: []float64{1, 0},
		Model:          model,
		UseEmbeddings:  true,
		UseLexical:     false,
	})
	if err != nil {
		t.Fatalf("search: %v", err)
	}
	if len(resp.Results) == 0 {
		t.Fatalf("expected results")
	}
	if resp.Results[0].DocKey != "skill:gog" {
		t.Fatalf("expected skill:gog, got %s", resp.Results[0].DocKey)
	}
}

func insertEmbedding(db *sql.DB, docKey, model string, embedding []float64, sourceHash string) error {
	blob := float64SliceToBlob(embedding)
	embID := uuid.New().String()
	now := time.Now().Unix()
	_, err := db.Exec(`
		INSERT INTO embeddings (id, target_type, target_id, model, embedding_blob, dimension, source_text_hash, created_at)
		VALUES (?, 'document', ?, ?, ?, ?, ?, ?)
	`, embID, docKey, model, blob, len(embedding), sourceHash, now)
	return err
}

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
