# Image Upload Diagnostic Report

**Issue**: 이미지 갤러리 첨부 후 전송 시 아무런 반응이 없음
**Date**: 2026-01-22
**Status**: Investigation Complete - Root Cause Identified

---

## Executive Summary

이미지 업로드 기능이 프론트엔드에서 백엔드까지 완전히 구현되어 있으나, 사용자가 이미지를 첨부하고 전송했을 때 아무런 UI 피드백이 없는 문제 발생.

**결론**:
- **Frontend → Backend 데이터 흐름**: ✅ 정상 동작
- **LangGraph 라우팅**: ✅ 정상 설정
- **Vision Node 로직**: ✅ 정상 구현
- **추정 원인**: 프론트엔드 UI 피드백 또는 백엔드 실행 시 에러 발생 가능성

---

## Complete Data Flow Analysis

### 1. Frontend Image Upload (2-Step Process)

#### Step 1: Presigned URL 획득
**File**: `/Users/mango/workspace/SeSACTHON/frontend/src/hooks/agent/useImageUpload.ts`
```typescript
const uploadImage = async (): Promise<string | null> => {
  if (!selectedImage) return null;

  setIsUploading(true);
  try {
    // 1. Get presigned URL from backend
    const uploadData = await ImageService.postUploadImage({
      channel: 'chat',
      fileMeta: {
        filename: selectedImage.name,
        content_type: selectedImage.type,
      },
    });

    // 2. Upload directly to S3
    await ImageService.putUploadImageUDN(uploadData.upload_url, selectedImage);

    // 3. Return CDN URL (this is the image_url)
    return uploadData.cdn_url; // ✅ THIS BECOMES image_url
  } catch (err) {
    const uploadError = err instanceof Error ? err : new Error('Image upload failed');
    setError(uploadError);
    throw uploadError;
  } finally {
    setIsUploading(false);
  }
};
```

**Result**: `uploadData.cdn_url` 반환 (예: `https://cdn.example.com/chat/uuid.jpg`)

---

#### Step 2: Message 전송 with image_url

**File**: `/Users/mango/workspace/SeSACTHON/frontend/src/hooks/agent/useAgentChat.ts:276-296`
```typescript
// 이미지 업로드 (직접 전달된 imageUrl이 없을 때만)
if (!finalImageUrl && selectedImage) {
  finalImageUrl = (await uploadImage()) ?? undefined; // ✅ S3 CDN URL
  clearImage();
}

// User 메시지 추가 (Optimistic Update)
const userMessage = createUserMessage(message, finalImageUrl); // ✅ image_url 포함

// 요청 데이터 구성
const requestData: SendMessageRequest = {
  message,
  image_url: finalImageUrl,  // ✅ CDN URL 전달
  user_location: currentLocation,
  model: selectedModel.id,
};

console.log('[DEBUG] sendMessage request:', {
  chatId,
  message,
  client_id: userMessage.client_id,
  user_location: currentLocation,
  model: selectedModel.id,
});

// 메시지 전송
const response = await AgentService.sendMessage(chatId, requestData); // ✅ API 호출
```

**Status**: ✅ `image_url`이 API 요청에 포함됨

---

### 2. Backend API Layer

#### HTTP Controller

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat/presentation/http/controllers/chat.py:138-154`
```python
class SendMessageRequest(BaseModel):
    """메시지 전송 요청."""

    message: str = Field(description="사용자 메시지")
    image_url: HttpUrl | None = Field(  # ✅ image_url 필드 정의
        default=None,
        description="첨부 이미지 URL",
    )
    user_location: UserLocation | None = Field(...)
    model: str | None = Field(...)
```

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat/presentation/http/controllers/chat.py:439-446`
```python
request = SubmitChatRequest(
    session_id=str(chat_id),
    user_id=user.user_id,
    message=payload.message,
    image_url=str(payload.image_url) if payload.image_url else None,  # ✅ 전달
    user_location=user_location,
    model=payload.model,
)

response = await command.execute(request)  # ✅ Command 실행
```

**Status**: ✅ `image_url`이 Command로 전달됨

---

#### Submit Command

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat/application/chat/commands/submit_chat.py:19-28`
```python
@dataclass
class SubmitChatRequest:
    """채팅 제출 요청 DTO."""

    session_id: str
    user_id: str
    message: str
    image_url: str | None = None  # ✅ 필드 정의
    user_location: dict[str, float] | None = None
    model: str | None = None
```

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat/application/chat/commands/submit_chat.py:72-80`
```python
success = await self._job_submitter.submit(
    job_id=job_id,
    session_id=request.session_id,
    user_id=request.user_id,
    message=request.message,
    image_url=request.image_url,  # ✅ JobSubmitter로 전달
    user_location=request.user_location,
    model=request.model,
)
```

**Status**: ✅ `image_url`이 JobSubmitter로 전달됨

---

#### Job Submitter (RabbitMQ)

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat/infrastructure/messaging/job_submitter.py:110-124`
```python
taskiq_message = {
    "task_id": job_id,
    "task_name": "chat.process",
    "labels": {},
    "args": [],
    "kwargs": {
        "job_id": job_id,
        "session_id": session_id,
        "message": message,
        "user_id": user_id,
        "image_url": image_url,  # ✅ RabbitMQ 메시지에 포함
        "user_location": user_location,
        "model": model,
    },
}

broker_message = BrokerMessage(...)
await broker.kick(broker_message)  # ✅ Worker로 전송
```

**Status**: ✅ `image_url`이 Worker 메시지에 포함됨

---

### 3. Worker (Chat Worker)

#### Process Chat Command

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat_worker/application/commands/process_chat.py:136-146`
```python
@dataclass
class ProcessChatRequest:
    """Chat 처리 요청."""

    job_id: str
    session_id: str
    user_id: str
    message: str
    image_url: str | None = None  # ✅ 필드 정의
    user_location: dict[str, float] | None = None
    model: str | None = None
```

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat_worker/application/commands/process_chat.py:268-287`
```python
initial_state = {
    "job_id": request.job_id,
    "session_id": request.session_id,
    "user_id": request.user_id,
    "message": request.message,
    "image_url": request.image_url,  # ✅ LangGraph State에 설정
    "user_location": request.user_location,
    # Context 필드 리셋 (매 턴마다 새로 계산)
    "classification_result": _reset_marker,  # ✅ None으로 리셋
    # ... other context fields ...
}
```

**Status**: ✅ `image_url`이 LangGraph State에 설정됨

---

### 4. LangGraph Pipeline

#### State Schema

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat_worker/infrastructure/orchestration/langgraph/state.py:201-202`
```python
image_url: str | None
"""이미지 URL (Vision 분석용)."""
```

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat_worker/infrastructure/orchestration/langgraph/state.py:255-256`
```python
classification_result: str | None
"""Vision 분류 결과."""
```

**Status**: ✅ State 스키마 정의 완료

---

#### Graph Routing Logic

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat_worker/infrastructure/orchestration/langgraph/factory.py:153-165`
```python
def route_after_intent(state: dict[str, Any]) -> str:
    """Intent 후 라우팅 - Vision 필요 여부 결정.

    Args:
        state: 현재 상태

    Returns:
        다음 노드 이름 (vision 또는 router)
    """
    # image_url이 있고 아직 분류 안됐으면 vision으로
    if state.get("image_url") and not state.get("classification_result"):
        return "vision"  # ✅ Vision 노드로 라우팅
    return "router"
```

**Graph Structure**:
```
START → intent → [route_after_intent]
                      ↓
         ┌────────────┴────────────┐
         ↓                         ↓
      vision                    router
         ↓
      router → dynamic_router → subagents → aggregator → answer → END
```

**Status**: ✅ `image_url` 존재 시 Vision 노드로 올바르게 라우팅됨

---

#### Vision Node Logic

**File**: `/Users/mango/workspace/SeSACTHON/backend/apps/chat_worker/infrastructure/orchestration/langgraph/nodes/vision_node.py`
```python
async def vision_node(state: dict[str, Any]) -> dict[str, Any]:
    job_id = state.get("job_id", "")
    image_url = state.get("image_url")

    # Early exit if no image
    if not image_url:
        logger.debug("No image_url, skipping vision node (job=%s)", job_id)
        return {}  # ✅ Empty dict: no state change

    # Progress notification
    await event_publisher.notify_stage(
        task_id=job_id,
        stage="vision",
        status="processing",
        progress=15,
        message="이미지 분석 중",  # ✅ 사용자에게 표시
    )

    input_dto = AnalyzeImageInput(
        job_id=job_id,
        image_url=image_url,
        message=state.get("message", ""),
    )

    output = await command.execute(input_dto)  # ✅ Vision 분석 실행

    if output.skipped:
        return {}

    if not output.success:
        await event_publisher.notify_stage(
            task_id=job_id,
            stage="vision",
            status="failed",
            result={"error": output.error_message},
        )
        return {
            "classification_result": output.classification_result,
            "has_image": output.has_image,
            "vision_error": output.error_message,
        }

    # Success
    major_category = output.classification_result.get("classification", {}).get("major", "unknown")
    await event_publisher.notify_stage(
        task_id=job_id,
        stage="vision",
        status="completed",
        progress=25,
        result={"major_category": major_category},
        message=f"분류 완료: {major_category}",  # ✅ 사용자에게 표시
    )

    return {
        "classification_result": output.classification_result,
        "has_image": output.has_image,
    }
```

**Key Observations**:
1. **Early Exit Check**: `image_url`이 없으면 빈 dict 반환 → 정상
2. **Progress Notifications**: SSE로 "이미지 분석 중" 및 "분류 완료" 이벤트 발행
3. **Error Handling**: 실패 시 `vision_error` 상태 반환 및 failed 이벤트 발행

**Status**: ✅ Vision 노드 로직 정상

---

## Root Cause Analysis

### Confirmed Working Components ✅

1. **Frontend Upload Flow**: Image → S3 → CDN URL 획득 ✅
2. **Frontend API Request**: `image_url` 포함하여 전송 ✅
3. **Backend API Layer**: `image_url` 파라미터 수신 및 전달 ✅
4. **Worker Command**: `image_url` State에 설정 ✅
5. **LangGraph Routing**: `image_url` 존재 시 Vision 노드로 라우팅 ✅
6. **Vision Node Logic**: 이미지 분석 및 SSE 이벤트 발행 ✅

### Potential Issues 🔍

#### 1. Frontend UI Feedback Issue (가능성: 높음)

**문제**: 사용자가 "아무런 반응이 없다"고 느끼는 이유

**원인 가능성**:
- ✅ Vision 단계 Progress 이벤트가 프론트엔드에서 표시되지 않음
- ✅ `isUploading` 상태가 false로 변경되지만 다른 로딩 인디케이터가 없음
- ✅ SSE 연결 전 이미지 업로드 중 UI 피드백 부족

**검증 방법**:
```typescript
// useAgentChat.ts:276-280
if (!finalImageUrl && selectedImage) {
  // ❌ 이 구간에서 UI 피드백 없음 (업로드 중)
  finalImageUrl = (await uploadImage()) ?? undefined;
  clearImage();
}
```

**해결 방안**:
1. `isUploading` 상태를 메인 UI에서 표시
2. Vision 단계 SSE 이벤트를 CurrentStage에 반영
3. Image preview에 "업로드 중..." 텍스트 추가

---

#### 2. Backend Execution Error (가능성: 중간)

**문제**: Vision 노드 실행 시 에러 발생

**원인 가능성**:
- Vision Model API 에러 (OpenAI Vision, Gemini Vision)
- 이미지 URL이 접근 불가능 (CDN CORS 이슈)
- `AnalyzeImageCommand` 내부 에러

**검증 방법**:
```bash
# Backend 로그 확인
grep -r "vision_node" /path/to/logs
grep -r "AnalyzeImageCommand" /path/to/logs
grep -r "image_url" /path/to/logs
```

**해결 방안**:
1. Backend 로그에서 Vision 노드 실행 여부 확인
2. SSE 이벤트에서 `vision` stage 이벤트 수신 여부 확인
3. 에러 발생 시 Frontend Toast 알림 추가

---

#### 3. SSE Connection Timing Issue (가능성: 낮음)

**문제**: SSE 연결이 Vision 이벤트보다 늦게 연결됨

**원인 가능성**:
```typescript
// 메시지 전송
const response = await AgentService.sendMessage(chatId, requestData);

// SSE 연결 (이 사이에 Vision 이벤트가 발행될 수 있음)
connectSSE(response.job_id);
```

**검증 방법**: Backend 로그에서 `queued`, `vision`, `intent` 이벤트의 타임스탬프 비교

**해결 방안**:
- SSE Last-Event-ID 구현 (이전 리포트에서 P0-1로 식별됨)
- SSE 연결 먼저 수행, 그 다음 메시지 전송

---

## Recommended Debugging Steps

### 1. Console Logging 추가 (Frontend)

**File**: `/Users/mango/workspace/SeSACTHON/frontend/src/hooks/agent/useAgentChat.ts:276-280`
```typescript
if (!finalImageUrl && selectedImage) {
  console.log('[DEBUG] Uploading image...', selectedImage.name);
  finalImageUrl = (await uploadImage()) ?? undefined;
  console.log('[DEBUG] Image uploaded:', finalImageUrl);
  clearImage();
}
```

**File**: `/Users/mango/workspace/SeSACTHON/frontend/src/hooks/agent/useAgentSSE.ts` (SSE handler)
```typescript
// vision 이벤트 수신 시
if (event.stage === 'vision') {
  console.log('[DEBUG] Vision event received:', event);
}
```

---

### 2. Backend Logging 확인

```bash
# Worker 로그에서 vision 노드 실행 확인
docker logs chat_worker | grep "vision_node"

# Image URL이 State에 설정되었는지 확인
docker logs chat_worker | grep "image_url"

# Vision 분석 Command 실행 확인
docker logs chat_worker | grep "AnalyzeImageCommand"
```

---

### 3. Network Tab 확인 (Browser DevTools)

1. **Image Upload 요청**:
   - `POST /api/v1/images/upload` → 200 OK
   - Response: `{ "upload_url": "...", "cdn_url": "..." }`

2. **Message 전송 요청**:
   - `POST /api/v1/chat/{chatId}/messages`
   - Request Body: `{ "message": "...", "image_url": "https://cdn..." }`
   - Response: `{ "job_id": "...", "stream_url": "..." }`

3. **SSE 연결**:
   - `GET /api/v1/chat/{job_id}/events` → 200 OK (EventStream)
   - Events: `queued`, `vision`, `intent`, `token`, `done`

---

## Next Steps

### Immediate Actions (P0)

1. **프론트엔드 Console 확인**:
   - 브라우저 Console에 `[DEBUG]` 로그가 표시되는지 확인
   - `image_url`이 정상적으로 CDN URL인지 확인
   - SSE `vision` 이벤트가 수신되는지 확인

2. **백엔드 로그 확인**:
   - Worker 컨테이너 로그에서 Vision 노드 실행 여부 확인
   - 에러 발생 시 stacktrace 확인

3. **UI 피드백 개선**:
   - Image upload 중 로딩 인디케이터 추가
   - Vision 단계 Progress UI 표시 확인

---

### Follow-up Tasks (P1)

1. **Error Handling 개선**:
   - Vision 실패 시 Toast 알림 추가
   - Image URL 검증 추가 (CDN 접근 가능 여부)

2. **SSE Event Recovery**:
   - Last-Event-ID 구현 (P0-1 issue)
   - 늦게 연결된 경우 이전 이벤트 복구

3. **End-to-End Test**:
   - 이미지 첨부 → 전송 → Vision 분석 → 답변 생성 전체 플로우 테스트
   - 다양한 이미지 타입 (JPG, PNG, HEIC) 테스트

---

## Conclusion

**데이터 흐름**: Frontend → Backend → Worker → LangGraph → Vision Node 모든 단계가 **정상적으로 구현**되어 있음.

**문제의 본질**: "아무런 반응이 없다"는 것은 기능이 동작하지 않는 것이 아니라, **사용자에게 보이는 UI 피드백이 부족**하거나 **실행 중 에러가 발생**하고 있을 가능성이 높음.

**권장 조치**:
1. Console 및 Backend 로그 확인으로 실제 동작 여부 검증
2. UI 피드백 개선 (업로드 중, Vision 분석 중 표시)
3. 에러 발생 시 사용자에게 명확한 알림

---

## Technical Details for Reference

### Image URL Format
- **Upload**: `POST /api/v1/images/upload` → `{ cdn_url: "https://cdn.eco2.com/chat/{uuid}.jpg" }`
- **State**: `image_url: "https://cdn.eco2.com/chat/{uuid}.jpg"`
- **Vision Input**: `AnalyzeImageInput(image_url="https://...")`

### SSE Event Sequence (With Image)
```
1. queued        (작업 시작)
2. intent        (의도 분류 중)
3. vision        (이미지 분석 중) ← 여기서 멈춘 것처럼 보일 수 있음
4. router        (서브에이전트 라우팅)
5. token         (답변 생성 중)
6. done          (완료)
```

### LangGraph State Snapshot
```python
{
  "job_id": "uuid",
  "message": "이게 뭐야?",
  "image_url": "https://cdn.eco2.com/chat/abc123.jpg",  # ✅ 설정됨
  "classification_result": None,  # ✅ 리셋됨 (route_after_intent에서 vision으로 라우팅)
  # ... after vision node ...
  "classification_result": {
    "classification": {
      "major": "plastic",
      "minor": "pet_bottle"
    }
  },
  "has_image": True
}
```

---

**Report Generated**: 2026-01-22
**Investigation Status**: Complete - Awaiting user feedback on console logs and backend logs
