# Backend 개발 가이드

FastAPI + SQLAlchemy + dependency-injector 기반 백엔드 개발 가이드

## 기술 스택

- **Framework**: FastAPI
- **ORM**: SQLAlchemy (async)
- **DI**: dependency-injector
- **Migration**: Alembic
- **Auth**: fastapi-users
- **Test**: pytest + pytest-asyncio

## 디렉토리 구조

```text
backend/app/
├── main.py              # FastAPI 앱 엔트리포인트
├── containers/          # DI 컨테이너
│   ├── application.py   # 메인 컨테이너
│   ├── database.py      # DB 컨테이너
│   └── services.py      # 서비스 컨테이너
├── core/
│   ├── settings/        # 환경별 설정
│   ├── models.py        # 공통 모델
│   ├── middlewares.py   # 미들웨어
│   └── errors/          # 에러 핸들링
├── db/
│   ├── base.py          # Base 클래스
│   ├── session.py       # SessionManager
│   ├── tables.py        # ORM 테이블 정의
│   └── migrations/      # Alembic 마이그레이션
├── auth/                # 인증 모듈
└── [domain]/            # 도메인별 모듈
    ├── models.py        # Pydantic 스키마
    ├── repository.py    # 데이터 접근 계층
    ├── service.py       # 비즈니스 로직
    └── view.py          # API 라우터
```

## 레이어드 아키텍처

```text
View (Router) → Service → Repository → DB
```

### View (Router)

```python
# app/lecture/view.py
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

app_router = APIRouter()

@app_router.get("", response_model=FetchLecturesSchema)
@inject
async def get_lectures(
    page: int = Query(1, ge=1),
    lecture_svc: BaseLectureService = Depends(
        Provide[ApplicationContainer.services.lecture_service]
    ),
):
    lectures, meta = await lecture_svc.get_recommended(page, per_page)
    return FetchLecturesSchema(data=lectures, meta=meta)
```

### Service

```python
# app/lecture/service.py
import abc

class BaseLectureService(abc.ABC):
    def __init__(self, repository: BaseLectureRepository) -> None:
        self.lecture_repository = repository

    @abc.abstractmethod
    async def get_recommended(self, page: int, per_page: int) -> tuple[list, Meta]:
        raise NotImplementedError

class LectureService(BaseLectureService):
    async def get_recommended(self, page: int, per_page: int):
        return await self.lecture_repository.fetch_lectures(page, per_page)
```

### Repository

```python
# app/lecture/repository.py
import abc
from sqlalchemy import select
from app.db.session import SessionManager

class BaseLectureRepository(abc.ABC):
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    @abc.abstractmethod
    async def fetch_lectures(self, page: int, per_page: int):
        raise NotImplementedError

class LectureRepository(BaseLectureRepository):
    async def fetch_lectures(self, page: int, per_page: int):
        async with self._session_manager.async_session() as session:
            result = await session.execute(
                select(tb.Lecture)
                .offset((page - 1) * per_page)
                .limit(per_page)
            )
            return result.scalars().all()
```

## DI 컨테이너

```python
# app/containers/services.py
from dependency_injector import containers, providers

class ServicesContainer(containers.DeclarativeContainer):
    database = providers.DependenciesContainer()

    lecture_service = providers.Factory(
        LectureService,
        repository=providers.Factory(
            LectureRepository,
            session_manager=database.session_manager,
        ),
    )
```

## Pydantic 스키마

```python
# app/lecture/models.py
from pydantic import BaseModel

class LectureInList(BaseModel):
    id: int
    title: str
    description: str | None

class FetchLecturesSchema(BaseModel):
    data: list[LectureInList]
    meta: PaginationMeta
```

## 테스트

### 실행

```bash
cd backend && uv run pytest
```

### Fixture 구조

```python
# tests/conftest.py
@pytest.fixture
async def test_session() -> AsyncSession:
    # 테스트용 DB 세션

# tests/api/conftest.py
@pytest.fixture
async def client() -> AsyncClient:
    # 테스트용 HTTP 클라이언트

@pytest.fixture
async def authorized_client_admin() -> AsyncClient:
    # 관리자 권한 클라이언트
```

### 테스트 작성

```python
# tests/api/test_lecture.py
import pytest
from httpx import AsyncClient

pytest_plugins = ["tests.conftest", "tests.api.conftest"]

@pytest.fixture
async def dummy_lectures(test_session: AsyncSession):
    # 테스트 데이터 생성
    async with test_session.begin():
        test_session.add_all(lectures)
    await test_session.commit()

async def test_sut_fetch_lectures(client: AsyncClient, dummy_lectures):
    response = await client.get("/lecture?page=1&per_page=20")

    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 20
```

### 테스트 네이밍

- `test_sut_` 접두사 사용 (System Under Test)
- 한글 설명 대신 명확한 영문 함수명

## 커맨드

| 명령어 | 설명 |
|--------|------|
| `uv run pytest` | 테스트 실행 |
| `uv run pytest -v` | 상세 출력 |
| `uv run pytest tests/api/test_lecture.py` | 특정 파일 |
| `uv run pytest -k "fetch"` | 패턴 매칭 |
| `uv run alembic upgrade head` | 마이그레이션 |
| `uv run alembic revision --autogenerate -m "msg"` | 마이그레이션 생성 |

## 주의사항

- Abstract Base Class로 인터페이스 정의
- Repository에서 ORM → Pydantic 매핑
- DI 컨테이너로 의존성 주입
- pytest-asyncio의 `--asyncio-mode=auto` 사용
- 테스트 fixture로 데이터 격리
