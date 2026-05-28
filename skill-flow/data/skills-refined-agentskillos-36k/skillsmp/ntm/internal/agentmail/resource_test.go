package agentmail

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestReadResource(t *testing.T) {
	// Mock JSON-RPC server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			t.Errorf("expected POST, got %s", r.Method)
		}

		var req JSONRPCRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			t.Fatalf("failed to decode request: %v", err)
		}

		if req.JSONRPC != "2.0" {
			t.Errorf("expected jsonrpc 2.0, got %s", req.JSONRPC)
		}
		if req.Method != "resources/read" {
			t.Errorf("expected method resources/read, got %s", req.Method)
		}

		params, ok := req.Params.(map[string]interface{})
		if !ok {
			t.Fatal("expected params to be a map")
		}
		if params["uri"] != "resource://test" {
			t.Errorf("expected uri resource://test, got %v", params["uri"])
		}

		// Return success response
		resp := JSONRPCResponse{
			JSONRPC: "2.0",
			ID:      req.ID,
			Result:  json.RawMessage(`{"contents": [{"uri": "resource://test", "mimeType": "application/json", "text": "{\"key\": \"value\"}"}]}`),
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(resp)
	}))
	defer server.Close()

	c := NewClient(WithBaseURL(server.URL + "/"))
	result, err := c.ReadResource(context.Background(), "resource://test")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	var resourceResp struct {
		Contents []struct {
			Text string `json:"text"`
		} `json:"contents"`
	}
	if err := json.Unmarshal(result, &resourceResp); err != nil {
		t.Fatalf("failed to unmarshal result: %v", err)
	}

	if len(resourceResp.Contents) != 1 {
		t.Errorf("expected 1 content item, got %d", len(resourceResp.Contents))
	}

	if resourceResp.Contents[0].Text != `{"key": "value"}` {
		t.Errorf("unexpected text content: %s", resourceResp.Contents[0].Text)
	}
}

func TestListProjectAgents(t *testing.T) {
	// Mock JSON-RPC server for resources/read
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var req JSONRPCRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			t.Fatalf("failed to decode request: %v", err)
		}

		if req.Method != "resources/read" {
			t.Errorf("expected method resources/read, got %s", req.Method)
		}

		// Return agents list
		agents := []Agent{
			{ID: 1, Name: "Agent1", Program: "prog1"},
			{ID: 2, Name: "Agent2", Program: "prog2"},
		}
		agentsJSON, _ := json.Marshal(agents)

		respContent := map[string]interface{}{
			"contents": []map[string]interface{}{
				{
					"uri":      "resource://agents/test-project",
					"mimeType": "application/json",
					"text":     string(agentsJSON),
				},
			},
		}
		contentJSON, _ := json.Marshal(respContent)

		resp := JSONRPCResponse{
			JSONRPC: "2.0",
			ID:      req.ID,
			Result:  json.RawMessage(contentJSON),
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(resp)
	}))
	defer server.Close()

	c := NewClient(WithBaseURL(server.URL + "/"))
	agents, err := c.ListProjectAgents(context.Background(), "test-project")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	if len(agents) != 2 {
		t.Errorf("expected 2 agents, got %d", len(agents))
	}
	if agents[0].Name != "Agent1" {
		t.Errorf("expected agent 1 name 'Agent1', got %s", agents[0].Name)
	}
}
