package cli

import (
	"testing"
)

func TestParsePersonaSpec(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    PersonaSpec
		wantErr bool
	}{
		{
			name:  "simple name",
			input: "architect",
			want:  PersonaSpec{Name: "architect", Count: 1},
		},
		{
			name:  "name with count",
			input: "implementer:2",
			want:  PersonaSpec{Name: "implementer", Count: 2},
		},
		{
			name:  "name with spaces",
			input: " reviewer ",
			want:  PersonaSpec{Name: "reviewer", Count: 1},
		},
		{
			name:  "count with spaces",
			input: "tester: 3 ",
			want:  PersonaSpec{Name: "tester", Count: 3},
		},
		{
			name:    "empty string",
			input:   "",
			wantErr: true,
		},
		{
			name:    "invalid count",
			input:   "architect:abc",
			wantErr: true,
		},
		{
			name:    "zero count",
			input:   "architect:0",
			wantErr: true,
		},
		{
			name:    "negative count",
			input:   "architect:-1",
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ParsePersonaSpec(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("ParsePersonaSpec(%q) error = %v, wantErr %v", tt.input, err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if got.Name != tt.want.Name {
					t.Errorf("ParsePersonaSpec(%q).Name = %v, want %v", tt.input, got.Name, tt.want.Name)
				}
				if got.Count != tt.want.Count {
					t.Errorf("ParsePersonaSpec(%q).Count = %v, want %v", tt.input, got.Count, tt.want.Count)
				}
			}
		})
	}
}

func TestPersonaSpecsString(t *testing.T) {
	tests := []struct {
		name  string
		specs PersonaSpecs
		want  string
	}{
		{
			name:  "empty",
			specs: PersonaSpecs{},
			want:  "",
		},
		{
			name: "single with count 1",
			specs: PersonaSpecs{
				{Name: "architect", Count: 1},
			},
			want: "architect",
		},
		{
			name: "single with count > 1",
			specs: PersonaSpecs{
				{Name: "implementer", Count: 2},
			},
			want: "implementer:2",
		},
		{
			name: "multiple",
			specs: PersonaSpecs{
				{Name: "architect", Count: 1},
				{Name: "implementer", Count: 2},
			},
			want: "architect,implementer:2",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.specs.String(); got != tt.want {
				t.Errorf("PersonaSpecs.String() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestPersonaSpecsSet(t *testing.T) {
	var specs PersonaSpecs

	// Add first spec
	if err := specs.Set("architect"); err != nil {
		t.Errorf("PersonaSpecs.Set(architect) unexpected error: %v", err)
	}
	if len(specs) != 1 {
		t.Errorf("after first Set, len = %d, want 1", len(specs))
	}

	// Add second spec
	if err := specs.Set("implementer:2"); err != nil {
		t.Errorf("PersonaSpecs.Set(implementer:2) unexpected error: %v", err)
	}
	if len(specs) != 2 {
		t.Errorf("after second Set, len = %d, want 2", len(specs))
	}

	// Verify specs
	if specs[0].Name != "architect" || specs[0].Count != 1 {
		t.Errorf("specs[0] = %+v, want {architect, 1}", specs[0])
	}
	if specs[1].Name != "implementer" || specs[1].Count != 2 {
		t.Errorf("specs[1] = %+v, want {implementer, 2}", specs[1])
	}
}

func TestPersonaSpecsTotalCount(t *testing.T) {
	tests := []struct {
		name  string
		specs PersonaSpecs
		want  int
	}{
		{
			name:  "empty",
			specs: PersonaSpecs{},
			want:  0,
		},
		{
			name: "single",
			specs: PersonaSpecs{
				{Name: "architect", Count: 1},
			},
			want: 1,
		},
		{
			name: "multiple",
			specs: PersonaSpecs{
				{Name: "architect", Count: 1},
				{Name: "implementer", Count: 2},
				{Name: "reviewer", Count: 3},
			},
			want: 6,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.specs.TotalCount(); got != tt.want {
				t.Errorf("PersonaSpecs.TotalCount() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestPersonaSpecsType(t *testing.T) {
	var specs PersonaSpecs
	if got := specs.Type(); got != "name[:count]" {
		t.Errorf("PersonaSpecs.Type() = %v, want name[:count]", got)
	}
}
