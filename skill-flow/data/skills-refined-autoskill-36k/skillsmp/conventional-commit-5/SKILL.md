---
name: conventional-commit
description: Use when writing commit messages or understanding conventional commit format. CSO keywords: 커밋 메시지, commit message, feat fix refactor, breaking change, 커밋 규칙, atomic commit, 원자적 커밋
---

# Conventional Commit Guide

Conventional Commit 형식으로 커밋 메시지를 작성하는 방법을 안내합니다. 사용자가 "커밋 메시지 형식", "conventional commit", "커밋 컨벤션", "커밋 규칙" 등에 대해 질문할 때 이 skill을 사용합니다.

---

## Conventional Commit 형식

커밋 메시지의 기본 구조는 다음과 같다:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Type (필수)

변경 사항의 종류를 나타내는 prefix:

| Type | 설명 | 사용 시점 |
|------|------|----------|
| `feat` | 새로운 기능 추가 | 사용자에게 보이는 새 기능 구현 |
| `fix` | 버그 수정 | 기존 기능의 오류 해결 |
| `refactor` | 코드 리팩토링 | 기능 변경 없이 코드 개선 |
| `docs` | 문서 변경 | README, 주석, API 문서 등 |
| `test` | 테스트 추가/수정 | 테스트 코드 관련 변경 |
| `chore` | 빌드/설정 변경 | package.json, 설정 파일 등 |
| `style` | 코드 스타일 변경 | 포맷팅, 세미콜론 등 (기능 변경 없음) |
| `perf` | 성능 개선 | 속도, 메모리 사용량 최적화 |
| `ci` | CI/CD 변경 | GitHub Actions, Jenkins 등 |
| `build` | 빌드 시스템 변경 | Webpack, Docker 등 |

### Scope (선택)

변경된 영역이나 모듈을 괄호 안에 명시:

```
feat(user): 사용자 프로필 API 추가
fix(auth): JWT 토큰 만료 처리 버그 수정
refactor(cache): Redis 캐시 서비스 분리
```

일반적인 scope 예시:
- 모듈명: `user`, `auth`, `payment`
- 레이어명: `api`, `db`, `ui`
- 기능명: `login`, `checkout`, `search`

### Description (필수)

변경 사항을 간결하게 설명:
- 한글로 작성 (팀 규칙에 따라)
- 명령형/현재형 사용
- 첫 글자 소문자 (영어의 경우)
- 마침표 없음
- 50자 이내 권장

---

## 커밋 분리 기준

### 원자적 커밋 (Atomic Commit)

하나의 커밋은 하나의 논리적 변경만 포함해야 한다:

**좋은 예**:
```
커밋 1: feat(user): 사용자 프로필 조회 API 추가
커밋 2: feat(user): 사용자 프로필 수정 API 추가
커밋 3: test(user): 사용자 프로필 API 테스트 추가
```

**나쁜 예**:
```
커밋 1: feat(user): 사용자 프로필 API 추가 및 테스트, 버그 수정
```

### 분리 기준

1. **기능 단위**: 각 기능은 별도 커밋
2. **모듈 단위**: 다른 모듈 변경은 분리
3. **롤백 가능성**: 독립적으로 롤백 가능한 단위

---

## 변경 유형별 예시

### feat - 기능 추가

```
feat(user): 사용자 프로필 API 추가

- GET /api/users/:id/profile 엔드포인트 구현
- 프로필 이미지 URL 필드 추가
```

포함되는 변경:
- 새 엔드포인트 추가
- 새 엔티티/DTO 생성
- 새 서비스 메서드 추가

### fix - 버그 수정

```
fix(auth): JWT 토큰 만료 시 갱신 실패 수정

토큰 갱신 요청 시 리프레시 토큰이 누락되던 문제 해결
```

포함되는 변경:
- 기존 로직 오류 수정
- 예외 처리 추가
- 조건문 수정

### refactor - 리팩토링

```
refactor(cache): Redis 연결 풀 관리 개선

- 연결 풀 크기를 환경변수로 설정 가능하게 변경
- 연결 실패 시 재시도 로직 추가
```

포함되는 변경:
- 코드 구조 개선
- 중복 코드 제거
- 네이밍 변경

### docs - 문서

```
docs(readme): API 사용 가이드 추가
```

### test - 테스트

```
test(user): 프로필 수정 API 통합 테스트 추가
```

### chore - 설정/빌드

```
chore(deps): lodash 4.17.21로 업데이트
```

### style - 스타일

```
style(lint): ESLint 규칙 적용
```

### perf - 성능

```
perf(query): 사용자 목록 조회 쿼리 최적화

- email 컬럼에 인덱스 추가
- N+1 쿼리 문제 해결
```

### ci - CI/CD

```
ci(github): PR 자동 라벨링 워크플로우 추가
```

### build - 빌드

```
build(docker): 멀티스테이지 빌드로 이미지 크기 최적화
```

---

## Breaking Changes

API 호환성이 깨지는 변경은 다음과 같이 표시:

```
feat(api)!: 사용자 응답 형식 변경

BREAKING CHANGE: 사용자 API 응답에서 'name' 필드가 'displayName'으로 변경됨
```

또는 footer에:
```
feat(api): 사용자 응답 형식 변경

BREAKING CHANGE: 사용자 API 응답에서 'name' 필드가 'displayName'으로 변경됨
```

---

## 커밋 메시지 작성 팁

1. **왜(Why)에 집중**: 무엇을 했는지보다 왜 했는지 설명
2. **문맥 제공**: 관련 이슈 번호, PR 링크 포함
3. **읽는 사람 고려**: 6개월 후 자신도 이해할 수 있게
4. **일관성 유지**: 팀/프로젝트 규칙 준수

---

## 한글 커밋 메시지 가이드

한글로 커밋 메시지를 작성할 때:

```
feat(user): 사용자 프로필 조회 기능 추가
fix(auth): 로그인 시 토큰 갱신 오류 수정
refactor(db): 데이터베이스 연결 로직 분리
docs(api): Swagger 문서 업데이트
test(payment): 결제 API 단위 테스트 추가
```

**피해야 할 표현**:
- ❌ "~함", "~했음" → ✅ "~추가", "~수정"
- ❌ "버그 픽스" → ✅ "버그 수정"
- ❌ "신규 피처" → ✅ "새 기능" 또는 "기능 추가"
