package util

import (
	"fmt"
	"os"
	"path/filepath"
)

// NTMDir returns the path to the ~/.ntm directory.
func NTMDir() (string, error) {
	home, err := os.UserHomeDir()
	if err != nil {
		return "", fmt.Errorf("failed to get home directory: %w", err)
	}
	return filepath.Join(home, ".ntm"), nil
}

// EnsureDir ensures that a directory exists, creating it if necessary.
func EnsureDir(path string) error {
	return os.MkdirAll(path, 0755)
}
