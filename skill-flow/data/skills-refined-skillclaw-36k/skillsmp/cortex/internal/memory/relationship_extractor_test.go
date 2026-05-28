package memory

import (
	"encoding/json"
	"testing"
)

func TestRelationshipExtractionResultParsing(t *testing.T) {
	// Test parsing of LLM response JSON
	jsonResponse := `{
		"extracted_relationships": [
			{
				"source_entity_id": 0,
				"relation_type": "HAS_EMAIL",
				"target_literal": "tyler@example.com",
				"fact": "Tyler's email is tyler@example.com",
				"source_type": "self_disclosed"
			},
			{
				"source_entity_id": 0,
				"relation_type": "WORKS_AT",
				"target_entity_id": 1,
				"fact": "Tyler works at Anthropic",
				"source_type": "self_disclosed",
				"valid_at": "2024-01"
			}
		]
	}`

	var result RelationshipExtractionResult
	err := json.Unmarshal([]byte(jsonResponse), &result)
	if err != nil {
		t.Fatalf("Failed to parse JSON: %v", err)
	}

	if len(result.ExtractedRelationships) != 2 {
		t.Fatalf("Expected 2 relationships, got %d", len(result.ExtractedRelationships))
	}

	// Check identity relationship
	rel1 := result.ExtractedRelationships[0]
	if rel1.SourceEntityID != 0 {
		t.Errorf("Expected source_entity_id=0, got %d", rel1.SourceEntityID)
	}
	if rel1.RelationType != "HAS_EMAIL" {
		t.Errorf("Expected relation_type=HAS_EMAIL, got %s", rel1.RelationType)
	}
	if rel1.TargetLiteral == nil || *rel1.TargetLiteral != "tyler@example.com" {
		t.Errorf("Expected target_literal=tyler@example.com")
	}
	if rel1.TargetEntityID != nil {
		t.Errorf("Expected target_entity_id to be nil for literal relationship")
	}
	if rel1.SourceType != "self_disclosed" {
		t.Errorf("Expected source_type=self_disclosed, got %s", rel1.SourceType)
	}

	// Check entity relationship with temporal bounds
	rel2 := result.ExtractedRelationships[1]
	if rel2.SourceEntityID != 0 {
		t.Errorf("Expected source_entity_id=0, got %d", rel2.SourceEntityID)
	}
	if rel2.RelationType != "WORKS_AT" {
		t.Errorf("Expected relation_type=WORKS_AT, got %s", rel2.RelationType)
	}
	if rel2.TargetEntityID == nil || *rel2.TargetEntityID != 1 {
		t.Errorf("Expected target_entity_id=1")
	}
	if rel2.TargetLiteral != nil {
		t.Errorf("Expected target_literal to be nil for entity relationship")
	}
	if rel2.ValidAt == nil || *rel2.ValidAt != "2024-01" {
		t.Errorf("Expected valid_at=2024-01")
	}
}

func TestRelationshipExtractionResultWithInvalidAt(t *testing.T) {
	// Test parsing with invalid_at for job change scenario
	jsonResponse := `{
		"extracted_relationships": [
			{
				"source_entity_id": 0,
				"relation_type": "WORKS_AT",
				"target_entity_id": 1,
				"fact": "Tyler worked at Intent Systems",
				"source_type": "self_disclosed",
				"invalid_at": "2025-12"
			},
			{
				"source_entity_id": 0,
				"relation_type": "WORKS_AT",
				"target_entity_id": 2,
				"fact": "Tyler joined Anthropic",
				"source_type": "self_disclosed",
				"valid_at": "2026-01"
			}
		]
	}`

	var result RelationshipExtractionResult
	err := json.Unmarshal([]byte(jsonResponse), &result)
	if err != nil {
		t.Fatalf("Failed to parse JSON: %v", err)
	}

	if len(result.ExtractedRelationships) != 2 {
		t.Fatalf("Expected 2 relationships, got %d", len(result.ExtractedRelationships))
	}

	// Old job has invalid_at
	rel1 := result.ExtractedRelationships[0]
	if rel1.InvalidAt == nil || *rel1.InvalidAt != "2025-12" {
		t.Errorf("Expected invalid_at=2025-12")
	}
	if rel1.ValidAt != nil {
		t.Errorf("Expected valid_at to be nil for ended job")
	}

	// New job has valid_at
	rel2 := result.ExtractedRelationships[1]
	if rel2.ValidAt == nil || *rel2.ValidAt != "2026-01" {
		t.Errorf("Expected valid_at=2026-01")
	}
	if rel2.InvalidAt != nil {
		t.Errorf("Expected invalid_at to be nil for current job")
	}
}

func TestValidateRelationships(t *testing.T) {
	extractor := NewRelationshipExtractor(nil, "")

	// Helper to create int pointer
	intPtr := func(i int) *int { return &i }
	strPtr := func(s string) *string { return &s }

	tests := []struct {
		name        string
		input       []ExtractedRelationship
		entityCount int
		wantCount   int
	}{
		{
			name: "valid relationships pass through",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "WORKS_AT",
					TargetEntityID: intPtr(1),
					Fact:           "Tyler works at Anthropic",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   1,
		},
		{
			name: "invalid source entity ID filtered",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 5, // Out of range
					RelationType:   "WORKS_AT",
					TargetEntityID: intPtr(1),
					Fact:           "Tyler works at Anthropic",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   0,
		},
		{
			name: "invalid target entity ID filtered",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "WORKS_AT",
					TargetEntityID: intPtr(10), // Out of range
					Fact:           "Tyler works at Anthropic",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   0,
		},
		{
			name: "negative entity ID filtered",
			input: []ExtractedRelationship{
				{
					SourceEntityID: -1,
					RelationType:   "WORKS_AT",
					TargetEntityID: intPtr(1),
					Fact:           "Tyler works at Anthropic",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   0,
		},
		{
			name: "empty relation type filtered",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "",
					TargetEntityID: intPtr(1),
					Fact:           "Tyler works at Anthropic",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   0,
		},
		{
			name: "empty fact filtered",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "WORKS_AT",
					TargetEntityID: intPtr(1),
					Fact:           "",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   0,
		},
		{
			name: "neither target set filtered",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "WORKS_AT",
					Fact:           "Tyler works somewhere",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   0,
		},
		{
			name: "both targets set - entity preferred for non-identity",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "WORKS_AT",
					TargetEntityID: intPtr(1),
					TargetLiteral:  strPtr("some literal"),
					Fact:           "Tyler works at Anthropic",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   1,
		},
		{
			name: "both targets set - literal preferred for identity",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "HAS_EMAIL",
					TargetEntityID: intPtr(1),
					TargetLiteral:  strPtr("tyler@example.com"),
					Fact:           "Tyler's email",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   1,
		},
		{
			name: "empty source_type defaults to mentioned",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "WORKS_AT",
					TargetEntityID: intPtr(1),
					Fact:           "Tyler works at Anthropic",
					SourceType:     "",
				},
			},
			entityCount: 2,
			wantCount:   1,
		},
		{
			name: "invalid source_type defaults to mentioned",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "WORKS_AT",
					TargetEntityID: intPtr(1),
					Fact:           "Tyler works at Anthropic",
					SourceType:     "invalid_type",
				},
			},
			entityCount: 2,
			wantCount:   1,
		},
		{
			name: "literal target relationship passes",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "HAS_EMAIL",
					TargetLiteral:  strPtr("tyler@example.com"),
					Fact:           "Tyler's email is tyler@example.com",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   1,
		},
		{
			name: "temporal literal relationship passes",
			input: []ExtractedRelationship{
				{
					SourceEntityID: 0,
					RelationType:   "BORN_ON",
					TargetLiteral:  strPtr("1990-05-15"),
					Fact:           "Tyler was born on May 15, 1990",
					SourceType:     "self_disclosed",
				},
			},
			entityCount: 2,
			wantCount:   1,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := extractor.validateRelationships(tt.input, tt.entityCount)
			if len(result) != tt.wantCount {
				t.Errorf("Expected %d relationships, got %d", tt.wantCount, len(result))
			}
		})
	}
}

func TestIsIdentityRelationType(t *testing.T) {
	identityTypes := []string{"HAS_EMAIL", "HAS_PHONE", "HAS_HANDLE", "HAS_USERNAME", "ALSO_KNOWN_AS"}
	for _, relType := range identityTypes {
		if !isIdentityRelationType(relType) {
			t.Errorf("Expected %s to be identity type", relType)
		}
	}

	nonIdentityTypes := []string{"WORKS_AT", "KNOWS", "BORN_ON", "LIVES_IN"}
	for _, relType := range nonIdentityTypes {
		if isIdentityRelationType(relType) {
			t.Errorf("Expected %s to NOT be identity type", relType)
		}
	}
}

func TestIsTemporalRelationType(t *testing.T) {
	temporalTypes := []string{"BORN_ON", "ANNIVERSARY_ON", "OCCURRED_ON", "SCHEDULED_FOR", "STARTED_ON", "ENDED_ON"}
	for _, relType := range temporalTypes {
		if !isTemporalRelationType(relType) {
			t.Errorf("Expected %s to be temporal type", relType)
		}
	}

	nonTemporalTypes := []string{"WORKS_AT", "KNOWS", "HAS_EMAIL", "LIVES_IN"}
	for _, relType := range nonTemporalTypes {
		if isTemporalRelationType(relType) {
			t.Errorf("Expected %s to NOT be temporal type", relType)
		}
	}
}

func TestIsLiteralTargetRelationType(t *testing.T) {
	// Both identity and temporal types should return true
	literalTypes := []string{
		"HAS_EMAIL", "HAS_PHONE", "HAS_HANDLE", "HAS_USERNAME", "ALSO_KNOWN_AS",
		"BORN_ON", "ANNIVERSARY_ON", "OCCURRED_ON", "SCHEDULED_FOR", "STARTED_ON", "ENDED_ON",
	}
	for _, relType := range literalTypes {
		if !IsLiteralTargetRelationType(relType) {
			t.Errorf("Expected %s to use literal target", relType)
		}
	}

	entityTypes := []string{"WORKS_AT", "KNOWS", "LIVES_IN", "CREATED", "OWNS"}
	for _, relType := range entityTypes {
		if IsLiteralTargetRelationType(relType) {
			t.Errorf("Expected %s to NOT use literal target", relType)
		}
	}
}

func TestIsValidSourceType(t *testing.T) {
	validTypes := []string{"self_disclosed", "mentioned", "inferred"}
	for _, st := range validTypes {
		if !isValidSourceType(st) {
			t.Errorf("Expected %s to be valid source type", st)
		}
	}

	invalidTypes := []string{"", "self-disclosed", "SELF_DISCLOSED", "unknown", "observed"}
	for _, st := range invalidTypes {
		if isValidSourceType(st) {
			t.Errorf("Expected %s to NOT be valid source type", st)
		}
	}
}

func TestBuildResolvedEntitiesJSON(t *testing.T) {
	extractor := NewRelationshipExtractor(nil, "")

	entities := []ResolvedEntity{
		{ID: "ent_abc123", Name: "Tyler", EntityTypeID: EntityTypePerson},
		{ID: "ent_def456", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
		{ID: "ent_ghi789", Name: "Austin", EntityTypeID: EntityTypeLocation},
	}

	jsonStr := extractor.buildResolvedEntitiesJSON(entities)

	// Parse it back to verify structure
	var parsed []ResolvedEntityForPrompt
	err := json.Unmarshal([]byte(jsonStr), &parsed)
	if err != nil {
		t.Fatalf("Failed to parse generated JSON: %v", err)
	}

	if len(parsed) != 3 {
		t.Fatalf("Expected 3 entities, got %d", len(parsed))
	}

	// Check first entity
	if parsed[0].ID != 0 {
		t.Errorf("Expected ID=0, got %d", parsed[0].ID)
	}
	if parsed[0].UUID != "ent_abc123" {
		t.Errorf("Expected UUID=ent_abc123, got %s", parsed[0].UUID)
	}
	if parsed[0].Name != "Tyler" {
		t.Errorf("Expected Name=Tyler, got %s", parsed[0].Name)
	}
	if parsed[0].EntityType != "Person" {
		t.Errorf("Expected EntityType=Person, got %s", parsed[0].EntityType)
	}

	// Check second entity
	if parsed[1].ID != 1 {
		t.Errorf("Expected ID=1, got %d", parsed[1].ID)
	}
	if parsed[1].EntityType != "Company" {
		t.Errorf("Expected EntityType=Company, got %s", parsed[1].EntityType)
	}
}

func TestBuildPrompt(t *testing.T) {
	extractor := NewRelationshipExtractor(nil, "")

	input := RelationshipExtractionInput{
		EpisodeContent: "Tyler: My email is tyler@example.com. I work at Anthropic.",
		ResolvedEntities: []ResolvedEntity{
			{ID: "ent_abc123", Name: "Tyler", EntityTypeID: EntityTypePerson},
			{ID: "ent_def456", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
		},
		ReferenceTime: "2026-01-21T10:00:00Z",
	}

	prompt := extractor.buildPrompt(input)

	// Verify prompt contains key elements
	if !contains(prompt, "<RESOLVED_ENTITIES>") {
		t.Error("Prompt should contain RESOLVED_ENTITIES section")
	}
	if !contains(prompt, "<REFERENCE_TIME>") {
		t.Error("Prompt should contain REFERENCE_TIME section")
	}
	if !contains(prompt, "<CURRENT_EPISODE>") {
		t.Error("Prompt should contain CURRENT_EPISODE section")
	}
	if !contains(prompt, "Tyler") {
		t.Error("Prompt should contain entity name Tyler")
	}
	if !contains(prompt, "Anthropic") {
		t.Error("Prompt should contain entity name Anthropic")
	}
	if !contains(prompt, "HAS_EMAIL") {
		t.Error("Prompt should mention HAS_EMAIL relationship type")
	}
	if !contains(prompt, "WORKS_AT") {
		t.Error("Prompt should mention WORKS_AT relationship type")
	}
	if !contains(prompt, "target_literal") {
		t.Error("Prompt should mention target_literal")
	}
	if !contains(prompt, "target_entity_id") {
		t.Error("Prompt should mention target_entity_id")
	}
}

func TestBuildPromptWithPreviousEpisodes(t *testing.T) {
	extractor := NewRelationshipExtractor(nil, "")

	input := RelationshipExtractionInput{
		EpisodeContent:   "Tyler: Starting the new project today.",
		ResolvedEntities: []ResolvedEntity{{ID: "ent_abc", Name: "Tyler", EntityTypeID: EntityTypePerson}},
		PreviousEpisodes: []string{"Yesterday Tyler mentioned he's working on a secret project."},
	}

	prompt := extractor.buildPrompt(input)

	if !contains(prompt, "<PREVIOUS_EPISODES>") {
		t.Error("Prompt should contain PREVIOUS_EPISODES section")
	}
	if !contains(prompt, "secret project") {
		t.Error("Prompt should contain previous episode content")
	}
}

func TestBuildPromptWithCustomInstructions(t *testing.T) {
	extractor := NewRelationshipExtractor(nil, "")

	input := RelationshipExtractionInput{
		EpisodeContent:     "Tyler: Working on Cortex.",
		ResolvedEntities:   []ResolvedEntity{{ID: "ent_abc", Name: "Tyler", EntityTypeID: EntityTypePerson}},
		CustomInstructions: "Focus on extracting project relationships.",
	}

	prompt := extractor.buildPrompt(input)

	if !contains(prompt, "Focus on extracting project relationships.") {
		t.Error("Prompt should contain custom instructions")
	}
}

func TestGetSourceEntityUUID(t *testing.T) {
	entities := []ResolvedEntity{
		{ID: "ent_abc", Name: "Tyler", EntityTypeID: EntityTypePerson},
		{ID: "ent_def", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
	}

	intPtr := func(i int) *int { return &i }

	tests := []struct {
		name     string
		rel      ExtractedRelationship
		expected string
	}{
		{
			name:     "valid source ID",
			rel:      ExtractedRelationship{SourceEntityID: 0, RelationType: "WORKS_AT", TargetEntityID: intPtr(1)},
			expected: "ent_abc",
		},
		{
			name:     "second entity as source",
			rel:      ExtractedRelationship{SourceEntityID: 1, RelationType: "KNOWS", TargetEntityID: intPtr(0)},
			expected: "ent_def",
		},
		{
			name:     "invalid source ID returns empty",
			rel:      ExtractedRelationship{SourceEntityID: 5, RelationType: "WORKS_AT", TargetEntityID: intPtr(1)},
			expected: "",
		},
		{
			name:     "negative source ID returns empty",
			rel:      ExtractedRelationship{SourceEntityID: -1, RelationType: "WORKS_AT", TargetEntityID: intPtr(1)},
			expected: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := GetSourceEntityUUID(tt.rel, entities)
			if result != tt.expected {
				t.Errorf("Expected %s, got %s", tt.expected, result)
			}
		})
	}
}

func TestGetTargetEntityUUID(t *testing.T) {
	entities := []ResolvedEntity{
		{ID: "ent_abc", Name: "Tyler", EntityTypeID: EntityTypePerson},
		{ID: "ent_def", Name: "Anthropic", EntityTypeID: EntityTypeCompany},
	}

	intPtr := func(i int) *int { return &i }
	strPtr := func(s string) *string { return &s }

	tests := []struct {
		name     string
		rel      ExtractedRelationship
		expected string
	}{
		{
			name:     "valid target entity ID",
			rel:      ExtractedRelationship{SourceEntityID: 0, RelationType: "WORKS_AT", TargetEntityID: intPtr(1)},
			expected: "ent_def",
		},
		{
			name:     "literal target returns empty",
			rel:      ExtractedRelationship{SourceEntityID: 0, RelationType: "HAS_EMAIL", TargetLiteral: strPtr("email@example.com")},
			expected: "",
		},
		{
			name:     "nil target entity ID returns empty",
			rel:      ExtractedRelationship{SourceEntityID: 0, RelationType: "WORKS_AT"},
			expected: "",
		},
		{
			name:     "invalid target ID returns empty",
			rel:      ExtractedRelationship{SourceEntityID: 0, RelationType: "WORKS_AT", TargetEntityID: intPtr(10)},
			expected: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := GetTargetEntityUUID(tt.rel, entities)
			if result != tt.expected {
				t.Errorf("Expected %s, got %s", tt.expected, result)
			}
		})
	}
}

// Note: contains helper is defined in entity_extractor_test.go
