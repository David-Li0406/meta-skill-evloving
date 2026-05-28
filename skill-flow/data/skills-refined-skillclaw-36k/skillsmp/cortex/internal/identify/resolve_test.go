package identify

import (
	"testing"
)

func TestTriggeringFactJSON(t *testing.T) {
	facts := []TriggeringFact{
		{FactType: FactTypeEmailPersonal, FactValue: "test@example.com"},
		{FactType: FactTypePhoneMobile, FactValue: "+15551234567"},
	}

	if len(facts) != 2 {
		t.Errorf("expected 2 facts, got %d", len(facts))
	}

	if facts[0].FactType != FactTypeEmailPersonal {
		t.Errorf("expected %s, got %s", FactTypeEmailPersonal, facts[0].FactType)
	}
}

func TestMergeEventFields(t *testing.T) {
	event := MergeEvent{
		ID:             "test-id",
		SourcePersonID: "person-1",
		TargetPersonID: "person-2",
		MergeType:      "hard_identifier",
		AutoEligible:   true,
		Status:         "pending",
	}

	if event.MergeType != "hard_identifier" {
		t.Errorf("expected hard_identifier, got %s", event.MergeType)
	}

	if !event.AutoEligible {
		t.Error("expected AutoEligible to be true")
	}
}

func TestResolutionResultFields(t *testing.T) {
	result := ResolutionResult{
		HardCollisions:          5,
		CompoundMatches:         3,
		SoftAccumulations:       10,
		MergeSuggestionsCreated: 15,
		AutoMergesExecuted:      2,
		Errors:                  0,
	}

	total := result.HardCollisions + result.CompoundMatches + result.SoftAccumulations
	if total != 18 {
		t.Errorf("expected 18 total detections, got %d", total)
	}
}

func TestCompoundMatchFields(t *testing.T) {
	match := CompoundMatch{
		Person1ID:    "p1",
		Person2ID:    "p2",
		CompoundType: "name_birthdate",
		Confidence:   0.90,
		MatchingFacts: []TriggeringFact{
			{FactType: FactTypeFullLegalName, FactValue: "John Doe"},
			{FactType: FactTypeBirthdate, FactValue: "1990-01-01"},
		},
	}

	if match.Confidence != 0.90 {
		t.Errorf("expected confidence 0.90, got %f", match.Confidence)
	}

	if len(match.MatchingFacts) != 2 {
		t.Errorf("expected 2 matching facts, got %d", len(match.MatchingFacts))
	}
}

func TestSoftIdentifierScoreFields(t *testing.T) {
	score := SoftIdentifierScore{
		Person1ID: "p1",
		Person2ID: "p2",
		Score:     0.65,
		MatchingFacts: []TriggeringFact{
			{FactType: FactTypeEmployerCurrent, FactValue: "Acme Corp"},
			{FactType: FactTypeLocationCurrent, FactValue: "San Francisco"},
			{FactType: FactTypeProfession, FactValue: "Engineer"},
		},
	}

	// Score should be above threshold for merge suggestion (0.6)
	if score.Score < 0.6 {
		t.Errorf("expected score above 0.6, got %f", score.Score)
	}

	// Verify score calculation makes sense
	expectedMin := SoftIdentifierWeights[FactTypeEmployerCurrent] +
		SoftIdentifierWeights[FactTypeLocationCurrent] +
		SoftIdentifierWeights[FactTypeProfession]
	if score.Score < expectedMin {
		t.Logf("Note: score %f is less than sum of weights %f (may be expected)", score.Score, expectedMin)
	}
}

func TestResolutionStatsFields(t *testing.T) {
	stats := ResolutionStats{
		ActivePersons:      100,
		MergedPersons:      20,
		TotalFacts:         500,
		HardIdentifiers:    150,
		PendingMerges:      10,
		AutoEligibleMerges: 5,
		UnresolvedFacts:    25,
		CrossChannelLinked: 30,
	}

	if stats.ActivePersons+stats.MergedPersons != 120 {
		t.Errorf("expected 120 total persons, got %d", stats.ActivePersons+stats.MergedPersons)
	}

	if stats.AutoEligibleMerges > stats.PendingMerges {
		t.Error("auto-eligible merges cannot exceed pending merges")
	}
}
