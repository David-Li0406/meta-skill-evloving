package cass

import (
	"context"
	"testing"
	"time"
)

type mockExecutor struct {
	output []byte
	err    error
}

func (m *mockExecutor) Run(ctx context.Context, args ...string) ([]byte, error) {
	return m.output, m.err
}

func TestNewClient(t *testing.T) {
	client := NewClient(WithTimeout(5 * time.Second))
	if client.timeout != 5*time.Second {
		t.Errorf("expected timeout 5s, got %v", client.timeout)
	}
}

func TestClient_Search(t *testing.T) {
	mockResp := `{"count": 1, "hits": [{"title": "test session", "score": 1.0}]}`
	client := NewClient(WithExecutor(&mockExecutor{output: []byte(mockResp), err: nil}))

	resp, err := client.Search(context.Background(), SearchOptions{Query: "test"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if resp.Count != 1 {
		t.Errorf("expected count 1, got %d", resp.Count)
	}
	if len(resp.Hits) != 1 || resp.Hits[0].Title != "test session" {
		t.Errorf("unexpected hits: %v", resp.Hits)
	}
}

func TestClient_Status(t *testing.T) {
	mockResp := `{"healthy": true, "conversations": 42}`
	client := NewClient(WithExecutor(&mockExecutor{output: []byte(mockResp), err: nil}))

	status, err := client.Status(context.Background())
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if !status.Healthy {
		t.Error("expected healthy status")
	}
	if status.Conversations != 42 {
		t.Errorf("expected 42 conversations, got %d", status.Conversations)
	}
}
