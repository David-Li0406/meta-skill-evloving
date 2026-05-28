package scanner

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/Dicklesworthstone/ntm/internal/agentmail"
)

// NotifyScanResults sends scan results to relevant agents via Agent Mail.
func NotifyScanResults(ctx context.Context, result *ScanResult, projectKey string) error {
	client := agentmail.NewClient(agentmail.WithProjectKey(projectKey))
	if !client.IsAvailable() {
		return nil
	}

	// Ensure scanner identity is registered
	if err := ensureScannerRegistered(ctx, client, projectKey); err != nil {
		fmt.Fprintf(os.Stderr, "Warning: failed to register scanner agent: %v\n", err)
		// Continue anyway, maybe it exists?
	}

	// 1. Fetch active file reservations to target notifications
	reservations, err := client.ListReservations(ctx, projectKey, "", true)
	if err != nil {
		// Log error but continue with summary
		fmt.Fprintf(os.Stderr, "Warning: failed to fetch reservations: %v\n", err)
	}

	// Group findings by file
	findingsByFile := make(map[string][]Finding)
	for _, f := range result.Findings {
		findingsByFile[f.File] = append(findingsByFile[f.File], f)
	}

	// 2. Send targeted alerts to agents holding locks
	notifiedAgents := make(map[string]bool)
	for _, res := range reservations {
		var relevantFindings []Finding

		// Check all files with findings against reservation pattern
		for file, findings := range findingsByFile {
			matched, _ := filepath.Match(res.PathPattern, file)
			if matched {
				relevantFindings = append(relevantFindings, findings...)
			}
		}

		if len(relevantFindings) > 0 {
			// Send targeted message
			msg := buildTargetedMessage(relevantFindings, res.PathPattern)
			_, err := client.SendMessage(ctx, agentmail.SendMessageOptions{
				ProjectKey: projectKey,
				SenderName: "ntm_scanner",
				To:         []string{res.AgentName},
				Subject:    fmt.Sprintf("[Scan] %d issues in %s", len(relevantFindings), res.PathPattern),
				BodyMD:     msg,
				Importance: "high",
			})
			if err == nil {
				notifiedAgents[res.AgentName] = true
			}
		}
	}

	// 3. Send summary to all other registered agents (optional, maybe too noisy?)
	// Task says: "Scan Summary - After each scan, send digest to all active agents"
	// But we don't want to spam. Maybe only if critical issues found?

	if result.HasCritical() || result.HasWarning() {
		agents, err := client.ListProjectAgents(ctx, projectKey)
		if err == nil {
			var broadcastTo []string
			for _, a := range agents {
				// Don't send duplicate if already notified via targeted alert
				if !notifiedAgents[a.Name] && a.Name != "ntm_scanner" && a.Name != "HumanOverseer" {
					broadcastTo = append(broadcastTo, a.Name)
				}
			}

			if len(broadcastTo) > 0 {
				summaryMsg := buildSummaryMessage(result)
				client.SendMessage(ctx, agentmail.SendMessageOptions{
					ProjectKey: projectKey,
					SenderName: "ntm_scanner",
					To:         broadcastTo,
					Subject:    fmt.Sprintf("[Scan] Summary: %d critical, %d warnings", result.Totals.Critical, result.Totals.Warning),
					BodyMD:     summaryMsg,
					Importance: "normal",
				})
			}
		}
	}

	return nil
}

func buildTargetedMessage(findings []Finding, pattern string) string {
	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("Found %d issues in files matching `%s`:\n\n", len(findings), pattern))

	for i, f := range findings {
		if i >= 10 {
			sb.WriteString(fmt.Sprintf("\n...and %d more\n", len(findings)-10))
			break
		}
		icon := "⚠"
		if f.Severity == SeverityCritical {
			icon = "❌"
		}
		sb.WriteString(fmt.Sprintf("- %s **%s**: %s (`%s:%d`)\n", icon, f.RuleID, f.Message, f.File, f.Line))
	}

	sb.WriteString("Please review and fix these issues.")
	return sb.String()
}

func buildSummaryMessage(result *ScanResult) string {
	var sb strings.Builder
	sb.WriteString("## Scan Summary\n\n")
	sb.WriteString(fmt.Sprintf("- **Critical**: %d\n", result.Totals.Critical))
	sb.WriteString(fmt.Sprintf("- **Warnings**: %d\n", result.Totals.Warning))
	sb.WriteString(fmt.Sprintf("- **Info**: %d\n", result.Totals.Info))
	sb.WriteString(fmt.Sprintf("- **Files**: %d\n\n", result.Totals.Files))
	if len(result.Findings) > 0 {
		sb.WriteString("## Top Issues\n\n")
		// Show top 5 critical/warning
		count := 0
		for _, f := range result.Findings {
			if count >= 5 {
				break
			}
			if f.Severity == SeverityCritical || f.Severity == SeverityWarning {
				icon := "⚠"
				if f.Severity == SeverityCritical {
					icon = "❌"
				}
				sb.WriteString(fmt.Sprintf("- %s %s: %s (`%s`)\n", icon, f.RuleID, f.Message, f.File))
				count++
			}
		}
	}

	return sb.String()
}

func ensureScannerRegistered(ctx context.Context, client *agentmail.Client, projectKey string) error {
	_, err := client.RegisterAgent(ctx, agentmail.RegisterAgentOptions{
		ProjectKey:      projectKey,
		Name:            "ntm_scanner",
		Program:         "ntm",
		Model:           "scanner",
		TaskDescription: "Automated vulnerability scanner",
	})
	return err
}
