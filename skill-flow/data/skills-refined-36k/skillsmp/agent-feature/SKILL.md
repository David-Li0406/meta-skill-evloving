---
name: agent-feature
description: Agent 페이지 구현 스킬. SSE 토큰 스트리밍, 사이드바, 마크다운 렌더링, 메시지 액션을 포함한 AI 챗봇 인터페이스 구현 시 사용. React 19 + TypeScript + TailwindCSS 기반.
---

# Agent Feature Implementation Skill

> 폐기물 분리배출 AI 코칭 서비스 "이코에코"의 Agent 페이지 구현 가이드

## 1. 개요

Agent 페이지는 기존 Chat과 분리된 새로운 AI 대화 인터페이스입니다.
주요 특징:
- SSE 기반 실시간 토큰 스트리밍
- Claude Code 스타일 사이드바
- 마크다운 + 코드 블록 렌더링
- 메시지 액션 (복사, 재생성, 피드백)

## 2. 구현 우선순위

### P0 (필수)
| 컴포넌트 | 설명 |
|---------|------|
| `AgentContainer` | 메인 레이아웃 |
| `AgentSidebar` | 대화 목록 사이드바 |
| `AgentMessageList` | 메시지 영역 |
| `AgentInputBar` | 입력창 + 전송 |
| `useAgentSSE` | SSE 토큰 스트리밍 훅 |
| `AgentMarkdownRenderer` | MD 렌더링 |
| `AgentCodeBlock` | 코드 블록 + 복사 |
| `AgentMessageActions` | 복사/재생성/피드백 |
| `AgentStopButton` | 생성 중단 |

### P1 (권장)
| 컴포넌트 | 설명 |
|---------|------|
| `AgentImageUpload` | 이미지 첨부 |
| `AgentScrollToBottom` | 하단 이동 FAB |
| `AgentImage` | MD 이미지 렌더링 |

### P2 (선택)
| 컴포넌트 | 설명 |
|---------|------|
| `AgentSidebarItem` | 제목 수정 기능 확장 |

## 3. 의사결정 트리

```
Agent 기능 구현 시작
    │
    ├─ SSE 스트리밍 구현?
    │   └─ references/api-spec.md 참조
    │
    ├─ 컴포넌트 설계 필요?
    │   └─ references/component-design.md 참조
    │
    ├─ 프론트엔드 컨벤션 확인?
    │   └─ references/frontend-stack.md 참조
    │
    ├─ 이미지 업로드 구현?
    │   └─ references/existing-code-reference.md §1 참조
    │   └─ 기존 image.service.ts 재사용
    │
    ├─ 위치 정보 포함?
    │   └─ references/existing-code-reference.md §2 참조
    │   └─ 기존 useGeolocation.tsx 재사용
    │   └─ ⚠️ { lat, lng } → { latitude, longitude } 변환 필수
    │
    ├─ 기존 Chat 코드 참조?
    │   └─ references/existing-code-reference.md §3 참조
    │   └─ Chat 페이지는 레퍼런스로 보존 (스키마 불일치 주의)
    │
    └─ 마크다운 렌더링?
        └─ react-markdown + remark-gfm + rehype-highlight 사용
```

## 4. 핵심 구현 패턴

### 4.1 SSE 토큰 스트리밍

```typescript
// hooks/agent/useAgentSSE.ts
const useAgentSSE = (jobId: string | null) => {
  const [streamingText, setStreamingText] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!jobId) return;

    const url = `${import.meta.env.VITE_API_URL}/api/v1/chat/${jobId}/events`;
    const es = new EventSource(url, { withCredentials: true });
    eventSourceRef.current = es;

    es.addEventListener('token', (e) => {
      const data = JSON.parse(e.data);
      setStreamingText((prev) => prev + data.content);
    });

    es.addEventListener('done', () => {
      es.close();
      setIsStreaming(false);
    });

    setIsStreaming(true);
    return () => es.close();
  }, [jobId]);

  const stopGeneration = useCallback(() => {
    eventSourceRef.current?.close();
    setIsStreaming(false);
  }, []);

  return { streamingText, isStreaming, stopGeneration };
};
```

### 4.2 마크다운 렌더링

```typescript
// components/agent/AgentMarkdownRenderer.tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';

const AgentMarkdownRenderer = ({ content }: { content: string }) => (
  <ReactMarkdown
    remarkPlugins={[remarkGfm]}
    rehypePlugins={[rehypeHighlight]}
    components={{
      code: ({ inline, className, children }) => {
        if (inline) return <code className="...">{children}</code>;
        const lang = className?.replace('language-', '') || '';
        return <AgentCodeBlock code={String(children)} language={lang} />;
      },
      img: ({ src, alt }) => <AgentImage src={src} alt={alt} />,
    }}
  >
    {content}
  </ReactMarkdown>
);
```

### 4.3 메시지 액션

```typescript
// 클립보드 복사
const handleCopy = async (text: string) => {
  await navigator.clipboard.writeText(text);
};

// 재생성
const handleRegenerate = async (messageId: string) => {
  // 이전 assistant 메시지 삭제 후 동일 질문 재전송
};
```

## 5. 디렉토리 구조

```
src/
├── pages/
│   └── Agent/
│       ├── Agent.tsx           # 메인 페이지
│       └── index.ts
│
├── components/
│   └── agent/
│       ├── index.ts
│       ├── AgentContainer.tsx
│       ├── AgentHeader.tsx
│       ├── AgentMessageList.tsx
│       ├── AgentMessage.tsx
│       ├── AgentMessageActions.tsx
│       ├── AgentStopButton.tsx
│       ├── AgentMarkdownRenderer.tsx
│       ├── AgentCodeBlock.tsx
│       ├── AgentImage.tsx
│       ├── AgentImageModal.tsx
│       ├── AgentScrollToBottom.tsx
│       ├── AgentImageUpload.tsx
│       ├── AgentInputBar.tsx
│       ├── AgentThinkingUI.tsx
│       ├── ModelSelector.tsx
│       └── sidebar/
│           ├── AgentSidebar.tsx
│           ├── AgentSidebarHeader.tsx
│           ├── AgentSidebarList.tsx
│           ├── AgentSidebarItem.tsx
│           └── AgentSidebarEmpty.tsx
│
├── hooks/
│   └── agent/
│       ├── useAgentSSE.ts
│       ├── useAgentChat.ts
│       ├── useAgentSidebar.ts
│       ├── useImageUpload.ts
│       └── useScrollToBottom.ts
│
├── api/
│   └── services/
│       └── agent/
│           ├── agent.service.ts
│           ├── agent.type.ts
│           ├── agent.queries.ts
│           └── agent.mutation.ts
│
└── types/
    └── AgentTypes.ts
```

## 6. 의존성

```bash
# 필수
yarn add react-markdown remark-gfm rehype-highlight

# highlight.js 테마 (global.css에서 import)
@import 'highlight.js/styles/github-dark.css';
```

## 7. 참조 문서

상세 정보는 `references/` 디렉토리 참조:

| 파일 | 내용 |
|------|------|
| `frontend-stack.md` | 프론트엔드 기술 스택, 컨벤션, Git 규칙, 배포 |
| `api-spec.md` | Agent API 엔드포인트, SSE 이벤트 형식 |
| `component-design.md` | 컴포넌트 상세 설계 (Props, 스타일) |
| `existing-code-reference.md` | Camera/Location/Chat 기존 코드 참조 |

### 재사용 파일

| 파일 | 용도 |
|------|------|
| `api/services/image/image.service.ts` | 이미지 업로드 (Presigned URL) |
| `hooks/useGeolocation.tsx` | 위치 정보 (Geolocation API) |
| `types/MapTypes.ts` | Position 타입 정의 |

### 레퍼런스 보존 (수정 금지)

| 파일 | 참조 용도 |
|------|----------|
| `pages/Chat/Chat.tsx` | 메시지 상태 관리 |
| `components/chat/*` | 메시지 UI 패턴 |
| `hooks/useScanSSE.ts` | SSE + 폴링 패턴 |

## 8. 체크리스트

구현 시 아래 순서대로 진행:

```
[ ] 1. API 서비스 레이어 (agent.service.ts, agent.type.ts)
[ ] 2. SSE 훅 (useAgentSSE.ts)
[ ] 3. 위치 정보 훅 (useGeolocation 재사용 + 변환 함수)
[ ] 4. 이미지 업로드 훅 (image.service.ts 재사용)
[ ] 5. 사이드바 컴포넌트
[ ] 6. 메시지 리스트 + 마크다운 렌더링
[ ] 7. 입력창 + 전송 (이미지/위치 통합)
[ ] 8. 메시지 액션 (복사, 재생성)
[ ] 9. 생성 중단 버튼
[ ] 10. 이미지 첨부 UI (P1)
[ ] 11. 스크롤 하단 FAB (P1)
[ ] 12. 제목 수정 (P2)
```

## 9. 주의사항

1. **SSE 연결 관리**: 컴포넌트 언마운트 시 반드시 `EventSource.close()` 호출
2. **토큰 복구**: 늦은 구독 시 `token_recovery` 이벤트로 누락 토큰 복구
3. **UTF-8 처리**: 한글 토큰이 분리될 수 있으므로 `TextDecoder` 사용 권장
4. **쿠키 인증**: `withCredentials: true` 필수 (s_access 쿠키)
5. **Axios 인터셉터**: 기존 axiosInstance.ts 활용 (401/403 자동 처리)
6. **위치 스키마 변환**: Frontend `{ lat, lng }` → Backend `{ latitude, longitude }`
7. **기존 Chat 스키마 불일치**: Chat 페이지는 Backend와 호환 안 됨 (레퍼런스로만 사용)
8. **이미지 업로드**: 2단계 (Presigned URL 획득 → S3 PUT)
