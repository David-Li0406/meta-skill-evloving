---
name: create-command
description: Create SEMO slash commands following Claude Code conventions. Use when (1) need to add new /SEMO:command, (2) creating interactive workflows triggered by slash commands, (3) packaging command-based operations.
tools: [Bash, Write]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: create-command 호출 - {커맨드 이름}` 시스템 메시지를 첫 줄에 출력하세요.

# Create Command Skill

> SEMO 슬래시 커맨드 생성 (Claude Code 규칙 준수)

## 역할

Claude Code의 slash command 규칙에 따라 SEMO 커맨드를 생성합니다.

## Quick Start

```bash
# 1. SEMO 디렉토리에 파일 생성 (: 프리픽스 없이)
touch sax/packages/semo-po/commands/SEMO/new-command.md

# 2. 커맨드 내용 작성 (Markdown 형식)
# 3. CLAUDE.md Commands 섹션에 추가
# 4. .claude/ 동기화

# 호출 형식 (자동)
/SEMO:new-command  # ✅ SAX: 프리픽스 자동 적용
```

## 네이밍 규칙

- ✅ 파일명: `commands/SEMO/onboarding.md` → 호출: `/SEMO:onboarding`
- ❌ 파일명: `commands/SEMO/:onboarding.md` → 이중 콜론 발생

## SEMO Message

```markdown
[SEMO] Skill: create-command 사용
[SEMO] Reference: Claude Code slash command 규칙 준수
```

## Related

- [Commands 섹션](../../CLAUDE.md#commands)
- [기존 SEMO Commands](../../commands/SEMO/)

## References

For detailed documentation, see:

- [Naming Rules](references/naming-rules.md) - 네이밍 규칙, 커맨드 파일 구조, CLAUDE.md 업데이트
- [Sync Commands](references/sync-commands.md) - .claude/ 동기화 명령어
