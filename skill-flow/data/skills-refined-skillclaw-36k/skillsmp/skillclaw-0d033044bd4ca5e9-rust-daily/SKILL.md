---
name: rust-daily
description: Use this skill to fetch and report on Rust community updates, filtered by daily, weekly, or monthly time ranges.
---

# Rust Daily Report

Fetch Rust community updates, filtered by time range.

## Data Sources

| Category | Sources |
|----------|---------|
| Ecosystem | Reddit r/rust, This Week in Rust |
| Official | blog.rust-lang.org, Inside Rust |
| Foundation | rustfoundation.org (news, blog, events) |

## Parameters

- `time_range`: day | week | month (default: week)
- `category`: all | ecosystem | official | foundation

## Execution

Read agent file then launch Task:

```
1. Read: ../../agents/rust-daily-reporter.md
2. Task(subagent_type: "general-purpose", run_in_background: false, prompt: <agent content>)
```

## Output Format

```markdown
# Rust {Weekly|Daily|Monthly} Report

**Time Range:** {start} - {end}

## Ecosystem
| Score | Title | Link |

## Official
| Date | Title | Summary |

## Foundation
| Date | Title | Summary |
```

## Validation

- Each source should have at least 1 result; otherwise, mark "No updates."
- On fetch failure, retry with an alternative tool.