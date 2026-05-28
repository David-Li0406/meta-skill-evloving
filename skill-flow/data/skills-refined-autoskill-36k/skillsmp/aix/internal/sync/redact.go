package sync

import (
	"math"
	"regexp"
	"strings"
)

// SecretPattern defines a pattern that matches secrets we want to redact
type SecretPattern struct {
	Name    string
	Pattern *regexp.Regexp
}

// Common secret patterns - API keys, tokens, OAuth codes, etc.
var secretPatterns = []SecretPattern{
	// Google OAuth authorization codes (4/0A...)
	{Name: "google_oauth_code", Pattern: regexp.MustCompile(`\b4/[0-9A-Za-z_-]{40,100}\b`)},
	// Google access tokens (ya29...)
	{Name: "google_access_token", Pattern: regexp.MustCompile(`\bya29\.[0-9A-Za-z_-]{50,200}\b`)},
	// Gemini/Google AI API keys (often start with "AI" or are high-entropy base64-ish)
	{Name: "gemini_api_key", Pattern: regexp.MustCompile(`\bAQ\.[A-Za-z0-9_-]{30,100}\b`)},
	// Generic API keys with common prefixes
	{Name: "api_key_sk", Pattern: regexp.MustCompile(`\bsk-[A-Za-z0-9_-]{20,100}\b`)},          // OpenAI style (sk-xxx, sk-proj-xxx, etc.)
	{Name: "api_key_pk", Pattern: regexp.MustCompile(`\bpk-[A-Za-z0-9]{20,100}\b`)},           // Public keys
	{Name: "api_key_key", Pattern: regexp.MustCompile(`\bkey-[A-Za-z0-9]{20,100}\b`)},         // Generic
	{Name: "anthropic_key", Pattern: regexp.MustCompile(`\bsk-ant-[A-Za-z0-9-]{20,100}\b`)},   // Anthropic
	{Name: "github_token", Pattern: regexp.MustCompile(`\bgh[ps]_[A-Za-z0-9]{36,100}\b`)},     // GitHub PAT
	{Name: "github_oauth", Pattern: regexp.MustCompile(`\bgho_[A-Za-z0-9]{36,100}\b`)},        // GitHub OAuth
	{Name: "npm_token", Pattern: regexp.MustCompile(`\bnpm_[A-Za-z0-9]{36,100}\b`)},           // NPM
	{Name: "stripe_key", Pattern: regexp.MustCompile(`\b[sr]k_(test|live)_[A-Za-z0-9]{20,100}\b`)},
	{Name: "aws_key", Pattern: regexp.MustCompile(`\bAKIA[0-9A-Z]{16}\b`)},                    // AWS Access Key ID
	{Name: "slack_token", Pattern: regexp.MustCompile(`\bxox[baprs]-[0-9A-Za-z-]{10,100}\b`)}, // Slack
	// Bearer tokens in Authorization headers
	{Name: "bearer_token", Pattern: regexp.MustCompile(`Bearer\s+[A-Za-z0-9._-]{20,500}`)},
	// Base64-encoded credentials
	{Name: "basic_auth", Pattern: regexp.MustCompile(`Basic\s+[A-Za-z0-9+/=]{20,200}`)},
}

// HighEntropyThreshold - strings above this entropy per character are likely secrets
const HighEntropyThreshold = 4.0

// MinSecretLength - minimum length for high-entropy detection
const MinSecretLength = 20

// RedactionPlaceholder is what we replace secrets with
const RedactionPlaceholder = "[REDACTED]"

// Pre-compiled regexes for detection (compiled once at init, not per-call)
var (
	potentialSecretRe = regexp.MustCompile(`[A-Za-z0-9+/=_-]{20,}`)
	uuidRe            = regexp.MustCompile(`^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`)
	gitShaRe          = regexp.MustCompile(`^[0-9a-f]{40}$`)
)

// Fast substring checks to avoid running regexes on most content.
// The export path can call RedactJSON hundreds of thousands of times; regex scans dominate runtime.
var secretMarkers = []string{
	"sk-ant-",
	"sk-",
	"pk-",
	"ghp_",
	"ghs_",
	"gho_",
	"npm_",
	"ya29.",
	"AQ.",
	"AKIA",
	"xoxb-",
	"xoxp-",
	"xoxa-",
	"xoxr-",
	"Bearer ",
	"Basic ",
	"BEGIN PRIVATE KEY",
	"AIza", // common Google API key prefix (not currently a strict regex match, but a good marker)
}

func maybeContainsSecret(content string) bool {
	for _, m := range secretMarkers {
		if strings.Contains(content, m) {
			return true
		}
	}
	return false
}

// RedactSecrets redacts known secret patterns from content
// Note: High-entropy detection is disabled for performance (was too slow on large exports)
func RedactSecrets(content string) string {
	if content == "" {
		return content
	}

	// Avoid regex scans when the string almost certainly contains no secrets.
	if !maybeContainsSecret(content) {
		return content
	}

	result := content

	// Redact known patterns (fast - pre-compiled regexes)
	for _, sp := range secretPatterns {
		result = sp.Pattern.ReplaceAllString(result, RedactionPlaceholder)
	}

	// High-entropy detection disabled for performance
	// Uncomment if you need to catch unknown secret formats:
	// result = redactHighEntropyStrings(result)

	return result
}

// redactHighEntropyStrings finds and redacts high-entropy strings that look like secrets
func redactHighEntropyStrings(content string) string {
	return potentialSecretRe.ReplaceAllStringFunc(content, func(match string) string {
		// Skip if it's already redacted
		if match == RedactionPlaceholder {
			return match
		}

		// Skip if it looks like a path or common pattern
		if looksLikePath(match) || looksLikeCommonNonSecret(match) {
			return match
		}

		// Calculate Shannon entropy
		entropy := shannonEntropy(match)

		// If entropy is high enough, redact it
		if entropy >= HighEntropyThreshold && len(match) >= MinSecretLength {
			return RedactionPlaceholder
		}

		return match
	})
}

// shannonEntropy calculates the Shannon entropy of a string (bits per character)
func shannonEntropy(s string) float64 {
	if len(s) == 0 {
		return 0
	}

	// Count character frequencies
	freq := make(map[rune]int)
	for _, c := range s {
		freq[c]++
	}

	// Calculate entropy
	var entropy float64
	length := float64(len(s))
	for _, count := range freq {
		p := float64(count) / length
		entropy -= p * math.Log2(p)
	}

	return entropy
}

// looksLikePath checks if a string looks like a file path segment
func looksLikePath(s string) bool {
	pathIndicators := []string{
		"Users", "home", "var", "etc", "usr", "opt", "tmp",
		"src", "lib", "bin", "pkg", "mod", "node_modules",
		"internal", "cmd", "api", "app", "config",
	}
	lower := strings.ToLower(s)
	for _, ind := range pathIndicators {
		if strings.Contains(lower, strings.ToLower(ind)) {
			return true
		}
	}
	return false
}

// looksLikeCommonNonSecret checks if a string is a common non-secret pattern
func looksLikeCommonNonSecret(s string) bool {
	// UUIDs (use pre-compiled regex)
	if uuidRe.MatchString(strings.ToLower(s)) {
		return true
	}
	// Hex strings that are likely hashes (commit SHAs, etc.)
	if gitShaRe.MatchString(strings.ToLower(s)) {
		return true // git SHA
	}
	// Common base64 padding patterns with low entropy
	if strings.HasSuffix(s, "====") || strings.HasSuffix(s, "==") {
		// Could be base64, check entropy
		return shannonEntropy(s) < 3.5
	}
	return false
}

// RedactJSON redacts secrets from a JSON string while preserving structure
// This is more careful than RedactSecrets - it only redacts string values
func RedactJSON(jsonStr string) string {
	// For now, use the same logic - we can make this smarter later
	// to parse JSON and only redact within string values
	return RedactSecrets(jsonStr)
}
