package agent

import (
	"time"
)

// parserImpl implements the Parser interface.
type parserImpl struct {
	config ParserConfig
}

// NewParser creates a parser with default configuration.
func NewParser() Parser {
	return &parserImpl{config: DefaultParserConfig()}
}

// NewParserWithConfig creates a parser with custom configuration.
func NewParserWithConfig(cfg ParserConfig) Parser {
	return &parserImpl{config: cfg}
}

// Parse analyzes terminal output and returns structured agent state.
// It performs the following steps:
// 1. Detect agent type from output patterns
// 2. Extract quantitative metrics (context %, tokens, memory)
// 3. Detect qualitative state flags (working, idle, rate limited, error)
// 4. Calculate confidence score
// 5. Keep raw sample for debugging
func (p *parserImpl) Parse(output string) (*AgentState, error) {
	// Strip ANSI codes for cleaner pattern matching
	cleanOutput := stripANSICodes(output)

	state := &AgentState{
		ParsedAt: time.Now().UTC(),
	}

	// Step 1: Detect agent type
	state.Type = p.DetectAgentType(cleanOutput)

	// Step 2: Extract metrics based on agent type
	p.extractMetrics(cleanOutput, state)

	// Step 3: Detect state flags
	p.detectStateFlags(cleanOutput, state)

	// Step 4: Calculate confidence
	state.Confidence = p.calculateConfidence(state)

	// Step 5: Keep sample for debugging (last N chars)
	if len(cleanOutput) > p.config.SampleLength {
		state.RawSample = cleanOutput[len(cleanOutput)-p.config.SampleLength:]
	} else {
		state.RawSample = cleanOutput
	}

	return state, nil
}

// DetectAgentType identifies which agent type produced the output.
// It checks for agent-specific signatures in priority order.
func (p *parserImpl) DetectAgentType(output string) AgentType {
	// Check for explicit headers/signatures in priority order
	// Priority: Claude > Codex > Gemini (based on specificity of patterns)

	if ccHeaderPattern.MatchString(output) {
		return AgentTypeClaudeCode
	}

	// Codex has unique context percentage display
	if codContextPattern.MatchString(output) {
		return AgentTypeCodex
	}
	if codHeaderPattern.MatchString(output) {
		return AgentTypeCodex
	}

	// Gemini patterns
	if gmiHeaderPattern.MatchString(output) {
		return AgentTypeGemini
	}
	if gmiYoloPattern.MatchString(output) {
		return AgentTypeGemini
	}

	// Fallback: use pattern frequency analysis
	return p.detectByPatternFrequency(output)
}

// detectByPatternFrequency analyzes pattern matches to guess agent type.
// Used when no explicit header is found.
func (p *parserImpl) detectByPatternFrequency(output string) AgentType {
	scores := make(map[AgentType]int)

	// Check working patterns (they're the most frequent indicators)
	if matchAny(output, ccWorkingPatterns) {
		scores[AgentTypeClaudeCode]++
	}
	if matchAny(output, codWorkingPatterns) {
		scores[AgentTypeCodex]++
	}
	if matchAny(output, gmiWorkingPatterns) {
		scores[AgentTypeGemini]++
	}

	// Find highest scoring type
	var maxType AgentType = AgentTypeUnknown
	var maxScore int
	for t, score := range scores {
		if score > maxScore {
			maxScore = score
			maxType = t
		}
	}

	return maxType
}

// extractMetrics pulls quantitative data from output based on agent type.
func (p *parserImpl) extractMetrics(output string, state *AgentState) {
	switch state.Type {
	case AgentTypeCodex:
		// Codex gives explicit context percentage - most valuable!
		// Example: "47% context left · ? for shortcuts"
		if pct := extractFloat(codContextPattern, output); pct != nil {
			state.ContextRemaining = pct
			if *pct < p.config.ContextLowThreshold {
				state.IsContextLow = true
			}
		}

		// Also extract token count if present
		// Example: "Token usage: total=219,582 input=206,150"
		if tokens := extractInt(codTokenPattern, output); tokens != nil {
			state.TokensUsed = tokens
		}

	case AgentTypeGemini:
		// Gemini shows memory usage
		// Example: "gemini-3-pro-preview /model | 396.8 MB"
		if mb := extractFloat(gmiMemoryPattern, output); mb != nil {
			state.MemoryMB = mb
		}

	case AgentTypeClaudeCode:
		// Claude doesn't give explicit metrics
		// We rely on warning messages instead
		if matchAny(output, ccContextWarnings) {
			state.IsContextLow = true
		}
	}
}

// detectStateFlags sets qualitative state flags based on output patterns.
func (p *parserImpl) detectStateFlags(output string, state *AgentState) {
	// Rate limit detection (highest priority - agent is blocked)
	state.IsRateLimited = p.detectRateLimit(output, state.Type)
	if state.IsRateLimited {
		state.LimitIndicators = p.collectLimitIndicators(output, state.Type)
		// If rate limited, we are effectively blocked, so clear other flags
		state.IsWorking = false
		state.IsIdle = false
		state.IsInError = p.detectError(output, state.Type)
		return
	}

	// Idle detection
	// We check this BEFORE trusting IsWorking, because IsWorking patterns
	// (like "testing", "running") might still be present in the scrollback
	// even after the agent has finished and printed a prompt.
	state.IsIdle = p.detectIdle(output, state.Type)

	// Working detection
	// We always run this to collect indicators for debugging/confidence
	rawIsWorking := p.detectWorking(output, state.Type)
	if rawIsWorking {
		state.WorkIndicators = p.collectWorkIndicators(output, state.Type)
	}

	// Conflict resolution: Prompt beats substring heuristics
	// If we see a definitive prompt at the end (IsIdle), we are not working,
	// regardless of what keywords appear in the scrollback.
	if state.IsIdle {
		state.IsWorking = false
	} else {
		state.IsWorking = rawIsWorking
	}

	// Error detection
	state.IsInError = p.detectError(output, state.Type)
}

// detectRateLimit checks if the agent hit an API usage limit.
func (p *parserImpl) detectRateLimit(output string, agentType AgentType) bool {
	switch agentType {
	case AgentTypeClaudeCode:
		return matchAny(output, ccRateLimitPatterns)
	case AgentTypeCodex:
		return matchAny(output, codRateLimitPatterns)
	case AgentTypeGemini:
		return matchAny(output, gmiRateLimitPatterns)
	default:
		// Check all patterns for unknown type
		return matchAny(output, ccRateLimitPatterns) ||
			matchAny(output, codRateLimitPatterns) ||
			matchAny(output, gmiRateLimitPatterns)
	}
}

// detectWorking checks if the agent is actively producing output.
// This focuses on recent output (last 20 lines) for accuracy.
func (p *parserImpl) detectWorking(output string, agentType AgentType) bool {
	// Check recent output - recent activity is more relevant
	recentOutput := getLastNLines(output, 20)

	switch agentType {
	case AgentTypeClaudeCode:
		return matchAny(recentOutput, ccWorkingPatterns)
	case AgentTypeCodex:
		return matchAny(recentOutput, codWorkingPatterns)
	case AgentTypeGemini:
		return matchAny(recentOutput, gmiWorkingPatterns)
	default:
		// Check all patterns for unknown type
		return matchAny(recentOutput, ccWorkingPatterns) ||
			matchAny(recentOutput, codWorkingPatterns) ||
			matchAny(recentOutput, gmiWorkingPatterns)
	}
}

// detectIdle checks if the agent is waiting for user input.
// This examines the last few lines for prompt patterns.
func (p *parserImpl) detectIdle(output string, agentType AgentType) bool {
	// Check last lines for prompt indicators
	lastLines := getLastNLines(output, 5)

	switch agentType {
	case AgentTypeClaudeCode:
		return matchAnyRegex(lastLines, ccIdlePatterns)
	case AgentTypeCodex:
		return matchAnyRegex(lastLines, codIdlePatterns)
	case AgentTypeGemini:
		// Gemini is trickier - check for prompt or lack of working indicators
		if matchAnyRegex(lastLines, gmiIdlePatterns) {
			return true
		}
		// If no working patterns in last lines, likely idle
		return !matchAny(lastLines, gmiWorkingPatterns)
	default:
		// Check all idle patterns for unknown type
		return matchAnyRegex(lastLines, ccIdlePatterns) ||
			matchAnyRegex(lastLines, codIdlePatterns) ||
			matchAnyRegex(lastLines, gmiIdlePatterns)
	}
}

// detectError checks if the agent is in an error state.
func (p *parserImpl) detectError(output string, agentType AgentType) bool {
	// Check recent output for error patterns
	recentOutput := getLastNLines(output, 10)

	switch agentType {
	case AgentTypeClaudeCode:
		return matchAny(recentOutput, ccErrorPatterns)
	case AgentTypeCodex:
		return matchAny(recentOutput, codErrorPatterns)
	case AgentTypeGemini:
		return matchAny(recentOutput, gmiErrorPatterns)
	default:
		return false // Unknown type - don't assume error
	}
}

// collectLimitIndicators returns the specific patterns that matched for rate limiting.
func (p *parserImpl) collectLimitIndicators(output string, agentType AgentType) []string {
	switch agentType {
	case AgentTypeClaudeCode:
		return collectMatches(output, ccRateLimitPatterns)
	case AgentTypeCodex:
		return collectMatches(output, codRateLimitPatterns)
	case AgentTypeGemini:
		return collectMatches(output, gmiRateLimitPatterns)
	default:
		// Collect from all for unknown type
		matches := collectMatches(output, ccRateLimitPatterns)
		matches = append(matches, collectMatches(output, codRateLimitPatterns)...)
		matches = append(matches, collectMatches(output, gmiRateLimitPatterns)...)
		return matches
	}
}

// collectWorkIndicators returns the specific patterns that matched for working state.
func (p *parserImpl) collectWorkIndicators(output string, agentType AgentType) []string {
	// Focus on recent output
	recentOutput := getLastNLines(output, 20)

	switch agentType {
	case AgentTypeClaudeCode:
		return collectMatches(recentOutput, ccWorkingPatterns)
	case AgentTypeCodex:
		return collectMatches(recentOutput, codWorkingPatterns)
	case AgentTypeGemini:
		return collectMatches(recentOutput, gmiWorkingPatterns)
	default:
		matches := collectMatches(recentOutput, ccWorkingPatterns)
		matches = append(matches, collectMatches(recentOutput, codWorkingPatterns)...)
		matches = append(matches, collectMatches(recentOutput, gmiWorkingPatterns)...)
		return matches
	}
}

// calculateConfidence determines how confident we are in the parsed state.
// Returns a value between 0.0 (no confidence) and 1.0 (highly confident).
func (p *parserImpl) calculateConfidence(state *AgentState) float64 {
	confidence := 0.5 // Base confidence

	// Boost for explicit metrics (Codex percentage is very reliable)
	if state.ContextRemaining != nil {
		confidence += 0.25
	}
	if state.TokensUsed != nil {
		confidence += 0.05
	}

	// Boost for clear working indicators
	indicatorCount := len(state.WorkIndicators)
	if indicatorCount > 0 {
		// Up to +0.3 for multiple indicators
		confidence += 0.1 * float64(minInt(indicatorCount, 3))
	}

	// Boost for rate limit indicators (unambiguous)
	if len(state.LimitIndicators) > 0 {
		confidence += 0.2
	}

	// Penalty for unknown agent type
	if state.Type == AgentTypeUnknown {
		confidence -= 0.3
	}

	// Penalty for conflicting signals
	if state.IsWorking && state.IsIdle {
		confidence -= 0.2 // Something's wrong
	}

	// Clamp to [0, 1]
	if confidence > 1.0 {
		confidence = 1.0
	}
	if confidence < 0.0 {
		confidence = 0.0
	}

	return confidence
}

// minInt returns the smaller of two integers.
// Note: Go 1.21+ has built-in min(), but we define for compatibility.
func minInt(a, b int) int {
	if a < b {
		return a
	}
	return b
}
