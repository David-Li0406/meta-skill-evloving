---
name: example-holon
description: Example skill demonstrating the holon pattern with bounded episode execution, stop conditions, and tool restrictions.
user-invocable: false
holon:
  # ============================================================================
  # Contract Definition
  # ============================================================================
  # The contract defines the input/output types for this holon. These are
  # type identifiers that document the expected data shapes. In a full
  # implementation, these would map to concrete Rust types.
  #
  # Design Decision: DEC-RFC-3001 - Holon as Async Trait with Associated Types
  # The contract surface is specified declaratively here and enforced at runtime.
  contract:
    # Input type: What the holon accepts when work is assigned via intake()
    input_type: TaskRequest

    # Output type: What the holon produces when work completes successfully
    output_type: TaskResult

    # State type: Internal state accessible for checkpointing (optional)
    state_type: TaskProgress

  # ============================================================================
  # Stop Conditions
  # ============================================================================
  # Stop conditions define when the holon should terminate its episode loop.
  # At least one stop condition MUST be configured to prevent unbounded execution.
  #
  # Design Decision: DEC-RFC-3004 - Episode Stop Condition Evaluation
  # Stop conditions are evaluated after each episode in priority order:
  #   1. Budget exhaustion (any resource dimension)
  #   2. Explicit completion signal (GoalSatisfied)
  #   3. Error threshold
  #   4. Max episodes reached
  #   5. Timeout reached
  #
  # Security Note: Omitting all stop conditions is rejected at parse time.
  # This prevents unbounded resource consumption by agents.
  stop_conditions:
    # Maximum number of episodes before forced termination.
    # This acts as a safety limit even if the holon doesn't signal completion.
    # Typical values: 5-100 depending on task complexity.
    max_episodes: 10

    # Timeout in milliseconds.
    # Total wall-clock time allowed for all episodes combined.
    # Typical values: 60000 (1 min) to 3600000 (1 hour).
    timeout_ms: 300000

    # Budget limits for various resources.
    # The episode loop terminates when any resource dimension is exhausted.
    # Resource names are arbitrary strings; common dimensions include:
    #   - tokens: LLM token consumption
    #   - tool_calls: Number of tool invocations
    #   - api_requests: External API calls
    budget:
      tokens: 50000
      tool_calls: 100

    # Maximum number of "stall" episodes before escalation.
    # A stall is when no observable progress is made (progress_update is None
    # or unchanged). This prevents infinite loops where the agent makes no
    # meaningful progress.
    max_stall_episodes: 3

  # ============================================================================
  # Tool Permissions
  # ============================================================================
  # Defines which tools this holon is allowed to invoke.
  #
  # Security Model (Fail-Close):
  #   - `tools` omitted (None): No tools permitted (maximum restriction)
  #   - `tools: []` (empty list): No tools permitted
  #   - `tools: [read_file, write_file]`: Only listed tools permitted
  #
  # This prevents fail-open behavior where omitting the field would
  # accidentally grant access to all tools.
  #
  # Design Decision: DEC-RFC-3003 - Lease Derivation for Sub-Holons
  # When this holon spawns sub-holons, their tool access is the intersection
  # of the parent's tools and the requested tools (subset only).
  tools:
    - read_file
    - write_file
    - glob
    - grep
---

# Example Holon Skill

This skill demonstrates the holon pattern for bounded agent execution. It serves
as a reference implementation and test fixture for the APM2 holonic coordination
framework.

## Purpose

The example-holon skill illustrates:

1. **Bounded Execution**: Episodes execute within resource limits
2. **Stop Conditions**: Multiple termination criteria prevent unbounded runs
3. **Tool Restrictions**: Explicit allowlist enforces least-privilege access
4. **Contract Surface**: Clear input/output type definitions

## Usage Pattern

When loaded as a holon, this skill:

1. Receives work via `intake()` with a `TaskRequest` input
2. Executes bounded episodes via `execute_episode()`
3. Evaluates stop conditions after each episode
4. Produces `TaskResult` output on successful completion
5. Escalates to supervisor if work cannot be completed

## Episode Lifecycle

```
+----------------+     +----------------+     +----------------+
|   Intake       | --> | Execute Episode| --> | Evaluate Stop  |
| (validate work)|     | (bounded work) |     | (check limits) |
+----------------+     +----------------+     +-------+--------+
                                                      |
                           +--------------------------+
                           |
     +---------------------+---------------------+
     v                     v                     v
+---------+          +-----------+         +----------+
| Continue|          | Completed |         | Escalate |
| (loop)  |          | (done)    |         | (hand-off)|
+---------+          +-----------+         +----------+
```

## Stop Conditions

The skill is configured with multiple stop conditions:

| Condition | Value | Description |
|-----------|-------|-------------|
| `max_episodes` | 10 | Hard limit on episode count |
| `timeout_ms` | 300000 | 5 minute wall-clock limit |
| `budget.tokens` | 50000 | Token consumption limit |
| `budget.tool_calls` | 100 | Tool invocation limit |
| `max_stall_episodes` | 3 | Progress stall detection |

## Tool Permissions

The skill has restricted tool access:

- `read_file`: Read file contents
- `write_file`: Write file contents
- `glob`: File pattern matching
- `grep`: Content search

Tools not in this list are denied (fail-close security model).

## Integration with spawn_holon

This skill can be executed via the `spawn_holon` orchestration function:

```rust
use apm2_holon::spawn::{spawn_holon, SpawnConfig};
use apm2_holon::resource::{Budget, LeaseScope};
use apm2_holon::skill::parse_skill_file;

// Parse skill frontmatter
let (frontmatter, _body) = parse_skill_file("documents/skills/example-holon/SKILL.md")?;
let holon_config = frontmatter.holon.expect("example-holon has holon config");

// Build spawn configuration from skill config
let config = SpawnConfig::builder()
    .work_id("example-work-001")
    .work_title("Example holon execution")
    .issuer_id("registrar")
    .holder_id("example-holon")
    .scope(LeaseScope::builder()
        .tools(holon_config.allowed_tools().unwrap_or(&[]))
        .build())
    .budget(Budget::new(
        holon_config.stop_conditions.max_episodes.unwrap_or(10),
        holon_config.stop_conditions.budget.get("tool_calls").copied().unwrap_or(100),
        holon_config.stop_conditions.budget.get("tokens").copied().unwrap_or(50000),
        holon_config.stop_conditions.timeout_ms.unwrap_or(300000),
    ))
    .build()?;

// Execute the holon
let result = spawn_holon(&mut holon, input, config, || current_time_ns())?;
```

## Related Documentation

- [RFC-0003: Holonic Framework](../../../documents/rfcs/RFC-0003/00_meta.yaml)
- [Principia Holonica](../holonic-agent-network/references/principia-holonic.md)
- [apm2-holon AGENTS.md](../../../crates/apm2-holon/AGENTS.md)

## Invariants

1. At least one stop condition is always configured (enforced at parse time)
2. Tool access follows fail-close semantics (omitted = denied)
3. Budget exhaustion triggers graceful termination, not error
4. Escalation preserves work state for supervisor continuation
5. All stop condition values must be > 0 (validated at parse time)
