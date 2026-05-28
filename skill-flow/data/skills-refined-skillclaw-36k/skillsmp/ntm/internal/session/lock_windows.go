//go:build windows

package session

import (
	"os"
	"sync"
)

var localMu sync.Mutex

// acquireLock acquires thread-level (mutex) lock only.
// Windows file locking is complex, skipping for now (CLI usage is low concurrency).
func acquireLock() (func(), error) {
	localMu.Lock()

	// Ensure directory exists
	dir := StorageDir()
	if err := os.MkdirAll(dir, 0755); err != nil {
		localMu.Unlock()
		return nil, err
	}

	return func() {
		localMu.Unlock()
	}, nil
}
