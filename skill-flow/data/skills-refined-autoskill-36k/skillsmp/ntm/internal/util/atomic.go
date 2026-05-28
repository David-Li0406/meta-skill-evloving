package util

import (
	"fmt"
	"os"
	"path/filepath"
)

// AtomicWriteFile writes data to a file atomically by writing to a temp file
// and then renaming it. This ensures the file is either fully written or not
// updated at all, preventing corruption on crash.
func AtomicWriteFile(filename string, data []byte, perm os.FileMode) error {
	dir := filepath.Dir(filename)

	// Create temp file in the same directory to ensure same filesystem (for atomic rename)
	tmpFile, err := os.CreateTemp(dir, "ntm-atomic-*")
	if err != nil {
		return fmt.Errorf("creating temp file: %w", err)
	}
	defer func() {
		tmpFile.Close()
		os.Remove(tmpFile.Name()) // Clean up if rename fails
	}()

	if _, err := tmpFile.Write(data); err != nil {
		return fmt.Errorf("writing to temp file: %w", err)
	}

	if err := tmpFile.Chmod(perm); err != nil {
		return fmt.Errorf("chmod temp file: %w", err)
	}

	// Sync to ensure data is on disk
	if err := tmpFile.Sync(); err != nil {
		return fmt.Errorf("syncing temp file: %w", err)
	}

	if err := tmpFile.Close(); err != nil {
		return fmt.Errorf("closing temp file: %w", err)
	}

	// Atomic rename
	if err := os.Rename(tmpFile.Name(), filename); err != nil {
		return fmt.Errorf("renaming temp file: %w", err)
	}

	return nil
}
