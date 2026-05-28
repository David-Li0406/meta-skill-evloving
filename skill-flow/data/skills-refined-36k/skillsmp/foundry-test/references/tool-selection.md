# AI Consultation

## When to Consult

**Mandatory** when research tools are available and:
- Failure cause is unclear after initial investigation
- Multiple potential root causes identified
- Flaky or non-deterministic behavior
- Complex multi-file interactions

**Skip** when:
- Failure is obvious (typo, missing import)
- Fix is straightforward
- Research tools unavailable

## Research Actions

### chat - Standard Consultation

Single AI conversation for focused debugging analysis.

```
mcp__plugin_foundry_foundry-mcp__research action="chat" prompt="..." system_prompt="You are debugging a test failure."
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| prompt | Yes | Your debugging question with error details |
| system_prompt | No | Context for the AI (e.g., "You are debugging Python tests") |
| thread_id | No | Continue previous conversation |

**Best for:** Most debugging scenarios, quick diagnosis.

### consensus - Multi-Perspective Analysis

Consult multiple AI providers and synthesize their responses.

```
mcp__plugin_foundry_foundry-mcp__research action="consensus" prompt="..." strategy="synthesize"
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| prompt | Yes | Your debugging question |
| strategy | No | How to combine responses (see below) |
| system_prompt | No | Context for all providers |

**Strategy options:**
- `synthesize` (default) - AI synthesizes all responses into coherent answer
- `all_responses` - Return all responses without synthesis
- `majority` - Use majority agreement (good for factual questions)
- `first_valid` - Return first successful response

**Best for:** Complex failures, architectural issues, when you want multiple opinions.

### thinkdeep - Systematic Investigation

Hypothesis-driven analysis for complex debugging scenarios.

```
mcp__plugin_foundry_foundry-mcp__research action="thinkdeep" topic="..." query="..."
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| topic | Yes | Initial topic for investigation |
| query | No | Follow-up query (for continuing investigation) |
| investigation_id | No | Resume previous investigation |
| max_depth | No | Maximum investigation depth |

**Best for:**
- Complex failures with multiple potential causes
- When you need to form and systematically test hypotheses
- Multi-step debugging requiring investigation tree
- When chat/consensus didn't yield clear answers

## Prompt Templates

### For Assertion Failures
```
mcp__plugin_foundry_foundry-mcp__research action="chat" prompt="Test {test_name} in {file} fails with assertion error.

Expected: {expected}
Actual: {actual}

Test purpose: {test_purpose}
Implementation:
{relevant_code}

What is causing the mismatch?" system_prompt="You are debugging test assertions. Focus on data flow and state."
```

### For Exception Failures
```
mcp__plugin_foundry_foundry-mcp__research action="chat" prompt="Test {test_name} raises {error_type}: {error_message}

Stack trace:
{stack_trace}

What is causing this and how should it be fixed?" system_prompt="You are debugging runtime errors. Analyze the stack trace carefully."
```

### For Flaky Tests (use consensus)
```
mcp__plugin_foundry_foundry-mcp__research action="consensus" prompt="Test {test_name} fails intermittently.

Fails when: {when_it_fails}
Passes when: {when_it_passes}

Test code:
{test_code}

What could cause non-deterministic behavior?" strategy="synthesize" system_prompt="You are diagnosing flaky tests. Consider race conditions, timing, and shared state."
```

### For Import/Module Failures
```
mcp__plugin_foundry_foundry-mcp__research action="chat" prompt="Test fails with import error: {error_message}

Project structure:
{relevant_structure}

Module path: {module_path}

What is causing the import to fail?"
```

### For Timeout/Performance
```
mcp__plugin_foundry_foundry-mcp__research action="chat" prompt="Test {test_name} times out.

Expected: {expected_duration}
Actual: {actual_duration}

Test does:
{test_description}

What could cause the performance issue?"
```

## Interpreting Results

**Good signals:**
- Specific code location identified
- Clear explanation of root cause
- Actionable fix suggested

**Investigate further if:**
- Multiple conflicting hypotheses
- Suggestion doesn't match observed behavior
- Fix seems too complex for the symptom

**Using consensus results:**
- Check if providers agree → high confidence
- Providers disagree → investigate both hypotheses
- Synthesis unclear → try with different prompt or `all_responses` strategy
