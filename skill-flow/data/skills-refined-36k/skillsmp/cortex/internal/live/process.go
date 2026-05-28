package live

import (
	"context"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"syscall"
	"time"
)

type UpstreamSpec struct {
	Name                   string
	Command                string
	Args                   []string
	Env                    []string
	Dir                    string
	PIDFile                string
	RestartBackoff         time.Duration
	MaxBackoff             time.Duration
	AlreadyRunningExitCode int
	ExternalCheckInterval  time.Duration
}

func ensureUpstream(ctx context.Context, spec UpstreamSpec, logf func(format string, args ...any), onError func(error)) {
	if spec.Command == "" {
		return
	}
	if logf == nil {
		logf = func(string, ...any) {}
	}
	if onError == nil {
		onError = func(error) {}
	}

	backoff := spec.RestartBackoff
	if backoff <= 0 {
		backoff = 3 * time.Second
	}
	maxBackoff := spec.MaxBackoff
	if maxBackoff <= 0 {
		maxBackoff = 30 * time.Second
	}
	checkInterval := spec.ExternalCheckInterval
	if checkInterval <= 0 {
		checkInterval = 30 * time.Second
	}

	go func() {
		for {
			if ctx.Err() != nil {
				return
			}

			if spec.PIDFile != "" {
				if pid, running := checkExistingPID(spec.PIDFile); running {
					logf("upstream %s already running (pid %d); rechecking in %s", spec.Name, pid, checkInterval)
					onError(nil)
					select {
					case <-time.After(checkInterval):
					case <-ctx.Done():
						return
					}
					backoff = spec.RestartBackoff
					continue
				}
			}

			cmd := exec.CommandContext(ctx, spec.Command, spec.Args...)
			if spec.Dir != "" {
				cmd.Dir = spec.Dir
			}
			if len(spec.Env) > 0 {
				cmd.Env = append(os.Environ(), spec.Env...)
			}
			cmd.Stdout = os.Stdout
			cmd.Stderr = os.Stderr

			if err := cmd.Start(); err != nil {
				onError(err)
				logf("upstream %s failed to start: %v", spec.Name, err)
				select {
				case <-time.After(backoff):
				case <-ctx.Done():
					return
				}
				backoff = nextBackoff(backoff, maxBackoff)
				continue
			}
			if spec.PIDFile != "" && cmd.Process != nil {
				if err := writePIDFileWithPID(spec.PIDFile, cmd.Process.Pid); err != nil {
					logf("failed to write pid file for %s: %v", spec.Name, err)
				}
			}
			onError(nil)

			err := cmd.Wait()
			if spec.PIDFile != "" && cmd.Process != nil {
				_ = removePIDFileIfMatches(spec.PIDFile, cmd.Process.Pid)
			}
			if ctx.Err() != nil {
				return
			}

			if err == nil {
				logf("upstream %s stopped (exit 0); restarting in %s", spec.Name, backoff)
				onError(fmt.Errorf("upstream %s stopped", spec.Name))
			} else if exitCode := exitCodeFromErr(err); exitCode == spec.AlreadyRunningExitCode {
				logf("upstream %s already running; rechecking in %s", spec.Name, checkInterval)
				onError(nil)
				select {
				case <-time.After(checkInterval):
				case <-ctx.Done():
					return
				}
				backoff = spec.RestartBackoff
				continue
			} else if errors.Is(err, context.Canceled) {
				return
			} else {
				logf("upstream %s exited: %v (restarting in %s)", spec.Name, err, backoff)
				onError(err)
			}

			select {
			case <-time.After(backoff):
			case <-ctx.Done():
				return
			}
			backoff = nextBackoff(backoff, maxBackoff)
		}
	}()
}

func exitCodeFromErr(err error) int {
	var exitErr *exec.ExitError
	if errors.As(err, &exitErr) {
		return exitErr.ExitCode()
	}
	return -1
}

func nextBackoff(current, max time.Duration) time.Duration {
	next := current * 2
	if next > max {
		return max
	}
	return next
}

func checkExistingPID(path string) (int, bool) {
	data, err := os.ReadFile(path)
	if err != nil {
		return 0, false
	}
	pid, err := strconv.Atoi(strings.TrimSpace(string(data)))
	if err != nil || pid <= 0 {
		return 0, false
	}
	if processRunning(pid) {
		return pid, true
	}
	_ = os.Remove(path)
	return pid, false
}

func writePIDFileWithPID(path string, pid int) error {
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		return fmt.Errorf("failed to create pid dir: %w", err)
	}
	if pid <= 0 {
		pid = os.Getpid()
	}
	data := []byte(fmt.Sprintf("%d", pid))
	if err := os.WriteFile(path, data, 0644); err != nil {
		return fmt.Errorf("failed to write pid file: %w", err)
	}
	return nil
}

func removePIDFileIfMatches(path string, pid int) error {
	if pid <= 0 {
		return os.Remove(path)
	}
	data, err := os.ReadFile(path)
	if err != nil {
		return err
	}
	existing, err := strconv.Atoi(strings.TrimSpace(string(data)))
	if err != nil || existing != pid {
		return nil
	}
	return os.Remove(path)
}

func processRunning(pid int) bool {
	if pid <= 0 {
		return false
	}
	proc, err := os.FindProcess(pid)
	if err != nil {
		return false
	}
	if err := proc.Signal(syscall.Signal(0)); err != nil {
		return false
	}
	return true
}
