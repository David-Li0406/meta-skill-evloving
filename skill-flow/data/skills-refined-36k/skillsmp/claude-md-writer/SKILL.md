---
name: claude-md-writer
description: CLAUDE.md 파일을 best practices에 맞게 수정/관리. Use when updating project instructions, adding new sections, or refactoring CLAUDE.md for clarity and conciseness. (project)
---

# CLAUDE.md Writer

CLAUDE.md는 **모든 대화에 자동 포함**되는 유일한 파일. 간결하고 보편적으로 작성해야 함.

---

## Core Principle

> "LLMs are stateless functions" - 매 세션마다 필요한 정보 제공
> "The context window is a public good" - 간결성 최우선

---

## 필수 구조: WHAT / WHY / HOW

| 섹션 | 내용 | 예시 |
|------|------|------|
| **WHAT** | 기술 스택, 프로젝트 구조 | "React 19 + Supabase + BGE-M3" |
| **WHY** | 프로젝트 목적, 각 부분 기능 | "수의안과 논문 검색 플랫폼" |
| **HOW** | 작업 방법, 명령어, 도구 | "npm run dev", "supabase functions serve" |

---

## 제한 사항

### 길이
- **권장**: 300줄 미만
- **이상적**: 60줄 이내
- Claude Code 자체가 ~50개 명령 포함 → 추가 명령 최소화

### 포함하지 말 것
| 항목 | 이유 | 대안 |
|------|------|------|
| 코드 스타일 가이드 | 린터 역할 금지 | Biome, ESLint 사용 |
| 상세 DB 스키마 | 특정 작업용 | `agent_docs/` 분리 |
| 긴 코드 예시 | 컨텍스트 낭비 | `file:line` 참조 |
| 일회성 정보 | 보편성 부족 | 작업 시 직접 전달 |

---

## 점진적 공개 패턴

**CLAUDE.md는 목록과 설명만, 상세 내용은 분리:**

```
agent_docs/
  ├── building_the_project.md
  ├── running_tests.md
  ├── code_conventions.md
  └── service_architecture.md
```

**CLAUDE.md에서 참조:**
```markdown
## 상세 가이드
- `agent_docs/building_the_project.md` - 빌드 방법
- `agent_docs/service_architecture.md` - 아키텍처 설명
```

---

## 수정 워크플로우

### 1. 추가 요청 시
```
사용자: "강의 자료 저장 구조 CLAUDE.md에 추가해줘"
```

**Before (나쁜 예):**
- 장황한 설명 추가
- 코드 블록 다수 포함
- 중복 정보

**After (좋은 예):**
```markdown
### 강의 자료 (이중 저장)
| 저장소 | 위치 | 검색 |
|--------|------|------|
| Qdrant | `textbook_chunks` | Vector |
| Supabase | `lecture_chunks` | BM25 |
```

### 2. 리팩토링 시

**체크리스트:**
- [ ] 300줄 이하인가?
- [ ] 모든 작업에 관련된 정보만 있는가?
- [ ] 중복 제거했는가?
- [ ] `file:line` 참조 사용했는가?
- [ ] 상세 내용은 분리했는가?

### 3. 검증

```bash
# 줄 수 확인
wc -l CLAUDE.md
# 권장: < 300
```

---

## 좋은 예 / 나쁜 예

### 기술 스택

**나쁜 예:**
```markdown
프론트엔드는 React 19를 사용하며 TypeScript로 작성됩니다.
Vite를 빌드 도구로 사용하고 TailwindCSS로 스타일링합니다.
상태 관리는 React의 기본 훅을 사용하며...
```

**좋은 예:**
```markdown
| 레이어 | 기술 |
|--------|------|
| Frontend | React 19 + TypeScript + Vite + TailwindCSS |
| Backend | Supabase (PostgreSQL + Edge Functions) |
```

### 파일 참조

**나쁜 예:**
```markdown
타입 정의는 다음과 같습니다:
\`\`\`typescript
export interface Paper {
  id: string;
  title: string;
  // ... 100줄
}
\`\`\`
```

**좋은 예:**
```markdown
**TypeScript 타입**: `frontend/src/types/supabase.types.ts`
```

### 명령어

**나쁜 예:**
```markdown
개발 서버를 시작하려면 먼저 frontend 디렉토리로 이동한 다음
npm install 명령어로 의존성을 설치하고
그 후 npm run dev 명령어를 실행하면 됩니다.
```

**좋은 예:**
```markdown
### 개발
\`\`\`bash
cd frontend && npm install && npm run dev
\`\`\`
```

---

## InsightsOphVet CLAUDE.md 현재 구조

```
1. 프로젝트 개요 (WHAT/WHY)
2. 필수 규칙
3. 개발 명령어 (HOW)
4. 기술 스택 (WHAT)
5. DB 스키마 참조
6. Edge Functions 목록
7. Frontend Pages 목록
8. 검색 파이프라인
9. 환경 변수
10. 프로젝트 구조
11. Skills 목록
12. 작업 시 참고
```

**현재 줄 수**: ~270줄 (권장 범위 내)

---

## Quick Actions

### 섹션 추가
1. 해당 섹션 위치 확인
2. 테이블 또는 간단한 목록으로 작성
3. 상세 내용은 `file:line` 참조

### 중복 제거
1. CTRL+F로 키워드 검색
2. 같은 정보 여러 번 등장 시 하나로 통합
3. 가장 적절한 섹션에 배치

### 분리 필요 시
1. `agent_docs/` 또는 `.claude/context/` 폴더 생성
2. 상세 내용 이동
3. CLAUDE.md에 참조 추가

---

**Last updated**: 2025-12-29
**Version**: 1.0.0
