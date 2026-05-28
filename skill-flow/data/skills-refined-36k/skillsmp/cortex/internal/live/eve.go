package live

import (
	"context"
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/fsnotify/fsnotify"

	"github.com/Napageneral/cortex/internal/adapters"
)

func NewEveWatcher(db *sql.DB, adapterName string, opts map[string]any, heartbeatInterval time.Duration, logf func(format string, args ...any)) WatcherSpec {
	if logf == nil {
		logf = func(string, ...any) {}
	}
	debounceSec := getIntOption(opts, "debounce_seconds", 2)
	eveDBPath := getStringOption(opts, "eve_db", "")
	manageUpstream := getBoolOption(opts, "ensure_upstream", true)
	upstreamCmd := getStringOption(opts, "upstream_cmd", "eve")
	upstreamPollMS := getIntOption(opts, "upstream_poll_ms", 50)
	upstreamDebounceMS := getIntOption(opts, "upstream_debounce_ms", 50)
	upstreamForward := getBoolOption(opts, "upstream_forward_comms", false)
	upstreamPIDFile := getStringOption(opts, "upstream_pid_file", "")
	upstreamCheckSec := getIntOption(opts, "upstream_check_seconds", 30)

	return WatcherSpec{
		Name:     adapterName,
		Adapters: []string{adapterName},
		Run: func(ctx context.Context, beat func()) error {
			adapter, err := adapters.NewEveAdapter()
			if err != nil {
				return fmt.Errorf("create eve adapter: %w", err)
			}

			if manageUpstream {
				args := []string{"live", "--poll", fmt.Sprintf("%d", upstreamPollMS), "--debounce", fmt.Sprintf("%d", upstreamDebounceMS)}
				if upstreamForward {
					args = append(args, "--forward-comms")
				}
				if upstreamPIDFile != "" {
					args = append(args, "--pid-file", upstreamPIDFile)
				}
				ensureUpstream(ctx, UpstreamSpec{
					Name:    "eve-live",
					Command: upstreamCmd,
					Args:    args,
					PIDFile: upstreamPIDFile,
					AlreadyRunningExitCode: 10,
					ExternalCheckInterval:  time.Duration(upstreamCheckSec) * time.Second,
				}, logf, func(err error) {
					setLiveError(db, adapterName, err)
				})
			}

			if eveDBPath == "" {
				home, err := os.UserHomeDir()
				if err != nil {
					return fmt.Errorf("failed to get home dir: %w", err)
				}
				eveDBPath = filepath.Join(home, "Library", "Application Support", "Eve", "eve.db")
			}
			eveDBDir := filepath.Dir(eveDBPath)

			watcher, err := fsnotify.NewWatcher()
			if err != nil {
				return fmt.Errorf("create watcher: %w", err)
			}
			defer watcher.Close()

			if err := watcher.Add(eveDBDir); err != nil {
				return fmt.Errorf("watch %s: %w", eveDBDir, err)
			}

			logf("Watching for Eve changes in %s (debounce: %ds)", eveDBDir, debounceSec)
			logf("Press Ctrl+C to stop")

			stopHeartbeat := startHeartbeat(heartbeatInterval, beat)
			defer stopHeartbeat()

			debounceDelay := time.Duration(debounceSec) * time.Second
			var debounceTimer *time.Timer

			runSync := func() {
				beat()
				result, err := adapter.Sync(ctx, db, false)
				if err != nil {
					logf("watch sync error (eve): %v", err)
					return
				}
				totalNew := result.EventsCreated + result.ReactionsCreated
				if totalNew > 0 {
					logf("[%s] Synced %d new events (%d messages, %d reactions, %d attachments)",
						time.Now().Format("15:04:05"),
						totalNew,
						result.EventsCreated,
						result.ReactionsCreated,
						result.AttachmentsCreated,
					)
				}
			}

			logf("[%s] Running initial sync...", time.Now().Format("15:04:05"))
			runSync()

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
					if strings.Contains(event.Name, "eve.db") {
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
