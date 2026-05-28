// Command verify-memory runs the memory system verification harness.
//
// Usage:
//
//	verify-memory [flags] [fixture-path]
//
// Flags:
//
//	-fixtures string
//	      Path to fixtures directory (default "scripts/ralph-memory/fixtures")
//	-fixture string
//	      Run only this specific fixture (e.g., "imessage/identity-disclosure")
//	-verbose
//	      Show detailed output for each fixture
//	-model string
//	      LLM model for extraction (default "gemini-2.0-flash")
//	-skip-embeddings
//	      Skip embedding generation (faster for testing)
//
// Exit codes:
//
//	0 - All fixtures passed
//	1 - One or more fixtures failed
//	2 - Error loading fixtures or configuration
package main

import (
	"context"
	"database/sql"
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"github.com/Napageneral/cortex/internal/gemini"
	"github.com/Napageneral/cortex/internal/memory"
	_ "github.com/mattn/go-sqlite3"
)

func main() {
	// Parse flags
	fixturesPath := flag.String("fixtures", "scripts/ralph-memory/fixtures", "Path to fixtures directory")
	singleFixture := flag.String("fixture", "", "Run only this specific fixture (e.g., 'imessage/identity-disclosure')")
	verbose := flag.Bool("verbose", false, "Show detailed output for each fixture")
	model := flag.String("model", "gemini-2.0-flash", "LLM model for extraction")
	skipEmbeddings := flag.Bool("skip-embeddings", true, "Skip embedding generation")
	flag.Parse()

	// Check for GEMINI_API_KEY
	apiKey := os.Getenv("GEMINI_API_KEY")
	if apiKey == "" {
		fmt.Fprintln(os.Stderr, "Error: GEMINI_API_KEY environment variable not set")
		os.Exit(2)
	}

	// Create temporary in-memory database for isolated testing
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error opening database: %v\n", err)
		os.Exit(2)
	}
	defer db.Close()

	// Initialize schema
	if err := initSchema(db); err != nil {
		fmt.Fprintf(os.Stderr, "Error initializing schema: %v\n", err)
		os.Exit(2)
	}

	// Create Gemini client
	geminiClient := gemini.NewClient(apiKey)

	// Create pipeline with config
	pipelineConfig := &memory.PipelineConfig{
		ExtractionModel: *model,
		SkipEmbeddings:  *skipEmbeddings,
	}
	pipeline := memory.NewMemoryPipeline(db, geminiClient, pipelineConfig)

	// Create verification harness
	harness := memory.NewVerificationHarness(db, *fixturesPath, pipeline)

	ctx := context.Background()

	var results []*memory.VerificationResult

	if *singleFixture != "" {
		// Run single fixture
		fixturePath := filepath.Join(*fixturesPath, *singleFixture)
		fixture, err := harness.LoadFixture(fixturePath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error loading fixture %s: %v\n", *singleFixture, err)
			os.Exit(2)
		}

		// Reset database for this fixture
		if err := initSchema(db); err != nil {
			fmt.Fprintf(os.Stderr, "Error resetting schema: %v\n", err)
			os.Exit(2)
		}

		result, err := harness.RunFixture(ctx, fixture)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error running fixture: %v\n", err)
			os.Exit(2)
		}
		results = append(results, result)

		if *verbose && result.ActualOutput != nil {
			fmt.Println("\nActual Output:")
			fmt.Println(memory.FormatDetailedOutput(result.ActualOutput))
		}
	} else {
		// Run all fixtures
		fixtures, err := harness.LoadAllFixtures()
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error loading fixtures: %v\n", err)
			os.Exit(2)
		}

		for _, fixture := range fixtures {
			// Reset database for each fixture to ensure isolation
			if err := initSchema(db); err != nil {
				fmt.Fprintf(os.Stderr, "Error resetting schema for %s: %v\n", fixture.Name, err)
				continue
			}

			result, err := harness.RunFixture(ctx, fixture)
			if err != nil {
				results = append(results, &memory.VerificationResult{
					Fixture: fixture,
					Passed:  false,
					Failures: []memory.VerificationFailure{{
						Category: "execution",
						Type:     "error",
						Message:  err.Error(),
					}},
				})
				continue
			}
			results = append(results, result)

			if *verbose && result.ActualOutput != nil {
				fmt.Printf("\n--- %s/%s Output ---\n", fixture.Source, fixture.Name)
				fmt.Println(memory.FormatDetailedOutput(result.ActualOutput))
			}
		}
	}

	// Print summary
	fmt.Println(memory.FormatSummary(results))

	// Print usage stats
	stats := geminiClient.GetUsageStats()
	fmt.Printf("\n--- API Usage ---\n")
	fmt.Printf("Generate calls: %d\n", stats.GenerateCalls)
	fmt.Printf("Prompt tokens: %d\n", stats.PromptTokens)
	fmt.Printf("Output tokens: %d\n", stats.OutputTokens)
	fmt.Printf("Embed calls: %d\n", stats.EmbedCalls)
	fmt.Printf("Embed characters: %d\n", stats.EmbedChars)
	fmt.Printf("Estimated cost: $%.6f\n", stats.EstimatedCostUSD)

	// Exit with appropriate code
	allPassed := true
	for _, r := range results {
		if !r.Passed {
			allPassed = false
			break
		}
	}

	if allPassed {
		os.Exit(0)
	} else {
		os.Exit(1)
	}
}

// initSchema creates the required tables for the memory system
func initSchema(db *sql.DB) error {
	// Drop existing tables for clean isolation
	tables := []string{
		"episode_relationship_mentions",
		"episode_entity_mentions",
		"entity_merge_events",
		"merge_candidates",
		"relationships",
		"entity_aliases",
		"entities",
		"embeddings",
		"episode_events",
		"episodes",
		"events",
	}

	for _, table := range tables {
		_, _ = db.Exec(fmt.Sprintf("DROP TABLE IF EXISTS %s", table))
	}

	// Create tables in order (dependencies first)
	schema := `
		-- Events table
		CREATE TABLE IF NOT EXISTS events (
			id TEXT PRIMARY KEY,
			channel TEXT NOT NULL,
			timestamp INTEGER NOT NULL,
			content TEXT,
			sender TEXT,
			metadata TEXT,
			created_at TEXT DEFAULT (datetime('now'))
		);

		-- Episodes table
		CREATE TABLE IF NOT EXISTS episodes (
			id TEXT PRIMARY KEY,
			channel TEXT NOT NULL,
			thread_id TEXT,
			start_time INTEGER,
			end_time INTEGER,
			event_count INTEGER DEFAULT 0,
			metadata TEXT,
			created_at TEXT DEFAULT (datetime('now'))
		);

		-- Episode events junction
		CREATE TABLE IF NOT EXISTS episode_events (
			episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
			event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
			position INTEGER NOT NULL,
			PRIMARY KEY (episode_id, event_id)
		);

		-- Embeddings table
		CREATE TABLE IF NOT EXISTS embeddings (
			id TEXT PRIMARY KEY,
			target_type TEXT NOT NULL,
			target_id TEXT NOT NULL,
			model TEXT NOT NULL,
			embedding_blob BLOB NOT NULL,
			dimension INTEGER NOT NULL,
			source_text_hash TEXT,
			created_at INTEGER NOT NULL,
			UNIQUE(target_type, target_id, model)
		);
		CREATE INDEX IF NOT EXISTS idx_embeddings_target ON embeddings(target_type, target_id);
		CREATE INDEX IF NOT EXISTS idx_embeddings_model ON embeddings(model);

		-- Entities table
		CREATE TABLE IF NOT EXISTS entities (
			id TEXT PRIMARY KEY,
			canonical_name TEXT NOT NULL,
			entity_type_id INTEGER NOT NULL,
			summary TEXT,
			summary_updated_at TEXT,
			origin TEXT,
			confidence REAL DEFAULT 1.0,
			merged_into TEXT REFERENCES entities(id),
			created_at TEXT DEFAULT (datetime('now')),
			updated_at TEXT DEFAULT (datetime('now'))
		);
		CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type_id);
		CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(canonical_name);

		-- Entity aliases table
		CREATE TABLE IF NOT EXISTS entity_aliases (
			id TEXT PRIMARY KEY,
			entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
			alias TEXT NOT NULL,
			alias_type TEXT NOT NULL,
			normalized TEXT NOT NULL,
			is_shared INTEGER DEFAULT 0,
			created_at TEXT DEFAULT (datetime('now'))
		);
		CREATE INDEX IF NOT EXISTS idx_entity_aliases_lookup ON entity_aliases(alias, alias_type);
		CREATE INDEX IF NOT EXISTS idx_entity_aliases_normalized ON entity_aliases(normalized, alias_type);
		CREATE INDEX IF NOT EXISTS idx_entity_aliases_entity ON entity_aliases(entity_id);

		-- Relationships table
		CREATE TABLE IF NOT EXISTS relationships (
			id TEXT PRIMARY KEY,
			source_entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
			target_entity_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
			target_literal TEXT,
			relation_type TEXT NOT NULL,
			fact TEXT,
			valid_at TEXT,
			invalid_at TEXT,
			created_at TEXT DEFAULT (datetime('now')),
			confidence REAL DEFAULT 1.0,
			CHECK ((target_entity_id IS NULL) != (target_literal IS NULL))
		);
		CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_entity_id);
		CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_entity_id);
		CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships(relation_type);
		CREATE INDEX IF NOT EXISTS idx_relationships_valid ON relationships(valid_at);
		CREATE INDEX IF NOT EXISTS idx_relationships_invalid ON relationships(invalid_at);
		CREATE UNIQUE INDEX IF NOT EXISTS idx_relationships_unique_entity
			ON relationships(source_entity_id, target_entity_id, relation_type, valid_at)
			WHERE target_entity_id IS NOT NULL;
		CREATE UNIQUE INDEX IF NOT EXISTS idx_relationships_unique_literal
			ON relationships(source_entity_id, target_literal, relation_type, valid_at)
			WHERE target_literal IS NOT NULL;

		-- Episode entity mentions
		CREATE TABLE IF NOT EXISTS episode_entity_mentions (
			episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
			entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
			mention_count INTEGER DEFAULT 1,
			created_at TEXT DEFAULT (datetime('now')),
			PRIMARY KEY (episode_id, entity_id)
		);
		CREATE INDEX IF NOT EXISTS idx_episode_entity_mentions_entity ON episode_entity_mentions(entity_id);

		-- Episode relationship mentions
		CREATE TABLE IF NOT EXISTS episode_relationship_mentions (
			id TEXT PRIMARY KEY,
			episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
			relationship_id TEXT REFERENCES relationships(id) ON DELETE CASCADE,
			extracted_fact TEXT,
			asserted_by_entity_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
			source_type TEXT,
			target_literal TEXT,
			alias_id TEXT REFERENCES entity_aliases(id) ON DELETE SET NULL,
			confidence REAL DEFAULT 1.0,
			created_at TEXT DEFAULT (datetime('now'))
		);
		CREATE INDEX IF NOT EXISTS idx_episode_rel_mentions_episode ON episode_relationship_mentions(episode_id);
		CREATE INDEX IF NOT EXISTS idx_episode_rel_mentions_relationship ON episode_relationship_mentions(relationship_id);

		-- Merge candidates
		CREATE TABLE IF NOT EXISTS merge_candidates (
			id TEXT PRIMARY KEY,
			entity_a_id TEXT NOT NULL REFERENCES entities(id),
			entity_b_id TEXT NOT NULL REFERENCES entities(id),

			-- Scoring
			confidence REAL NOT NULL,
			auto_eligible INTEGER DEFAULT 0,

			-- Evidence
			reason TEXT NOT NULL,
			matching_facts TEXT,
			context TEXT,
			candidates_considered TEXT,

			-- Conflicts
			conflicts TEXT,

			-- Status
			status TEXT DEFAULT 'pending',

			-- Resolution
			created_at TEXT NOT NULL,
			resolved_at TEXT,
			resolved_by TEXT,
			resolution_reason TEXT,
			UNIQUE(entity_a_id, entity_b_id)
		);
		CREATE INDEX IF NOT EXISTS idx_merge_candidates_status ON merge_candidates(status);
		CREATE INDEX IF NOT EXISTS idx_merge_candidates_auto ON merge_candidates(auto_eligible) WHERE status = 'pending';

		-- Entity merge events
		CREATE TABLE IF NOT EXISTS entity_merge_events (
			id TEXT PRIMARY KEY,
			source_entity_id TEXT NOT NULL,
			target_entity_id TEXT NOT NULL,
			merge_type TEXT,
			triggering_facts TEXT,
			similarity_score REAL,
			created_at TEXT DEFAULT (datetime('now')),
			resolved_by TEXT
		);
		CREATE INDEX IF NOT EXISTS idx_entity_merge_events_target ON entity_merge_events(target_entity_id);
	`

	_, err := db.Exec(schema)
	return err
}
