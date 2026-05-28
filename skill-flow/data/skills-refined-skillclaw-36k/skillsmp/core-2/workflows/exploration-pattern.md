# Codebase Exploration Pattern

## When to Use

Triggers:
- "I need to understand..."
- "Before we start..."
- "Explore the codebase..."
- Starting work in unfamiliar code area

## Pattern: Parallel Exploration

### Step 1: Launch Exploration Agents

```typescript
// File discovery
task({
  agent: "codebase-locator",
  task: "Locate all files related to [TOPIC]. Include: main implementation, tests, config, types."
});

// Pattern analysis
task({
  agent: "codebase-pattern-finder",
  task: "Identify patterns in [TOPIC]: naming conventions, architectural patterns, common utilities."
});

// Architecture documentation
task({
  agent: "codebase-analyzer",
  task: "Analyze architecture of [TOPIC]: dependencies, data flow, entry points, external interfaces."
});
```

### Step 2: Synthesis

```typescript
// Spotcheck synthesis
task({
  agent: "agent",
  task: `SPOTCHECK: Synthesize exploration findings.

Create:
1. Mermaid diagram of architecture
2. List of key files and their roles
3. Identified patterns and conventions
4. Dependencies and integration points
5. Risk areas and constraints

Output to: working/exploration-[topic].md`
});
```

### Step 3: Document Assumptions

Update `working/session-context.md`:
```markdown
## Exploration: [Topic]

**Architecture**: [Key insights]
**Patterns**: [Conventions found]
**Constraints**: [Limitations discovered]
**Risks**: [What could go wrong]
```

## Duration

Typical: 5-15 minutes
Complex: 20-30 minutes

## Output

- `working/exploration-[topic].md` - Full findings
- `working/session-context.md` - Key assumptions
- Mermaid diagram (if complex)

## Next Steps

After exploration:
1. If complex → Use /plan mode
2. If clear → Proceed with implementation
3. If uncertain → Ask clarifying questions
