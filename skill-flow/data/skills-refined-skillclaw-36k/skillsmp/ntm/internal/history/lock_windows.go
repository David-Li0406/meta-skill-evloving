//go:build windows

package history

import (
	"os"
	"path/filepath"
)

// acquireLock acquires thread-level mutex lock only on Windows.
// File locking is not supported on Windows in this implementation.
// Returns an unlock function to release the lock.
func acquireLock() (func(), error) {
	localMu.Lock()

	// Ensure directory exists
	path := StoragePath()
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		localMu.Unlock()
		return nil, err
	}

	return func() {
		localMu.Unlock()
	}, nil
}
