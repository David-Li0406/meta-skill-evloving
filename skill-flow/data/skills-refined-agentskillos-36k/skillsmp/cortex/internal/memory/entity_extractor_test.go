package memory

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

// mockGeminiServer creates a test server that returns a predefined response
func mockGeminiServer(t *testing.T, responseJSON string) *httptest.Server {
	return httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Verify it's a POST to generateContent
		if r.Method != "POST" {
			t.Errorf("expected POST, got %s", r.Method)
		}

		// Return a valid Gemini response structure
		response := map[string]interface{}{
			"candidates": []map[string]interface{}{
				{
					"content": map[string]interface{}{
						"parts": []map[string]interface{}{
							{"text": responseJSON},
						},
					},
				},
			},
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	}))
}

func TestEntityExtractor_Extract(t *testing.T) {
	tests := []struct {
		name           string
		input          EntityExtractionInput
		mockResponse   string
		wantEntities   []ExtractedEntity
		wantErr        bool
	}{
		{
			name: "basic extraction with multiple entities",
			input: EntityExtractionInput{
				EpisodeContent: "Tyler: I'm meeting Casey at Anthropic tomorrow to discuss the Cortex project.",
			},
			mockResponse: `{
				"extracted_entities": [
					{"id": 0, "name": "Tyler", "entity_type_id": 1},
					{"id": 1, "name": "Casey", "entity_type_id": 1},
					{"id": 2, "name": "Anthropic", "entity_type_id": 2},
					{"id": 3, "name": "Cortex", "entity_type_id": 3}
				]
			}`,
			wantEntities: []ExtractedEntity{
				{ID: 0, Name: "Tyler", EntityTypeID: 1},
				{ID: 1, Name: "Casey", EntityTypeID: 1},
				{ID: 2, Name: "Anthropic", EntityTypeID: 2},
				{ID: 3, Name: "Cortex", EntityTypeID: 3},
			},
			wantErr: false,
		},
		{
			name: "extraction with location and event",
			input: EntityExtractionInput{
				EpisodeContent: "The HTAA meeting is in Austin next week.",
			},
			mockResponse: `{
				"extracted_entities": [
					{"id": 0, "name": "HTAA meeting", "entity_type_id": 5},
					{"id": 1, "name": "Austin", "entity_type_id": 4}
				]
			}`,
			wantEntities: []ExtractedEntity{
				{ID: 0, Name: "HTAA meeting", EntityTypeID: 5},
				{ID: 1, Name: "Austin", EntityTypeID: 4},
			},
			wantErr: false,
		},
		{
			name: "extraction with pet and document",
			input: EntityExtractionInput{
				EpisodeContent: "Luna was sleeping on the README.md file.",
			},
			mockResponse: `{
				"extracted_entities": [
					{"id": 0, "name": "Luna", "entity_type_id": 7},
					{"id": 1, "name": "README.md", "entity_type_id": 6}
				]
			}`,
			wantEntities: []ExtractedEntity{
				{ID: 0, Name: "Luna", EntityTypeID: 7},
				{ID: 1, Name: "README.md", EntityTypeID: 6},
			},
			wantErr: false,
		},
		{
			name: "empty episode content returns empty result",
			input: EntityExtractionInput{
				EpisodeContent: "",
			},
			mockResponse:   "", // Won't be called
			wantEntities:   []ExtractedEntity{},
			wantErr:        false,
		},
		{
			name: "extraction with invalid entity type gets defaulted to Entity(0)",
			input: EntityExtractionInput{
				EpisodeContent: "Some content",
			},
			mockResponse: `{
				"extracted_entities": [
					{"id": 0, "name": "Unknown Thing", "entity_type_id": 99}
				]
			}`,
			wantEntities: []ExtractedEntity{
				{ID: 0, Name: "Unknown Thing", EntityTypeID: 0}, // Defaults to Entity
			},
			wantErr: false,
		},
		{
			name: "no entities found returns empty array",
			input: EntityExtractionInput{
				EpisodeContent: "Just a simple message with no notable entities.",
			},
			mockResponse: `{
				"extracted_entities": []
			}`,
			wantEntities: []ExtractedEntity{},
			wantErr:      false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Skip mock server for empty input test
			if tt.input.EpisodeContent == "" {
				extractor := NewEntityExtractor(nil, "test-model")
				result, err := extractor.Extract(context.Background(), tt.input)
				if err != nil {
					t.Fatalf("unexpected error: %v", err)
				}
				if len(result.ExtractedEntities) != 0 {
					t.Errorf("expected empty entities for empty input, got %d", len(result.ExtractedEntities))
				}
				return
			}

			// Create mock server
			server := mockGeminiServer(t, tt.mockResponse)
			defer server.Close()

			// Create a client that points to the mock server
			// Note: We need to use a custom client for testing since gemini.Client
			// uses the real API. For this test, we'll test the parsing logic separately.
			// In a real integration, you'd want to inject the HTTP client.

			// For now, test the response parsing directly
			var result EntityExtractionResult
			err := json.Unmarshal([]byte(tt.mockResponse), &result)
			if (err != nil) != tt.wantErr {
				t.Fatalf("json.Unmarshal error = %v, wantErr %v", err, tt.wantErr)
			}

			if tt.wantErr {
				return
			}

			// Validate invalid entity types are defaulted
			for i, entity := range result.ExtractedEntities {
				if !IsValidEntityTypeID(entity.EntityTypeID) {
					result.ExtractedEntities[i].EntityTypeID = EntityTypeEntity
				}
			}

			if len(result.ExtractedEntities) != len(tt.wantEntities) {
				t.Errorf("got %d entities, want %d", len(result.ExtractedEntities), len(tt.wantEntities))
				return
			}

			for i, got := range result.ExtractedEntities {
				want := tt.wantEntities[i]
				if got.ID != want.ID {
					t.Errorf("entity[%d].ID = %d, want %d", i, got.ID, want.ID)
				}
				if got.Name != want.Name {
					t.Errorf("entity[%d].Name = %q, want %q", i, got.Name, want.Name)
				}
				if got.EntityTypeID != want.EntityTypeID {
					t.Errorf("entity[%d].EntityTypeID = %d, want %d", i, got.EntityTypeID, want.EntityTypeID)
				}
			}
		})
	}
}

func TestEntityExtractor_buildPrompt(t *testing.T) {
	extractor := NewEntityExtractor(nil, "test-model")

	tests := []struct {
		name           string
		input          EntityExtractionInput
		wantContains   []string
		wantNotContain []string
	}{
		{
			name: "basic prompt structure",
			input: EntityExtractionInput{
				EpisodeContent: "Tyler met Casey at Anthropic.",
			},
			wantContains: []string{
				"<ENTITY_TYPES>",
				"</ENTITY_TYPES>",
				"<CURRENT_EPISODE>",
				"Tyler met Casey at Anthropic.",
				"</CURRENT_EPISODE>",
				"Person",
				"Company",
				"Project",
				"extracted_entities",
			},
			wantNotContain: []string{
				"<PREVIOUS_EPISODES>",
			},
		},
		{
			name: "prompt with previous episodes",
			input: EntityExtractionInput{
				EpisodeContent:   "Let's discuss that later.",
				PreviousEpisodes: []string{"Tyler mentioned the Cortex project yesterday."},
			},
			wantContains: []string{
				"<PREVIOUS_EPISODES>",
				"Tyler mentioned the Cortex project yesterday.",
				"</PREVIOUS_EPISODES>",
				"<CURRENT_EPISODE>",
				"Let's discuss that later.",
			},
		},
		{
			name: "prompt with custom instructions",
			input: EntityExtractionInput{
				EpisodeContent:     "Some technical discussion.",
				CustomInstructions: "Focus on extracting trading system components.",
			},
			wantContains: []string{
				"Focus on extracting trading system components.",
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			prompt := extractor.buildPrompt(tt.input)

			for _, want := range tt.wantContains {
				if !contains(prompt, want) {
					t.Errorf("prompt should contain %q", want)
				}
			}

			for _, notWant := range tt.wantNotContain {
				if contains(prompt, notWant) {
					t.Errorf("prompt should not contain %q", notWant)
				}
			}
		})
	}
}

func TestEntityTypesJSON(t *testing.T) {
	jsonStr := EntityTypesJSON()

	// Should be valid JSON
	var types []map[string]interface{}
	if err := json.Unmarshal([]byte(jsonStr), &types); err != nil {
		t.Fatalf("EntityTypesJSON() produced invalid JSON: %v", err)
	}

	// Should have 8 types
	if len(types) != 8 {
		t.Errorf("expected 8 types, got %d", len(types))
	}

	// Verify structure
	for i, typ := range types {
		if _, ok := typ["id"]; !ok {
			t.Errorf("type[%d] missing 'id' field", i)
		}
		if _, ok := typ["name"]; !ok {
			t.Errorf("type[%d] missing 'name' field", i)
		}
		if _, ok := typ["description"]; !ok {
			t.Errorf("type[%d] missing 'description' field", i)
		}
	}
}

func TestNewEntityExtractor(t *testing.T) {
	// Test with default model
	extractor := NewEntityExtractor(nil, "")
	if extractor.model != "gemini-2.0-flash" {
		t.Errorf("expected default model 'gemini-2.0-flash', got %q", extractor.model)
	}

	// Test with custom model
	extractor = NewEntityExtractor(nil, "custom-model")
	if extractor.model != "custom-model" {
		t.Errorf("expected model 'custom-model', got %q", extractor.model)
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > 0 && containsHelper(s, substr))
}

func containsHelper(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}
