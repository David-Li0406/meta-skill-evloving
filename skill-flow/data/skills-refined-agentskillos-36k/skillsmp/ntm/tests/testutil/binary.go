package testutil

import (
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
	"testing"
)

var (
	buildOnce  sync.Once
	binaryPath string
	buildErr   error
)

func findRepoRoot(start string) (string, error) {
	dir := start
	for {
		if _, err := os.Stat(filepath.Join(dir, "go.mod")); err == nil {
			return dir, nil
		}
		parent := filepath.Dir(dir)
		if parent == dir {
			return "", errors.New("could not find go.mod while walking up from working directory")
		}
		dir = parent
	}
}

// BuildLocalNTM builds the ntm binary from the current workspace and returns its path.
// It builds only once per test process.
func BuildLocalNTM(t *testing.T) string {
	t.Helper()

	buildOnce.Do(func() {
		cwd, err := os.Getwd()
		if err != nil {
			buildErr = err
			return
		}
		repoRoot, err := findRepoRoot(cwd)
		if err != nil {
			buildErr = err
			return
		}

		dir, err := os.MkdirTemp("", "ntm-bin-*")
		if err != nil {
			buildErr = err
			return
		}

		exeSuffix := ""
		if runtime.GOOS == "windows" {
			exeSuffix = ".exe"
		}
		binaryPath = filepath.Join(dir, "ntm"+exeSuffix)

		cmd := exec.Command("go", "build", "-o", binaryPath, "./cmd/ntm")
		cmd.Dir = repoRoot
		cmd.Env = os.Environ()
		out, err := cmd.CombinedOutput()
		if err != nil {
			buildErr = fmt.Errorf("go build failed (dir=%s): %w\n%s", repoRoot, err, strings.TrimSpace(string(out)))
			return
		}
	})

	if buildErr != nil {
		t.Fatalf("failed to build local ntm binary: %v", buildErr)
	}
	return binaryPath
}
