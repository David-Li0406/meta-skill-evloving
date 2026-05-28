---
name: grpc-service
description: gRPC 서비스 통합 가이드. Port/Adapter 패턴, Proto 정의, Async Client 구현 시 참조. "grpc", "proto", "subagent", "character", "location", "rpc" 키워드로 트리거.
---

# gRPC Service Integration Guide

## Eco² gRPC 통합 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    gRPC Integration (Clean Architecture)                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Application Layer (Ports)                                               │
│  ├─ CharacterClientPort (Protocol)                                       │
│  ├─ LocationClientPort (Protocol)                                        │
│  └─ DTOs: CharacterDTO, LocationDTO                                     │
│                         │                                                │
│                         ▼                                                │
│  Infrastructure Layer (Adapters)                                         │
│  ├─ CharacterGrpcClient ──→ character-api:50051                         │
│  └─ LocationGrpcClient ──→ location-api:50051                           │
│                         │                                                │
│                         ▼                                                │
│  Proto Files (Contract)                                                  │
│  ├─ character.proto → character_pb2.py, character_pb2_grpc.py           │
│  └─ location.proto → location_pb2.py, location_pb2_grpc.py              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 왜 gRPC인가? (vs HTTP/Celery)

| Aspect | HTTP | Celery | gRPC |
|--------|------|--------|------|
| Latency | ~10ms | ~50ms+ | ~1-3ms |
| Type Safety | 런타임 | 없음 | 컴파일타임 |
| Asyncio | 제한적 | 미지원 | 네이티브 |
| Streaming | 복잡 | 미지원 | 기본 지원 |
| LangGraph 통합 | OK | await 불가 | 최적 |

## Reference Files

- **Port 정의**: See [port-definition.md](./references/port-definition.md)
- **Client 구현**: See [client-implementation.md](./references/client-implementation.md)
- **Proto 가이드**: See [proto-guide.md](./references/proto-guide.md)
- **테스트 패턴**: See [testing-patterns.md](./references/testing-patterns.md)

## Quick Start

### 1. Port 정의 (Application Layer)

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
    """캐릭터 서비스 클라이언트 Port"""

    @abstractmethod
    async def get_character_by_waste_category(
        self,
        waste_category: str,
    ) -> CharacterDTO | None:
        """폐기물 카테고리로 캐릭터 조회"""
        ...

    @abstractmethod
    async def get_catalog(self) -> list[CharacterDTO]:
        """전체 캐릭터 목록 조회"""
        ...
```

### 2. gRPC Client 구현 (Infrastructure Layer)

```python
# infrastructure/integrations/character/grpc_client.py
import grpc.aio
from .proto import character_pb2, character_pb2_grpc

class CharacterGrpcClient(CharacterClientPort):
    """gRPC 기반 캐릭터 클라이언트"""

    def __init__(self, host: str = "character-api", port: int = 50051):
        self._host = host
        self._port = port
        self._channel: grpc.aio.Channel | None = None
        self._stub: character_pb2_grpc.CharacterServiceStub | None = None

    async def _get_stub(self) -> character_pb2_grpc.CharacterServiceStub:
        """Lazy 연결 (첫 호출 시 채널 생성)"""
        if self._stub is None:
            self._channel = grpc.aio.insecure_channel(
                f"{self._host}:{self._port}"
            )
            self._stub = character_pb2_grpc.CharacterServiceStub(self._channel)
        return self._stub

    async def get_character_by_waste_category(
        self,
        waste_category: str,
    ) -> CharacterDTO | None:
        try:
            stub = await self._get_stub()
            request = character_pb2.GetByMatchRequest(
                match_label=waste_category
            )
            response = await stub.GetCharacterByMatch(request)

            if not response.found:
                return None

            return CharacterDTO(
                name=response.name,
                character_type=response.character_type,
                dialog=response.dialog,
                match_label=response.match_label,
            )
        except grpc.aio.AioRpcError as e:
            logger.error("gRPC error", code=e.code().name, details=e.details())
            return None

    async def close(self) -> None:
        """채널 종료"""
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stub = None
```

### 3. LangGraph 노드 통합

```python
# infrastructure/orchestration/langgraph/nodes/character_node.py

def create_character_node(
    character_client: CharacterClientPort,
    llm: LLMClientPort,
) -> Callable:
    """캐릭터 Subagent 노드 생성"""

    async def character_node(state: dict) -> dict:
        query = state["query"]

        # LLM으로 폐기물 카테고리 추출
        category = await extract_waste_category(llm, query)

        # gRPC 호출
        character = await character_client.get_character_by_waste_category(
            category
        )

        return {
            "character_context": character.__dict__ if character else None,
        }

    return character_node
```

### 4. 의존성 주입

```python
# setup/dependencies.py
from functools import lru_cache

@lru_cache
def get_character_client() -> CharacterClientPort:
    settings = get_settings()
    return CharacterGrpcClient(
        host=settings.character_grpc_host,
        port=settings.character_grpc_port,
    )

async def cleanup():
    """애플리케이션 종료 시 리소스 정리"""
    client = get_character_client()
    await client.close()
```
