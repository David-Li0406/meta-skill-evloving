package watcher

import (
	"testing"
	"time"
)

func TestFileConflict_TimeRemaining(t *testing.T) {
	tests := []struct {
		name      string
		expiresAt *time.Time
		wantZero  bool
	}{
		{
			name:      "nil expires at returns zero",
			expiresAt: nil,
			wantZero:  true,
		},
		{
			name:      "expired returns zero",
			expiresAt: timePtr(time.Now().Add(-1 * time.Hour)),
			wantZero:  true,
		},
		{
			name:      "future expires at returns positive",
			expiresAt: timePtr(time.Now().Add(1 * time.Hour)),
			wantZero:  false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			fc := FileConflict{
				ExpiresAt: tt.expiresAt,
			}
			remaining := fc.TimeRemaining()
			if tt.wantZero && remaining != 0 {
				t.Errorf("TimeRemaining() = %v, want 0", remaining)
			}
			if !tt.wantZero && remaining <= 0 {
				t.Errorf("TimeRemaining() = %v, want positive duration", remaining)
			}
		})
	}
}

func TestFileConflict_TimeSinceReserved(t *testing.T) {
	tests := []struct {
		name          string
		reservedSince *time.Time
		wantZero      bool
	}{
		{
			name:          "nil reserved since returns zero",
			reservedSince: nil,
			wantZero:      true,
		},
		{
			name:          "past time returns positive",
			reservedSince: timePtr(time.Now().Add(-1 * time.Hour)),
			wantZero:      false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			fc := FileConflict{
				ReservedSince: tt.reservedSince,
			}
			since := fc.TimeSinceReserved()
			if tt.wantZero && since != 0 {
				t.Errorf("TimeSinceReserved() = %v, want 0", since)
			}
			if !tt.wantZero && since <= 0 {
				t.Errorf("TimeSinceReserved() = %v, want positive duration", since)
			}
		})
	}
}

func TestFileConflict_IsExpired(t *testing.T) {
	tests := []struct {
		name      string
		expiresAt *time.Time
		want      bool
	}{
		{
			name:      "nil expires at not expired",
			expiresAt: nil,
			want:      false,
		},
		{
			name:      "past time is expired",
			expiresAt: timePtr(time.Now().Add(-1 * time.Hour)),
			want:      true,
		},
		{
			name:      "future time not expired",
			expiresAt: timePtr(time.Now().Add(1 * time.Hour)),
			want:      false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			fc := FileConflict{
				ExpiresAt: tt.expiresAt,
			}
			if got := fc.IsExpired(); got != tt.want {
				t.Errorf("IsExpired() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestConflictAction_String(t *testing.T) {
	tests := []struct {
		action ConflictAction
		want   string
	}{
		{ConflictActionWait, "wait"},
		{ConflictActionRequest, "request"},
		{ConflictActionForce, "force"},
		{ConflictActionDismiss, "dismiss"},
		{ConflictAction(99), "unknown"},
	}

	for _, tt := range tests {
		t.Run(tt.want, func(t *testing.T) {
			if got := tt.action.String(); got != tt.want {
				t.Errorf("String() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestFileConflictCallback(t *testing.T) {
	// Test that the callback type is correctly defined
	var called bool
	var receivedConflict FileConflict

	cb := ConflictCallback(func(conflict FileConflict) {
		called = true
		receivedConflict = conflict
	})

	testConflict := FileConflict{
		Path:           "/test/file.go",
		RequestorAgent: "TestAgent",
		Holders:        []string{"HolderAgent"},
		DetectedAt:     time.Now(),
	}

	cb(testConflict)

	if !called {
		t.Error("Callback was not called")
	}
	if receivedConflict.Path != testConflict.Path {
		t.Errorf("Received conflict path = %v, want %v", receivedConflict.Path, testConflict.Path)
	}
}

// timePtr returns a pointer to the given time value.
func timePtr(t time.Time) *time.Time {
	return &t
}
