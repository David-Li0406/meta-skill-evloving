---
name: rlm-processing
description: "Process large codebases using Recursive Language Model patterns. Use when context exceeds 50K tokens or requires deep multi-file analysis."
---

# RLM Processing Skill

Expert guidance for using Recursive Language Model (RLM) patterns to analyze large codebases efficiently.

## Core Concept

RLM treats large context as an **external environment** rather than loading it directly into the LLM's context window. The LLM:
1. Loads files as variables in a REPL
2. Writes code to chunk, filter, and process
3. Uses `llm_query()` for semantic sub-tasks
4. Returns condensed, relevant results

## When to Use

### Trigger Conditions

- **Token Threshold**: Context exceeds 50K tokens
- **File Count**: Story requires understanding >5 interconnected files
- **Pattern Discovery**: Need to find where something happens in unfamiliar code
- **Cross-Cutting Analysis**: Auth, logging, error handling across modules

### Activation Examples

```
Scenario: "Add rate limiting to all API endpoints"
- Need to find: All endpoint definitions
- Files involved: Likely 15+ route files
- Context size: ~100K tokens
- Decision: USE RLM
```

```
Scenario: "Fix typo in login button"
- Location: Known (src/components/Login.tsx)
- Files involved: 1
- Context size: ~2K tokens
- Decision: SKIP RLM
```

## REPL Environment

### Available Variables

```python
context       # Dict: {file_path: file_content}
total_chars   # Total characters loaded
total_tokens  # Estimated tokens (~chars/4)
```

### Available Functions

```python
llm_query(prompt)     # Query sub-LLM for semantic tasks
print(text)           # Output (truncated to 30K chars)
FINAL(answer)         # Return text answer
FINAL_VAR(var_name)   # Return variable content
```

## Chunking Strategies

### By File Type

**TypeScript/JavaScript:**
```python
# Split by exports/functions/classes
pattern = r'export\s+(?:const|function|class|interface|type)\s+\w+'
```

**Python:**
```python
# Split by def/class
pattern = r'^(?:def|class)\s+\w+'
```

**Markdown:**
```python
# Split by headers
pattern = r'^#{1,3}\s+.+'
```

### By Size

```python
def chunk_by_size(text, max_chars=5000):
    """Safe fallback for any file type"""
    chunks = []
    current = ""
    for line in text.split('\n'):
        if len(current) + len(line) > max_chars:
            chunks.append(current)
            current = line
        else:
            current += '\n' + line
    if current:
        chunks.append(current)
    return chunks
```

## When to Use llm_query() vs Code

### Use Code When:

| Task | Code Approach |
|------|---------------|
| Find function names | `re.findall(r'function (\w+)', code)` |
| Count occurrences | `content.count('TODO')` |
| Filter by path | `[p for p in context if '/api/' in p]` |
| Extract imports | `re.findall(r'import .+ from [\'"](.+)[\'"]', code)` |
| Find string patterns | `re.search(r'jwt|token|session', code)` |

### Use llm_query() When:

| Task | Why LLM Needed |
|------|----------------|
| "What does this function do?" | Semantic understanding |
| "Is this a security risk?" | Judgment required |
| "Summarize this module" | Abstraction needed |
| "How do these relate?" | Relationship inference |

## Common Patterns

### Find All Endpoints

```python
endpoints = []
for path, content in context.items():
    if not path.endswith(('.ts', '.js')):
        continue
    # Express/Koa style
    rest = re.findall(r'\.(get|post|put|delete|patch)\([\'"]([^\'"]+)', content)
    # Next.js style
    if '/pages/api/' in path or '/app/api/' in path:
        endpoints.append((path, 'route', path))
    endpoints.extend([(path, m, r) for m, r in rest])
```

### Map Authentication Flow

```python
auth_files = [p for p in context.keys()
              if any(x in p.lower() for x in ['auth', 'login', 'session'])]

auth_map = {}
for path in auth_files[:5]:
    role = llm_query(f"What role does this play in auth? (1 sentence)\n\n{context[path][:2500]}")
    auth_map[path] = role
```

### Find Error Handling

```python
error_patterns = []
for path, content in context.items():
    if re.search(r'(try\s*\{|\.catch\(|catch\s*\(|throw\s+new)', content):
        # Count error handling instances
        count = len(re.findall(r'catch', content))
        error_patterns.append((path, count))

# Sort by error handling density
error_patterns.sort(key=lambda x: -x[1])
```

### Identify Test Files

```python
test_files = [p for p in context.keys()
              if re.search(r'(\.test\.|\.spec\.|__tests__)', p)]

# Map tests to source files
test_mapping = {}
for test_path in test_files:
    # Extract what's being tested
    source = re.sub(r'\.(test|spec)', '', test_path)
    source = re.sub(r'__tests__/', '', source)
    test_mapping[test_path] = source
```

## Cost Optimization

### Budget llm_query() Calls

```python
MAX_SUB_CALLS = 20
sub_calls_made = 0

def budget_query(prompt):
    global sub_calls_made
    if sub_calls_made >= MAX_SUB_CALLS:
        return "[BUDGET EXCEEDED - skipping]"
    sub_calls_made += 1
    return llm_query(prompt)
```

### Batch Similar Queries

```python
# Instead of 10 separate calls:
# BAD: for f in files: llm_query(f"Analyze {f}")

# Batch into one:
batch = "\n---\n".join([f"File: {f}\n{context[f][:1000]}" for f in files[:5]])
analysis = llm_query(f"For each file below, state its purpose (1 line each):\n\n{batch}")
```

### Filter Before Querying

```python
# Don't query all files - filter first
relevant = [p for p in context.keys()
            if re.search(r'user|auth|login', context[p].lower())]

# Then query only relevant files
for path in relevant[:10]:
    # Now llm_query is worth the cost
    ...
```

## Output Format

Always return structured JSON:

```json
{
  "analysis": "Summary of findings",
  "relevant_files": ["src/auth/index.ts", "src/middleware/auth.ts"],
  "code_patterns": [
    "Pattern: JWT tokens stored in httpOnly cookies",
    "Pattern: Auth middleware applied via app.use() in src/app.ts"
  ],
  "implementation_hints": "To add a new auth check, follow the pattern in src/middleware/auth.ts line 45",
  "tokens_processed": 85000,
  "sub_calls_made": 8
}
```

## Verification Checklist

Before returning FINAL():

- [ ] All relevant files identified
- [ ] Patterns extracted and documented
- [ ] Implementation hints are actionable
- [ ] Token count tracked
- [ ] Sub-call count within budget (≤20)
- [ ] Answer directly addresses the original query
