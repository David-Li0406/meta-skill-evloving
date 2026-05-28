# With-Codex Workflows Reference

Detailed workflow documentation for Claude and Codex collaboration.

## Workflow Details and Examples

### Second Opinion Workflow

**When to use**: User explicitly asks for a second opinion, wants validation, or says something like "what would Codex say about this?"

**Process**:

1. **Formulate Claude's answer first**
   - Complete your analysis independently
   - Document your reasoning and approach

2. **Query Codex for comparison**

   ```bash
   wsl bash -c 'codex exec "Question: [exact user question]

   Context: [any relevant context]

   Please provide your analysis and recommended approach." 2>/dev/null'
   ```

3. **Analyze differences**
   - Identify points of agreement
   - Note alternative approaches
   - Consider trade-offs of each approach

4. **Present synthesized response**

   ```markdown
   ## Analysis Comparison

   ### Claude's Approach
   [Your detailed analysis]

   ### Codex's Approach
   [Codex's response]

   ### Synthesis
   Both approaches agree on [X, Y, Z].

   Key differences:
   - Claude suggests [A] while Codex suggests [B]
   - Trade-off analysis: [explanation]

   **Recommendation**: [Best combined approach with reasoning]
   ```

### Collaborative Task Division Workflow

**When to use**: Complex tasks that benefit from multiple perspectives, large implementations, or when the user wants to leverage both AIs.

**Process**:

1. **Analyze and divide the task**
   - Claude focuses on: High-level design, architecture, patterns, documentation
   - Codex handles: Implementation details, edge cases, testing, performance

2. **Query Codex for specific sub-tasks**

   ```bash
   wsl bash -c 'codex exec "Task: Implement [specific component]

   Requirements:
   - [requirement 1]
   - [requirement 2]

   Focus on: error handling, edge cases, and input validation." 2>/dev/null'
   ```

3. **Integrate and refine**
   - Review Codex's output
   - Integrate with your architectural decisions
   - Add documentation and explanations

### Interactive Visual Mode Workflow

**When to use**: User explicitly requests visual split-pane mode, wants to see both AIs working side-by-side, or for demo/teaching purposes.

**Setup sequence**:

```bash
# 1. Initialize the tmux session
wsl bash -c '<skill-path>/scripts/codex-manager.sh setup'

# 2. Send a prompt
wsl bash -c '<skill-path>/scripts/codex-manager.sh send "Analyze the trade-offs of using Redis vs Memcached for session storage"'

# 3. Wait for response (with timeout)
wsl bash -c '<skill-path>/scripts/codex-manager.sh wait 30'

# 4. Capture the response
CODEX_RESPONSE=$(wsl bash -c '<skill-path>/scripts/codex-manager.sh capture 150')

# 5. When done, cleanup
wsl bash -c '<skill-path>/scripts/codex-manager.sh cleanup'
```

## Response Parsing Strategies

### Parsing Non-Interactive Output

The `codex exec` command outputs the final response to stdout. To parse:

```bash
# Capture to variable
RESPONSE=$(wsl bash -c 'codex exec "your prompt" 2>/dev/null')

# Save to file
wsl bash -c 'codex exec "your prompt" 2>/dev/null' > /tmp/codex_response.txt
```

### Parsing Interactive Mode Captures

The captured pane content includes terminal formatting. Key patterns:

- Look for response markers in Codex output
- Filter out prompt lines (usually start with `>` or specific markers)
- Extract the substantive response content

## Error Handling

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| "Codex CLI not found" | Install Codex in WSL: `npm install -g @openai/codex` |
| "Authentication failed" | Run `codex login` in WSL to re-authenticate |
| Timeout waiting for response | Increase timeout or use non-interactive mode |
| tmux session conflicts | Run `cleanup` before `setup` |
| Empty response captured | Increase wait time before capture |

### Graceful Degradation

If Codex is unavailable:

1. Inform the user that Codex is not accessible
2. Offer to proceed with Claude-only analysis
3. Suggest troubleshooting steps

## Best Practices

1. **Prefer non-interactive mode** for reliability and speed
2. **Use interactive mode** only when visual collaboration is explicitly requested
3. **Always escape special characters** in shell commands
4. **Set appropriate timeouts** based on query complexity
5. **Present unbiased comparisons** - let the user decide which approach is better
6. **Acknowledge limitations** - both AIs can be wrong

## Example Prompts for Different Use Cases

### Architecture Review

```plain
Review this architecture decision:
[description]

Consider: scalability, maintainability, and trade-offs.
```

### Bug Analysis

```plain
Analyze this code for potential bugs:
[code]

Focus on: edge cases, null handling, and race conditions.
```

### Performance Review

```plain
Review this code for performance issues:
[code]

Consider: time complexity, memory usage, and optimization opportunities.
```

### Security Review

```plain
Review this code for security vulnerabilities:
[code]

Focus on: input validation, injection attacks, and authentication issues.
```
