---
name: conventional-commit
description: 'Generate Conventional Commit messages by analyzing git diffs. Use when committing code changes, when the user needs to write commit messages, or after staging changes.'
compatibility: 'Requires git CLI or git MCP, and a working git repository with changes (staged or unstaged).'
allowed-tools:
    - Bash(git:*)
    - Read
    - mcp__git
---

# Conventional Commit Messages (Korean Output)

## When to use this skill

Use this skill when:

- The user needs to write a commit message
- The user has staged or unstaged git changes
- The user asks for commit message suggestions

## OUTPUT LANGUAGE (MANDATORY)

- Final commit message MUST be Korean for all natural-language parts.
- English ONLY for protected identifiers, code keywords, paths, backtick content, code blocks.
- Output ONLY the final commit message (no explanations or meta commentary).

## FORMAT

- Structure: `<type>[optional scope]: <description>` → `[optional body]` → `[optional footer]`.
- Allowed `type`: `feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert`.
- Header: `type(scope): description` or `type: description`; scope only if it adds clarity.
- Description: Korean, imperative, concise, no trailing period.
- Breaking changes: mark with `!` in header and/or `BREAKING CHANGE:` in footer.

## Workflow

1. If diffs are already in context, skip git commands
2. Otherwise: `git status` → `git diff` / `git diff --cached`
   → generate message

## Examples

```text
feat(parser): 배열 파싱 기능 추가
fix(ui): 버튼 정렬 문제 수정
refactor: 데이터 처리 성능 개선
```

### Multi-line example

```text
feat(auth): OAuth 로그인 기능 구현

- Google OAuth 2.0 Provider 추가
- Login Callback Handler 구현
- Session 관리 Middleware 적용

Closes #123
```

## Validation checklist

- [ ] Type is one of allowed values
- [ ] Header matches format
- [ ] Description: imperative, concise, no trailing period
- [ ] Breaking changes clearly marked
- [ ] Korean output rules respected

---

## Preservation rules

Do not translate:

- Code blocks, backtick content
- CamelCase / snake_case / kebab-case identifiers
- Paths with `.` `/` `[]`
- ALL_CAPS acronyms (API, SDK, etc.)
- Framework/library proper nouns

## Notes

- MCP tools are optional; omit if unavailable or add others as needed
