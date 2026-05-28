// Package e2e contains end-to-end tests for NTM robot mode commands.
// robot_format_test.go validates --robot-format selection for JSON/TOON/auto.
//
// Bead: bd-1a6c4 - Task: E2E robot-format selection (json/toon/auto)
package e2e

import (
	"encoding/json"
	"fmt"
	"os/exec"
	"strings"
	"testing"
)

// runRobotFormatCmd executes an ntm robot command with a specific format.
func runRobotFormatCmd(t *testing.T, suite *TestSuite, format string, cmd string, args ...string) []byte {
	t.Helper()

	fullArgs := append([]string{fmt.Sprintf("--robot-format=%s", format)}, args...)
	command := exec.Command("ntm", fullArgs...)
	output, err := command.CombinedOutput()

	suite.Logger().Log("[E2E-ROBOT-FORMAT] format=%s cmd=%s bytes=%d", format, cmd, len(output))

	if err != nil {
		suite.Logger().Log("[E2E-ROBOT-FORMAT] error cmd=%s err=%v output=%s", cmd, err, string(output))
		t.Fatalf("[E2E-ROBOT-FORMAT] Command failed: %v", err)
	}

	return output
}

func parseJSONOrFail(t *testing.T, output []byte) map[string]interface{} {
	t.Helper()
	var parsed map[string]interface{}
	if err := json.Unmarshal(output, &parsed); err != nil {
		t.Fatalf("[E2E-ROBOT-FORMAT] JSON parse failed: %v output=%s", err, string(output))
	}
	return parsed
}

func TestE2E_RobotFormatSelection(t *testing.T) {
	CommonE2EPrerequisites(t)
	if !supportsRobotFormat(t) {
		t.Skip("ntm --robot-format not supported by current binary")
	}

	suite := NewTestSuite(t, "robot_format")
	defer suite.Teardown()

	if err := suite.Setup(); err != nil {
		t.Fatalf("[E2E-ROBOT-FORMAT] Setup failed: %v", err)
	}

	session := suite.Session()

	t.Run("status_json", func(t *testing.T) {
		output := runRobotFormatCmd(t, suite, "json", "robot-status", "--robot-status")
		parsed := parseJSONOrFail(t, output)

		if _, ok := parsed["sessions"]; !ok {
			t.Fatalf("[E2E-ROBOT-FORMAT] status JSON missing sessions: %v", parsed)
		}
	})

	t.Run("status_toon", func(t *testing.T) {
		output := runRobotFormatCmd(t, suite, "toon", "robot-status", "--robot-status")

		trimmed := strings.TrimSpace(string(output))
		if strings.HasPrefix(trimmed, "{") || strings.HasPrefix(trimmed, "[") {
			if json.Valid([]byte(trimmed)) {
				t.Fatalf("[E2E-ROBOT-FORMAT] status TOON should not be valid JSON, got: %s", string(output))
			}
		}
		if !strings.Contains(string(output), "sessions") {
			t.Fatalf("[E2E-ROBOT-FORMAT] status TOON missing sessions field: %s", string(output))
		}
	})

	t.Run("status_auto_defaults_json", func(t *testing.T) {
		output := runRobotFormatCmd(t, suite, "auto", "robot-status", "--robot-status")
		parseJSONOrFail(t, output)
		suite.Logger().Log("[E2E-ROBOT-FORMAT] fallback=%t reason=%s", true, "auto defaults to JSON")
	})

	t.Run("assign_json", func(t *testing.T) {
		output := runRobotFormatCmd(t, suite, "json", "robot-assign", fmt.Sprintf("--robot-assign=%s", session))
		parsed := parseJSONOrFail(t, output)

		if parsed["session"] != session {
			t.Fatalf("[E2E-ROBOT-FORMAT] assign JSON session mismatch: got=%v want=%s", parsed["session"], session)
		}
		if _, ok := parsed["strategy"]; !ok {
			t.Fatalf("[E2E-ROBOT-FORMAT] assign JSON missing strategy: %v", parsed)
		}
	})

	t.Run("assign_toon", func(t *testing.T) {
		output := runRobotFormatCmd(t, suite, "toon", "robot-assign", fmt.Sprintf("--robot-assign=%s", session))
		if !strings.Contains(string(output), "session:") {
			t.Fatalf("[E2E-ROBOT-FORMAT] assign TOON missing session: %s", string(output))
		}
		if !strings.Contains(string(output), "strategy:") {
			t.Fatalf("[E2E-ROBOT-FORMAT] assign TOON missing strategy: %s", string(output))
		}
	})

	t.Run("assign_auto_defaults_json", func(t *testing.T) {
		output := runRobotFormatCmd(t, suite, "auto", "robot-assign", fmt.Sprintf("--robot-assign=%s", session))
		parseJSONOrFail(t, output)
	})
}

func supportsRobotFormat(t *testing.T) bool {
	t.Helper()
	cmd := exec.Command("ntm", "--help")
	output, err := cmd.CombinedOutput()
	if err != nil {
		return false
	}
	return strings.Contains(string(output), "--robot-format")
}
