package adapters

import (
	"testing"
)

func TestNormalizePhone(t *testing.T) {
	cases := map[string]string{
		"":                     "",
		"  +1 (707) 287-4936 ": "+17072874936",
		"6376797":              "6376797",
		"+17079276461":         "+17079276461",
	}
	for in, want := range cases {
		got := normalizePhone(in)
		if got != want {
			t.Fatalf("normalizePhone(%q)=%q want %q", in, got, want)
		}
	}
}
