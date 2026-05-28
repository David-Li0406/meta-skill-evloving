package pipeline

import (
	"testing"
	"time"
)

func TestDuration_UnmarshalText(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name    string
		input   string
		want    time.Duration
		wantErr bool
	}{
		{
			name:  "seconds",
			input: "30s",
			want:  30 * time.Second,
		},
		{
			name:  "minutes",
			input: "5m",
			want:  5 * time.Minute,
		},
		{
			name:  "hours",
			input: "2h",
			want:  2 * time.Hour,
		},
		{
			name:  "combined",
			input: "1h30m45s",
			want:  1*time.Hour + 30*time.Minute + 45*time.Second,
		},
		{
			name:  "milliseconds",
			input: "500ms",
			want:  500 * time.Millisecond,
		},
		{
			name:  "zero",
			input: "0s",
			want:  0,
		},
		{
			name:    "invalid format",
			input:   "invalid",
			wantErr: true,
		},
		{
			name:    "missing unit",
			input:   "30",
			wantErr: true,
		},
		{
			name:    "empty string",
			input:   "",
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			var d Duration
			err := d.UnmarshalText([]byte(tt.input))
			if tt.wantErr {
				if err == nil {
					t.Errorf("UnmarshalText(%q) expected error, got nil", tt.input)
				}
				return
			}
			if err != nil {
				t.Errorf("UnmarshalText(%q) unexpected error: %v", tt.input, err)
				return
			}
			if d.Duration != tt.want {
				t.Errorf("UnmarshalText(%q) = %v, want %v", tt.input, d.Duration, tt.want)
			}
		})
	}
}

func TestDuration_MarshalText(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name string
		d    Duration
		want string
	}{
		{
			name: "seconds",
			d:    Duration{Duration: 30 * time.Second},
			want: "30s",
		},
		{
			name: "minutes",
			d:    Duration{Duration: 5 * time.Minute},
			want: "5m0s",
		},
		{
			name: "hours",
			d:    Duration{Duration: 2 * time.Hour},
			want: "2h0m0s",
		},
		{
			name: "combined",
			d:    Duration{Duration: 1*time.Hour + 30*time.Minute + 45*time.Second},
			want: "1h30m45s",
		},
		{
			name: "zero",
			d:    Duration{Duration: 0},
			want: "0s",
		},
		{
			name: "milliseconds",
			d:    Duration{Duration: 500 * time.Millisecond},
			want: "500ms",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			got, err := tt.d.MarshalText()
			if err != nil {
				t.Errorf("MarshalText() unexpected error: %v", err)
				return
			}
			if string(got) != tt.want {
				t.Errorf("MarshalText() = %q, want %q", string(got), tt.want)
			}
		})
	}
}

func TestDuration_RoundTrip(t *testing.T) {
	t.Parallel()

	durations := []time.Duration{
		0,
		time.Second,
		5 * time.Minute,
		2*time.Hour + 30*time.Minute,
		time.Hour,
	}

	for _, original := range durations {
		d := Duration{Duration: original}
		marshaled, err := d.MarshalText()
		if err != nil {
			t.Errorf("MarshalText(%v) unexpected error: %v", original, err)
			continue
		}

		var unmarshaled Duration
		if err := unmarshaled.UnmarshalText(marshaled); err != nil {
			t.Errorf("UnmarshalText(%q) unexpected error: %v", string(marshaled), err)
			continue
		}

		if unmarshaled.Duration != original {
			t.Errorf("RoundTrip(%v) = %v, want %v", original, unmarshaled.Duration, original)
		}
	}
}

func TestOutputParse_UnmarshalText(t *testing.T) {
	t.Parallel()

	tests := []struct {
		name  string
		input string
		want  string
	}{
		{
			name:  "json",
			input: "json",
			want:  "json",
		},
		{
			name:  "yaml",
			input: "yaml",
			want:  "yaml",
		},
		{
			name:  "lines",
			input: "lines",
			want:  "lines",
		},
		{
			name:  "first_line",
			input: "first_line",
			want:  "first_line",
		},
		{
			name:  "regex",
			input: "regex",
			want:  "regex",
		},
		{
			name:  "none",
			input: "none",
			want:  "none",
		},
		{
			name:  "empty",
			input: "",
			want:  "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			var o OutputParse
			err := o.UnmarshalText([]byte(tt.input))
			if err != nil {
				t.Errorf("UnmarshalText(%q) unexpected error: %v", tt.input, err)
				return
			}
			if o.Type != tt.want {
				t.Errorf("UnmarshalText(%q).Type = %q, want %q", tt.input, o.Type, tt.want)
			}
		})
	}
}

func TestDefaultStepTimeout(t *testing.T) {
	t.Parallel()

	d := DefaultStepTimeout()
	expected := 5 * time.Minute

	if d.Duration != expected {
		t.Errorf("DefaultStepTimeout() = %v, want %v", d.Duration, expected)
	}
}

func TestDefaultWorkflowSettings(t *testing.T) {
	t.Parallel()

	s := DefaultWorkflowSettings()

	if s.Timeout.Duration != 30*time.Minute {
		t.Errorf("DefaultWorkflowSettings().Timeout = %v, want 30m", s.Timeout.Duration)
	}

	if s.OnError != ErrorActionFail {
		t.Errorf("DefaultWorkflowSettings().OnError = %q, want %q", s.OnError, ErrorActionFail)
	}

	if s.NotifyOnComplete {
		t.Error("DefaultWorkflowSettings().NotifyOnComplete = true, want false")
	}

	if !s.NotifyOnError {
		t.Error("DefaultWorkflowSettings().NotifyOnError = false, want true")
	}
}
