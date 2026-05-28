//go:build !unix

package alerts

// checkDiskSpace is a stub for non-Unix platforms (Windows, etc.)
// Disk space checking is not implemented on these platforms.
func (g *Generator) checkDiskSpace() (*Alert, error) {
	// Not implemented on non-Unix platforms
	return nil, nil
}
