package live

import (
	"database/sql"
	"fmt"

	"github.com/Napageneral/cortex/internal/config"
)

type AdapterLiveStatus struct {
	Adapter       string `json:"adapter"`
	Type          string `json:"type"`
	Enabled       bool   `json:"enabled"`
	Supported     bool   `json:"supported"`
	Status        string `json:"status,omitempty"`
	LastHeartbeat *int64 `json:"last_heartbeat,omitempty"`
	LastError     string `json:"last_error,omitempty"`
	Restarts      int    `json:"restarts,omitempty"`
}

func GetStatuses(db *sql.DB, cfg *config.Config) ([]AdapterLiveStatus, error) {
	if cfg == nil {
		return nil, fmt.Errorf("config is required")
	}

	var out []AdapterLiveStatus
	for name, adapterCfg := range cfg.Adapters {
		enabled := false
		if adapterCfg.Live != nil && adapterCfg.Live.Enabled {
			enabled = true
		}
		status, lastHeartbeat, lastError, restarts := readLiveStatus(db, name)
		out = append(out, AdapterLiveStatus{
			Adapter:       name,
			Type:          adapterCfg.Type,
			Enabled:       enabled,
			Supported:     LiveSupported(adapterCfg.Type),
			Status:        status,
			LastHeartbeat: lastHeartbeat,
			LastError:     lastError,
			Restarts:      restarts,
		})
	}
	return out, nil
}
