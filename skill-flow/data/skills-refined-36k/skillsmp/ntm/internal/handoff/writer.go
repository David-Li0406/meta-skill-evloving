package handoff

import (
	"fmt"
	"log/slog"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"sync"
	"time"

	"gopkg.in/yaml.v3"
)

var (
	// writeMu protects concurrent writes to the same directory.
	writeMu sync.Mutex

	// descriptionRegex is defined in validate.go as sessionNameRegex
	// We reuse it for description validation (alphanumeric + hyphen).
)

// DefaultMaxPerDir is the default number of handoffs to keep before rotation.
const DefaultMaxPerDir = 50

// Writer handles writing handoff files to disk with atomic writes and rotation.
type Writer struct {
	baseDir   string // typically .ntm/handoffs
	maxPerDir int    // max handoffs before rotation (default 50)
	logger    *slog.Logger
}

// NewWriter creates a Writer for the given project directory.
func NewWriter(projectDir string) *Writer {
	return &Writer{
		baseDir:   filepath.Join(projectDir, ".ntm", "handoffs"),
		maxPerDir: DefaultMaxPerDir,
		logger:    slog.Default().With("component", "handoff.writer"),
	}
}

// NewWriterWithOptions creates a Writer with custom options.
func NewWriterWithOptions(projectDir string, maxPerDir int, logger *slog.Logger) *Writer {
	if maxPerDir <= 0 {
		maxPerDir = DefaultMaxPerDir
	}
	if logger == nil {
		logger = slog.Default()
	}
	return &Writer{
		baseDir:   filepath.Join(projectDir, ".ntm", "handoffs"),
		maxPerDir: maxPerDir,
		logger:    logger.With("component", "handoff.writer"),
	}
}

// Write saves a handoff to the appropriate directory using atomic write.
// The description is sanitized to kebab-case for use in the filename.
// Returns the path to the written file.
func (w *Writer) Write(h *Handoff, description string) (string, error) {
	writeMu.Lock()
	defer writeMu.Unlock()

	w.logger.Debug("starting handoff write",
		"session", h.Session,
		"description", description,
		"goal_length", len(h.Goal),
		"now_length", len(h.Now),
	)

	// Validate handoff (includes session name validation)
	if errs := h.Validate(); len(errs) > 0 {
		w.logger.Error("handoff validation failed",
			"session", h.Session,
			"error_count", len(errs),
			"first_error", errs[0].Error(),
		)
		return "", fmt.Errorf("validation failed: %v", errs[0])
	}

	// Sanitize description
	desc := sanitizeDescription(description)
	if desc == "" {
		desc = "handoff"
	}

	// Ensure directory exists
	if err := w.EnsureDir(h.Session); err != nil {
		return "", err
	}

	// Check for rotation
	if err := w.checkRotation(h.Session); err != nil {
		w.logger.Warn("rotation check failed", "error", err)
		// Non-fatal, continue with write
	}

	// Set defaults
	h.SetDefaults()

	// Generate filename: YYYY-MM-DD_HH-MM_{description}.yaml
	filename := fmt.Sprintf("%s_%s.yaml",
		time.Now().Format("2006-01-02_15-04"),
		desc,
	)
	path := filepath.Join(w.baseDir, h.Session, filename)

	// Serialize to YAML
	data, err := yaml.Marshal(h)
	if err != nil {
		w.logger.Error("yaml marshaling failed",
			"session", h.Session,
			"error", err,
		)
		return "", fmt.Errorf("marshal failed: %w", err)
	}

	// Atomic write: write to temp, then rename
	if err := w.atomicWrite(path, data); err != nil {
		return "", err
	}

	w.logger.Info("handoff written successfully",
		"path", path,
		"session", h.Session,
		"goal", truncateLog(h.Goal, 50),
		"now", truncateLog(h.Now, 50),
		"size_bytes", len(data),
	)

	return path, nil
}

// WriteAuto saves an auto-generated handoff with timestamp naming.
// Auto handoffs use the format: auto-handoff-{ISO8601-timestamp}.yaml
func (w *Writer) WriteAuto(h *Handoff) (string, error) {
	writeMu.Lock()
	defer writeMu.Unlock()

	w.logger.Debug("starting auto-handoff write",
		"session", h.Session,
		"tokens_pct", h.TokensPct,
	)

	// Validate
	if errs := h.Validate(); len(errs) > 0 {
		w.logger.Error("auto-handoff validation failed",
			"session", h.Session,
			"error_count", len(errs),
		)
		return "", fmt.Errorf("validation failed: %v", errs[0])
	}

	// Ensure directory
	if err := w.EnsureDir(h.Session); err != nil {
		return "", err
	}

	// Check for rotation
	if err := w.checkRotation(h.Session); err != nil {
		w.logger.Warn("rotation check failed", "error", err)
	}

	// Set defaults
	h.SetDefaults()

	// Generate auto filename with ISO8601 timestamp
	filename := fmt.Sprintf("auto-handoff-%s.yaml",
		time.Now().Format("2006-01-02T15-04-05"),
	)
	path := filepath.Join(w.baseDir, h.Session, filename)

	// Serialize
	data, err := yaml.Marshal(h)
	if err != nil {
		return "", fmt.Errorf("marshal failed: %w", err)
	}

	// Atomic write
	if err := w.atomicWrite(path, data); err != nil {
		return "", err
	}

	w.logger.Info("auto-handoff written",
		"path", path,
		"session", h.Session,
		"tokens_pct", h.TokensPct,
		"size_bytes", len(data),
	)

	return path, nil
}

// EnsureDir creates the handoff directory for a session if needed.
func (w *Writer) EnsureDir(sessionName string) error {
	if sessionName == "" {
		sessionName = "general"
	}

	dir := filepath.Join(w.baseDir, sessionName)

	if err := os.MkdirAll(dir, 0755); err != nil {
		w.logger.Error("failed to create handoff directory",
			"dir", dir,
			"error", err,
		)
		return fmt.Errorf("mkdir failed: %w", err)
	}

	w.logger.Debug("ensured handoff directory", "dir", dir)
	return nil
}

// BaseDir returns the base directory where handoffs are stored.
func (w *Writer) BaseDir() string {
	return w.baseDir
}

// atomicWrite writes data to a temp file then renames to target path.
// This ensures the file is either fully written or not at all.
func (w *Writer) atomicWrite(path string, data []byte) error {
	dir := filepath.Dir(path)

	// Create temp file in same directory (ensures same filesystem for atomic rename)
	tmp, err := os.CreateTemp(dir, ".handoff-*.tmp")
	if err != nil {
		w.logger.Error("failed to create temp file",
			"dir", dir,
			"error", err,
		)
		return fmt.Errorf("temp file creation failed: %w", err)
	}
	tmpPath := tmp.Name()

	// Cleanup on failure
	success := false
	defer func() {
		if !success {
			os.Remove(tmpPath)
		}
	}()

	// Write data
	if _, err := tmp.Write(data); err != nil {
		tmp.Close()
		w.logger.Error("failed to write temp file",
			"path", tmpPath,
			"error", err,
		)
		return fmt.Errorf("write failed: %w", err)
	}

	// Sync to disk
	if err := tmp.Sync(); err != nil {
		tmp.Close()
		w.logger.Error("failed to sync temp file",
			"path", tmpPath,
			"error", err,
		)
		return fmt.Errorf("sync failed: %w", err)
	}

	// Close before rename
	if err := tmp.Close(); err != nil {
		return fmt.Errorf("close failed: %w", err)
	}

	// Set permissions
	if err := os.Chmod(tmpPath, 0644); err != nil {
		return fmt.Errorf("chmod failed: %w", err)
	}

	// Atomic rename
	if err := os.Rename(tmpPath, path); err != nil {
		w.logger.Error("failed to rename temp to target",
			"temp", tmpPath,
			"target", path,
			"error", err,
		)
		return fmt.Errorf("rename failed: %w", err)
	}

	success = true // Prevent cleanup of successful write
	return nil
}

// checkRotation moves old handoffs to .archive if count exceeds maxPerDir.
func (w *Writer) checkRotation(sessionName string) error {
	if sessionName == "" {
		sessionName = "general"
	}

	dir := filepath.Join(w.baseDir, sessionName)
	archiveDir := filepath.Join(dir, ".archive")

	entries, err := os.ReadDir(dir)
	if err != nil {
		if os.IsNotExist(err) {
			return nil // Directory doesn't exist yet, nothing to rotate
		}
		return err
	}

	// Count YAML files (exclude .archive dir and hidden files)
	var yamlFiles []os.DirEntry
	for _, e := range entries {
		if !e.IsDir() && strings.HasSuffix(e.Name(), ".yaml") && !strings.HasPrefix(e.Name(), ".") {
			yamlFiles = append(yamlFiles, e)
		}
	}

	// Check rotation needs: since we're about to write a new file,
	// rotate if count >= maxPerDir to make room
	if len(yamlFiles) < w.maxPerDir {
		return nil // No rotation needed
	}

	// Sort by name ascending (older files have earlier timestamps in name)
	sort.Slice(yamlFiles, func(i, j int) bool {
		return yamlFiles[i].Name() < yamlFiles[j].Name()
	})

	// Create archive dir
	if err := os.MkdirAll(archiveDir, 0755); err != nil {
		return err
	}

	// Move oldest files to archive (at least 1 to make room for new file)
	toMove := len(yamlFiles) - w.maxPerDir + 1
	moved := 0
	for i := 0; i < toMove; i++ {
		oldPath := filepath.Join(dir, yamlFiles[i].Name())
		newPath := filepath.Join(archiveDir, yamlFiles[i].Name())
		if err := os.Rename(oldPath, newPath); err != nil {
			w.logger.Warn("failed to archive handoff",
				"path", oldPath,
				"error", err,
			)
		} else {
			w.logger.Debug("archived old handoff",
				"from", oldPath,
				"to", newPath,
			)
			moved++
		}
	}

	if moved > 0 {
		w.logger.Info("handoff rotation completed",
			"session", sessionName,
			"archived", moved,
		)
	}

	return nil
}

// sanitizeDescription converts a description to kebab-case for use in filenames.
// It lowercases, replaces spaces/underscores with hyphens, removes non-alphanumeric
// characters (except hyphens), collapses multiple hyphens, and limits length.
func sanitizeDescription(desc string) string {
	// Lowercase
	desc = strings.ToLower(desc)

	// Replace spaces/underscores with hyphens
	desc = strings.ReplaceAll(desc, " ", "-")
	desc = strings.ReplaceAll(desc, "_", "-")

	// Remove non-alphanumeric except hyphens
	var result strings.Builder
	for _, r := range desc {
		if (r >= 'a' && r <= 'z') || (r >= '0' && r <= '9') || r == '-' {
			result.WriteRune(r)
		}
	}
	desc = result.String()

	// Collapse multiple hyphens
	for strings.Contains(desc, "--") {
		desc = strings.ReplaceAll(desc, "--", "-")
	}

	// Trim hyphens from ends
	desc = strings.Trim(desc, "-")

	// Limit length
	if len(desc) > 50 {
		desc = desc[:50]
		// Don't leave trailing hyphen after truncation
		desc = strings.TrimRight(desc, "-")
	}

	return desc
}

// truncateLog truncates a string for logging purposes.
func truncateLog(s string, max int) string {
	if len(s) <= max {
		return s
	}
	if max <= 3 {
		return "" // Can't fit any content + "..."
	}
	return s[:max-3] + "..."
}

// Delete removes a specific handoff file.
// Use with caution - typically handoffs should be archived, not deleted.
func (w *Writer) Delete(path string) error {
	writeMu.Lock()
	defer writeMu.Unlock()

	// Verify path is within our base directory (safety check)
	absPath, err := filepath.Abs(path)
	if err != nil {
		return fmt.Errorf("invalid path: %w", err)
	}
	absBase, err := filepath.Abs(w.baseDir)
	if err != nil {
		return fmt.Errorf("invalid base dir: %w", err)
	}
	if !strings.HasPrefix(absPath, absBase) {
		return fmt.Errorf("path %s is not within handoff directory", path)
	}

	if err := os.Remove(path); err != nil {
		w.logger.Error("failed to delete handoff",
			"path", path,
			"error", err,
		)
		return fmt.Errorf("delete failed: %w", err)
	}

	w.logger.Info("handoff deleted", "path", path)
	return nil
}

// Archive moves a specific handoff to the .archive directory.
func (w *Writer) Archive(path string) error {
	writeMu.Lock()
	defer writeMu.Unlock()

	// Verify path is within our base directory
	absPath, err := filepath.Abs(path)
	if err != nil {
		return fmt.Errorf("invalid path: %w", err)
	}
	absBase, err := filepath.Abs(w.baseDir)
	if err != nil {
		return fmt.Errorf("invalid base dir: %w", err)
	}
	if !strings.HasPrefix(absPath, absBase) {
		return fmt.Errorf("path %s is not within handoff directory", path)
	}

	// Don't archive files already in .archive
	if strings.Contains(path, "/.archive/") {
		return fmt.Errorf("file is already archived")
	}

	dir := filepath.Dir(path)
	archiveDir := filepath.Join(dir, ".archive")

	// Ensure archive dir exists
	if err := os.MkdirAll(archiveDir, 0755); err != nil {
		return fmt.Errorf("create archive dir failed: %w", err)
	}

	newPath := filepath.Join(archiveDir, filepath.Base(path))
	if err := os.Rename(path, newPath); err != nil {
		w.logger.Error("failed to archive handoff",
			"from", path,
			"to", newPath,
			"error", err,
		)
		return fmt.Errorf("archive failed: %w", err)
	}

	w.logger.Info("handoff archived",
		"from", path,
		"to", newPath,
	)
	return nil
}

// CleanArchive removes archived handoffs older than the given duration.
func (w *Writer) CleanArchive(sessionName string, olderThan time.Duration) (int, error) {
	writeMu.Lock()
	defer writeMu.Unlock()

	if sessionName == "" {
		sessionName = "general"
	}

	archiveDir := filepath.Join(w.baseDir, sessionName, ".archive")
	entries, err := os.ReadDir(archiveDir)
	if err != nil {
		if os.IsNotExist(err) {
			return 0, nil // No archive dir, nothing to clean
		}
		return 0, err
	}

	cutoff := time.Now().Add(-olderThan)
	removed := 0

	for _, e := range entries {
		if e.IsDir() || !strings.HasSuffix(e.Name(), ".yaml") {
			continue
		}

		info, err := e.Info()
		if err != nil {
			continue
		}

		if info.ModTime().Before(cutoff) {
			path := filepath.Join(archiveDir, e.Name())
			if err := os.Remove(path); err != nil {
				w.logger.Warn("failed to remove old archived handoff",
					"path", path,
					"error", err,
				)
			} else {
				removed++
			}
		}
	}

	if removed > 0 {
		w.logger.Info("cleaned archive",
			"session", sessionName,
			"removed", removed,
			"older_than", olderThan,
		)
	}

	return removed, nil
}
