---
name: implement
description: Spring Boot 서버 코드 구현을 시작합니다. spec.md 기반으로 멀티모듈 아키텍처에 맞게 코드를 작성합니다.
---

# Implement Skill (Spring Boot)

Spring Boot 멀티모듈 프로젝트의 구현을 수행합니다.

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

### 2. 기존 API 패턴 분석 (구현 전 필수)

새로운 API 구현 전 기존 코드 패턴을 분석합니다:

#### 2-1. Controller 패턴 분석
```bash
# 기존 Controller 파일 검색
Glob: **/sw-campus-api/**/*Controller.java
```

분석 항목:
- 패키지 구조: `com.swcampus.api.{domain}`
- 클래스 네이밍: `{Domain}Controller`
- URL 패턴: `/api/{domain}`, `/api/{domain}/{id}`
- HTTP 메서드 사용 패턴

#### 2-2. DTO 패턴 분석
```bash
# Request/Response DTO 검색
Glob: **/sw-campus-api/**/*Request.java
Glob: **/sw-campus-api/**/*Response.java
```

분석 항목:
- Request DTO: `{Action}{Domain}Request` (예: `CreateCourseRequest`)
- Response DTO: `{Domain}Response` (예: `CourseResponse`)
- Validation 어노테이션 사용 패턴

#### 2-3. Service 연동 패턴 분석
```bash
# Service 클래스 검색
Glob: **/sw-campus-domain/**/*Service.java
```

분석 항목:
- 의존성 주입 패턴 (생성자 주입)
- Transaction 경계 (@Transactional)
- 예외 처리 패턴

#### 2-4. Swagger 문서화 패턴
- `@Tag(name = "도메인명")` 사용
- `@Operation(summary = "...")` 사용
- `@ApiResponse` 상태 코드 패턴

### 3. 통합점 검증 (변경 영향도 확인)

기존 코드 변경 시 반드시 확인:

#### 3-1. 참조 분석
```bash
# 클래스/메서드 사용처 검색
Grep: "{클래스명}" 또는 "{메서드명}"
```

확인 항목:
- **Upstream**: 이 코드가 의존하는 것
- **Downstream**: 이 코드에 의존하는 것

#### 3-2. 모듈 경계 검증
- `api → domain` 의존: 허용
- `domain → 외부`: 금지
- `infra → domain` 의존: 허용
- `api → infra` 직접 의존: 금지 (runtimeOnly만)

#### 3-3. 인터페이스 호환성
- 메서드 시그니처 변경 시 모든 호출부 확인
- Repository 인터페이스 변경 시 구현체 확인

#### 3-4. Safety Checklist
- [ ] 모든 참조 확인 완료
- [ ] 공개 API 변경 없음 (또는 계획됨)
- [ ] 모듈 경계 준수
- [ ] 테스트 영향도 파악
- [ ] DB 마이그레이션 고려 (Entity 변경 시)

### 4. Plan 모드 진입

구현 계획 수립:
- 파일별 변경사항 정리
- 모듈별 구현 순서 확정
- 사용자 승인 요청

### 5. 구현 순서 (멀티모듈)

```
1. Domain 모듈 (sw-campus-domain)
   ├── Domain POJO 생성/수정
   │   └── 순수 Java 객체, JPA 의존 없음
   ├── Repository 인터페이스 정의
   │   └── 도메인 관점의 메서드 시그니처
   ├── Service 로직 구현
   │   └── 비즈니스 로직, 트랜잭션 관리
   └── Exception 클래스 추가

2. Infra 모듈 (sw-campus-infra/db-postgres)
   ├── Entity 생성/수정
   │   └── @Entity, JPA 매핑
   ├── JpaRepository 인터페이스
   │   └── Spring Data JPA 상속
   └── EntityRepository 구현체
       └── Domain Repository 구현

3. API 모듈 (sw-campus-api)
   ├── Request/Response DTO 생성
   │   └── 입력 검증, 변환 로직
   ├── Controller 구현
   │   └── HTTP 엔드포인트, 요청 처리
   └── Swagger 문서화
       └── @Tag, @Operation, @ApiResponse

4. 마이그레이션 (필요시)
   └── Flyway SQL 파일 추가
       └── V{version}__{description}.sql
```

### 6. 빌드 및 테스트

```bash
# 전체 빌드
./gradlew build

# 모듈별 테스트
./gradlew :sw-campus-domain:test
./gradlew :sw-campus-api:test

# API 테스트 (필요시)
./gradlew :sw-campus-api:bootRun
```

### 7. 결과 안내

```
✅ 구현 완료

변경된 파일:
- sw-campus-domain/src/main/.../
- sw-campus-infra/db-postgres/src/main/.../
- sw-campus-api/src/main/.../

다음 단계:
1. 로컬 테스트 실행
2. PR 생성
3. /done {PR번호} 실행하여 문서 업데이트
```

## 코딩 규칙

### 패키지 구조
```
com.swcampus.domain.{domain}    # Domain 모듈
com.swcampus.infra.{domain}     # Infra 모듈
com.swcampus.api.{domain}       # API 모듈
```

### 네이밍 컨벤션
| 구분 | 패턴 | 예시 |
|------|------|------|
| Controller | `{Domain}Controller` | `CourseController` |
| Service | `{Domain}Service` | `CourseService` |
| Repository (interface) | `{Domain}Repository` | `CourseRepository` |
| Repository (impl) | `{Domain}EntityRepository` | `CourseEntityRepository` |
| Entity | `{Domain}Entity` | `CourseEntity` |
| Request DTO | `{Action}{Domain}Request` | `CreateCourseRequest` |
| Response DTO | `{Domain}Response` | `CourseResponse` |

### 주의사항

- Controller에 비즈니스 로직 작성 금지
- Domain 모듈에 JPA/Spring 의존성 최소화
- Entity와 Domain POJO 간 변환 로직 명확히
- 예외는 도메인별 커스텀 예외 사용
- 파일 업로드 시 `@RequestPart` 사용 (`@ModelAttribute` 금지)

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
