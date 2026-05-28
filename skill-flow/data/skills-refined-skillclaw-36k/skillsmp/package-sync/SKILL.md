---
name: package-sync
description: SEMO 패키지 소스와 .claude/ 동기화 자동화. Use when (1) Agent/Skill/Command 변경 후 동기화, (2) 서브모듈 업데이트 후 심볼릭 링크 동기화, (3) 버저닝 완료 후 배포 준비.
tools: [Bash, Read, Grep]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: package-sync 호출 - {대상 패키지}` 시스템 메시지를 첫 줄에 출력하세요.

# package-sync Skill

> SEMO 패키지 소스 → .claude/ 디렉토리 동기화 자동화
>
> **SoT 참조**: 패키징 규칙은 `semo-core/PACKAGING.md`에서 관리됩니다.

## Purpose

1. **docs 레포**: `sax/packages/{package}/` 소스를 `.claude/{package}/`로 동기화
2. **로컬 환경**: 서브모듈 업데이트 후 `.claude/` 심볼릭 링크 동기화
3. **무결성 검증**: 동기화 상태만 검증 (수정 없이)

## 호출 모드

| 모드 | 동작 | 사용 상황 |
|------|------|----------|
| (기본) | 동기화 실행 | 수동 동기화 요청 시 |
| `--check-only` | 검증만 수행, 불일치 리포트 | version-updater에서 호출 시 |

### --check-only 모드

동기화 실행 없이 현재 상태만 검증합니다:

```bash
# 심볼릭 링크 상태 검증
for type in skills agents; do
  for link in .claude/$type/*/; do
    [ -L "${link%/}" ] || continue
    target=$(readlink "${link%/}")
    [ -e "${link%/}" ] && echo "✅ $type/$(basename $link)" || echo "❌ $type/$(basename $link) → 깨진 링크"
  done
done
```

**출력 포맷** (version-updater 파싱용):

```markdown
[SEMO] Skill: package-sync --check-only 실행

## 동기화 상태 검증

| 유형 | 정상 | 깨진 링크 | 누락 |
|------|------|----------|------|
| Skills | 8 | 0 | 0 |
| Agents | 5 | 1 | 2 |
| Commands | 4 | 0 | 0 |

**결과**: ⚠️ 불일치 발견 (자동 수정 필요)
```

**결과 상태**:

- `✅ 동기화 정상` - 모든 링크 정상
- `⚠️ 불일치 발견` - 수정 필요 (version-updater가 동기화 실행 결정)

## Quick Start

### docs 레포 동기화

```bash
# SEMO-PO 동기화
rsync -av --delete --exclude='.git' \
  sax/packages/semo-po/ \
  .claude/semo-po/

# SEMO-Meta 동기화
rsync -av --delete --exclude='.git' \
  sax/packages/semo-meta/ \
  .claude/semo-meta/
```

### 로컬 심볼릭 링크 동기화

```bash
# 서브모듈 업데이트 후 실행
package-sync --symlinks
```

## 심볼릭 링크 동기화 (--symlinks)

서브모듈 업데이트 후 `.claude/` 심볼릭 링크를 동기화합니다.

### 동기화 대상

| 유형 | 소스 | 대상 |
|------|------|------|
| Skills | `.claude/semo-meta/skills/*` | `.claude/skills/{name}` |
| Skills | `.claude/semo-core/skills/*` | `.claude/skills/{name}` |
| Agents | `.claude/semo-meta/agents/*` | `.claude/agents/{name}` |
| Agents | `.claude/semo-core/agents/*` | `.claude/agents/{name}` |
| Commands | `.claude/semo-meta/commands/*` | `.claude/commands/{name}` |

### 동기화 워크플로우

```text
1. 서브모듈 업데이트
   git submodule update --remote --merge

2. 기존 끊어진 링크 정리
   find .claude/skills -type l ! -exec test -e {} \; -delete
   find .claude/agents -type l ! -exec test -e {} \; -delete
   find .claude/commands -type l ! -exec test -e {} \; -delete

3. semo-core 컴포넌트 링크 (우선순위 낮음)
   for skill in .claude/semo-core/skills/*/; do
     name=$(basename "$skill")
     ln -sf "../semo-core/skills/$name" ".claude/skills/$name"
   done

4. semo-meta 컴포넌트 링크 (우선순위 높음, 덮어쓰기)
   for skill in .claude/semo-meta/skills/*/; do
     name=$(basename "$skill")
     ln -sf "../semo-meta/skills/$name" ".claude/skills/$name"
   done

5. 결과 검증
   ls -la .claude/skills/
```

### 우선순위 규칙

**semo-meta > semo-core**: 동일 이름 컴포넌트가 있으면 semo-meta가 우선

| 컴포넌트 | semo-core | semo-meta | 결과 |
|----------|----------|----------|------|
| `version-updater` | ✅ | ❌ | semo-core |
| `notify-slack` | ✅ | ❌ | semo-core |
| `version-manager` | ❌ | ✅ | semo-meta |
| `package-sync` | ❌ | ✅ | semo-meta |

### 동기화 스크립트

```bash
#!/bin/bash
# sync-symlinks.sh

CLAUDE_DIR=".claude"

# 끊어진 심볼릭 링크 제거
echo "🧹 Cleaning broken symlinks..."
find "$CLAUDE_DIR/skills" -type l ! -exec test -e {} \; -delete 2>/dev/null
find "$CLAUDE_DIR/agents" -type l ! -exec test -e {} \; -delete 2>/dev/null
find "$CLAUDE_DIR/commands" -type l ! -exec test -e {} \; -delete 2>/dev/null

# semo-core 링크 (우선순위 낮음)
echo "🔗 Linking semo-core components..."
if [ -d "$CLAUDE_DIR/semo-core/skills" ]; then
  for skill in "$CLAUDE_DIR/semo-core/skills"/*/; do
    [ -d "$skill" ] || continue
    name=$(basename "$skill")
    ln -sf "../semo-core/skills/$name" "$CLAUDE_DIR/skills/$name"
  done
fi

if [ -d "$CLAUDE_DIR/semo-core/agents" ]; then
  for agent in "$CLAUDE_DIR/semo-core/agents"/*/; do
    [ -d "$agent" ] || continue
    name=$(basename "$agent")
    ln -sf "../semo-core/agents/$name" "$CLAUDE_DIR/agents/$name"
  done
fi

# semo-meta 링크 (우선순위 높음, 덮어쓰기)
echo "🔗 Linking semo-meta components..."
if [ -d "$CLAUDE_DIR/semo-meta/skills" ]; then
  for skill in "$CLAUDE_DIR/semo-meta/skills"/*/; do
    [ -d "$skill" ] || continue
    name=$(basename "$skill")
    ln -sf "../semo-meta/skills/$name" "$CLAUDE_DIR/skills/$name"
  done
fi

if [ -d "$CLAUDE_DIR/semo-meta/agents" ]; then
  for agent in "$CLAUDE_DIR/semo-meta/agents"/*/; do
    [ -d "$agent" ] || continue
    name=$(basename "$agent")
    ln -sf "../semo-meta/agents/$name" "$CLAUDE_DIR/agents/$name"
  done
fi

if [ -d "$CLAUDE_DIR/semo-meta/commands" ]; then
  for cmd in "$CLAUDE_DIR/semo-meta/commands"/*/; do
    [ -d "$cmd" ] || continue
    name=$(basename "$cmd")
    ln -sf "../../semo-meta/commands/$name" "$CLAUDE_DIR/commands/$name"
  done
fi

echo "✅ Symlink sync complete!"
ls -la "$CLAUDE_DIR/skills/"
```

## Supported Packages

| 패키지 | 소스 경로 | 대상 경로 | 비고 |
|--------|----------|----------|------|
| semo-po | `sax/packages/semo-po/` | `.claude/semo-po/` | PO/기획자용 |
| semo-meta | `sax/packages/semo-meta/` | `.claude/semo-meta/` | SEMO 개발용 |
| semo-core | `.claude/semo-core/` | 심볼릭 링크 | 공통 컴포넌트 |

## SEMO Message

```markdown
[SEMO] Skill: package-sync 실행

[SEMO] Sync: {package} 동기화 완료 ({file_count}개 파일)

[SEMO] Sync: 심볼릭 링크 동기화 완료
- Skills: {skill_count}개
- Agents: {agent_count}개
- Commands: {command_count}개
```

## Related

- [package-deploy Skill](../package-deploy/SKILL.md) - 외부 프로젝트 배포
- [version-manager Skill](../version-manager/SKILL.md) - 버저닝 후 동기화
- [semo-architect Agent](../../agents/semo-architect.md)

## References

For detailed documentation, see:

- [Sync Workflow](references/sync-workflow.md) - 동기화 프로세스 상세
- [Package Mapping](references/package-mapping.md) - 패키지별 경로 매핑
- [Output Format](references/output-format.md) - 성공/실패 출력 형식
