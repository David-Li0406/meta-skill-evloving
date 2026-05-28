// Command verify-memory-live runs memory extraction directly against cortex.db
// using proper event encoding with sender names, attachments, and reactions.
//
// Usage:
//
//	verify-memory-live [flags]
//
// Flags:
//
//	-threads string
//	      Comma-separated thread IDs to test (default: auto-selects top threads)
//	-episodes-per-thread int
//	      Number of episodes to extract per thread (default: 10)
//	-events-per-episode int
//	      Number of events per episode (default: 50)
//	-verbose
//	      Show detailed output
package main

import (
	"context"
	"database/sql"
	"flag"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/Napageneral/cortex/internal/gemini"
	"github.com/Napageneral/cortex/internal/memory"
	_ "github.com/mattn/go-sqlite3"
)

const cortexDBPath = "/Users/tyler/Library/Application Support/Cortex/cortex.db"

func main() {
	// Parse flags
	threadIDs := flag.String("threads", "", "Comma-separated thread IDs (empty = auto-select)")
	episodesPerThread := flag.Int("episodes-per-thread", 5, "Episodes per thread")
	eventsPerEpisode := flag.Int("events-per-episode", 50, "Events per episode")
	verbose := flag.Bool("verbose", false, "Show detailed output")
	model := flag.String("model", "gemini-2.0-flash", "LLM model for extraction")
	outputDB := flag.String("output-db", "", "Path to output SQLite DB (persists results)")
	flag.Parse()

	// Check for GEMINI_API_KEY
	apiKey := os.Getenv("GEMINI_API_KEY")
	if apiKey == "" {
		fmt.Fprintln(os.Stderr, "Error: GEMINI_API_KEY environment variable not set")
		os.Exit(2)
	}

	// Open cortex.db (read-only for source data)
	cortexDB, err := sql.Open("sqlite3", cortexDBPath+"?mode=ro")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error opening cortex.db: %v\n", err)
		os.Exit(2)
	}
	defer cortexDB.Close()

	// Create database for memory system (file or in-memory)
	dbPath := ":memory:"
	if *outputDB != "" {
		dbPath = *outputDB
		// Remove existing file for clean slate
		os.Remove(dbPath)
	}
	memDB, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating memory db: %v\n", err)
		os.Exit(2)
	}
	defer memDB.Close()

	// Initialize memory schema
	if err := initMemorySchema(memDB); err != nil {
		fmt.Fprintf(os.Stderr, "Error initializing schema: %v\n", err)
		os.Exit(2)
	}

	persistResults := *outputDB != ""

	// Create Gemini client
	geminiClient := gemini.NewClient(apiKey)

	// Create pipeline
	pipelineConfig := &memory.PipelineConfig{
		ExtractionModel: *model,
		SkipEmbeddings:  true, // Skip for faster testing
	}
	pipeline := memory.NewMemoryPipeline(memDB, geminiClient, pipelineConfig)

	ctx := context.Background()

	// Get threads to test
	var threads []ThreadInfo
	if *threadIDs == "" {
		// Auto-select diverse threads
		threads, err = selectDiverseThreads(cortexDB, 10)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error selecting threads: %v\n", err)
			os.Exit(2)
		}
	} else {
		for _, id := range strings.Split(*threadIDs, ",") {
			info, err := getThreadInfo(cortexDB, strings.TrimSpace(id))
			if err != nil {
				fmt.Fprintf(os.Stderr, "Warning: thread %s not found: %v\n", id, err)
				continue
			}
			threads = append(threads, info)
		}
	}

	fmt.Printf("Testing %d threads × %d episodes × %d events = %d total events\n\n",
		len(threads), *episodesPerThread, *eventsPerEpisode,
		len(threads)**episodesPerThread**eventsPerEpisode)

	// Process each thread
	var totalEntities, totalRelationships int
	var totalDuration time.Duration

	for _, thread := range threads {
		fmt.Printf("=== Thread: %s ===\n", thread.DisplayName())
		fmt.Printf("    ID: %s\n", thread.ID)
		fmt.Printf("    Channel: %s\n", thread.Channel)
		fmt.Printf("    Event count: %d\n", thread.EventCount)

		// Get episodes for this thread
		episodes, err := getEpisodes(cortexDB, thread.ID, *episodesPerThread, *eventsPerEpisode)
		if err != nil {
			fmt.Printf("    Error getting episodes: %v\n\n", err)
			continue
		}

		// Get thread participants for context
		participants, _ := getThreadParticipants(cortexDB, thread.ID)

		// Build episode context
		episodeCtx := &EpisodeContext{
			ThreadName:   thread.Name,
			Channel:      thread.Channel,
			IsGroup:      thread.IsGroup,
			Participants: participants,
		}

		// Convert participants to known entities for the pipeline
		var knownEntities []memory.KnownEntity
		for _, p := range participants {
			knownEntities = append(knownEntities, memory.KnownEntity{
				Name:       p,
				EntityType: "Person",
			})
		}

		for i, ep := range episodes {
			// Encode episode with rich context
			content := encodeEpisodeWithContext(ep, episodeCtx)

			// Create pipeline input
			input := memory.EpisodeInput{
				ID:            fmt.Sprintf("%s-ep%d", thread.ID, i),
				Channel:       thread.Channel,
				ThreadID:      &thread.ID,
				Content:       content,
				StartTime:     ep.StartTime,
				ReferenceTime: ep.EndTime.Format(time.RFC3339),
				KnownEntities: knownEntities,
			}

			// Process through pipeline
			start := time.Now()
			result, err := pipeline.Process(ctx, input)
			duration := time.Since(start)
			totalDuration += duration

			if err != nil {
				fmt.Printf("    Episode %d: ERROR - %v\n", i+1, err)
				continue
			}

			totalEntities += result.NewEntities
			totalRelationships += result.NewRelationships

			if *verbose {
				fmt.Printf("    Episode %d (%d events, %s):\n", i+1, len(ep.Events), duration.Round(time.Millisecond))
				fmt.Printf("      Entities: %d new, %d existing\n", result.NewEntities, result.ExistingEntities)
				fmt.Printf("      Relationships: %d new, %d existing\n", result.NewRelationships, result.ExistingRelationships)
				fmt.Printf("      Aliases: %d, Mentions: %d\n", result.AliasesCreated, result.EntityMentionsCreated)
			}

			// Reset memory DB for each episode to test in isolation (unless persisting)
			if !persistResults {
				if err := initMemorySchema(memDB); err != nil {
					fmt.Printf("    Error resetting schema: %v\n", err)
				}
			}
		}
		fmt.Println()
	}

	// Print summary
	fmt.Println("=== Summary ===")
	fmt.Printf("Total entities extracted: %d\n", totalEntities)
	fmt.Printf("Total relationships extracted: %d\n", totalRelationships)
	fmt.Printf("Total processing time: %s\n", totalDuration.Round(time.Millisecond))

	// Print API usage
	stats := geminiClient.GetUsageStats()
	fmt.Printf("\n--- API Usage ---\n")
	fmt.Printf("Generate calls: %d\n", stats.GenerateCalls)
	fmt.Printf("Prompt tokens: %d\n", stats.PromptTokens)
	fmt.Printf("Output tokens: %d\n", stats.OutputTokens)
	fmt.Printf("Estimated cost: $%.6f\n", stats.EstimatedCostUSD)

	// Print database info if persisted
	if persistResults {
		fmt.Printf("\n--- Results persisted to: %s ---\n", *outputDB)
		fmt.Println("Query examples:")
		fmt.Println("  sqlite3 " + *outputDB + " \"SELECT canonical_name, entity_type_id FROM entities ORDER BY canonical_name\"")
		fmt.Println("  sqlite3 " + *outputDB + " \"SELECT e1.canonical_name, r.relation_type, COALESCE(e2.canonical_name, r.target_literal) FROM relationships r JOIN entities e1 ON r.source_entity_id = e1.id LEFT JOIN entities e2 ON r.target_entity_id = e2.id\"")
	}
}

// ThreadInfo contains metadata about a thread
type ThreadInfo struct {
	ID         string
	Channel    string
	Name       string
	EventCount int
	IsGroup    bool
}

func (t ThreadInfo) DisplayName() string {
	if t.Name != "" {
		return t.Name
	}
	// Extract identifier from thread ID
	parts := strings.SplitN(t.ID, ":", 2)
	if len(parts) == 2 {
		return parts[1]
	}
	return t.ID
}

// Episode contains a batch of events for processing
type Episode struct {
	Events    []Event
	StartTime time.Time
	EndTime   time.Time
}

// Event represents a single event with sender info
type Event struct {
	ID         string
	Timestamp  time.Time
	SenderName string
	Content    string
	Direction  string
	HasImage   bool
}

// selectDiverseThreads selects a diverse set of threads for testing
func selectDiverseThreads(db *sql.DB, count int) ([]ThreadInfo, error) {
	// Get top threads by event count, mixing 1:1 and group chats
	query := `
		SELECT 
			e.thread_id,
			COALESCE(t.channel, 'unknown') as channel,
			COALESCE(t.name, '') as name,
			COUNT(*) as event_count,
			CASE WHEN e.thread_id LIKE '%chat%' THEN 1 ELSE 0 END as is_group
		FROM events e
		LEFT JOIN threads t ON e.thread_id = t.id
		WHERE e.thread_id IS NOT NULL
		  AND e.content IS NOT NULL
		  AND e.content != ''
		GROUP BY e.thread_id
		ORDER BY event_count DESC
		LIMIT ?
	`
	rows, err := db.Query(query, count*2) // Get more to filter
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var threads []ThreadInfo
	var groups, oneOnOne int

	for rows.Next() {
		var t ThreadInfo
		var isGroup int
		if err := rows.Scan(&t.ID, &t.Channel, &t.Name, &t.EventCount, &isGroup); err != nil {
			continue
		}
		t.IsGroup = isGroup == 1

		// Balance group vs 1:1
		if t.IsGroup && groups < count/3 {
			threads = append(threads, t)
			groups++
		} else if !t.IsGroup && oneOnOne < count*2/3 {
			threads = append(threads, t)
			oneOnOne++
		}

		if len(threads) >= count {
			break
		}
	}

	return threads, rows.Err()
}

// getThreadInfo gets info about a specific thread
func getThreadInfo(db *sql.DB, threadID string) (ThreadInfo, error) {
	query := `
		SELECT 
			e.thread_id,
			COALESCE(t.channel, 'unknown'),
			COALESCE(t.name, ''),
			COUNT(*),
			CASE WHEN e.thread_id LIKE '%chat%' THEN 1 ELSE 0 END
		FROM events e
		LEFT JOIN threads t ON e.thread_id = t.id
		WHERE e.thread_id = ?
		GROUP BY e.thread_id
	`
	var t ThreadInfo
	var isGroup int
	err := db.QueryRow(query, threadID).Scan(&t.ID, &t.Channel, &t.Name, &t.EventCount, &isGroup)
	t.IsGroup = isGroup == 1
	return t, err
}

// getThreadParticipants gets the names of participants in a thread
func getThreadParticipants(db *sql.DB, threadID string) ([]string, error) {
	// Filter out phone numbers, emails, and other non-name identifiers
	query := `
		SELECT DISTINCT COALESCE(p.canonical_name, p.display_name, 'Unknown') as name
		FROM events e
		JOIN event_participants ep ON e.id = ep.event_id
		JOIN persons p ON ep.person_id = p.id
		WHERE e.thread_id = ?
		  AND p.canonical_name IS NOT NULL
		  AND p.canonical_name != ''
		  AND p.canonical_name NOT GLOB '[0-9]*'
		  AND p.canonical_name NOT LIKE '%@%'
		ORDER BY name
		LIMIT 20
	`
	rows, err := db.Query(query, threadID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var participants []string
	for rows.Next() {
		var name string
		if err := rows.Scan(&name); err != nil {
			continue
		}
		participants = append(participants, name)
	}
	return participants, rows.Err()
}

// getEpisodes gets episodes (batched events) from a thread
func getEpisodes(db *sql.DB, threadID string, numEpisodes, eventsPerEpisode int) ([]Episode, error) {
	// Get events with sender names from event_participants
	query := `
		SELECT 
			e.id,
			e.timestamp,
			COALESCE(p.canonical_name, p.display_name, 
				CASE e.direction WHEN 'sent' THEN 'Me' ELSE 'Unknown' END) as sender,
			COALESCE(e.content, '') as content,
			e.direction,
			CASE WHEN e.content_types LIKE '%image%' THEN 1 ELSE 0 END as has_image
		FROM events e
		LEFT JOIN event_participants ep ON e.id = ep.event_id AND ep.role = 'sender'
		LEFT JOIN persons p ON ep.person_id = p.id
		WHERE e.thread_id = ?
		  AND e.content IS NOT NULL
		  AND e.content != ''
		ORDER BY e.timestamp DESC
		LIMIT ?
	`

	totalEvents := numEpisodes * eventsPerEpisode
	rows, err := db.Query(query, threadID, totalEvents)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var allEvents []Event
	for rows.Next() {
		var ev Event
		var ts int64
		var hasImage int
		if err := rows.Scan(&ev.ID, &ts, &ev.SenderName, &ev.Content, &ev.Direction, &hasImage); err != nil {
			continue
		}
		ev.Timestamp = time.Unix(ts, 0)
		ev.HasImage = hasImage == 1
		allEvents = append(allEvents, ev)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}

	// Reverse to chronological order
	for i, j := 0, len(allEvents)-1; i < j; i, j = i+1, j-1 {
		allEvents[i], allEvents[j] = allEvents[j], allEvents[i]
	}

	// Batch into episodes
	var episodes []Episode
	for i := 0; i < len(allEvents) && len(episodes) < numEpisodes; i += eventsPerEpisode {
		end := i + eventsPerEpisode
		if end > len(allEvents) {
			end = len(allEvents)
		}
		if end-i < 10 { // Skip tiny episodes
			continue
		}

		batch := allEvents[i:end]
		ep := Episode{
			Events:    batch,
			StartTime: batch[0].Timestamp,
			EndTime:   batch[len(batch)-1].Timestamp,
		}
		episodes = append(episodes, ep)
	}

	return episodes, nil
}

// EpisodeContext contains metadata about the episode for encoding
type EpisodeContext struct {
	ThreadName   string
	Channel      string
	IsGroup      bool
	Participants []string // Known participants in this thread
}

// encodeEpisode encodes an episode with rich context for LLM extraction
// Format:
//
//	<EPISODE_CONTEXT>
//	Thread: Casey Adams (iMessage, 1:1)
//	Participants: Tyler Brandt, Casey Adams
//	</EPISODE_CONTEXT>
//
//	<MESSAGES>
//	[2025-01-20T09:15:23Z] Casey Adams: heading to the gym now
//	[2025-01-20T09:16:01Z] Tyler Brandt: ok have fun!
//	  → Casey Adams ❤️
//	</MESSAGES>
func encodeEpisode(ep Episode) string {
	return encodeEpisodeWithContext(ep, nil)
}

// encodeEpisodeWithContext encodes an episode with optional thread context
func encodeEpisodeWithContext(ep Episode, ctx *EpisodeContext) string {
	var sb strings.Builder

	// Episode context header (if provided)
	if ctx != nil {
		sb.WriteString("<EPISODE_CONTEXT>\n")
		
		// Thread info
		threadType := "1:1"
		if ctx.IsGroup {
			threadType = "group"
		}
		if ctx.ThreadName != "" {
			sb.WriteString(fmt.Sprintf("Thread: %s (%s, %s)\n", ctx.ThreadName, ctx.Channel, threadType))
		} else {
			sb.WriteString(fmt.Sprintf("Thread: (%s, %s)\n", ctx.Channel, threadType))
		}
		
		// Participants
		if len(ctx.Participants) > 0 {
			sb.WriteString(fmt.Sprintf("Participants: %s\n", strings.Join(ctx.Participants, ", ")))
		}
		
		sb.WriteString("</EPISODE_CONTEXT>\n\n")
	}

	// Messages section
	sb.WriteString("<MESSAGES>\n")

	for _, ev := range ep.Events {
		// ISO 8601 timestamp + sender + content
		timestamp := ev.Timestamp.UTC().Format(time.RFC3339)
		
		if ev.Content != "" {
			sb.WriteString(fmt.Sprintf("[%s] %s: %s", timestamp, ev.SenderName, ev.Content))
		} else if ev.HasImage {
			sb.WriteString(fmt.Sprintf("[%s] %s:", timestamp, ev.SenderName))
		} else {
			continue // Skip empty events
		}

		// Attachment on same line
		if ev.HasImage {
			sb.WriteString(" [Image]")
		}
		sb.WriteString("\n")

		// TODO: Add reactions on indented line when we have reaction data
		// e.g., "  → Casey Adams ❤️\n"
	}

	sb.WriteString("</MESSAGES>")

	return sb.String()
}

// initMemorySchema creates the memory system schema (matches cmd/verify-memory)
func initMemorySchema(db *sql.DB) error {
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
	for _, t := range tables {
		db.Exec("DROP TABLE IF EXISTS " + t)
	}

	schema := `
		CREATE TABLE IF NOT EXISTS events (
			id TEXT PRIMARY KEY,
			channel TEXT NOT NULL,
			timestamp INTEGER NOT NULL,
			content TEXT,
			sender TEXT,
			metadata TEXT,
			created_at TEXT DEFAULT (datetime('now'))
		);

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

		CREATE TABLE IF NOT EXISTS episode_events (
			episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
			event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
			position INTEGER NOT NULL,
			PRIMARY KEY (episode_id, event_id)
		);

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

		CREATE TABLE IF NOT EXISTS episode_entity_mentions (
			episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
			entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
			mention_count INTEGER DEFAULT 1,
			created_at TEXT DEFAULT (datetime('now')),
			PRIMARY KEY (episode_id, entity_id)
		);
		CREATE INDEX IF NOT EXISTS idx_episode_entity_mentions_entity ON episode_entity_mentions(entity_id);

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

		CREATE TABLE IF NOT EXISTS merge_candidates (
			id TEXT PRIMARY KEY,
			entity_a_id TEXT NOT NULL REFERENCES entities(id),
			entity_b_id TEXT NOT NULL REFERENCES entities(id),
			confidence REAL NOT NULL,
			auto_eligible INTEGER DEFAULT 0,
			reason TEXT NOT NULL,
			matching_facts TEXT,
			context TEXT,
			candidates_considered TEXT,
			conflicts TEXT,
			status TEXT DEFAULT 'pending',
			created_at TEXT NOT NULL,
			resolved_at TEXT,
			resolved_by TEXT,
			resolution_reason TEXT,
			UNIQUE(entity_a_id, entity_b_id)
		);
		CREATE INDEX IF NOT EXISTS idx_merge_candidates_status ON merge_candidates(status);

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
	`
	_, err := db.Exec(schema)
	return err
}
