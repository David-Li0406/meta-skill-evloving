package adapters

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"mime"
	"net/mail"
	"os/exec"
	"strconv"
	"strings"
	"sync"
	"time"

	"encoding/base64"
	"github.com/Napageneral/cortex/internal/bus"
	"github.com/Napageneral/cortex/internal/state"
	"github.com/google/uuid"
	_ "modernc.org/sqlite"
)

// GmailAdapter syncs Gmail events via gogcli
type GmailAdapter struct {
	name    string
	account string
	opts    GmailAdapterOptions
}

type GmailAdapterOptions struct {
	Workers          int
	QPS              float64
	SearchPageDelay  time.Duration
	MaxPages         int
	MaxThreadRetries int
}

func (o GmailAdapterOptions) withDefaults() GmailAdapterOptions {
	if o.Workers <= 0 {
		o.Workers = 8
	}
	if o.QPS <= 0 {
		o.QPS = 8 // slightly aggressive; retries handle rate limits
	}
	if o.SearchPageDelay <= 0 {
		o.SearchPageDelay = 500 * time.Millisecond
	}
	if o.MaxPages <= 0 {
		o.MaxPages = 500
	}
	if o.MaxThreadRetries <= 0 {
		o.MaxThreadRetries = 8
	}
	return o
}

// NewGmailAdapter creates a new Gmail adapter
func NewGmailAdapter(name, account string, opts GmailAdapterOptions) (*GmailAdapter, error) {
	if name == "" {
		return nil, fmt.Errorf("adapter instance name is required for Gmail adapter")
	}
	if account == "" {
		return nil, fmt.Errorf("account email is required for Gmail adapter")
	}

	// Verify gogcli is available
	if _, err := exec.LookPath("gog"); err != nil {
		return nil, fmt.Errorf("gogcli (gog) not found in PATH. Install with: brew install steipete/tap/gogcli")
	}

	return &GmailAdapter{
		name:    name,
		account: account,
		opts:    opts.withDefaults(),
	}, nil
}

func (g *GmailAdapter) Name() string {
	return g.name
}

func (g *GmailAdapter) ensureSyncJobsTable(db *sql.DB) error {
	_, err := db.Exec(`
		CREATE TABLE IF NOT EXISTS sync_jobs (
			adapter TEXT PRIMARY KEY,
			status TEXT NOT NULL,
			phase TEXT NOT NULL,
			cursor TEXT,
			started_at INTEGER,
			updated_at INTEGER NOT NULL,
			last_error TEXT,
			progress_json TEXT
		)
	`)
	if err != nil {
		return fmt.Errorf("failed to ensure sync_jobs table: %w", err)
	}
	return nil
}

func (g *GmailAdapter) updateJobProgress(db *sql.DB, phase string, cursor string, progress map[string]any) {
	// Best-effort; failures shouldn't kill sync.
	if err := g.ensureSyncJobsTable(db); err != nil {
		return
	}
	now := time.Now().Unix()
	var cursorVal any = nil
	if strings.TrimSpace(cursor) != "" {
		cursorVal = cursor
	}
	var progressJSON any = nil
	if progress != nil {
		if b, err := json.Marshal(progress); err == nil {
			progressJSON = string(b)
		}
	}
	_, _ = db.Exec(`
		INSERT INTO sync_jobs (adapter, status, phase, cursor, started_at, updated_at, last_error, progress_json)
		VALUES (?, 'running', ?, ?, NULL, ?, NULL, ?)
		ON CONFLICT(adapter) DO UPDATE SET
			status = 'running',
			phase = excluded.phase,
			cursor = excluded.cursor,
			updated_at = excluded.updated_at,
			last_error = NULL,
			progress_json = excluded.progress_json
	`, g.Name(), phase, cursorVal, now, progressJSON)
}

func (g *GmailAdapter) ensureGmailStateTables(db *sql.DB) error {
	stmts := []string{
		`CREATE TABLE IF NOT EXISTS event_state (
			event_id TEXT PRIMARY KEY REFERENCES events(id) ON DELETE CASCADE,
			read_state TEXT NOT NULL DEFAULT 'unknown',
			flagged INTEGER NOT NULL DEFAULT 0,
			archived INTEGER NOT NULL DEFAULT 0,
			status TEXT NOT NULL DEFAULT 'sent',
			updated_at INTEGER NOT NULL
		)`,
		`CREATE TABLE IF NOT EXISTS event_tags (
			event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
			tag TEXT NOT NULL,
			source TEXT NOT NULL DEFAULT 'system',
			created_at INTEGER NOT NULL,
			PRIMARY KEY (event_id, tag, source)
		)`,
	}
	for _, s := range stmts {
		if _, err := db.Exec(s); err != nil {
			return fmt.Errorf("failed to ensure gmail state tables: %w", err)
		}
	}
	return nil
}

func (g *GmailAdapter) getHistoryID(db *sql.DB) (int64, bool) {
	v, ok, err := state.Get(db, g.Name(), "gmail_history_id")
	if err != nil || !ok {
		return 0, false
	}
	v = strings.TrimSpace(v)
	if v == "" {
		return 0, false
	}
	n, err := strconv.ParseInt(v, 10, 64)
	if err != nil || n <= 0 {
		return 0, false
	}
	return n, true
}

func (g *GmailAdapter) setHistoryID(db *sql.DB, historyID int64) {
	if historyID <= 0 {
		return
	}
	_ = state.Set(db, g.Name(), "gmail_history_id", fmt.Sprintf("%d", historyID))
}

func (g *GmailAdapter) syncGmailStateAndTags(cortexDB *sql.DB, eventID string, labelIDs []string, direction string) error {
	now := time.Now().Unix()

	// Replace current gmail tags for this event.
	_, _ = cortexDB.Exec(`DELETE FROM event_tags WHERE event_id = ? AND source = 'gmail'`, eventID)
	for _, l := range labelIDs {
		l = strings.TrimSpace(l)
		if l == "" {
			continue
		}
		_, _ = cortexDB.Exec(`
			INSERT INTO event_tags (event_id, tag, source, created_at)
			VALUES (?, ?, 'gmail', ?)
			ON CONFLICT(event_id, tag, source) DO NOTHING
		`, eventID, "gmail_label:"+l, now)
	}

	// Derive state.
	readState := "unknown"
	if len(labelIDs) > 0 {
		readState = "read"
		for _, l := range labelIDs {
			if l == "UNREAD" {
				readState = "unread"
				break
			}
		}
	}
	flagged := 0
	archived := 1
	status := "unknown"
	for _, l := range labelIDs {
		switch l {
		case "STARRED", "IMPORTANT":
			flagged = 1
		case "INBOX":
			archived = 0
		case "DRAFT":
			status = "draft"
		}
	}
	if status == "unknown" {
		if direction == "sent" {
			status = "sent"
		} else if direction == "received" {
			status = "received"
		}
	}

	_, err := cortexDB.Exec(`
		INSERT INTO event_state (event_id, read_state, flagged, archived, status, updated_at)
		VALUES (?, ?, ?, ?, ?, ?)
		ON CONFLICT(event_id) DO UPDATE SET
			read_state = excluded.read_state,
			flagged = excluded.flagged,
			archived = excluded.archived,
			status = excluded.status,
			updated_at = excluded.updated_at
	`, eventID, readState, flagged, archived, status, now)
	if err != nil {
		return fmt.Errorf("failed to upsert event_state: %w", err)
	}
	return nil
}

func (g *GmailAdapter) Sync(ctx context.Context, cortexDB *sql.DB, full bool) (SyncResult, error) {
	startTime := time.Now()
	result := SyncResult{Perf: map[string]string{}}

	// Enable foreign keys on cortex DB
	if _, err := cortexDB.Exec("PRAGMA foreign_keys = ON"); err != nil {
		return result, fmt.Errorf("failed to enable foreign keys: %w", err)
	}
	if err := g.ensureGmailStateTables(cortexDB); err != nil {
		return result, err
	}

	// Get sync watermark (last synced date)
	tWM := time.Now()
	var lastSyncTimestamp int64
	var lastEventID sql.NullString
	row := cortexDB.QueryRow("SELECT last_sync_at, last_event_id FROM sync_watermarks WHERE adapter = ?", g.Name())
	if err := row.Scan(&lastSyncTimestamp, &lastEventID); err != nil && err != sql.ErrNoRows {
		return result, fmt.Errorf("failed to get sync watermark: %w", err)
	}
	result.Perf["watermark_read"] = time.Since(tWM).String()

	// A simple-but-reliable strategy:
	// - Full sync: backfill month-by-month from a fixed start (resumable via last_event_id = "backfill:YYYY-MM-01")
	// - Incremental: Gmail search using after:YYYY/MM/DD (day granularity; duplicates are OK via upsert)
	//
	// This avoids the Gmail History API requirement of a "since history ID", which we don't have initially.
	personCache := newEmailPersonCache()

	backfillCursor := ""
	if lastEventID.Valid && strings.HasPrefix(lastEventID.String, "backfill:") {
		backfillCursor = strings.TrimPrefix(lastEventID.String, "backfill:")
	}

	firstRun := lastSyncTimestamp == 0
	if full || backfillCursor != "" || firstRun {
		start := time.Date(2004, 1, 1, 0, 0, 0, 0, time.UTC)
		if backfillCursor != "" {
			// Accept either YYYY-MM-DD or YYYY-MM-01 (preferred).
			if t, err := time.Parse("2006-01-02", backfillCursor); err == nil {
				start = t
			}
		}

		now := time.Now().UTC()
		// Recent-first window (for fast onboarding UX).
		// Use whole-month boundaries to avoid gaps and keep behavior deterministic.
		recentMonth := time.Date(now.Year(), now.Month(), 1, 0, 0, 0, 0, time.UTC).AddDate(0, -3, 0)

		monthStart := time.Date(start.Year(), start.Month(), 1, 0, 0, 0, 0, time.UTC)
		endMonth := recentMonth

		backfillWindows := 0
		backfillTotal := time.Duration(0)
		backfillLastLabel := ""
		backfillLastDur := time.Duration(0)

		// Recent-first: fetch last ~3 months quickly (month boundary avoids gaps).
		recentQuery := fmt.Sprintf("in:anywhere -in:spam -in:trash after:%s", recentMonth.Format("2006/01/02"))
		g.updateJobProgress(cortexDB, "recent", "", map[string]any{
			"recent": map[string]any{
				"after": recentMonth.Format("2006-01-02"),
			},
		})
		eventsCreated, eventsUpdated, personsCreated, maxHist, err := g.syncQuery(ctx, cortexDB, recentQuery, personCache, func(done, total int) {
			g.updateJobProgress(cortexDB, "recent", "", map[string]any{
				"threads": map[string]any{
					"done":  done,
					"total": total,
				},
			})
		})
		if err != nil {
			return result, err
		}
		g.setHistoryID(cortexDB, maxHist)
		result.EventsCreated += eventsCreated
		result.EventsUpdated += eventsUpdated
		result.PersonsCreated += personsCreated

		// Backfill from 2004 up to recentMonth.
		// Compute total windows for ETA and progress reporting.
		windowsTotal := 0
		for t := monthStart; t.Before(endMonth); t = t.AddDate(0, 1, 0) {
			windowsTotal++
		}

		for monthStart.Before(endMonth) {
			monthEnd := monthStart.AddDate(0, 1, 0)
			after := monthStart.Format("2006/01/02")
			before := monthEnd.Format("2006/01/02")
			// "Inbox + archive" (aka everything except spam/trash).
			query := fmt.Sprintf("in:anywhere -in:spam -in:trash after:%s before:%s", after, before)

			fmt.Printf("  Gmail backfill %s → %s\n", after, before)
			tMonth := time.Now()
			monthLabel := monthStart.Format("2006-01")
			nextCursor := monthEnd.Format("2006-01-02")
			g.updateJobProgress(cortexDB, "backfill", "backfill:"+nextCursor, map[string]any{
				"backfill": map[string]any{
					"current_window": monthLabel,
					"windows_done":   backfillWindows,
					"windows_total":  windowsTotal,
				},
			})

			var lastProgressWrite time.Time
			eventsCreated, eventsUpdated, personsCreated, maxHist, err := g.syncQuery(ctx, cortexDB, query, personCache, func(done, total int) {
				// Rate-limit DB writes.
				if time.Since(lastProgressWrite) < 2*time.Second {
					return
				}
				lastProgressWrite = time.Now()
				g.updateJobProgress(cortexDB, "backfill", "backfill:"+nextCursor, map[string]any{
					"backfill": map[string]any{
						"current_window": monthLabel,
						"windows_done":   backfillWindows,
						"windows_total":  windowsTotal,
					},
					"threads": map[string]any{
						"done":  done,
						"total": total,
					},
				})
			})
			if err != nil {
				return result, err
			}
			g.setHistoryID(cortexDB, maxHist)
			dur := time.Since(tMonth)
			backfillWindows++
			backfillTotal += dur
			backfillLastLabel = monthStart.Format("2006-01")
			backfillLastDur = dur
			result.EventsCreated += eventsCreated
			result.EventsUpdated += eventsUpdated
			result.PersonsCreated += personsCreated

			// Persist backfill cursor after each month.
			if err := g.upsertWatermark(cortexDB, time.Now().Unix(), "backfill:"+nextCursor); err != nil {
				return result, err
			}

			// Rough ETA from avg month duration.
			if backfillWindows > 0 {
				avg := time.Duration(int64(backfillTotal) / int64(backfillWindows))
				remaining := windowsTotal - backfillWindows
				eta := avg * time.Duration(remaining)
				if eta > 0 {
					result.Perf["eta_backfill"] = eta.Truncate(time.Minute).String()
				}
				if eta >= 4*time.Hour {
					hint := "Backfill ETA is >4h. For a faster initial bulk snapshot, use Google Takeout (takeout.google.com) and import the MBOX."
					result.Perf["hint_takeout"] = hint
					g.updateJobProgress(cortexDB, "backfill", "backfill:"+nextCursor, map[string]any{
						"eta_seconds":  int64(eta.Seconds()),
						"hint_takeout": hint,
						"backfill": map[string]any{
							"current_window": monthLabel,
							"windows_done":   backfillWindows,
							"windows_total":  windowsTotal,
							"avg_window_sec": int64(avg.Seconds()),
						},
					})
				}
			}

			monthStart = monthEnd
		}

		result.Perf["backfill_windows"] = fmt.Sprintf("%d", backfillWindows)
		result.Perf["backfill_total"] = backfillTotal.String()
		if backfillLastLabel != "" {
			result.Perf["backfill_last"] = fmt.Sprintf("%s (%s)", backfillLastLabel, backfillLastDur.String())
		}

		// Clear backfill cursor; future runs will be incremental.
		nowUnix := time.Now().Unix()
		if err := g.upsertWatermark(cortexDB, nowUnix, ""); err != nil {
			return result, err
		}
	} else {
		// Prefer History API when we have a baseline. This catches up label changes/deletes
		// even if the machine was off, and avoids re-scanning huge time ranges.
		usedHistory := false
		if since, ok := g.getHistoryID(cortexDB); ok {
			tHist := time.Now()
			g.updateJobProgress(cortexDB, "history", fmt.Sprintf("%d", since), map[string]any{
				"history": map[string]any{
					"since": since,
				},
			})
			eventsCreated, eventsUpdated, personsCreated, newHist, err := g.syncHistory(ctx, cortexDB, since, personCache)
			if err == nil {
				usedHistory = true
				g.setHistoryID(cortexDB, newHist)
				result.Perf["incremental_sync_history"] = time.Since(tHist).String()
				result.EventsCreated += eventsCreated
				result.EventsUpdated += eventsUpdated
				result.PersonsCreated += personsCreated
			} else {
				result.Perf["history_fallback"] = err.Error()
			}
		}

		// Fallback: date-based incremental.
		if !usedHistory {
			searchQuery := "in:anywhere -in:spam -in:trash"
			if lastSyncTimestamp > 0 {
				lastSyncDate := time.Unix(lastSyncTimestamp, 0).UTC().Format("2006/01/02")
				searchQuery = fmt.Sprintf("in:anywhere -in:spam -in:trash after:%s", lastSyncDate)
			}
			tInc := time.Now()
			g.updateJobProgress(cortexDB, "incremental", "", map[string]any{
				"incremental": map[string]any{
					"query": searchQuery,
				},
			})
			var lastProgressWrite time.Time
			eventsCreated, eventsUpdated, personsCreated, maxHist, err := g.syncQuery(ctx, cortexDB, searchQuery, personCache, func(done, total int) {
				if time.Since(lastProgressWrite) < 2*time.Second {
					return
				}
				lastProgressWrite = time.Now()
				g.updateJobProgress(cortexDB, "incremental", "", map[string]any{
					"threads": map[string]any{
						"done":  done,
						"total": total,
					},
				})
			})
			if err != nil {
				return result, err
			}
			g.setHistoryID(cortexDB, maxHist)
			result.Perf["incremental_sync_query"] = time.Since(tInc).String()
			result.EventsCreated += eventsCreated
			result.EventsUpdated += eventsUpdated
			result.PersonsCreated += personsCreated
		}

		nowUnix := time.Now().Unix()
		if err := g.upsertWatermark(cortexDB, nowUnix, lastEventID.String); err != nil {
			return result, err
		}
	}

	// Update sync watermark
	result.Duration = time.Since(startTime)
	result.Perf["total"] = result.Duration.String()
	return result, nil
}

func (g *GmailAdapter) upsertWatermark(db *sql.DB, ts int64, lastEventID string) error {
	var last sql.NullString
	if strings.TrimSpace(lastEventID) != "" {
		last = sql.NullString{String: lastEventID, Valid: true}
	}
	_, err := db.Exec(`
		INSERT INTO sync_watermarks (adapter, last_sync_at, last_event_id)
		VALUES (?, ?, ?)
		ON CONFLICT(adapter) DO UPDATE SET
			last_sync_at = excluded.last_sync_at,
			last_event_id = excluded.last_event_id
	`, g.Name(), ts, last)
	if err != nil {
		return fmt.Errorf("failed to update sync watermark: %w", err)
	}
	return nil
}

// GmailThread represents a Gmail thread from gogcli
type GmailThread struct {
	ID        string         `json:"id"`
	HistoryID string         `json:"historyId"`
	Snippet   string         `json:"snippet"`
	Messages  []GmailMessage `json:"messages"`
}

// GmailMessage represents a single message in a thread
type GmailMessage struct {
	ID           string       `json:"id"`
	ThreadID     string       `json:"threadId"`
	LabelIDs     []string     `json:"labelIds"`
	Snippet      string       `json:"snippet"`
	InternalDate string       `json:"internalDate"` // Unix timestamp in milliseconds as string
	HistoryID    string       `json:"historyId"`
	Payload      GmailPayload `json:"payload"`
	SizeEstimate int          `json:"sizeEstimate"`
}

// GmailPayload contains the message headers and body
type GmailPayload struct {
	PartID   string         `json:"partId"`
	MimeType string         `json:"mimeType"`
	Filename string         `json:"filename"`
	Headers  []GmailHeader  `json:"headers"`
	Body     GmailBody      `json:"body"`
	Parts    []GmailPayload `json:"parts"`
}

// GmailHeader represents an email header
type GmailHeader struct {
	Name  string `json:"name"`
	Value string `json:"value"`
}

// GmailBody contains the message body
type GmailBody struct {
	Size int    `json:"size"`
	Data string `json:"data"`
}

// gogcliSearchResponse wraps the response from gog gmail search (minimal thread info)
type gogcliSearchResponse struct {
	NextPageToken string `json:"nextPageToken"`
	Threads       []struct {
		ID string `json:"id"`
	} `json:"threads"`
}

// gogcliThreadResponse wraps the response from gog gmail thread get (full thread with messages)
type gogcliThreadResponse struct {
	Thread GmailThread `json:"thread"`
}

type gogcliMessageResponse struct {
	Message GmailMessage `json:"message"`
}

type gogcliHistoryResponse struct {
	HistoryID     string   `json:"historyId"`
	Messages      []string `json:"messages"`
	NextPageToken string   `json:"nextPageToken"`
}

// fetchThreadIDs executes gogcli to fetch Gmail thread IDs with pagination.
func (g *GmailAdapter) fetchThreadIDs(ctx context.Context, query string) ([]string, error) {
	var allThreadIDs []string
	pageToken := ""
	pageCount := 0
	maxPages := g.opts.MaxPages // Safety limit to prevent infinite loops

	// Step 1: Paginate through search results to get all thread IDs
	for pageCount < maxPages {
		args := []string{"gmail", "search", query, "--json", "--max", "500", "--account", g.account}
		if pageToken != "" {
			args = append(args, "--page", pageToken)
		}

		cmd := exec.CommandContext(ctx, "gog", args...)
		output, err := cmd.CombinedOutput()
		if err != nil {
			// Check for rate limit - if so, wait and retry
			if strings.Contains(string(output), "rateLimitExceeded") {
				fmt.Printf("  Rate limited on search, waiting 10s...\n")
				time.Sleep(10 * time.Second)
				continue // Retry same page
			}
			return nil, fmt.Errorf("gogcli search failed: %w (output: %s)", err, string(output))
		}

		var searchResp gogcliSearchResponse
		if err := json.Unmarshal(output, &searchResp); err != nil {
			return nil, fmt.Errorf("failed to parse search JSON: %w", err)
		}

		for _, t := range searchResp.Threads {
			allThreadIDs = append(allThreadIDs, t.ID)
		}

		fmt.Printf("  Fetched page %d: %d threads (total so far: %d)\n", pageCount+1, len(searchResp.Threads), len(allThreadIDs))

		// Check if there are more pages
		if searchResp.NextPageToken == "" || len(searchResp.Threads) == 0 {
			break
		}
		pageToken = searchResp.NextPageToken
		pageCount++

		// Delay between pages to avoid user-rate-limit (keep it conservative).
		time.Sleep(g.opts.SearchPageDelay)
	}

	fmt.Printf("  Total thread IDs found: %d\n", len(allThreadIDs))
	return allThreadIDs, nil
}

// fetchThread fetches a single thread with full messages
func (g *GmailAdapter) fetchThread(ctx context.Context, threadID string) (GmailThread, error) {
	cmd := exec.CommandContext(ctx, "gog", "gmail", "thread", "get", threadID, "--json", "--account", g.account)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return GmailThread{}, fmt.Errorf("gogcli thread get failed: %w (output: %s)", err, string(output))
	}

	var resp gogcliThreadResponse
	if err := json.Unmarshal(output, &resp); err != nil {
		return GmailThread{}, fmt.Errorf("failed to parse thread JSON: %w", err)
	}

	return resp.Thread, nil
}

func isGmailRateLimited(err error) bool {
	if err == nil {
		return false
	}
	// gogcli tends to surface Gmail API errors as strings.
	s := err.Error()
	return strings.Contains(s, "rateLimitExceeded") || strings.Contains(s, "userRateLimitExceeded")
}

func (g *GmailAdapter) fetchThreadWithRetry(ctx context.Context, threadID string) (GmailThread, error) {
	backoff := 500 * time.Millisecond
	for attempt := 0; attempt <= g.opts.MaxThreadRetries; attempt++ {
		if attempt > 0 {
			select {
			case <-ctx.Done():
				return GmailThread{}, ctx.Err()
			case <-time.After(backoff):
			}
			// Exponential backoff, capped.
			backoff *= 2
			if backoff > 30*time.Second {
				backoff = 30 * time.Second
			}
		}

		thread, err := g.fetchThread(ctx, threadID)
		if err == nil {
			return thread, nil
		}
		if isGmailRateLimited(err) {
			// Retry with backoff.
			continue
		}
		return GmailThread{}, err
	}
	return GmailThread{}, fmt.Errorf("thread fetch retries exceeded for %s", threadID)
}

func (g *GmailAdapter) fetchMessage(ctx context.Context, messageID string) (GmailMessage, error) {
	cmd := exec.CommandContext(ctx, "gog", "gmail", "get", messageID, "--json", "--account", g.account)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return GmailMessage{}, fmt.Errorf("gogcli message get failed: %w (output: %s)", err, string(output))
	}

	var resp gogcliMessageResponse
	if err := json.Unmarshal(output, &resp); err != nil {
		return GmailMessage{}, fmt.Errorf("failed to parse message JSON: %w", err)
	}

	return resp.Message, nil
}

func (g *GmailAdapter) fetchMessageWithRetry(ctx context.Context, messageID string) (GmailMessage, error) {
	backoff := 500 * time.Millisecond
	for attempt := 0; attempt <= g.opts.MaxThreadRetries; attempt++ {
		if attempt > 0 {
			select {
			case <-ctx.Done():
				return GmailMessage{}, ctx.Err()
			case <-time.After(backoff):
			}
			// Exponential backoff, capped.
			backoff *= 2
			if backoff > 30*time.Second {
				backoff = 30 * time.Second
			}
		}

		msg, err := g.fetchMessage(ctx, messageID)
		if err == nil {
			return msg, nil
		}
		if isGmailRateLimited(err) {
			continue
		}
		return GmailMessage{}, err
	}
	return GmailMessage{}, fmt.Errorf("message fetch retries exceeded for %s", messageID)
}

// syncQuery searches threads for query, fetches each thread, and upserts all messages.
func (g *GmailAdapter) syncQuery(ctx context.Context, cortexDB *sql.DB, query string, cache *emailPersonCache, onProgress func(done, total int)) (int, int, int, int64, error) {
	start := time.Now()
	tSearch := time.Now()
	threadIDs, err := g.fetchThreadIDs(ctx, query)
	if err != nil {
		return 0, 0, 0, 0, err
	}
	searchDur := time.Since(tSearch)
	if onProgress != nil {
		onProgress(0, len(threadIDs))
	}

	// Bound external-process parallelism + API QPS.
	workers := g.opts.Workers
	interval := time.Duration(float64(time.Second) / g.opts.QPS)
	if interval < 10*time.Millisecond {
		interval = 10 * time.Millisecond
	}
	reqTicker := time.NewTicker(interval)
	defer reqTicker.Stop()

	type threadResult struct {
		created int
		updated int
		persons int
		maxHist int64
		err     error
	}

	jobs := make(chan string)
	results := make(chan threadResult)
	var wg sync.WaitGroup

	for w := 0; w < workers; w++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for threadID := range jobs {
				select {
				case <-ctx.Done():
					results <- threadResult{err: ctx.Err()}
					continue
				case <-reqTicker.C:
					// proceed
				}

				thread, err := g.fetchThreadWithRetry(ctx, threadID)
				if err != nil {
					// Don't kill the whole run; log and continue.
					fmt.Printf("Warning: failed to fetch thread %s: %v\n", threadID, err)
					results <- threadResult{}
					continue
				}

				created, updated, persons, maxHist, err := g.syncThread(ctx, cortexDB, thread, cache)
				if err != nil {
					fmt.Printf("Warning: failed to sync thread %s: %v\n", threadID, err)
					results <- threadResult{}
					continue
				}
				results <- threadResult{created: created, updated: updated, persons: persons, maxHist: maxHist}
			}
		}()
	}

	go func() {
		for _, id := range threadIDs {
			jobs <- id
		}
		close(jobs)
		wg.Wait()
		close(results)
	}()

	eventsCreated := 0
	eventsUpdated := 0
	personsCreated := 0
	maxHistory := int64(0)
	seen := 0
	tSync := time.Now()
	for r := range results {
		if r.err != nil {
			return eventsCreated, eventsUpdated, personsCreated, maxHistory, r.err
		}
		eventsCreated += r.created
		eventsUpdated += r.updated
		personsCreated += r.persons
		if r.maxHist > maxHistory {
			maxHistory = r.maxHist
		}
		seen++
		if onProgress != nil && (seen%50 == 0 || seen == len(threadIDs)) {
			onProgress(seen, len(threadIDs))
		}
		if seen%200 == 0 {
			fmt.Printf("  Synced %d/%d threads (%s)\n", seen, len(threadIDs), time.Since(start).Truncate(time.Second))
		}
	}
	syncDur := time.Since(tSync)

	totalThreads := len(threadIDs)
	totalEvents := eventsCreated + eventsUpdated
	if totalThreads > 0 {
		fmt.Printf("  Gmail query perf: search=%s sync=%s threads=%d events=%d\n", searchDur.Truncate(time.Millisecond), syncDur.Truncate(time.Millisecond), totalThreads, totalEvents)
	}

	return eventsCreated, eventsUpdated, personsCreated, maxHistory, nil
}

// syncThread syncs a single Gmail thread into the cortex database
func (g *GmailAdapter) syncThread(ctx context.Context, cortexDB *sql.DB, thread GmailThread, cache *emailPersonCache) (int, int, int, int64, error) {
	eventsCreated := 0
	eventsUpdated := 0
	personsCreated := 0
	maxHistory := int64(0)

	if h, err := strconv.ParseInt(strings.TrimSpace(thread.HistoryID), 10, 64); err == nil && h > maxHistory {
		maxHistory = h
	}

	for _, message := range thread.Messages {
		if h, err := strconv.ParseInt(strings.TrimSpace(message.HistoryID), 10, 64); err == nil && h > maxHistory {
			maxHistory = h
		}
		// Parse message timestamp (internalDate is Unix timestamp in milliseconds)
		var timestamp int64
		if _, err := fmt.Sscanf(message.InternalDate, "%d", &timestamp); err == nil {
			timestamp = timestamp / 1000 // Convert milliseconds to seconds
		} else {
			timestamp = time.Now().Unix()
		}

		// Extract headers
		headers := make(map[string]string)
		for _, h := range message.Payload.Headers {
			headers[strings.ToLower(h.Name)] = h.Value
		}

		from := headers["from"]
		to := headers["to"]
		cc := headers["cc"]
		subject := decodeMIMEHeader(headers["subject"])

		// Extract body content
		body := decodeGmailBody(g.extractBody(message.Payload))
		content := subject
		if body != "" {
			content = fmt.Sprintf("Subject: %s\n\n%s", subject, body)
		}

		// Build content types
		contentTypes := []string{"text"}
		if g.hasAttachments(message.Payload) {
			contentTypes = append(contentTypes, "attachment")
		}
		contentTypesJSON, _ := json.Marshal(contentTypes)

		// Determine direction based on SENT label
		direction := "received"
		for _, label := range message.LabelIDs {
			if label == "SENT" {
				direction = "sent"
				break
			}
		}

		// Upsert event with deterministic ID (no UUID churn).
		eventID := fmt.Sprintf("%s:%s", g.Name(), message.ID)
		created, updated, err := g.upsertEvent(cortexDB, eventID, timestamp, string(contentTypesJSON), content, direction, thread.ID, message.ID)
		if err != nil {
			return eventsCreated, eventsUpdated, personsCreated, maxHistory, err
		}
		if created {
			eventsCreated++
		} else if updated {
			eventsUpdated++
		}

		// Process participants
		participantsCreated, err := g.syncParticipants(cortexDB, eventID, from, to, cc, direction, cache)
		if err != nil {
			return eventsCreated, eventsUpdated, personsCreated, maxHistory, fmt.Errorf("failed to sync participants: %w", err)
		}
		personsCreated += participantsCreated

		if err := g.syncGmailStateAndTags(cortexDB, eventID, message.LabelIDs, direction); err != nil {
			return eventsCreated, eventsUpdated, personsCreated, maxHistory, err
		}
	}

	return eventsCreated, eventsUpdated, personsCreated, maxHistory, nil
}

func (g *GmailAdapter) syncHistory(ctx context.Context, cortexDB *sql.DB, since int64, cache *emailPersonCache) (int, int, int, int64, error) {
	start := time.Now()
	pageToken := ""
	newHistory := since

	// Bound external-process parallelism + API QPS for message fetch.
	workers := g.opts.Workers
	interval := time.Duration(float64(time.Second) / g.opts.QPS)
	if interval < 10*time.Millisecond {
		interval = 10 * time.Millisecond
	}
	reqTicker := time.NewTicker(interval)
	defer reqTicker.Stop()

	eventsCreated := 0
	eventsUpdated := 0
	personsCreated := 0

	for {
		args := []string{"gmail", "history", "--since", fmt.Sprintf("%d", since), "--max", "500", "--json", "--account", g.account}
		if pageToken != "" {
			args = append(args, "--page", pageToken)
		}

		cmd := exec.CommandContext(ctx, "gog", args...)
		output, err := cmd.CombinedOutput()
		if err != nil {
			return eventsCreated, eventsUpdated, personsCreated, newHistory, fmt.Errorf("gogcli history failed: %w (output: %s)", err, string(output))
		}

		var resp gogcliHistoryResponse
		if err := json.Unmarshal(output, &resp); err != nil {
			return eventsCreated, eventsUpdated, personsCreated, newHistory, fmt.Errorf("failed to parse history JSON: %w", err)
		}
		if h, err := strconv.ParseInt(strings.TrimSpace(resp.HistoryID), 10, 64); err == nil && h > newHistory {
			newHistory = h
		}

		msgIDs := resp.Messages
		if len(msgIDs) > 0 {
			type msgResult struct {
				created int
				updated int
				persons int
			}
			jobs := make(chan string)
			results := make(chan msgResult)
			var wg sync.WaitGroup

			for w := 0; w < workers; w++ {
				wg.Add(1)
				go func() {
					defer wg.Done()
					for mid := range jobs {
						select {
						case <-ctx.Done():
							return
						case <-reqTicker.C:
						}
						msg, err := g.fetchMessageWithRetry(ctx, mid)
						if err != nil {
							fmt.Printf("Warning: failed to fetch message %s: %v\n", mid, err)
							continue
						}
						created, updated, persons, err := g.syncMessage(ctx, cortexDB, msg, cache)
						if err != nil {
							fmt.Printf("Warning: failed to sync message %s: %v\n", mid, err)
							continue
						}
						results <- msgResult{created: created, updated: updated, persons: persons}
					}
				}()
			}

			go func() {
				for _, id := range msgIDs {
					jobs <- id
				}
				close(jobs)
				wg.Wait()
				close(results)
			}()

			for r := range results {
				eventsCreated += r.created
				eventsUpdated += r.updated
				personsCreated += r.persons
			}
		}

		if resp.NextPageToken == "" {
			break
		}
		pageToken = resp.NextPageToken
	}

	fmt.Printf("  Gmail history perf: since=%d new=%d duration=%s\n", since, newHistory, time.Since(start).Truncate(time.Millisecond))
	return eventsCreated, eventsUpdated, personsCreated, newHistory, nil
}

func (g *GmailAdapter) syncMessage(ctx context.Context, cortexDB *sql.DB, message GmailMessage, cache *emailPersonCache) (int, int, int, error) {
	eventsCreated := 0
	eventsUpdated := 0
	personsCreated := 0

	// Parse message timestamp (internalDate is Unix timestamp in milliseconds)
	var timestamp int64
	if _, err := fmt.Sscanf(message.InternalDate, "%d", &timestamp); err == nil {
		timestamp = timestamp / 1000 // Convert milliseconds to seconds
	} else {
		timestamp = time.Now().Unix()
	}

	// Extract headers
	headers := make(map[string]string)
	for _, h := range message.Payload.Headers {
		headers[strings.ToLower(h.Name)] = h.Value
	}

	from := headers["from"]
	to := headers["to"]
	cc := headers["cc"]
	subject := decodeMIMEHeader(headers["subject"])

	// Extract body content
	body := decodeGmailBody(g.extractBody(message.Payload))
	content := subject
	if body != "" {
		content = fmt.Sprintf("Subject: %s\n\n%s", subject, body)
	}

	// Build content types
	contentTypes := []string{"text"}
	if g.hasAttachments(message.Payload) {
		contentTypes = append(contentTypes, "attachment")
	}
	contentTypesJSON, _ := json.Marshal(contentTypes)

	// Determine direction based on SENT label
	direction := "received"
	for _, label := range message.LabelIDs {
		if label == "SENT" {
			direction = "sent"
			break
		}
	}

	threadID := message.ThreadID
	if threadID == "" {
		threadID = message.ID
	}

	eventID := fmt.Sprintf("%s:%s", g.Name(), message.ID)
	created, updated, err := g.upsertEvent(cortexDB, eventID, timestamp, string(contentTypesJSON), content, direction, threadID, message.ID)
	if err != nil {
		return eventsCreated, eventsUpdated, personsCreated, err
	}
	if created {
		eventsCreated++
	} else if updated {
		eventsUpdated++
	}

	participantsCreated, err := g.syncParticipants(cortexDB, eventID, from, to, cc, direction, cache)
	if err != nil {
		return eventsCreated, eventsUpdated, personsCreated, fmt.Errorf("failed to sync participants: %w", err)
	}
	personsCreated += participantsCreated

	if err := g.syncGmailStateAndTags(cortexDB, eventID, message.LabelIDs, direction); err != nil {
		return eventsCreated, eventsUpdated, personsCreated, err
	}

	return eventsCreated, eventsUpdated, personsCreated, nil
}

func (g *GmailAdapter) upsertEvent(cortexDB *sql.DB, eventID string, timestamp int64, contentTypesJSON string, content string, direction string, threadID string, sourceID string) (created bool, updated bool, err error) {
	// Try insert first.
	res, err := cortexDB.Exec(`
		INSERT OR IGNORE INTO events (
			id, timestamp, channel, content_types, content,
			direction, thread_id, reply_to, source_adapter, source_id
		) VALUES (?, ?, 'gmail', ?, ?, ?, ?, '', ?, ?)
	`, eventID, timestamp, contentTypesJSON, content, direction, threadID, g.Name(), sourceID)
	if err != nil {
		return false, false, fmt.Errorf("failed to insert event: %w", err)
	}
	if n, _ := res.RowsAffected(); n > 0 {
		_ = bus.Emit(cortexDB, "cortex.event.created", g.Name(), eventID, map[string]any{
			"channel":        "gmail",
			"direction":      direction,
			"timestamp":      timestamp,
			"thread_id":      threadID,
			"source_id":      sourceID,
			"source_adapter": g.Name(),
		})
		return true, false, nil
	}

	// Already exists: update selectively.
	res, err = cortexDB.Exec(`
		UPDATE events
		SET
			timestamp = ?,
			content_types = ?,
			content = ?,
			direction = ?,
			thread_id = ?
		WHERE source_adapter = ? AND source_id = ?
	`, timestamp, contentTypesJSON, content, direction, threadID, g.Name(), sourceID)
	if err != nil {
		return false, false, fmt.Errorf("failed to update event: %w", err)
	}
	if n, _ := res.RowsAffected(); n > 0 {
		_ = bus.Emit(cortexDB, "cortex.event.updated", g.Name(), eventID, map[string]any{
			"channel":        "gmail",
			"direction":      direction,
			"timestamp":      timestamp,
			"thread_id":      threadID,
			"source_id":      sourceID,
			"source_adapter": g.Name(),
		})
		return false, true, nil
	}
	return false, false, nil
}

// extractBody extracts the text body from Gmail message payload
func (g *GmailAdapter) extractBody(payload GmailPayload) string {
	// Try to get body from main payload
	if payload.Body.Size > 0 && payload.Body.Data != "" {
		return payload.Body.Data
	}

	// Check parts for text/plain or text/html
	for _, part := range payload.Parts {
		if strings.HasPrefix(part.MimeType, "text/") && part.Body.Size > 0 {
			return part.Body.Data
		}
		// Recursively check nested parts
		if len(part.Parts) > 0 {
			body := g.extractBody(part)
			if body != "" {
				return body
			}
		}
	}

	return ""
}

// hasAttachments checks if the message has attachments
func (g *GmailAdapter) hasAttachments(payload GmailPayload) bool {
	if payload.Filename != "" {
		return true
	}
	for _, part := range payload.Parts {
		if part.Filename != "" || g.hasAttachments(part) {
			return true
		}
	}
	return false
}

// syncParticipants creates persons and identities for email participants
func (g *GmailAdapter) syncParticipants(cortexDB *sql.DB, eventID, from, to, cc, direction string, cache *emailPersonCache) (int, error) {
	personsCreated := 0

	// Parse and add sender
	if from != "" {
		fromEmails := parseEmailAddresses(from)
		for _, email := range fromEmails {
			personID, created, err := g.getOrCreatePersonByEmail(cortexDB, email, cache)
			if err != nil {
				return personsCreated, err
			}
			if created {
				personsCreated++
			}

			// Add as sender
			role := "sender"
			_, err = cortexDB.Exec(`
				INSERT INTO event_participants (event_id, person_id, role)
				VALUES (?, ?, ?)
				ON CONFLICT(event_id, person_id, role) DO NOTHING
			`, eventID, personID, role)
			if err != nil {
				return personsCreated, fmt.Errorf("failed to insert sender participant: %w", err)
			}
		}
	}

	// Parse and add recipients
	if to != "" {
		toEmails := parseEmailAddresses(to)
		for _, email := range toEmails {
			personID, created, err := g.getOrCreatePersonByEmail(cortexDB, email, cache)
			if err != nil {
				return personsCreated, err
			}
			if created {
				personsCreated++
			}

			// Add as recipient
			_, err = cortexDB.Exec(`
				INSERT INTO event_participants (event_id, person_id, role)
				VALUES (?, ?, ?)
				ON CONFLICT(event_id, person_id, role) DO NOTHING
			`, eventID, personID, "recipient")
			if err != nil {
				return personsCreated, fmt.Errorf("failed to insert recipient participant: %w", err)
			}
		}
	}

	// Parse and add CC recipients
	if cc != "" {
		ccEmails := parseEmailAddresses(cc)
		for _, email := range ccEmails {
			personID, created, err := g.getOrCreatePersonByEmail(cortexDB, email, cache)
			if err != nil {
				return personsCreated, err
			}
			if created {
				personsCreated++
			}

			// Add as CC
			_, err = cortexDB.Exec(`
				INSERT INTO event_participants (event_id, person_id, role)
				VALUES (?, ?, ?)
				ON CONFLICT(event_id, person_id, role) DO NOTHING
			`, eventID, personID, "cc")
			if err != nil {
				return personsCreated, fmt.Errorf("failed to insert CC participant: %w", err)
			}
		}
	}

	return personsCreated, nil
}

// getOrCreatePersonByEmail finds or creates a person by email address
func (g *GmailAdapter) getOrCreatePersonByEmail(cortexDB *sql.DB, email string, cache *emailPersonCache) (string, bool, error) {
	email = strings.TrimSpace(strings.ToLower(email))
	if email == "" {
		return "", false, fmt.Errorf("empty email address")
	}

	if cache != nil {
		if personID, ok := cache.get(email); ok {
			return personID, false, nil
		}
	}

	// Try to find existing person by email identity
	var personID string
	row := cortexDB.QueryRow(`
		SELECT person_id FROM identities
		WHERE channel = 'email' AND identifier = ?
	`, email)
	if err := row.Scan(&personID); err == nil {
		if cache != nil {
			cache.set(email, personID)
		}
		return personID, false, nil
	} else if err != sql.ErrNoRows {
		return "", false, fmt.Errorf("failed to query identity: %w", err)
	}

	// Person doesn't exist, create new one
	personID = uuid.New().String()
	now := time.Now().Unix()

	// Use email as canonical name (user can update later with display name)
	_, err := cortexDB.Exec(`
		INSERT INTO persons (id, canonical_name, is_me, created_at, updated_at)
		VALUES (?, ?, 0, ?, ?)
	`, personID, email, now, now)
	if err != nil {
		return "", false, fmt.Errorf("failed to insert person: %w", err)
	}

	// Create identity
	identityID := uuid.New().String()
	_, err = cortexDB.Exec(`
		INSERT INTO identities (id, person_id, channel, identifier, created_at)
		VALUES (?, ?, ?, ?, ?)
		ON CONFLICT(channel, identifier) DO NOTHING
	`, identityID, personID, "email", email, now)
	if err != nil {
		return "", false, fmt.Errorf("failed to insert identity: %w", err)
	}

	if cache != nil {
		cache.set(email, personID)
	}
	return personID, true, nil
}

// parseEmailAddresses parses a comma-separated list of email addresses
// Handles formats like: "Name <email@example.com>, email2@example.com"
func parseEmailAddresses(s string) []string {
	s = strings.TrimSpace(s)
	if s == "" {
		return nil
	}

	// Try robust parsing first.
	if addrs, err := mail.ParseAddressList(s); err == nil && len(addrs) > 0 {
		emails := make([]string, 0, len(addrs))
		for _, a := range addrs {
			if a == nil {
				continue
			}
			if e := strings.TrimSpace(strings.ToLower(a.Address)); e != "" {
				emails = append(emails, e)
			}
		}
		if len(emails) > 0 {
			return emails
		}
	}

	// Fallback: naive split.
	var emails []string
	parts := strings.Split(s, ",")
	for _, part := range parts {
		part = strings.TrimSpace(part)
		if part == "" {
			continue
		}
		if idx := strings.Index(part, "<"); idx >= 0 {
			endIdx := strings.Index(part[idx:], ">")
			if endIdx > 0 {
				email := strings.TrimSpace(part[idx+1 : idx+endIdx])
				if email != "" {
					emails = append(emails, strings.ToLower(email))
				}
				continue
			}
		}
		emails = append(emails, strings.ToLower(part))
	}
	return emails
}

func decodeMIMEHeader(s string) string {
	s = strings.TrimSpace(s)
	if s == "" {
		return ""
	}
	if decoded, err := (&mime.WordDecoder{}).DecodeHeader(s); err == nil {
		return decoded
	}
	return s
}

func decodeGmailBody(s string) string {
	s = strings.TrimSpace(s)
	if s == "" {
		return ""
	}
	// Gmail API returns base64url (often without padding).
	b, err := base64.RawURLEncoding.DecodeString(s)
	if err != nil {
		// Some payloads are already plain-ish; return as-is if decode fails.
		return s
	}
	return string(b)
}

type emailPersonCache struct {
	mu      sync.RWMutex
	byEmail map[string]string
}

func newEmailPersonCache() *emailPersonCache {
	return &emailPersonCache{byEmail: make(map[string]string, 1024)}
}

func (c *emailPersonCache) get(email string) (string, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	id, ok := c.byEmail[email]
	return id, ok
}

func (c *emailPersonCache) set(email, personID string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.byEmail[email] = personID
}
