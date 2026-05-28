---
name: implement
description: Next.js 클라이언트 코드 구현을 시작합니다. spec.md 기반으로 Feature-Sliced 아키텍처에 맞게 코드를 작성합니다.
---

# Implement Skill (Next.js)

Next.js App Router + Feature-Sliced 아키텍처 프로젝트의 구현을 수행합니다.

## 사용법

```
/implement {feature-name}
```

feature-name을 생략하면 현재 작업 중인 feature를 자동 감지합니다.

## 실행 단계

### 1. 문서 읽기

- `sw-campus-docs/features/{feature-name}/spec.md` 읽기
- `sw-campus-docs/features/{feature-name}/prd.md` 읽기 (컨텍스트)
- `sw-campus-docs/features/{feature-name}/sequence/*.md` 읽기 (흐름 파악)
- **코드 규칙**: `.claude/rules/`에서 자동 로드됨

### 2. 기존 코드 패턴 분석 (구현 전 필수)

새로운 기능 구현 전 기존 코드 패턴을 분석합니다:

#### 2-1. Feature 구조 분석
```bash
# 기존 feature 폴더 확인
Glob: src/features/*/
```

분석 항목:
- 폴더 구조: `api/`, `components/`, `hooks/`, `types/`
- index.ts public API 패턴
- 컴포넌트 분리 기준

#### 2-2. API 함수 패턴 분석
```bash
# API 파일 검색
Glob: src/features/*/api/*.ts
```

분석 항목:
- Axios 인스턴스 사용 패턴 (`lib/axios.ts`)
- 에러 핸들링 패턴
- Request/Response 타입 정의

#### 2-3. Hook 패턴 분석
```bash
# Hook 파일 검색
Glob: src/features/*/hooks/*.ts
```

분석 항목:
- TanStack Query 사용 패턴 (`useQuery`, `useMutation`)
- Query key 네이밍 컨벤션
- 낙관적 업데이트 패턴

#### 2-4. 컴포넌트 패턴 분석
```bash
# 컴포넌트 파일 검색
Glob: src/features/*/components/*.tsx
```

분석 항목:
- 서버/클라이언트 컴포넌트 구분
- Props 타입 정의 패턴
- Tailwind CSS 클래스 패턴

### 3. 통합점 검증 (변경 영향도 확인)

기존 코드 변경 시 반드시 확인:

#### 3-1. 참조 분석
```bash
# 컴포넌트/훅 사용처 검색
Grep: "import.*from.*'{모듈명}'"
```

확인 항목:
- 어느 페이지에서 사용되는가
- 어느 컴포넌트에서 import하는가

#### 3-2. 타입 호환성
- API 응답 타입 변경 시 모든 사용처 확인
- Props 타입 변경 시 부모 컴포넌트 확인

#### 3-3. Safety Checklist
- [ ] 모든 import 확인 완료
- [ ] 타입 변경 시 영향도 파악
- [ ] 서버/클라이언트 컴포넌트 경계 확인
- [ ] API 변경 시 서버와 동기화 필요 여부 확인

### 4. Plan 모드 진입

구현 계획 수립:
- 파일별 변경사항 정리
- 구현 순서 확정
- 사용자 승인 요청

### 5. 구현 순서 (Feature-Sliced)

```
1. Types 정의
   └── src/features/{domain}/types/
       └── {domain}.type.ts
       └── API 요청/응답 타입, 도메인 모델 타입

2. API 함수
   └── src/features/{domain}/api/
       └── {domain}Api.ts
       └── Axios 인스턴스 사용, 에러 핸들링

3. Hooks
   └── src/features/{domain}/hooks/
       └── use{Domain}Query.ts (조회)
       └── use{Domain}Mutation.ts (변경)
       └── TanStack Query 기반

4. Components
   └── src/features/{domain}/components/
       └── {Domain}Card.tsx
       └── {Domain}List.tsx
       └── {Domain}Form.tsx
       └── 서버/클라이언트 컴포넌트 구분

5. Pages (App Router)
   └── src/app/{route}/
       └── page.tsx (서버 컴포넌트 우선)
       └── layout.tsx (필요시)
       └── loading.tsx (필요시)

6. Public API (index.ts)
   └── src/features/{domain}/index.ts
       └── 외부에 노출할 API만 export
```

### 6. 빌드 및 테스트

```bash
# 개발 서버 실행
pnpm dev

# 타입 체크
pnpm tsc --noEmit

# Lint 검사
pnpm lint

# 프로덕션 빌드
pnpm build
```

### 7. 결과 안내

```
✅ 구현 완료

변경된 파일:
- src/features/{domain}/types/...
- src/features/{domain}/api/...
- src/features/{domain}/hooks/...
- src/features/{domain}/components/...
- src/app/{route}/...

다음 단계:
1. 로컬 테스트 실행 (pnpm dev)
2. PR 생성
3. /done {PR번호} 실행하여 문서 업데이트
```

## 코딩 규칙

### 파일 네이밍 (kebab-case)
| 구분 | 패턴 | 예시 |
|------|------|------|
| 컴포넌트 | kebab-case.tsx | `course-card.tsx` |
| Hook | use-{name}.ts | `use-course-query.ts` |
| API | {domain}-api.ts | `course-api.ts` |
| 타입 | {domain}.type.ts | `course.type.ts` |

> 파일명은 kebab-case, export 이름은 PascalCase/camelCase

### 컴포넌트 규칙

```tsx
// 서버 컴포넌트 (기본)
export default async function CoursePage() {
  const courses = await fetchCourses();
  return <CourseList courses={courses} />;
}

// 클라이언트 컴포넌트 (필요시에만)
"use client";
export function CourseFilter() {
  const [filter, setFilter] = useState("");
  return <input value={filter} onChange={e => setFilter(e.target.value)} />;
}
```

### 상태 관리 규칙

```tsx
// 서버 상태: TanStack Query
const { data, isLoading } = useCourseQuery(courseId);

// 클라이언트 상태 (UI): Zustand
const { isModalOpen, openModal } = useUIStore();

// ❌ 금지: API 응답을 Zustand에 저장
// ❌ 금지: 컴포넌트에서 직접 API 호출
```

### API 호출 규칙

```tsx
// ✅ feature hook 사용
import { useCourseQuery } from '@/features/course';

// ❌ 직접 API 호출 금지
import { courseApi } from '@/features/course/api';
```

### TailwindCSS 규칙

```tsx
// ✅ 토큰 사용
<div className="bg-primary text-foreground rounded-md">

// ❌ 하드코딩 금지
<div className="bg-[#3B82F6] text-[#FFFFFF] rounded-[8px]">
```

### 주의사항

- 컴포넌트 내부에서 직접 API 호출 금지 (feature hooks 사용)
- API 응답을 Zustand에 저장 금지 (TanStack Query 캐시 사용)
- 서버 컴포넌트 우선, 필요시에만 `"use client"` 선언
- Axios 인스턴스(`lib/axios.ts`) 사용 필수
- TailwindCSS 토큰 사용, 하드코딩 색상/radius 금지

## PR 생성 시 Base 브랜치 자동 감지

```bash
# 분기점 확인 후 적절한 base 브랜치 선택
DEVELOP_MERGE_BASE=$(git merge-base HEAD develop 2>/dev/null)
MAIN_MERGE_BASE=$(git merge-base HEAD main 2>/dev/null)

if [ -n "$DEVELOP_MERGE_BASE" ]; then
  DEVELOP_DISTANCE=$(git rev-list --count $DEVELOP_MERGE_BASE..HEAD)
else
  DEVELOP_DISTANCE=999999
fi

if [ -n "$MAIN_MERGE_BASE" ]; then
  MAIN_DISTANCE=$(git rev-list --count $MAIN_MERGE_BASE..HEAD)
else
  MAIN_DISTANCE=999999
fi

if [ "$DEVELOP_DISTANCE" -le "$MAIN_DISTANCE" ]; then
  BASE_BRANCH="develop"
else
  BASE_BRANCH="main"
fi

gh pr create --base $BASE_BRANCH ...
```
