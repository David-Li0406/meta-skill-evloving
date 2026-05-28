package documents

import (
	"context"
	"testing"

	"github.com/Napageneral/cortex/internal/testutil"
)

func TestUpsertDocument(t *testing.T) {
	db := testutil.OpenTestDB(t)
	defer db.Close()

	ctx := context.Background()
	input := DocumentInput{
		DocKey:      "skill:gog",
		Channel:     "skill",
		Title:       "gog",
		Description: "Google Workspace CLI",
		Content:     "First version",
		Metadata: map[string]any{
			"provides": []string{"email-send", "calendar"},
		},
		Timestamp: 1000,
	}

	res, err := UpsertDocument(ctx, db, input)
	if err != nil {
		t.Fatalf("upsert create: %v", err)
	}
	if !res.Created || res.EventID == "" {
		t.Fatalf("expected created document, got %+v", res)
	}

	var currentEventID string
	if err := db.QueryRow(`SELECT current_event_id FROM document_heads WHERE doc_key = ?`, input.DocKey).Scan(&currentEventID); err != nil {
		t.Fatalf("query document_heads: %v", err)
	}
	if currentEventID != res.EventID {
		t.Fatalf("expected current_event_id=%s, got %s", res.EventID, currentEventID)
	}

	res2, err := UpsertDocument(ctx, db, input)
	if err != nil {
		t.Fatalf("upsert skip: %v", err)
	}
	if !res2.Skipped {
		t.Fatalf("expected skip on unchanged content, got %+v", res2)
	}

	input.Content = "Second version"
	input.Timestamp = 2000
	res3, err := UpsertDocument(ctx, db, input)
	if err != nil {
		t.Fatalf("upsert update: %v", err)
	}
	if !res3.Updated || res3.EventID == "" {
		t.Fatalf("expected updated document, got %+v", res3)
	}

	var count int
	if err := db.QueryRow(`SELECT COUNT(*) FROM events WHERE channel = 'skill'`).Scan(&count); err != nil {
		t.Fatalf("count events: %v", err)
	}
	if count != 2 {
		t.Fatalf("expected 2 events, got %d", count)
	}
}
