# ai-comm Usage Examples

## Code Review

```bash
ai-comm list-ai-windows
# Output: ID 12 is codex

ai-comm send "Review src/parser.py for edge cases and performance issues. \
Write findings to review_$(date +%Y%m%d_%H%M%S).md" --window 12
```

## Architecture Analysis

```bash
ai-comm send "Analyze error handling patterns in src/commands/ and \
src/parsers/. Write summary to analysis_$(date +%Y%m%d_%H%M%S).md" --window 8
```

## Long Output (redirect)

```bash
ai-comm send "Explain the entire codebase structure" --window 5 \
  > explanation_$(date +%Y%m%d_%H%M%S).md
```

## Parallel Requests

Send to multiple AIs by invoking multiple Bash tool calls in a single response:

```python
# Two parallel Bash tool calls
Bash: ai-comm send "Review security..." -w 8
Bash: ai-comm send "Review performance..." -w 12
# Both execute concurrently, each waits for its response
```
