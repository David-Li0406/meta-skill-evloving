---
name: toon-formatter
description: Use this skill to AGGRESSIVELY apply TOON v2.0 format for structured data, optimizing token usage when handling large, uniform datasets.
---

# TOON v2.0 Formatter Skill (AGGRESSIVE MODE)

## Purpose

**AGGRESSIVELY** apply TOON v2.0 format to save 30-60% tokens on structured data. Use TOON **by default** for biggish, regular data. 

## When to Use (AGGRESSIVE)

**TOON ALL DAY** - Use automatically for:
- ✅ Arrays with ≥ 5 similar items
- ✅ Tables, logs, events, transactions, analytics
- ✅ API responses with uniform structure (≥60% field overlap)
- ✅ Database query results
- ✅ Repeatedly-used, structured data in prompts
- ✅ RAG pipelines, tool calls, agents passing data around
- ✅ Benchmarks/evals where prompt size = money
- ✅ Shape is more important than labels
- ✅ You know what each column means
- ✅ Can declare headers once, go row-by-row

**MAYBE, BUT NOT AUTOMATICALLY** - Be selective when:
- ⚠️ Human collaborators reading/editing data a lot
- ⚠️ APIs/tools expect JSON (use JSON on wire, TOON in prompts)
- ⚠️ Structure is uneven (many optional keys, weird nesting)

**NO, JUST DON'T** - Stick to JSON/text for:
- ❌ Short arrays (< 5 items)
- ❌ One-off examples in docs
- ❌ Narrative text, instructions, essays
- ❌ Deep, irregular trees where hierarchy matters

## What is TOON v2.0?

**TOON (Token-Oriented Object Notation) v2.0** reduces token consumption by 30-60% for structured data:

### Three Array Types

**1. Tabular** (uniform objects ≥5 items):
```
[2]{id,name,balance}:
  1,Alice,5420.50
  2,Bob,3210.75
```

**2. Inline** (primitives ≤10):
```
tags[5]: javascript,react,node,express,api
```

**3. Expanded** (non-uniform):
```
- name: Alice
  role: admin
- name: Bob
  level: 5
```

### Three Delimiters

**Comma** (default, most compact):
```
[2]{name,city}: Alice,NYC Bob,LA
```

**Tab** (for data with commas):
```
[2\t]{name,address}: Alice	123 Main St, NYC
```

**Pipe** (markdown-like):
```
[2|]{method,path}: GET
```