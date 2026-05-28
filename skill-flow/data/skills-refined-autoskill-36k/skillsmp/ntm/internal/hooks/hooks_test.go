package hooks

import (
	"strings"
	"testing"
)

func TestGeneratePreCommitScriptIncludesBeadsSync(t *testing.T) {
	repoRoot := "/tmp/project path/with spaces"
	script := generatePreCommitScript("/usr/local/bin/ntm", repoRoot)

	if !strings.Contains(script, "br sync --flush-only") {
		t.Errorf("expected beads sync in pre-commit hook, got: %q", script)
	}
	if !strings.Contains(script, "hooks run pre-commit") {
		t.Errorf("expected pre-commit hook to call ntm hooks run, got: %q", script)
	}
	if !strings.Contains(script, "REPO_ROOT="+quoteShell(repoRoot)) {
		t.Errorf("expected quoted REPO_ROOT assignment, got: %q", script)
	}
}

func TestGeneratePostCheckoutScriptWarnsOnBeadsChanges(t *testing.T) {
	repoRoot := "/tmp/project path/with spaces"
	script := generatePostCheckoutScript(repoRoot)

	if !strings.Contains(script, "post-checkout") {
		t.Errorf("expected post-checkout marker in hook, got: %q", script)
	}
	if !strings.Contains(script, "Warning: .beads has uncommitted changes") {
		t.Errorf("expected .beads warning in post-checkout hook, got: %q", script)
	}
	if !strings.Contains(script, "REPO_ROOT="+quoteShell(repoRoot)) {
		t.Errorf("expected quoted REPO_ROOT assignment, got: %q", script)
	}
}
