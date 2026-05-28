package policy

import (
	"testing"
)

func TestDefaultPolicy(t *testing.T) {
	p := DefaultPolicy()

	blocked, approval, allowed := p.Stats()
	if blocked == 0 {
		t.Error("expected blocked rules in default policy")
	}
	if approval == 0 {
		t.Error("expected approval rules in default policy")
	}
	if allowed == 0 {
		t.Error("expected allowed rules in default policy")
	}
}

func TestCheck_Blocked(t *testing.T) {
	p := DefaultPolicy()

	cases := []struct {
		name    string
		command string
		blocked bool
	}{
		{"git reset --hard", "git reset --hard HEAD", true},
		{"git reset --hard with spaces", "git   reset   --hard", true},
		{"git clean -fd", "git clean -fd", true},
		{"git push --force", "git push --force", true},
		{"git push -f end", "git push origin main -f", true},
		{"git push -f space", "git push -f origin main", true},
		{"rm -rf /", "rm -rf /", true},
		{"rm -rf ~", "rm -rf ~", true},
		{"git branch -D", "git branch -D feature", true},
		{"git stash drop", "git stash drop", true},
		{"git stash clear", "git stash clear", true},

		// Not blocked
		{"git status", "git status", false},
		{"git add", "git add .", false},
		{"git commit", "git commit -m 'test'", false},
		{"git push", "git push origin main", false},
		{"rm file", "rm file.txt", false},
		{"git reset --soft", "git reset --soft HEAD~1", false},
		// force-with-lease is explicitly allowed (takes precedence)
		{"git push --force-with-lease", "git push --force-with-lease", false},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			if got := p.IsBlocked(tc.command); got != tc.blocked {
				t.Errorf("IsBlocked(%q) = %v, want %v", tc.command, got, tc.blocked)
			}
		})
	}
}

func TestCheck_ApprovalRequired(t *testing.T) {
	p := DefaultPolicy()

	cases := []struct {
		name     string
		command  string
		approval bool
	}{
		{"git rebase -i", "git rebase -i HEAD~3", true},
		{"git commit --amend", "git commit --amend", true},
		{"rm -rf (general)", "rm -rf node_modules", true},

		// Not requiring approval
		{"git status", "git status", false},
		{"git add", "git add .", false},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			if got := p.NeedsApproval(tc.command); got != tc.approval {
				t.Errorf("NeedsApproval(%q) = %v, want %v", tc.command, got, tc.approval)
			}
		})
	}
}

func TestCheck_Allowed(t *testing.T) {
	p := DefaultPolicy()

	cases := []struct {
		name    string
		command string
		action  Action
	}{
		{"force-with-lease allowed", "git push --force-with-lease origin main", ActionAllow},
		{"soft reset allowed", "git reset --soft HEAD~1", ActionAllow},
		{"mixed reset allowed", "git reset HEAD~1", ActionAllow},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			match := p.Check(tc.command)
			if match == nil {
				t.Errorf("Check(%q) = nil, want Action=%v", tc.command, tc.action)
				return
			}
			if match.Action != tc.action {
				t.Errorf("Check(%q).Action = %v, want %v", tc.command, match.Action, tc.action)
			}
		})
	}
}

func TestCheck_Precedence(t *testing.T) {
	// Allowed should take precedence over blocked
	p := DefaultPolicy()

	// git push --force-with-lease contains --force which could match block pattern
	// but should be allowed due to explicit allow rule
	match := p.Check("git push --force-with-lease")
	if match == nil {
		t.Error("expected match for git push --force-with-lease")
		return
	}
	if match.Action != ActionAllow {
		t.Errorf("expected ActionAllow, got %v", match.Action)
	}
}

func TestCheck_NoMatch(t *testing.T) {
	p := DefaultPolicy()

	match := p.Check("ls -la")
	if match != nil {
		t.Errorf("Check('ls -la') = %v, want nil", match)
	}
}

func TestAutomationConfig(t *testing.T) {
	p := DefaultPolicy()

	// Test default automation settings
	if !p.Automation.AutoCommit {
		t.Error("expected AutoCommit to be true by default")
	}
	if p.Automation.AutoPush {
		t.Error("expected AutoPush to be false by default")
	}
	if p.Automation.ForceRelease != "approval" {
		t.Errorf("expected ForceRelease to be 'approval', got %q", p.Automation.ForceRelease)
	}
}

func TestAutomationEnabled(t *testing.T) {
	p := DefaultPolicy()

	if !p.AutomationEnabled("auto_commit") {
		t.Error("expected auto_commit to be enabled")
	}
	if p.AutomationEnabled("auto_push") {
		t.Error("expected auto_push to be disabled")
	}
	if p.AutomationEnabled("unknown_feature") {
		t.Error("expected unknown feature to be disabled")
	}
}

func TestForceReleasePolicy(t *testing.T) {
	p := DefaultPolicy()

	// Default should be "approval"
	if got := p.ForceReleasePolicy(); got != "approval" {
		t.Errorf("ForceReleasePolicy() = %q, want 'approval'", got)
	}

	// Test with empty value
	p.Automation.ForceRelease = ""
	if got := p.ForceReleasePolicy(); got != "approval" {
		t.Errorf("ForceReleasePolicy() with empty = %q, want 'approval'", got)
	}

	// Test explicit values
	for _, val := range []string{"never", "approval", "auto"} {
		p.Automation.ForceRelease = val
		if got := p.ForceReleasePolicy(); got != val {
			t.Errorf("ForceReleasePolicy() = %q, want %q", got, val)
		}
	}
}

func TestNeedsSLBApproval(t *testing.T) {
	p := DefaultPolicy()

	// force_release rule has SLB=true in default policy
	if !p.NeedsSLBApproval("force_release lock-123") {
		t.Error("expected force_release to require SLB approval")
	}

	// Regular commands don't need SLB
	if p.NeedsSLBApproval("git commit --amend") {
		t.Error("git commit --amend should not require SLB approval")
	}

	// Unmatched commands don't need SLB
	if p.NeedsSLBApproval("ls -la") {
		t.Error("ls -la should not require SLB approval")
	}
}

func TestMatchSLBFlag(t *testing.T) {
	p := DefaultPolicy()

	match := p.Check("force_release lock-123")
	if match == nil {
		t.Fatal("expected match for force_release")
	}
	if !match.SLB {
		t.Error("expected SLB flag to be true for force_release match")
	}

	// Non-SLB rule should have SLB=false
	match = p.Check("git commit --amend")
	if match == nil {
		t.Fatal("expected match for git commit --amend")
	}
	if match.SLB {
		t.Error("expected SLB flag to be false for git commit --amend")
	}
}

func TestValidate(t *testing.T) {
	cases := []struct {
		name    string
		policy  func() *Policy
		wantErr bool
	}{
		{
			name: "default policy is valid",
			policy: func() *Policy {
				return DefaultPolicy()
			},
			wantErr: false,
		},
		{
			name: "invalid force_release value",
			policy: func() *Policy {
				p := DefaultPolicy()
				p.Automation.ForceRelease = "invalid"
				return p
			},
			wantErr: true,
		},
		{
			name: "zero version is corrected",
			policy: func() *Policy {
				p := DefaultPolicy()
				p.Version = 0
				return p
			},
			wantErr: false, // Should not error, just default to 1
		},
		{
			name: "valid force_release values",
			policy: func() *Policy {
				p := DefaultPolicy()
				p.Automation.ForceRelease = "never"
				return p
			},
			wantErr: false,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			p := tc.policy()
			err := p.Validate()
			if (err != nil) != tc.wantErr {
				t.Errorf("Validate() error = %v, wantErr %v", err, tc.wantErr)
			}
		})
	}
}

func TestPolicyVersion(t *testing.T) {
	p := DefaultPolicy()
	if p.Version != 1 {
		t.Errorf("expected Version to be 1, got %d", p.Version)
	}
}
