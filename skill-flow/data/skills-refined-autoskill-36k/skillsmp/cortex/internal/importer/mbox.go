package importer

import (
	"bufio"
	"bytes"
	"context"
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"mime"
	"net/mail"
	"os"
	"strings"
	"time"

	"github.com/google/uuid"
)

type MBoxImportOptions struct {
	AdapterName  string
	AccountEmail string
	Path         string
	Source       string // "takeout" etc

	MaxMessageBytes int64 // safety cap per message (body may be truncated)
	CommitEvery     int   // commit per N messages
	LimitMessages   int   // 0 = no limit
	DryRun          bool
}

type MBoxImportResult struct {
	MessagesSeen      int
	EventsCreated     int
	EventsUpdated     int
	PersonsCreated    int
	MessagesTruncated int
	Duration          time.Duration
}

func (o MBoxImportOptions) withDefaults() MBoxImportOptions {
	if o.Source == "" {
		o.Source = "takeout"
	}
	if o.MaxMessageBytes <= 0 {
		o.MaxMessageBytes = 50 * 1024 * 1024
	}
	if o.CommitEvery <= 0 {
		o.CommitEvery = 500
	}
	return o
}

func ensureImportTables(db *sql.DB) error {
	// Defensive: existing installs may not have re-run schema init.
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
			return fmt.Errorf("failed to ensure importer tables: %w", err)
		}
	}
	return nil
}

func ImportMBox(ctx context.Context, db *sql.DB, opts MBoxImportOptions) (MBoxImportResult, error) {
	start := time.Now()
	opts = opts.withDefaults()
	var out MBoxImportResult

	if strings.TrimSpace(opts.AdapterName) == "" {
		return out, fmt.Errorf("AdapterName is required")
	}
	if strings.TrimSpace(opts.AccountEmail) == "" {
		return out, fmt.Errorf("AccountEmail is required")
	}
	if strings.TrimSpace(opts.Path) == "" {
		return out, fmt.Errorf("Path is required")
	}

	if _, err := db.Exec("PRAGMA foreign_keys = ON"); err != nil {
		return out, fmt.Errorf("failed to enable foreign keys: %w", err)
	}
	if err := ensureImportTables(db); err != nil {
		return out, err
	}

	f, err := os.Open(opts.Path)
	if err != nil {
		return out, fmt.Errorf("failed to open mbox: %w", err)
	}
	defer f.Close()

	emailCache := make(map[string]string, 4096)

	type prepared struct {
		tx *sql.Tx

		insEvent    *sql.Stmt
		updEvent    *sql.Stmt
		insPart     *sql.Stmt
		delTags     *sql.Stmt
		insTag      *sql.Stmt
		upsertState *sql.Stmt

		selPersonByEmail *sql.Stmt
		insPerson        *sql.Stmt
		insIdentity      *sql.Stmt
	}

	begin := func() (*prepared, error) {
		if opts.DryRun {
			// We still use a tx for statement prep (but won't commit).
		}
		tx, err := db.BeginTx(ctx, nil)
		if err != nil {
			return nil, err
		}

		p := &prepared{tx: tx}
		if p.insEvent, err = tx.Prepare(`
			INSERT OR IGNORE INTO events (
				id, timestamp, channel, content_types, content,
				direction, thread_id, reply_to, source_adapter, source_id
			) VALUES (?, ?, 'gmail', ?, ?, ?, ?, '', ?, ?)
		`); err != nil {
			return nil, err
		}
		if p.updEvent, err = tx.Prepare(`
			UPDATE events
			SET
				timestamp = ?,
				content_types = ?,
				content = ?,
				direction = ?,
				thread_id = ?
			WHERE source_adapter = ? AND source_id = ?
		`); err != nil {
			return nil, err
		}
		if p.insPart, err = tx.Prepare(`
			INSERT INTO event_participants (event_id, person_id, role)
			VALUES (?, ?, ?)
			ON CONFLICT(event_id, person_id, role) DO NOTHING
		`); err != nil {
			return nil, err
		}
		if p.delTags, err = tx.Prepare(`
			DELETE FROM event_tags
			WHERE event_id = ? AND source = 'gmail'
		`); err != nil {
			return nil, err
		}
		if p.insTag, err = tx.Prepare(`
			INSERT INTO event_tags (event_id, tag, source, created_at)
			VALUES (?, ?, 'gmail', ?)
			ON CONFLICT(event_id, tag, source) DO NOTHING
		`); err != nil {
			return nil, err
		}
		if p.upsertState, err = tx.Prepare(`
			INSERT INTO event_state (event_id, read_state, flagged, archived, status, updated_at)
			VALUES (?, ?, ?, ?, ?, ?)
			ON CONFLICT(event_id) DO UPDATE SET
				read_state = excluded.read_state,
				flagged = excluded.flagged,
				archived = excluded.archived,
				status = excluded.status,
				updated_at = excluded.updated_at
		`); err != nil {
			return nil, err
		}

		if p.selPersonByEmail, err = tx.Prepare(`
			SELECT person_id FROM identities
			WHERE channel = 'email' AND identifier = ?
		`); err != nil {
			return nil, err
		}
		if p.insPerson, err = tx.Prepare(`
			INSERT INTO persons (id, canonical_name, is_me, created_at, updated_at)
			VALUES (?, ?, 0, ?, ?)
		`); err != nil {
			return nil, err
		}
		if p.insIdentity, err = tx.Prepare(`
			INSERT INTO identities (id, person_id, channel, identifier, created_at)
			VALUES (?, ?, 'email', ?, ?)
			ON CONFLICT(channel, identifier) DO NOTHING
		`); err != nil {
			return nil, err
		}

		return p, nil
	}

	commit := func(p *prepared) error {
		if opts.DryRun {
			return p.tx.Rollback()
		}
		return p.tx.Commit()
	}

	p, err := begin()
	if err != nil {
		return out, fmt.Errorf("failed to begin import tx: %w", err)
	}
	defer func() { _ = p.tx.Rollback() }()

	decodeHeader := func(s string) string {
		s = strings.TrimSpace(s)
		if s == "" {
			return ""
		}
		if decoded, err := (&mime.WordDecoder{}).DecodeHeader(s); err == nil {
			return decoded
		}
		return s
	}

	parseAddrList := func(s string) []string {
		s = strings.TrimSpace(s)
		if s == "" {
			return nil
		}
		addrs, err := mail.ParseAddressList(s)
		if err == nil && len(addrs) > 0 {
			out := make([]string, 0, len(addrs))
			for _, a := range addrs {
				if a == nil {
					continue
				}
				if e := strings.TrimSpace(strings.ToLower(a.Address)); e != "" {
					out = append(out, e)
				}
			}
			return out
		}
		// Fallback: split by comma.
		parts := strings.Split(s, ",")
		var out []string
		for _, part := range parts {
			part = strings.TrimSpace(part)
			if part == "" {
				continue
			}
			out = append(out, strings.ToLower(part))
		}
		return out
	}

	labelsFromHeader := func(v string) []string {
		v = strings.TrimSpace(v)
		if v == "" {
			return nil
		}
		// Handle forms like: (\Inbox Important "Some Label")
		v = strings.TrimPrefix(v, "(")
		v = strings.TrimSuffix(v, ")")
		v = strings.ReplaceAll(v, "\"", "")
		v = strings.ReplaceAll(v, "\t", " ")
		v = strings.ReplaceAll(v, "\r", " ")
		v = strings.ReplaceAll(v, "\n", " ")
		parts := strings.FieldsFunc(v, func(r rune) bool {
			return r == ',' || r == ' '
		})
		out := make([]string, 0, len(parts))
		seen := make(map[string]struct{}, len(parts))
		for _, p := range parts {
			p = strings.TrimSpace(p)
			if p == "" {
				continue
			}
			// Gmail system labels sometimes come as \Inbox etc; normalize to INBOX-ish.
			p = strings.TrimPrefix(p, "\\")
			p = strings.TrimSpace(p)
			if p == "" {
				continue
			}
			if _, ok := seen[p]; ok {
				continue
			}
			seen[p] = struct{}{}
			out = append(out, p)
		}
		return out
	}

	hasLabel := func(labels []string, want string) bool {
		want = strings.ToUpper(strings.TrimSpace(want))
		for _, l := range labels {
			if strings.ToUpper(strings.TrimSpace(l)) == want {
				return true
			}
		}
		return false
	}

	getOrCreatePersonByEmail := func(email string) (string, bool, error) {
		email = strings.TrimSpace(strings.ToLower(email))
		if email == "" {
			return "", false, fmt.Errorf("empty email")
		}
		if id, ok := emailCache[email]; ok {
			return id, false, nil
		}
		var personID string
		err := p.selPersonByEmail.QueryRow(email).Scan(&personID)
		if err == nil {
			emailCache[email] = personID
			return personID, false, nil
		}
		if err != sql.ErrNoRows {
			return "", false, err
		}

		personID = uuid.New().String()
		now := time.Now().Unix()
		if _, err := p.insPerson.Exec(personID, email, now, now); err != nil {
			return "", false, err
		}
		identityID := uuid.New().String()
		if _, err := p.insIdentity.Exec(identityID, personID, email, now); err != nil {
			return "", false, err
		}
		emailCache[email] = personID
		return personID, true, nil
	}

	upsertEvent := func(eventID string, ts int64, contentTypesJSON string, content string, direction string, threadID string, sourceID string) (created bool, updated bool, err error) {
		res, err := p.insEvent.Exec(eventID, ts, contentTypesJSON, content, direction, threadID, opts.AdapterName, sourceID)
		if err != nil {
			return false, false, err
		}
		if n, _ := res.RowsAffected(); n > 0 {
			return true, false, nil
		}
		res, err = p.updEvent.Exec(ts, contentTypesJSON, content, direction, threadID, opts.AdapterName, sourceID)
		if err != nil {
			return false, false, err
		}
		if n, _ := res.RowsAffected(); n > 0 {
			return false, true, nil
		}
		return false, false, nil
	}

	// Iterate MBOX messages.
	reader := bufio.NewReader(f)
	var buf bytes.Buffer
	var overLimit bool
	var bufBytes int64

	flush := func() error {
		if buf.Len() == 0 {
			overLimit = false
			bufBytes = 0
			return nil
		}
		out.MessagesSeen++

		wasTruncated := overLimit
		raw := buf.Bytes()
		if wasTruncated {
			out.MessagesTruncated++
		}
		buf.Reset()
		overLimit = false
		bufBytes = 0

		msg, err := mail.ReadMessage(bytes.NewReader(raw))
		if err != nil {
			// Skip unparseable message, but keep going.
			return nil
		}

		h := msg.Header
		subject := decodeHeader(h.Get("Subject"))
		dateHeader := h.Get("Date")
		var ts int64
		if t, err := mail.ParseDate(dateHeader); err == nil {
			ts = t.Unix()
		} else {
			ts = time.Now().Unix()
		}

		from := h.Get("From")
		to := h.Get("To")
		cc := h.Get("Cc")
		bcc := h.Get("Bcc")

		// Read body (may include multipart raw; better than nothing for now).
		// Cap the amount we read to avoid huge attachment blobs blowing memory.
		bodyBytes, _ := io.ReadAll(io.LimitReader(msg.Body, 2*1024*1024))
		body := strings.TrimSpace(string(bodyBytes))
		content := subject
		if body != "" {
			content = fmt.Sprintf("Subject: %s\n\n%s", subject, body)
		}

		labels := []string{}
		for _, k := range []string{"X-GM-LABELS", "X-Gmail-Labels", "X-Google-Labels"} {
			if v := h.Get(k); v != "" {
				labels = append(labels, labelsFromHeader(v)...)
			}
		}
		// Some Takeout exports use a single header key:
		if v := h.Get("X-GM-LABELS"); v != "" {
			labels = append(labels, labelsFromHeader(v)...)
		}

		xMsgID := strings.TrimSpace(h.Get("X-GM-MSGID"))
		if xMsgID == "" {
			xMsgID = strings.TrimSpace(h.Get("X-Gmail-Msgid"))
		}
		xThrID := strings.TrimSpace(h.Get("X-GM-THRID"))
		if xThrID == "" {
			xThrID = strings.TrimSpace(h.Get("X-Gmail-Threadid"))
		}

		messageID := strings.TrimSpace(h.Get("Message-ID"))
		sourceID := xMsgID
		if sourceID == "" {
			sourceID = messageID
		}
		if sourceID == "" {
			sum := sha256.Sum256([]byte(fmt.Sprintf("%d|%s|%s|%s", ts, from, subject, body)))
			sourceID = hex.EncodeToString(sum[:])
		}
		sourceID = strings.Trim(sourceID, "<>")

		threadID := xThrID
		if threadID == "" {
			threadID = sourceID
		}

		direction := "received"
		if hasLabel(labels, "SENT") || strings.Contains(strings.ToLower(from), strings.ToLower(opts.AccountEmail)) {
			direction = "sent"
		}

		// Content types: treat as text; tag if truncated.
		cts := []string{"text"}
		if wasTruncated {
			cts = append(cts, "truncated")
		}
		ctsJSON, _ := json.Marshal(cts)

		eventID := fmt.Sprintf("%s:%s", opts.AdapterName, sourceID)
		created, updated, err := upsertEvent(eventID, ts, string(ctsJSON), content, direction, threadID, sourceID)
		if err != nil {
			return err
		}
		if created {
			out.EventsCreated++
		} else if updated {
			out.EventsUpdated++
		}

		// Participants.
		roleSender := "sender"
		roleRecipient := "recipient"
		if direction == "sent" {
			// Still model as sender/recipient; direction is on event.
		}
		for _, e := range parseAddrList(from) {
			personID, created, err := getOrCreatePersonByEmail(e)
			if err != nil {
				continue
			}
			if created {
				out.PersonsCreated++
			}
			if _, err := p.insPart.Exec(eventID, personID, roleSender); err != nil {
				return err
			}
		}
		for _, e := range parseAddrList(to) {
			personID, created, err := getOrCreatePersonByEmail(e)
			if err != nil {
				continue
			}
			if created {
				out.PersonsCreated++
			}
			if _, err := p.insPart.Exec(eventID, personID, roleRecipient); err != nil {
				return err
			}
		}
		for _, e := range parseAddrList(cc) {
			personID, created, err := getOrCreatePersonByEmail(e)
			if err != nil {
				continue
			}
			if created {
				out.PersonsCreated++
			}
			if _, err := p.insPart.Exec(eventID, personID, "cc"); err != nil {
				return err
			}
		}
		for _, e := range parseAddrList(bcc) {
			personID, created, err := getOrCreatePersonByEmail(e)
			if err != nil {
				continue
			}
			if created {
				out.PersonsCreated++
			}
			if _, err := p.insPart.Exec(eventID, personID, "bcc"); err != nil {
				return err
			}
		}

		// Replace Gmail tags for this event with current label set.
		if _, err := p.delTags.Exec(eventID); err != nil {
			return err
		}
		now := time.Now().Unix()
		for _, l := range labels {
			tag := "gmail_label:" + l
			if _, err := p.insTag.Exec(eventID, tag, now); err != nil {
				return err
			}
		}
		// Add provenance tag.
		if _, err := p.insTag.Exec(eventID, "source:"+opts.Source, now); err != nil {
			return err
		}
		if wasTruncated {
			_, _ = p.insTag.Exec(eventID, "mbox:truncated", now)
		}

		// State derivation (best-effort).
		readState := "unknown"
		if len(labels) > 0 {
			if hasLabel(labels, "UNREAD") {
				readState = "unread"
			} else {
				readState = "read"
			}
		}
		flagged := 0
		if hasLabel(labels, "STARRED") || hasLabel(labels, "IMPORTANT") {
			flagged = 1
		}
		archived := 1
		if hasLabel(labels, "INBOX") {
			archived = 0
		}
		status := "unknown"
		if hasLabel(labels, "DRAFT") {
			status = "draft"
		} else if direction == "sent" {
			status = "sent"
		} else if direction == "received" {
			status = "received"
		}
		if _, err := p.upsertState.Exec(eventID, readState, flagged, archived, status, now); err != nil {
			return err
		}

		// Commit chunk.
		if opts.CommitEvery > 0 && out.MessagesSeen%opts.CommitEvery == 0 {
			if err := commit(p); err != nil {
				return err
			}
			p, err = begin()
			if err != nil {
				return err
			}
		}

		if opts.LimitMessages > 0 && out.MessagesSeen >= opts.LimitMessages {
			return io.EOF
		}
		return nil
	}

	for {
		select {
		case <-ctx.Done():
			return out, ctx.Err()
		default:
		}

		line, err := reader.ReadString('\n')
		if err != nil && err != io.EOF {
			return out, fmt.Errorf("failed reading mbox: %w", err)
		}

		// MBOX separator: line begins with "From " at column 0.
		if strings.HasPrefix(line, "From ") {
			if err := flush(); err != nil {
				if err == io.EOF {
					break
				}
				return out, err
			}
		} else {
			if !overLimit {
				bufBytes += int64(len(line))
				if bufBytes > opts.MaxMessageBytes {
					overLimit = true
					// keep what we have; drop remainder until next separator
				} else {
					buf.WriteString(line)
				}
			}
		}

		if err == io.EOF {
			_ = flush()
			break
		}
	}

	// Final commit.
	if err := commit(p); err != nil {
		return out, err
	}

	out.Duration = time.Since(start)
	return out, nil
}
