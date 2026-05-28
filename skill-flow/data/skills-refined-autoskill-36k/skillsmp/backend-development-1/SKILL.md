---
name: backend-development
description: ForkLore 백엔드(Django/DRF) 개발 워크플로우 스킬. 이슈 기반 개발 + develop 브랜치 전략 + TDD(RED-GREEN-REFACTOR) + 서비스 레이어(views는 thin wrapper) + StandardJSONRenderer/camelCase API 규약 + drf-spectacular 문서화 + ruff/pytest 커맨드까지 한 번에 강제한다. Use when working on backend features/bugfixes, services.py, serializers.py, views.py, migrations, API schema, pytest/ruff, or when asked to create PR targeting develop.
requires-skills:
  - tdd-flow
  - python-patterns
  - lint-and-validate
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Backend Development (ForkLore)

ForkLore 백엔드(Django) 개발을 **이슈 기반 + TDD + develop 중심 브랜치 전략**으로 일관되게 진행하기 위한 표준 워크플로.

## Quick Reference (빠른 참조)

### 자주 쓰는 커맨드

```bash
# 테스트
poetry run pytest                              # 전체 테스트
poetry run pytest apps/novels/tests/           # 특정 앱
poetry run pytest -k "test_create"             # 키워드 매칭
poetry run pytest --cov=apps                   # 커버리지

# 린트/포맷
poetry run ruff check apps/                    # 린트 체크
poetry run ruff check apps/ --fix              # 자동 수정
poetry run ruff format apps/                   # 포맷

# 마이그레이션
poetry run python manage.py makemigrations     # 생성
poetry run python manage.py migrate            # 적용
poetry run python manage.py showmigrations     # 상태 확인

# 서버
poetry run python manage.py runserver          # 로컬
docker compose up -d                           # Docker
```

### Context7 빠른 조회

```python
# Django 최신 패턴
context7_query-docs(libraryId="/websites/djangoproject_en_5_2", query="...")

# DRF 최신 패턴  
context7_query-docs(libraryId="/encode/django-rest-framework", query="...")

# drf-spectacular
context7_query-docs(libraryId="/tfranzel/drf-spectacular", query="...")
```

## 소스 오브 트루스

- 레포 전체 규칙: `AGENTS.md`
- 백엔드 구조/원칙: `backend/AGENTS.md`
- API 규약(응답 래핑, camelCase, pagination): `docs/api-specification.md`
- 백엔드 아키텍처(서비스 레이어 등): `docs/backend-architecture.md`
- Git 이슈/브랜치/커밋/PR: `docs/development-guidelines.md`

## 필수 원칙 (하드 룰)

- **TDD 필수**: RED(테스트 먼저) → GREEN(최소 구현) → REFACTOR(정리)
- **Service Layer 필수**: 비즈니스 로직/트랜잭션/도메인 규칙은 `apps/*/services*.py`에 위치
- **View는 thin wrapper**: 입력 검증(Serializer) → Service 호출 → `Response(serializer.data)`만 반환
- **응답 래핑 금지**: View에서 `{success, data, ...}` 직접 만들지 말 것 (renderer가 처리)
  - 설정: `backend/config/settings/base.py`
  - 구현: `backend/common/renderers.py`, `backend/common/exceptions.py`
- **외부 JSON은 camelCase, 내부는 snake_case**
  - parser/renderer 설정: `backend/config/settings/base.py`
- **문서화는 drf-spectacular**: schema 변경 시 Swagger/Redoc 정합성 유지

## 워크플로우

### 1) 이슈 확인/생성 (GitHub)

- 작업 시작 전 GitHub에서 관련 이슈가 있는지 검색한다.
- 없으면 새 이슈를 생성하고, 요구사항/범위/완료 조건(AC)을 간단히 정리한다.

### 2) 브랜치 생성 (Base: develop)

- `develop` 최신화 후, 이슈 기준으로 새 브랜치를 만든다.
- 브랜치명 규칙: `feat/#<issue>-<short-english-summary>` 또는 `fix/#<issue>-<short-english-summary>`

### 3) 개발 환경 준비 (로컬 or Docker)

로컬(Poetry):
```bash
cd backend
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Docker Compose(권장: DB/Redis 포함):
```bash
docker compose up -d
docker compose exec backend poetry run python manage.py migrate
docker compose exec backend poetry run python manage.py runserver 0.0.0.0:8000
```

### 4) TDD - RED (테스트 먼저 작성)

- 기능 구현 전, 실패하는 테스트를 먼저 작성한다.
- 대상 레벨을 명확히 선택:
  - Service/Domain Unit 테스트
  - Serializer Unit 테스트
  - View/API Integration 테스트(APIClient)
  - 핵심 플로우는 E2E 테스트로 보강: `backend/tests/e2e/`

테스트 위치(관례): `backend/apps/<domain>/tests/`

### 5) TDD - GREEN (최소 구현)

- 테스트를 통과하는 “최소 코드”만 작성한다.
- 권장 책임 분리:
  - View/ViewSet: 요청/응답, 검증, 인증/권한, 문서화
  - Service: 트랜잭션/도메인 규칙/외부 연동/여러 모델 조합
  - Model: 관계/제약/단순 도메인 메서드

### 6) TDD - REFACTOR (정리)

- 테스트 통과를 유지한 채로 코드 품질을 개선한다.
- 중복 제거, 네이밍 정리, 서비스 경계 조정(과도한 View 로직 제거) 등을 수행한다.

### 7) 모델 변경 시 마이그레이션 생성/적용

```bash
cd backend
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

PRD/API/DB 문서와 스키마가 충돌하면 “정합성”부터 먼저 맞춘다.

### 8) API 규약 반영 (필수)

- 응답 래퍼 규약(Success/Failure)을 유지한다.
  - renderer: `backend/common/renderers.py`
  - exception handler: `backend/common/exceptions.py`
- Pagination은 `page(1-indexed)`, `size`를 기본으로 한다.
- API JSON은 camelCase, 내부 코드는 snake_case 원칙을 지킨다.
- 문서화(OpenAPI 3.1)는 drf-spectacular 기준으로 최신 상태를 유지한다.

### 9) Context7로 최신 사용법 확인 (필수)

**모든 라이브러리 사용 시 Context7로 최신 버전/패턴을 확인한다.**

#### 필수 확인 라이브러리 (ForkLore 스택)

| 라이브러리 | Context7 ID | 주요 확인 사항 |
|------------|-------------|----------------|
| Django 5.x+ | `/websites/djangoproject_en_5_2` | async views, ORM, composite PK |
| DRF 3.x | `/encode/django-rest-framework` | ViewSet, Serializer, pagination |
| drf-spectacular | `/tfranzel/drf-spectacular` | OpenAPI 3.1 스키마 생성 |
| Celery | `resolve-library-id`로 확인 | task, beat, worker 패턴 |
| pytest-django | `resolve-library-id`로 확인 | fixtures, markers, db 접근 |

#### Context7 활용 워크플로우

```
1. 라이브러리 사용 전:
   context7_resolve-library-id(libraryName="djangorestframework", query="DRF viewset pagination")
   
2. 최신 패턴 확인:
   context7_query-docs(libraryId="/encode/django-rest-framework", query="pagination best practices")
   
3. 코드 적용 시:
   - deprecated 경고 발견 → 즉시 대체 구현
   - 최신 권장 패턴 우선 적용
   - 버전별 차이 주의 (Django 5.x vs 4.x)
```

#### 언제 Context7를 확인해야 하는가?

| 상황 | Context7 필수 |
|------|---------------|
| 새 라이브러리 도입 | ✅ 반드시 |
| 기존 패턴 확신 없음 | ✅ 반드시 |
| deprecated 경고 발생 | ✅ 반드시 |
| 버전 업그레이드 후 | ✅ 반드시 |
| 익숙한 패턴 반복 사용 | ⚪ 선택 |

### 10) 전체 테스트/커버리지 확인

```bash
cd backend
poetry run pytest
poetry run pytest --cov=apps
```

### 11) 린트/포맷 + 보안/민감정보 점검

```bash
cd backend
poetry run ruff check apps/
poetry run ruff format apps/

git diff --cached
```

- `.env`, `.env.local`, `*.secret` 등은 커밋 금지(.gitignore 확인)
- `SECRET`, `PASSWORD`, `API_KEY` 등 의심 문자열 포함 여부 점검

### 12) 커밋/푸시/PR 생성 (Target: develop)

- “하나의 feature 단위”가 끝날 때마다 커밋한다.
- PR 생성 시 포함:
  - 이슈 링크/설명/테스트 결과
  - 마이그레이션 여부
  - API 변경점(엔드포인트/필드/응답)

## 연관 스킬 활용 (Skill Composition)

백엔드 개발 중 상황에 따라 다음 스킬을 적극 활용한다:

| 상황 | 활용 스킬 | 트리거 키워드 |
|------|-----------|---------------|
| **테스트 실패 시** | `/test-fixing` | 테스트 실패, pytest error, make tests pass |
| **TDD 상세 패턴** | `/tdd-flow` | RED-GREEN-REFACTOR 세부 절차 |
| **디버깅 막힐 때** | `/systematic-debugging` | 버그, 에러, 원인 불명, 2회 이상 실패 |
| **Python 패턴 고민** | `/python-patterns` | async, 프레임워크 선택, 타입힌트 |
| **코드 린트/검증** | `/lint-and-validate` | ruff, mypy, 포맷, 린트 |
| **API 패턴 검토** | `/api-pattern` | REST, 응답 포맷, pagination |
| **Docker 이슈** | `/docker-expert` | 컨테이너, 이미지, docker-compose |
| **코드 리뷰 요청** | `/requesting-code-review` | PR 생성 전, 머지 전 검토 |
| **코드 리뷰 수신** | `/receiving-code-review` | 리뷰 피드백 받았을 때 |
| **Git 작업** | `/git-master` (내장) | commit, rebase, squash, blame |

### 스킬 활용 규칙

1. **TDD 실패 시**: 2회 이상 테스트 실패 → `/systematic-debugging` 먼저 invoke
2. **PR 생성 전**: `/requesting-code-review` invoke로 셀프 리뷰 수행
3. **린트 에러 시**: `/lint-and-validate` invoke 후 자동 수정 시도
4. **라이브러리 사용 전 (필수)**: Context7로 최신 패턴 확인
   - `context7_resolve-library-id` → 라이브러리 ID 획득
   - `context7_query-docs` → 최신 사용법/권장 패턴 확인
   - deprecated 발견 시 → 즉시 대체 구현 적용
5. **새 패턴 적용 시**: Context7 + `/python-patterns` 함께 참조

### 워크플로우 예시 (스킬 체이닝 + Context7)

```
사용자: "Novel 모델에 word_count 필드 추가해줘"

1. 이슈 확인/생성 → GitHub CLI
2. 브랜치 생성 → /git-master
3. Context7 확인 → Django 5.x 모델 필드 최신 패턴 조회
   - context7_query-docs(libraryId="/websites/djangoproject_en_5_2", query="IntegerField model field")
4. TDD RED → /tdd-flow 참조하여 테스트 먼저 작성
5. TDD GREEN → 최소 구현 (Model + Migration)
6. TDD REFACTOR → 정리
7. 테스트 실패 시 → /systematic-debugging
8. 린트 체크 → /lint-and-validate
9. PR 생성 전 → /requesting-code-review
10. 커밋/푸시 → /git-master
```

### 복잡한 기능 워크플로우 (Context7 집중 활용)

```
사용자: "Celery로 비동기 이메일 발송 기능 추가해줘"

1. Context7로 라이브러리 ID 확인
   - context7_resolve-library-id(libraryName="celery", query="celery django async task")
2. Context7로 최신 패턴 조회
   - context7_query-docs(libraryId="...", query="shared_task django email")
3. /python-patterns 참조 → async 패턴 결정
4. TDD RED → 테스트 작성 (/tdd-flow)
5. 서비스 레이어 구현 (services.py + tasks.py)
6. TDD GREEN/REFACTOR
7. Docker 설정 필요 시 → /docker-expert
8. 린트/PR → /lint-and-validate + /requesting-code-review
```

## 빠른 파일 네비게이션

- 설정/규약
  - `backend/config/settings/base.py`
  - `backend/common/renderers.py`
  - `backend/common/exceptions.py`
- 서비스 레이어 예시
  - `backend/apps/users/services.py`
  - `backend/apps/contents/services.py`
  - `backend/apps/novels/services/novel_service.py`
  - `backend/apps/novels/services/branch_service.py`
- 테스트 예시
  - `backend/apps/novels/tests/test_services.py`
  - `backend/apps/contents/tests/test_chapter_services.py`
  - `backend/common/tests/test_renderers.py`

## Quality Checklist (PR 전 필수 점검)

PR 생성 전 아래 항목을 모두 확인한다:

### 코드 품질
- [ ] TDD 사이클 완료 (RED → GREEN → REFACTOR)
- [ ] 비즈니스 로직이 `services.py`에 위치
- [ ] View는 thin wrapper (입력 검증 → Service 호출 → Response)
- [ ] 타입 힌트 적용 (함수 인자, 반환값)
- [ ] Docstring 작성 (Google Style)

### 테스트
- [ ] `poetry run pytest` 전체 통과
- [ ] 새 기능에 대한 테스트 존재
- [ ] 커버리지 감소 없음 (`--cov=apps`)

### 린트/포맷
- [ ] `poetry run ruff check apps/` 에러 없음
- [ ] `poetry run ruff format apps/` 적용

### API 규약
- [ ] 응답 래핑 직접 안 함 (renderer가 처리)
- [ ] JSON 필드 camelCase (외부) / snake_case (내부)
- [ ] drf-spectacular 스키마 정합성

### 보안/민감정보
- [ ] `.env`, 시크릿 파일 커밋 안 함
- [ ] `SECRET`, `PASSWORD`, `API_KEY` 하드코딩 없음

### 마이그레이션
- [ ] 모델 변경 시 마이그레이션 파일 생성/적용
- [ ] 기존 데이터 영향도 검토

## Works well with

| 스킬 | 용도 |
|------|------|
| `/tdd-flow` | TDD RED-GREEN-REFACTOR 상세 절차 |
| `/python-patterns` | Python/Django async, 타입힌트, 프레임워크 패턴 |
| `/lint-and-validate` | Ruff 린트, MyPy 타입 체크 |
| `/api-pattern` | REST API 설계, 응답 포맷, pagination |
| `/systematic-debugging` | 버그 원인 분석, 디버깅 전략 |
| `/docker-expert` | 컨테이너, Docker Compose 설정 |
| `/requesting-code-review` | PR 생성 전 셀프 리뷰 |
| `/git-master` | 커밋, 브랜치, rebase, squash |
