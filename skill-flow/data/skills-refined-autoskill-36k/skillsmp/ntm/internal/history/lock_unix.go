//go:build unix

package history

import (
	"os"
	"path/filepath"
	"syscall"
)

// acquireLock acquires both process-level (flock) and thread-level (mutex) locks.
// Returns an unlock function to release both.
func acquireLock() (func(), error) {
	localMu.Lock()

	// Ensure directory exists for lock file
	path := StoragePath()
	lockPath := path + ".lock"
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		localMu.Unlock()
		return nil, err
	}

	f, err := os.OpenFile(lockPath, os.O_CREATE|os.O_RDWR, 0666)
	if err != nil {
		localMu.Unlock()
		return nil, err
	}

	if err := syscall.Flock(int(f.Fd()), syscall.LOCK_EX); err != nil {
		f.Close()
		localMu.Unlock()
		return nil, err
	}

	return func() {
		_ = syscall.Flock(int(f.Fd()), syscall.LOCK_UN)
		f.Close()
		localMu.Unlock()
	}, nil
}
