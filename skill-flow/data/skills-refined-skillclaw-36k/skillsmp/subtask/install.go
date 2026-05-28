package install

import (
	"bytes"
	"crypto/sha256"
	_ "embed"
	"encoding/hex"
	"errors"
	"os"
	"path/filepath"

	"github.com/zippoxer/subtask/internal/homedir"
)

//go:embed SKILL.md
var embeddedSkill []byte

type Scope string

const (
	ScopeUser    Scope = "user"
	ScopeProject Scope = "project"
)

// SkillStatus describes the installation state of the embedded skill.
type SkillStatus struct {
	Path            string
	Installed       bool
	UpToDate        bool
	EmbeddedSHA256  string
	InstalledSHA256 string
}

// Embedded returns the embedded skill contents.
func Embedded() []byte {
	return bytes.Clone(embeddedSkill)
}

// SkillPath returns the Claude Code skill path for the given base directory.
// For user scope, baseDir should be the user's home directory.
// For project scope, baseDir should be the project root directory.
func SkillPath(scope Scope, baseDir string) string {
	_ = scope // for symmetry with other install targets
	if baseDir == "" {
		return ""
	}
	return filepath.Join(baseDir, ".claude", "skills", "subtask", "SKILL.md")
}

// Install writes the embedded skill to the Claude Code skill location (user scope).
func Install() (string, error) {
	homeDir, err := homedir.Dir()
	if err != nil {
		return "", err
	}
	return InstallTo(ScopeUser, homeDir)
}

// InstallTo writes the embedded skill to the Claude Code skill location under baseDir.
func InstallTo(scope Scope, baseDir string) (string, error) {
	path, _, err := syncSkillTo(scope, baseDir)
	return path, err
}

// Uninstall removes the skill from the Claude Code skill location (user scope).
func Uninstall() (string, error) {
	homeDir, err := homedir.Dir()
	if err != nil {
		return "", err
	}
	return UninstallFrom(ScopeUser, homeDir)
}

// UninstallFrom removes the skill from the Claude Code skill location under baseDir.
func UninstallFrom(scope Scope, baseDir string) (string, error) {
	path := SkillPath(scope, baseDir)
	if path == "" {
		return "", errors.New("invalid base directory")
	}
	if err := os.Remove(path); err != nil && !os.IsNotExist(err) {
		return "", err
	}
	return path, nil
}

// GetSkillStatus returns installation status for the Claude Code skill location (user scope).
func GetSkillStatus() (SkillStatus, error) {
	homeDir, err := homedir.Dir()
	if err != nil {
		return SkillStatus{}, err
	}
	return GetSkillStatusFor(ScopeUser, homeDir)
}

// GetSkillStatusFor returns status for baseDir/scope without consulting environment.
func GetSkillStatusFor(scope Scope, baseDir string) (SkillStatus, error) {
	path := SkillPath(scope, baseDir)
	if path == "" {
		return SkillStatus{}, errors.New("invalid base directory")
	}

	embeddedSHA := sha256Hex(embeddedSkill)
	st := SkillStatus{
		Path:           path,
		Installed:      false,
		UpToDate:       false,
		EmbeddedSHA256: embeddedSHA,
	}

	installed, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return st, nil
		}
		return SkillStatus{}, err
	}

	st.Installed = true
	st.InstalledSHA256 = sha256Hex(installed)
	st.UpToDate = bytes.Equal(installed, embeddedSkill)
	return st, nil
}

func sha256Hex(b []byte) string {
	sum := sha256.Sum256(b)
	return hex.EncodeToString(sum[:])
}

func syncSkillTo(scope Scope, baseDir string) (string, bool, error) {
	path := SkillPath(scope, baseDir)
	if path == "" {
		return "", false, errors.New("invalid base directory")
	}

	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		return "", false, err
	}

	if existing, err := os.ReadFile(path); err == nil && bytes.Equal(existing, embeddedSkill) {
		return path, false, nil
	}

	if err := os.WriteFile(path, embeddedSkill, 0o644); err != nil {
		return "", false, err
	}
	return path, true, nil
}

func isSkillInstalled(scope Scope, baseDir string) bool {
	path := SkillPath(scope, baseDir)
	if path == "" {
		return false
	}
	_, err := os.Stat(path)
	return err == nil
}
