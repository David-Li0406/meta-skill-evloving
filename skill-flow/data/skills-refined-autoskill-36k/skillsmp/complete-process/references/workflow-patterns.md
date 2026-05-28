# Workflow Patterns

Common workflow patterns for the Complete Process Orchestrator.

## Pipeline Patterns

### Automated Linear Pipeline (Complete Mode) - FULLY AUTOMATED
```
Input → Transform → Validate → Optimize → Output + Todos
```

**Characteristics**:
- **FULLY AUTOMATED**: Runs continuously without user intervention
- Sequential execution with structured agent communication
- Each agent outputs workflow signals (WORKFLOW_CONTINUES, NEXT_AGENT)
- Orchestrator checks signals and invokes next agent automatically
- Full traceability with chain progress tracking
- Final step generates implementation todos automatically

**Agent Communication Protocol**:
```
1. Transform Agent outputs:
   - Transformed pseudo-code
   - WORKFLOW_CONTINUES: YES
   - NEXT_AGENT: requirement-validator

2. Orchestrator reads output → Invokes requirement-validator immediately

3. Validator Agent outputs:
   - Validation report
   - WORKFLOW_CONTINUES: YES
   - NEXT_AGENT: prompt-optimizer

4. Orchestrator reads output → Invokes prompt-optimizer immediately

5. Optimizer Agent outputs:
   - Optimized pseudo-code
   - TODO_LIST: [implementation tasks]
   - WORKFLOW_CONTINUES: NO
   - CHAIN_COMPLETE: All steps finished

6. Orchestrator reads output → Creates todos with TodoWrite → Done
```

**Use When**:
- Quality is priority over speed
- Need comprehensive validation
- Production-ready output required
- Want automated end-to-end transformation

### Fast-Track Pipeline (Quick Mode)
```
Input → Transform → Output
```

**Characteristics**:
- Minimal processing
- No intermediate steps
- Fast execution
- Basic validation only

**Use When**:
- Speed is priority
- Simple, clear requirements
- Prototyping or exploration
- Iterative refinement

### Conditional Pipeline
```
Input → Transform → [User Decision] → Quick Exit
                                    → Continue → Validate → Optimize
```

**Characteristics**:
- User controls execution path
- Saves time when quick transform sufficient
- Option to upgrade to full pipeline
- Preference-based routing

**Use When**:
- User knows their needs vary
- Want flexibility per query
- Learning what mode fits which queries

## Error Handling Patterns

### Fail-Fast Pattern
```
Transform [Error] → Abort Pipeline → Return Error
```

**Use When**:
- Critical errors that can't be recovered
- Invalid input that needs user correction
- Resource unavailability

**Example**:
```
Query: [empty string]
→ Input Validation Error
→ Pipeline Aborted
→ User Message: "Query must be between 10-5000 characters"
```

### Graceful Degradation Pattern
```
Transform → Validate [Warning] → Ask User → Continue → Optimize
                                          → Stop → Return Validated
```

**Use When**:
- Non-critical warnings found
- User can decide risk acceptance
- Optimization might fix warnings

**Example**:
```
Query: "Add authentication"
→ Transform Success
→ Validation Warning: "Missing error handling"
→ User Choice: Continue to optimization
→ Optimize: Adds error handling
→ Success
```

### Rollback Pattern
```
Transform → Checkpoint → Validate [Error] → Rollback to Transform
```

**Use When**:
- Step fails but previous work is valid
- User wants to retry or adjust
- Partial results are useful

**Example**:
```
Transform ✓ → Validate ✗ → Optimize [Not Started]
User gets: Transformed pseudo-code + validation report
Can: Use transform output OR revise query and retry
```

### Retry with Fallback Pattern
```
Optimize [Timeout] → Retry (1/3) → Retry (2/3) → Fallback to Validated Output
```

**Use When**:
- Transient failures possible
- Network or resource issues
- Step has valid fallback

**Example**:
```
Optimize: Timeout after 45s
→ Retry 1: Timeout
→ Retry 2: Timeout
→ Fallback: Return validated pseudo-code with warning
```

## State Management Patterns

### Checkpoint Pattern
```
Transform → [Save State] → Validate → [Save State] → Optimize → [Save State]
```

**Benefits**:
- Resume on failure
- Audit trail
- Debugging capability
- Recovery options

**Implementation**:
```
Checkpoint {
  step_name: "validate",
  status: "completed",
  output: {...},
  timestamp: "2026-01-18T12:00:00Z",
  duration: "12s"
}
```

### In-Memory Handoff Pattern
```
Transform → [Memory Buffer] → Validate → [Memory Buffer] → Optimize
```

**Benefits**:
- Fast data transfer
- No I/O overhead
- Reduced latency
- Simpler implementation

**Use When**:
- Steps run in same process
- Output size is reasonable (< 1MB)
- Performance is critical

### Persistent State Pattern
```
Transform → [Save to Disk] → Validate → [Save to Disk] → Optimize
```

**Benefits**:
- Survives crashes
- Large output handling
- Cross-session resume
- Debugging with saved states

**Use When**:
- Long-running pipelines
- Large intermediate outputs
- Resume capability needed
- Audit requirements exist

## User Interaction Patterns

### Upfront Decision Pattern
```
[Mode Selection UI] → Execute Selected Pipeline → Return Results
```

**Flow**:
1. Show mode options
2. User selects
3. Execute without further interaction
4. Return final results

**Best For**: Most common use case

### Progressive Disclosure Pattern
```
Start Pipeline → [Issue Found] → Ask User → Continue Based on Response
```

**Flow**:
1. Start with default mode
2. Pause if issues arise
3. Present options to user
4. Continue based on choice

**Best For**: Handling unexpected situations

### Preference-Based Pattern
```
[Load Saved Preference] → Execute Preferred Mode → [Update Preference if Changed]
```

**Flow**:
1. Load last choice
2. Show as default
3. Allow override
4. Execute selected
5. Save if changed

**Best For**: Returning users with consistent needs

## Integration Patterns

### Skill Invocation Pattern
```
Orchestrator
    ├─→ Invoke prompt-structurer skill
    ├─→ Invoke requirement-validator skill
    └─→ Invoke prompt-optimizer skill
```

**Implementation**:
```javascript
// Pseudo-code
result = invoke_skill("prompt-structurer", query)
if complete_mode:
  result = invoke_skill("requirement-validator", result)
  result = invoke_skill("prompt-optimizer", result)
return result
```

### Command Reuse Pattern
```
Orchestrator
    ├─→ Execute /transform-query command
    ├─→ Execute /validate-requirements command
    └─→ Execute /optimize-prompt command
```

**Benefits**:
- Leverages existing commands
- No code duplication
- Consistent behavior
- Easy testing

### Cache Integration Pattern
```
Query → [Check Semantic Cache] → Cache Hit → Return Cached
                                → Cache Miss → Execute Pipeline → Cache Result
```

**Benefits**:
- Instant results for repeated queries
- Reduced processing time
- Lower resource usage

**Implementation**:
```bash
# Execute pipeline
execute_pipeline
return_result
```

## Performance Patterns

### Timeout Management Pattern
```
[Start Timer] → Execute Step → [Monitor Duration] → Warn at 80% → Timeout at 100%
```

**Timeouts**:
- Transform: 30s (warn at 24s)
- Validate: 15s (warn at 12s)
- Optimize: 45s (warn at 36s)
- Total: 120s (warn at 96s)

**Benefits**:
- Prevents hanging
- User awareness
- Graceful failure

### Parallel Execution Pattern (Future)
```
Transform → Split
            ├─→ Validate (parallel)
            └─→ Syntax Check (parallel)
            Merge → Optimize
```

**Benefits**:
- Faster execution
- Better resource utilization
- Independent validations

**Note**: Not implemented in v1.0.0, planned for future

### Lazy Loading Pattern
```
Load Orchestrator → Load Dependencies On-Demand → Execute
```

**Flow**:
1. Orchestrator loads quickly
2. Skills loaded when needed
3. Only selected mode's skills loaded

**Benefits**:
- Faster startup
- Reduced memory
- Efficient resource use

## Decision Flow Patterns

### Quick vs Complete Decision Tree
```
User Query
    ├─→ Simple query? → Quick Mode
    │       ├─→ < 50 words
    │       ├─→ Single action
    │       └─→ Clear requirements
    │
    └─→ Complex query? → Complete Mode
            ├─→ Multiple parameters
            ├─→ Security requirements
            ├─→ Production feature
            └─→ Validation needed
```

### Error Recovery Decision Tree
```
Error Occurred
    ├─→ Critical Error?
    │       ├─→ Invalid Input → Abort + Error Message
    │       ├─→ Resource Unavailable → Abort + Retry Later
    │       └─→ Dependency Missing → Abort + Install Guide
    │
    └─→ Non-Critical Error?
            ├─→ Warning → Ask User → Continue or Stop
            ├─→ Timeout → Return Partial Results
            └─→ Optimization Failed → Return Validated Output
```

## Metrics Collection Patterns

### Anonymous Metrics Pattern
```
Pipeline Execution
    ├─→ Track: mode, duration, success/failure
    ├─→ Aggregate: counts, averages, rates
    └─→ Store: .claude/plugin_metrics.json
    └─→ Never: PII, query content, user identity
```

**Collected**:
- Mode selection frequency
- Step durations
- Success/failure rates
- Error types

**Not Collected**:
- Query content
- User identity
- File paths
- Sensitive data

### Performance Monitoring Pattern
```
[Start Timestamp] → Execute Step → [End Timestamp] → Calculate Duration → Log Metric
```

**Tracked Metrics**:
```json
{
  "step": "validate",
  "duration_ms": 8500,
  "status": "success",
  "warnings": 2,
  "timestamp": "2026-01-18T12:00:00Z"
}
```

## Common Workflow Scenarios

### Scenario 1: First-Time User
```
1. User runs /complete-process
2. No preference found
3. Show mode selection with descriptions
4. User selects "Complete" (recommended)
5. Execute full pipeline
6. Save preference
7. Next time: Auto-suggest "Complete"
```

### Scenario 2: Quick Iteration
```
1. User has complex feature idea
2. Runs complete mode → Gets optimized output
3. Realizes needs tweaking
4. Runs quick mode for iterations
5. Once refined, runs complete mode again
6. Gets final validated output
```

### Scenario 3: Validation Failure Recovery
```
1. User runs complete mode
2. Transform succeeds
3. Validation finds critical issues
4. User presented with options:
   a. Abort and revise query
   b. Continue to optimize (might fix issues)
   c. Return validated output as-is
5. User chooses (b)
6. Optimization adds missing parameters
7. Final output passes all checks
```

### Scenario 4: Large Query Handling
```
1. User pastes 4000-character requirement
2. System warns: "Consider /compress-context first"
3. User compresses context
4. Runs complete mode on compressed version
5. Gets optimized output
6. Implementation-ready
```

## Best Practices

### Pattern Selection
- **Default to Complete Mode** for production work
- **Use Quick Mode** for iteration and exploration
- **Leverage Preferences** to reduce repeated choices
- **Monitor Metrics** to optimize workflow

### Error Handling
- **Always checkpoint** after successful steps
- **Preserve user input** on failures
- **Provide clear options** when errors occur
- **Log for debugging** but never expose sensitive data

### Performance
- **Set realistic timeouts** based on query complexity
- **Warn users early** when approaching limits
- **Return partial results** better than nothing
- **Cache aggressively** for repeated patterns

### User Experience
- **Show progress** for multi-step operations
- **Remember preferences** to reduce friction
- **Provide clear feedback** at each decision point
- **Enable recovery** from any failure state

## Future Patterns (Roadmap)

### Parallel Execution
Execute validation and syntax checking simultaneously for faster results.

### Adaptive Timeouts
Adjust timeouts based on query complexity and historical performance.

### Smart Mode Selection
Auto-detect query complexity and suggest best mode without prompting.

### Background Execution
Allow long-running complete modes to execute in background.

### Batch Processing
Process multiple queries through the same pipeline configuration.

### A/B Testing
Compare quick vs complete mode results for learning and optimization.
