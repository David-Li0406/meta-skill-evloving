package live

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"time"

	"github.com/Napageneral/cortex/internal/config"
)

type WatcherSpec struct {
	Name     string
	Adapters []string
	Run      func(ctx context.Context, beat func()) error
}

type Manager struct {
	DB                *sql.DB
	Config            *config.Config
	HeartbeatInterval time.Duration
	RestartBackoff    time.Duration
	Logf              func(format string, args ...any)
}

func NewManager(db *sql.DB, cfg *config.Config) *Manager {
	return &Manager{
		DB:                db,
		Config:            cfg,
		HeartbeatInterval: 10 * time.Second,
		RestartBackoff:    3 * time.Second,
		Logf:              log.Printf,
	}
}

func (m *Manager) Run(ctx context.Context) error {
	specs, err := m.BuildSpecs()
	if err != nil {
		return err
	}
	if len(specs) == 0 {
		return fmt.Errorf("no live watchers enabled")
	}

	for _, spec := range specs {
		spec := spec
		go m.runWatcher(ctx, spec)
	}

	<-ctx.Done()
	return nil
}

func (m *Manager) runWatcher(ctx context.Context, spec WatcherSpec) {
	backoff := m.RestartBackoff
	if backoff <= 0 {
		backoff = 2 * time.Second
	}
	maxBackoff := 30 * time.Second

	for {
		if ctx.Err() != nil {
			for _, adapter := range spec.Adapters {
				setLiveStatus(m.DB, adapter, "stopped")
			}
			return
		}

		for _, adapter := range spec.Adapters {
			setLiveStatus(m.DB, adapter, "running")
			setLiveError(m.DB, adapter, nil)
			setLiveHeartbeat(m.DB, adapter, time.Now())
		}

		beat := func() {
			for _, adapter := range spec.Adapters {
				setLiveHeartbeat(m.DB, adapter, time.Now())
			}
		}

		err := spec.Run(ctx, beat)
		if ctx.Err() != nil {
			for _, adapter := range spec.Adapters {
				setLiveStatus(m.DB, adapter, "stopped")
			}
			return
		}

		for _, adapter := range spec.Adapters {
			setLiveStatus(m.DB, adapter, "error")
			setLiveError(m.DB, adapter, err)
			incrementLiveRestarts(m.DB, adapter)
		}
		if err != nil {
			m.Logf("live watcher %s stopped: %v (restarting in %s)", spec.Name, err, backoff)
		} else {
			m.Logf("live watcher %s stopped (restarting in %s)", spec.Name, backoff)
		}

		select {
		case <-time.After(backoff):
		case <-ctx.Done():
			for _, adapter := range spec.Adapters {
				setLiveStatus(m.DB, adapter, "stopped")
			}
			return
		}

		backoff = backoff * 2
		if backoff > maxBackoff {
			backoff = maxBackoff
		}
	}
}

func (m *Manager) BuildSpecs() ([]WatcherSpec, error) {
	if m.Config == nil {
		return nil, fmt.Errorf("config is required")
	}

	var specs []WatcherSpec
	var gmailAdapters []string
	var gmailOptions map[string]any

	for name, adapterCfg := range m.Config.Adapters {
		if !adapterCfg.Enabled {
			continue
		}
		if adapterCfg.Live == nil || !adapterCfg.Live.Enabled {
			continue
		}

		opts := mergeOptions(adapterCfg.Live.Options, adapterCfg.Options)

		switch adapterCfg.Type {
		case "imessage":
			specs = append(specs, NewIMessageWatcher(m.DB, name, opts, m.HeartbeatInterval, m.Logf))
		case "eve":
			specs = append(specs, NewEveWatcher(m.DB, name, opts, m.HeartbeatInterval, m.Logf))
		case "aix":
			specs = append(specs, NewAixWatcher(m.DB, name, opts, m.HeartbeatInterval, m.Logf))
		case "gogcli":
			gmailAdapters = append(gmailAdapters, name)
			if gmailOptions == nil {
				gmailOptions = opts
			}
		default:
			m.Logf("live not supported for adapter %s (type=%s)", name, adapterCfg.Type)
		}
	}

	if len(gmailAdapters) > 0 {
		specs = append(specs, NewGmailWatcher(m.DB, m.Config, gmailAdapters, gmailOptions, m.HeartbeatInterval, m.Logf))
	}

	return specs, nil
}

func LiveSupported(adapterType string) bool {
	switch adapterType {
	case "imessage", "eve", "aix", "gogcli":
		return true
	default:
		return false
	}
}
