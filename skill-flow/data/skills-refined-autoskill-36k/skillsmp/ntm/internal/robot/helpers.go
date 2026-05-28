package robot

import (
	"os"
)

func mustGetwd() string {
	wd, err := os.Getwd()
	if err != nil {
		return "."
	}
	return wd
}

// capitalize returns the string with its first letter uppercased.
// For simple ASCII strings; use golang.org/x/text/cases for full Unicode support.
func capitalize(s string) string {
	if len(s) == 0 {
		return s
	}
	// For ASCII lowercase letters, convert to uppercase
	if s[0] >= 'a' && s[0] <= 'z' {
		return string(s[0]-32) + s[1:]
	}
	return s
}
