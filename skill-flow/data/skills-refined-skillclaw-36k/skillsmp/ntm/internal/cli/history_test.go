package cli

import "testing"

func TestRunHistoryListRejectsNonPositiveLimit(t *testing.T) {
	err := runHistoryList(0, "", "", "", "")
	if err == nil {
		t.Fatalf("expected error for limit <= 0")
	}
}
