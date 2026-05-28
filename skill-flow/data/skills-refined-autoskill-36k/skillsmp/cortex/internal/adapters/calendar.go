package adapters

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"os/exec"
	"strings"
	"time"

	"github.com/Napageneral/cortex/internal/bus"
	"github.com/Napageneral/cortex/internal/state"
	"github.com/google/uuid"
)

// CalendarAdapter syncs Google Calendar events via gogcli.
type CalendarAdapter struct {
	name    string
	account string
}

func NewCalendarAdapter(name, account string) (*CalendarAdapter, error) {
	if strings.TrimSpace(name) == "" {
		return nil, fmt.Errorf("adapter instance name is required for calendar adapter")
	}
	if strings.TrimSpace(account) == "" {
		return nil, fmt.Errorf("account email is required for calendar adapter")
	}
	if _, err := exec.LookPath("gog"); err != nil {
		return nil, fmt.Errorf("gogcli (gog) not found in PATH. Install with: brew install steipete/tap/gogcli")
	}
	return &CalendarAdapter{name: name, account: account}, nil
}

func (c *CalendarAdapter) Name() string { return c.name }

type gogCalendarsResponse struct {
	Calendars     []gogCalendar `json:"calendars"`
	NextPageToken string        `json:"nextPageToken"`
}

type gogCalendar struct {
	ID      string `json:"id"`
	Summary string `json:"summary"`
	Primary bool   `json:"primary"`
}

type gogEventsResponse struct {
	Events        []gogCalendarEvent `json:"events"`
	NextPageToken string             `json:"nextPageToken"`
}

type gogCalendarEvent struct {
	ID          string `json:"id"`
	Status      string `json:"status"` // confirmed|cancelled|tentative
	Summary     string `json:"summary"`
	Description string `json:"description"`
	Location    string `json:"location"`
	HTMLLink    string `json:"htmlLink"`
	Created     string `json:"created"`
	Updated     string `json:"updated"`

	Start gogEventTime `json:"start"`
	End   gogEventTime `json:"end"`

	Organizer *gogEventPerson  `json:"organizer"`
	Attendees []gogEventPerson `json:"attendees"`
}

type gogEventTime struct {
	Date     string `json:"date"`     // all-day
	DateTime string `json:"dateTime"` // RFC3339
	TimeZone string `json:"timeZone"`
}

type gogEventPerson struct {
	Email       string `json:"email"`
	DisplayName string `json:"displayName"`
	Self        bool   `json:"self"`
	Response    string `json:"responseStatus"`
}

func (c *CalendarAdapter) ensureCalendarTables(db *sql.DB) error {
	// Defensive for existing DBs.
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
			return fmt.Errorf("failed to ensure calendar tables: %w", err)
		}
	}
	return nil
}

func (c *CalendarAdapter) fetchCalendars(ctx context.Context) ([]gogCalendar, error) {
	pageToken := ""
	var out []gogCalendar
	for {
		args := []string{"calendar", "calendars", "--json", "--max", "100", "--account", c.account}
		if pageToken != "" {
			args = append(args, "--page", pageToken)
		}
		cmd := exec.CommandContext(ctx, "gog", args...)
		b, err := cmd.CombinedOutput()
		if err != nil {
			return nil, fmt.Errorf("gog calendar calendars failed: %w (output: %s)", err, string(b))
		}
		var resp gogCalendarsResponse
		if err := json.Unmarshal(b, &resp); err != nil {
			return nil, fmt.Errorf("failed to parse calendars json: %w", err)
		}
		out = append(out, resp.Calendars...)
		if resp.NextPageToken == "" || len(resp.Calendars) == 0 {
			break
		}
		pageToken = resp.NextPageToken
	}
	return out, nil
}

func (c *CalendarAdapter) fetchEvents(ctx context.Context, calendarID string, from, to time.Time) ([]gogCalendarEvent, error) {
	pageToken := ""
	var out []gogCalendarEvent
	for {
		args := []string{
			"calendar", "events", calendarID,
			"--json",
			"--from", from.Format(time.RFC3339),
			"--to", to.Format(time.RFC3339),
			"--max", "250",
			"--account", c.account,
		}
		if pageToken != "" {
			args = append(args, "--page", pageToken)
		}
		cmd := exec.CommandContext(ctx, "gog", args...)
		b, err := cmd.CombinedOutput()
		if err != nil {
			return nil, fmt.Errorf("gog calendar events failed (cal=%s): %w (output: %s)", calendarID, err, string(b))
		}
		var resp gogEventsResponse
		if err := json.Unmarshal(b, &resp); err != nil {
			return nil, fmt.Errorf("failed to parse events json: %w", err)
		}
		out = append(out, resp.Events...)
		if resp.NextPageToken == "" || len(resp.Events) == 0 {
			break
		}
		pageToken = resp.NextPageToken
	}
	return out, nil
}

func parseEventStartUTC(e gogCalendarEvent) (int64, error) {
	if e.Start.DateTime != "" {
		t, err := time.Parse(time.RFC3339, e.Start.DateTime)
		if err != nil {
			return 0, err
		}
		return t.UTC().Unix(), nil
	}
	if e.Start.Date != "" {
		// All-day: interpret as midnight UTC.
		t, err := time.Parse("2006-01-02", e.Start.Date)
		if err != nil {
			return 0, err
		}
		return t.UTC().Unix(), nil
	}
	return 0, fmt.Errorf("missing start time")
}

func (c *CalendarAdapter) getOrCreatePersonByEmail(db *sql.DB, email string, cache map[string]string) (string, bool, error) {
	email = strings.TrimSpace(strings.ToLower(email))
	if email == "" {
		return "", false, fmt.Errorf("empty email")
	}
	if id, ok := cache[email]; ok {
		return id, false, nil
	}

	var personID string
	err := db.QueryRow(`
		SELECT person_id FROM identities
		WHERE channel = 'email' AND identifier = ?
	`, email).Scan(&personID)
	if err == nil {
		cache[email] = personID
		return personID, false, nil
	}
	if err != sql.ErrNoRows {
		return "", false, err
	}

	personID = uuid.New().String()
	now := time.Now().Unix()
	_, err = db.Exec(`
		INSERT INTO persons (id, canonical_name, is_me, created_at, updated_at)
		VALUES (?, ?, 0, ?, ?)
	`, personID, email, now, now)
	if err != nil {
		return "", false, err
	}
	identityID := uuid.New().String()
	_, err = db.Exec(`
		INSERT INTO identities (id, person_id, channel, identifier, created_at)
		VALUES (?, ?, 'email', ?, ?)
		ON CONFLICT(channel, identifier) DO NOTHING
	`, identityID, personID, email, now)
	if err != nil {
		return "", false, err
	}

	cache[email] = personID
	return personID, true, nil
}

func (c *CalendarAdapter) upsertEvent(db *sql.DB, eventID string, ts int64, content string, threadID string, sourceID string) (created bool, updated bool, err error) {
	contentTypes := `["calendar_event"]`
	direction := "observed"

	res, err := db.Exec(`
		INSERT OR IGNORE INTO events (
			id, timestamp, channel, content_types, content,
			direction, thread_id, reply_to, source_adapter, source_id
		) VALUES (?, ?, 'calendar', ?, ?, ?, ?, '', ?, ?)
	`, eventID, ts, contentTypes, content, direction, threadID, c.Name(), sourceID)
	if err != nil {
		return false, false, err
	}
	if n, _ := res.RowsAffected(); n > 0 {
		_ = bus.Emit(db, "cortex.event.created", c.Name(), eventID, map[string]any{
			"channel":        "calendar",
			"direction":      direction,
			"timestamp":      ts,
			"thread_id":      threadID,
			"source_id":      sourceID,
			"source_adapter": c.Name(),
		})
		return true, false, nil
	}

	res, err = db.Exec(`
		UPDATE events
		SET
			timestamp = ?,
			content = ?,
			thread_id = ?
		WHERE source_adapter = ? AND source_id = ?
	`, ts, content, threadID, c.Name(), sourceID)
	if err != nil {
		return false, false, err
	}
	if n, _ := res.RowsAffected(); n > 0 {
		_ = bus.Emit(db, "cortex.event.updated", c.Name(), eventID, map[string]any{
			"channel":        "calendar",
			"direction":      direction,
			"timestamp":      ts,
			"thread_id":      threadID,
			"source_id":      sourceID,
			"source_adapter": c.Name(),
		})
		return false, true, nil
	}
	return false, false, nil
}

func (c *CalendarAdapter) upsertStateAndTags(db *sql.DB, eventID string, calendarID string, ev gogCalendarEvent) error {
	now := time.Now().Unix()
	_, _ = db.Exec(`DELETE FROM event_tags WHERE event_id = ? AND source = 'calendar'`, eventID)
	_, _ = db.Exec(`
		INSERT INTO event_tags (event_id, tag, source, created_at)
		VALUES (?, ?, 'calendar', ?)
		ON CONFLICT(event_id, tag, source) DO NOTHING
	`, eventID, "calendar_id:"+calendarID, now)

	status := "unknown"
	switch strings.ToLower(strings.TrimSpace(ev.Status)) {
	case "confirmed":
		status = "confirmed"
	case "cancelled":
		status = "cancelled"
	}
	_, err := db.Exec(`
		INSERT INTO event_state (event_id, read_state, flagged, archived, status, updated_at)
		VALUES (?, 'unknown', 0, 0, ?, ?)
		ON CONFLICT(event_id) DO UPDATE SET
			status = excluded.status,
			updated_at = excluded.updated_at
	`, eventID, status, now)
	return err
}

func (c *CalendarAdapter) getCursor(db *sql.DB) (string, bool) {
	v, ok, err := state.Get(db, c.Name(), "calendar_backfill_cursor")
	if err != nil || !ok || strings.TrimSpace(v) == "" {
		return "", false
	}
	return strings.TrimSpace(v), true
}

func (c *CalendarAdapter) setCursor(db *sql.DB, v string) {
	_ = state.Set(db, c.Name(), "calendar_backfill_cursor", v)
}

func (c *CalendarAdapter) Sync(ctx context.Context, cortexDB *sql.DB, full bool) (SyncResult, error) {
	start := time.Now()
	res := SyncResult{Perf: map[string]string{}}

	if _, err := cortexDB.Exec("PRAGMA foreign_keys = ON"); err != nil {
		return res, err
	}
	if err := c.ensureCalendarTables(cortexDB); err != nil {
		return res, err
	}

	calendars, err := c.fetchCalendars(ctx)
	if err != nil {
		return res, err
	}
	if len(calendars) == 0 {
		res.Duration = time.Since(start)
		return res, nil
	}

	// Backfill strategy:
	// - Full sync: month windows from 2004 -> now+1y, cursor stored in adapter_state.
	// - Incremental: last 30d -> now+1y.
	cursor, hasCursor := c.getCursor(cortexDB)
	firstRun := !hasCursor

	if full || firstRun || hasCursor {
		// Cursor is YYYY-MM-01.
		begin := time.Date(2004, 1, 1, 0, 0, 0, 0, time.UTC)
		if hasCursor {
			if t, err := time.Parse("2006-01-02", cursor); err == nil {
				begin = t
			}
		}
		monthStart := time.Date(begin.Year(), begin.Month(), 1, 0, 0, 0, 0, time.UTC)
		end := time.Date(time.Now().UTC().Year(), time.Now().UTC().Month(), 1, 0, 0, 0, 0, time.UTC).AddDate(1, 0, 0)

		cache := map[string]string{}
		windows := 0
		for monthStart.Before(end) {
			monthEnd := monthStart.AddDate(0, 1, 0)
			windows++
			res.Perf["calendar_backfill_window"] = monthStart.Format("2006-01")

			for _, cal := range calendars {
				events, err := c.fetchEvents(ctx, cal.ID, monthStart, monthEnd)
				if err != nil {
					return res, err
				}
				for _, ev := range events {
					if strings.TrimSpace(ev.ID) == "" {
						continue
					}
					ts, err := parseEventStartUTC(ev)
					if err != nil {
						continue
					}

					sourceID := fmt.Sprintf("%s:%s", cal.ID, ev.ID)
					eventID := fmt.Sprintf("%s:%s", c.Name(), sourceID)
					threadID := "calendar:" + cal.ID

					content := fmt.Sprintf("Summary: %s\nCalendar: %s\nStatus: %s\nLink: %s\nLocation: %s\n\n%s",
						ev.Summary, cal.Summary, ev.Status, ev.HTMLLink, ev.Location, ev.Description)

					created, updated, err := c.upsertEvent(cortexDB, eventID, ts, content, threadID, sourceID)
					if err != nil {
						return res, err
					}
					if created {
						res.EventsCreated++
					} else if updated {
						res.EventsUpdated++
					}

					// Participants: organizer + attendees
					if ev.Organizer != nil && ev.Organizer.Email != "" {
						pid, created, err := c.getOrCreatePersonByEmail(cortexDB, ev.Organizer.Email, cache)
						if err == nil {
							if created {
								res.PersonsCreated++
							}
							_, _ = cortexDB.Exec(`INSERT OR IGNORE INTO event_participants (event_id, person_id, role) VALUES (?, ?, 'organizer')`, eventID, pid)
						}
					}
					for _, a := range ev.Attendees {
						if a.Email == "" {
							continue
						}
						pid, created, err := c.getOrCreatePersonByEmail(cortexDB, a.Email, cache)
						if err == nil {
							if created {
								res.PersonsCreated++
							}
							_, _ = cortexDB.Exec(`INSERT OR IGNORE INTO event_participants (event_id, person_id, role) VALUES (?, ?, 'attendee')`, eventID, pid)
						}
					}

					_ = c.upsertStateAndTags(cortexDB, eventID, cal.ID, ev)
				}
			}

			// Persist cursor
			c.setCursor(cortexDB, monthEnd.Format("2006-01-02"))
			monthStart = monthEnd
		}

		res.Perf["calendar_backfill_windows"] = fmt.Sprintf("%d", windows)
		// Mark backfill complete (empty cursor disables future full loops).
		c.setCursor(cortexDB, "")
	} else {
		// Incremental poll: past 30d to 1y ahead.
		from := time.Now().UTC().AddDate(0, 0, -30)
		to := time.Now().UTC().AddDate(1, 0, 0)
		cache := map[string]string{}

		for _, cal := range calendars {
			events, err := c.fetchEvents(ctx, cal.ID, from, to)
			if err != nil {
				return res, err
			}
			for _, ev := range events {
				ts, err := parseEventStartUTC(ev)
				if err != nil {
					continue
				}
				sourceID := fmt.Sprintf("%s:%s", cal.ID, ev.ID)
				eventID := fmt.Sprintf("%s:%s", c.Name(), sourceID)
				threadID := "calendar:" + cal.ID
				content := fmt.Sprintf("Summary: %s\nCalendar: %s\nStatus: %s\nLink: %s\nLocation: %s\n\n%s",
					ev.Summary, cal.Summary, ev.Status, ev.HTMLLink, ev.Location, ev.Description)

				created, updated, err := c.upsertEvent(cortexDB, eventID, ts, content, threadID, sourceID)
				if err != nil {
					return res, err
				}
				if created {
					res.EventsCreated++
				} else if updated {
					res.EventsUpdated++
				}
				if ev.Organizer != nil && ev.Organizer.Email != "" {
					pid, created, err := c.getOrCreatePersonByEmail(cortexDB, ev.Organizer.Email, cache)
					if err == nil {
						if created {
							res.PersonsCreated++
						}
						_, _ = cortexDB.Exec(`INSERT OR IGNORE INTO event_participants (event_id, person_id, role) VALUES (?, ?, 'organizer')`, eventID, pid)
					}
				}
				for _, a := range ev.Attendees {
					if a.Email == "" {
						continue
					}
					pid, created, err := c.getOrCreatePersonByEmail(cortexDB, a.Email, cache)
					if err == nil {
						if created {
							res.PersonsCreated++
						}
						_, _ = cortexDB.Exec(`INSERT OR IGNORE INTO event_participants (event_id, person_id, role) VALUES (?, ?, 'attendee')`, eventID, pid)
					}
				}
				_ = c.upsertStateAndTags(cortexDB, eventID, cal.ID, ev)
			}
		}
	}

	res.Duration = time.Since(start)
	res.Perf["total"] = res.Duration.String()
	return res, nil
}
