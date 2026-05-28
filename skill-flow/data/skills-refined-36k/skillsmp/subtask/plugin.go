package install

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"os"
	"path/filepath"
)

const claudePluginName = "subtask"

// PluginStatus describes the installation state of the embedded plugin.
type PluginStatus struct {
	Dir             string
	Installed       bool
	UpToDate        bool
	EmbeddedSHA256  string
	InstalledSHA256 string
}

func PluginDir(scope Scope, baseDir string) string {
	_ = scope // for symmetry
	if baseDir == "" {
		return ""
	}
	return filepath.Join(baseDir, ".claude", "plugins", claudePluginName)
}

func pluginMarkerPath(scope Scope, baseDir string) string {
	dir := PluginDir(scope, baseDir)
	if dir == "" {
		return ""
	}
	return filepath.Join(dir, ".claude-plugin", "plugin.json")
}

func isPluginInstalled(scope Scope, baseDir string) bool {
	marker := pluginMarkerPath(scope, baseDir)
	if marker == "" {
		return false
	}
	_, err := os.Stat(marker)
	return err == nil
}

func InstallPluginTo(scope Scope, baseDir string) (string, bool, error) {
	dir := PluginDir(scope, baseDir)
	if dir == "" {
		return "", false, errors.New("invalid base directory")
	}

	manifest, _, err := embeddedPluginManifest()
	if err != nil {
		return "", false, err
	}

	updated := false
	for _, f := range manifest {
		dst := filepath.Join(dir, f.RelPath)
		if existing, err := os.ReadFile(dst); err == nil && bytes.Equal(existing, f.Data) {
			continue
		}
		if err := os.MkdirAll(filepath.Dir(dst), 0o755); err != nil {
			return "", false, err
		}
		if err := os.WriteFile(dst, f.Data, f.Perm); err != nil {
			return "", false, err
		}
		updated = true
	}

	return dir, updated, nil
}

func UninstallPluginFrom(scope Scope, baseDir string) (string, error) {
	dir := PluginDir(scope, baseDir)
	if dir == "" {
		return "", errors.New("invalid base directory")
	}
	if err := os.RemoveAll(dir); err != nil {
		return "", err
	}
	return dir, nil
}

func GetPluginStatusFor(scope Scope, baseDir string) (PluginStatus, error) {
	dir := PluginDir(scope, baseDir)
	if dir == "" {
		return PluginStatus{}, errors.New("invalid base directory")
	}

	manifest, embeddedSHA, err := embeddedPluginManifest()
	if err != nil {
		return PluginStatus{}, err
	}

	st := PluginStatus{
		Dir:            dir,
		Installed:      false,
		UpToDate:       false,
		EmbeddedSHA256: embeddedSHA,
	}

	if !isPluginInstalled(scope, baseDir) {
		return st, nil
	}

	st.Installed = true

	allPresent := true
	allMatch := true
	h := sha256.New()

	for _, f := range manifest {
		p := filepath.Join(dir, f.RelPath)
		b, err := os.ReadFile(p)
		if err != nil {
			allPresent = false
			allMatch = false
			break
		}

		_, _ = h.Write([]byte(f.RelPath))
		_, _ = h.Write([]byte{0})
		_, _ = h.Write(b)
		_, _ = h.Write([]byte{0})

		if !bytes.Equal(b, f.Data) {
			allMatch = false
		}
	}

	if allPresent {
		st.InstalledSHA256 = hex.EncodeToString(h.Sum(nil))
	}
	st.UpToDate = allMatch
	return st, nil
}
