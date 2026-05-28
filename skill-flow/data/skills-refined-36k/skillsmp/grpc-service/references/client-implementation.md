# gRPC Client 구현 가이드

## Lazy Connection 패턴

첫 호출 시 채널 생성 (Cold Start 최소화).

```python
import grpc.aio
from .proto import character_pb2, character_pb2_grpc

class CharacterGrpcClient(CharacterClientPort):
    """gRPC 기반 캐릭터 클라이언트"""

    def __init__(
        self,
        host: str = "character-api",
        port: int = 50051,
    ):
        self._host = host
        self._port = port
        self._channel: grpc.aio.Channel | None = None
        self._stub: character_pb2_grpc.CharacterServiceStub | None = None

    async def _get_stub(self) -> character_pb2_grpc.CharacterServiceStub:
        """Lazy 채널/스텁 초기화"""
        if self._stub is None:
            self._channel = grpc.aio.insecure_channel(
                f"{self._host}:{self._port}"
            )
            self._stub = character_pb2_grpc.CharacterServiceStub(self._channel)
        return self._stub

    async def close(self) -> None:
        """리소스 정리"""
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stub = None
```

---

## 에러 처리

```python
import grpc.aio
import structlog

logger = structlog.get_logger()

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

        return self._to_dto(response)

    except grpc.aio.AioRpcError as e:
        logger.error(
            "gRPC call failed",
            service="character",
            method="GetCharacterByMatch",
            code=e.code().name,
            details=e.details(),
        )
        return None  # Graceful degradation

    except Exception as e:
        logger.exception("Unexpected error in gRPC client")
        return None
```

### gRPC Status Code 처리

```python
import grpc

async def call_with_retry(
    self,
    method: Callable,
    request: Any,
    max_retries: int = 3,
) -> Any:
    """재시도 로직이 포함된 gRPC 호출"""
    for attempt in range(max_retries):
        try:
            return await method(request)
        except grpc.aio.AioRpcError as e:
            # 재시도 가능한 에러
            if e.code() in (
                grpc.StatusCode.UNAVAILABLE,
                grpc.StatusCode.DEADLINE_EXCEEDED,
            ):
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
            # 재시도 불가능한 에러
            raise
```

---

## DTO 변환

```python
def _to_dto(self, response: character_pb2.GetByMatchResponse) -> CharacterDTO:
    """Proto Response → DTO 변환"""
    return CharacterDTO(
        name=response.name,
        character_type=response.character_type,
        dialog=response.dialog,
        match_label=response.match_label,
    )

def _to_dto_list(
    self,
    response: location_pb2.SearchNearbyResponse,
) -> list[LocationDTO]:
    """Proto Response → DTO 리스트 변환"""
    return [
        LocationDTO(
            id=entry.id,
            name=entry.name,
            address=entry.address,
            latitude=entry.latitude,
            longitude=entry.longitude,
            distance_meters=entry.distance_meters,
            store_category=entry.store_category or None,
            pickup_category=entry.pickup_category or None,
            phone=entry.phone or None,
            is_open=entry.is_open if entry.HasField("is_open") else None,
        )
        for entry in response.locations
    ]
```

---

## 전체 구현 예시: LocationGrpcClient

```python
# infrastructure/integrations/location/grpc_client.py
import grpc.aio
import structlog
from .proto import location_pb2, location_pb2_grpc
from apps.chat_worker.application.ports.location_client import (
    LocationClientPort,
    LocationDTO,
)

logger = structlog.get_logger()

class LocationGrpcClient(LocationClientPort):
    """gRPC 기반 위치 서비스 클라이언트"""

    def __init__(
        self,
        host: str = "location-api",
        port: int = 50051,
    ):
        self._host = host
        self._port = port
        self._channel: grpc.aio.Channel | None = None
        self._stub: location_pb2_grpc.LocationServiceStub | None = None

    async def _get_stub(self) -> location_pb2_grpc.LocationServiceStub:
        if self._stub is None:
            self._channel = grpc.aio.insecure_channel(
                f"{self._host}:{self._port}"
            )
            self._stub = location_pb2_grpc.LocationServiceStub(self._channel)
        return self._stub

    async def search_recycling_centers(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int = 5000,
        limit: int = 10,
    ) -> list[LocationDTO]:
        return await self._search(
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius_meters,
            limit=limit,
            store_category="recycling_center",
        )

    async def search_zerowaste_shops(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int = 5000,
        limit: int = 10,
    ) -> list[LocationDTO]:
        return await self._search(
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius_meters,
            limit=limit,
            store_category="zerowaste_shop",
        )

    async def _search(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int,
        limit: int,
        store_category: str,
    ) -> list[LocationDTO]:
        try:
            stub = await self._get_stub()
            request = location_pb2.SearchNearbyRequest(
                latitude=latitude,
                longitude=longitude,
                radius_meters=radius_meters,
                limit=limit,
                store_category=store_category,
            )
            response = await stub.SearchNearby(request)
            return self._to_dto_list(response)

        except grpc.aio.AioRpcError as e:
            logger.error(
                "Location gRPC error",
                code=e.code().name,
                details=e.details(),
            )
            return []

        except Exception as e:
            logger.exception("Unexpected error in LocationGrpcClient")
            return []

    def _to_dto_list(
        self,
        response: location_pb2.SearchNearbyResponse,
    ) -> list[LocationDTO]:
        return [
            LocationDTO(
                id=entry.id,
                name=entry.name,
                address=entry.address,
                latitude=entry.latitude,
                longitude=entry.longitude,
                distance_meters=entry.distance_meters,
                store_category=entry.store_category or None,
                pickup_category=entry.pickup_category or None,
                phone=entry.phone or None,
                is_open=entry.is_open if entry.HasField("is_open") else None,
            )
            for entry in response.locations
        ]

    async def close(self) -> None:
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stub = None
```

---

## Connection Pool (고성능)

```python
from grpc.aio import insecure_channel
from grpc import ChannelConnectivity

class PooledGrpcClient:
    """Connection Pool 지원 gRPC 클라이언트"""

    def __init__(
        self,
        host: str,
        port: int,
        pool_size: int = 5,
    ):
        self._target = f"{host}:{port}"
        self._pool_size = pool_size
        self._channels: list[grpc.aio.Channel] = []
        self._current = 0

    async def _get_channel(self) -> grpc.aio.Channel:
        """Round-robin 채널 선택"""
        if len(self._channels) < self._pool_size:
            channel = insecure_channel(self._target)
            self._channels.append(channel)
            return channel

        # Round-robin
        channel = self._channels[self._current]
        self._current = (self._current + 1) % self._pool_size

        # Health check
        state = channel.get_state()
        if state == ChannelConnectivity.SHUTDOWN:
            channel = insecure_channel(self._target)
            self._channels[self._current] = channel

        return channel

    async def close_all(self) -> None:
        for channel in self._channels:
            await channel.close()
        self._channels.clear()
```

---

## Timeout 설정

```python
async def call_with_timeout(
    self,
    stub: Any,
    method_name: str,
    request: Any,
    timeout: float = 5.0,
) -> Any:
    """타임아웃이 설정된 gRPC 호출"""
    method = getattr(stub, method_name)
    return await method(request, timeout=timeout)

# 사용 예
response = await self.call_with_timeout(
    stub,
    "GetCharacterByMatch",
    request,
    timeout=3.0,  # 3초 타임아웃
)
```
