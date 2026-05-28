---
name: package-validator
description: SEMO 패키지 구조 및 Sub-Agent 최적화 규칙 검증. Use when (1) Agent/Skill 추가/수정/삭제 후 검증, (2) CLAUDE.md 업데이트 후 일관성 확인, (3) 버저닝 전 품질 게이트, (4) Sub-Agent 최적화 규칙 준수 감사.
tools: [Bash, Read, Grep]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: package-validator 호출 - {검증 대상 패키지}` 시스템 메시지를 첫 줄에 출력하세요.

# package-validator Skill

> SEMO 패키지 구조 및 Sub-Agent 최적화 규칙 자동 검증

## Purpose

SEMO 패키지의 구조적 완전성과 **Claude Code Sub-Agent 최적화 규칙** 준수를 자동으로 검증합니다.

## Quick Start

```bash
# 패키지 전체 검증
ls -la sax/packages/{package}/agents/
ls -la sax/packages/{package}/skills/

# Frontmatter 검증 (필수 4개 필드: name, description, tools, model)
head -n 20 sax/packages/{package}/agents/*.md | grep -E "^(name|description|tools|model):"

# PROACTIVELY 패턴 검증
grep -l "PROACTIVELY use when" sax/packages/{package}/agents/*.md

# 도구 표준화 검증 (금지 도구 사용 확인)
grep -l "grep_search\|write_to_file\|slash_command\|web_fetch" sax/packages/{package}/agents/*.md

# CLAUDE.md 일관성 검증
grep -E "^\| .+ \|" sax/packages/{package}/CLAUDE.md
```

## Validation Checklist

| 검증 항목 | 명령어 | 기대 결과 |
|----------|--------|----------|
| Frontmatter (4필드) | `head -n 20 {file}` | name, description, tools, **model** 존재 |
| PROACTIVELY 패턴 | `grep "PROACTIVELY"` | 모든 Agent에 포함 |
| 도구 표준화 | `grep "grep_search"` | **결과 없음** (금지 도구) |
| Model 필드 | `grep "model:"` | opus/sonnet/haiku/inherit |
| 네이밍 | `ls {dir}` | kebab-case 준수 |
| CLAUDE.md | `grep {agent}` | 테이블에 모든 Agent 나열 |
| Progressive Disclosure | `ls skills/*/` | SKILL.md + references/ |

## SEMO Message

```markdown
[SEMO] Skill: package-validator 사용

[SEMO] Validation: {package} 패키지 검증 완료
```

## Related

- [semo-architect Agent](../../agents/semo-architect.md)
- [SEMO Core - Packaging](https://github.com/semicolon-devteam/docs/blob/main/sax/core/PACKAGING.md)

## References

For detailed documentation, see:

- [Validation Rules](references/validation-rules.md) - Frontmatter, 네이밍, CLAUDE.md, Orchestrator 검증 규칙
- [Validation Process](references/validation-process.md) - 5단계 검증 프로세스 상세
- [Output Format](references/output-format.md) - 성공/실패 출력 형식, 에러 핸들링
