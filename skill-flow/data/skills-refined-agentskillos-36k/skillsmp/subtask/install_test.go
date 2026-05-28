package install

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestInstallTo_WritesEmbeddedSkill(t *testing.T) {
	home := t.TempDir()

	path, err := InstallTo(ScopeUser, home)
	require.NoError(t, err)
	require.Equal(t, filepath.Join(home, ".claude", "skills", "subtask", "SKILL.md"), path)

	got, err := os.ReadFile(path)
	require.NoError(t, err)
	require.Equal(t, Embedded(), got)
}

func TestUninstallFrom_RemovesSkillFile(t *testing.T) {
	home := t.TempDir()

	path, err := InstallTo(ScopeUser, home)
	require.NoError(t, err)

	_, err = os.Stat(path)
	require.NoError(t, err)

	removedPath, err := UninstallFrom(ScopeUser, home)
	require.NoError(t, err)
	require.Equal(t, path, removedPath)

	_, err = os.Stat(path)
	require.ErrorIs(t, err, os.ErrNotExist)
}

func TestGetSkillStatusFor(t *testing.T) {
	home := t.TempDir()

	st, err := GetSkillStatusFor(ScopeUser, home)
	require.NoError(t, err)
	require.False(t, st.Installed)
	require.False(t, st.UpToDate)
	require.NotEmpty(t, st.Path)
	require.Len(t, st.EmbeddedSHA256, 64)
	require.Empty(t, st.InstalledSHA256)

	_, err = InstallTo(ScopeUser, home)
	require.NoError(t, err)

	st, err = GetSkillStatusFor(ScopeUser, home)
	require.NoError(t, err)
	require.True(t, st.Installed)
	require.True(t, st.UpToDate)
	require.Len(t, st.InstalledSHA256, 64)

	// Drift the installed skill.
	require.NoError(t, os.WriteFile(st.Path, []byte("different"), 0o644))

	st, err = GetSkillStatusFor(ScopeUser, home)
	require.NoError(t, err)
	require.True(t, st.Installed)
	require.False(t, st.UpToDate)
}
