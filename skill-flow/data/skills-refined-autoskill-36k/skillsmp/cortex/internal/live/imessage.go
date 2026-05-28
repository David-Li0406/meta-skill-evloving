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

func NewIMessageWatcher(db *sql.DB, adapterName string, opts map[string]any, heartbeatInterval time.Duration, logf func(format string, args ...any)) WatcherSpec {
	if logf == nil {
		logf = func(string, ...any) {}
	}
	debounceSec := getIntOption(opts, "debounce_seconds", 2)
	chatDBPath := getStringOption(opts, "chat_db", "")
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
			adapter, err := adapters.NewIMessageAdapter()
			if err != nil {
				return fmt.Errorf("create imessage adapter: %w", err)
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

			if chatDBPath == "" {
				chatDBPath = os.ExpandEnv("$HOME/Library/Messages/chat.db")
				if override := os.Getenv("EVE_SOURCE_CHAT_DB"); override != "" {
					chatDBPath = os.ExpandEnv(override)
				}
			}
			chatDBDir := filepath.Dir(chatDBPath)

			watcher, err := fsnotify.NewWatcher()
			if err != nil {
				return fmt.Errorf("create watcher: %w", err)
			}
			defer watcher.Close()

			if err := watcher.Add(chatDBDir); err != nil {
				return fmt.Errorf("watch %s: %w", chatDBDir, err)
			}

			logf("Watching for iMessage changes in %s (debounce: %ds)", chatDBDir, debounceSec)
			logf("Press Ctrl+C to stop")

			stopHeartbeat := startHeartbeat(heartbeatInterval, beat)
			defer stopHeartbeat()

			debounceDelay := time.Duration(debounceSec) * time.Second
			var debounceTimer *time.Timer

			runSync := func() {
				beat()
				result, err := adapter.Sync(ctx, db, false)
				if err != nil {
					logf("watch sync error (imessage): %v", err)
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
					if strings.Contains(event.Name, "chat.db") {
						triggerSync()
					}
				case err, ok := <-watcher.Errors:
					if !ok {
						return nil
					}
					logf("watch error (imessage): %v", err)
				}
			}
		},
	}
}
