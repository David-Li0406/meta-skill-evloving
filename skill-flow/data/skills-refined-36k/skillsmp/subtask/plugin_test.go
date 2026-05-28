package install

import (
	"os"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestInstallPluginTo_WritesEmbeddedFiles(t *testing.T) {
	base := t.TempDir()

	dir, updated, err := InstallPluginTo(ScopeUser, base)
	require.NoError(t, err)
	require.True(t, updated)

	require.FileExists(t, filepath.Join(dir, ".claude-plugin", "plugin.json"))
	require.FileExists(t, filepath.Join(dir, "hooks", "hooks.json"))
	require.FileExists(t, filepath.Join(dir, "scripts", "skill-reminder.sh"))

	info, err := os.Stat(filepath.Join(dir, "scripts", "skill-reminder.sh"))
	require.NoError(t, err)
	if runtime.GOOS != "windows" {
		require.NotZero(t, info.Mode().Perm()&0o111, "should be executable on Unix")
	}

	_, updated, err = InstallPluginTo(ScopeUser, base)
	require.NoError(t, err)
	require.False(t, updated)
}

func TestGetPluginStatusFor(t *testing.T) {
	base := t.TempDir()

	st, err := GetPluginStatusFor(ScopeUser, base)
	require.NoError(t, err)
	require.False(t, st.Installed)
	require.False(t, st.UpToDate)
	require.NotEmpty(t, st.Dir)
	require.Len(t, st.EmbeddedSHA256, 64)
	require.Empty(t, st.InstalledSHA256)

	_, _, err = InstallPluginTo(ScopeUser, base)
	require.NoError(t, err)

	st, err = GetPluginStatusFor(ScopeUser, base)
	require.NoError(t, err)
	require.True(t, st.Installed)
	require.True(t, st.UpToDate)
	require.Len(t, st.InstalledSHA256, 64)

	// Drift.
	require.NoError(t, os.WriteFile(filepath.Join(st.Dir, "hooks", "hooks.json"), []byte(`{}`), 0o644))

	st, err = GetPluginStatusFor(ScopeUser, base)
	require.NoError(t, err)
	require.True(t, st.Installed)
	require.False(t, st.UpToDate)
}
