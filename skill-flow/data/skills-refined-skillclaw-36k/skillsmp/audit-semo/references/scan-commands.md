# Scan Commands

> audit-semo Skill에서 사용하는 패키지별 스캔 명령어

## 전체 패키지 스캔

### 1. 패키지 목록 확인

```bash
# SEMO 패키지 디렉토리 목록
ls -d sax-*/

# 예상 패키지:
# semo-meta/   - SEMO 자체 관리
# semo-next/   - Next.js 프로젝트
# semo-backend/ - 백엔드 프로젝트
# semo-po/     - PO (Product Owner) 작업
# semo-qa/     - QA 작업
# semo-core/   - 공통 컴포넌트
# semo-pm/     - 스프린트 관리
```

### 2. 컴포넌트 수량 집계

```bash
# 패키지별 Agent/Skill/Command 수량
for pkg in sax-*/; do
  agents=$(ls -d ${pkg}agents/*/ 2>/dev/null | wc -l)
  skills=$(ls -d ${pkg}skills/*/ 2>/dev/null | wc -l)
  commands=$(ls ${pkg}commands/*.md 2>/dev/null | wc -l)
  echo "$pkg: Agent=$agents, Skill=$skills, Command=$commands"
done
```

---

## Agent 스캔

### Frontmatter 검증

```bash
# 모든 Agent의 Frontmatter 추출
for f in semo-*/agents/*/*.md; do
  echo "=== $f ==="
  head -n 15 "$f" | grep -E "^(name|description|tools|model):"
done
```

### model 필드 누락

```bash
# model 필드 없는 Agent
grep -rL "^model:" semo-*/agents/*/*.md 2>/dev/null
```

### PROACTIVELY 패턴 누락

```bash
# PROACTIVELY 패턴 없는 Agent
grep -rL "PROACTIVELY use when" semo-*/agents/*/*.md 2>/dev/null
```

### 라인 수 확인

```bash
# 200 lines 초과
wc -l semo-*/agents/*/*.md 2>/dev/null | awk '$1 > 200'

# 라인 수 기준 정렬
wc -l semo-*/agents/*/*.md 2>/dev/null | sort -rn | head -20
```

### 금지 도구 사용

```bash
# 비표준 도구명
grep -rn "grep_search\|write_to_file\|slash_command\|web_fetch" semo-*/agents/*/*.md
```

---

## Skill 스캔

### Frontmatter 검증

```bash
# 모든 Skill의 Frontmatter 추출
for f in semo-*/skills/*/SKILL.md; do
  echo "=== $f ==="
  head -n 10 "$f" | grep -E "^(name|description|tools):"
done
```

### 시스템 메시지 누락

```bash
# 시스템 메시지 없는 Skill
for f in semo-*/skills/*/SKILL.md; do
  if ! grep -q "시스템 메시지" "$f"; then
    echo "$f"
  fi
done
```

### "Use when" 패턴 누락

```bash
# description에 "Use when" 없는 Skill
for f in semo-*/skills/*/SKILL.md; do
  if ! head -n 10 "$f" | grep -q "Use when"; then
    echo "$f"
  fi
done
```

### 라인 수 확인

```bash
# 100 lines 초과
wc -l semo-*/skills/*/SKILL.md 2>/dev/null | awk '$1 > 100'

# references/ 없이 100+ lines
for dir in semo-*/skills/*/; do
  f="${dir}SKILL.md"
  if [ -f "$f" ]; then
    lines=$(wc -l < "$f")
    if [ "$lines" -gt 100 ] && [ ! -d "${dir}references" ]; then
      echo "$f: $lines lines (no references/)"
    fi
  fi
done
```

---

## Command 스캔

### 파일 존재 확인

```bash
# 모든 Command 파일
ls -la semo-*/commands/*.md 2>/dev/null
```

### Frontmatter 검증

```bash
# Command Frontmatter 추출
for f in semo-*/commands/*.md; do
  echo "=== $f ==="
  head -n 10 "$f" | grep -E "^(name|description):"
done
```

### CLAUDE.md 연동

```bash
# CLAUDE.md에 등록된 커맨드 확인
grep -E "^- /.*:" sax-*/CLAUDE.md 2>/dev/null
```

---

## 일괄 감사 스크립트

```bash
#!/bin/bash
# audit_sax.sh - 전체 SEMO 패키지 감사

echo "=== SEMO 패키지 통합 감사 ==="
echo "실행 일시: $(date)"
echo ""

# 1. 패키지 현황
echo "## 패키지 현황"
for pkg in sax-*/; do
  agents=$(ls -d ${pkg}agents/*/ 2>/dev/null | wc -l | tr -d ' ')
  skills=$(ls -d ${pkg}skills/*/ 2>/dev/null | wc -l | tr -d ' ')
  commands=$(ls ${pkg}commands/*.md 2>/dev/null 2>&1 | wc -l | tr -d ' ')
  echo "- $pkg: Agent=$agents, Skill=$skills, Command=$commands"
done
echo ""

# 2. Critical 문제
echo "## 🔴 Critical 문제"

echo "### Agent: model 필드 누락"
grep -rL "^model:" semo-*/agents/*/*.md 2>/dev/null || echo "(없음)"

echo ""
echo "### Agent: PROACTIVELY 패턴 누락"
grep -rL "PROACTIVELY use when" semo-*/agents/*/*.md 2>/dev/null || echo "(없음)"

echo ""
echo "### Skill: 시스템 메시지 누락"
for f in semo-*/skills/*/SKILL.md; do
  if [ -f "$f" ] && ! grep -q "시스템 메시지" "$f"; then
    echo "$f"
  fi
done
echo ""

# 3. Important 문제
echo "## 🟡 Important 문제"

echo "### Agent: 200 lines 초과"
wc -l semo-*/agents/*/*.md 2>/dev/null | awk '$1 > 200 {print $2 ": " $1 " lines"}'

echo ""
echo "### Skill: 100 lines 초과"
wc -l semo-*/skills/*/SKILL.md 2>/dev/null | awk '$1 > 100 {print $2 ": " $1 " lines"}'

echo ""
echo "=== 감사 완료 ==="
```

**실행**:

```bash
chmod +x audit_sax.sh
./audit_sax.sh > audit_report.md
```
