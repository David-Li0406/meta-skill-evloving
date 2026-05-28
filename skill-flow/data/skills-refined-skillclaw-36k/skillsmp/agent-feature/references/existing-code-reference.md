# Existing Code Reference

> Camera, Location, Chat 기존 코드 참조 - Agent 구현 시 재사용

## 1. 이미지 업로드 (Camera 참조)

### 1.1 2단계 업로드 플로우

```
[1] POST /api/v1/images/{channel}
    → { upload_url (presigned), cdn_url }

[2] PUT {upload_url}
    → S3 직접 업로드

[3] cdn_url을 메시지에 포함
```

### 1.2 이미지 서비스 (재사용)

```typescript
// api/services/image/image.service.ts

export class ImageService {
  // 1. Presigned URL 획득
  static async postUploadImage({ channel, fileMeta }: ImageUpload) {
    return api.post(`/api/v1/images/${channel}`, fileMeta, {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // 2. S3 직접 업로드
  static async putUploadImageUDN(udn_url: string, imageFile: File) {
    return axios.put(udn_url, imageFile, {
      headers: { 'Content-Type': imageFile.type }
    });
  }
}
```

### 1.3 이미지 타입

```typescript
// api/services/image/image.type.ts

export type CHANNEL_TYPE = 'chat' | 'scan' | 'my';

export type ImageUpload = {
  channel: CHANNEL_TYPE;
  fileMeta: {
    filename: string;       // "image_1705123456789.png"
    content_type: string;   // "image/png"
  };
};

export type ImageUploadResponse = {
  key: string;
  upload_url: string;       // AWS S3 Presigned URL
  cdn_url: string;          // 최종 CDN URL
  expires_in: number;
};
```

### 1.4 Agent에서 이미지 업로드 사용

```typescript
// hooks/agent/useImageUpload.ts (신규)

export const useImageUpload = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);

  const uploadImage = async (): Promise<string | null> => {
    if (!selectedImage) return null;

    // 1. Presigned URL 획득
    const { data } = await ImageService.postUploadImage({
      channel: 'chat',  // Agent는 'chat' 채널 사용
      fileMeta: {
        filename: selectedImage.name,
        content_type: selectedImage.type,
      },
    });

    // 2. S3 업로드
    await ImageService.putUploadImageUDN(data.upload_url, selectedImage);

    // 3. CDN URL 반환
    return data.cdn_url;
  };

  return { selectedImage, setSelectedImage, uploadImage };
};
```

---

## 2. 위치 정보 (Map 참조)

### 2.1 useGeolocation 훅 (재사용)

```typescript
// hooks/useGeolocation.tsx

export interface Position {
  lat: number;
  lng: number;
}

export const useGeolocation = () => {
  const [userLocation, setUserLocation] = useState<Position | null>(null);
  const [permissionStatus, setPermissionStatus] = useState<
    'prompt' | 'granted' | 'denied' | 'unsupported'
  >('prompt');

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setUserLocation({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        });
        setPermissionStatus('granted');
      },
      (err) => {
        setPermissionStatus('denied');
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      }
    );
  }, []);

  return { userLocation, permissionStatus };
};
```

### 2.2 Backend 스키마 (주의: 필드명 차이!)

```typescript
// Frontend (hooks/useGeolocation.tsx)
interface Position {
  lat: number;   // ← 'lat'
  lng: number;   // ← 'lng'
}

// Backend (SendMessageRequest)
interface UserLocation {
  latitude: number;    // ← 'latitude'
  longitude: number;   // ← 'longitude'
}
```

### 2.3 Agent 요청 시 변환 필요

```typescript
// 변환 함수
const toBackendLocation = (pos: Position | null) => {
  if (!pos) return undefined;
  return {
    latitude: pos.lat,
    longitude: pos.lng,
  };
};

// 사용 예시
const { userLocation } = useGeolocation();

await api.post(`/api/v1/chat/${chatId}/messages`, {
  message: text,
  image_url: cdnUrl,
  user_location: toBackendLocation(userLocation),
});
```

---

## 3. Chat 코드 (레퍼런스 보존)

### 3.1 현재 Chat 스키마 (문제점)

**Frontend 송신:**
```typescript
// components/chat/ChatInputBar.tsx (현재)
const payload = {
  session_id: sessionId,    // ❌ Backend에서 받지 않음
  message: text,
  temperature: 0.2,         // ❌ Backend에서 받지 않음
  image_url: cdnUrl,
};
```

**Backend 기대:**
```python
# SendMessageRequest (Backend)
class SendMessageRequest(BaseModel):
    message: str                          # ✅ 필수
    image_url: HttpUrl | None = None      # ✅ 선택
    user_location: UserLocation | None    # ✅ 선택 (Frontend 누락)
    model: str | None = None              # ✅ 선택 (Frontend 누락)
```

### 3.2 응답 스키마 불일치

**Frontend 예상:**
```typescript
// ChatInputBar.tsx (현재)
if (data.session_id) {
  setSessionId(data.session_id);  // ❌ Backend가 반환 안 함
}
if (data.user_answer) {
  addMessage('assistant', data.user_answer);  // ❌ Backend가 반환 안 함
}
```

**Backend 실제 반환:**
```python
# SendMessageResponse (Backend)
class SendMessageResponse(BaseModel):
    job_id: str         # ✅ 반환
    stream_url: str     # ✅ 반환
    status: str         # ✅ 반환
```

### 3.3 Chat 페이지 보존 이유

기존 Chat 페이지는 다음 용도로 보존:
1. 즉시 응답 모드 레퍼런스
2. 메시지 UI 컴포넌트 참조
3. 마이그레이션 전 비교 대상

**파일 위치:**
```
src/pages/Chat/Chat.tsx
src/components/chat/
├── ChatInputBar.tsx
├── ChatMessageList.tsx
└── ChatEndWarningDialog.tsx
```

---

## 4. Agent 통합 스키마 (신규)

### 4.1 요청 스키마

```typescript
// Agent 메시지 전송 요청
interface AgentSendMessageRequest {
  message: string;                    // 필수
  image_url?: string;                 // 선택 (CDN URL)
  user_location?: {                   // 선택 (매 요청마다 포함)
    latitude: number;
    longitude: number;
  };
  model?: string;                     // 선택
}
```

### 4.2 응답 스키마

```typescript
// Agent 메시지 전송 응답
interface AgentSendMessageResponse {
  job_id: string;           // SSE 구독용
  stream_url: string;       // "/api/v1/chat/{job_id}/events"
  status: 'submitted' | 'queued' | 'failed';
}
```

### 4.3 SSE 이벤트

```typescript
// 핵심 이벤트
interface TokenEvent {
  content: string;          // 토큰 텍스트
  seq: number;              // 시퀀스 번호
  node: string;             // "answer"
}

interface TokenRecoveryEvent {
  accumulated: string;      // 누적 텍스트
  last_seq: number;
  completed: boolean;
}

interface DoneEvent {
  job_id: string;
  stage: 'done';
  status: 'completed' | 'failed';
  result: {
    intent: string;
    answer: string;
    persistence: {
      conversation_id: string;
      user_message: string;
      assistant_message: string;
    };
  };
}
```

---

## 5. 파일 위치 요약

### 재사용 가능 (복사/import)

| 파일 | 용도 |
|------|------|
| `api/services/image/image.service.ts` | 이미지 업로드 |
| `api/services/image/image.type.ts` | 이미지 타입 |
| `hooks/useGeolocation.tsx` | 위치 정보 |
| `types/MapTypes.ts` | Position 타입 |

### 레퍼런스용 (보존)

| 파일 | 참고 내용 |
|------|----------|
| `pages/Chat/Chat.tsx` | 메시지 상태 관리 |
| `components/chat/ChatMessageList.tsx` | 메시지 UI |
| `components/chat/ChatInputBar.tsx` | 입력 UI (스키마 주의) |
| `hooks/useScanSSE.ts` | SSE + 폴링 패턴 |

### 신규 생성 필요

| 파일 | 내용 |
|------|------|
| `api/services/agent/agent.service.ts` | Agent API |
| `api/services/agent/agent.type.ts` | Agent 타입 |
| `hooks/agent/useAgentSSE.ts` | SSE 스트리밍 |
| `hooks/agent/useAgentChat.ts` | 채팅 로직 |
| `hooks/agent/useImageUpload.ts` | 이미지 업로드 |

---

## 6. 스키마 정합성 체크리스트

```
[ ] message: string (필수)
[ ] image_url: string (선택, CDN URL)
[ ] user_location: { latitude, longitude } (선택, 매 요청)
    ⚠️ Frontend Position은 { lat, lng } → 변환 필요
[ ] model: string (선택)

응답:
[ ] job_id → SSE 구독
[ ] stream_url → EventSource URL
[ ] status → 초기 상태

SSE:
[ ] token → 실시간 스트리밍
[ ] token_recovery → 재연결 복구
[ ] done → 완료 + 최종 결과
```
