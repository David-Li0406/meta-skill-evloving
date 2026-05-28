package memory

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
)

// FixtureEpisode represents the input episode from episode.json
type FixtureEpisode struct {
	ID            string          `json:"id"`
	Source        string          `json:"source"`
	Channel       string          `json:"channel"`
	ThreadID      string          `json:"thread_id,omitempty"`
	ReferenceTime string          `json:"reference_time"`
	Events        []FixtureEvent  `json:"events"`
	Metadata      FixtureMetadata `json:"metadata,omitempty"`
}

// FixtureEvent represents an event within a fixture episode
type FixtureEvent struct {
	ID               string `json:"id"`
	Timestamp        string `json:"timestamp"`
	Sender           string `json:"sender"`
	SenderIdentifier string `json:"sender_identifier,omitempty"`
	Content          string `json:"content"`
	Direction        string `json:"direction"` // "inbound" or "outbound"
}

// FixtureMetadata contains test metadata
type FixtureMetadata struct {
	Description  string   `json:"description"`
	CoverageTags []string `json:"coverage_tags,omitempty"`
	Notes        string   `json:"notes,omitempty"`
}

// Expectations represents the expected outputs from expectations.yaml
type Expectations struct {
	Description string `yaml:"description"`
	Source      string `yaml:"source,omitempty"`

	Entities                     ExpectationGroup `yaml:"entities,omitempty"`
	Relationships                ExpectationGroup `yaml:"relationships,omitempty"`
	Aliases                      ExpectationGroup `yaml:"aliases,omitempty"`
	EpisodeEntityMentions        ExpectationGroup `yaml:"episode_entity_mentions,omitempty"`
	EpisodeRelationshipMentions  ExpectationGroup `yaml:"episode_relationship_mentions,omitempty"`
}

// ExpectationGroup contains must_have, must_not_have, and optional items
type ExpectationGroup struct {
	MustHave    []map[string]interface{} `yaml:"must_have,omitempty"`
	MustNotHave []map[string]interface{} `yaml:"must_not_have,omitempty"`
	Optional    []map[string]interface{} `yaml:"optional,omitempty"`
}

// Fixture represents a complete test fixture
type Fixture struct {
	Path         string       // Directory path
	Name         string       // Fixture name (directory name)
	Source       string       // Source type (imessage, gmail, aix)
	Episode      FixtureEpisode
	Expectations Expectations
}

// VerificationResult represents the result of running a single fixture
type VerificationResult struct {
	Fixture      *Fixture
	Passed       bool
	Failures     []VerificationFailure
	Warnings     []string
	ActualOutput *VerificationOutput
	Duration     time.Duration
}

// VerificationFailure represents a single assertion failure
type VerificationFailure struct {
	Category    string // "entities", "relationships", "aliases", etc.
	Type        string // "must_have", "must_not_have"
	Expectation map[string]interface{}
	Message     string
}

// VerificationOutput captures the actual outputs from pipeline processing
type VerificationOutput struct {
	Entities                    []VerifyEntity
	Relationships               []VerifyRelationship
	Aliases                     []VerifyAlias
	EpisodeEntityMentions       []VerifyEntityMention
	EpisodeRelationshipMentions []VerifyRelMention
}

// VerifyEntity is an entity with all fields for verification
type VerifyEntity struct {
	ID            string
	CanonicalName string
	EntityTypeID  int
	EntityType    string // Human-readable type name
}

// VerifyRelationship is a relationship with all fields for verification
type VerifyRelationship struct {
	ID               string
	SourceEntityID   string
	SourceEntityName string
	RelationType     string
	TargetEntityID   *string
	TargetEntityName *string
	TargetLiteral    *string
	Fact             string
	ValidAt          *string
	InvalidAt        *string
}

// VerifyAlias is an alias with all fields for verification
type VerifyAlias struct {
	ID             string
	EntityID       string
	EntityName     string
	Alias          string
	AliasType      string
	Normalized     string
	IsShared       bool
}

// VerifyEntityMention represents an episode_entity_mentions row
type VerifyEntityMention struct {
	EpisodeID    string
	EntityID     string
	EntityName   string
	MentionCount int
}

// VerifyRelMention represents an episode_relationship_mentions row
type VerifyRelMention struct {
	ID                string
	EpisodeID         string
	RelationshipID    *string
	ExtractedFact     string
	AssertedByID      *string
	SourceType        string
	TargetLiteral     *string
	AliasID           *string
}

// VerificationHarness loads and runs verification fixtures
type VerificationHarness struct {
	db           *sql.DB
	fixturesPath string
	pipeline     *MemoryPipeline
}

// NewVerificationHarness creates a new VerificationHarness
func NewVerificationHarness(db *sql.DB, fixturesPath string, pipeline *MemoryPipeline) *VerificationHarness {
	return &VerificationHarness{
		db:           db,
		fixturesPath: fixturesPath,
		pipeline:     pipeline,
	}
}

// LoadFixture loads a single fixture from a directory
func (h *VerificationHarness) LoadFixture(fixturePath string) (*Fixture, error) {
	episodePath := filepath.Join(fixturePath, "episode.json")
	expectationsPath := filepath.Join(fixturePath, "expectations.yaml")

	// Load episode.json
	episodeData, err := os.ReadFile(episodePath)
	if err != nil {
		return nil, fmt.Errorf("read episode.json: %w", err)
	}

	var episode FixtureEpisode
	if err := json.Unmarshal(episodeData, &episode); err != nil {
		return nil, fmt.Errorf("parse episode.json: %w", err)
	}

	// Load expectations.yaml
	expectationsData, err := os.ReadFile(expectationsPath)
	if err != nil {
		return nil, fmt.Errorf("read expectations.yaml: %w", err)
	}

	var expectations Expectations
	if err := yaml.Unmarshal(expectationsData, &expectations); err != nil {
		return nil, fmt.Errorf("parse expectations.yaml: %w", err)
	}

	// Extract fixture name and source from path
	name := filepath.Base(fixturePath)
	source := filepath.Base(filepath.Dir(fixturePath))

	return &Fixture{
		Path:         fixturePath,
		Name:         name,
		Source:       source,
		Episode:      episode,
		Expectations: expectations,
	}, nil
}

// LoadAllFixtures loads all fixtures from the fixtures directory
func (h *VerificationHarness) LoadAllFixtures() ([]*Fixture, error) {
	var fixtures []*Fixture

	// Iterate over source directories (imessage, gmail, aix)
	sources, err := os.ReadDir(h.fixturesPath)
	if err != nil {
		return nil, fmt.Errorf("read fixtures directory: %w", err)
	}

	for _, source := range sources {
		if !source.IsDir() || source.Name() == "README.md" {
			continue
		}

		sourcePath := filepath.Join(h.fixturesPath, source.Name())
		fixturesDirs, err := os.ReadDir(sourcePath)
		if err != nil {
			continue
		}

		for _, fixtureDir := range fixturesDirs {
			if !fixtureDir.IsDir() {
				continue
			}

			fixturePath := filepath.Join(sourcePath, fixtureDir.Name())
			fixture, err := h.LoadFixture(fixturePath)
			if err != nil {
				// Log but continue with other fixtures
				fmt.Printf("Warning: failed to load fixture %s: %v\n", fixturePath, err)
				continue
			}
			fixtures = append(fixtures, fixture)
		}
	}

	return fixtures, nil
}

// RunFixture runs a single fixture and returns the verification result
func (h *VerificationHarness) RunFixture(ctx context.Context, fixture *Fixture) (*VerificationResult, error) {
	startTime := time.Now()
	result := &VerificationResult{
		Fixture: fixture,
		Passed:  true,
	}

	// Build episode content from events
	content := h.buildEpisodeContent(fixture.Episode)

	// Parse reference time
	refTime, err := time.Parse(time.RFC3339, fixture.Episode.ReferenceTime)
	if err != nil {
		refTime = time.Now()
	}

	// Create EpisodeInput for the pipeline
	episodeInput := EpisodeInput{
		ID:            fixture.Episode.ID,
		Channel:       fixture.Episode.Channel,
		Content:       content,
		StartTime:     refTime,
		ReferenceTime: fixture.Episode.ReferenceTime,
	}
	if fixture.Episode.ThreadID != "" {
		episodeInput.ThreadID = &fixture.Episode.ThreadID
	}

	// Run the pipeline
	_, err = h.pipeline.Process(ctx, episodeInput)
	if err != nil {
		return nil, fmt.Errorf("pipeline process: %w", err)
	}

	// Collect actual outputs
	output, err := h.collectOutputs(ctx, fixture.Episode.ID)
	if err != nil {
		return nil, fmt.Errorf("collect outputs: %w", err)
	}
	result.ActualOutput = output

	// Verify expectations
	h.verifyExpectations(result, fixture.Expectations, output)

	result.Duration = time.Since(startTime)
	return result, nil
}

// buildEpisodeContent formats events with full context for extraction
func (h *VerificationHarness) buildEpisodeContent(episode FixtureEpisode) string {
	var parts []string

	// Add thread context header
	if episode.ThreadID != "" {
		parts = append(parts, fmt.Sprintf("[Thread: %s]", episode.ThreadID))
	}

	for _, event := range episode.Events {
		if event.Content == "" {
			continue
		}

		// Build event line with full context
		var line strings.Builder

		// Timestamp (if available)
		if event.Timestamp != "" {
			line.WriteString(fmt.Sprintf("[%s] ", event.Timestamp))
		}

		// Sender with identifier (phone/email)
		if event.SenderIdentifier != "" {
			line.WriteString(fmt.Sprintf("%s (%s)", event.Sender, event.SenderIdentifier))
		} else {
			line.WriteString(event.Sender)
		}

		// Direction indicator
		if event.Direction == "outbound" {
			line.WriteString(" →")
		} else {
			line.WriteString(" ←")
		}

		// Content
		line.WriteString(fmt.Sprintf(" %s", event.Content))

		parts = append(parts, line.String())
	}
	return strings.Join(parts, "\n")
}

// collectOutputs queries the database for all outputs related to an episode
func (h *VerificationHarness) collectOutputs(ctx context.Context, episodeID string) (*VerificationOutput, error) {
	output := &VerificationOutput{}

	// Collect entities via episode_entity_mentions
	entities, err := h.collectEntities(ctx, episodeID)
	if err != nil {
		return nil, fmt.Errorf("collect entities: %w", err)
	}
	output.Entities = entities

	// Collect entity mentions
	mentions, err := h.collectEntityMentions(ctx, episodeID)
	if err != nil {
		return nil, fmt.Errorf("collect entity mentions: %w", err)
	}
	output.EpisodeEntityMentions = mentions

	// Collect relationships via episode_relationship_mentions
	relationships, err := h.collectRelationships(ctx, episodeID)
	if err != nil {
		return nil, fmt.Errorf("collect relationships: %w", err)
	}
	output.Relationships = relationships

	// Collect relationship mentions
	relMentions, err := h.collectRelMentions(ctx, episodeID)
	if err != nil {
		return nil, fmt.Errorf("collect relationship mentions: %w", err)
	}
	output.EpisodeRelationshipMentions = relMentions

	// Collect aliases for the entities in this episode
	aliases, err := h.collectAliases(ctx, episodeID)
	if err != nil {
		return nil, fmt.Errorf("collect aliases: %w", err)
	}
	output.Aliases = aliases

	return output, nil
}

func (h *VerificationHarness) collectEntities(ctx context.Context, episodeID string) ([]VerifyEntity, error) {
	rows, err := h.db.QueryContext(ctx, `
		SELECT DISTINCT e.id, e.canonical_name, e.entity_type_id
		FROM entities e
		JOIN episode_entity_mentions eem ON e.id = eem.entity_id
		WHERE eem.episode_id = ?
		  AND e.merged_into IS NULL
	`, episodeID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var entities []VerifyEntity
	for rows.Next() {
		var e VerifyEntity
		if err := rows.Scan(&e.ID, &e.CanonicalName, &e.EntityTypeID); err != nil {
			return nil, err
		}
		// Get human-readable type name
		if et := GetEntityTypeByID(e.EntityTypeID); et != nil {
			e.EntityType = et.Name
		} else {
			e.EntityType = "Unknown"
		}
		entities = append(entities, e)
	}
	return entities, rows.Err()
}

func (h *VerificationHarness) collectEntityMentions(ctx context.Context, episodeID string) ([]VerifyEntityMention, error) {
	rows, err := h.db.QueryContext(ctx, `
		SELECT eem.episode_id, eem.entity_id, e.canonical_name, eem.mention_count
		FROM episode_entity_mentions eem
		JOIN entities e ON eem.entity_id = e.id
		WHERE eem.episode_id = ?
	`, episodeID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var mentions []VerifyEntityMention
	for rows.Next() {
		var m VerifyEntityMention
		if err := rows.Scan(&m.EpisodeID, &m.EntityID, &m.EntityName, &m.MentionCount); err != nil {
			return nil, err
		}
		mentions = append(mentions, m)
	}
	return mentions, rows.Err()
}

func (h *VerificationHarness) collectRelationships(ctx context.Context, episodeID string) ([]VerifyRelationship, error) {
	rows, err := h.db.QueryContext(ctx, `
		SELECT DISTINCT r.id, r.source_entity_id, se.canonical_name,
			   r.relation_type, r.target_entity_id, te.canonical_name,
			   r.target_literal, r.fact, r.valid_at, r.invalid_at
		FROM relationships r
		JOIN episode_relationship_mentions erm ON r.id = erm.relationship_id
		JOIN entities se ON r.source_entity_id = se.id
		LEFT JOIN entities te ON r.target_entity_id = te.id
		WHERE erm.episode_id = ?
	`, episodeID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var relationships []VerifyRelationship
	for rows.Next() {
		var r VerifyRelationship
		var targetEntityID, targetEntityName, targetLiteral, validAt, invalidAt sql.NullString
		if err := rows.Scan(&r.ID, &r.SourceEntityID, &r.SourceEntityName,
			&r.RelationType, &targetEntityID, &targetEntityName,
			&targetLiteral, &r.Fact, &validAt, &invalidAt); err != nil {
			return nil, err
		}
		if targetEntityID.Valid {
			r.TargetEntityID = &targetEntityID.String
		}
		if targetEntityName.Valid {
			r.TargetEntityName = &targetEntityName.String
		}
		if targetLiteral.Valid {
			r.TargetLiteral = &targetLiteral.String
		}
		if validAt.Valid {
			r.ValidAt = &validAt.String
		}
		if invalidAt.Valid {
			r.InvalidAt = &invalidAt.String
		}
		relationships = append(relationships, r)
	}
	return relationships, rows.Err()
}

func (h *VerificationHarness) collectRelMentions(ctx context.Context, episodeID string) ([]VerifyRelMention, error) {
	rows, err := h.db.QueryContext(ctx, `
		SELECT erm.id, erm.episode_id, erm.relationship_id, erm.extracted_fact,
			   erm.asserted_by_entity_id, erm.source_type, erm.target_literal, erm.alias_id
		FROM episode_relationship_mentions erm
		WHERE erm.episode_id = ?
	`, episodeID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var mentions []VerifyRelMention
	for rows.Next() {
		var m VerifyRelMention
		var relID, assertedByID, targetLiteral, aliasID sql.NullString
		if err := rows.Scan(&m.ID, &m.EpisodeID, &relID, &m.ExtractedFact,
			&assertedByID, &m.SourceType, &targetLiteral, &aliasID); err != nil {
			return nil, err
		}
		if relID.Valid {
			m.RelationshipID = &relID.String
		}
		if assertedByID.Valid {
			m.AssertedByID = &assertedByID.String
		}
		if targetLiteral.Valid {
			m.TargetLiteral = &targetLiteral.String
		}
		if aliasID.Valid {
			m.AliasID = &aliasID.String
		}
		mentions = append(mentions, m)
	}
	return mentions, rows.Err()
}

func (h *VerificationHarness) collectAliases(ctx context.Context, episodeID string) ([]VerifyAlias, error) {
	// Get aliases for entities mentioned in this episode
	rows, err := h.db.QueryContext(ctx, `
		SELECT DISTINCT ea.id, ea.entity_id, e.canonical_name,
			   ea.alias, ea.alias_type, ea.normalized, ea.is_shared
		FROM entity_aliases ea
		JOIN entities e ON ea.entity_id = e.id
		JOIN episode_entity_mentions eem ON e.id = eem.entity_id
		WHERE eem.episode_id = ?
	`, episodeID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var aliases []VerifyAlias
	for rows.Next() {
		var a VerifyAlias
		if err := rows.Scan(&a.ID, &a.EntityID, &a.EntityName,
			&a.Alias, &a.AliasType, &a.Normalized, &a.IsShared); err != nil {
			return nil, err
		}
		aliases = append(aliases, a)
	}
	return aliases, rows.Err()
}

// verifyExpectations checks all expectations against actual output
func (h *VerificationHarness) verifyExpectations(result *VerificationResult, expectations Expectations, output *VerificationOutput) {
	// Verify entities
	h.verifyEntityExpectations(result, expectations.Entities, output.Entities)

	// Verify relationships
	h.verifyRelationshipExpectations(result, expectations.Relationships, output.Relationships)

	// Verify aliases
	h.verifyAliasExpectations(result, expectations.Aliases, output.Aliases)

	// Verify entity mentions
	h.verifyEntityMentionExpectations(result, expectations.EpisodeEntityMentions, output.EpisodeEntityMentions)

	// Verify relationship mentions
	h.verifyRelMentionExpectations(result, expectations.EpisodeRelationshipMentions, output.EpisodeRelationshipMentions)
}

func (h *VerificationHarness) verifyEntityExpectations(result *VerificationResult, group ExpectationGroup, entities []VerifyEntity) {
	// Check must_have
	for _, expected := range group.MustHave {
		if !h.matchEntity(expected, entities) {
			result.Passed = false
			result.Failures = append(result.Failures, VerificationFailure{
				Category:    "entities",
				Type:        "must_have",
				Expectation: expected,
				Message:     fmt.Sprintf("Expected entity not found: %v", expected),
			})
		}
	}

	// Check must_not_have
	for _, forbidden := range group.MustNotHave {
		if h.matchEntity(forbidden, entities) {
			result.Passed = false
			result.Failures = append(result.Failures, VerificationFailure{
				Category:    "entities",
				Type:        "must_not_have",
				Expectation: forbidden,
				Message:     fmt.Sprintf("Forbidden entity found: %v", forbidden),
			})
		}
	}
}

func (h *VerificationHarness) matchEntity(expected map[string]interface{}, entities []VerifyEntity) bool {
	for _, entity := range entities {
		if h.entityMatches(expected, entity) {
			return true
		}
	}
	return false
}

func (h *VerificationHarness) entityMatches(expected map[string]interface{}, entity VerifyEntity) bool {
	// Check name
	if name, ok := expected["name"].(string); ok {
		if entity.CanonicalName != name {
			return false
		}
	}

	// Check name_contains
	if nameContains, ok := expected["name_contains"].(string); ok {
		if !strings.Contains(strings.ToLower(entity.CanonicalName), strings.ToLower(nameContains)) {
			return false
		}
	}

	// Check entity_type
	if entityType, ok := expected["entity_type"].(string); ok {
		if entityType != "any" && !strings.EqualFold(entity.EntityType, entityType) {
			return false
		}
	}

	return true
}

func (h *VerificationHarness) verifyRelationshipExpectations(result *VerificationResult, group ExpectationGroup, relationships []VerifyRelationship) {
	// Check must_have
	for _, expected := range group.MustHave {
		if !h.matchRelationship(expected, relationships) {
			result.Passed = false
			result.Failures = append(result.Failures, VerificationFailure{
				Category:    "relationships",
				Type:        "must_have",
				Expectation: expected,
				Message:     fmt.Sprintf("Expected relationship not found: %v", expected),
			})
		}
	}

	// Check must_not_have
	for _, forbidden := range group.MustNotHave {
		if h.matchRelationship(forbidden, relationships) {
			result.Passed = false
			result.Failures = append(result.Failures, VerificationFailure{
				Category:    "relationships",
				Type:        "must_not_have",
				Expectation: forbidden,
				Message:     fmt.Sprintf("Forbidden relationship found: %v", forbidden),
			})
		}
	}
}

func (h *VerificationHarness) matchRelationship(expected map[string]interface{}, relationships []VerifyRelationship) bool {
	for _, rel := range relationships {
		if h.relationshipMatches(expected, rel) {
			return true
		}
	}
	return false
}

func (h *VerificationHarness) relationshipMatches(expected map[string]interface{}, rel VerifyRelationship) bool {
	// Check relation_type
	if relType, ok := expected["relation_type"].(string); ok {
		if rel.RelationType != relType {
			return false
		}
	}

	// Check source_entity_name_contains
	if sourceContains, ok := expected["source_entity_name_contains"].(string); ok {
		if !strings.Contains(strings.ToLower(rel.SourceEntityName), strings.ToLower(sourceContains)) {
			return false
		}
	}

	// Check target_entity_name_contains
	if targetContains, ok := expected["target_entity_name_contains"].(string); ok {
		if rel.TargetEntityName == nil || !strings.Contains(strings.ToLower(*rel.TargetEntityName), strings.ToLower(targetContains)) {
			return false
		}
	}

	// Check target (shorthand for target_entity_name_contains)
	if target, ok := expected["target"].(string); ok {
		if rel.TargetEntityName == nil || !strings.Contains(strings.ToLower(*rel.TargetEntityName), strings.ToLower(target)) {
			return false
		}
	}

	// Check target_literal
	if literal, ok := expected["target_literal"].(string); ok {
		if rel.TargetLiteral == nil || *rel.TargetLiteral != literal {
			return false
		}
	}

	// Check target_literal_like (SQL LIKE pattern with %)
	if literalLike, ok := expected["target_literal_like"].(string); ok {
		if rel.TargetLiteral == nil || !matchLikePattern(*rel.TargetLiteral, literalLike) {
			return false
		}
	}

	// Check valid_at
	if validAtVal, exists := expected["valid_at"]; exists {
		if validAtVal == nil {
			// Expecting null - relationship must have nil ValidAt
			if rel.ValidAt != nil {
				return false
			}
		} else if validAt, ok := validAtVal.(string); ok {
			if rel.ValidAt == nil || *rel.ValidAt != validAt {
				return false
			}
		}
	}

	// Check valid_at_like
	if validAtLike, ok := expected["valid_at_like"].(string); ok {
		if rel.ValidAt == nil || !matchLikePattern(*rel.ValidAt, validAtLike) {
			return false
		}
	}

	// Check invalid_at
	if invalidAtVal, exists := expected["invalid_at"]; exists {
		if invalidAtVal == nil {
			// Expecting null - relationship must have nil InvalidAt
			if rel.InvalidAt != nil {
				return false
			}
		} else if invalidAt, ok := invalidAtVal.(string); ok {
			if rel.InvalidAt == nil || *rel.InvalidAt != invalidAt {
				return false
			}
		}
	}

	// Check invalid_at_like
	if invalidAtLike, ok := expected["invalid_at_like"].(string); ok {
		if rel.InvalidAt == nil || !matchLikePattern(*rel.InvalidAt, invalidAtLike) {
			return false
		}
	}

	return true
}

func (h *VerificationHarness) verifyAliasExpectations(result *VerificationResult, group ExpectationGroup, aliases []VerifyAlias) {
	// Check must_have
	for _, expected := range group.MustHave {
		if !h.matchAlias(expected, aliases) {
			result.Passed = false
			result.Failures = append(result.Failures, VerificationFailure{
				Category:    "aliases",
				Type:        "must_have",
				Expectation: expected,
				Message:     fmt.Sprintf("Expected alias not found: %v", expected),
			})
		}
	}

	// Check must_not_have
	for _, forbidden := range group.MustNotHave {
		if h.matchAlias(forbidden, aliases) {
			result.Passed = false
			result.Failures = append(result.Failures, VerificationFailure{
				Category:    "aliases",
				Type:        "must_not_have",
				Expectation: forbidden,
				Message:     fmt.Sprintf("Forbidden alias found: %v", forbidden),
			})
		}
	}
}

func (h *VerificationHarness) matchAlias(expected map[string]interface{}, aliases []VerifyAlias) bool {
	for _, alias := range aliases {
		if h.aliasMatches(expected, alias) {
			return true
		}
	}
	return false
}

func (h *VerificationHarness) aliasMatches(expected map[string]interface{}, alias VerifyAlias) bool {
	// Check entity_name_contains
	if entityContains, ok := expected["entity_name_contains"].(string); ok {
		if !strings.Contains(strings.ToLower(alias.EntityName), strings.ToLower(entityContains)) {
			return false
		}
	}

	// Check alias (exact match)
	if aliasVal, ok := expected["alias"].(string); ok {
		if alias.Alias != aliasVal {
			return false
		}
	}

	// Check alias_type
	if aliasType, ok := expected["alias_type"].(string); ok {
		if alias.AliasType != aliasType {
			return false
		}
	}

	// Check is_shared
	if isShared, ok := expected["is_shared"].(bool); ok {
		if alias.IsShared != isShared {
			return false
		}
	}

	return true
}

func (h *VerificationHarness) verifyEntityMentionExpectations(result *VerificationResult, group ExpectationGroup, mentions []VerifyEntityMention) {
	// Check must_have
	for _, expected := range group.MustHave {
		if !h.matchEntityMention(expected, mentions) {
			result.Passed = false
			result.Failures = append(result.Failures, VerificationFailure{
				Category:    "episode_entity_mentions",
				Type:        "must_have",
				Expectation: expected,
				Message:     fmt.Sprintf("Expected entity mention not found: %v", expected),
			})
		}
	}

	// Check must_not_have
	for _, forbidden := range group.MustNotHave {
		if h.matchEntityMention(forbidden, mentions) {
			result.Passed = false
			result.Failures = append(result.Failures, VerificationFailure{
				Category:    "episode_entity_mentions",
				Type:        "must_not_have",
				Expectation: forbidden,
				Message:     fmt.Sprintf("Forbidden entity mention found: %v", forbidden),
			})
		}
	}
}

func (h *VerificationHarness) matchEntityMention(expected map[string]interface{}, mentions []VerifyEntityMention) bool {
	for _, mention := range mentions {
		if h.entityMentionMatches(expected, mention) {
			return true
		}
	}
	return false
}

func (h *VerificationHarness) entityMentionMatches(expected map[string]interface{}, mention VerifyEntityMention) bool {
	// Check entity_name_contains
	if entityContains, ok := expected["entity_name_contains"].(string); ok {
		if !strings.Contains(strings.ToLower(mention.EntityName), strings.ToLower(entityContains)) {
			return false
		}
	}

	return true
}

func (h *VerificationHarness) verifyRelMentionExpectations(result *VerificationResult, group ExpectationGroup, mentions []VerifyRelMention) {
	// Check must_have
	for _, expected := range group.MustHave {
		if !h.matchRelMention(expected, mentions) {
			result.Passed = false
			result.Failures = append(result.Failures, VerificationFailure{
				Category:    "episode_relationship_mentions",
				Type:        "must_have",
				Expectation: expected,
				Message:     fmt.Sprintf("Expected relationship mention not found: %v", expected),
			})
		}
	}

	// Check must_not_have
	for _, forbidden := range group.MustNotHave {
		if h.matchRelMention(forbidden, mentions) {
			result.Passed = false
			result.Failures = append(result.Failures, VerificationFailure{
				Category:    "episode_relationship_mentions",
				Type:        "must_not_have",
				Expectation: forbidden,
				Message:     fmt.Sprintf("Forbidden relationship mention found: %v", forbidden),
			})
		}
	}
}

func (h *VerificationHarness) matchRelMention(expected map[string]interface{}, mentions []VerifyRelMention) bool {
	for _, mention := range mentions {
		if h.relMentionMatches(expected, mention) {
			return true
		}
	}
	return false
}

func (h *VerificationHarness) relMentionMatches(expected map[string]interface{}, mention VerifyRelMention) bool {
	// Check extracted_fact_contains
	if factContains, ok := expected["extracted_fact_contains"].(string); ok {
		if !strings.Contains(strings.ToLower(mention.ExtractedFact), strings.ToLower(factContains)) {
			return false
		}
	}

	// Check source_type
	if sourceType, ok := expected["source_type"].(string); ok {
		if mention.SourceType != sourceType {
			return false
		}
	}

	// Check target_literal
	if targetLiteral, ok := expected["target_literal"].(string); ok {
		if mention.TargetLiteral == nil || *mention.TargetLiteral != targetLiteral {
			return false
		}
	}

	// Check relationship_id (null check)
	if relID, ok := expected["relationship_id"]; ok {
		if relID == nil {
			// Expected null
			if mention.RelationshipID != nil {
				return false
			}
		} else if relIDStr, ok := relID.(string); ok {
			if mention.RelationshipID == nil || *mention.RelationshipID != relIDStr {
				return false
			}
		}
	}

	return true
}

// matchLikePattern implements SQL LIKE pattern matching
// Supports % as wildcard (matches any sequence of characters)
func matchLikePattern(value, pattern string) bool {
	// Convert SQL LIKE pattern to a simple prefix/suffix/contains check
	if pattern == "%" {
		return true // Match everything
	}

	if strings.HasPrefix(pattern, "%") && strings.HasSuffix(pattern, "%") {
		// %contains%
		substr := pattern[1 : len(pattern)-1]
		return strings.Contains(value, substr)
	}

	if strings.HasSuffix(pattern, "%") {
		// prefix%
		prefix := pattern[:len(pattern)-1]
		return strings.HasPrefix(value, prefix)
	}

	if strings.HasPrefix(pattern, "%") {
		// %suffix
		suffix := pattern[1:]
		return strings.HasSuffix(value, suffix)
	}

	// Exact match
	return value == pattern
}

// RunAll runs all fixtures and returns results
func (h *VerificationHarness) RunAll(ctx context.Context) ([]*VerificationResult, error) {
	fixtures, err := h.LoadAllFixtures()
	if err != nil {
		return nil, fmt.Errorf("load fixtures: %w", err)
	}

	var results []*VerificationResult
	for _, fixture := range fixtures {
		result, err := h.RunFixture(ctx, fixture)
		if err != nil {
			// Record error as failure, continue with other fixtures
			results = append(results, &VerificationResult{
				Fixture: fixture,
				Passed:  false,
				Failures: []VerificationFailure{{
					Category: "execution",
					Type:     "error",
					Message:  err.Error(),
				}},
			})
			continue
		}
		results = append(results, result)
	}

	return results, nil
}

// FormatResult formats a single verification result as human-readable text
func FormatResult(result *VerificationResult) string {
	var sb strings.Builder

	status := "PASS"
	if !result.Passed {
		status = "FAIL"
	}

	sb.WriteString(fmt.Sprintf("[%s] %s/%s (%s)\n", status, result.Fixture.Source, result.Fixture.Name, result.Duration))

	if len(result.Failures) > 0 {
		sb.WriteString("  Failures:\n")
		for _, f := range result.Failures {
			sb.WriteString(fmt.Sprintf("    - [%s/%s] %s\n", f.Category, f.Type, f.Message))
		}
	}

	if len(result.Warnings) > 0 {
		sb.WriteString("  Warnings:\n")
		for _, w := range result.Warnings {
			sb.WriteString(fmt.Sprintf("    - %s\n", w))
		}
	}

	return sb.String()
}

// FormatSummary formats a summary of all results
func FormatSummary(results []*VerificationResult) string {
	var sb strings.Builder

	passed := 0
	failed := 0
	for _, r := range results {
		if r.Passed {
			passed++
		} else {
			failed++
		}
	}

	sb.WriteString(fmt.Sprintf("Verification Summary: %d passed, %d failed, %d total\n", passed, failed, len(results)))
	sb.WriteString(strings.Repeat("-", 60) + "\n")

	for _, result := range results {
		sb.WriteString(FormatResult(result))
	}

	return sb.String()
}

// FormatDetailedOutput formats the actual output for debugging
func FormatDetailedOutput(output *VerificationOutput) string {
	var sb strings.Builder

	sb.WriteString("Entities:\n")
	for _, e := range output.Entities {
		sb.WriteString(fmt.Sprintf("  - %s (%s): %s\n", e.CanonicalName, e.EntityType, e.ID))
	}

	sb.WriteString("\nRelationships:\n")
	for _, r := range output.Relationships {
		target := "<literal>"
		if r.TargetEntityName != nil {
			target = *r.TargetEntityName
		} else if r.TargetLiteral != nil {
			target = fmt.Sprintf("\"%s\"", *r.TargetLiteral)
		}
		validAt := "?"
		if r.ValidAt != nil {
			validAt = *r.ValidAt
		}
		sb.WriteString(fmt.Sprintf("  - %s -[%s]-> %s (valid_at: %s)\n", r.SourceEntityName, r.RelationType, target, validAt))
	}

	sb.WriteString("\nAliases:\n")
	for _, a := range output.Aliases {
		shared := ""
		if a.IsShared {
			shared = " [shared]"
		}
		sb.WriteString(fmt.Sprintf("  - %s: %s (%s)%s\n", a.EntityName, a.Alias, a.AliasType, shared))
	}

	sb.WriteString("\nEntity Mentions:\n")
	for _, m := range output.EpisodeEntityMentions {
		sb.WriteString(fmt.Sprintf("  - %s (count: %d)\n", m.EntityName, m.MentionCount))
	}

	sb.WriteString("\nRelationship Mentions:\n")
	for _, m := range output.EpisodeRelationshipMentions {
		relID := "null"
		if m.RelationshipID != nil {
			relID = *m.RelationshipID
		}
		sb.WriteString(fmt.Sprintf("  - %s (source_type: %s, rel_id: %s)\n", m.ExtractedFact, m.SourceType, relID))
	}

	return sb.String()
}
