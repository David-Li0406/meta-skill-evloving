package live

import (
	"database/sql"
	"fmt"
	"strconv"
	"time"

	"github.com/Napageneral/cortex/internal/state"
)

const (
	keyLiveStatus        = "live_status"
	keyLiveLastHeartbeat = "live_last_heartbeat"
	keyLiveLastError     = "live_last_error"
	keyLiveRestarts      = "live_restarts"
)

func setLiveStatus(db *sql.DB, adapter string, status string) {
	_ = state.Set(db, adapter, keyLiveStatus, status)
}

func setLiveHeartbeat(db *sql.DB, adapter string, t time.Time) {
	_ = state.Set(db, adapter, keyLiveLastHeartbeat, fmt.Sprintf("%d", t.Unix()))
}

func setLiveError(db *sql.DB, adapter string, err error) {
	msg := ""
	if err != nil {
		msg = err.Error()
	}
	_ = state.Set(db, adapter, keyLiveLastError, msg)
}

func incrementLiveRestarts(db *sql.DB, adapter string) {
	v, ok, err := state.Get(db, adapter, keyLiveRestarts)
	if err != nil {
		return
	}
	cur := 0
	if ok && v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			cur = n
		}
	}
	_ = state.Set(db, adapter, keyLiveRestarts, fmt.Sprintf("%d", cur+1))
}

func readLiveStatus(db *sql.DB, adapter string) (status string, lastHeartbeat *int64, lastError string, restarts int) {
	if v, ok, _ := state.Get(db, adapter, keyLiveStatus); ok {
		status = v
	}
	if v, ok, _ := state.Get(db, adapter, keyLiveLastHeartbeat); ok && v != "" {
		if n, err := strconv.ParseInt(v, 10, 64); err == nil {
			lastHeartbeat = &n
		}
	}
	if v, ok, _ := state.Get(db, adapter, keyLiveLastError); ok {
		lastError = v
	}
	if v, ok, _ := state.Get(db, adapter, keyLiveRestarts); ok && v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			restarts = n
		}
	}
	return status, lastHeartbeat, lastError, restarts
}
