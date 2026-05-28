package robot

import (
	"fmt"
	"os"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/tmux"
	"github.com/Dicklesworthstone/ntm/internal/tokens"
)

// Output tracking state
var (
	outputStateMu sync.RWMutex
	paneStates    = make(map[string]*paneState)
)

type paneState struct {
	lastHash      string
	lastTS        time.Time
	lastLineCount int
}

// Rate limit patterns
var rateLimitPatterns = []*regexp.Regexp{
	regexp.MustCompile(`(?i)you've hit your limit`),
	regexp.MustCompile(`(?i)rate limit`),
	regexp.MustCompile(`(?i)too many requests`),
	regexp.MustCompile(`RESOURCE_EXHAUSTED`),
	regexp.MustCompile(`resets \d+[ap]m`),
}

func enrichAgentStatus(agent *Agent, sessionName, modelName string) {
	// 1. PID is already populated from tmux
	if agent.PID == 0 {
		return // Cannot do much without PID
	}

	// 2. Get Child PID

	childPID, err := getChildPID(agent.PID)
	if err == nil {
		agent.ChildPID = childPID
	} else {
		// Fallback: if no child, maybe the shell IS the process?
		// But usually agent is a child of the shell.
	}

	// 3. Process State
	targetPID := agent.ChildPID
	if targetPID == 0 {
		targetPID = agent.PID
	}
	state, stateName, err := getProcessState(targetPID)
	if err == nil {
		agent.ProcessState = state
		agent.ProcessStateName = stateName
	}

	// 4. Memory
	mem, err := getProcessMemoryMB(targetPID)
	if err == nil {
		agent.MemoryMB = mem
	}

	// 5. Output analysis
	// Capture output for rate limit detection, activity, and context usage
	// We use agent.Pane which is the pane ID (e.g. %3)
	captureFn := tmux.CaptureForStatusDetection
	if modelName != "" {
		captureFn = tmux.CaptureForFullContext
		agent.ContextModel = modelName
	}
	content, err := captureFn(agent.Pane)
	if err == nil {
		// Rate limit
		detected, match := detectRateLimit(content)
		agent.RateLimitDetected = detected
		agent.RateLimitMatch = match

		// Output activity
		lastOutputTS, linesDelta := updateActivity(agent.Pane, content)
		agent.LastOutputTS = lastOutputTS
		agent.OutputLinesSinceLast = linesDelta

		if !agent.LastOutputTS.IsZero() {
			agent.SecondsSinceOutput = int(time.Since(agent.LastOutputTS).Seconds())
		}

		if modelName != "" {
			usage := tokens.GetUsageInfo(content, modelName)
			if usage != nil {
				agent.ContextTokens = usage.EstimatedTokens
				agent.ContextLimit = usage.ContextLimit
				agent.ContextPercent = usage.UsagePercent
				agent.ContextModel = usage.Model
			}
		}
	}
}

func getChildPID(shellPID int) (int, error) {
	// Try /proc first (Linux)
	taskPath := fmt.Sprintf("/proc/%d/task/%d/children", shellPID, shellPID)
	data, err := os.ReadFile(taskPath)
	if err == nil {
		parts := strings.Fields(string(data))
		if len(parts) > 0 {
			return strconv.Atoi(parts[0])
		}
	}

	// Fallback to pgrep
	out, err := exec.Command("pgrep", "-P", strconv.Itoa(shellPID)).Output()
	if err == nil {
		lines := strings.Split(strings.TrimSpace(string(out)), "\n")
		if len(lines) > 0 {
			return strconv.Atoi(lines[0])
		}
	}

	return 0, fmt.Errorf("no child process found")
}

func getProcessState(pid int) (string, string, error) {
	data, err := os.ReadFile(fmt.Sprintf("/proc/%d/status", pid))
	if err != nil {
		return "", "", err
	}

	for _, line := range strings.Split(string(data), "\n") {
		if strings.HasPrefix(line, "State:") {
			// Format: "State:  S (sleeping)"
			parts := strings.Fields(line)
			if len(parts) >= 3 {
				code := parts[1]
				name := strings.Trim(parts[2], "()")
				return code, name, nil
			}
		}
	}
	return "unknown", "unknown", nil
}

func getProcessMemoryMB(pid int) (int, error) {
	data, err := os.ReadFile(fmt.Sprintf("/proc/%d/status", pid))
	if err != nil {
		return 0, err
	}

	for _, line := range strings.Split(string(data), "\n") {
		if strings.HasPrefix(line, "VmRSS:") {
			// Format: "VmRSS:    123456 kB"
			parts := strings.Fields(line)
			if len(parts) >= 2 {
				kb, _ := strconv.Atoi(parts[1])
				return kb / 1024, nil
			}
		}
	}
	return 0, nil
}

func detectRateLimit(content string) (bool, string) {
	for _, pattern := range rateLimitPatterns {
		if match := pattern.FindString(content); match != "" {
			return true, match
		}
	}
	return false, ""
}

func updateActivity(paneID, content string) (time.Time, int) {
	outputStateMu.Lock()
	defer outputStateMu.Unlock()

	currentLines := countNonEmptyLines(content)
	state, ok := paneStates[paneID]
	if !ok {
		state = &paneState{
			lastTS:        time.Now(), // Initialize with current time
			lastHash:      content,
			lastLineCount: currentLines,
		}
		paneStates[paneID] = state
		return state.lastTS, currentLines
	}

	linesDelta := currentLines - state.lastLineCount
	if linesDelta < 0 {
		// Buffer wrap or clear - treat as reset
		linesDelta = currentLines
	} else if linesDelta == 0 && state.lastHash != content {
		// Output changed but line count stayed flat (window shift). Signal activity.
		linesDelta = 1
	}

	if state.lastHash != content {
		state.lastTS = time.Now()
		state.lastHash = content
	}
	state.lastLineCount = currentLines

	return state.lastTS, linesDelta
}

func getLastOutput(paneID string) time.Time {
	outputStateMu.RLock()
	defer outputStateMu.RUnlock()
	if state, ok := paneStates[paneID]; ok {
		return state.lastTS
	}
	return time.Time{}
}
