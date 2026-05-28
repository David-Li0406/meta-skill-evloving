package main

import (
	"fmt"
	"os"

	"github.com/Dicklesworthstone/ntm/internal/agent"
)

func main() {
	p := agent.NewParser()

	// Scenario: Agent ran tests (producing "testing" keyword) but has finished and is waiting.
	output := `Claude Opus 4.5
Running tests...
testing package internal/agent...
ok  	github.com/Dicklesworthstone/ntm/internal/agent	0.123s
Tests completed.
> `

	state, err := p.Parse(output)
	if err != nil {
		fmt.Printf("Parse error: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Parsed State:\n")
	fmt.Printf("Type: %v\n", state.Type)
	fmt.Printf("IsIdle: %v\n", state.IsIdle)
	fmt.Printf("IsWorking: %v\n", state.IsWorking)

	success := true
	if state.Type != agent.AgentTypeClaudeCode {
		fmt.Printf("FAIL: Expected Type ClaudeCode, got %v\n", state.Type)
		success = false
	}

	if !state.IsIdle {
		fmt.Printf("FAIL: Expected IsIdle=true\n")
		success = false
	}

	if state.IsWorking {
		fmt.Printf("FAIL: Expected IsWorking=false\n")
		success = false
	}

	if success {
		fmt.Println("SUCCESS: Test passed!")
	} else {
		os.Exit(1)
	}
}
