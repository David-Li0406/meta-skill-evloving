# Codex-CLI Prompt Templates

Prompt templates for code review with codex-cli.

## Swift Review Prompt

```
You are a senior Swift developer reviewing iOS code.

Review for:
1. Memory leaks (retain cycles in closures - missing [weak self])
2. Concurrency issues (missing @MainActor for @Observable classes)
3. Force unwrap without safety (!, try!)
4. Performance (unnecessary @State changes, DateFormatter creation)
5. SwiftUI best practices (@Observable vs @StateObject)
6. SwiftData patterns (proper @Model usage)
7. async/await error handling

Output ONLY a JSON array. No explanation text.
Each issue object: {
  "file": "filename.swift",
  "line": 42,
  "severity": "Critical|High|Medium|Low",
  "category": "Memory|Concurrency|Safety|Performance|Style",
  "description": "What is wrong",
  "current_code": "problematic code snippet",
  "suggested_fix": "corrected code snippet"
}

If no issues found, output: []

Code to review:
```

## TypeScript Review Prompt

```
You are a senior TypeScript developer reviewing Next.js/React code.

Review for:
1. Type safety (any types, missing types)
2. React hooks (missing useEffect dependencies, rules of hooks)
3. Performance (unnecessary re-renders, missing memoization)
4. Next.js patterns (use client/server correctly, SSR issues)
5. Null safety (optional chaining, null checks)
6. Error handling (try/catch, error boundaries)
7. Accessibility (missing ARIA, keyboard navigation)

Output ONLY a JSON array. No explanation text.
Each issue object: {
  "file": "filename.tsx",
  "line": 42,
  "severity": "Critical|High|Medium|Low",
  "category": "TypeSafety|React|Performance|NextJS|Accessibility",
  "description": "What is wrong",
  "current_code": "problematic code snippet",
  "suggested_fix": "corrected code snippet"
}

If no issues found, output: []

Code to review:
```

## Usage Examples

### Single File Review

```bash
# Swift
codex -q "$(cat .claude/skills/code-review/references/codex-prompts.md | sed -n '/Swift Review Prompt/,/```$/p' | sed '1d;$d')

$(cat path/to/File.swift)"

# TypeScript
codex -q "$(cat .claude/skills/code-review/references/codex-prompts.md | sed -n '/TypeScript Review Prompt/,/```$/p' | sed '1d;$d')

$(cat path/to/file.tsx)"
```

### Quick One-liner

```bash
# Swift quick review
codex -q "Review Swift code for issues. Output JSON array [{file,line,severity,category,description,current_code,suggested_fix}]: $(cat File.swift)"

# TypeScript quick review
codex -q "Review TypeScript code for issues. Output JSON array [{file,line,severity,category,description,current_code,suggested_fix}]: $(cat file.tsx)"
```

### Batch Review (Changed Files)

```bash
# Review all changed Swift files
for f in $(git diff master --name-only | grep '\.swift$'); do
  echo "=== Reviewing: $f ==="
  codex -q "Review Swift code. Output JSON issues [{file,line,severity,category,description,current_code,suggested_fix}]. File: $f

$(cat "$f")"
done
```

## Parsing Output

The JSON output can be parsed by Claude Code to:

1. Display issues in a readable format
2. Apply fixes using the Edit tool
3. Track which issues have been fixed

### Example Output

```json
[
  {
    "file": "ViewModel.swift",
    "line": 15,
    "severity": "High",
    "category": "Concurrency",
    "description": "@Observable class should have @MainActor for UI safety",
    "current_code": "@Observable\nclass ViewModel {",
    "suggested_fix": "@Observable\n@MainActor\nclass ViewModel {"
  },
  {
    "file": "ViewModel.swift",
    "line": 42,
    "severity": "Medium",
    "category": "Memory",
    "description": "Potential retain cycle - closure captures self strongly",
    "current_code": "onComplete = { self.handleComplete() }",
    "suggested_fix": "onComplete = { [weak self] in self?.handleComplete() }"
  }
]
```
