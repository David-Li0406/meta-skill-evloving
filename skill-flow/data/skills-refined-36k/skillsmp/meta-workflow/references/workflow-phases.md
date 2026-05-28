# Meta Workflow Phases

> meta-workflow 스킬의 각 단계별 상세 가이드

## Overview

```
Phase 1: 환경 검증 → Phase 2: 작업 수행 → Phase 3: 버저닝 & 배포 → Phase 4: 로컬 동기화
```

---

## Phase 1: 환경 검증

### 1.1 Meta 패키지 확인

```bash
# 필수 조건: semo-system/meta/ 디렉토리 존재
if [ ! -d "semo-system/meta" ]; then
  echo "❌ Meta 패키지가 설치되어 있지 않습니다"
  echo "💡 설치: semo add meta"
  exit 1
fi
```

### 1.2 GitHub 인증 확인

```bash
# gh CLI 인증 상태 확인
gh auth status

# 실패 시:
# gh auth login
```

### 1.3 브랜치 확인

```bash
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "⚠️ 현재 브랜치: $CURRENT_BRANCH"
  echo "💡 main 브랜치에서 작업하는 것을 권장합니다"
fi
```

### 1.4 작업 디렉토리 확인

```bash
# semo 루트 디렉토리인지 확인
if [ ! -f "semo-system/semo-core/VERSION" ]; then
  echo "❌ SEMO 루트 디렉토리가 아닙니다"
  exit 1
fi
```

---

## Phase 2: 작업 수행

### 2.1 동작 범위

| 패키지 | VERSION 파일 | 설명 |
|--------|-------------|------|
| `semo-core` | `semo-system/semo-core/VERSION` | 에이전트, 커맨드, 원칙 |
| `semo-skills` | `semo-system/semo-skills/VERSION` | 통합 스킬 |
| `meta` | `semo-system/meta/VERSION` | 메타 스킬/에이전트 |
| `semo-remote` | `semo-system/semo-remote/VERSION` | 원격 통합 |
| `semo-hooks` | `semo-system/semo-hooks/VERSION` | 훅 시스템 |

### 2.2 작업 유형별 활용 스킬

| 작업 유형 | 활용 스킬 | 예시 |
|----------|----------|------|
| 스킬 생성 | `skill-creator` | "새 스킬 만들어줘" |
| 에이전트 관리 | `agent-manager` | "에이전트 추가해줘" |
| 커맨드 관리 | `command-manager` | "커맨드 수정해줘" |
| 코드 작성 | `write-code` | "구현해줘" |
| 테스트 작성 | `write-test` | "테스트 추가해줘" |

### 2.3 작업 완료 감지

```bash
# 변경된 파일 확인
git status --short | grep "semo-system/"

# 변경된 패키지 추출
git diff --name-only | grep "semo-system/" | cut -d'/' -f2 | sort -u
```

---

## Phase 3: 버저닝 & 배포

### 3.1 버전 범프 규칙

| 변경 유형 | 버전 범프 | 예시 |
|----------|----------|------|
| Breaking Change | MAJOR | 1.0.0 → 2.0.0 |
| 새 기능 추가 | MINOR | 1.0.0 → 1.1.0 |
| 버그 수정/문서 | PATCH | 1.0.0 → 1.0.1 |

### 3.2 CHANGELOG 형식

```markdown
# {version} ({date})

## Added
- 새로 추가된 기능

## Changed
- 변경된 기능

## Fixed
- 수정된 버그

## Notes
- 추가 메모
```

### 3.3 커밋 메시지 형식

```bash
git commit -m "$(cat <<'EOF'
feat({package}): {변경 요약} ({version})

## {Added/Changed/Fixed}
- 상세 내용

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### 3.4 배포 순서

```bash
# 1. 스테이징
git add semo-system/{package}/

# 2. 커밋
git commit -m "..."

# 3. 푸시
git push origin main

# 4. Slack 알림 (skill:notify-slack)
```

### 3.5 Slack 알림 형식

```json
{
  "channel": "#_협업",
  "blocks": [
    {
      "type": "header",
      "text": { "type": "plain_text", "text": "🚀 SEMO 배포 완료" }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*패키지*\n{package}" },
        { "type": "mrkdwn", "text": "*버전*\n{old} → {new}" }
      ]
    },
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*변경 내용*\n{summary}" }
    }
  ]
}
```

---

## Phase 4: 로컬 동기화

### 4.1 심볼릭 링크 재생성

```bash
# 스킬 심볼릭 링크
.claude/skills/{skill_name} → semo-system/semo-skills/{skill_name}
.claude/skills/{skill_name} → semo-system/meta/skills/{skill_name}

# 에이전트 심볼릭 링크
.claude/agents/{agent_name} → semo-system/semo-core/agents/{agent_name}
.claude/agents/{agent_name} → semo-system/meta/agents/{agent_name}
```

### 4.2 동기화 스크립트

```bash
#!/bin/bash
# 로컬 동기화 스크립트

echo "🔄 로컬 동기화 시작..."

# 1. 기존 스킬 심볼릭 링크 정리
find .claude/skills -type l -delete 2>/dev/null

# 2. semo-skills 재링크
for skill in semo-system/semo-skills/*/; do
  if [ -d "$skill" ]; then
    skill_name=$(basename "$skill")
    ln -sf "../../semo-system/semo-skills/$skill_name" ".claude/skills/$skill_name"
    echo "  ✅ $skill_name (semo-skills)"
  fi
done

# 3. meta 스킬 재링크
if [ -d "semo-system/meta/skills" ]; then
  for skill in semo-system/meta/skills/*/; do
    if [ -d "$skill" ]; then
      skill_name=$(basename "$skill")
      ln -sf "../../semo-system/meta/skills/$skill_name" ".claude/skills/$skill_name"
      echo "  ✅ $skill_name (meta)"
    fi
  done
fi

# 4. 에이전트 심볼릭 링크 정리 및 재생성
find .claude/agents -type l -delete 2>/dev/null

for agent in semo-system/semo-core/agents/*/; do
  if [ -d "$agent" ]; then
    agent_name=$(basename "$agent")
    ln -sf "../../semo-system/semo-core/agents/$agent_name" ".claude/agents/$agent_name"
    echo "  ✅ $agent_name (semo-core)"
  fi
done

if [ -d "semo-system/meta/agents" ]; then
  for agent in semo-system/meta/agents/*/; do
    if [ -d "$agent" ]; then
      agent_name=$(basename "$agent")
      ln -sf "../../semo-system/meta/agents/$agent_name" ".claude/agents/$agent_name"
      echo "  ✅ $agent_name (meta)"
    fi
  done
fi

echo "✅ 로컬 동기화 완료"
```

### 4.3 CLAUDE.md 업데이트

새 스킬/에이전트가 추가된 경우 `.claude/CLAUDE.md`의 스킬 목록 업데이트가 필요할 수 있습니다.

```bash
# semo-cli를 통한 재생성
npx @anthropic/claude-code semo regenerate-claude-md

# 또는 수동 업데이트
# .claude/CLAUDE.md 파일의 스킬 목록 섹션 수정
```

---

## 전체 흐름 요약

```
[사용자 요청] (또는 자동 감지)
    │
    ├─ Phase 1: 환경 검증
    │   ├─ Meta 패키지 확인 ✓
    │   ├─ GitHub 인증 확인 ✓
    │   └─ 브랜치 확인 ✓
    │
    ├─ Phase 2: 작업 수행
    │   └─ semo-system/ 파일 수정
    │
    ├─ Phase 3: 버저닝 & 배포
    │   ├─ 변경 패키지 감지
    │   ├─ VERSION 범프
    │   ├─ CHANGELOG 생성
    │   ├─ git commit & push
    │   └─ Slack 알림
    │
    └─ Phase 4: 로컬 동기화
        ├─ 심볼릭 링크 재생성
        └─ CLAUDE.md 업데이트 (필요 시)
```

---

## Error Handling

### 환경 검증 실패

```markdown
❌ Meta 환경 검증 실패

- Meta 패키지가 설치되어 있지 않습니다
- 설치: `semo add meta`
```

### GitHub 인증 실패

```markdown
❌ GitHub 인증 실패

- `gh auth login` 명령어로 인증해주세요
```

### 버저닝 실패

```markdown
❌ 버저닝 실패

- VERSION 파일을 찾을 수 없습니다
- 수동으로 버전을 지정해주세요
```

### 로컬 동기화 실패

```markdown
⚠️ 로컬 동기화 경고

- 일부 심볼릭 링크 생성 실패
- 수동으로 확인해주세요: ls -la .claude/skills/
```
