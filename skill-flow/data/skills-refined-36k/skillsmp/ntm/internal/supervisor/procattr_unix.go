//go:build unix

package supervisor

import (
	"os"
	"os/exec"
	"syscall"
)

// setSysProcAttr sets platform-specific process attributes for clean shutdown.
// On Unix systems, this sets Setpgid to create a new process group.
func setSysProcAttr(cmd *exec.Cmd) {
	cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
}

// terminateProcess attempts graceful shutdown, falling back to force kill.
// On Unix, sends SIGTERM first, then SIGKILL if that fails.
func terminateProcess(p *os.Process) {
	if err := p.Signal(syscall.SIGTERM); err != nil {
		p.Kill()
	}
}
