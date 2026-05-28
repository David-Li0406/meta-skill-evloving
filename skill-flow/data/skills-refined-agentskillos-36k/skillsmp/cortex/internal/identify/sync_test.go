package identify

import (
	"testing"
)

func TestFacetToFactMapping(t *testing.T) {
	// Verify all expected mappings exist
	expectedMappings := []struct {
		facetType string
		category  string
		factType  string
	}{
		{"pii_email_personal", CategoryContactInfo, FactTypeEmailPersonal},
		{"pii_email_work", CategoryContactInfo, FactTypeEmailWork},
		{"pii_phone_mobile", CategoryContactInfo, FactTypePhoneMobile},
		{"pii_full_legal_name", CategoryCoreIdentity, FactTypeFullLegalName},
		{"pii_employer_current", CategoryProfessional, FactTypeEmployerCurrent},
		{"pii_business_owned", CategoryProfessional, FactTypeBusinessOwned},
		{"pii_ssn", CategoryGovernmentID, FactTypeSSN},
	}

	for _, expected := range expectedMappings {
		mapping, ok := FacetToFactMapping[expected.facetType]
		if !ok {
			t.Errorf("missing mapping for %s", expected.facetType)
			continue
		}
		if mapping.Category != expected.category {
			t.Errorf("wrong category for %s: got %s, want %s", expected.facetType, mapping.Category, expected.category)
		}
		if mapping.FactType != expected.factType {
			t.Errorf("wrong factType for %s: got %s, want %s", expected.facetType, mapping.FactType, expected.factType)
		}
	}
}

func TestIsSensitiveFactType(t *testing.T) {
	tests := []struct {
		factType  string
		sensitive bool
	}{
		{FactTypeSSN, true},
		{FactTypePassportNumber, true},
		{FactTypeDriversLicense, true},
		{FactTypeEmailPersonal, false},
		{FactTypePhoneMobile, false},
		{FactTypeFullLegalName, false},
		{FactTypeEmployerCurrent, false},
	}

	for _, tt := range tests {
		result := isSensitiveFactType(tt.factType)
		if result != tt.sensitive {
			t.Errorf("isSensitiveFactType(%s) = %v, want %v", tt.factType, result, tt.sensitive)
		}
	}
}

func TestMapFactKey(t *testing.T) {
	tests := []struct {
		input  string
		output string
	}{
		{"full_legal_name", FactTypeFullLegalName},
		{"given_name", FactTypeGivenName},
		{"email_personal", FactTypeEmailPersonal},
		{"phone_mobile", FactTypePhoneMobile},
		{"employer_current", FactTypeEmployerCurrent},
		{"business_owned", FactTypeBusinessOwned},
		{"date_of_birth", FactTypeBirthdate},
		{"spouse", FactTypeSpouseFirstName},
		{"unknown_key", "unknown_key"}, // Unmapped keys pass through
	}

	for _, tt := range tests {
		result := mapFactKey(tt.input)
		if result != tt.output {
			t.Errorf("mapFactKey(%s) = %s, want %s", tt.input, result, tt.output)
		}
	}
}

func TestMapCategory(t *testing.T) {
	tests := []struct {
		input  string
		output string
	}{
		{"core_identity", CategoryCoreIdentity},
		{"contact_information", CategoryContactInfo},
		{"professional", CategoryProfessional},
		{"relationships", CategoryRelationships},
		{"government_legal_ids", CategoryGovernmentID},
		{"unknown_category", "unknown_category"}, // Unmapped categories pass through
	}

	for _, tt := range tests {
		result := mapCategory(tt.input)
		if result != tt.output {
			t.Errorf("mapCategory(%s) = %s, want %s", tt.input, result, tt.output)
		}
	}
}
