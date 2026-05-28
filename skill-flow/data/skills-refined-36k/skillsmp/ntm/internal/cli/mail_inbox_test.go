package cli

import (
	"bytes"
	"context"
	"errors"
	"strings"
	"testing"
	"time"

	"github.com/spf13/cobra"

	"github.com/Dicklesworthstone/ntm/internal/agentmail"
)

// MockMailClient implements MailClient interface for testing
type MockMailClient struct {
	Available     bool
	ProjKey       string
	Agents        []agentmail.Agent
	Inboxes       map[string][]agentmail.InboxMessage
	ListAgentsErr error
	FetchInboxErr error
}

func (m *MockMailClient) IsAvailable() bool {
	return m.Available
}

func (m *MockMailClient) ProjectKey() string {
	return m.ProjKey
}

func (m *MockMailClient) ListProjectAgents(ctx context.Context, projectKey string) ([]agentmail.Agent, error) {
	if m.ListAgentsErr != nil {
		return nil, m.ListAgentsErr
	}
	return m.Agents, nil
}

func (m *MockMailClient) FetchInbox(ctx context.Context, opts agentmail.FetchInboxOptions) ([]agentmail.InboxMessage, error) {
	if m.FetchInboxErr != nil {
		return nil, m.FetchInboxErr
	}
	msgs, ok := m.Inboxes[opts.AgentName]
	if !ok {
		return []agentmail.InboxMessage{}, nil
	}
	// Filter logic similar to real client (basic)
	var filtered []agentmail.InboxMessage
	count := 0
	for _, msg := range msgs {
		if opts.UrgentOnly && msg.Importance != "urgent" && msg.Importance != "high" {
			continue
		}
		filtered = append(filtered, msg)
		count++
		if opts.Limit > 0 && count >= opts.Limit {
			break
		}
	}
	return filtered, nil
}

func TestRunMailInbox(t *testing.T) {
	tests := []struct {
		name          string
		client        *MockMailClient
		session       string
		sessionAgents bool
		agentFilter   string
		urgent        bool
		wantErr       bool
		wantOutput    []string
	}{
		{
			name: "unavailable client",
			client: &MockMailClient{
				Available: false,
			},
			wantErr: true,
		},
		{
			name: "list agents error",
			client: &MockMailClient{
				Available:     true,
				ListAgentsErr: errors.New("failed to list agents"),
			},
			wantErr: true,
		},
		{
			name: "successful list empty inbox",
			client: &MockMailClient{
				Available: true,
				ProjKey:   "/test/project",
				Agents: []agentmail.Agent{
					{Name: "BlueLake"},
					{Name: "GreenCastle"},
				},
				Inboxes: map[string][]agentmail.InboxMessage{},
			},
			wantErr:    false,
			wantOutput: []string{"Inbox empty"},
		},
		{
			name: "successful list with messages",
			client: &MockMailClient{
				Available: true,
				ProjKey:   "/test/project",
				Agents: []agentmail.Agent{
					{Name: "BlueLake"},
				},
				Inboxes: map[string][]agentmail.InboxMessage{
					"BlueLake": {
						{ID: 1,
							Subject:    "Test Message",
							From:       "GreenCastle",
							CreatedTS:  time.Now(),
							Importance: "normal",
						},
					},
				},
			},
			wantErr: false,
			wantOutput: []string{
				"Project Inbox: cli",
				"Test Message",
				"GreenCastle → BlueLake",
			},
		},
		{
			name: "urgent filter",
			client: &MockMailClient{
				Available: true,
				ProjKey:   "/test/project",
				Agents: []agentmail.Agent{
					{Name: "BlueLake"},
				},
				Inboxes: map[string][]agentmail.InboxMessage{
					"BlueLake": {
						{ID: 1, Subject: "Normal Msg", Importance: "normal"},
						{ID: 2, Subject: "Urgent Msg", Importance: "urgent"},
					},
				},
			},
			urgent:  true,
			wantErr: false,
			wantOutput: []string{
				"Urgent Msg",
				"[URGENT]",
			},
		},
		{
			name: "agent filter",
			client: &MockMailClient{
				Available: true,
				ProjKey:   "/test/project",
				Agents: []agentmail.Agent{
					{Name: "BlueLake"},
					{Name: "RedStone"},
				},
				Inboxes: map[string][]agentmail.InboxMessage{
					"RedStone": {
						{ID: 1, Subject: "Msg for Red", From: "BlueLake"},
					},
					"BlueLake": {
						{ID: 2, Subject: "Msg for Blue", From: "GreenCastle"},
					},
				},
			},
			agentFilter: "RedStone", // Matches the RedStone inbox key above
			wantErr:     false,
			wantOutput: []string{
				"Msg for Red",
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			cmd := &cobra.Command{}
			var buf bytes.Buffer
			cmd.SetOut(&buf)

			// Reset global JSON output flag if needed, or mock it?
			// runMailInbox uses IsJSONOutput() which reads a global variable.
			// We assume text output for these tests.

			err := runMailInbox(cmd, tt.client, tt.session, tt.sessionAgents, tt.agentFilter, tt.urgent, 10, false)
			if (err != nil) != tt.wantErr {
				t.Errorf("runMailInbox() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if !tt.wantErr {
				output := buf.String()
				for _, want := range tt.wantOutput {
					if !strings.Contains(output, want) {
						t.Errorf("output missing %q, got:\n%s", want, output)
					}
				}
				// Verify urgent filter excluded non-urgent
				if tt.urgent && strings.Contains(output, "Normal Msg") {
					t.Error("output contained normal message when urgent filter applied")
				}
				// Verify agent filter - "Msg for Blue" should NOT be present
				if tt.agentFilter == "RedStone" && strings.Contains(output, "Msg for Blue") {
					t.Error("output contained message not matching agent filter")
				}
			}
		})
	}
}
