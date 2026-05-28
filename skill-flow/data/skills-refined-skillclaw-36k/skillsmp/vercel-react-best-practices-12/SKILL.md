---
name: vercel-react-best-practices
description: React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements.
---

# Vercel 리액트 모범 사례 (Vercel React Best Practices)

Vercel 엔지니어링 팀에서 유지 관리하는 React 및 Next.js 애플리케이션을 위한 포괄적인 성능 최적화 가이드입니다. 자동화된 리팩토링과 코드 생성을 돕기 위해 영향도 순으로 우선순위가 매겨진 8개 카테고리, 45개 규칙을 포함합니다.

## 언제 적용하나요? (When to Apply)

다음 상황에서 이 가이드라인을 참조하세요:
- 새로운 React 컴포넌트나 Next.js 페이지를 작성할 때
- 데이터 페칭을 구현할 때 (클라이언트 또는 서버 사이드)
- 성능 이슈로 코드를 리뷰할 때
- 기존 React/Next.js 코드를 리팩토링할 때
- 번들 사이즈나 로딩 시간을 최적화할 때

## 우선순위별 규칙 카테고리 (Rule Categories by Priority)

| 우선순위 | 카테고리 | 영향도 | 접두사 |
|----------|----------|--------|--------|
| 1 | 워터폴(Waterfall) 제거 | **치명적 (CRITICAL)** | `async-` |
| 2 | 번들 사이즈 최적화 | **치명적 (CRITICAL)** | `bundle-` |
| 3 | 서버 사이드 성능 | 높음 (HIGH) | `server-` |
| 4 | 클라이언트 사이드 데이터 페칭 | 중간-높음 (MEDIUM-HIGH) | `client-` |
| 5 | 리렌더링 최적화 | 중간 (MEDIUM) | `rerender-` |
| 6 | 렌더링 성능 | 중간 (MEDIUM) | `rendering-` |
| 7 | 자바스크립트 성능 | 낮음-중간 (LOW-MEDIUM) | `js-` |
| 8 | 고급 패턴 | 낮음 (LOW) | `advanced-` |

## 빠른 참조 (Quick Reference)

### 1. 워터폴 제거 (Eliminating Waterfalls) - CRITICAL

- `async-defer-await` - `await`는 실제로 값이 필요한 분기 안으로 이동시키세요.
- `async-parallel` - 독립적인 작업은 `Promise.all()`을 사용해 병렬로 처리하세요.
- `async-dependencies` - 부분적인 의존성만 필요하다면 데이터를 미리 가져오세요.
- `async-api-routes` - API 라우트에서 프로미스는 일찍 시작하고, `await`는 늦게 하세요.
- `async-suspense-boundaries` - `Suspense`를 사용해 콘텐츠를 스트리밍하세요.

### 2. 번들 사이즈 최적화 (Bundle Size Optimization) - CRITICAL

- `bundle-barrel-imports` - 배럴 파일(index.js 등)을 통하지 말고 직접 임포트하세요.
- `bundle-dynamic-imports` - 무거운 컴포넌트는 `next/dynamic`을 사용하세요.
- `bundle-defer-third-party` - 분석/로깅 도구 등은 하이드레이션(Hydration) 이후에 로드하세요.
- `bundle-conditional` - 특정 기능이 활성화될 때만 모듈을 로드하세요.
- `bundle-preload` - 호버/포커스 시점에 리소스를 미리 로드(Preload)하세요.

### 3. 서버 사이드 성능 (Server-Side Performance) - HIGH

- `server-cache-react` - 요청(Request)당 중복 제거를 위해 `React.cache()`를 사용하세요.
- `server-cache-lru` - 요청 간 캐싱을 위해 LRU 캐시를 사용하세요.
- `server-serialization` - 클라이언트 컴포넌트로 전달하는 데이터 크기를 최소화하세요.
- `server-parallel-fetching` - 병렬 데이터 페칭이 가능하도록 컴포넌트 구조를 재조정하세요.
- `server-after-nonblocking` - 논블로킹 작업은 `after()`를 사용하세요.

### 4. 클라이언트 사이드 데이터 페칭 (Client-Side Data Fetching) - MEDIUM-HIGH

- `client-swr-dedup` - 자동 요청 중복 제거를 위해 `SWR`을 사용하세요.
- `client-event-listeners` - 전역 이벤트 리스너가 중복 등록되지 않게 하세요.

### 5. 리렌더링 최적화 (Re-render Optimization) - MEDIUM

- `rerender-defer-reads` - 콜백에서만 쓰이는 상태(State)는 미리 구독하지 마세요.
- `rerender-memo` - 비용이 큰 작업은 `memo` 컴포넌트로 분리하세요.
- `rerender-dependencies` - `useEffect` 의존성 배열에는 원시값(Primitive)을 넣으세요.
- `rerender-derived-state` - 원본 값이 아니라, 거기서 파생된 불리언(Boolean) 값을 구독하세요.
- `rerender-functional-setstate` - 콜백 안정성을 위해 함수형 `setState`를 사용하세요.
- `rerender-lazy-state-init` - 초기값이 비용이 크다면 `useState`에 함수를 전달하세요.
- `rerender-transitions` - 긴급하지 않은 업데이트는 `startTransition`을 사용하세요.

### 6. 렌더링 성능 (Rendering Performance) - MEDIUM

- `rendering-animate-svg-wrapper` - SVG 요소 대신 부모 `div` 래퍼를 애니메이션하세요.
- `rendering-content-visibility` - 긴 목록에는 `content-visibility` CSS 속성을 사용하세요.
- `rendering-hoist-jsx` - 정적인 JSX는 컴포넌트 외부로 빼세요.
- `rendering-svg-precision` - SVG 좌표 정밀도를 낮추세요.
- `rendering-hydration-no-flicker` - 클라이언트 전용 데이터는 인라인 스크립트를 사용해 깜빡임을 방지하세요.
- `rendering-activity` - 보여주고 숨길 때 `Activity` 컴포넌트를 사용하세요.
- `rendering-conditional-render` - 조건부 렌더링에는 `&&` 대신 삼항 연산자를 사용하세요.

### 7. 자바스크립트 성능 (JavaScript Performance) - LOW-MEDIUM

- `js-batch-dom-css` - CSS 변경은 클래스나 `cssText`로 한 번에 처리하세요.
- `js-index-maps` - 반복적인 조회(Lookup)가 필요하면 `Map`을 만드세요.
- `js-cache-property-access` - 루프 안에서는 객체 속성 접근을 캐싱하세요.
- `js-cache-function-results` - 함수 결과는 모듈 레벨 `Map`에 캐싱하세요.
- `js-cache-storage` - `localStorage/sessionStorage` 읽기를 캐싱하세요.
- `js-combine-iterations` - 여러 번의 `filter/map`을 하나의 루프로 합치세요.
- `js-length-check-first` - 비용이 큰 비교 전에 배열 길이부터 체크하세요.
- `js-early-exit` - 함수에서 조건이 맞지 않으면 빠르게 리턴(Early Return)하세요.
- `js-hoist-regexp` - 정규식 생성은 루프 밖으로 빼세요.
- `js-min-max-loop` - 정렬(sort) 대신 루프를 돌며 최소/최대값을 찾으세요.
- `js-set-map-lookups` - O(1) 조회를 위해 `Set`/`Map`을 사용하세요.
- `js-tosorted-immutable` - 불변성을 위해 `toSorted()`를 사용하세요.

### 8. 고급 패턴 (Advanced Patterns) - LOW

- `advanced-event-handler-refs` - 이벤트 핸들러는 `ref`에 저장하세요.
- `advanced-use-latest` - 안정적인 콜백 참조를 위해 `useLatest`를 사용하세요.

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
