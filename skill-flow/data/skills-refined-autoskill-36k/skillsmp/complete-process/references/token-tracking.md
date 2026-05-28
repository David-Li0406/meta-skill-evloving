# Token Tracking for Complete Process Orchestrator

## Overview

Track and display token consumption after each step to provide real-time cost visibility and budget planning information.

## Display Format

After each step completion, display token usage in this format:

```text
✓ Step N/M complete | Tokens: X,XXX
```

## Implementation Instructions

### After Each Step

1. Check current conversation token usage
2. Display completion message with token count
3. Format numbers with comma separators (e.g., 1,234 not 1234)

### Step-by-Step Format

**Step 1/3: Transform**

```text
Step 1/3: 🔄 Transforming query to pseudo-code...
[transformation process and output]
✓ Step 1/3 complete | Tokens: 1,234
```

**Step 2/3: Validate**

```text
Step 2/3: ✓ Validating requirements...
[validation process and output]
✓ Step 2/3 complete | Tokens: 2,567
```

**Step 3/3: Optimize**

```text
Step 3/3: ⚡ Optimizing for implementation...
[optimization process and output]
✓ Step 3/3 complete | Tokens: 3,891
```

### Final Summary

Update the pipeline completion summary to include total tokens:

```text
═══════════════════════════════════════════════════════════
✓ Pipeline complete! Review output below.
Total duration: 38 seconds | Total tokens: 3,891
═══════════════════════════════════════════════════════════
```

## Benefits

- **Real-time cost tracking**: Users see token consumption as it happens
- **Budget planning**: Helps predict costs for similar workflows
- **Performance insights**: Shows which steps consume more tokens
- **Transparency**: Clear visibility into resource usage
