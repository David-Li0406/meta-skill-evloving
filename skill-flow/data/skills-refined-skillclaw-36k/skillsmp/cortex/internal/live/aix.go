package live

import (
	"context"
	"database/sql"
	"fmt"
	"path/filepath"
	"strings"
	"time"

	"github.com/fsnotify/fsnotify"

	"github.com/Napageneral/cortex/internal/adapters"
)

func NewAixWatcher(db *sql.DB, adapterName string, opts map[string]any, heartbeatInterval time.Duration, logf func(format string, args ...any)) WatcherSpec {
	if logf == nil {
		logf = func(string, ...any) {}
	}
	debounceSec := getIntOption(opts, "debounce_seconds", 2)
	extractMetadata := getBoolOption(opts, "extract_metadata", true)
	source := getStringOption(opts, "source", "cursor")
	manageUpstream := getBoolOption(opts, "ensure_upstream", true)
	upstreamCmd := getStringOption(opts, "upstream_cmd", "aix")
	upstreamPollMS := getIntOption(opts, "upstream_poll_ms", 250)
	upstreamDebounceMS := getIntOption(opts, "upstream_debounce_ms", 200)
	upstreamPidFile := getStringOption(opts, "upstream_pid_file", "")
	upstreamCheckSec := getIntOption(opts, "upstream_check_seconds", 30)

	return WatcherSpec{
		Name:     adapterName,
		Adapters: []string{adapterName},
		Run: func(ctx context.Context, beat func()) error {
			adapter, err := adapters.NewAixAdapter(source)
			if err != nil {
				return fmt.Errorf("create aix adapter: %w", err)
			}

			if manageUpstream {
				args := []string{"live", "--source", source, "--poll-ms", fmt.Sprintf("%d", upstreamPollMS), "--debounce-ms", fmt.Sprintf("%d", upstreamDebounceMS)}
				if upstreamPidFile != "" {
					args = append(args, "--pid-file", upstreamPidFile)
				}
				ensureUpstream(ctx, UpstreamSpec{
					Name:                   "aix-live",
					Command:                upstreamCmd,
					Args:                   args,
					PIDFile:                upstreamPidFile,
					AlreadyRunningExitCode: 10,
					ExternalCheckInterval:  time.Duration(upstreamCheckSec) * time.Second,
				}, logf, func(err error) {
					setLiveError(db, adapterName, err)
				})
			}

			aixDBPath, err := adapters.DefaultAixDBPath()
			if err != nil {
				return fmt.Errorf("determine aix.db path: %w", err)
			}
			aixDBDir := filepath.Dir(aixDBPath)

			watcher, err := fsnotify.NewWatcher()
			if err != nil {
				return fmt.Errorf("create watcher: %w", err)
			}
			defer watcher.Close()

			if err := watcher.Add(aixDBDir); err != nil {
				return fmt.Errorf("watch %s: %w", aixDBDir, err)
			}

			logf("Watching for AIX changes in %s (debounce: %ds)", aixDBDir, debounceSec)
			logf("Press Ctrl+C to stop")

			stopHeartbeat := startHeartbeat(heartbeatInterval, beat)
			defer stopHeartbeat()

			getLastSync := func() int64 {
				var lastSync int64
				_ = db.QueryRow(`SELECT last_sync_at FROM sync_watermarks WHERE adapter = ?`, adapter.Name()).Scan(&lastSync)
				return lastSync
			}

			runSync := func() {
				beat()
				lastSync := getLastSync()
				result, err := adapter.Sync(ctx, db, false)
				if err != nil {
					logf("[%s] Sync error: %v", time.Now().Format("15:04:05"), err)
					return
				}
				if result.EventsCreated > 0 || result.EventsUpdated > 0 {
					logf("[%s] Synced %d events (%d new, %d updated)",
						time.Now().Format("15:04:05"),
						result.EventsCreated+result.EventsUpdated,
						result.EventsCreated,
						result.EventsUpdated,
					)
				} else {
					logf("[%s] No new AIX events", time.Now().Format("15:04:05"))
				}

				if extractMetadata {
					extractor := adapters.NewAIXFacetExtractor(db)
					extractResult, err := extractor.ExtractFacetsFromMetadata(ctx, adapter.Name(), lastSync)
					if err != nil {
						logf("[%s] AIX metadata extraction error: %v", time.Now().Format("15:04:05"), err)
						return
					}
					if extractResult.FacetsCreated > 0 {
						logf("[%s] Extracted %d facets (%d episodes)",
							time.Now().Format("15:04:05"),
							extractResult.FacetsCreated,
							extractResult.EpisodesCreated,
						)
					} else {
						logf("[%s] No new AIX metadata facets", time.Now().Format("15:04:05"))
					}
				}
			}

			logf("[%s] Running initial sync...", time.Now().Format("15:04:05"))
			runSync()

			debounceDelay := time.Duration(debounceSec) * time.Second
			var debounceTimer *time.Timer
			triggerSync := func() {
				if debounceTimer != nil {
					debounceTimer.Stop()
				}
				debounceTimer = time.AfterFunc(debounceDelay, runSync)
			}

			for {
				select {
				case <-ctx.Done():
					return nil
				case event, ok := <-watcher.Events:
					if !ok {
						return nil
					}
					if strings.Contains(event.Name, "aix.db") {
						triggerSync()
					}
				case err, ok := <-watcher.Errors:
					if !ok {
						return nil
					}
					logf("[%s] Watch error: %v", time.Now().Format("15:04:05"), err)
				}
			}
		},
	}
}
