# Proto 파일 가이드

## Proto 파일 구조

```
infrastructure/integrations/
├── character/
│   ├── proto/
│   │   ├── character.proto          # 원본 Proto 정의
│   │   ├── character_pb2.py         # 생성된 메시지 클래스
│   │   └── character_pb2_grpc.py    # 생성된 Stub 클래스
│   └── grpc_client.py
└── location/
    ├── proto/
    │   ├── location.proto
    │   ├── location_pb2.py
    │   └── location_pb2_grpc.py
    └── grpc_client.py
```

---

## Character Proto 예시

```protobuf
// character.proto
syntax = "proto3";

package character;

service CharacterService {
  // 폐기물 카테고리로 캐릭터 조회
  rpc GetCharacterByMatch(GetByMatchRequest) returns (GetByMatchResponse);

  // 기본 캐릭터 조회
  rpc GetDefaultCharacter(Empty) returns (GetByMatchResponse);

  // 캐릭터 리워드 요청
  rpc GetCharacterReward(RewardRequest) returns (RewardResponse);
}

message Empty {}

message GetByMatchRequest {
  string match_label = 1;  // 폐기물 카테고리 (예: "플라스틱")
}

message GetByMatchResponse {
  bool found = 1;
  string name = 2;
  string character_type = 3;
  string dialog = 4;
  string match_label = 5;
}

message ClassificationSummary {
  string major_category = 1;
  string middle_category = 2;
  string minor_category = 3;
}

message RewardRequest {
  string user_id = 1;
  string character_id = 2;
  ClassificationSummary classification = 3;
}

message RewardResponse {
  bool success = 1;
  int32 points_earned = 2;
  string message = 3;
}
```

---

## Location Proto 예시

```protobuf
// location.proto
syntax = "proto3";

package location;

service LocationService {
  // 주변 위치 검색
  rpc SearchNearby(SearchNearbyRequest) returns (SearchNearbyResponse);
}

message SearchNearbyRequest {
  double latitude = 1;
  double longitude = 2;
  int32 radius_meters = 3;
  int32 limit = 4;
  string store_category = 5;    // "recycling_center", "zerowaste_shop"
  string pickup_category = 6;   // optional 필터
}

message SearchNearbyResponse {
  repeated LocationEntry locations = 1;
}

message LocationEntry {
  string id = 1;
  string name = 2;
  string address = 3;
  double latitude = 4;
  double longitude = 5;
  double distance_meters = 6;
  string store_category = 7;
  string pickup_category = 8;
  string phone = 9;
  optional bool is_open = 10;   // 영업 상태 (optional)
}
```

---

## Proto 컴파일

### grpcio-tools 사용

```bash
# 설치
pip install grpcio-tools

# 컴파일
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./proto \
  --grpc_python_out=./proto \
  ./proto/character.proto
```

### buf 사용 (권장)

```yaml
# buf.yaml
version: v1
breaking:
  use:
    - FILE
lint:
  use:
    - DEFAULT
```

```bash
# buf 설치 후
buf generate
```

---

## 생성된 코드 사용

### character_pb2.py (메시지)

```python
# 자동 생성됨 - 수정 금지
from google.protobuf import descriptor as _descriptor

class GetByMatchRequest:
    match_label: str

class GetByMatchResponse:
    found: bool
    name: str
    character_type: str
    dialog: str
    match_label: str
```

### character_pb2_grpc.py (Stub)

```python
# 자동 생성됨 - 수정 금지
import grpc

class CharacterServiceStub:
    """클라이언트 Stub"""

    def __init__(self, channel: grpc.Channel):
        self.GetCharacterByMatch = channel.unary_unary(
            '/character.CharacterService/GetCharacterByMatch',
            request_serializer=GetByMatchRequest.SerializeToString,
            response_deserializer=GetByMatchResponse.FromString,
        )

class CharacterServiceServicer:
    """서버 Servicer (서버 구현 시 사용)"""

    def GetCharacterByMatch(self, request, context):
        raise NotImplementedError()
```

---

## RPC 패턴

### Unary-Unary (단일 요청 → 단일 응답)

```protobuf
rpc GetCharacter(GetRequest) returns (GetResponse);
```

```python
response = await stub.GetCharacter(request)
```

### Server Streaming (단일 요청 → 스트림 응답)

```protobuf
rpc ListCharacters(ListRequest) returns (stream Character);
```

```python
async for character in stub.ListCharacters(request):
    print(character.name)
```

### Client Streaming (스트림 요청 → 단일 응답)

```protobuf
rpc BatchCreate(stream CreateRequest) returns (BatchResponse);
```

```python
async def request_generator():
    for item in items:
        yield CreateRequest(data=item)

response = await stub.BatchCreate(request_generator())
```

### Bidirectional Streaming (스트림 ↔ 스트림)

```protobuf
rpc Chat(stream ChatMessage) returns (stream ChatMessage);
```

```python
async def chat():
    async for response in stub.Chat(request_generator()):
        print(response.message)
```

---

## Proto Best Practices

### 1. 필드 번호 보존

```protobuf
message User {
  string id = 1;       // 절대 변경 금지
  string name = 2;     // 절대 변경 금지
  // string email = 3; // 삭제된 필드 - 번호 재사용 금지
  string phone = 4;    // 새 필드는 새 번호 사용
}
```

### 2. Optional 활용

```protobuf
message LocationEntry {
  optional bool is_open = 10;  // 값이 없을 수 있음
}
```

```python
# Python에서 확인
if entry.HasField("is_open"):
    is_open = entry.is_open
else:
    is_open = None
```

### 3. Enum 정의

```protobuf
enum StoreCategory {
  STORE_CATEGORY_UNSPECIFIED = 0;
  STORE_CATEGORY_RECYCLING_CENTER = 1;
  STORE_CATEGORY_ZEROWASTE_SHOP = 2;
}
```

### 4. Well-Known Types

```protobuf
import "google/protobuf/timestamp.proto";
import "google/protobuf/duration.proto";

message Event {
  google.protobuf.Timestamp created_at = 1;
  google.protobuf.Duration duration = 2;
}
```
