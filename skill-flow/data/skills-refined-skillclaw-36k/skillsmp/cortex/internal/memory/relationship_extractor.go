package memory

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"

	"github.com/Napageneral/cortex/internal/gemini"
)

// ExtractedRelationship represents a relationship extracted from episode content.
// The source/target IDs reference the resolved entity IDs from entity resolution.
type ExtractedRelationship struct {
	SourceEntityID int     `json:"source_entity_id"` // ID from resolved entities
	RelationType   string  `json:"relation_type"`    // SCREAMING_SNAKE_CASE
	TargetEntityID *int    `json:"target_entity_id"` // ID from resolved entities (for entity targets)
	TargetLiteral  *string `json:"target_literal"`   // For identity/temporal relationships
	Fact           string  `json:"fact"`             // Natural language description
	SourceType     string  `json:"source_type"`      // 'self_disclosed', 'mentioned', 'inferred'
	ValidAt        *string `json:"valid_at"`         // ISO 8601 date when became true (optional)
	InvalidAt      *string `json:"invalid_at"`       // ISO 8601 date when stopped being true (optional)
}

// RelationshipExtractionResult contains the output from relationship extraction.
type RelationshipExtractionResult struct {
	ExtractedRelationships []ExtractedRelationship `json:"extracted_relationships"`
}

// RelationshipExtractionInput contains the input for relationship extraction.
type RelationshipExtractionInput struct {
	EpisodeContent   string           // The content of the current episode
	ResolvedEntities []ResolvedEntity // Entities with resolved UUIDs from entity resolution
	ReferenceTime    string           // ISO 8601 timestamp for temporal reference
	PreviousEpisodes []string         // Optional: previous episodes for coreference context
	CustomInstructions string         // Optional: domain-specific extraction guidance
}

// ResolvedEntityForPrompt is the structure passed to the LLM prompt.
// Uses temporary ID for LLM reference while carrying the real UUID.
type ResolvedEntityForPrompt struct {
	ID         int    `json:"id"`          // Temporary ID for reference in extraction
	UUID       string `json:"uuid"`        // Real entity UUID
	Name       string `json:"name"`        // Canonical name
	EntityType string `json:"entity_type"` // Human-readable type name
}

// RelationshipExtractor extracts relationships from episode content using an LLM.
// It runs after entity extraction and resolution to ensure relationships
// reference resolved entity UUIDs.
type RelationshipExtractor struct {
	geminiClient *gemini.Client
	model        string
}

// NewRelationshipExtractor creates a new RelationshipExtractor.
func NewRelationshipExtractor(geminiClient *gemini.Client, model string) *RelationshipExtractor {
	if model == "" {
		model = "gemini-2.0-flash" // Default model
	}
	return &RelationshipExtractor{
		geminiClient: geminiClient,
		model:        model,
	}
}

// Extract extracts relationships from episode content.
// The resolved entities are passed in with their UUIDs, and relationships
// reference them via temporary IDs (0, 1, 2...).
func (e *RelationshipExtractor) Extract(ctx context.Context, input RelationshipExtractionInput) (*RelationshipExtractionResult, error) {
	if input.EpisodeContent == "" {
		return &RelationshipExtractionResult{ExtractedRelationships: []ExtractedRelationship{}}, nil
	}

	if len(input.ResolvedEntities) == 0 {
		return &RelationshipExtractionResult{ExtractedRelationships: []ExtractedRelationship{}}, nil
	}

	prompt := e.buildPrompt(input)

	req := &gemini.GenerateContentRequest{
		Contents: []gemini.Content{{
			Role:  "user",
			Parts: []gemini.Part{{Text: prompt}},
		}},
		GenerationConfig: &gemini.GenerationConfig{
			ResponseMimeType: "application/json",
		},
	}

	resp, err := e.geminiClient.GenerateContent(ctx, e.model, req)
	if err != nil {
		return nil, fmt.Errorf("generate content: %w", err)
	}

	text := extractTextFromResponse(resp)
	if text == "" {
		return nil, fmt.Errorf("empty response from LLM")
	}

	var result RelationshipExtractionResult
	if err := json.Unmarshal([]byte(text), &result); err != nil {
		return nil, fmt.Errorf("parse response JSON: %w (response: %s)", err, text)
	}

	// Validate extracted relationships
	result.ExtractedRelationships = e.validateRelationships(result.ExtractedRelationships, len(input.ResolvedEntities))

	return &result, nil
}

// validateRelationships validates and filters extracted relationships.
func (e *RelationshipExtractor) validateRelationships(rels []ExtractedRelationship, entityCount int) []ExtractedRelationship {
	valid := make([]ExtractedRelationship, 0, len(rels))

	for _, rel := range rels {
		// Validate source entity ID is in range
		if rel.SourceEntityID < 0 || rel.SourceEntityID >= entityCount {
			continue // Skip invalid source
		}

		// Validate relation type is not empty
		if rel.RelationType == "" {
			continue
		}

		// Validate exactly one of target_entity_id or target_literal is set
		hasTargetEntity := rel.TargetEntityID != nil
		hasTargetLiteral := rel.TargetLiteral != nil && *rel.TargetLiteral != ""

		if hasTargetEntity && hasTargetLiteral {
			// Both set - prefer entity for non-identity types, literal for identity types
			if isIdentityRelationType(rel.RelationType) || isTemporalRelationType(rel.RelationType) {
				rel.TargetEntityID = nil
			} else {
				rel.TargetLiteral = nil
			}
		} else if !hasTargetEntity && !hasTargetLiteral {
			continue // Neither set, skip
		}

		// Validate target entity ID is in range if present
		if rel.TargetEntityID != nil {
			if *rel.TargetEntityID < 0 || *rel.TargetEntityID >= entityCount {
				continue // Skip invalid target
			}
		}

		// Validate source_type
		if rel.SourceType == "" {
			rel.SourceType = "mentioned" // Default
		}
		if !isValidSourceType(rel.SourceType) {
			rel.SourceType = "mentioned"
		}

		// Validate fact is not empty
		if rel.Fact == "" {
			continue
		}

		valid = append(valid, rel)
	}

	return valid
}

// isIdentityRelationType returns true if the relation type is an identity relationship.
func isIdentityRelationType(relType string) bool {
	switch relType {
	case "HAS_EMAIL", "HAS_PHONE", "HAS_HANDLE", "HAS_USERNAME", "ALSO_KNOWN_AS":
		return true
	default:
		return false
	}
}

// isTemporalRelationType returns true if the relation type is a temporal relationship.
func isTemporalRelationType(relType string) bool {
	switch relType {
	case "BORN_ON", "ANNIVERSARY_ON", "OCCURRED_ON", "SCHEDULED_FOR", "STARTED_ON", "ENDED_ON":
		return true
	default:
		return false
	}
}

// isValidSourceType returns true if the source type is valid.
func isValidSourceType(sourceType string) bool {
	switch sourceType {
	case "self_disclosed", "mentioned", "inferred":
		return true
	default:
		return false
	}
}

// IsLiteralTargetRelationType returns true if the relation type uses target_literal.
// This includes both identity and temporal relationship types.
func IsLiteralTargetRelationType(relType string) bool {
	return isIdentityRelationType(relType) || isTemporalRelationType(relType)
}

// buildPrompt constructs the extraction prompt from the template.
func (e *RelationshipExtractor) buildPrompt(input RelationshipExtractionInput) string {
	var sb strings.Builder

	// System context
	sb.WriteString("You are an AI assistant that extracts relationships from text.\n")
	sb.WriteString("Your task is to identify facts connecting the provided entities, including temporal and identity information.\n\n")

	// Resolved entities
	sb.WriteString("<RESOLVED_ENTITIES>\n")
	entitiesJSON := e.buildResolvedEntitiesJSON(input.ResolvedEntities)
	sb.WriteString(entitiesJSON)
	sb.WriteString("\n</RESOLVED_ENTITIES>\n\n")

	// Reference time
	if input.ReferenceTime != "" {
		sb.WriteString("<REFERENCE_TIME>\n")
		sb.WriteString(input.ReferenceTime)
		sb.WriteString("\n</REFERENCE_TIME>\n\n")
	}

	// Previous episodes (for coreference context)
	if len(input.PreviousEpisodes) > 0 {
		sb.WriteString("<PREVIOUS_EPISODES>\n")
		for _, ep := range input.PreviousEpisodes {
			sb.WriteString(ep)
			sb.WriteString("\n---\n")
		}
		sb.WriteString("</PREVIOUS_EPISODES>\n\n")
	}

	// Current episode
	sb.WriteString("<CURRENT_EPISODE>\n")
	sb.WriteString(input.EpisodeContent)
	sb.WriteString("\n</CURRENT_EPISODE>\n\n")

	// Instructions
	sb.WriteString(`## Instructions

Extract relationships (facts) from the CURRENT_EPISODE.

### Relationship Structure

Each relationship is a triple: (source_entity) --RELATION_TYPE--> (target)

The target is either:
- **Another entity** (target_entity_id) — for most relationships
- **A literal value** (target_literal) — for identity and temporal relationships

### target_literal Relationships

These relationship types use target_literal instead of target_entity_id:

| Category | Relationship Types | Format | Promoted to Alias? |
|----------|-------------------|--------|-------------------|
| **Identity** | HAS_EMAIL | email@example.com | Yes |
| **Identity** | HAS_PHONE | +1-555-123-4567 | Yes |
| **Identity** | HAS_HANDLE | @username | Yes |
| **Identity** | HAS_USERNAME | username | Yes |
| **Identity** | ALSO_KNOWN_AS | Nickname | Yes |
| **Financial** | HAS_ACCOUNT_NUMBER | account number string | No |
| **Financial** | HAS_ROUTING_NUMBER | routing number string | No |
| **Financial** | HAS_COMPENSATION | 280k TC, $150k base | No |
| **Credentials** | HAS_PASSWORD | password string | No |
| **Credentials** | HAS_IP_ADDRESS | IP address | No |
| **Temporal** | BORN_ON | 1990-05-15 | No |
| **Temporal** | ANNIVERSARY_ON | 2023-02-18 | No |
| **Temporal** | OCCURRED_ON | 2026-01-22 | No |
| **Temporal** | SCHEDULED_FOR | 2026-01-25 | No |
| **Temporal** | STARTED_ON | 2024-01 | No |
| **Temporal** | ENDED_ON | 2025-12 | No |

**Date format:** ISO 8601 — YYYY-MM-DD (full date), YYYY-MM (month), or YYYY (year).

Use REFERENCE_TIME to resolve relative dates ("yesterday", "last month", "next week").

### URL Pattern Recognition

When you see profile URLs, extract the handle as HAS_HANDLE:
- venmo.com/u/{username} → HAS_HANDLE: @{username}
- twitter.com/{username} or x.com/{username} → HAS_HANDLE: @{username}
- instagram.com/{username} → HAS_HANDLE: @{username}
- github.com/{username} → HAS_HANDLE: @{username}
- linkedin.com/in/{username} → HAS_HANDLE: {username}

**Important**: If a URL is shared and context suggests it belongs to a mentioned person, associate the handle with THAT person, not create a new entity from the username.

### target_entity_id Relationships

All other relationships point to entities:

| Category | Relationship Types | Target Entity Type |
|----------|-------------------|-------------------|
| Personal | BORN_IN, LIVES_IN | Location |
| Personal | HAS_PET | Pet |
| Professional | WORKS_AT, OWNS, FOUNDED | Company/Organization |
| Professional | CUSTOMER_OF, USES | Company (vendor/service) |
| Professional | ATTENDED (school) | Company (school) |
| Social | KNOWS, FRIEND_OF, SPOUSE_OF, PARENT_OF, CHILD_OF, SIBLING_OF, DATING | Person |

**Direction semantics for hierarchical relationships:**
- PARENT_OF: source is the parent of target (e.g., "Alice is the parent of Bob" → Alice --PARENT_OF--> Bob)
- CHILD_OF: source is the child of target (e.g., "Bob is the child of Alice" → Bob --CHILD_OF--> Alice)
| Legal | SUED_BY, DEFENDANT_IN, PLAINTIFF_IN | Person or Organization |
| Legal | FILED_BANKRUPTCY_IN | Location (court jurisdiction) |
| Projects | CREATED, BUILDING, WORKING_ON, CONTRIBUTED_TO | Project |
| Events | ATTENDED, HOSTED, SCHEDULED_FOR | Event |
| Location | LOCATED_IN, VISITED | Location |
| Content | AUTHORED, REFERENCES | Document |
| Financial | WIRED_TO, RECEIVED_FROM | Person or Company |

### Required Fields

- source_entity_id: ID from RESOLVED_ENTITIES
- relation_type: SCREAMING_SNAKE_CASE
- target_entity_id OR target_literal: Where the relationship points (exactly one)
- fact: Natural language description
- source_type: self_disclosed / mentioned / inferred

### Temporal Fields (valid_at / invalid_at)

Extract dates when relationships started (valid_at) or ended (invalid_at):

| Signal Words | Field | Example |
|--------------|-------|---------|
| "started at", "joined", "began", "since" | valid_at | "I started at Anthropic" → valid_at: 2026-01 |
| "left", "quit", "used to", "former", "ex-", "previously" | invalid_at | "I left Intent Systems" → invalid_at: 2025-12 |
| "for N months/years", "been together since" | valid_at | "dating for 6 months" → valid_at: 6 months ago |

Use REFERENCE_TIME to resolve relative dates ("last month" = month before reference_time).

**Critical**: When someone says "I left X", extract the relationship WITH invalid_at set. The fact becomes "Person used to work at X" with invalid_at populated.

### Source Type Guidelines

- **self_disclosed**: The source entity directly stated this about themselves
- **mentioned**: Someone else mentioned this fact about the source entity
- **inferred**: The fact is implied but not explicitly stated

`)

	// Custom instructions
	if input.CustomInstructions != "" {
		sb.WriteString(input.CustomInstructions)
		sb.WriteString("\n\n")
	}

	// Output schema
	sb.WriteString(`## Output Schema

Return a JSON object with this exact structure:
{
  "extracted_relationships": [
    {
      "source_entity_id": 0,
      "relation_type": "RELATION_TYPE",
      "target_entity_id": 1,
      "fact": "Natural language description",
      "source_type": "self_disclosed"
    },
    {
      "source_entity_id": 0,
      "relation_type": "HAS_EMAIL",
      "target_literal": "email@example.com",
      "fact": "Natural language description",
      "source_type": "self_disclosed"
    }
  ]
}

Where:
- source_entity_id: Integer ID from RESOLVED_ENTITIES (0, 1, 2...)
- relation_type: SCREAMING_SNAKE_CASE relationship type
- target_entity_id: Integer ID from RESOLVED_ENTITIES (for entity targets)
- target_literal: String value (for identity/temporal targets)
- fact: Human-readable description of the relationship
- source_type: 'self_disclosed', 'mentioned', or 'inferred'
- valid_at: (optional) ISO date when became true
- invalid_at: (optional) ISO date when stopped being true

Return ONLY the JSON object, no other text.
`)

	return sb.String()
}

// buildResolvedEntitiesJSON builds the JSON representation of resolved entities for the prompt.
func (e *RelationshipExtractor) buildResolvedEntitiesJSON(entities []ResolvedEntity) string {
	promptEntities := make([]ResolvedEntityForPrompt, len(entities))
	for i, ent := range entities {
		typeName := "Entity"
		if et := GetEntityTypeByID(ent.EntityTypeID); et != nil {
			typeName = et.Name
		}
		promptEntities[i] = ResolvedEntityForPrompt{
			ID:         i,
			UUID:       ent.ID,
			Name:       ent.Name,
			EntityType: typeName,
		}
	}
	data, _ := json.MarshalIndent(promptEntities, "", "  ")
	return string(data)
}

// MapRelationshipsToUUIDs converts temporary entity IDs in relationships to UUIDs.
// This is used after extraction to map the LLM's temporary IDs to real entity UUIDs.
func MapRelationshipsToUUIDs(rels []ExtractedRelationship, entities []ResolvedEntity) []ExtractedRelationship {
	result := make([]ExtractedRelationship, len(rels))
	copy(result, rels)
	// Note: The source_entity_id and target_entity_id remain as indices.
	// The actual UUID mapping is done by the caller using entities[id].ID
	return result
}

// GetSourceEntityUUID returns the UUID for a relationship's source entity.
func GetSourceEntityUUID(rel ExtractedRelationship, entities []ResolvedEntity) string {
	if rel.SourceEntityID >= 0 && rel.SourceEntityID < len(entities) {
		return entities[rel.SourceEntityID].ID
	}
	return ""
}

// GetTargetEntityUUID returns the UUID for a relationship's target entity (if applicable).
func GetTargetEntityUUID(rel ExtractedRelationship, entities []ResolvedEntity) string {
	if rel.TargetEntityID == nil {
		return ""
	}
	if *rel.TargetEntityID >= 0 && *rel.TargetEntityID < len(entities) {
		return entities[*rel.TargetEntityID].ID
	}
	return ""
}
