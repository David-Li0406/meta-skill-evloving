# GUI Agent Code Review Checklist

Complete review criteria organized by domain. Use this checklist when reviewing code changes to the GUI Agent project.

## Domain 1: LLM Prompts (prompt-engineer)

### Clarity and Structure

- [ ] **Unambiguous instructions**: Each instruction has one clear interpretation
- [ ] **Consistent terminology**: Uses same terms as codebase (e.g., "normalized coordinates" not "relative position")
- [ ] **Logical ordering**: Instructions flow from context → task → constraints → output format
- [ ] **Role definition**: Clear "You are..." opening that establishes agent persona

### Structured Output

- [ ] **JSON schema specified**: Output format references Pydantic model or explicit schema
- [ ] **Field descriptions**: Each output field has clear purpose explained
- [ ] **Type constraints**: Numeric ranges, string patterns, enum values specified
- [ ] **Required vs optional**: Clear indication of which fields must be present

### Token Efficiency

- [ ] **No redundant examples**: Single clear example preferred over multiple similar ones
- [ ] **Concise phrasing**: Avoid verbose explanations when brief ones suffice
- [ ] **Deduplication**: Same information not repeated in different sections
- [ ] **Appropriate detail level**: Match verbosity to task complexity

### Action Guidance

- [ ] **Available actions listed**: All ActionType values documented with usage
- [ ] **Parameter requirements**: What each action needs (coordinates, text, keys)
- [ ] **When to use each**: Clear guidance on action selection
- [ ] **Common patterns**: Multi-step sequences for complex tasks

### Error Handling Prompts

- [ ] **Recovery instructions**: What to do when action fails
- [ ] **Retry guidance**: When to retry vs. try alternative approach
- [ ] **Completion criteria**: How to know task is done
- [ ] **Failure reporting**: Format for explaining what went wrong

---

## Domain 2: Execution Debugging (plan-debugger)

### Error Context

- [ ] **Action included**: Error message contains what action was attempted
- [ ] **Parameters logged**: Coordinates, text, or other inputs recorded
- [ ] **State captured**: Screenshot or screen state at failure time
- [ ] **Sequence position**: Where in multi-step plan failure occurred

### Screenshot Artifacts

- [ ] **Before screenshot**: Captured before action execution
- [ ] **After screenshot**: Captured after action (success or failure)
- [ ] **Grid overlay option**: Screenshots can include coordinate grid
- [ ] **Timestamp naming**: Screenshots identifiable by when taken

### Logging Quality

- [ ] **Structured format**: JSON or consistent parseable format
- [ ] **Severity levels**: DEBUG, INFO, WARNING, ERROR used appropriately
- [ ] **Correlation IDs**: Related log entries can be grouped
- [ ] **Sensitive data**: No secrets or PII in logs

### Recovery Paths

- [ ] **Graceful degradation**: Partial failure doesn't crash entire task
- [ ] **Retry logic**: Transient failures have retry mechanism
- [ ] **Alternative actions**: Backup approach when primary fails
- [ ] **User notification**: User informed of failures requiring intervention

### Traceability

- [ ] **Action history**: Complete record of actions attempted
- [ ] **Decision points**: Why specific action was chosen
- [ ] **State transitions**: How screen state changed between actions
- [ ] **Timing info**: Duration of actions and waits

---

## Domain 3: Context Management (context-optimizer)

### KV-Cache Stability

- [ ] **Stable prefix**: System prompt + tools never modified after init
- [ ] **Append-only history**: New content added, never inserted/modified
- [ ] **No mid-session changes**: Prefix content frozen for session
- [ ] **Deterministic ordering**: Same conversation produces same prefix

### Token Budget

- [ ] **Budget defined**: ContextConfig.max_tokens set appropriately
- [ ] **Component allocation**: Clear budget for each context section
- [ ] **Monitoring**: Token count tracked and logged
- [ ] **Threshold triggers**: Compression triggered before overflow

### History Compression

- [ ] **Task info preserved**: Critical details survive compression
- [ ] **Configurable threshold**: compression_threshold in ContextConfig
- [ ] **Summarization quality**: Compressed history still useful
- [ ] **Recent pairs kept**: min_recent_pairs respected

### Checkpoint/Restore

- [ ] **Serializable state**: Context can be saved to disk
- [ ] **Restore fidelity**: Restored context matches original
- [ ] **Version compatibility**: Old checkpoints work with new code
- [ ] **context_dir used**: Checkpoints go to configured directory

### Image Handling

- [ ] **Token cost awareness**: ~1500 tokens per image accounted for
- [ ] **History images**: Old screenshots compressed or removed
- [ ] **Current image only**: Only latest screenshot in full detail
- [ ] **Base64 encoding**: Images properly encoded for API

---

## Domain 4: Action Design (action-designer)

### Schema Completeness

- [ ] **ActionType enum**: New action added to enum class
- [ ] **NextAction fields**: Required parameters added to model
- [ ] **Field validation**: Pydantic validators for constraints
- [ ] **Default values**: Sensible defaults for optional params

### Executor Integration

- [ ] **Dispatch case**: elif branch in InputController.execute()
- [ ] **Parameter extraction**: Fields correctly read from action
- [ ] **Validation check**: Required params verified before use
- [ ] **Error return**: Missing params return (False, "message")

### Implementation Method

- [ ] **Naming convention**: _action_name() private method
- [ ] **Return type**: tuple[bool, str] for success/message
- [ ] **PyAutoGUI call**: Correct function with parameters
- [ ] **Action delay**: time.sleep(config.action_delay) after action
- [ ] **Exception handling**: try/except with error message

### Coordinate Handling

- [ ] **Normalized input**: Coordinates expected as 0.0-1.0
- [ ] **Pixel conversion**: Multiply by screen dimensions
- [ ] **Screen size**: Use pyautogui.size() not hardcoded
- [ ] **Bounds checking**: Coordinates within screen limits

### Cross-Platform

- [ ] **macOS compatibility**: Works on macOS
- [ ] **Windows compatibility**: Works on Windows (if required)
- [ ] **Linux compatibility**: Works on Linux (if required)
- [ ] **Permission handling**: Accessibility permissions noted

---

## Domain 5: Screenshot Analysis (screenshot-analyzer)

### Coordinate System

- [ ] **Normalized coordinates**: All positions as 0.0-1.0
- [ ] **Origin consistency**: (0,0) at top-left corner
- [ ] **Axis direction**: X increases right, Y increases down
- [ ] **No pixel leakage**: Pixel values not exposed to LLM

### Grid Overlay

- [ ] **add_grid parameter**: Respects configuration
- [ ] **Grid interval**: Lines at 0.1 intervals (configurable)
- [ ] **Label readability**: Text visible against background
- [ ] **Non-destructive**: Original screenshot preserved

### Resolution Independence

- [ ] **Dynamic dimensions**: Uses actual screen size
- [ ] **Scaling handled**: Works with display scaling
- [ ] **Aspect ratio**: Calculations account for non-16:9
- [ ] **Multi-monitor**: Primary screen correctly identified

### Pixel Conversion

```python
# Correct pattern
pixel_x = normalized_x * screen_width
pixel_y = normalized_y * screen_height

# Inverse conversion
normalized_x = pixel_x / screen_width
normalized_y = pixel_y / screen_height
```

- [ ] **Conversion direction**: Normalized → Pixel for execution
- [ ] **Integer rounding**: Pixel values are integers
- [ ] **Boundary handling**: Edge coordinates handled correctly

### Image Quality

- [ ] **Format appropriate**: PNG for quality, JPEG for size
- [ ] **Compression level**: Balanced quality/size for LLM
- [ ] **Color depth**: Sufficient for element identification
- [ ] **File size**: Not exceeding practical limits

---

## Cross-Domain Checks

### Prompt ↔ Action Consistency

- [ ] Prompt documents all available ActionTypes
- [ ] Prompt parameter guidance matches NextAction fields
- [ ] Examples in prompt use correct action schemas

### Action ↔ Screenshot Consistency

- [ ] Actions receive normalized coordinates
- [ ] Screenshot grid matches coordinate system
- [ ] Click targets align with grid labels

### Context ↔ Prompt Consistency

- [ ] System prompt in stable prefix
- [ ] Compression preserves action guidance
- [ ] Token budget accounts for prompt size

### Screenshot ↔ Debugging Consistency

- [ ] Failed actions have associated screenshots
- [ ] Coordinates logged with screenshots
- [ ] Grid overlay available for debugging

---

## Severity Guidelines

### Critical (Must Fix)

- Security vulnerabilities
- Data loss potential
- Breaking changes to public API
- KV-cache prefix mutation
- Coordinate system bugs (clicks wrong location)

### Important (Should Fix)

- Missing error handling
- Token budget violations
- Incomplete action implementation
- Missing logging for failures
- Undocumented behavior changes

### Minor (Nice to Fix)

- Code style inconsistencies
- Minor token inefficiency
- Missing optional fields
- Documentation gaps
- Test coverage gaps

---

## Review Output Template

```markdown
## Code Review: [filename or feature]

### Summary
[1-2 sentence overview of changes and overall assessment]

### Critical Issues
[List any critical issues that must be addressed]

### Important Issues
[List important issues that should be addressed]

### Minor Issues
[List minor issues for consideration]

### Positive Notes
[Acknowledge good patterns or improvements]

### Checklist Domains Reviewed
- [ ] Prompts
- [ ] Debugging
- [ ] Context
- [ ] Actions
- [ ] Screenshots
```
