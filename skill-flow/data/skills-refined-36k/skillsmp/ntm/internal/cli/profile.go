package cli

import (
	"os"

	"github.com/Dicklesworthstone/ntm/internal/profiler"
)

// profileStartup controls startup profiling
var profileStartup bool

// EnableProfilingIfRequested enables profiling if --profile-startup was set.
// Call this at the start of command execution.
func EnableProfilingIfRequested() {
	if profileStartup {
		profiler.Enable()
		profiler.StartWithPhase("cli_init", "startup").End()
	}
}

// ProfileConfigLoad profiles config loading if profiling is enabled.
// Returns a function to call when loading is complete.
func ProfileConfigLoad() func() {
	if !profileStartup {
		return func() {}
	}
	span := profiler.StartWithPhase("config_load", "startup")
	return span.End
}

// PrintProfilingIfEnabled prints profiling output if enabled.
// Call this at the end of command execution.
func PrintProfilingIfEnabled() {
	if !profileStartup {
		return
	}
	if jsonOutput {
		profiler.WriteJSON(os.Stdout)
	} else {
		profiler.WriteText(os.Stderr)
	}
}
