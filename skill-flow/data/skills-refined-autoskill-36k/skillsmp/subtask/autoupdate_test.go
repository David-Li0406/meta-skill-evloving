package install

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestAutoUpdateIfInstalled_DoesNotCreateWhenMissing(t *testing.T) {
	base := t.TempDir()

	res, err := AutoUpdateIfInstalled(ScopeUser, base)
	require.NoError(t, err)
	require.False(t, res.UpdatedSkill)
	require.False(t, res.UpdatedPlugin)

	_, err = os.Stat(SkillPath(ScopeUser, base))
	require.ErrorIs(t, err, os.ErrNotExist)
	_, err = os.Stat(pluginMarkerPath(ScopeUser, base))
	require.ErrorIs(t, err, os.ErrNotExist)
}

func TestAutoUpdateIfInstalled_RepairsDrift(t *testing.T) {
	base := t.TempDir()

	_, err := InstallTo(ScopeUser, base)
	require.NoError(t, err)
	_, _, err = InstallPluginTo(ScopeUser, base)
	require.NoError(t, err)

	// Drift both.
	require.NoError(t, os.WriteFile(SkillPath(ScopeUser, base), []byte("different"), 0o644))
	require.NoError(t, os.WriteFile(filepath.Join(PluginDir(ScopeUser, base), "hooks", "hooks.json"), []byte(`{}`), 0o644))

	res, err := AutoUpdateIfInstalled(ScopeUser, base)
	require.NoError(t, err)
	require.True(t, res.UpdatedSkill)
	require.True(t, res.UpdatedPlugin)

	got, err := os.ReadFile(SkillPath(ScopeUser, base))
	require.NoError(t, err)
	require.Equal(t, Embedded(), got)

	pst, err := GetPluginStatusFor(ScopeUser, base)
	require.NoError(t, err)
	require.True(t, pst.UpToDate)
}
