---
name: changelog-writer
description: |
  SEMO 변경사항을 블로그 원고로 자동 기록. Use when:
  (1) 버저닝 완료 후 자동 호출, (2) 주요 기능 추가/삭제 시,
  (3) 아키텍처 변경 시.
tools: [Read, Write, Edit, Bash, Glob]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: changelog-writer 호출` 시스템 메시지를 첫 줄에 출력하세요.

# changelog-writer Skill

> SEMO 변경사항을 블로그 원고로 자동 기록

## Purpose

버저닝 완료 후 주요 변경사항을 `docs/blog/drafts/` 디렉토리에 원고로 기록합니다.
이 원고들은 나중에 블로그 포스팅으로 편집됩니다.

## Trigger

### 자동 호출 (version-manager 체인)

```text
version-manager 완료
    ↓
[자동] changelog-writer 호출
    ↓
변경사항 분석 → 원고 생성
```

### 수동 호출

- "변경사항 원고 작성해줘"
- "블로그 원고 업데이트"
- "릴리스 노트 정리"

## Workflow

### 1. 변경사항 수집

```bash
# 최근 커밋에서 변경사항 추출
git log --oneline -10

# CHANGELOG 파일 확인
cat semo-system/semo-core/CHANGELOG/{version}.md

# 버전 정보
cat semo-system/semo-core/VERSION
```

### 2. 변경 유형 분류

| 유형 | 키워드 | 원고 포함 |
|------|--------|----------|
| **Major** | 아키텍처, 구조 변경 | ✅ 필수 |
| **Feature** | feat, 신규 기능 | ✅ 필수 |
| **Fix** | fix, 버그 수정 | ⚠️ 중요한 것만 |
| **Refactor** | refactor, 개선 | ⚠️ 영향 큰 것만 |
| **Docs** | docs, 문서 | ❌ 제외 |
| **Chore** | chore, 잡무 | ❌ 제외 |

### 3. 원고 생성

```markdown
# docs/blog/drafts/{YYYY-MM-DD}-{package}-{version}.md

---
date: {YYYY-MM-DD}
package: {package_name}
version: {version}
type: {major|minor|patch}
status: draft
---

# {Package} {Version} 변경사항

## 주요 변경

### {변경 제목 1}

{상세 설명}

**Before:**
{이전 동작/구조}

**After:**
{변경 후 동작/구조}

### {변경 제목 2}

...

## 마이그레이션 가이드

{필요한 경우}

## 관련 커밋

- {commit_hash}: {commit_message}
- ...

## 태그

#semo #{package} #v{version}
```

### 4. 원고 저장

```text
docs/blog/drafts/
├── 2024-12-29-semo-core-2.2.0.md
├── 2024-12-29-semo-scripts-1.1.0.md
└── 2024-12-29-semo-agents-1.0.0.md
```

## Output Format

### 성공

```markdown
[SEMO] Skill: changelog-writer 호출

## 원고 생성 완료

| 파일 | 패키지 | 버전 | 유형 |
|------|--------|------|------|
| 2024-12-29-semo-core-2.2.0.md | semo-core | 2.2.0 | minor |

📝 원고 위치: docs/blog/drafts/

💡 다음 단계:
1. 원고 검토 및 편집
2. docs/blog/로 이동
3. 00-series-index.md 업데이트
```

### 스킵 (변경사항 없음)

```markdown
[SEMO] Skill: changelog-writer 호출

ℹ️ 블로그 원고 불필요
- 유형: patch (버그 수정)
- 사유: 마이너 변경으로 원고 생성 스킵

💡 주요 변경 시에만 원고가 생성됩니다.
```

## 🔴 version-manager 연동

### version-manager SKILL.md에 추가할 내용

```markdown
## 🔴 블로그 원고 자동 생성 (선택)

버저닝 완료 후 **주요 변경** 시 changelog-writer를 호출합니다:

| 버전 유형 | 원고 생성 |
|----------|----------|
| MAJOR | ✅ 자동 |
| MINOR (기능 추가) | ✅ 자동 |
| MINOR (개선) | ⚠️ 선택 |
| PATCH | ❌ 스킵 |

**호출 조건:**
- CHANGELOG에 `## Added` 또는 `## Changed` 섹션이 있는 경우
- 커밋 메시지에 `feat:` 또는 `refactor:` 접두사가 있는 경우
```

## 원고 템플릿

### Major Release

```markdown
---
date: 2024-12-29
package: semo-core
version: 2.0.0
type: major
status: draft
---

# SEMO Core 2.0.0 - 대규모 재구성

## 개요

이번 릴리스에서는 {핵심 변경 요약}.

## Breaking Changes

### 1. {Breaking Change 1}

**영향받는 사용자:** {누가 영향 받는지}

**이전 방식:**
```
{code/config}
```

**새로운 방식:**
```
{code/config}
```

**마이그레이션:**
```bash
{migration steps}
```

## 새로운 기능

### {Feature 1}

{설명}

## 개선사항

### {Improvement 1}

{설명}

## 관련 링크

- [GitHub Release](https://github.com/semicolon-devteam/semo/releases/tag/v2.0.0)
- [마이그레이션 가이드](../docs/migration-v2.md)

## 태그

#semo #semo-core #v2.0.0 #breaking-change
```

### Minor Release

```markdown
---
date: 2024-12-29
package: semo-core
version: 2.2.0
type: minor
status: draft
---

# SEMO Core 2.2.0 - /SEMO:health 커맨드 추가

## 새로운 기능

### /SEMO:health 커맨드

환경 헬스체크를 위한 새 커맨드가 추가되었습니다.

**사용법:**
```
/SEMO:health
```

**출력 예시:**
```markdown
## .claude 디렉토리 검증 결과

| 항목 | 상태 | 비고 |
|------|------|------|
| semo-core | ✅ | 존재 |
| agents/ | ✅ | 6 symlinks |
```

## 관련 커밋

- 1f3e066: feat(core): #SEMO:health 커맨드 추가

## 태그

#semo #semo-core #v2.2.0 #health-check
```

## 디렉토리 구조

```
docs/blog/
├── 00-series-index.md    # 시리즈 목차
├── 01-beginning.md       # 1편
├── ...
├── 08-v5-restructuring.md # 8편
└── drafts/                # 원고 디렉토리
    ├── README.md          # 원고 작성 가이드
    ├── 2024-12-29-semo-core-2.2.0.md
    └── ...
```

## Related

- [version-manager Skill](../version-manager/SKILL.md) - 버저닝 후 체인 호출
- [Blog Series Index](../../../../docs/blog/00-series-index.md) - 블로그 시리즈
