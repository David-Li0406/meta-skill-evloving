# Sync Commands Reference

## .claude/ 동기화

```bash
# SEMO commands 동기화
rsync -av --delete \
  sax/packages/semo-po/commands/SEMO/ \
  .claude/commands/SEMO/

# CLAUDE.md 동기화
rsync -av \
  sax/packages/semo-po/CLAUDE.md \
  .claude/CLAUDE.md
```

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

## Related Resources

- [Commands 섹션](../../CLAUDE.md#commands)
- [기존 SEMO Commands](../../commands/SEMO/)
- [Claude Code Slash Commands](https://code.claude.com/docs/en/slash-commands)
