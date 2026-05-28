package memory

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"

	"github.com/Napageneral/cortex/internal/gemini"
)

// ExtractedEntity represents an entity extracted from episode content.
// The ID is a temporary identifier (0, 1, 2...) for this extraction only;
// entity resolution assigns real UUIDs.
type ExtractedEntity struct {
	ID           int    `json:"id"`             // Temporary ID for reference within this extraction
	Name         string `json:"name"`           // Name of the extracted entity
	EntityTypeID int    `json:"entity_type_id"` // ID from DefaultEntityTypes
}

// EntityExtractionResult contains the output from entity extraction.
type EntityExtractionResult struct {
	ExtractedEntities []ExtractedEntity `json:"extracted_entities"`
}

// KnownEntity represents an entity we already know about (e.g., thread participant)
type KnownEntity struct {
	Name       string `json:"name"`
	EntityType string `json:"entity_type"`
}

// EntityExtractionInput contains the input for entity extraction.
type EntityExtractionInput struct {
	EpisodeContent     string        // The content of the current episode
	ReferenceTime      string        // ISO 8601 timestamp for temporal reference (optional)
	PreviousEpisodes   []string      // Optional: previous episodes for coreference context
	KnownEntities      []KnownEntity // Optional: entities we already know are in this context (e.g., thread participants)
	CustomInstructions string        // Optional: domain-specific extraction guidance
}

// EntityExtractor extracts entities from episode content using an LLM.
// Extraction is graph-independent — disambiguation happens at resolution time.
type EntityExtractor struct {
	geminiClient *gemini.Client
	model        string
}

// NewEntityExtractor creates a new EntityExtractor.
func NewEntityExtractor(geminiClient *gemini.Client, model string) *EntityExtractor {
	if model == "" {
		model = "gemini-2.0-flash" // Default model
	}
	return &EntityExtractor{
		geminiClient: geminiClient,
		model:        model,
	}
}

// Extract extracts entities from episode content.
// Returns a list of extracted entities with temporary IDs (0, 1, 2...).
func (e *EntityExtractor) Extract(ctx context.Context, input EntityExtractionInput) (*EntityExtractionResult, error) {
	if input.EpisodeContent == "" {
		return &EntityExtractionResult{ExtractedEntities: []ExtractedEntity{}}, nil
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

	var result EntityExtractionResult
	if err := json.Unmarshal([]byte(text), &result); err != nil {
		return nil, fmt.Errorf("parse response JSON: %w (response: %s)", err, text)
	}

	// Filter and validate extracted entities
	filtered := make([]ExtractedEntity, 0, len(result.ExtractedEntities))
	for _, entity := range result.ExtractedEntities {
		// Filter out AI assistants (per spec: "AI agents — no durable identity")
		if isAIAssistant(entity.Name) {
			continue
		}
		// Validate entity type
		if !IsValidEntityTypeID(entity.EntityTypeID) {
			// Default to Entity (type 0) if invalid
			entity.EntityTypeID = EntityTypeEntity
		}
		filtered = append(filtered, entity)
	}
	result.ExtractedEntities = filtered

	return &result, nil
}

// isAIAssistant returns true if the name refers to a known AI assistant.
// Per the spec, AI agents have no durable identity and should not be entities.
func isAIAssistant(name string) bool {
	lowerName := strings.ToLower(strings.TrimSpace(name))
	aiAssistants := []string{
		"claude", "gpt", "chatgpt", "gpt-4", "gpt-3", "gpt-3.5",
		"gemini", "bard", "copilot", "llama", "mistral", "anthropic assistant",
	}
	for _, ai := range aiAssistants {
		if lowerName == ai {
			return true
		}
	}
	return false
}

// buildPrompt constructs the extraction prompt from the template.
func (e *EntityExtractor) buildPrompt(input EntityExtractionInput) string {
	var sb strings.Builder

	// System context
	sb.WriteString("You are an AI assistant that extracts entity nodes from text.\n")
	sb.WriteString("Your primary task is to extract and classify significant entities mentioned in the provided content.\n\n")

	// Entity types
	sb.WriteString("<ENTITY_TYPES>\n")
	sb.WriteString(EntityTypesJSON())
	sb.WriteString("\n</ENTITY_TYPES>\n\n")

	// Known entities (e.g., thread participants we already know about)
	if len(input.KnownEntities) > 0 {
		sb.WriteString("<KNOWN_ENTITIES>\n")
		sb.WriteString("These entities are already known to be present in this context. Include them in your output if they appear in the content:\n")
		for _, ke := range input.KnownEntities {
			sb.WriteString(fmt.Sprintf("- %s (%s)\n", ke.Name, ke.EntityType))
		}
		sb.WriteString("</KNOWN_ENTITIES>\n\n")
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

Extract **entity nodes** from the CURRENT_EPISODE.

### What to Extract

1. **People**: Extract by name. If only a role is mentioned ("my dad", "the CEO"), use a descriptive name like "Dad" or "the CEO".
2. **Organizations**: Companies, schools, institutions.
3. **Projects**: Software, products, codebases, initiatives being discussed.
4. **Locations**: Cities, addresses, countries, venues.
5. **Events**: Named meetings, conferences, occurrences (e.g., "the standup", "HTAA meeting").
6. **Documents**: Files, articles, specs being referenced.
7. **Pets**: Named animals.

### What NOT to Extract

- **Dates**: These are captured as target_literal in relationships, not as entities.
- **AI agents**: Claude, GPT, etc. — no durable identity; the content is what matters.
- **Concepts, technologies, activities, professions**: Searchable via episode text, not entities.
- **Relationships or actions**: "works at" is a relationship, not an entity.
- **Entities only in PREVIOUS_EPISODES**: Those are for coreference context only.

### Formatting Rules

- Use the most complete name available (full names over nicknames)
- Resolve pronouns to their referent when clear from context
- For conversations: always extract speakers as entities (if they're people)

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
  "extracted_entities": [
    {
      "id": 0,
      "name": "Entity Name",
      "entity_type_id": 1
    }
  ]
}

Where:
- id: Temporary integer ID starting from 0
- name: Name of the extracted entity
- entity_type_id: ID from ENTITY_TYPES (0-7)

Return ONLY the JSON object, no other text.
`)

	return sb.String()
}

// EntityTypesJSON returns the entity types as a JSON string for prompt injection.
func EntityTypesJSON() string {
	types := make([]map[string]interface{}, len(DefaultEntityTypes))
	for i, et := range DefaultEntityTypes {
		types[i] = map[string]interface{}{
			"id":          et.ID,
			"name":        et.Name,
			"description": et.Description,
		}
	}
	data, _ := json.MarshalIndent(types, "", "  ")
	return string(data)
}

// extractTextFromResponse extracts the text content from a Gemini response.
func extractTextFromResponse(resp *gemini.GenerateContentResponse) string {
	if resp == nil || len(resp.Candidates) == 0 {
		return ""
	}
	candidate := resp.Candidates[0]
	if len(candidate.Content.Parts) == 0 {
		return ""
	}
	return candidate.Content.Parts[0].Text
}
