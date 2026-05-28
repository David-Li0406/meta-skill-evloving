package cass

import (
	"encoding/json"
	"testing"
)

func TestStatusResponseRobustness(t *testing.T) {
	// Scenario: cass returns Unix timestamp (int) instead of RFC3339 string
	jsonData := `{
		"healthy": true,
		"index": {
			"doc_count": 1000,
			"size_bytes": 10485760,
			"last_updated": 1702200000,
			"healthy": true
		},
		"database": {
			"path": "/db",
			"size_bytes": 0,
			"healthy": true,
			"session_count": 0
		},
		"pending": {"sessions": 0, "files": 0}
	}`

	var resp StatusResponse
	err := json.Unmarshal([]byte(jsonData), &resp)
	if err == nil {
		t.Log("StatusResponse successfully handled Unix timestamp (unexpected for standard time.Time)")
	} else {
		t.Logf("StatusResponse failed on Unix timestamp: %v", err)
	}
}

func TestSearchHitRobustness(t *testing.T) {
	// Scenario: cass returns RFC3339 string instead of Unix timestamp (int)
	jsonData := `{
		"source_path": "path",
		"agent": "cc",
		"workspace": "ws",
		"title": "title",
		"score": 1.0,
		"snippet": "snippet",
		"match_type": "kw",
		"created_at": "2023-12-10T09:20:00Z"
	}`

	var hit SearchHit
	err := json.Unmarshal([]byte(jsonData), &hit)
	if err == nil {
		t.Log("SearchHit successfully handled RFC3339 string (unexpected for *int64)")
	} else {
		t.Logf("SearchHit failed on RFC3339 string: %v", err)
	}
}
