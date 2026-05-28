package memory

import "testing"

func TestDefaultEntityTypes(t *testing.T) {
	// Verify we have exactly 8 entity types
	if len(DefaultEntityTypes) != 8 {
		t.Errorf("expected 8 entity types, got %d", len(DefaultEntityTypes))
	}

	// Verify IDs are sequential from 0 to 7
	for i, et := range DefaultEntityTypes {
		if et.ID != i {
			t.Errorf("entity type at index %d has ID %d, expected %d", i, et.ID, i)
		}
	}

	// Verify expected types exist with correct IDs
	expectedTypes := []struct {
		id   int
		name string
	}{
		{0, "Entity"},
		{1, "Person"},
		{2, "Company"},
		{3, "Project"},
		{4, "Location"},
		{5, "Event"},
		{6, "Document"},
		{7, "Pet"},
	}

	for _, exp := range expectedTypes {
		et := DefaultEntityTypes[exp.id]
		if et.Name != exp.name {
			t.Errorf("entity type ID %d: expected name %q, got %q", exp.id, exp.name, et.Name)
		}
	}
}

func TestGetEntityTypeByID(t *testing.T) {
	tests := []struct {
		id       int
		wantName string
		wantNil  bool
	}{
		{0, "Entity", false},
		{1, "Person", false},
		{2, "Company", false},
		{3, "Project", false},
		{4, "Location", false},
		{5, "Event", false},
		{6, "Document", false},
		{7, "Pet", false},
		{-1, "", true},
		{8, "", true},
		{100, "", true},
	}

	for _, tt := range tests {
		t.Run(tt.wantName, func(t *testing.T) {
			got := GetEntityTypeByID(tt.id)
			if tt.wantNil {
				if got != nil {
					t.Errorf("GetEntityTypeByID(%d) = %v, want nil", tt.id, got)
				}
			} else {
				if got == nil {
					t.Errorf("GetEntityTypeByID(%d) = nil, want %q", tt.id, tt.wantName)
				} else if got.Name != tt.wantName {
					t.Errorf("GetEntityTypeByID(%d).Name = %q, want %q", tt.id, got.Name, tt.wantName)
				}
			}
		})
	}
}

func TestGetEntityTypeByName(t *testing.T) {
	tests := []struct {
		name   string
		wantID int
		wantNil bool
	}{
		{"Person", 1, false},
		{"person", 1, false}, // case-insensitive
		{"PERSON", 1, false}, // case-insensitive
		{"Company", 2, false},
		{"company", 2, false},
		{"Entity", 0, false},
		{"Pet", 7, false},
		{"Invalid", 0, true},
		{"", 0, true},
		{"PersonX", 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := GetEntityTypeByName(tt.name)
			if tt.wantNil {
				if got != nil {
					t.Errorf("GetEntityTypeByName(%q) = %v, want nil", tt.name, got)
				}
			} else {
				if got == nil {
					t.Errorf("GetEntityTypeByName(%q) = nil, want ID %d", tt.name, tt.wantID)
				} else if got.ID != tt.wantID {
					t.Errorf("GetEntityTypeByName(%q).ID = %d, want %d", tt.name, got.ID, tt.wantID)
				}
			}
		})
	}
}

func TestIsValidEntityTypeID(t *testing.T) {
	tests := []struct {
		id   int
		want bool
	}{
		{0, true},
		{1, true},
		{7, true},
		{-1, false},
		{8, false},
		{100, false},
	}

	for _, tt := range tests {
		if got := IsValidEntityTypeID(tt.id); got != tt.want {
			t.Errorf("IsValidEntityTypeID(%d) = %v, want %v", tt.id, got, tt.want)
		}
	}
}

func TestEntityTypeNames(t *testing.T) {
	names := EntityTypeNames()

	if len(names) != 8 {
		t.Errorf("expected 8 names, got %d", len(names))
	}

	expectedNames := []string{"Entity", "Person", "Company", "Project", "Location", "Event", "Document", "Pet"}
	for i, name := range names {
		if name != expectedNames[i] {
			t.Errorf("name at index %d: got %q, want %q", i, name, expectedNames[i])
		}
	}
}

func TestEntityTypeConstants(t *testing.T) {
	// Verify constants match the DefaultEntityTypes slice
	tests := []struct {
		constant int
		name     string
	}{
		{EntityTypeEntity, "Entity"},
		{EntityTypePerson, "Person"},
		{EntityTypeCompany, "Company"},
		{EntityTypeProject, "Project"},
		{EntityTypeLocation, "Location"},
		{EntityTypeEvent, "Event"},
		{EntityTypeDocument, "Document"},
		{EntityTypePet, "Pet"},
	}

	for _, tt := range tests {
		et := GetEntityTypeByID(tt.constant)
		if et == nil {
			t.Errorf("constant %d (%s) does not match any entity type", tt.constant, tt.name)
			continue
		}
		if et.Name != tt.name {
			t.Errorf("constant %d: expected name %q, got %q", tt.constant, tt.name, et.Name)
		}
	}
}
