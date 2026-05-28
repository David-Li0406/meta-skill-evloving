//go:build unix

package alerts

import (
	"fmt"
	"syscall"
	"time"
)

// checkDiskSpace verifies available disk space (Unix implementation)
func (g *Generator) checkDiskSpace() (*Alert, error) {
	var stat syscall.Statfs_t

	// Check space on project directory if configured, otherwise root
	checkPath := "/"
	if g.config.ProjectsDir != "" {
		checkPath = g.config.ProjectsDir
	}

	err := syscall.Statfs(checkPath, &stat)
	if err != nil {
		// If project dir check fails (e.g. doesn't exist), fallback to root
		if checkPath != "/" {
			err = syscall.Statfs("/", &stat)
		}
		if err != nil {
			return nil, err
		}
	}

	// Calculate free space in GB
	// Convert to float64 directly to handle different field types across Unix variants
	// (Bavail is int64 on Linux/FreeBSD, uint64 on macOS)
	freeGB := float64(stat.Bavail) * float64(stat.Bsize) / (1024 * 1024 * 1024)

	if freeGB < g.config.DiskLowThresholdGB {
		severity := SeverityWarning
		if freeGB < 1.0 {
			severity = SeverityCritical
		}

		return &Alert{
			ID:       generateAlertID(AlertDiskLow, "", ""),
			Type:     AlertDiskLow,
			Severity: severity,
			Source:   "disk",
			Message:  fmt.Sprintf("Low disk space: %.1f GB remaining on %s", freeGB, checkPath),
			Context: map[string]interface{}{
				"free_gb":      freeGB,
				"threshold_gb": g.config.DiskLowThresholdGB,
				"path":         checkPath,
			},
			CreatedAt:  time.Now(),
			LastSeenAt: time.Now(),
			Count:      1,
		}, nil
	}

	return nil, nil
}
