package install

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestEnsurePluginEnabled_CreatesAndIsIdempotent(t *testing.T) {
	base := t.TempDir()

	ch, err := EnsurePluginEnabled(ScopeUser, base)
	require.NoError(t, err)
	require.True(t, ch.Changed)

	settingsPath := filepath.Join(base, ".claude", "settings.json")
	data, err := os.ReadFile(settingsPath)
	require.NoError(t, err)

	var m map[string]any
	require.NoError(t, json.Unmarshal(data, &m))
	plugins, ok := m["enabledPlugins"].(map[string]any)
	require.True(t, ok, "enabledPlugins should be an object")
	require.Equal(t, true, plugins[claudePluginName])

	ch2, err := EnsurePluginEnabled(ScopeUser, base)
	require.NoError(t, err)
	require.False(t, ch2.Changed)
}

func TestRemovePluginEnabled_DoesNotCreateMissingFile(t *testing.T) {
	base := t.TempDir()

	ch, err := RemovePluginEnabled(ScopeUser, base)
	require.NoError(t, err)
	require.False(t, ch.Changed)

	_, err = os.Stat(filepath.Join(base, ".claude", "settings.json"))
	require.ErrorIs(t, err, os.ErrNotExist)
}

func TestEnsurePluginEnabled_MalformedJSON_BackupsAndRewrites(t *testing.T) {
	base := t.TempDir()
	settingsPath := filepath.Join(base, ".claude", "settings.json")
	require.NoError(t, os.MkdirAll(filepath.Dir(settingsPath), 0o755))
	require.NoError(t, os.WriteFile(settingsPath, []byte("{not json"), 0o644))

	ch, err := EnsurePluginEnabled(ScopeUser, base)
	require.NoError(t, err)
	require.True(t, ch.Rewrote)
	require.NotEmpty(t, ch.BackupTo)
	require.FileExists(t, ch.BackupTo)

	data, err := os.ReadFile(settingsPath)
	require.NoError(t, err)
	var m map[string]any
	require.NoError(t, json.Unmarshal(data, &m))
	plugins, ok := m["enabledPlugins"].(map[string]any)
	require.True(t, ok, "enabledPlugins should be an object")
	require.Equal(t, true, plugins[claudePluginName])
}

func TestEnsurePluginEnabled_PreservesExistingSettings(t *testing.T) {
	base := t.TempDir()
	settingsPath := filepath.Join(base, ".claude", "settings.json")
	require.NoError(t, os.MkdirAll(filepath.Dir(settingsPath), 0o755))

	// Write existing settings with object format
	existing := map[string]any{
		"someOtherSetting": true,
		"enabledPlugins": map[string]any{
			"other-plugin": true,
		},
	}
	data, _ := json.MarshalIndent(existing, "", "  ")
	require.NoError(t, os.WriteFile(settingsPath, append(data, '\n'), 0o644))

	ch, err := EnsurePluginEnabled(ScopeUser, base)
	require.NoError(t, err)
	require.True(t, ch.Changed)

	// Read back and verify
	data, err = os.ReadFile(settingsPath)
	require.NoError(t, err)
	var m map[string]any
	require.NoError(t, json.Unmarshal(data, &m))

	// Other settings preserved
	require.Equal(t, true, m["someOtherSetting"])

	// Both plugins present
	plugins, ok := m["enabledPlugins"].(map[string]any)
	require.True(t, ok, "enabledPlugins should be an object")
	require.Equal(t, true, plugins["other-plugin"])
	require.Equal(t, true, plugins[claudePluginName])
}

func TestRemovePluginEnabled_PreservesOtherPlugins(t *testing.T) {
	base := t.TempDir()
	settingsPath := filepath.Join(base, ".claude", "settings.json")
	require.NoError(t, os.MkdirAll(filepath.Dir(settingsPath), 0o755))

	// Write existing settings
	existing := map[string]any{
		"enabledPlugins": map[string]any{
			"other-plugin":   true,
			claudePluginName: true,
		},
	}
	data, _ := json.MarshalIndent(existing, "", "  ")
	require.NoError(t, os.WriteFile(settingsPath, append(data, '\n'), 0o644))

	ch, err := RemovePluginEnabled(ScopeUser, base)
	require.NoError(t, err)
	require.True(t, ch.Changed)

	// Read back and verify
	data, err = os.ReadFile(settingsPath)
	require.NoError(t, err)
	var m map[string]any
	require.NoError(t, json.Unmarshal(data, &m))

	plugins, ok := m["enabledPlugins"].(map[string]any)
	require.True(t, ok, "enabledPlugins should be an object")
	require.Equal(t, true, plugins["other-plugin"])
	_, hasSubtask := plugins[claudePluginName]
	require.False(t, hasSubtask)
}
