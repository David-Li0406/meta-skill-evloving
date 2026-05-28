# Audit Checklist

> audit-semo Skill의 상세 검증 기준

## Agent 검증 상세

### 🔴 Critical (즉시 수정)

#### Frontmatter 4필드 검증

```yaml
---
name: agent-name        # ✅ kebab-case
description: |          # ✅ 멀티라인 지원
  역할 설명. PROACTIVELY use when:
  (1) 조건1, (2) 조건2, (3) 조건3.
tools:                  # ✅ 배열 형식
  - read_file
  - write_file
model: sonnet           # ✅ 필수 (opus|sonnet|haiku|inherit)
---
```

**검증 명령**:

```bash
# model 필드 누락 확인
grep -rL "^model:" semo-*/agents/*/*.md

# 4필드 모두 존재 확인
for f in semo-*/agents/*/*.md; do
  count=$(head -n 20 "$f" | grep -cE "^(name|description|tools|model):")
  if [ "$count" -lt 4 ]; then
    echo "❌ $f: $count/4 필드"
  fi
done
```

#### PROACTIVELY 패턴 검증

```bash
# PROACTIVELY 패턴 누락 확인
grep -rL "PROACTIVELY use when" semo-*/agents/*/*.md

# 올바른 예시
description: |
  Code reviewer. PROACTIVELY use when:
  (1) PR 리뷰, (2) 코드 품질 검토, (3) 보안 취약점 확인.
```

#### model 필드 유효값 검증

| 값 | 용도 |
|---|------|
| `opus` | 아키텍처 결정, 복잡한 분석 |
| `sonnet` | 품질 중심 작업, 구현 (기본값) |
| `haiku` | 빠른 응답, 단순 조회 |
| `inherit` | Orchestrator 전용 (부모 모델 상속) |

```bash
# 잘못된 model 값 확인
grep "^model:" semo-*/agents/*/*.md | grep -vE "(opus|sonnet|haiku|inherit)"
```

### 🟡 Important (권장 수정)

#### 라인 수 검증 (200 lines 이하)

```bash
# 200 lines 초과 Agent
wc -l semo-*/agents/*/*.md | awk '$1 > 200 {print "⚠️", $2, ":", $1, "lines"}'
```

#### 금지 도구 사용 확인

```bash
# 비표준 도구명 사용 확인
grep -rE "(grep_search|write_to_file|slash_command|web_fetch)" semo-*/agents/*/*.md
```

**도구명 표준화**:

| ❌ 금지 | ✅ 표준 |
|--------|---------|
| `grep_search` | `grep` |
| `write_to_file` | `write_file` |
| `slash_command` | `skill` |
| `web_fetch` | (제거) |

---

## Skill 검증 상세

### 🔴 Critical

#### Frontmatter 3필드 검증

```yaml
---
name: skill-name        # ✅ kebab-case
description: |          # ✅ "Use when" 포함 권장
  역할 설명. Use when (1) 조건1, (2) 조건2.
tools: [Bash, Read]     # ✅ 배열 형식
---
```

#### 시스템 메시지 존재 검증

```bash
# 시스템 메시지 누락 확인 (Frontmatter 직후)
for f in semo-*/skills/*/SKILL.md; do
  if ! grep -q "시스템 메시지" "$f"; then
    echo "❌ $f: 시스템 메시지 누락"
  fi
done
```

**올바른 형식**:

```markdown
---
name: example-skill
...
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: example-skill 호출 - {context}` 시스템 메시지를 첫 줄에 출력하세요.
```

### 🟡 Important

#### 라인 수 검증 (100 lines 이하)

```bash
# 100 lines 초과 Skill
wc -l semo-*/skills/*/SKILL.md | awk '$1 > 100 {print "⚠️", $2, ":", $1, "lines"}'
```

#### "Use when" 패턴 검증

```bash
# description에 "Use when" 누락 확인
for f in semo-*/skills/*/SKILL.md; do
  if ! head -n 10 "$f" | grep -q "Use when"; then
    echo "⚠️ $f: 'Use when' 패턴 누락"
  fi
done
```

### 🟢 Nice-to-have

#### Progressive Disclosure 검증

```bash
# 100+ lines인데 references/ 없는 경우
for dir in semo-*/skills/*/; do
  skill_file="$dir/SKILL.md"
  if [ -f "$skill_file" ]; then
    lines=$(wc -l < "$skill_file")
    if [ "$lines" -gt 100 ] && [ ! -d "${dir}references" ]; then
      echo "💡 $dir: $lines lines, references/ 분리 권장"
    fi
  fi
done
```

---

## Command 검증 상세

### 🔴 Critical

#### 파일 존재 확인

```bash
# commands 디렉토리 스캔
ls -la semo-*/commands/*.md 2>/dev/null
```

#### Frontmatter 필수 필드

```yaml
---
name: command-name
description: 커맨드 설명
---
```

### 🟡 Important

#### CLAUDE.md 연동 확인

```bash
# CLAUDE.md에 커맨드 등록 여부 확인
for cmd in semo-*/commands/*.md; do
  cmd_name=$(basename "$cmd" .md)
  pkg_dir=$(dirname $(dirname "$cmd"))
  if ! grep -q "$cmd_name" "$pkg_dir/CLAUDE.md" 2>/dev/null; then
    echo "⚠️ $cmd: CLAUDE.md에 미등록"
  fi
done
```

---

## 심각도별 우선순위

| 심각도 | 조치 기한 | 대응 방법 |
|--------|----------|----------|
| 🔴 Critical | **즉시** | agent-manager/skill-manager 호출하여 수정 |
| 🟡 Important | 1주 내 | 다음 버저닝 전 수정 |
| 🟢 Nice-to-have | 선택적 | 리팩토링 시 함께 처리 |
