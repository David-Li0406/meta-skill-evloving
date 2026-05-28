package sync

import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	"time"

	"github.com/Napageneral/cortex/internal/adapters"
	"github.com/Napageneral/cortex/internal/config"
)

// AdapterResult contains the result of syncing a single adapter
type AdapterResult struct {
	AdapterName        string            `json:"adapter_name"`
	Success            bool              `json:"success"`
	Error              string            `json:"error,omitempty"`
	EventsCreated      int               `json:"events_created"`
	EventsUpdated      int               `json:"events_updated"`
	PersonsCreated     int               `json:"persons_created"`
	ThreadsCreated     int               `json:"threads_created"`
	ThreadsUpdated     int               `json:"threads_updated"`
	AttachmentsCreated int               `json:"attachments_created"`
	AttachmentsUpdated int               `json:"attachments_updated"`
	ReactionsCreated   int               `json:"reactions_created"`
	ReactionsUpdated   int               `json:"reactions_updated"`
	Duration           string            `json:"duration"`
	Perf               map[string]string `json:"perf,omitempty"`
}

// SyncResult contains the results of syncing all adapters
type SyncResult struct {
	OK       bool            `json:"ok"`
	Message  string          `json:"message,omitempty"`
	Adapters []AdapterResult `json:"adapters,omitempty"`
}

// SyncAll runs all enabled adapters
func SyncAll(ctx context.Context, db *sql.DB, cfg *config.Config, full bool) SyncResult {
	result := SyncResult{OK: true}

	if len(cfg.Adapters) == 0 {
		result.Message = "No adapters configured"
		return result
	}

	enabledCount := 0
	for _, adapter := range cfg.Adapters {
		if adapter.Enabled {
			enabledCount++
		}
	}

	if enabledCount == 0 {
		result.Message = "No adapters enabled"
		return result
	}

	// Sync each enabled adapter
	for name, adapterCfg := range cfg.Adapters {
		if !adapterCfg.Enabled {
			continue
		}

		adapterResult := syncAdapter(ctx, db, name, adapterCfg, full)
		result.Adapters = append(result.Adapters, adapterResult)

		if !adapterResult.Success {
			// One adapter failing doesn't stop others, but overall sync is not OK
			result.OK = false
		}
	}

	return result
}

// SyncOne runs a specific adapter by name
func SyncOne(ctx context.Context, db *sql.DB, cfg *config.Config, adapterName string, full bool) SyncResult {
	result := SyncResult{OK: true}

	adapterCfg, exists := cfg.Adapters[adapterName]
	if !exists {
		result.OK = false
		result.Message = fmt.Sprintf("Adapter '%s' not configured", adapterName)
		return result
	}

	if !adapterCfg.Enabled {
		result.OK = false
		result.Message = fmt.Sprintf("Adapter '%s' is disabled", adapterName)
		return result
	}

	adapterResult := syncAdapter(ctx, db, adapterName, adapterCfg, full)
	result.Adapters = []AdapterResult{adapterResult}

	if !adapterResult.Success {
		result.OK = false
	}

	return result
}

// syncAdapter syncs a single adapter and returns its result
func syncAdapter(ctx context.Context, db *sql.DB, name string, cfg config.AdapterConfig, full bool) AdapterResult {
	result := AdapterResult{
		AdapterName: name,
		Success:     false,
	}

	_ = StartJob(db, name)

	// Create adapter instance based on type
	var adapter adapters.Adapter
	var err error

	switch cfg.Type {
	case "eve":
		// Eve DB adapter (reads from ~/Library/Application Support/Eve/eve.db).
		// This is useful for full rebuilds when Eve has already materialized a clean dataset.
		adapter, err = adapters.NewEveAdapter()
		if err != nil {
			result.Error = fmt.Sprintf("Failed to create adapter: %v", err)
			return result
		}

	case "imessage":
		// Direct iMessage adapter (reads chat.db directly via Eve library).
		adapter, err = adapters.NewIMessageAdapter()
		if err != nil {
			result.Error = fmt.Sprintf("Failed to create adapter: %v", err)
			return result
		}

	case "gogcli":
		// Gmail adapter via gogcli
		accountVal, ok := cfg.Options["account"]
		if !ok {
			result.Error = "Gmail adapter requires 'account' in config"
			return result
		}
		account, ok := accountVal.(string)
		if !ok || account == "" {
			result.Error = "Gmail adapter 'account' must be a string"
			return result
		}
		// Standardize instance name across installs: gmail-<account email>
		instanceName := fmt.Sprintf("gmail-%s", strings.TrimSpace(strings.ToLower(account)))
		var opts adapters.GmailAdapterOptions
		if v, ok := cfg.Options["workers"]; ok {
			if n, ok := v.(int); ok {
				opts.Workers = n
			}
		}
		if v, ok := cfg.Options["qps"]; ok {
			switch t := v.(type) {
			case float64:
				opts.QPS = t
			case int:
				opts.QPS = float64(t)
			}
		}
		adapter, err = adapters.NewGmailAdapter(instanceName, account, opts)
		if err != nil {
			result.Error = fmt.Sprintf("Failed to create adapter: %v", err)
			return result
		}

	case "gogcli_calendar":
		accountVal, ok := cfg.Options["account"]
		if !ok {
			result.Error = "Calendar adapter requires 'account' in config"
			return result
		}
		account, ok := accountVal.(string)
		if !ok || account == "" {
			result.Error = "Calendar adapter 'account' must be a string"
			return result
		}
		instanceName := fmt.Sprintf("calendar-%s", strings.TrimSpace(strings.ToLower(account)))
		adapter, err = adapters.NewCalendarAdapter(instanceName, account)
		if err != nil {
			result.Error = fmt.Sprintf("Failed to create adapter: %v", err)
			return result
		}

	case "gogcli_contacts":
		accountVal, ok := cfg.Options["account"]
		if !ok {
			result.Error = "Contacts adapter requires 'account' in config"
			return result
		}
		account, ok := accountVal.(string)
		if !ok || account == "" {
			result.Error = "Contacts adapter 'account' must be a string"
			return result
		}
		instanceName := fmt.Sprintf("contacts-%s", strings.TrimSpace(strings.ToLower(account)))
		var opts adapters.ContactsAdapterOptions
		if v, ok := cfg.Options["workers"]; ok {
			if n, ok := v.(int); ok {
				opts.Workers = n
			}
		}
		if v, ok := cfg.Options["qps"]; ok {
			switch t := v.(type) {
			case float64:
				opts.QPS = t
			case int:
				opts.QPS = float64(t)
			}
		}
		adapter, err = adapters.NewContactsAdapter(instanceName, account, opts)
		if err != nil {
			result.Error = fmt.Sprintf("Failed to create adapter: %v", err)
			return result
		}

	case "aix":
		sourceVal, ok := cfg.Options["source"]
		if !ok {
			result.Error = "aix adapter requires 'source' in config (e.g., cursor)"
			return result
		}
		source, ok := sourceVal.(string)
		if !ok || source == "" {
			result.Error = "aix adapter 'source' must be a string"
			return result
		}
		adapter, err = adapters.NewAixAdapter(source)
		if err != nil {
			result.Error = fmt.Sprintf("Failed to create adapter: %v", err)
			return result
		}

	case "nexus":
		var opts adapters.NexusAdapterOptions
		if v, ok := cfg.Options["events_dir"]; ok {
			if s, ok := v.(string); ok && s != "" {
				opts.EventsDir = s
			}
		}
		if v, ok := cfg.Options["state_dir"]; ok {
			if s, ok := v.(string); ok && s != "" {
				opts.StateDir = s
			}
		}
		if v, ok := cfg.Options["source"]; ok {
			if s, ok := v.(string); ok && s != "" {
				opts.Source = s
			}
		}
		adapter, err = adapters.NewNexusAdapter(opts)
		if err != nil {
			result.Error = fmt.Sprintf("Failed to create adapter: %v", err)
			return result
		}

	case "bird":
		// X/Twitter adapter via bird CLI
		username := ""
		if usernameVal, ok := cfg.Options["username"]; ok {
			username, _ = usernameVal.(string)
		}
		adapter, err = adapters.NewBirdAdapter(username)
		if err != nil {
			result.Error = fmt.Sprintf("Failed to create adapter: %v", err)
			return result
		}

	default:
		result.Error = fmt.Sprintf("Unknown adapter type: %s", cfg.Type)
		return result
	}

	// Run sync
	syncResult, err := adapter.Sync(ctx, db, full)
	if err != nil {
		result.Error = fmt.Sprintf("Sync failed: %v", err)
		_ = FinishJobError(db, name, "sync", nil, result.Error, nil)
		return result
	}

	// Populate result
	result.Success = true
	result.EventsCreated = syncResult.EventsCreated
	result.EventsUpdated = syncResult.EventsUpdated
	result.PersonsCreated = syncResult.PersonsCreated
	result.ThreadsCreated = syncResult.ThreadsCreated
	result.ThreadsUpdated = syncResult.ThreadsUpdated
	result.AttachmentsCreated = syncResult.AttachmentsCreated
	result.AttachmentsUpdated = syncResult.AttachmentsUpdated
	result.ReactionsCreated = syncResult.ReactionsCreated
	result.ReactionsUpdated = syncResult.ReactionsUpdated
	result.Duration = syncResult.Duration.String()
	result.Perf = syncResult.Perf

	_ = FinishJobSuccess(db, name, "sync", nil, map[string]any{
		"events_created":      result.EventsCreated,
		"events_updated":      result.EventsUpdated,
		"persons_created":     result.PersonsCreated,
		"threads_created":     result.ThreadsCreated,
		"threads_updated":     result.ThreadsUpdated,
		"attachments_created": result.AttachmentsCreated,
		"attachments_updated": result.AttachmentsUpdated,
		"reactions_created":   result.ReactionsCreated,
		"reactions_updated":   result.ReactionsUpdated,
		"duration":            result.Duration,
		"finished_at":         time.Now().Unix(),
	})

	return result
}
