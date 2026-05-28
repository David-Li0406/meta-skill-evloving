---
name: vercel-react-best-practices
description: >
  Vercel Engineering의 React/Next.js 성능 최적화 가이드.
  49개 규칙, 8개 카테고리, 영향도 기반 우선순위.
version: 1.0.0

triggers:
  keywords:
    - "React 최적화"
    - "Next.js 성능"
    - "waterfall"
    - "bundle size"
    - "SSR"
    - "RSC"
    - "서버 컴포넌트"
    - "리렌더링"
    - "React 성능"
  file_patterns:
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/next.config.*"
  context:
    - "React 컴포넌트 리뷰"
    - "성능 최적화 요청"
    - "코드 리뷰"

capabilities:
  - detect_async_waterfalls
  - suggest_bundle_optimization
  - review_server_components
  - recommend_rerender_fixes

model_preference: sonnet
phase: [2]
auto_trigger: true
dependencies:
  - frontend-dev
  - code-reviewer
token_budget: 2000
---

# Vercel React Best Practices

Vercel Engineering의 React/Next.js 성능 최적화 가이드입니다.

## 개요

**Version 1.0.0** | Vercel Engineering | January 2026

이 스킬은 AI 에이전트와 LLM이 React/Next.js 코드베이스를 유지보수, 생성, 리팩토링할 때 따라야 할 종합 성능 최적화 가이드입니다.

## 영향도별 카테고리

| 우선순위 | 카테고리 | 규칙 수 | 설명 |
|:--------:|----------|:-------:|------|
| **CRITICAL** | Eliminating Waterfalls | 5 | async waterfall 제거 |
| **CRITICAL** | Bundle Size Optimization | 5 | 번들 크기 최적화 |
| **HIGH** | Server-Side Performance | 5 | 서버 사이드 성능 |
| **MEDIUM-HIGH** | Client-Side Data Fetching | 4 | 클라이언트 데이터 페칭 |
| **MEDIUM** | Re-render Optimization | 7 | 리렌더링 최적화 |
| **MEDIUM** | Rendering Performance | 7 | 렌더링 성능 |
| **LOW-MEDIUM** | JavaScript Performance | 12 | JS 성능 최적화 |
| **LOW** | Advanced Patterns | 2 | 고급 패턴 |

## Quick Reference

### CRITICAL 이슈 (즉시 수정 필요)

#### 1. Waterfall 제거
```typescript
// ❌ 잘못된 예: sequential await
const user = await fetchUser()
const posts = await fetchPosts()

// ✅ 올바른 예: parallel execution
const [user, posts] = await Promise.all([
  fetchUser(),
  fetchPosts()
])
```

#### 2. Barrel File 피하기
```typescript
// ❌ 잘못된 예: 전체 라이브러리 import
import { Check, X } from 'lucide-react'

// ✅ 올바른 예: 직접 import
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
```

### HIGH 이슈

#### 서버 컴포넌트 직렬화 최소화
```tsx
// ❌ 잘못된 예: 모든 필드 전달
<Profile user={user} />  // 50개 필드

// ✅ 올바른 예: 필요한 필드만 전달
<Profile name={user.name} />  // 1개 필드
```

### MEDIUM 이슈

#### 함수형 setState 사용
```typescript
// ❌ 잘못된 예: stale closure 위험
setItems([...items, newItem])

// ✅ 올바른 예: 안전한 업데이트
setItems(curr => [...curr, newItem])
```

## 사용법

### 코드 리뷰 시
```
/check --react [파일경로]
```

### 성능 분석 시
```
/check --react --perf
```

### 전체 검사
```
/check --all
```

## 상세 규칙

전체 규칙은 `AGENTS.md`를 참조하세요:
- 8개 카테고리의 상세 설명
- 49개 규칙의 잘못된 예 / 올바른 예
- 영향도 및 최적화 효과

## 관련 리소스

- [React 공식 문서](https://react.dev)
- [Next.js 공식 문서](https://nextjs.org)
- [SWR](https://swr.vercel.app)
- [better-all](https://github.com/shuding/better-all)
- [Vercel 성능 블로그](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)

## 에이전트 연동

이 스킬은 다음 에이전트와 자동 연동됩니다:

| 에이전트 | 연동 내용 |
|----------|----------|
| `frontend-dev` | React 컴포넌트 작업 시 자동 참조 |
| `code-reviewer` | 코드 리뷰 시 성능 규칙 적용 |

---

> Source: [Vercel Labs Agent Skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices)
