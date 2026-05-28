---
name: pre-work-research
description: >
  신규 기능 구현 전 PRE_WORK 워크플로우 자동화.
  오픈소스 검색, 중복 확인, Make vs Buy 분석 수행.
version: 2.0.0

triggers:
  keywords:
    - "신규 기능"
    - "오픈소스"
    - "라이브러리 검색"
    - "Make vs Buy"
    - "PRE_WORK"
  file_patterns: []
  context:
    - "새 기능 구현 전 조사"
    - "오픈소스 솔루션 검토"

capabilities:
  - github_search
  - make_vs_buy_analysis
  - duplicate_check

model_preference: sonnet

phase: [0]
auto_trigger: true
dependencies: []
token_budget: 1800
---

# PRE_WORK Research

신규 기능 구현 전 필수 사전 조사 워크플로우입니다.

## Quick Start

```bash
# GitHub 오픈소스 검색
python .claude/skills/pre-work-research/scripts/github_search.py "검색 키워드"

# Make vs Buy 분석 템플릿 생성
python .claude/skills/pre-work-research/scripts/github_search.py --analyze "기능명"
```

## 워크플로우

```
사용자 요청
    ↓
1. 오픈소스 검색 (MIT/Apache/BSD, Stars>500)
    ↓
2. 중복 확인 (gh issue/pr list)
    ↓
3. Make vs Buy 분석
    ↓
4. 사용자 승인
    ↓
구현 진행 (Phase 1)
```

## Step 1: 오픈소스 검색

### 검색 우선순위

| 우선순위 | 기준 |
|----------|------|
| 1순위 | MIT/Apache 2.0/BSD 라이선스 |
| 2순위 | Stars > 1k, 최근 커밋 < 6개월 |
| 3순위 | 상용 솔루션 (비용 명시) |
| 최후 | 직접 개발 (시간/비용 분석) |

### MCP 활용

```bash
# Exa 검색 (mcp__exa__search)
mcp__exa__search(query="Python logging library best 2025")

# Context7 문서 검색 (mcp__ref__search)
mcp__ref__search(query="FastAPI authentication patterns")
```

### 평가 체크리스트

- [ ] 라이선스 호환성 (MIT/Apache/BSD)
- [ ] 활성 유지보수 (최근 6개월 내 커밋)
- [ ] 커뮤니티 규모 (Stars, Issues 응답률)
- [ ] 문서화 품질
- [ ] 의존성 개수

## Step 2: 중복 확인

```bash
# 기존 이슈 확인
gh issue list --search "feature-name" --state all

# 기존 PR 확인
gh pr list --search "feature-name" --state all

# 관련 브랜치 확인
git branch -a | grep -i "feature-name"
```

### 중복 발견 시

1. 기존 이슈/PR 링크 첨부
2. 재사용 가능 여부 검토
3. 필요 시 기존 작업 확장

## Step 3: Make vs Buy 분석

### 분석 템플릿

```markdown
## Make vs Buy 분석: [기능명]

### Option A: 직접 개발 (Make)
- **예상 시간**: X일
- **복잡도**: 높음/중간/낮음
- **장점**: 커스터마이징 자유, 의존성 감소
- **단점**: 유지보수 부담, 개발 시간

### Option B: 오픈소스 활용 (Buy)
- **후보**: [라이브러리명] (Stars: X, License: MIT)
- **통합 시간**: X일
- **장점**: 검증된 솔루션, 커뮤니티 지원
- **단점**: 의존성 추가, 커스터마이징 제한

### 권장사항
[A 또는 B] 권장

**이유**: [구체적 근거]
```

### 의사결정 기준

| 조건 | Make | Buy |
|------|------|-----|
| 핵심 비즈니스 로직 | ✅ | - |
| 표준 기능 (인증, 로깅 등) | - | ✅ |
| 빠른 출시 필요 | - | ✅ |
| 높은 커스터마이징 필요 | ✅ | - |
| 장기 유지보수 리소스 있음 | ✅ | - |

## Step 4: 사용자 승인

분석 결과를 사용자에게 제시하고 승인을 받습니다.

```markdown
## PRE_WORK 결과 요약

### 검색 결과
- 후보 1: [라이브러리A] - Stars: 5k, License: MIT
- 후보 2: [라이브러리B] - Stars: 3k, License: Apache 2.0

### 중복 확인
- 관련 이슈: 없음 / #123 (유사)
- 관련 PR: 없음 / #456 (관련)

### 권장사항
[Buy: 라이브러리A 사용] / [Make: 직접 개발]

### 다음 단계
승인 시 Phase 1 (구현) 진행

**승인하시겠습니까? (Y/N)**
```

## 관련 도구

| 도구 | 용도 |
|------|------|
| `scripts/github_search.py` | GitHub 오픈소스 검색 |
| `references/oss-evaluation.md` | 평가 기준표 |
| `mcp__exa__search` | 웹 기술 검색 |
| `/pre-work` | 기존 Command (deprecated) |

---

> 관련: CLAUDE.md 섹션 3 Workflow
