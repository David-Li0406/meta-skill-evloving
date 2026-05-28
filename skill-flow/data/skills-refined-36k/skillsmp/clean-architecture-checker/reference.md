# Clean Architecture Reference

This document provides detailed reference information for implementing Clean Architecture in Polibase.

## Architecture Migration Status

**Overall: 🟢 100% Complete** ✅

| Layer | Files | Status |
|-------|-------|--------|
| Domain | 77 | ✅ 100% |
| Application | 37 | ✅ 100% |
| Infrastructure | 63 | ✅ 100% |
| Interfaces | 63 | ✅ 100% |
| **Legacy Cleanup** | ~20 | ✅ 100% |

**Completed**:
- ✅ All 22 domain repositories have infrastructure implementations
- ✅ All 21 use cases implemented
- ✅ Full async/await support across all repositories
- ✅ Complete dependency inversion (Domain ← Infrastructure)
- ✅ `ISessionAdapter` complete with `get()` and `delete()` (Issue #592)
- ✅ CLI fully migrated to `src/interfaces/cli/` (Issue #641, Phase 5/5)
- ✅ Web UI migrated to `src/interfaces/web/streamlit/`
- ✅ Legacy Streamlit directories removed (`src/streamlit/`, `src/interfaces/streamlit/`) (Issue #602)
- ✅ `src/models/` directory completely removed (Issue #640, Phase 4/5)
  - All DTOs migrated to `src/application/dtos/`
  - All entities migrated to `src/domain/entities/`
  - All tests updated to use domain entities and DTOs
- ✅ `src/cli_package/` completely migrated to `src/interfaces/cli/` (Issue #641, Phase 5/5)
- ✅ All deprecated files removed (cli.py, exceptions.py, process_minutes.py, monitoring_app.py)
- ✅ All backward compatibility stubs removed
- ✅ 100% Clean Architecture compliance achieved

参考:
- [CLEAN_ARCHITECTURE_MIGRATION.md](../../../docs/CLEAN_ARCHITECTURE_MIGRATION.md) - Migration guide
- [tmp/clean_architecture_analysis_2025.md](../../../tmp/clean_architecture_analysis_2025.md) - Detailed analysis

## Layer Structure

### 1. Domain Layer (`src/domain/`) - ✅ Complete (77 files)

**Purpose**: Core business logic and rules

**Contains**:

#### Entities (21 files)
Core business objects with business rules:
- `BaseEntity`: Common fields and methods for all entities
- Business entities: `Politician`, `Speaker`, `Meeting`, `Conference`, `Proposal`, `Conversation`, `Minutes`, `GoverningBody`, `PoliticalParty`, `PoliticianAffiliation`, `ExtractedConferenceMember`, `ParliamentaryGroup`, `ParliamentaryGroupMembership`, etc.

#### Repository Interfaces (22 files)
Abstract interfaces for data access:
- `BaseRepository[T]`: Generic repository with common CRUD operations
  - `create()`, `get()`, `update()`, `delete()`, `list()`
- `ISessionAdapter`: Database session abstraction (Issue #592: now complete with `get()` and `delete()` methods)
- Entity-specific repositories with additional query methods:
  - `IPoliticianRepository`: `find_by_name_and_party()`, `find_duplicates()`
  - `ISpeakerRepository`: `find_by_name()`, `find_unmatched()`
  - `IConversationRepository`: `find_by_meeting()`, `find_by_speaker()`
  - など各エンティティ用のリポジトリインターフェース

#### Domain Services (18 files)
Business logic that doesn't belong to entities:
- `SpeakerDomainService`: Name normalization, party extraction, similarity calculation
- `PoliticianDomainService`: Deduplication, validation, merging logic
- `MinutesDomainService`: Text processing, conversation extraction
- `ConferenceDomainService`: Member role extraction
- `ParliamentaryGroupDomainService`: Group membership validation
- `SpeakerMatchingService`, `PoliticianMatchingService`: Matching algorithms

#### Service Interfaces (8 files)
External service abstractions:
- `ILLMService`: LLM API抽象化
- `IStorageService`: ファイルストレージ抽象化
- `IWebScraperService`: Webスクレイピング抽象化
- `ITextExtractorService`: テキスト抽出抽象化
- その他外部サービスのインターフェース

**Rules**:
- ✅ No imports from outer layers
- ✅ Framework-independent (no SQLAlchemy, no Streamlit)
- ✅ Only Python standard library and minimal dependencies
- ✅ All repository interfaces use `async def`

### 2. Application Layer (`src/application/`) - ✅ Complete (37 files)

**Purpose**: Application-specific business rules and orchestration

**Contains**:

#### Use Cases (15 files)
Application-specific business rules:
- `ProcessMinutesUseCase`: Orchestrates minutes processing workflow
- `MatchSpeakersUseCase`: Speaker-politician matching coordination
- `ManageConferenceMembersUseCase`: Conference member management
- `ExtractConferenceMembersUseCase`: Conference member extraction
- `MatchConferenceMembersUseCase`: Conference member matching
- `CreateAffiliationsUseCase`: Affiliation creation
- `Extract*UseCase`, `Manage*UseCase`: Various data processing and management

各UseCaseの責務:
- リポジトリとサービスの調整
- トランザクション境界の定義
- エラーハンドリング
- ビジネスロジックのオーケストレーション

#### DTOs (16+ files)
Data Transfer Objects for clean layer separation:
- Input/Output DTOs for each use case
- Prevents domain model leakage to outer layers
- Includes validation logic
- 例: `ProcessMinutesInputDTO`, `ProcessMinutesOutputDTO`

**DTOの配置ルール（Issue #969）**:
- ✅ DTOは `src/application/dtos/` に専用ファイルとして配置
- ✅ 関連するDTOは同一ファイルにまとめる（例: `politician_dto.py`）
- ❌ **UseCaseファイル内にDTO定義を混在させない**
- ✅ 後方互換性のため、UseCaseファイルからre-exportは許容

```python
# ✅ GOOD: DTOは専用ファイルに配置
# src/application/dtos/politician_dto.py
@dataclass
class CreatePoliticianInputDto: ...

@dataclass
class CreatePoliticianOutputDto: ...

# src/application/usecases/manage_politicians_usecase.py
from src.application.dtos.politician_dto import (
    CreatePoliticianInputDto,
    CreatePoliticianOutputDto,
)

class ManagePoliticiansUseCase:
    async def create(self, dto: CreatePoliticianInputDto) -> CreatePoliticianOutputDto:
        ...
```

```python
# ❌ BAD: UseCaseファイル内にDTO定義が混在
# src/application/usecases/manage_politicians_usecase.py
@dataclass
class CreatePoliticianInputDto: ...  # ← ここに書かない！

class ManagePoliticiansUseCase:
    ...
```

**Rules**:
- ✅ Import only from Domain layer
- ✅ Use repository interfaces (not implementations)
- ✅ Accept and return DTOs (not entities)
- ✅ No direct database access
- ✅ No UI concerns

### 3. Infrastructure Layer (`src/infrastructure/`) - ✅ Complete (63 files)

**Purpose**: External system integrations and implementations

**Contains**:

#### Persistence (22+ files)
Database access implementations:
- `BaseRepositoryImpl[T]`: Generic SQLAlchemy repository using `ISessionAdapter`
- All 22 domain repositories have corresponding implementations:
  - `PoliticianRepositoryImpl`
  - `SpeakerRepositoryImpl`
  - `ConversationRepositoryImpl`
  - `MeetingRepositoryImpl`
  - `ConferenceRepositoryImpl`
  - など
- `AsyncSessionAdapter`: Adapts sync sessions for async usage
- `UnitOfWorkImpl`: Transaction management implementation

#### External Services
Third-party integrations:
- `GeminiLLMService`: Google Gemini API integration
- `CachedLLMService`, `InstrumentedLLMService`: Decorator pattern for caching and instrumentation
- `GCSStorageService`: Google Cloud Storage integration
- `WebScraperService`: Playwright-based web scraping
- `MinutesProcessingService`, `ProposalScraperService`: Domain-specific services

#### Infrastructure Support
- **DI Container** (`di/`): Dependency injection setup
- **Logging** (`logging/`): Structured logging configuration
- **Monitoring** (`monitoring/`): Performance metrics collection
- **Error Handling** (`error_handling/`): Centralized error management

**Rules**:
- ✅ Import from Domain and Application layers
- ✅ Implement repository interfaces
- ✅ Depend on abstractions (not concretions)
- ✅ Use async/await consistently

### 4. Interfaces Layer (`src/interfaces/`) - ✅ Mostly Complete (63 files)

**Purpose**: User interfaces and external API endpoints

**Contains**:

#### CLI (`src/interfaces/cli/`)
Command-line interfaces:
- Unified `sagebase` command entry point
- Structured commands organized by category:
  - `scraping/`: Web scraping commands
  - `database/`: Database management commands
  - `processing/`: Data processing commands
  - `monitoring/`: Monitoring commands

#### Web (`src/interfaces/web/streamlit/`)
Streamlit UI:
- `views/`: Page views for各entity types
  - `politician_view.py`
  - `speaker_view.py`
  - `meeting_view.py`
  - など
- `presenters/`: Business logic presentation layer
- `components/`: Reusable UI components
- `dto/`: UI-specific data transfer objects
- Complete separation of business logic from UI

**Rules**:
- ✅ Import from all inner layers
- ✅ Depend on Use Cases (not repositories directly)
- ✅ Handle user input validation
- ✅ Format output for presentation

## When Adding New Features

Clean Architectureに従って新機能を追加する際の推奨手順：

1. **Start with Domain Entities and Services**
   - `src/domain/entities/` に必要なエンティティを定義
   - `src/domain/services/` にビジネスロジックを実装

2. **Define Repository Interfaces Needed**
   - `src/domain/repositories/` にリポジトリインターフェースを定義
   - 必要なメソッドをasync defで宣言

3. **Create Use Cases in Application Layer**
   - `src/application/usecases/` にユースケースを実装
   - Input/Output DTOを `src/application/dtos/` に定義

4. **Implement Infrastructure (Repositories, External Services)**
   - `src/infrastructure/persistence/` にリポジトリ実装を追加
   - 必要に応じて外部サービス統合を実装

5. **Add Interface Layer Last (CLI/Web)**
   - `src/interfaces/cli/` または `src/interfaces/web/` にUI/CLI追加
   - ユースケースを呼び出してDTOをやり取り

6. **Write Tests at Each Layer**
   - Domain: ユニットテスト（モック不要）
   - Application: ユニットテスト（リポジトリをモック）
   - Infrastructure: 統合テスト（実際のDB使用）
   - Interfaces: E2Eテスト

## Dependency Rule
- ✅ Import from Domain and Application
- ✅ Implement interfaces defined in Domain
- ✅ All repository methods are `async def`
- ✅ Use `ISessionAdapter` for database operations
- ✅ Convert between domain entities and SQLAlchemy models

### Interfaces Layer (`src/interfaces/`)

**Purpose**: User interface and external API adapters

**Contains**:
- **CLI** (`src/interfaces/cli/`): Command-line interfaces
  - Unified `sagebase` command
  - Command groups: `scraping/`, `database/`, `processing/`
- **Web** (`src/interfaces/web/streamlit/`): Web UI
  - `views/`: Page views
  - `presenters/`: Business logic presentation
  - `components/`: Reusable UI components
  - `dto/`: UI-specific DTOs

**Rules**:
- ✅ Import from all inner layers
- ✅ Use use cases (not repositories directly)
- ✅ Convert between UI format and DTOs
- ✅ No business logic (delegate to use cases)
- ❌ No imports between different Interface modules

## Repository Pattern Details

### Interface Definition (Domain)

```python
# src/domain/repositories/politician_repository.py
from typing import Protocol
from src.domain.entities.politician import Politician
from src.domain.repositories.base_repository import BaseRepository

class IPoliticianRepository(BaseRepository[Politician]):
    """Repository interface for Politician entities."""

    async def find_by_name(self, name: str) -> list[Politician]:
        """Find politicians by exact name match."""
        ...

    async def find_by_party(self, party_id: int) -> list[Politician]:
        """Find all politicians belonging to a party."""
        ...

    async def search_by_name_fuzzy(
        self, name: str, threshold: float = 0.8
    ) -> list[tuple[Politician, float]]:
        """Fuzzy search politicians by name with similarity scores."""
        ...
```

### Implementation (Infrastructure)

```python
# src/infrastructure/persistence/politician_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.politician import Politician
from src.domain.repositories.politician_repository import IPoliticianRepository
from src.infrastructure.persistence.base_repository import BaseRepositoryImpl
from src.infrastructure.persistence.models.politician import Politician as PoliticianModel

class PoliticianRepositoryImpl(
    BaseRepositoryImpl[Politician], IPoliticianRepository
):
    """SQLAlchemy implementation of IPoliticianRepository."""

    def __init__(self, session: AsyncSession):
        super().__init__(session, PoliticianModel, Politician)

    async def find_by_name(self, name: str) -> list[Politician]:
        query = select(PoliticianModel).where(PoliticianModel.name == name)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def find_by_party(self, party_id: int) -> list[Politician]:
        query = select(PoliticianModel).where(
            PoliticianModel.party_id == party_id
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    def _to_entity(self, model: PoliticianModel) -> Politician:
        """Convert SQLAlchemy model to domain entity."""
        return Politician(
            id=model.id,
            name=model.name,
            party_id=model.party_id,
            furigana=model.furigana,
            # ... other fields
        )

    def _to_model(self, entity: Politician) -> PoliticianModel:
        """Convert domain entity to SQLAlchemy model."""
        return PoliticianModel(
            id=entity.id,
            name=entity.name,
            party_id=entity.party_id,
            furigana=entity.furigana,
            # ... other fields
        )
```

## Use Case Pattern Details

### Use Case Structure

```python
# src/application/usecases/create_politician_usecase.py
from src.application.dto.politician_dto import (
    CreatePoliticianInputDTO,
    CreatePoliticianOutputDTO,
)
from src.domain.repositories.politician_repository import IPoliticianRepository
from src.domain.repositories.political_party_repository import IPoliticalPartyRepository
from src.domain.services.politician_domain_service import PoliticianDomainService
from src.domain.entities.politician import Politician

class CreatePoliticianUseCase:
    """Use case for creating a new politician."""

    def __init__(
        self,
        politician_repository: IPoliticianRepository,
        party_repository: IPoliticalPartyRepository,
        politician_service: PoliticianDomainService,
    ):
        self.politician_repository = politician_repository
        self.party_repository = party_repository
        self.politician_service = politician_service

    async def execute(
        self, input_dto: CreatePoliticianInputDTO
    ) -> CreatePoliticianOutputDTO:
        """
        Execute the use case.

        Args:
            input_dto: Input data for creating a politician

        Returns:
            Output DTO with result information

        Raises:
            ValueError: If party doesn't exist or data is invalid
        """
        # Validate party exists
        party = await self.party_repository.find_by_id(input_dto.party_id)
        if party is None:
            raise ValueError(f"Party with id {input_dto.party_id} not found")

        # Check for duplicates using domain service
        existing = await self.politician_repository.find_by_name(input_dto.name)
        if self.politician_service.has_duplicate(input_dto.name, existing):
            raise ValueError(f"Politician {input_dto.name} already exists")

        # Create entity
        politician = Politician(
            id=None,  # Will be assigned by database
            name=input_dto.name,
            party_id=input_dto.party_id,
            furigana=input_dto.furigana,
        )

        # Save to repository
        saved_politician = await self.politician_repository.save(politician)

        # Return output DTO
        return CreatePoliticianOutputDTO(
            success=True,
            politician_id=saved_politician.id,
            message=f"Successfully created politician: {saved_politician.name}",
        )
```

## UseCase間依存（Orchestratorパターン）（Issue #969）

### 許容されるUseCase間依存

Clean Architectureでは通常UseCase間の直接依存は避けるべきですが、以下のケースは**Orchestratorパターン**として許容されます：

```
ExecuteMinutesProcessingUseCase（Orchestrator）
  └── UpdateStatementFromExtractionUseCase（抽出ログ統合）

MatchSpeakersUseCase（Orchestrator）
  └── UpdateSpeakerFromExtractionUseCase（抽出ログ統合）
```

### 許容の理由

1. **Bronze Layer / Gold Layer アーキテクチャの保護**（ADR-0005）
   - `UpdateEntityFromExtractionUseCase` 基底クラスは、人間の手動修正を保護する重要な機能を持つ
   - `is_manually_verified` フラグのチェックが組み込まれている
   - この保護機構をバイパスすると、人間の修正がAI抽出結果で上書きされる危険性がある

2. **トランザクション境界の管理**
   - 抽出ログ保存とエンティティ更新は同一トランザクション内で行う必要がある
   - UseCase分離よりもデータ整合性を優先

### ガイドライン

```python
# ✅ GOOD: OrchestratorパターンによるUseCase間依存
class ExecuteMinutesProcessingUseCase:
    def __init__(
        self,
        update_statement_usecase: UpdateStatementFromExtractionUseCase,  # 許容
        # 他の依存性...
    ):
        self.update_statement_usecase = update_statement_usecase

    async def execute(self, dto: ExecuteMinutesProcessingDTO) -> None:
        # 処理実行...

        # 抽出ログ統合UseCaseを呼び出し（保護機構が働く）
        await self.update_statement_usecase.execute(extraction_result)
```

```python
# ❌ BAD: 保護機構をバイパスして直接更新
class ExecuteMinutesProcessingUseCase:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
        extraction_log_repo: ExtractionLogRepository,
    ):
        ...

    async def execute(self, dto: ExecuteMinutesProcessingDTO) -> None:
        # ❌ 直接更新すると is_manually_verified チェックが行われない！
        await self.conversation_repo.update(conversation)
        await self.extraction_log_repo.create(log)
```

### UseCase間依存を避けるべきケース

- 循環依存が発生する場合
- 単純なCRUD操作のみの場合
- 保護機構が不要な場合

## Domain Service vs Entity

### When to Use Domain Services

Use domain services when:
- Logic involves multiple entities
- Logic doesn't naturally belong to any single entity
- Logic requires external dependencies (repositories, etc.)
- Logic is a pure algorithm or calculation

### When to Use Entity Methods

Use entity methods when:
- Logic operates on single entity's data
- Logic is intrinsic to the entity's identity
- Logic doesn't require external dependencies
- Logic is simple state change or validation

### Example: Speaker Name Normalization

**Domain Service** (correct placement):
```python
# src/domain/services/speaker_domain_service.py
class SpeakerDomainService:
    """Domain service for speaker-related business logic."""

    HONORIFICS = ["氏", "君", "議員", "委員", "さん"]

    def normalize_name(self, raw_name: str) -> str:
        """
        Normalize speaker name by removing honorifics and standardizing format.

        Args:
            raw_name: Raw name from minutes

        Returns:
            Normalized name
        """
        name = raw_name.strip()
        name = name.replace("　", " ")  # Full-width to half-width space

        # Remove honorifics
        for honorific in self.HONORIFICS:
            if name.endswith(honorific):
                name = name[: -len(honorific)]

        return name.strip()

    def calculate_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity score between two names."""
        # Levenshtein distance or other algorithm
        ...
```

**Why Service?** Name normalization is a pure algorithm that doesn't depend on any specific Speaker entity's state.

## DTO Pattern Details

### Input DTO

```python
# src/application/dto/politician_dto.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class CreatePoliticianInputDTO:
    """Input data for creating a politician."""

    name: str
    party_id: int
    furigana: Optional[str] = None
    district: Optional[str] = None

    def validate(self) -> None:
        """Validate input data."""
        if not self.name or not self.name.strip():
            raise ValueError("Name is required")
        if self.party_id <= 0:
            raise ValueError("Invalid party_id")
        if len(self.name) > 100:
            raise ValueError("Name too long (max 100 characters)")
```

### Output DTO

```python
@dataclass
class CreatePoliticianOutputDTO:
    """Output data from creating a politician."""

    success: bool
    politician_id: Optional[int] = None
    message: str = ""
    errors: list[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
```

### Why DTOs?

1. **Stability**: Domain entities can change without breaking interfaces
2. **Validation**: DTOs can have validation logic separate from entities
3. **Transformation**: Convert between different representations
4. **Security**: Don't expose internal entity structure
5. **Versioning**: Different DTO versions for API versioning

## Async/Await Pattern

All repository methods MUST be async:

```python
# ✅ CORRECT
async def find_by_id(self, id: int) -> Politician | None:
    result = await self.session.execute(
        select(PoliticianModel).where(PoliticianModel.id == id)
    )
    model = result.scalar_one_or_none()
    return self._to_entity(model) if model else None

# ❌ WRONG: Synchronous method
def find_by_id(self, id: int) -> Politician | None:
    result = self.session.execute(...)  # Missing await!
```

Use cases must also be async:

```python
# ✅ CORRECT
async def execute(self, input_dto: InputDTO) -> OutputDTO:
    entity = await self.repository.find_by_id(input_dto.id)
    # ...

# ❌ WRONG: Synchronous use case
def execute(self, input_dto: InputDTO) -> OutputDTO:
    entity = self.repository.find_by_id(input_dto.id)  # Won't work!
```

## Type Safety Guidelines

### Use Union Types

```python
# ✅ CORRECT (Python 3.10+)
def find_politician(id: int) -> Politician | None:
    ...

# ✅ CORRECT (older style)
from typing import Optional
def find_politician(id: int) -> Optional[Politician]:
    ...
```

### Explicit None Checks

```python
# ✅ CORRECT
politician = await repository.find_by_id(1)
if politician is not None:
    print(politician.name)  # Type checker knows it's not None
else:
    raise ValueError("Not found")

# ❌ WRONG
politician = await repository.find_by_id(1)
print(politician.name)  # Type error: might be None
```

### Generic Type Parameters

```python
# ✅ CORRECT
class BaseRepository(Protocol[T]):
    async def find_by_id(self, id: int) -> T | None:
        ...

class PoliticianRepository(BaseRepository[Politician]):
    pass  # Inherits correct return types
```

## Testing Strategy

### Unit Tests for Domain Services

```python
# tests/unit/domain/test_speaker_domain_service.py
def test_normalize_name_removes_honorifics():
    service = SpeakerDomainService()
    assert service.normalize_name("山田太郎氏") == "山田太郎"
```

### Unit Tests for Use Cases (with mocks)

```python
# tests/unit/application/test_create_politician_usecase.py
@pytest.mark.asyncio
async def test_execute_creates_politician(mock_repo):
    mock_repo.save.return_value = Politician(id=1, name="Test")
    usecase = CreatePoliticianUseCase(mock_repo)
    output = await usecase.execute(input_dto)
    assert output.success
```

### Integration Tests for Repositories

```python
# tests/integration/test_politician_repository.py
@pytest.mark.asyncio
async def test_find_by_id_returns_politician(db_session):
    repo = PoliticianRepositoryImpl(db_session)
    politician = await repo.find_by_id(1)
    assert politician is not None
```

## Migration Checklist

When migrating existing code to Clean Architecture:

1. [ ] Create domain entity (if doesn't exist)
2. [ ] Create repository interface in Domain
3. [ ] Create repository implementation in Infrastructure
4. [ ] Create DTOs in Application
5. [ ] Create use case in Application
6. [ ] Update interface layer (CLI/Web) to use use case
7. [ ] Write unit tests for domain services
8. [ ] Write unit tests for use cases (with mocks)
9. [ ] Write integration tests for repositories
10. [ ] Remove old direct database access code
11. [ ] Update documentation

## Common Pitfalls

### Pitfall 1: Domain Entities with Framework Dependencies

```python
# ❌ BAD: SQLAlchemy in domain
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Politician(Base):
    __tablename__ = 'politicians'
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

**Fix**: Keep entities pure, SQLAlchemy models in Infrastructure

### Pitfall 2: Use Cases Containing Business Logic

```python
# ❌ BAD: Business logic in use case
class ProcessMinutesUseCase:
    async def execute(self, input_dto):
        # Complex name normalization here
        name = input_dto.name.strip().replace("　", " ")
        for honorific in ["氏", "君"]:
            if name.endswith(honorific):
                name = name[:-len(honorific)]
        # More logic...
```

**Fix**: Move to domain service

### Pitfall 3: Repositories Returning DTOs

```python
# ❌ BAD: Repository returns DTO
class PoliticianRepositoryImpl:
    async def find_by_id(self, id: int) -> PoliticianOutputDTO:
        # Returns DTO instead of entity
```

**Fix**: Repositories return domain entities, use cases convert to DTOs

### Pitfall 4: Missing Async/Await

```python
# ❌ BAD: Forgot async/await
class UseCase:
    def execute(self, input_dto):
        result = self.repository.find_by_id(1)  # Missing await
```

**Fix**: Make everything async

## Further Reading

- [CLEAN_ARCHITECTURE_MIGRATION.md](../../../docs/CLEAN_ARCHITECTURE_MIGRATION.md) - Migration guide
- [tmp/clean_architecture_analysis_2025.md](../../../tmp/clean_architecture_analysis_2025.md) - Detailed analysis
- Robert C. Martin's "Clean Architecture" book
- Hexagonal Architecture by Alistair Cockburn
