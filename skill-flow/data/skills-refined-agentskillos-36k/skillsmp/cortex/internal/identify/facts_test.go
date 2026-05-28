package identify

import (
	"testing"
)

func TestFactTypeConstants(t *testing.T) {
	// Test that hard identifiers list is not empty
	if len(HardIdentifiers) == 0 {
		t.Error("HardIdentifiers list should not be empty")
	}

	// Test that specific hard identifiers are present
	expectedHard := []string{
		FactTypeEmailPersonal,
		FactTypePhoneMobile,
		FactTypeFullLegalName,
	}

	for _, expected := range expectedHard {
		found := false
		for _, hard := range HardIdentifiers {
			if hard == expected {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("Expected hard identifier %s not found in HardIdentifiers list", expected)
		}
	}
}

func TestSoftIdentifierWeights(t *testing.T) {
	// Test that soft identifier weights are defined
	if len(SoftIdentifierWeights) == 0 {
		t.Error("SoftIdentifierWeights should not be empty")
	}

	// Test that all weights are between 0 and 1
	for factType, weight := range SoftIdentifierWeights {
		if weight < 0 || weight > 1 {
			t.Errorf("Weight for %s should be between 0 and 1, got %f", factType, weight)
		}
	}

	// Test expected weights
	expectedWeights := map[string]float64{
		FactTypeEmployerCurrent: 0.20,
		FactTypeLocationCurrent: 0.15,
		FactTypeProfession:      0.15,
		FactTypeSpouseFirstName: 0.25,
		FactTypeSchoolAttended:  0.15,
		FactTypeBirthdate:       0.25,
	}

	for factType, expectedWeight := range expectedWeights {
		actualWeight, exists := SoftIdentifierWeights[factType]
		if !exists {
			t.Errorf("Expected soft identifier weight for %s not found", factType)
		} else if actualWeight != expectedWeight {
			t.Errorf("Weight for %s should be %f, got %f", factType, expectedWeight, actualWeight)
		}
	}
}

func TestIsHardIdentifierType(t *testing.T) {
	// Test hard identifier detection
	if !isHardIdentifierType(FactTypeEmailPersonal) {
		t.Error("email_personal should be detected as hard identifier")
	}
	if !isHardIdentifierType(FactTypePhoneMobile) {
		t.Error("phone_mobile should be detected as hard identifier")
	}
	if !isHardIdentifierType(FactTypeFullLegalName) {
		t.Error("full_legal_name should be detected as hard identifier")
	}

	// Test non-hard identifiers
	if isHardIdentifierType(FactTypeEmployerCurrent) {
		t.Error("employer_current should not be detected as hard identifier")
	}
	if isHardIdentifierType(FactTypeLocationCurrent) {
		t.Error("location_current should not be detected as hard identifier")
	}
}

func TestIsIdentifierType(t *testing.T) {
	// Test hard identifiers are also identifiers
	if !isIdentifierType(FactTypeEmailPersonal) {
		t.Error("email_personal should be identifier")
	}

	// Test soft identifiers
	if !isIdentifierType(FactTypeEmployerCurrent) {
		t.Error("employer_current should be identifier")
	}
	if !isIdentifierType(FactTypeSpouseFirstName) {
		t.Error("spouse_first_name should be identifier")
	}

	// Test non-identifiers (enrichment facts)
	if isIdentifierType("hobbies") {
		t.Error("hobbies should not be identifier")
	}
}

func TestSplitPersonIDs(t *testing.T) {
	tests := []struct {
		input    string
		expected []string
	}{
		{"", nil},
		{"id1", []string{"id1"}},
		{"id1,id2", []string{"id1", "id2"}},
		{"id1,id2,id3", []string{"id1", "id2", "id3"}},
	}

	for _, test := range tests {
		result := splitPersonIDs(test.input)
		if len(result) != len(test.expected) {
			t.Errorf("splitPersonIDs(%q) returned %d items, expected %d", test.input, len(result), len(test.expected))
			continue
		}
		for i := range result {
			if result[i] != test.expected[i] {
				t.Errorf("splitPersonIDs(%q)[%d] = %q, expected %q", test.input, i, result[i], test.expected[i])
			}
		}
	}
}

func TestBoolToInt(t *testing.T) {
	if boolToInt(true) != 1 {
		t.Error("boolToInt(true) should return 1")
	}
	if boolToInt(false) != 0 {
		t.Error("boolToInt(false) should return 0")
	}
}
