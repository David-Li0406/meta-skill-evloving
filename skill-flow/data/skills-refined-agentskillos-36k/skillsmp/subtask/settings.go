package install

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"time"
)

// SettingsStatus describes plugin registration status for Claude Code.
type SettingsStatus struct {
	Path          string
	Exists        bool
	PluginEnabled bool
	Error         string
}

func SettingsPath(scope Scope, baseDir string) string {
	_ = scope // for symmetry
	if baseDir == "" {
		return ""
	}
	return filepath.Join(baseDir, ".claude", "settings.json")
}

func GetSettingsStatusFor(scope Scope, baseDir string) SettingsStatus {
	path := SettingsPath(scope, baseDir)
	st := SettingsStatus{Path: path}
	if path == "" {
		st.Error = "invalid base directory"
		return st
	}

	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return st
		}
		st.Error = err.Error()
		return st
	}

	st.Exists = true
	var m map[string]any
	if err := json.Unmarshal(data, &m); err != nil {
		st.Error = "malformed JSON"
		return st
	}

	plugins := getEnabledPluginsMap(m)
	if enabled, ok := plugins[claudePluginName].(bool); ok && enabled {
		st.PluginEnabled = true
	}
	return st
}

type SettingsChange struct {
	Path     string
	Changed  bool
	Rewrote  bool
	BackupTo string
}

func EnsurePluginEnabled(scope Scope, baseDir string) (SettingsChange, error) {
	path := SettingsPath(scope, baseDir)
	if path == "" {
		return SettingsChange{}, errors.New("invalid base directory")
	}
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		return SettingsChange{}, err
	}

	m, rewrote, backupTo, err := readSettingsFile(path)
	if err != nil {
		return SettingsChange{}, err
	}

	plugins := getEnabledPluginsMap(m)

	// Check if already enabled
	if enabled, ok := plugins[claudePluginName].(bool); ok && enabled {
		return SettingsChange{Path: path, Changed: false, Rewrote: rewrote, BackupTo: backupTo}, nil
	}

	// Enable the plugin
	plugins[claudePluginName] = true
	m["enabledPlugins"] = plugins

	if err := writeSettingsFile(path, m); err != nil {
		return SettingsChange{}, err
	}

	return SettingsChange{Path: path, Changed: true, Rewrote: rewrote, BackupTo: backupTo}, nil
}

func RemovePluginEnabled(scope Scope, baseDir string) (SettingsChange, error) {
	path := SettingsPath(scope, baseDir)
	if path == "" {
		return SettingsChange{}, errors.New("invalid base directory")
	}

	// Don't create file if it doesn't exist
	if _, err := os.Stat(path); os.IsNotExist(err) {
		return SettingsChange{Path: path, Changed: false}, nil
	}

	m, rewrote, backupTo, err := readSettingsFile(path)
	if err != nil {
		return SettingsChange{}, err
	}

	plugins := getEnabledPluginsMap(m)

	// Check if not present
	if _, ok := plugins[claudePluginName]; !ok {
		// If we had to rewrite due to malformed JSON, write out a fresh, valid settings file.
		if rewrote {
			m["enabledPlugins"] = plugins
			if err := writeSettingsFile(path, m); err != nil {
				return SettingsChange{}, err
			}
		}
		return SettingsChange{Path: path, Changed: false, Rewrote: rewrote, BackupTo: backupTo}, nil
	}

	// Remove the plugin
	delete(plugins, claudePluginName)
	m["enabledPlugins"] = plugins

	if err := writeSettingsFile(path, m); err != nil {
		return SettingsChange{}, err
	}

	return SettingsChange{Path: path, Changed: true, Rewrote: rewrote, BackupTo: backupTo}, nil
}

// readSettingsFile reads and parses settings.json, returning empty map if missing.
func readSettingsFile(path string) (m map[string]any, rewrote bool, backupTo string, err error) {
	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return make(map[string]any), false, "", nil
		}
		return nil, false, "", err
	}

	if err := json.Unmarshal(data, &m); err != nil {
		// Malformed JSON - backup and start fresh
		backupTo, err2 := backupFile(path)
		if err2 != nil {
			return nil, false, "", err2
		}
		return make(map[string]any), true, backupTo, nil
	}

	if m == nil {
		m = make(map[string]any)
	}
	return m, false, "", nil
}

// writeSettingsFile writes settings map to path with pretty formatting.
func writeSettingsFile(path string, m map[string]any) error {
	b, err := json.MarshalIndent(m, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, append(b, '\n'), 0o644)
}

// getEnabledPluginsMap extracts or creates the enabledPlugins map.
// Claude Code expects enabledPlugins to be an object: {"plugin-name": true, ...}
func getEnabledPluginsMap(m map[string]any) map[string]any {
	if m == nil {
		return make(map[string]any)
	}

	v := m["enabledPlugins"]
	if v == nil {
		return make(map[string]any)
	}

	// Already correct format
	if plugins, ok := v.(map[string]any); ok {
		return plugins
	}
	// Also accept map[string]bool if produced by other tooling.
	if plugins, ok := v.(map[string]bool); ok {
		out := make(map[string]any, len(plugins))
		for k, b := range plugins {
			out[k] = b
		}
		return out
	}

	// Convert from array format (legacy/incorrect) to object format
	if arr, ok := v.([]any); ok {
		plugins := make(map[string]any)
		for _, item := range arr {
			if name, ok := item.(string); ok && name != "" {
				plugins[name] = true
			}
		}
		return plugins
	}

	// Unknown format, return empty
	return make(map[string]any)
}
func backupFile(path string) (string, error) {
	if _, err := os.Stat(path); err != nil {
		if os.IsNotExist(err) {
			return "", nil
		}
		return "", err
	}

	backupTo := path + ".bak"
	if _, err := os.Stat(backupTo); err == nil {
		backupTo = path + ".bak-" + time.Now().UTC().Format("20060102T150405Z")
	}
	if err := os.Rename(path, backupTo); err != nil {
		return "", err
	}
	return backupTo, nil
}
