package sync

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	gosync "sync"
	"sync/atomic"

	_ "github.com/mattn/go-sqlite3"
	"github.com/tidwall/gjson"
)

// ParsedSessionStream is sent through a channel for streaming import
type ParsedSessionStream struct {
	Session *ParsedSession
	Error   error
}

// ParseAllStreaming parses sessions and streams them to a channel for parallel import.
// This allows DB import to happen while parsing/export is still running.
// The caller should read from the returned channel until it's closed.
// The waitDone function should be called after draining the channel to wait for all workers.
func (p *CursorDBParser) ParseAllStreaming(exportStats *ExportStats, bubbleExportMode string) (<-chan *ParsedSessionStream, func()) {
	sessionCh := make(chan *ParsedSessionStream, runtime.NumCPU()*4)

	// Check if DB exists
	if _, err := os.Stat(p.dbPath); os.IsNotExist(err) {
		go func() {
			sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("cursor database not found: %s", p.dbPath)}
			close(sessionCh)
		}()
		return sessionCh, func() {}
	}

	// Open read-only
	db, err := sql.Open("sqlite3", p.dbPath+"?mode=ro")
	if err != nil {
		go func() {
			sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("failed to open cursor db: %w", err)}
			close(sessionCh)
		}()
		return sessionCh, func() {}
	}

	// Setup export directories if exporting
	var composerDir, bubblesDir string
	if p.exportPath != "" {
		composerDir = filepath.Join(p.exportPath, "composer")
		bubblesDir = filepath.Join(p.exportPath, "bubbles")
		if err := os.MkdirAll(composerDir, 0755); err != nil {
			go func() {
				sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("failed to create composer export dir: %w", err)}
				close(sessionCh)
			}()
			db.Close()
			return sessionCh, func() {}
		}
		if err := os.MkdirAll(bubblesDir, 0755); err != nil {
			go func() {
				sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("failed to create bubbles export dir: %w", err)}
				close(sessionCh)
			}()
			db.Close()
			return sessionCh, func() {}
		}
	}

	// Capture current max rowid for composerData
	{
		var maxRow sql.NullInt64
		if err := db.QueryRow(`SELECT IFNULL(MAX(rowid), 0) FROM cursorDiskKV WHERE key LIKE 'composerData:%' AND value IS NOT NULL`).Scan(&maxRow); err == nil {
			p.maxComposerID = maxRow.Int64
		}
	}

	// Capture current max rowid for bubbleId
	{
		var maxRow sql.NullInt64
		if err := db.QueryRow(`SELECT IFNULL(MAX(rowid), 0) FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' AND value IS NOT NULL`).Scan(&maxRow); err == nil {
			p.maxBubbleRowID = maxRow.Int64
		}
	}

	// Find sessions with new bubbles (for bubble-aware incremental sync)
	sessionsWithNewBubbles := make(map[string]bool)
	if p.sinceBubbleRowID > 0 {
		rows, err := db.Query(
			`SELECT DISTINCT substr(key, 10, instr(substr(key, 10), ':') - 1) AS session_id
			 FROM cursorDiskKV
			 WHERE key LIKE 'bubbleId:%' AND rowid > ?`,
			p.sinceBubbleRowID,
		)
		if err == nil {
			for rows.Next() {
				var sessionID string
				if rows.Scan(&sessionID) == nil && sessionID != "" {
					sessionsWithNewBubbles[sessionID] = true
				}
			}
			rows.Close()
		}
	}

	var wg gosync.WaitGroup
	var composerCount64, bubbleCount64, composerSkipped64, bubbleSkipped64 int64

	// Use fast path if we have rowid-based incremental
	if p.sinceRowID > 0 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			defer close(sessionCh)
			defer db.Close()

			rows, err := db.Query(
				`SELECT rowid, key, value FROM cursorDiskKV
				 WHERE key LIKE 'composerData:%' AND value IS NOT NULL AND rowid > ?`,
				p.sinceRowID,
			)
			if err != nil {
				sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("failed to query sessions: %w", err)}
				return
			}
			defer rows.Close()

			// Track which sessions we process (to avoid re-processing in bubble path)
			processedSessions := make(map[string]bool)

			for rows.Next() {
				var rowid int64
				var key, value string
				if err := rows.Scan(&rowid, &key, &value); err != nil {
					sessionCh <- &ParsedSessionStream{Error: err}
					continue
				}

				composerID := strings.TrimPrefix(key, "composerData:")
				processedSessions[composerID] = true

				// Export composerData if exporting
				if composerDir != "" {
					exportFile := filepath.Join(composerDir, composerID+".json")
					redactedValue := RedactJSON(value)
					if err := os.WriteFile(exportFile, []byte(redactedValue), 0644); err != nil {
						sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("failed to export %s: %w", key, err)}
					} else {
						atomic.AddInt64(&composerCount64, 1)
					}
				}

				// Fetch bubbles for this session
				bubbleCache := make(map[string]string)
				bubbleRows, err := db.Query(
					`SELECT key, value FROM cursorDiskKV WHERE key LIKE ? AND value IS NOT NULL`,
					fmt.Sprintf("bubbleId:%s:%%", composerID),
				)
				if err == nil {
					for bubbleRows.Next() {
						var bkey, bval string
						if err := bubbleRows.Scan(&bkey, &bval); err != nil {
							continue
						}
						bubbleCache[bkey] = bval
					}
					bubbleRows.Close()
				}

				session, bubbles, err := p.parseSessionWithBubblesFromCache(bubbleCache, key, value)
				if err != nil {
					sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("%s: %w", key, err)}
					continue
				}
				if session == nil {
					continue
				}

				// Export bubbles
				if bubblesDir != "" && len(bubbles) > 0 {
					sessionBubbleDir := filepath.Join(bubblesDir, session.Session.ID)
					if err := os.MkdirAll(sessionBubbleDir, 0755); err != nil {
						sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("failed to create bubble dir for %s: %w", session.Session.ID, err)}
					} else {
						if bubbleExportMode == "jsonl" {
							n, err := exportBubblesJSONL(sessionBubbleDir, bubbles)
							if err != nil {
								sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("failed to export bubbles for %s: %w", session.Session.ID, err)}
							} else {
								atomic.AddInt64(&bubbleCount64, int64(n))
							}
						} else {
							for bubbleID, bubbleJSON := range bubbles {
								bubbleFile := filepath.Join(sessionBubbleDir, bubbleID+".json")
								redactedBubble := RedactJSON(bubbleJSON)
								if err := os.WriteFile(bubbleFile, []byte(redactedBubble), 0644); err != nil {
									// Non-fatal, continue
								} else {
									atomic.AddInt64(&bubbleCount64, 1)
								}
							}
						}
					}
				}

				// Stream the session
				sessionCh <- &ParsedSessionStream{Session: session}
			}

			// Also process sessions with new bubbles (bubble-aware incremental)
			for sessionID := range sessionsWithNewBubbles {
				if processedSessions[sessionID] {
					continue // Already processed above
				}

				// Fetch composerData for this session
				var value string
				err := db.QueryRow(
					`SELECT value FROM cursorDiskKV WHERE key = ? AND value IS NOT NULL`,
					"composerData:"+sessionID,
				).Scan(&value)
				if err != nil {
					continue
				}

				// Fetch bubbles for this session
				bubbleCache := make(map[string]string)
				bubbleRows, err := db.Query(
					`SELECT key, value FROM cursorDiskKV WHERE key LIKE ? AND value IS NOT NULL`,
					fmt.Sprintf("bubbleId:%s:%%", sessionID),
				)
				if err == nil {
					for bubbleRows.Next() {
						var bkey, bval string
						if bubbleRows.Scan(&bkey, &bval) == nil {
							bubbleCache[bkey] = bval
						}
					}
					bubbleRows.Close()
				}

				session, bubbles, err := p.parseSessionWithBubblesFromCache(bubbleCache, "composerData:"+sessionID, value)
				if err != nil || session == nil {
					continue
				}

				// Export bubbles if exporting
				if bubblesDir != "" && len(bubbles) > 0 {
					sessionBubbleDir := filepath.Join(bubblesDir, session.Session.ID)
					if os.MkdirAll(sessionBubbleDir, 0755) == nil {
						if bubbleExportMode == "jsonl" {
							n, _ := exportBubblesJSONL(sessionBubbleDir, bubbles)
							atomic.AddInt64(&bubbleCount64, int64(n))
						} else {
							for bubbleID, bubbleJSON := range bubbles {
								bubbleFile := filepath.Join(sessionBubbleDir, bubbleID+".json")
								redactedBubble := RedactJSON(bubbleJSON)
								if os.WriteFile(bubbleFile, []byte(redactedBubble), 0644) == nil {
									atomic.AddInt64(&bubbleCount64, 1)
								}
							}
						}
					}
				}

				// Stream the session
				sessionCh <- &ParsedSessionStream{Session: session}
			}

			if exportStats != nil {
				exportStats.ComposerFiles = int(atomic.LoadInt64(&composerCount64))
				exportStats.ComposerFilesSkipped = int(atomic.LoadInt64(&composerSkipped64))
				exportStats.BubbleFiles = int(atomic.LoadInt64(&bubbleCount64))
				exportStats.BubbleFilesSkipped = int(atomic.LoadInt64(&bubbleSkipped64))
			}
		}()

		return sessionCh, func() { wg.Wait() }
	}

	// Full sync path with parallel workers
	wg.Add(1)
	go func() {
		defer wg.Done()
		defer close(sessionCh)
		defer db.Close()

		// First pass: identify sessions to process
		type sessionEntry struct {
			key, value string
		}
		var entriesToProcess []sessionEntry
		changedSessionIDs := make(map[string]bool)

		rows1, err := db.Query(`SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%' AND value IS NOT NULL`)
		if err != nil {
			sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("failed to query sessions: %w", err)}
			return
		}
		for rows1.Next() {
			var key, value string
			if err := rows1.Scan(&key, &value); err != nil {
				continue
			}
			composerID := strings.TrimPrefix(key, "composerData:")
			changedSessionIDs[composerID] = true
			entriesToProcess = append(entriesToProcess, sessionEntry{key: key, value: value})
		}
		rows1.Close()

		// Fetch bubbles for all sessions
		bubbleCache := make(map[string]string)
		if len(changedSessionIDs) > 0 {
			bubbleRows, err := db.Query(`SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' AND value IS NOT NULL`)
			if err != nil {
				sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("failed to query bubbles: %w", err)}
				return
			}
			for bubbleRows.Next() {
				var key, value string
				if err := bubbleRows.Scan(&key, &value); err != nil {
					continue
				}
				parts := strings.Split(key, ":")
				if len(parts) >= 2 {
					composerID := parts[1]
					if changedSessionIDs[composerID] {
						bubbleCache[key] = value
					}
				}
			}
			bubbleRows.Close()
		}

		// Worker pool
		workerCount := runtime.NumCPU()
		if workerCount > 8 {
			workerCount = 8
		}

		jobs := make(chan sessionEntry, workerCount*2)
		var workerWg gosync.WaitGroup

		worker := func() {
			defer workerWg.Done()
			for entry := range jobs {
				key := entry.key
				value := entry.value
				composerID := strings.TrimPrefix(key, "composerData:")

				// Check if already exported
				skipExport := false
				if composerDir != "" {
					exportFile := filepath.Join(composerDir, composerID+".json")
					if _, err := os.Stat(exportFile); err == nil {
						skipExport = true
						atomic.AddInt64(&composerSkipped64, 1)
					}
				}

				// Export composerData
				if composerDir != "" && !skipExport {
					exportFile := filepath.Join(composerDir, composerID+".json")
					redactedValue := RedactJSON(value)
					if err := os.WriteFile(exportFile, []byte(redactedValue), 0644); err == nil {
						atomic.AddInt64(&composerCount64, 1)
					}
				}

				session, bubbles, err := p.parseSessionWithBubblesFromCache(bubbleCache, key, value)
				if err != nil {
					sessionCh <- &ParsedSessionStream{Error: fmt.Errorf("%s: %w", key, err)}
					continue
				}
				if session == nil {
					continue
				}

				// Export bubbles
				if bubblesDir != "" && len(bubbles) > 0 && !skipExport {
					sessionBubbleDir := filepath.Join(bubblesDir, session.Session.ID)
					if err := os.MkdirAll(sessionBubbleDir, 0755); err == nil {
						if bubbleExportMode == "jsonl" {
							n, _ := exportBubblesJSONL(sessionBubbleDir, bubbles)
							atomic.AddInt64(&bubbleCount64, int64(n))
						} else {
							for bubbleID, bubbleJSON := range bubbles {
								bubbleFile := filepath.Join(sessionBubbleDir, bubbleID+".json")
								redactedBubble := RedactJSON(bubbleJSON)
								if err := os.WriteFile(bubbleFile, []byte(redactedBubble), 0644); err == nil {
									atomic.AddInt64(&bubbleCount64, 1)
								}
							}
						}
					}
				} else if bubblesDir != "" && skipExport {
					atomic.AddInt64(&bubbleSkipped64, int64(len(bubbles)))
				}

				// Stream the session
				sessionCh <- &ParsedSessionStream{Session: session}
			}
		}

		workerWg.Add(workerCount)
		for i := 0; i < workerCount; i++ {
			go worker()
		}

		for _, entry := range entriesToProcess {
			jobs <- entry
		}
		close(jobs)
		workerWg.Wait()

		if exportStats != nil {
			exportStats.ComposerFiles = int(atomic.LoadInt64(&composerCount64))
			exportStats.ComposerFilesSkipped = int(atomic.LoadInt64(&composerSkipped64))
			exportStats.BubbleFiles = int(atomic.LoadInt64(&bubbleCount64))
			exportStats.BubbleFilesSkipped = int(atomic.LoadInt64(&bubbleSkipped64))
		}
	}()

	return sessionCh, func() { wg.Wait() }
}

// Helper to extract composerID from gjson result
func extractComposerIDFromJSON(value string) string {
	return gjson.Get(value, "composerId").String()
}
