package adapters

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"os/exec"
	"time"

	"github.com/google/uuid"
	_ "modernc.org/sqlite"
)

// BirdAdapter syncs X/Twitter events via bird CLI
type BirdAdapter struct {
	username string
}

// NewBirdAdapter creates a new bird adapter
func NewBirdAdapter(username string) (*BirdAdapter, error) {
	// Verify bird is available
	if _, err := exec.LookPath("bird"); err != nil {
		return nil, fmt.Errorf("bird not found in PATH. Install with: brew install steipete/tap/bird")
	}

	// Get username from bird whoami if not provided
	if username == "" {
		cmd := exec.Command("bird", "whoami", "--plain")
		output, err := cmd.CombinedOutput()
		if err != nil {
			return nil, fmt.Errorf("failed to get X account: %w (output: %s)", err, string(output))
		}
		// Parse output to get username
		username = "unknown"
	}

	return &BirdAdapter{
		username: username,
	}, nil
}

func (b *BirdAdapter) Name() string {
	return "x"
}

func (b *BirdAdapter) Sync(ctx context.Context, cortexDB *sql.DB, full bool) (SyncResult, error) {
	startTime := time.Now()
	result := SyncResult{}

	// Enable foreign keys on cortex DB
	if _, err := cortexDB.Exec("PRAGMA foreign_keys = ON"); err != nil {
		return result, fmt.Errorf("failed to enable foreign keys: %w", err)
	}

	// Sync bookmarks (tweets you've saved)
	bookmarksCreated, bookmarksPersons, err := b.syncBookmarks(ctx, cortexDB)
	if err != nil {
		fmt.Printf("Warning: failed to sync bookmarks: %v\n", err)
	}
	result.EventsCreated += bookmarksCreated
	result.PersonsCreated += bookmarksPersons

	// Sync likes (tweets you've engaged with)
	likesCreated, likesPersons, err := b.syncLikes(ctx, cortexDB)
	if err != nil {
		fmt.Printf("Warning: failed to sync likes: %v\n", err)
	}
	result.EventsCreated += likesCreated
	result.PersonsCreated += likesPersons

	// Sync mentions (tweets mentioning you)
	mentionsCreated, mentionsPersons, err := b.syncMentions(ctx, cortexDB)
	if err != nil {
		fmt.Printf("Warning: failed to sync mentions: %v\n", err)
	}
	result.EventsCreated += mentionsCreated
	result.PersonsCreated += mentionsPersons

	// Update sync watermark
	now := time.Now().Unix()
	_, err = cortexDB.Exec(`
		INSERT INTO sync_watermarks (adapter, last_sync_at)
		VALUES (?, ?)
		ON CONFLICT(adapter) DO UPDATE SET last_sync_at = excluded.last_sync_at
	`, b.Name(), now)
	if err != nil {
		return result, fmt.Errorf("failed to update sync watermark: %w", err)
	}

	result.Duration = time.Since(startTime)
	return result, nil
}

// BirdTweet represents a tweet from bird CLI JSON output
type BirdTweet struct {
	ID             string `json:"id"`
	Text           string `json:"text"`
	CreatedAt      string `json:"createdAt"`
	ReplyCount     int    `json:"replyCount"`
	RetweetCount   int    `json:"retweetCount"`
	LikeCount      int    `json:"likeCount"`
	ConversationID string `json:"conversationId"`
	Author         struct {
		Username string `json:"username"`
		Name     string `json:"name"`
	} `json:"author"`
	AuthorID string `json:"authorId"`
}

func (b *BirdAdapter) syncBookmarks(ctx context.Context, cortexDB *sql.DB) (int, int, error) {
	tweets, err := b.fetchTweets(ctx, "bookmarks", "-n", "100")
	if err != nil {
		return 0, 0, err
	}
	return b.syncTweets(cortexDB, tweets, "bookmark")
}

func (b *BirdAdapter) syncLikes(ctx context.Context, cortexDB *sql.DB) (int, int, error) {
	tweets, err := b.fetchTweets(ctx, "likes", "-n", "100")
	if err != nil {
		return 0, 0, err
	}
	return b.syncTweets(cortexDB, tweets, "like")
}

func (b *BirdAdapter) syncMentions(ctx context.Context, cortexDB *sql.DB) (int, int, error) {
	tweets, err := b.fetchTweets(ctx, "mentions", "-n", "100")
	if err != nil {
		return 0, 0, err
	}
	return b.syncTweets(cortexDB, tweets, "mention")
}

func (b *BirdAdapter) fetchTweets(ctx context.Context, command string, args ...string) ([]BirdTweet, error) {
	cmdArgs := append([]string{command}, args...)
	cmdArgs = append(cmdArgs, "--json")

	cmd := exec.CommandContext(ctx, "bird", cmdArgs...)
	// Capture stdout only (JSON), ignore stderr (warnings)
	output, err := cmd.Output()
	if err != nil {
		// For exit errors, include stderr
		if exitErr, ok := err.(*exec.ExitError); ok {
			return nil, fmt.Errorf("bird %s failed: %w (stderr: %s)", command, err, string(exitErr.Stderr))
		}
		return nil, fmt.Errorf("bird %s failed: %w", command, err)
	}

	// Handle empty output (no results)
	if len(output) == 0 {
		return []BirdTweet{}, nil
	}

	var tweets []BirdTweet
	if err := json.Unmarshal(output, &tweets); err != nil {
		return nil, fmt.Errorf("failed to parse bird JSON: %w (output: %s)", err, string(output))
	}

	return tweets, nil
}

func (b *BirdAdapter) syncTweets(cortexDB *sql.DB, tweets []BirdTweet, interactionType string) (int, int, error) {
	eventsCreated := 0
	personsCreated := 0

	for _, tweet := range tweets {
		// Parse tweet timestamp
		var timestamp int64
		if t, err := time.Parse(time.RubyDate, tweet.CreatedAt); err == nil {
			timestamp = t.Unix()
		} else {
			timestamp = time.Now().Unix()
		}

		// Build content types
		contentTypesJSON := `["text"]`

		// Create event - use interaction type + tweet ID as source_id for uniqueness
		sourceID := fmt.Sprintf("%s:%s", interactionType, tweet.ID)
		eventID := uuid.New().String()

		_, err := cortexDB.Exec(`
			INSERT INTO events (
				id, timestamp, channel, content_types, content,
				direction, thread_id, reply_to, source_adapter, source_id
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
			ON CONFLICT(source_adapter, source_id) DO UPDATE SET
				content = excluded.content,
				content_types = excluded.content_types
		`, eventID, timestamp, "x", contentTypesJSON, tweet.Text,
			"observed", tweet.ConversationID, "", b.Name(), sourceID)

		if err != nil {
			return eventsCreated, personsCreated, fmt.Errorf("failed to insert event: %w", err)
		}

		// Check if this was an insert
		var existingEventID string
		row := cortexDB.QueryRow("SELECT id FROM events WHERE source_adapter = ? AND source_id = ?", b.Name(), sourceID)
		if err := row.Scan(&existingEventID); err == nil && existingEventID == eventID {
			eventsCreated++
		}

		// Create person for author
		if tweet.Author.Username != "" {
			personID, created, err := b.getOrCreatePersonByHandle(cortexDB, tweet.Author.Username, tweet.Author.Name)
			if err != nil {
				return eventsCreated, personsCreated, fmt.Errorf("failed to create person: %w", err)
			}
			if created {
				personsCreated++
			}

			// Add as sender
			_, err = cortexDB.Exec(`
				INSERT INTO event_participants (event_id, person_id, role)
				VALUES (?, ?, ?)
				ON CONFLICT(event_id, person_id, role) DO NOTHING
			`, eventID, personID, "sender")
			if err != nil {
				return eventsCreated, personsCreated, fmt.Errorf("failed to insert participant: %w", err)
			}
		}
	}

	return eventsCreated, personsCreated, nil
}

func (b *BirdAdapter) getOrCreatePersonByHandle(cortexDB *sql.DB, handle, displayName string) (string, bool, error) {
	handle = "@" + handle

	// Try to find existing person by X handle
	var personID string
	row := cortexDB.QueryRow(`
		SELECT person_id FROM identities
		WHERE channel = 'x' AND identifier = ?
	`, handle)
	if err := row.Scan(&personID); err == nil {
		return personID, false, nil
	} else if err != sql.ErrNoRows {
		return "", false, fmt.Errorf("failed to query identity: %w", err)
	}

	// Person doesn't exist, create new one
	personID = uuid.New().String()
	now := time.Now().Unix()

	canonicalName := displayName
	if canonicalName == "" {
		canonicalName = handle
	}

	_, err := cortexDB.Exec(`
		INSERT INTO persons (id, canonical_name, display_name, is_me, created_at, updated_at)
		VALUES (?, ?, ?, 0, ?, ?)
	`, personID, canonicalName, displayName, now, now)
	if err != nil {
		return "", false, fmt.Errorf("failed to insert person: %w", err)
	}

	// Create identity
	identityID := uuid.New().String()
	_, err = cortexDB.Exec(`
		INSERT INTO identities (id, person_id, channel, identifier, created_at)
		VALUES (?, ?, ?, ?, ?)
		ON CONFLICT(channel, identifier) DO NOTHING
	`, identityID, personID, "x", handle, now)
	if err != nil {
		return "", false, fmt.Errorf("failed to insert identity: %w", err)
	}

	return personID, true, nil
}
