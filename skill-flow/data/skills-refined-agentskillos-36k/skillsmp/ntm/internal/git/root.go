package git

import (
	"os/exec"
	"strings"
)

// FindProjectRoot attempts to find the root of the git repository
// containing the given directory. Returns empty string if not found.
func FindProjectRoot(startDir string) (string, error) {
	cmd := exec.Command("git", "rev-parse", "--show-toplevel")
	cmd.Dir = startDir
	output, err := cmd.Output()
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(output)), nil
}
