# Agent Evaluator Test Cases

This file contains test cases for the AgentEvaluator class. Test cases are organized by functionality and can be dynamically loaded into unit tests.

## File Pattern Matching Tests

### Basic File Pattern Matching

- **Description**: Test basic glob pattern matching functionality
- **Test Cases**:
	- `*.md` should match `test.md` but not `test.txt`
	- `docs/**` should match `docs/README.md` but not `src/README.md`
	- `**/*.ts` should match `src/components/Button.tsx` and `src/utils/helpers.ts`

### File Pattern Edge Cases

- **Description**: Test edge cases and error handling for file patterns
- **Test Cases**:
	- Empty patterns should not match anything
	- Invalid regex patterns should be handled gracefully
	- Empty file paths should not match

## Intent Pattern Matching Tests

### Basic Intent Pattern Matching

- **Description**: Test regex-based intent pattern matching
- **Test Cases**:
	- Pattern `\b(create|generate)\b.*\b(diagram)\b` should match `"create a diagram"` but not `"draw a picture"`
	- Case insensitive matching should work
	- Complex patterns should be supported

### Intent Pattern Edge Cases

- **Description**: Test edge cases for intent patterns
- **Test Cases**:
	- Empty patterns should not match
	- Invalid regex should be handled gracefully
	- Empty text should not match

## Agent Evaluation Tests

### Git-Committer Keyword - Commit
- **Description**: Test activation for commit keyword
- **Input**: `"commit my changes"`
- **Expected**:
	- Git-Committer should be activated (YES)
	- Should have keyword matches > 0

### Git-Committer Keyword - Push
- **Description**: Test activation for push keyword
- **Input**: `"push to remote"`
- **Expected**:
	- Git-Committer should be activated (YES)
	- Should have keyword matches > 0

### Git-Committer Keyword - Atomic Commit
- **Description**: Test activation for atomic commit phrase
- **Input**: `"create atomic commit"`
- **Expected**:
	- Git-Committer should be activated (YES)
	- Should have keyword matches > 0

### Git-Committer Keyword - Atomic Commits Plan
- **Description**: Test activation for atomic commits plan phrase
- **Input**: `"atomic commits plan"`
- **Expected**:
	- Git-Committer should be activated (YES)
	- Should have keyword matches > 0

### Diataxis Keyword - Documentation
- **Description**: Test activation for documentation keyword
- **Input**: `"write documentation"`
- **Expected**:
	- Diataxis-Documentation-Expert should be activated (YES)
	- Should have keyword matches > 0

### Diataxis Keyword - Tutorial
- **Description**: Test activation for tutorial keyword
- **Input**: `"create a tutorial"`
- **Expected**:
	- Diataxis-Documentation-Expert should be activated (YES)
	- Should have keyword matches > 0

### Diataxis Keyword - Extract Knowledge
- **Description**: Test activation for extract knowledge phrase
- **Input**: `"extract knowledge"`
- **Expected**:
	- Diataxis-Documentation-Expert should be activated (YES)
	- Should have keyword matches > 0

### Generic-Research Keyword - Research
- **Description**: Test activation for research keyword
- **Input**: `"research best practices"`
- **Expected**:
	- Generic-Research-Agent should be activated (YES)
	- Should have keyword matches > 0

### Generic-Research Keyword - Investigate
- **Description**: Test activation for investigate keyword
- **Input**: `"investigate the error"`
- **Expected**:
	- Generic-Research-Agent should be activated (YES)
	- Should have keyword matches > 0

### Generic-Research Keyword - Conduct Research
- **Description**: Test activation for conduct research phrase
- **Input**: `"conduct research"`
- **Expected**:
	- Generic-Research-Agent should be activated (YES)
	- Should have keyword matches > 0

### Instruction-Writer Keyword - Instruction
- **Description**: Test activation for instruction keyword
- **Input**: `"create instruction file"`
- **Expected**:
	- Instruction-Writer should be activated (YES)
	- Should have keyword matches > 0

### Instruction-Writer Keyword - Guidelines
- **Description**: Test activation for guidelines keyword
- **Input**: `"add coding guidelines"`
- **Expected**:
	- Instruction-Writer should be activated (YES)
	- Should have keyword matches > 0

### Instruction-Writer Keyword - Revise Custom Instruction
- **Description**: Test activation for revise custom instruction phrase
- **Input**: `"revise custom instruction"`
- **Expected**:
	- Instruction-Writer should be activated (YES)
	- Should have keyword matches > 0

### Instruction-Writer Keyword - Create Custom Instruction
- **Description**: Test activation for create custom instruction phrase
- **Input**: `"create custom instruction"`
- **Expected**:
	- Instruction-Writer should be activated (YES)
	- Should have keyword matches > 0

### Mermaid-Agent Keyword - Diagram
- **Description**: Test activation for diagram keyword
- **Input**: `"create a diagram"`
- **Expected**:
	- Mermaid-Agent should be activated (YES)
	- Should have keyword matches > 0

### Mermaid-Agent Keyword - Flowchart
- **Description**: Test activation for flowchart keyword
- **Input**: `"generate a flowchart"`
- **Expected**:
	- Mermaid-Agent should be activated (YES)
	- Should have keyword matches > 0

### Meta-Agent Keyword - Agent
- **Description**: Test activation for agent keyword
- **Input**: `"create a new agent"`
- **Expected**:
	- Meta-Agent should be activated (YES)
	- Should have keyword matches > 0

### Meta-Agent Keyword - Create New Custom Agent
- **Description**: Test activation for create new custom agent phrase
- **Input**: `"create new custom agent"`
- **Expected**:
	- Meta-Agent should be activated (YES)
	- Should have keyword matches > 0

### Meta-Agent Keyword - Revise Custom Agent
- **Description**: Test activation for revise custom agent phrase
- **Input**: `"revise custom agent"`
- **Expected**:
	- Meta-Agent should be activated (YES)
	- Should have keyword matches > 0

### PM-Changelog Keyword - Changelog
- **Description**: Test activation for changelog keyword
- **Input**: `"generate changelog"`
- **Expected**:
	- PM-Changelog should be activated (YES)
	- Should have keyword matches > 0

### PM-Changelog Keyword - Generate Monthly Summary
- **Description**: Test activation for generate monthly summary phrase
- **Input**: `"generate monthly summary"`
- **Expected**:
	- PM-Changelog should be activated (YES)
	- Should have keyword matches > 0

### PM-Changelog Keyword - Generate Monthly Changelog
- **Description**: Test activation for generate monthly changelog phrase
- **Input**: `"generate monthly changelog"`
- **Expected**:
	- PM-Changelog should be activated (YES)
	- Should have keyword matches > 0

### Intent Pattern Activation

- **Description**: Test activation based on intent patterns
- **Input**: `"create a flowchart for my application"`
- **Expected**:
	- Mermaid-Agent should be activated (YES)
	- Should have intent_matches = 1
	- Should be in required_agents list

### File Pattern Activation

- **Description**: Test activation based on file patterns
- **Input**:
	- Query: `"create new instruction file"`
	- File Path: `"instructions/new-feature.instructions.md"`
- **Expected**:
	- Instruction-Writer should be activated (YES)
	- Should have file_matches = 1
	- Should have keyword_matches > 0

### Combined Pattern Activation

- **Description**: Test activation using all three pattern types
- **Input**:
	- Query: `"create a new instruction file"`
	- File Path: `"instructions/setup.instructions.md"`
- **Expected**:
	- Instruction-Writer should be activated (YES)
	- Should have keyword_matches = 2
	- Should have intent_matches = 1
	- Should have file_matches = 1
	- Relevance score should be maximum (10)

### Priority-Based Thresholds

- **Description**: Test that different priorities have different activation thresholds
- **Input**: `"create a diagram"`
- **Expected**:
	- Mermaid-Agent should be activated (YES)
	- Priority should be "high"
	- Relevance score should be >= 4

### No Activation Scenario

- **Description**: Test query that should not activate any agents
- **Input**: `"what is the weather today"`
- **Expected**:
	- No agents should be activated
	- activated_agents should be empty
	- additional_context should be empty

### File Path Integration

- **Description**: Test evaluation with file path parameter
- **Input**:
	- Query: `"update documentation"`
	- File Path: `"README.md"`
- **Expected**:
	- file_path should be included in result
	- Diataxis-Documentation-Expert should be activated via file pattern

## Structured Output Tests

### Required vs Suggested Separation

- **Description**: Test that critical/high priority agents go to required, others to suggested
- **Input**: `"create a flowchart and commit changes"`
- **Expected**:
	- Mermaid-Agent and Git-Committer should be in required_agents
	- Neither should be in suggested_agents

### Context Generation

- **Description**: Test that structured context is generated correctly
- **Input**: `"commit changes"`
- **Expected**:
	- additional_context should contain "IMPORTANT GUIDELINES:"
	- Should mention Git Committer agent
	- Should include description and guidelines

## Reasoning Generation Tests

### High Relevance Reasoning

- **Description**: Test reasoning for high relevance scores
- **Input**: Agent "Test-Agent", score 9, keyword_matches 2, intent_matches 1, file_matches 1
- **Expected**:
	- Reasoning should contain "High relevance (9/10)"
	- Should mention all match types

### Moderate Relevance Reasoning

- **Description**: Test reasoning for moderate relevance scores
- **Input**: Agent "Test-Agent", score 6, keyword_matches 1, intent_matches 0, file_matches 0
- **Expected**:
	- Reasoning should contain "Moderate relevance (6/10)"
	- Should mention keyword matches

### Low Relevance Reasoning

- **Description**: Test reasoning for low relevance scores
- **Input**: Agent "Test-Agent", score 2, keyword_matches 0, intent_matches 0, file_matches 0
- **Expected**:
	- Reasoning should contain "Low relevance (2/10)"
	- Should mention "minimal overlap"

## Special Cases

### Git Committer Special Activation

- **Description**: Test that Git-Committer activates on any keyword match
- **Input**: `"git status"`
- **Expected**:
	- Git-Committer should be activated (YES)
	- Should have keyword_matches = 1
	- Special case activation should work

### Context-Aware Boosts

- **Description**: Test context-aware scoring boosts
- **Input**: `"create a custom agent"`
- **Expected**:
	- Meta-Agent should get scoring boost
	- Relevance score should be >= 5

## Agent Configuration Tests

### Agent Initialization

- **Description**: Test that AgentEvaluator initializes with correct agent definitions
- **Expected**:
	- Should have 8 agents
	- All agents should have required fields: description, keywords, file_patterns, intent_patterns, priority, relevance_score

### Priority Distribution

- **Description**: Test that agents have appropriate priority distribution
- **Expected**:
	- Should have at least 1 critical priority agent (Git-Committer)
	- Should have multiple high priority agents
	- Should have medium and low priority agents

## Command Line Interface Tests

### CLI Success Case

- **Description**: Test main function with valid arguments
- **Input**: `['agent_evaluator.py', 'test query']`
- **Expected**:
	- Should output valid JSON
	- Should contain query field
	- Should not exit with error

### CLI With File Path

- **Description**: Test main function with file path argument
- **Input**: `['agent_evaluator.py', 'create instructions', 'instructions/test.instructions.md']`
- **Expected**:
	- Should include file_path in output
	- Should activate appropriate agents

### CLI Error Case

- **Description**: Test main function with insufficient arguments
- **Input**: `['agent_evaluator.py']`
- **Expected**:
	- Should exit with code 1
	- Should output error message
