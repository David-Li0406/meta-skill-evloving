# Port 정의 가이드

## Port/Adapter 패턴

Clean Architecture에서 gRPC 클라이언트는 **Port** (추상)와 **Adapter** (구현)로 분리.

```
Application Layer
├── ports/
│   ├── character_client.py  ← Port (ABC/Protocol)
│   └── location_client.py   ← Port (ABC/Protocol)

Infrastructure Layer
├── integrations/
│   ├── character/
│   │   ├── grpc_client.py   ← Adapter (구현)
│   │   └── proto/           ← gRPC 생성 코드
│   └── location/
│       ├── grpc_client.py   ← Adapter (구현)
│       └── proto/           ← gRPC 생성 코드
```

---

## Port 정의 원칙

### 1. 도메인 타입 사용 (Proto 타입 노출 금지)

```python
# BAD: Proto 타입 직접 노출
class CharacterClientPort(ABC):
    @abstractmethod
    async def get_character(
        self,
        request: character_pb2.GetByMatchRequest,  # Proto 타입!
    ) -> character_pb2.GetByMatchResponse:  # Proto 타입!
        ...

# GOOD: DTO로 변환
@dataclass(frozen=True)
class CharacterDTO:
    name: str
    character_type: str
    dialog: str
    match_label: str

class CharacterClientPort(ABC):
    @abstractmethod
    async def get_character_by_waste_category(
        self,
        waste_category: str,  # 도메인 타입
    ) -> CharacterDTO | None:  # DTO
        ...
```

### 2. Immutable DTO (frozen=True)

```python
@dataclass(frozen=True)
class LocationDTO:
    """위치 정보 DTO (불변)"""
    id: str
    name: str
    address: str
    latitude: float
    longitude: float
    distance_meters: float
    store_category: str | None
    pickup_category: str | None
    phone: str | None
    is_open: bool | None
```

### 3. Optional 반환 (None 허용)

```python
class CharacterClientPort(ABC):
    @abstractmethod
    async def get_character_by_waste_category(
        self,
        waste_category: str,
    ) -> CharacterDTO | None:  # 찾지 못하면 None
        ...

    @abstractmethod
    async def get_catalog(self) -> list[CharacterDTO]:  # 빈 리스트 가능
        ...
```

---

## CharacterClientPort

```python
# application/ports/character_client.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class CharacterDTO:
    """캐릭터 정보 DTO"""
    name: str
    character_type: str
    dialog: str
    match_label: str

class CharacterClientPort(ABC):
    """캐릭터 서비스 클라이언트 Port

    캐릭터 마이크로서비스와 통신하는 인터페이스.
    gRPC, HTTP, Mock 등 다양한 구현 가능.
    """

    @abstractmethod
    async def get_character_by_waste_category(
        self,
        waste_category: str,
    ) -> CharacterDTO | None:
        """폐기물 카테고리로 캐릭터 조회

        Args:
            waste_category: 폐기물 카테고리 (예: "플라스틱", "유리")

        Returns:
            매칭되는 캐릭터 또는 None
        """
        ...

    @abstractmethod
    async def get_catalog(self) -> list[CharacterDTO]:
        """전체 캐릭터 목록 조회

        Returns:
            모든 캐릭터 리스트 (빈 리스트 가능)
        """
        ...
```

---

## LocationClientPort

```python
# application/ports/location_client.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class LocationDTO:
    """위치 정보 DTO"""
    id: str
    name: str
    address: str
    latitude: float
    longitude: float
    distance_meters: float
    store_category: str | None = None
    pickup_category: str | None = None
    phone: str | None = None
    is_open: bool | None = None

class LocationClientPort(ABC):
    """위치 서비스 클라이언트 Port

    위치 기반 검색을 제공하는 마이크로서비스 인터페이스.
    """

    @abstractmethod
    async def search_recycling_centers(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int = 5000,
        limit: int = 10,
    ) -> list[LocationDTO]:
        """주변 재활용 센터 검색

        Args:
            latitude: 위도
            longitude: 경도
            radius_meters: 검색 반경 (미터)
            limit: 최대 결과 수

        Returns:
            거리순 정렬된 재활용 센터 리스트
        """
        ...

    @abstractmethod
    async def search_zerowaste_shops(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int = 5000,
        limit: int = 10,
    ) -> list[LocationDTO]:
        """주변 제로웨이스트 샵 검색

        Args:
            latitude: 위도
            longitude: 경도
            radius_meters: 검색 반경 (미터)
            limit: 최대 결과 수

        Returns:
            거리순 정렬된 제로웨이스트 샵 리스트
        """
        ...
```

---

## Generic Port 패턴 (확장용)

```python
from typing import TypeVar, Generic

T = TypeVar("T")
Q = TypeVar("Q")

class ServiceClientPort(ABC, Generic[Q, T]):
    """제네릭 서비스 클라이언트 Port"""

    @abstractmethod
    async def query(self, request: Q) -> T | None:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...

# 사용 예
class CharacterClientPort(ServiceClientPort[str, CharacterDTO]):
    async def query(self, waste_category: str) -> CharacterDTO | None:
        ...
```

---

## Port 테스트 (Mock)

```python
# tests/mocks/character_client_mock.py
class MockCharacterClient(CharacterClientPort):
    """테스트용 Mock 클라이언트"""

    def __init__(self, characters: list[CharacterDTO] | None = None):
        self._characters = characters or []
        self._call_count = 0

    async def get_character_by_waste_category(
        self,
        waste_category: str,
    ) -> CharacterDTO | None:
        self._call_count += 1
        for char in self._characters:
            if char.match_label == waste_category:
                return char
        return None

    async def get_catalog(self) -> list[CharacterDTO]:
        return self._characters

    @property
    def call_count(self) -> int:
        return self._call_count
```
