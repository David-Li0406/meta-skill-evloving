---
name: pkm
description: |
  TechPKM GitHub Repository Search - Searches through 1000+ curated AI/ML project summaries.

  Activation triggers:
  - Explicit: /pkm <query>
  - Questions about GitHub repos, libraries, or open-source tools
  - "Find/search repositories for...", "... 관련 프로젝트", "라이브러리 추천"
  - Technical keyword + search intent (e.g., "langchain alternatives", "RAG 구현 도구")

  Capabilities:
  - Fuzzy search with typo tolerance
  - Korean/English bilingual search
  - Filter by language (Python, TypeScript, etc.) and tags
  - Returns relevance-scored results with summaries
invocation: user
---

# PKM Search Skill

You are now enhanced with the PKM (Personal Knowledge Management) search capability for TechPKM.

## What This Skill Does

This skill searches through **1000+ curated GitHub repository summaries** in TechPKM. Each repo has been analyzed and summarized in Korean with metadata including:
- Programming language
- Tags (in Korean)
- Aliases
- Concise summary

## When to Use

Automatically activate when users:
1. Ask about GitHub repositories or open-source tools
2. Request library/framework recommendations
3. Search for specific technical implementations
4. Use phrases like "깃헙", "프로젝트", "라이브러리", "레포"
5. Ask about AI/ML tools, frameworks, or implementations

## How to Search

### Basic Search

```bash
cd /Users/imgeunseog/Documents/Github/TechPKM/.claude/skills/pkm
python scripts/search.py "<query>"
```

### With Filters

```bash
# Filter by language
python scripts/search.py "langchain" --language Python

# Filter by tags (comma-separated)
python scripts/search.py "RAG" --tags "오픈소스,LLM"

# Limit results
python scripts/search.py "embedding" --limit 5

# JSON output for programmatic use
python scripts/search.py "agent" --json
```

### Combined Example

```bash
python scripts/search.py "자연어처리" --language Python --tags "LLM" --limit 10
```

## Search Features

### 1. Fuzzy Matching
Tolerates typos: "langchan" → finds "langchain"

### 2. Korean/English Translation
Automatically expands queries:
- "NLP" → also searches "자연어처리"
- "딥러닝" → also searches "deep learning"
- "RAG" → also searches "검색 증강 생성"

### 3. Scoring System
Results ranked by relevance (0-100):
- Exact repo name match: +100
- Alias match: +80
- Exact tag match: +60
- Partial tag match: +40
- Summary contains query: +30
- Fuzzy similarity: up to +25

## Index Management

### Rebuild Index (if needed)

```bash
python scripts/build_index.py
```

The index auto-detects changes:
- New files added to `/github/`
- Modified files
- Deleted files

Force rebuild:
```bash
python scripts/build_index.py --force
```

## Response Format

When presenting results, use this format:

```markdown
## PKM Search Results: "<query>"

X repositories found:

### 1. owner/repo-name
**Language**: Python | **Score**: 95/100
**Tags**: Tag1, Tag2, Tag3
**URL**: https://github.com/owner/repo

> Summary of the repository's purpose and capabilities...

### 2. ...
```

## Example Interactions

**User**: "langchain 대안 뭐 있어?"
**Action**: Search for "langchain" and related frameworks

**User**: "RAG 구현할 때 쓸만한 Python 라이브러리"
**Action**: `python scripts/search.py "RAG" --language Python --limit 10`

**User**: "음성 인식 오픈소스"
**Action**: `python scripts/search.py "음성 인식"` (will also find "speech recognition")

**User**: "Find TypeScript AI agent frameworks"
**Action**: `python scripts/search.py "AI agent" --language TypeScript`

## Important Notes

1. **Always run search first** before claiming no results exist
2. **Try multiple queries** if initial search yields few results
3. **Use Korean terms** for better matches (most tags are in Korean)
4. **Check the URL** before sharing - all repos link to github.com
5. **Summarize relevantly** - don't just list all results, highlight the most relevant ones

## Troubleshooting

If search returns no results:
1. Try simpler/shorter query
2. Try the Korean equivalent term
3. Remove filters and search broadly first
4. Check if index exists: `ls data/index.json`
5. Rebuild index if needed: `python scripts/build_index.py --force`
