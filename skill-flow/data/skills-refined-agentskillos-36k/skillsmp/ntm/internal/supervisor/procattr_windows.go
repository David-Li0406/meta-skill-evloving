//go:build windows

package supervisor

import (
	"os"
	"os/exec"
)

// setSysProcAttr sets platform-specific process attributes for clean shutdown.
// On Windows, process groups work differently; this is a no-op placeholder.
func setSysProcAttr(cmd *exec.Cmd) {
	// Windows doesn't support Setpgid. Process management is handled differently.
	// For now, this is a no-op. Future enhancement could use CREATE_NEW_PROCESS_GROUP.
}

// terminateProcess attempts graceful shutdown, falling back to force kill.
// On Windows, os.Interrupt sends a Ctrl+C equivalent; fall back to Kill.
func terminateProcess(p *os.Process) {
	if err := p.Signal(os.Interrupt); err != nil {
		p.Kill()
	}
}
