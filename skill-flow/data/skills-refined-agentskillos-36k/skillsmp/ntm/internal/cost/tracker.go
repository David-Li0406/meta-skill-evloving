// Package cost provides API cost tracking for AI agent sessions.
package cost

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/Dicklesworthstone/ntm/internal/tokens"
)

// ModelPricing defines the cost per 1K tokens for input and output.
type ModelPricing struct {
	InputPer1K  float64 `json:"input_per_1k"`
	OutputPer1K float64 `json:"output_per_1k"`
}

// modelPricing contains pricing data for known models (USD per 1K tokens).
// Updated as of May 2025.
var modelPricing = map[string]ModelPricing{
	// Claude models
	"claude-opus":       {InputPer1K: 0.015, OutputPer1K: 0.075},
	"claude-opus-4":     {InputPer1K: 0.015, OutputPer1K: 0.075},
	"claude-opus-4-5":   {InputPer1K: 0.015, OutputPer1K: 0.075},
	"claude-sonnet":     {InputPer1K: 0.003, OutputPer1K: 0.015},
	"claude-sonnet-4":   {InputPer1K: 0.003, OutputPer1K: 0.015},
	"claude-haiku":      {InputPer1K: 0.00025, OutputPer1K: 0.00125},
	"claude-haiku-3-5":  {InputPer1K: 0.00025, OutputPer1K: 0.00125},
	"claude-3-opus":     {InputPer1K: 0.015, OutputPer1K: 0.075},
	"claude-3-sonnet":   {InputPer1K: 0.003, OutputPer1K: 0.015},
	"claude-3-haiku":    {InputPer1K: 0.00025, OutputPer1K: 0.00125},
	"claude-3-5-sonnet": {InputPer1K: 0.003, OutputPer1K: 0.015},
	"claude-3-5-haiku":  {InputPer1K: 0.00025, OutputPer1K: 0.00125},

	// OpenAI models
	"gpt-4o":      {InputPer1K: 0.005, OutputPer1K: 0.015},
	"gpt-4o-mini": {InputPer1K: 0.00015, OutputPer1K: 0.0006},
	"gpt-4-turbo": {InputPer1K: 0.01, OutputPer1K: 0.03},
	"gpt-4":       {InputPer1K: 0.03, OutputPer1K: 0.06},
	"o1":          {InputPer1K: 0.015, OutputPer1K: 0.06},
	"o1-mini":     {InputPer1K: 0.003, OutputPer1K: 0.012},
	"o1-preview":  {InputPer1K: 0.015, OutputPer1K: 0.06},

	// Google models
	"gemini-pro":       {InputPer1K: 0.00025, OutputPer1K: 0.0005},
	"gemini-pro-1.5":   {InputPer1K: 0.00025, OutputPer1K: 0.0005},
	"gemini-ultra":     {InputPer1K: 0.00125, OutputPer1K: 0.00375},
	"gemini-flash":     {InputPer1K: 0.000075, OutputPer1K: 0.0003},
	"gemini-flash-1.5": {InputPer1K: 0.000075, OutputPer1K: 0.0003},
	"gemini-2.0-flash": {InputPer1K: 0.000075, OutputPer1K: 0.0003},

	// Default fallback
	"default": {InputPer1K: 0.003, OutputPer1K: 0.015},
}

// AgentCost tracks token usage for a single agent.
type AgentCost struct {
	InputTokens  int       `json:"input_tokens"`
	OutputTokens int       `json:"output_tokens"`
	Model        string    `json:"model"`
	LastUpdated  time.Time `json:"last_updated"`
}

// Cost calculates the USD cost for this agent.
func (a *AgentCost) Cost() float64 {
	pricing := GetModelPricing(a.Model)
	inputCost := float64(a.InputTokens) / 1000 * pricing.InputPer1K
	outputCost := float64(a.OutputTokens) / 1000 * pricing.OutputPer1K
	return inputCost + outputCost
}

// SessionCost tracks costs for all agents in a session.
type SessionCost struct {
	Agents    map[string]*AgentCost `json:"agents"`
	StartTime time.Time             `json:"start_time"`
}

// TotalCost calculates the total USD cost for this session.
func (s *SessionCost) TotalCost() float64 {
	var total float64
	for _, agent := range s.Agents {
		total += agent.Cost()
	}
	return total
}

// TotalTokens returns total input and output tokens for this session.
func (s *SessionCost) TotalTokens() (input, output int) {
	for _, agent := range s.Agents {
		input += agent.InputTokens
		output += agent.OutputTokens
	}
	return
}

// CostTracker manages cost tracking across multiple sessions.
type CostTracker struct {
	mu       sync.RWMutex
	sessions map[string]*SessionCost
	dataDir  string
}

// NewCostTracker creates a new CostTracker instance.
// If dataDir is empty, persistence is disabled.
func NewCostTracker(dataDir string) *CostTracker {
	return &CostTracker{
		sessions: make(map[string]*SessionCost),
		dataDir:  dataDir,
	}
}

// LoadFromDir loads cost data from the .ntm directory.
func (t *CostTracker) LoadFromDir(dir string) error {
	t.mu.Lock()
	defer t.mu.Unlock()

	costPath := filepath.Join(dir, ".ntm", "costs.json")
	data, err := os.ReadFile(costPath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil // No cost file yet, that's fine
		}
		return fmt.Errorf("read costs file: %w", err)
	}

	var sessions map[string]*SessionCost
	if err := json.Unmarshal(data, &sessions); err != nil {
		return fmt.Errorf("parse costs file: %w", err)
	}

	t.sessions = sessions
	return nil
}

// SaveToDir saves cost data to the .ntm directory.
func (t *CostTracker) SaveToDir(dir string) error {
	t.mu.RLock()
	defer t.mu.RUnlock()

	ntmDir := filepath.Join(dir, ".ntm")
	if err := os.MkdirAll(ntmDir, 0755); err != nil {
		return fmt.Errorf("create .ntm dir: %w", err)
	}

	costPath := filepath.Join(ntmDir, "costs.json")
	data, err := json.MarshalIndent(t.sessions, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal costs: %w", err)
	}

	if err := os.WriteFile(costPath, data, 0644); err != nil {
		return fmt.Errorf("write costs file: %w", err)
	}

	return nil
}

// getOrCreateSession returns the session cost, creating it if needed.
func (t *CostTracker) getOrCreateSession(session string) *SessionCost {
	if s, ok := t.sessions[session]; ok {
		return s
	}
	s := &SessionCost{
		Agents:    make(map[string]*AgentCost),
		StartTime: time.Now(),
	}
	t.sessions[session] = s
	return s
}

// getOrCreateAgent returns the agent cost, creating it if needed.
func (s *SessionCost) getOrCreateAgent(pane, model string) *AgentCost {
	if a, ok := s.Agents[pane]; ok {
		return a
	}
	a := &AgentCost{
		Model:       model,
		LastUpdated: time.Now(),
	}
	s.Agents[pane] = a
	return a
}

// RecordPrompt records input tokens from a prompt.
func (t *CostTracker) RecordPrompt(session, pane, model, prompt string) {
	t.mu.Lock()
	defer t.mu.Unlock()

	tokens := EstimateTokens(prompt)
	s := t.getOrCreateSession(session)
	a := s.getOrCreateAgent(pane, model)
	a.InputTokens += tokens
	a.LastUpdated = time.Now()
	if model != "" && a.Model == "" {
		a.Model = model
	}
}

// RecordResponse records output tokens from a response.
func (t *CostTracker) RecordResponse(session, pane, model, response string) {
	t.mu.Lock()
	defer t.mu.Unlock()

	tokens := EstimateTokens(response)
	s := t.getOrCreateSession(session)
	a := s.getOrCreateAgent(pane, model)
	a.OutputTokens += tokens
	a.LastUpdated = time.Now()
	if model != "" && a.Model == "" {
		a.Model = model
	}
}

// RecordTokens records token counts directly (for when exact counts are known).
func (t *CostTracker) RecordTokens(session, pane, model string, inputTokens, outputTokens int) {
	t.mu.Lock()
	defer t.mu.Unlock()

	s := t.getOrCreateSession(session)
	a := s.getOrCreateAgent(pane, model)
	a.InputTokens += inputTokens
	a.OutputTokens += outputTokens
	a.LastUpdated = time.Now()
	if model != "" {
		a.Model = model
	}
}

// GetSessionCost returns the total USD cost for a session.
func (t *CostTracker) GetSessionCost(session string) float64 {
	t.mu.RLock()
	defer t.mu.RUnlock()

	s, ok := t.sessions[session]
	if !ok {
		return 0
	}
	return s.TotalCost()
}

// GetSession returns the session cost data (nil if not found).
func (t *CostTracker) GetSession(session string) *SessionCost {
	t.mu.RLock()
	defer t.mu.RUnlock()

	s, ok := t.sessions[session]
	if !ok {
		return nil
	}
	// Return a copy to avoid race conditions
	copy := &SessionCost{
		StartTime: s.StartTime,
		Agents:    make(map[string]*AgentCost, len(s.Agents)),
	}
	for k, v := range s.Agents {
		agentCopy := *v
		copy.Agents[k] = &agentCopy
	}
	return copy
}

// GetAllSessions returns all session names.
func (t *CostTracker) GetAllSessions() []string {
	t.mu.RLock()
	defer t.mu.RUnlock()

	names := make([]string, 0, len(t.sessions))
	for name := range t.sessions {
		names = append(names, name)
	}
	return names
}

// GetTotalCost returns the total cost across all sessions.
func (t *CostTracker) GetTotalCost() float64 {
	t.mu.RLock()
	defer t.mu.RUnlock()

	var total float64
	for _, s := range t.sessions {
		total += s.TotalCost()
	}
	return total
}

// ClearSession removes cost data for a session.
func (t *CostTracker) ClearSession(session string) {
	t.mu.Lock()
	defer t.mu.Unlock()

	delete(t.sessions, session)
}

// GetModelPricing returns the pricing for a model.
// If the model is not found, returns default pricing.
func GetModelPricing(model string) ModelPricing {
	if pricing, ok := modelPricing[model]; ok {
		return pricing
	}
	return modelPricing["default"]
}

// EstimateTokens estimates the token count for text.
// Uses the heuristics from the internal/tokens package.
func EstimateTokens(text string) int {
	return tokens.EstimateTokens(text)
}

// FormatCost formats a USD amount as a string.
func FormatCost(usd float64) string {
	if usd < 0.01 {
		return fmt.Sprintf("$%.4f", usd)
	}
	if usd < 1.0 {
		return fmt.Sprintf("$%.3f", usd)
	}
	return fmt.Sprintf("$%.2f", usd)
}
