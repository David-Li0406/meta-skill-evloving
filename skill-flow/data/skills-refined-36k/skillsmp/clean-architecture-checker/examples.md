# Clean Architecture Examples

This document provides concrete examples of good and bad code patterns in Clean Architecture.

## Table of Contents

1. [Dependency Rule Examples](#dependency-rule-examples)
2. [Entity Independence Examples](#entity-independence-examples)
3. [Repository Pattern Examples](#repository-pattern-examples)
4. [Use Case Pattern Examples](#use-case-pattern-examples)
5. [DTO Pattern Examples](#dto-pattern-examples)
6. [Type Safety Examples](#type-safety-examples)

---

## Dependency Rule Examples

### ❌ BAD: Domain Importing from Infrastructure

```python
# src/domain/entities/politician.py
from src.infrastructure.persistence.models.politician import Politician as PoliticianModel  # WRONG!

class Politician:
    def to_model(self) -> PoliticianModel:
        # Domain shouldn't know about SQLAlchemy models
        return PoliticianModel(id=self.id, name=self.name)
```

### ✅ GOOD: Domain Independent

```python
# src/domain/entities/politician.py
from dataclasses import dataclass

@dataclass
class Politician:
    """Pure domain entity with no external dependencies."""
    id: int | None
    name: str
    party_id: int
    furigana: str | None = None
    # No knowledge of SQLAlchemy or any framework
```

### ❌ BAD: Application Importing from Infrastructure

```python
# src/application/usecases/process_minutes_usecase.py
from src.infrastructure.external.gemini_llm_service import GeminiLLMService  # WRONG!

class ProcessMinutesUseCase:
    def __init__(self):
        self.llm_service = GeminiLLMService(api_key="...")  # Direct dependency
```

### ✅ GOOD: Application Using Interface

```python
# src/application/usecases/process_minutes_usecase.py
from src.domain.services.interfaces.llm_service import ILLMService

class ProcessMinutesUseCase:
    def __init__(self, llm_service: ILLMService):
        self.llm_service = llm_service  # Depends on interface, not implementation
```

---

## Entity Independence Examples

### ❌ BAD: SQLAlchemy in Domain Entity

```python
# src/domain/entities/politician.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Politician(Base):  # WRONG! Framework dependency
    __tablename__ = 'politicians'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    party_id = Column(Integer)
```

### ✅ GOOD: Pure Domain Entity

```python
# src/domain/entities/politician.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Politician:
    """Domain entity representing a politician."""
    id: int | None
    name: str
    party_id: int
    furigana: str | None = None
    district: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_name(self, new_name: str) -> None:
        """Business rule: name cannot be empty."""
        if not new_name or not new_name.strip():
            raise ValueError("Name cannot be empty")
        self.name = new_name
        self.updated_at = datetime.now()
```

### ❌ BAD: Streamlit in Domain

```python
# src/domain/services/politician_domain_service.py
import streamlit as st  # WRONG! UI framework in domain

class PoliticianDomainService:
    def display_politician(self, politician):
        st.write(f"Name: {politician.name}")  # UI logic doesn't belong here
```

### ✅ GOOD: Pure Business Logic

```python
# src/domain/services/politician_domain_service.py
class PoliticianDomainService:
    """Pure business logic for politician operations."""

    def is_duplicate(self, politician1, politician2) -> bool:
        """Check if two politicians are duplicates based on business rules."""
        return (
            politician1.name == politician2.name
            and politician1.party_id == politician2.party_id
        )

    def merge_politicians(self, primary, duplicate):
        """Merge duplicate politician records."""
        # Business logic only, no UI, no database
        ...
```

---

## Repository Pattern Examples

### ❌ BAD: Synchronous Repository

```python
# src/infrastructure/persistence/politician_repository.py
class PoliticianRepositoryImpl:
    def find_by_id(self, id: int) -> Politician:  # WRONG! Not async
        result = self.session.execute(...)  # Missing await
        return result
```

### ✅ GOOD: Async Repository with ISessionAdapter

```python
# src/infrastructure/persistence/politician_repository.py
from sqlalchemy import select
from src.domain.entities.politician import Politician
from src.domain.repositories.politician_repository import IPoliticianRepository
from src.infrastructure.persistence.base_repository import BaseRepositoryImpl
from src.infrastructure.persistence.models.politician import Politician as PoliticianModel

class PoliticianRepositoryImpl(
    BaseRepositoryImpl[Politician], IPoliticianRepository
):
    """SQLAlchemy implementation of politician repository."""

    async def find_by_id(self, id: int) -> Politician | None:
        """Find politician by ID."""
        query = select(PoliticianModel).where(PoliticianModel.id == id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_name(self, name: str) -> list[Politician]:
        """Find politicians by exact name match."""
        query = select(PoliticianModel).where(PoliticianModel.name == name)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: PoliticianModel) -> Politician:
        """Convert SQLAlchemy model to domain entity."""
        return Politician(
            id=model.id,
            name=model.name,
            party_id=model.party_id,
            furigana=model.furigana,
            district=model.district,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Politician) -> PoliticianModel:
        """Convert domain entity to SQLAlchemy model."""
        return PoliticianModel(
            id=entity.id,
            name=entity.name,
            party_id=entity.party_id,
            furigana=entity.furigana,
            district=entity.district,
        )
```

### ❌ BAD: Repository with Business Logic

```python
# src/infrastructure/persistence/politician_repository.py
class PoliticianRepositoryImpl:
    async def find_active_senior_politicians(self):  # WRONG! Business logic in repository
        politicians = await self.find_all()
        # Complex business rule here
        return [p for p in politicians if p.age > 65 and p.terms > 5]
```

### ✅ GOOD: Repository Only Does Data Access

```python
# src/infrastructure/persistence/politician_repository.py
class PoliticianRepositoryImpl:
    async def find_all(self) -> list[Politician]:
        """Find all politicians. Just data access, no business logic."""
        query = select(PoliticianModel)
        result = await self.session.execute(query)
        return [self._to_entity(m) for m in result.scalars().all()]

# src/domain/services/politician_domain_service.py
class PoliticianDomainService:
    def is_senior_politician(self, politician: Politician) -> bool:
        """Business rule for senior politicians."""
        return politician.age > 65 and politician.terms > 5

    def filter_senior(self, politicians: list[Politician]) -> list[Politician]:
        """Filter for senior politicians."""
        return [p for p in politicians if self.is_senior_politician(p)]
```

---

## Use Case Pattern Examples

### ❌ BAD: Use Case with Business Logic

```python
# src/application/usecases/match_speakers_usecase.py
class MatchSpeakersUseCase:
    async def execute(self, input_dto):
        speakers = await self.speaker_repo.find_all()
        politicians = await self.politician_repo.find_all()

        # WRONG! Complex business logic in use case
        for speaker in speakers:
            name = speaker.name.strip().replace("　", " ")
            for honorific in ["氏", "君", "議員"]:
                if name.endswith(honorific):
                    name = name[:-len(honorific)]

            for politician in politicians:
                if self._calculate_similarity(name, politician.name) > 0.8:
                    speaker.politician_id = politician.id
                    await self.speaker_repo.save(speaker)

    def _calculate_similarity(self, s1, s2):  # Business logic here
        # Levenshtein distance calculation
        ...
```

### ✅ GOOD: Use Case Orchestrates, Domain Service Has Logic

```python
# src/application/usecases/match_speakers_usecase.py
from src.domain.services.speaker_domain_service import SpeakerDomainService
from src.domain.services.speaker_matching_service import SpeakerMatchingService

class MatchSpeakersUseCase:
    """Use case orchestrates workflow, delegates business logic to services."""

    def __init__(
        self,
        speaker_repo: ISpeakerRepository,
        politician_repo: IPoliticianRepository,
        speaker_service: SpeakerDomainService,
        matching_service: SpeakerMatchingService,
    ):
        self.speaker_repo = speaker_repo
        self.politician_repo = politician_repo
        self.speaker_service = speaker_service
        self.matching_service = matching_service

    async def execute(
        self, input_dto: MatchSpeakersInputDTO
    ) -> MatchSpeakersOutputDTO:
        """
        Orchestrate speaker matching workflow.

        Business logic is delegated to domain services.
        """
        # Get data
        speakers = await self.speaker_repo.find_unmatched()
        politicians = await self.politician_repo.find_all()

        matches = []
        for speaker in speakers:
            # Delegate to domain service for normalization
            normalized_name = self.speaker_service.normalize_name(speaker.name)

            # Delegate to domain service for matching
            match = self.matching_service.find_best_match(
                normalized_name, politicians, threshold=0.8
            )

            if match:
                speaker.politician_id = match.politician_id
                await self.speaker_repo.save(speaker)
                matches.append((speaker, match))

        return MatchSpeakersOutputDTO(
            success=True,
            matched_count=len(matches),
            matches=[
                MatchResultDTO(
                    speaker_id=s.id,
                    politician_id=m.politician_id,
                    confidence=m.confidence,
                )
                for s, m in matches
            ],
        )

# src/domain/services/speaker_domain_service.py
class SpeakerDomainService:
    """Business logic for speaker operations."""

    HONORIFICS = ["氏", "君", "議員", "委員"]

    def normalize_name(self, raw_name: str) -> str:
        """Normalize speaker name (business rule)."""
        name = raw_name.strip().replace("　", " ")
        for honorific in self.HONORIFICS:
            if name.endswith(honorific):
                name = name[: -len(honorific)]
        return name.strip()

# src/domain/services/speaker_matching_service.py
class SpeakerMatchingService:
    """Business logic for speaker-politician matching."""

    def find_best_match(
        self, speaker_name: str, politicians: list[Politician], threshold: float
    ) -> MatchResult | None:
        """Find best matching politician (business rule)."""
        best_match = None
        best_score = 0.0

        for politician in politicians:
            score = self._calculate_similarity(speaker_name, politician.name)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = politician

        if best_match:
            return MatchResult(
                politician_id=best_match.id, confidence=best_score
            )
        return None

    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """Calculate similarity score."""
        # Levenshtein or other algorithm
        ...
```

### ❌ BAD: Use Case Accessing Database Directly

```python
# src/application/usecases/create_politician_usecase.py
from sqlalchemy import create_engine

class CreatePoliticianUseCase:
    def __init__(self):
        self.engine = create_engine("postgresql://...")  # WRONG!

    async def execute(self, input_dto):
        with self.engine.connect() as conn:  # Direct DB access
            conn.execute("INSERT INTO politicians ...")
```

### ✅ GOOD: Use Case Using Repository

```python
# src/application/usecases/create_politician_usecase.py
class CreatePoliticianUseCase:
    def __init__(
        self,
        politician_repo: IPoliticianRepository,
        party_repo: IPoliticalPartyRepository,
    ):
        self.politician_repo = politician_repo
        self.party_repo = party_repo

    async def execute(
        self, input_dto: CreatePoliticianInputDTO
    ) -> CreatePoliticianOutputDTO:
        # Validate
        input_dto.validate()

        # Check party exists
        party = await self.party_repo.find_by_id(input_dto.party_id)
        if not party:
            raise ValueError(f"Party {input_dto.party_id} not found")

        # Create entity
        politician = Politician(
            id=None,
            name=input_dto.name,
            party_id=input_dto.party_id,
            furigana=input_dto.furigana,
        )

        # Save via repository
        saved = await self.politician_repo.save(politician)

        return CreatePoliticianOutputDTO(
            success=True,
            politician_id=saved.id,
        )
```

---

## DTO Pattern Examples

### ❌ BAD: Exposing Domain Entity Directly

```python
# src/interfaces/cli/commands/politician_commands.py
from src.domain.entities.politician import Politician  # WRONG!

def create_politician_command(name: str, party_id: int) -> Politician:
    politician = Politician(id=None, name=name, party_id=party_id)
    # Exposing entity directly to CLI
    return politician
```

### ✅ GOOD: Using DTOs for Layer Boundaries

```python
# src/application/dto/politician_dto.py
from dataclasses import dataclass

@dataclass
class CreatePoliticianInputDTO:
    """Input DTO for creating politician."""
    name: str
    party_id: int
    furigana: str | None = None

    def validate(self) -> None:
        """Validate input data."""
        if not self.name or not self.name.strip():
            raise ValueError("Name is required")
        if self.party_id <= 0:
            raise ValueError("Invalid party_id")

@dataclass
class CreatePoliticianOutputDTO:
    """Output DTO for create politician result."""
    success: bool
    politician_id: int | None = None
    message: str = ""

# src/interfaces/cli/commands/politician_commands.py
def create_politician_command(name: str, party_id: int) -> None:
    # Create input DTO
    input_dto = CreatePoliticianInputDTO(
        name=name,
        party_id=party_id
    )

    # Execute use case
    usecase = CreatePoliticianUseCase(politician_repo, party_repo)
    output_dto = usecase.execute(input_dto)

    # Use output DTO
    if output_dto.success:
        print(f"Created politician with ID: {output_dto.politician_id}")
    else:
        print(f"Error: {output_dto.message}")
```

### ❌ BAD: DTO with Business Logic

```python
# src/application/dto/politician_dto.py
@dataclass
class PoliticianDTO:
    name: str
    party_id: int

    def normalize_name(self):  # WRONG! Business logic in DTO
        self.name = self.name.strip().replace("　", " ")
        # ...
```

### ✅ GOOD: DTO Only for Data Transfer and Validation

```python
# src/application/dto/politician_dto.py
@dataclass
class CreatePoliticianInputDTO:
    """Input DTO - only validation, no business logic."""
    name: str
    party_id: int
    furigana: str | None = None

    def validate(self) -> None:
        """Validate structure and basic constraints."""
        if not self.name:
            raise ValueError("Name is required")
        if self.party_id <= 0:
            raise ValueError("party_id must be positive")
        if self.furigana and len(self.furigana) > 200:
            raise ValueError("furigana too long")
        # Only structural validation, no complex business rules

# Business logic stays in domain service
class PoliticianDomainService:
    def normalize_name(self, name: str) -> str:
        """Business rule for name normalization."""
        return name.strip().replace("　", " ")
```

---

## Type Safety Examples

### ❌ BAD: Missing Type Hints

```python
# src/domain/repositories/politician_repository.py
class IPoliticianRepository:
    def find_by_id(self, id):  # WRONG! No type hints
        ...

    def find_all(self):  # WRONG! No return type
        ...
```

### ✅ GOOD: Complete Type Hints

```python
# src/domain/repositories/politician_repository.py
from typing import Protocol
from src.domain.entities.politician import Politician

class IPoliticianRepository(Protocol):
    async def find_by_id(self, id: int) -> Politician | None:
        """Find politician by ID. Returns None if not found."""
        ...

    async def find_all(self) -> list[Politician]:
        """Find all politicians."""
        ...

    async def save(self, politician: Politician) -> Politician:
        """Save politician and return saved entity with ID."""
        ...
```

### ❌ BAD: No None Checks

```python
# src/application/usecases/update_politician_usecase.py
async def execute(self, input_dto):
    politician = await self.repo.find_by_id(input_dto.id)
    politician.name = input_dto.new_name  # WRONG! Might be None
    await self.repo.save(politician)
```

### ✅ GOOD: Explicit None Handling

```python
# src/application/usecases/update_politician_usecase.py
async def execute(
    self, input_dto: UpdatePoliticianInputDTO
) -> UpdatePoliticianOutputDTO:
    politician = await self.repo.find_by_id(input_dto.id)

    # Explicit None check
    if politician is None:
        return UpdatePoliticianOutputDTO(
            success=False,
            message=f"Politician {input_dto.id} not found",
        )

    # Type checker knows politician is not None here
    politician.name = input_dto.new_name
    updated = await self.repo.save(politician)

    return UpdatePoliticianOutputDTO(
        success=True,
        politician_id=updated.id,
    )
```

### ❌ BAD: Generic Types Without Parameters

```python
# src/domain/repositories/base_repository.py
class BaseRepository:  # WRONG! Missing type parameter
    def find_by_id(self, id: int):  # Return type unclear
        ...
```

### ✅ GOOD: Proper Generic Types

```python
# src/domain/repositories/base_repository.py
from typing import TypeVar, Protocol

T = TypeVar("T")

class BaseRepository(Protocol[T]):
    """Base repository with generic type parameter."""

    async def find_by_id(self, id: int) -> T | None:
        """Find entity by ID."""
        ...

    async def find_all(self) -> list[T]:
        """Find all entities."""
        ...

    async def save(self, entity: T) -> T:
        """Save entity."""
        ...

# Usage
class IPoliticianRepository(BaseRepository[Politician]):
    """Politician repository with concrete type."""
    pass  # Inherits correctly typed methods
```

---

## Complete Example: End-to-End Feature

Here's a complete example showing all layers working together:

### 1. Domain Entity

```python
# src/domain/entities/speaker.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Speaker:
    """Domain entity for a speaker in meeting minutes."""
    id: int | None
    name: str
    politician_id: int | None = None
    meeting_id: int | None = None
    created_at: datetime | None = None
```

### 2. Repository Interface (Domain)

```python
# src/domain/repositories/speaker_repository.py
from typing import Protocol
from src.domain.entities.speaker import Speaker

class ISpeakerRepository(Protocol):
    async def find_unmatched(self) -> list[Speaker]:
        """Find speakers without politician link."""
        ...

    async def save(self, speaker: Speaker) -> Speaker:
        """Save speaker."""
        ...
```

### 3. Domain Service

```python
# src/domain/services/speaker_domain_service.py
class SpeakerDomainService:
    """Business logic for speakers."""

    def normalize_name(self, raw_name: str) -> str:
        """Normalize speaker name."""
        name = raw_name.strip().replace("　", " ")
        honorifics = ["氏", "君", "議員"]
        for h in honorifics:
            if name.endswith(h):
                name = name[:-len(h)]
        return name.strip()
```

### 4. Repository Implementation (Infrastructure)

```python
# src/infrastructure/persistence/speaker_repository.py
from sqlalchemy import select
from src.domain.repositories.speaker_repository import ISpeakerRepository
from src.infrastructure.persistence.base_repository import BaseRepositoryImpl

class SpeakerRepositoryImpl(BaseRepositoryImpl[Speaker], ISpeakerRepository):
    async def find_unmatched(self) -> list[Speaker]:
        query = select(SpeakerModel).where(
            SpeakerModel.politician_id.is_(None)
        )
        result = await self.session.execute(query)
        return [self._to_entity(m) for m in result.scalars().all()]
```

### 5. DTOs (Application)

```python
# src/application/dto/speaker_dto.py
from dataclasses import dataclass

@dataclass
class NormalizeSpeakerNamesInputDTO:
    """Input for normalizing speaker names."""
    meeting_id: int | None = None  # None = all meetings

@dataclass
class NormalizeSpeakerNamesOutputDTO:
    """Output from normalizing speaker names."""
    success: bool
    processed_count: int
    message: str
```

### 6. Use Case (Application)

```python
# src/application/usecases/normalize_speaker_names_usecase.py
class NormalizeSpeakerNamesUseCase:
    def __init__(
        self,
        speaker_repo: ISpeakerRepository,
        speaker_service: SpeakerDomainService,
    ):
        self.speaker_repo = speaker_repo
        self.speaker_service = speaker_service

    async def execute(
        self, input_dto: NormalizeSpeakerNamesInputDTO
    ) -> NormalizeSpeakerNamesOutputDTO:
        speakers = await self.speaker_repo.find_unmatched()

        count = 0
        for speaker in speakers:
            normalized = self.speaker_service.normalize_name(speaker.name)
            if normalized != speaker.name:
                speaker.name = normalized
                await self.speaker_repo.save(speaker)
                count += 1

        return NormalizeSpeakerNamesOutputDTO(
            success=True,
            processed_count=count,
            message=f"Normalized {count} speaker names",
        )
```

### 7. CLI Command (Interface)

```python
# src/interfaces/cli/commands/speaker_commands.py
import click
from src.application.dto.speaker_dto import NormalizeSpeakerNamesInputDTO

@click.command()
@click.option("--meeting-id", type=int, help="Specific meeting ID")
def normalize_speakers(meeting_id: int | None):
    """Normalize speaker names in meeting minutes."""
    # Create input DTO
    input_dto = NormalizeSpeakerNamesInputDTO(meeting_id=meeting_id)

    # Get use case from DI container
    usecase = get_normalize_speakers_usecase()

    # Execute
    output_dto = asyncio.run(usecase.execute(input_dto))

    # Display result
    if output_dto.success:
        click.echo(output_dto.message)
    else:
        click.echo(f"Error: {output_dto.message}", err=True)
```

This complete example shows:
- ✅ Proper layer separation
- ✅ Dependencies pointing inward
- ✅ Business logic in domain services
- ✅ Use case orchestrating workflow
- ✅ DTOs for layer boundaries
- ✅ Complete type safety
- ✅ Async/await throughout
