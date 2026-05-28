package live

import (
	"context"
	"database/sql"
	"fmt"
	"io"
	"net/http"
	"path/filepath"
	"strings"
	stdsync "sync"
	"time"

	"github.com/Napageneral/cortex/internal/config"
	"github.com/Napageneral/cortex/internal/sync"
)

func NewGmailWatcher(db *sql.DB, cfg *config.Config, adapterNames []string, opts map[string]any, heartbeatInterval time.Duration, logf func(format string, args ...any)) WatcherSpec {
	if logf == nil {
		logf = func(string, ...any) {}
	}
	bind := getStringOption(opts, "bind", "127.0.0.1")
	port := getIntOption(opts, "port", 8799)
	path := getStringOption(opts, "path", "/hook/gmail")
	token := getStringOption(opts, "token", "")
	debounceSec := getIntOption(opts, "debounce_seconds", 10)
	adapterOnly := getStringOption(opts, "adapter", "")
	manageUpstream := getBoolOption(opts, "ensure_upstream", true)
	upstreamCmd := getStringOption(opts, "upstream_cmd", "gog")
	upstreamBind := getStringOption(opts, "upstream_bind", "127.0.0.1")
	upstreamPort := getIntOption(opts, "upstream_port", 8788)
	upstreamPath := getStringOption(opts, "upstream_path", "/gmail-pubsub")
	upstreamToken := getStringOption(opts, "upstream_token", "")
	upstreamPIDFile := getStringOption(opts, "upstream_pid_file", "")
	upstreamCheckSec := getIntOption(opts, "upstream_check_seconds", 30)

	return WatcherSpec{
		Name:     "gmail",
		Adapters: adapterNames,
		Run: func(ctx context.Context, beat func()) error {
			if cfg == nil {
				return fmt.Errorf("config is required")
			}
			type adapterRunState struct {
				running bool
				lastAt  time.Time
			}
			var mu stdsync.Mutex
			stateByAdapter := map[string]*adapterRunState{}

			selectAdapters := func() []string {
				if adapterOnly != "" {
					return []string{adapterOnly}
				}
				out := make([]string, 0, len(adapterNames))
				for _, name := range adapterNames {
					out = append(out, name)
				}
				return out
			}

			runAdapter := func(adapterName string) {
				mu.Lock()
				st, ok := stateByAdapter[adapterName]
				if !ok {
					st = &adapterRunState{}
					stateByAdapter[adapterName] = st
				}
				if st.running {
					mu.Unlock()
					return
				}
				if debounceSec > 0 && !st.lastAt.IsZero() && time.Since(st.lastAt) < time.Duration(debounceSec)*time.Second {
					mu.Unlock()
					return
				}
				st.running = true
				st.lastAt = time.Now()
				mu.Unlock()

				go func() {
					defer func() {
						mu.Lock()
						st.running = false
						mu.Unlock()
					}()
					if ctx.Err() != nil {
						return
					}
					beat()
					res := sync.SyncOne(ctx, db, cfg, adapterName, false)
					if !res.OK {
						logf("watch sync error (%s): %s", adapterName, res.Message)
					} else {
						logf("watch sync OK (%s)", adapterName)
					}
				}()
			}

			mux := http.NewServeMux()
			mux.HandleFunc(path, func(w http.ResponseWriter, r *http.Request) {
				if r.Method != http.MethodPost && r.Method != http.MethodPut {
					w.WriteHeader(http.StatusMethodNotAllowed)
					return
				}
				if token != "" {
					ok := false
					auth := r.Header.Get("Authorization")
					if strings.HasPrefix(strings.ToLower(auth), "bearer ") && strings.TrimSpace(auth[7:]) == token {
						ok = true
					}
					if r.URL.Query().Get("token") == token {
						ok = true
					}
					if !ok {
						w.WriteHeader(http.StatusUnauthorized)
						return
					}
				}

				_, _ = io.ReadAll(io.LimitReader(r.Body, 256*1024))
				_ = r.Body.Close()

				for _, a := range selectAdapters() {
					runAdapter(a)
				}

				w.WriteHeader(http.StatusOK)
				_, _ = w.Write([]byte("ok\n"))
			})

			addr := fmt.Sprintf("%s:%d", bind, port)
			logf("Listening on http://%s%s", addr, path)
			logf("To connect gogcli watch forwarding:")
			logf("  gog gmail watch serve --bind %s --port 8788 --path /gmail-pubsub --hook-url http://%s%s", bind, addr, path)
			if token != "" {
				logf("  (token configured)")
			}

			if manageUpstream {
				setGmailErr := func(err error) {
					for _, name := range adapterNames {
						setLiveError(db, name, err)
					}
				}
				if upstreamPIDFile == "" {
					if dataDir, err := config.GetDataDir(); err == nil {
						upstreamPIDFile = filepath.Join(dataDir, "gog-watch.pid")
					}
				}
				hookURL := fmt.Sprintf("http://%s:%d%s", bind, port, path)
				args := []string{
					"gmail", "watch", "serve",
					"--bind", upstreamBind,
					"--port", fmt.Sprintf("%d", upstreamPort),
					"--path", upstreamPath,
					"--hook-url", hookURL,
				}
				if upstreamToken != "" {
					args = append(args, "--hook-token", upstreamToken)
				} else if token != "" {
					args = append(args, "--hook-token", token)
				}
				ensureUpstream(ctx, UpstreamSpec{
					Name:                  "gog-watch",
					Command:               upstreamCmd,
					Args:                  args,
					PIDFile:               upstreamPIDFile,
					ExternalCheckInterval: time.Duration(upstreamCheckSec) * time.Second,
				}, logf, setGmailErr)
			}

			stopHeartbeat := startHeartbeat(heartbeatInterval, beat)
			defer stopHeartbeat()

			srv := &http.Server{Addr: addr, Handler: mux}
			go func() {
				<-ctx.Done()
				_ = srv.Shutdown(context.Background())
			}()

			if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
				return err
			}
			return nil
		},
	}
}
