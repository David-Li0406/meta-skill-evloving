# Agent Component Design

> Agent 페이지 컴포넌트 상세 설계 (Props, 스타일, 구현 가이드)

## 1. 레이아웃 구조

```
┌─────────────────────────────────────────────────────────────┐
│ AgentContainer                                              │
├──────────────────┬──────────────────────────────────────────┤
│                  │ AgentHeader                              │
│                  ├──────────────────────────────────────────┤
│  AgentSidebar    │                                          │
│  (260px)         │ AgentMessageList                         │
│                  │   ├─ AgentMessage                        │
│                  │   │   └─ AgentMarkdownRenderer           │
│                  │   │       └─ AgentCodeBlock / AgentImage │
│                  │   └─ AgentMessageActions                 │
│                  │                                          │
│                  │           AgentScrollToBottom (FAB)      │
│                  ├──────────────────────────────────────────┤
│                  │ AgentInputBar                            │
│                  │   ├─ AgentImageUpload                    │
│                  │   └─ AgentStopButton (스트리밍 중)        │
└──────────────────┴──────────────────────────────────────────┘
```

---

## 2. 색상 테마 (다크 모드)

```css
/* 배경 */
--agent-bg: #1a1a1a;
--agent-sidebar-bg: #1a1a1a;
--agent-header-bg: #242424;
--agent-input-bg: #2a2a2a;

/* 텍스트 */
--agent-text-primary: #ffffff;
--agent-text-secondary: #888888;
--agent-text-muted: #666666;

/* 인터랙션 */
--agent-hover: #2a2a2a;
--agent-active: #333333;
--agent-border: #444444;

/* 메시지 */
--agent-user-bubble: #333333;
--agent-assistant-bubble: transparent;

/* 코드 블록 */
--agent-code-bg: #2a2a2a;
--agent-code-header: #333333;
```

---

## 3. 핵심 컴포넌트

### 3.1 AgentContainer

```typescript
interface AgentContainerProps {
  children?: React.ReactNode;
}

export const AgentContainer = ({ children }: AgentContainerProps) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen bg-[#1a1a1a]">
      {sidebarOpen && <AgentSidebar onClose={() => setSidebarOpen(false)} />}
      <main className="flex flex-1 flex-col">
        {children}
      </main>
    </div>
  );
};
```

### 3.2 AgentSidebar

```typescript
interface AgentSidebarProps {
  onClose?: () => void;
}

export const AgentSidebar = ({ onClose }: AgentSidebarProps) => {
  const { data, fetchNextPage, hasNextPage } = useInfiniteQuery({
    queryKey: ['agent', 'chats'],
    queryFn: ({ pageParam }) => AgentService.getChatList({ cursor: pageParam }),
    getNextPageParam: (lastPage) => lastPage.next_cursor,
  });

  return (
    <aside className="flex w-[260px] flex-col border-r border-[#333] bg-[#1a1a1a]">
      <AgentSidebarHeader onNewChat={handleNewChat} />
      <AgentSidebarList
        items={data?.pages.flatMap((p) => p.chats) ?? []}
        onLoadMore={fetchNextPage}
        hasMore={hasNextPage}
      />
    </aside>
  );
};
```

### 3.3 AgentSidebarItem

```typescript
interface AgentSidebarItemProps {
  item: ChatSummary;
  isActive: boolean;
  onClick: () => void;
  onDelete?: () => void;
  onRename?: (newTitle: string) => void;
}

export const AgentSidebarItem = ({
  item,
  isActive,
  onClick,
  onDelete,
  onRename,
}: AgentSidebarItemProps) => {
  const [isEditing, setIsEditing] = useState(false);
  const [showMenu, setShowMenu] = useState(false);

  return (
    <div
      className={cn(
        'group flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2',
        isActive ? 'bg-[#333]' : 'hover:bg-[#2a2a2a]'
      )}
      onClick={onClick}
    >
      <MessageSquareIcon className="h-5 w-5 text-[#666]" />
      <span className="flex-1 truncate text-sm text-[#ccc]">
        {item.title || item.preview || '새 대화'}
      </span>
      <span className="text-xs text-[#666]">
        {formatRelativeTime(item.last_message_at)}
      </span>
    </div>
  );
};
```

### 3.4 AgentMessage

```typescript
interface AgentMessageProps {
  message: {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    created_at: string;
  };
  isStreaming?: boolean;
  onRegenerate?: () => void;
}

export const AgentMessage = ({
  message,
  isStreaming,
  onRegenerate,
}: AgentMessageProps) => {
  const isUser = message.role === 'user';

  return (
    <div className={cn('flex gap-4 py-4', isUser && 'flex-row-reverse')}>
      {/* 아바타 */}
      <div className="flex-shrink-0">
        {isUser ? (
          <UserAvatar className="h-8 w-8" />
        ) : (
          <BotAvatar className="h-8 w-8" />
        )}
      </div>

      {/* 메시지 본문 */}
      <div className={cn('flex-1', isUser && 'text-right')}>
        <div
          className={cn(
            'inline-block max-w-[80%] rounded-2xl px-4 py-3',
            isUser
              ? 'bg-[#333] text-white'
              : 'bg-transparent text-[#eee]'
          )}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <AgentMarkdownRenderer content={message.content} />
          )}
        </div>

        {/* 메시지 액션 (assistant만) */}
        {!isUser && !isStreaming && (
          <AgentMessageActions
            messageId={message.id}
            content={message.content}
            onRegenerate={onRegenerate}
          />
        )}
      </div>
    </div>
  );
};
```

### 3.5 AgentMarkdownRenderer

```typescript
interface AgentMarkdownRendererProps {
  content: string;
}

export const AgentMarkdownRenderer = ({
  content,
}: AgentMarkdownRendererProps) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeHighlight]}
      className="prose prose-invert max-w-none"
      components={{
        code({ node, inline, className, children, ...props }) {
          if (inline) {
            return (
              <code
                className="rounded bg-[#333] px-1.5 py-0.5 text-sm"
                {...props}
              >
                {children}
              </code>
            );
          }
          const match = /language-(\w+)/.exec(className || '');
          const language = match ? match[1] : '';
          return (
            <AgentCodeBlock
              code={String(children).replace(/\n$/, '')}
              language={language}
            />
          );
        },
        img({ src, alt }) {
          return <AgentImage src={src} alt={alt} />;
        },
        a({ href, children }) {
          return (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:underline"
            >
              {children}
            </a>
          );
        },
        ul({ children }) {
          return <ul className="list-disc pl-6">{children}</ul>;
        },
        ol({ children }) {
          return <ol className="list-decimal pl-6">{children}</ol>;
        },
        strong({ children }) {
          return <strong className="font-bold text-white">{children}</strong>;
        },
      }}
    >
      {content}
    </ReactMarkdown>
  );
};
```

### 3.6 AgentCodeBlock

```typescript
interface AgentCodeBlockProps {
  code: string;
  language: string;
}

export const AgentCodeBlock = ({ code, language }: AgentCodeBlockProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="my-3 overflow-hidden rounded-lg border border-[#444] bg-[#2a2a2a]">
      {/* 헤더 */}
      <div className="flex items-center justify-between bg-[#333] px-4 py-2">
        <span className="text-xs text-[#888]">
          {language || 'code'}
        </span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 text-xs text-[#888] hover:text-white"
        >
          {copied ? (
            <>
              <CheckIcon className="h-4 w-4" />
              <span>복사됨</span>
            </>
          ) : (
            <>
              <CopyIcon className="h-4 w-4" />
              <span>복사</span>
            </>
          )}
        </button>
      </div>
      {/* 코드 */}
      <pre className="overflow-x-auto p-4">
        <code className={`language-${language}`}>{code}</code>
      </pre>
    </div>
  );
};
```

### 3.7 AgentImage

```typescript
interface AgentImageProps {
  src?: string;
  alt?: string;
}

export const AgentImage = ({ src, alt }: AgentImageProps) => {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  if (!src) return null;

  if (hasError) {
    return (
      <div className="my-2 flex items-center gap-2 rounded-lg bg-[#2a2a2a] p-3 text-[#888]">
        <ImageOffIcon className="h-5 w-5" />
        <span className="text-sm">이미지를 불러올 수 없습니다</span>
      </div>
    );
  }

  return (
    <>
      <div className="my-2">
        {isLoading && (
          <div className="flex h-48 w-full items-center justify-center rounded-lg bg-[#2a2a2a]">
            <Spinner className="h-6 w-6" />
          </div>
        )}
        <img
          src={src}
          alt={alt || '이미지'}
          onLoad={() => setIsLoading(false)}
          onError={() => {
            setIsLoading(false);
            setHasError(true);
          }}
          onClick={() => setIsExpanded(true)}
          className={cn(
            'max-h-96 max-w-full cursor-zoom-in rounded-lg object-contain',
            isLoading && 'hidden'
          )}
        />
        {alt && !isLoading && (
          <p className="mt-1 text-center text-xs text-[#666]">{alt}</p>
        )}
      </div>

      {isExpanded && (
        <AgentImageModal
          src={src}
          alt={alt}
          onClose={() => setIsExpanded(false)}
        />
      )}
    </>
  );
};
```

### 3.8 AgentMessageActions

```typescript
interface AgentMessageActionsProps {
  messageId: string;
  content: string;
  onRegenerate?: () => void;
  onFeedback?: (type: 'up' | 'down') => void;
}

export const AgentMessageActions = ({
  messageId,
  content,
  onRegenerate,
  onFeedback,
}: AgentMessageActionsProps) => {
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState<'up' | 'down' | null>(null);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="mt-2 flex items-center gap-2">
      {/* 복사 */}
      <button
        onClick={handleCopy}
        className="flex items-center gap-1 rounded px-2 py-1 text-xs text-[#666] hover:bg-[#333] hover:text-white"
      >
        {copied ? <CheckIcon className="h-4 w-4" /> : <CopyIcon className="h-4 w-4" />}
      </button>

      {/* 재생성 */}
      {onRegenerate && (
        <button
          onClick={onRegenerate}
          className="flex items-center gap-1 rounded px-2 py-1 text-xs text-[#666] hover:bg-[#333] hover:text-white"
        >
          <RefreshCwIcon className="h-4 w-4" />
        </button>
      )}

      {/* 피드백 */}
      <button
        onClick={() => {
          setFeedback('up');
          onFeedback?.('up');
        }}
        className={cn(
          'rounded px-2 py-1 text-xs hover:bg-[#333]',
          feedback === 'up' ? 'text-green-500' : 'text-[#666] hover:text-white'
        )}
      >
        <ThumbsUpIcon className="h-4 w-4" />
      </button>
      <button
        onClick={() => {
          setFeedback('down');
          onFeedback?.('down');
        }}
        className={cn(
          'rounded px-2 py-1 text-xs hover:bg-[#333]',
          feedback === 'down' ? 'text-red-500' : 'text-[#666] hover:text-white'
        )}
      >
        <ThumbsDownIcon className="h-4 w-4" />
      </button>
    </div>
  );
};
```

### 3.9 AgentInputBar

```typescript
interface AgentInputBarProps {
  onSend: (message: string, imageUrl?: string) => void;
  isStreaming: boolean;
  onStop: () => void;
}

export const AgentInputBar = ({
  onSend,
  isStreaming,
  onStop,
}: AgentInputBarProps) => {
  const [input, setInput] = useState('');
  const { selectedImage, previewUrl, selectImage, uploadImage, clearImage } =
    useImageUpload();

  const handleSubmit = async () => {
    if (!input.trim() && !selectedImage) return;

    let imageUrl: string | undefined;
    if (selectedImage) {
      imageUrl = await uploadImage();
    }

    onSend(input.trim(), imageUrl);
    setInput('');
    clearImage();
  };

  return (
    <div className="border-t border-[#333] bg-[#1a1a1a] p-4">
      {/* 이미지 미리보기 */}
      {previewUrl && (
        <AgentImageUpload
          previewUrl={previewUrl}
          onRemove={clearImage}
        />
      )}

      <div className="flex items-end gap-3">
        {/* 이미지 첨부 버튼 */}
        <AgentImageUpload onImageSelect={selectImage} />

        {/* 입력창 */}
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit();
            }
          }}
          placeholder="메시지를 입력하세요..."
          className="flex-1 resize-none rounded-xl bg-[#2a2a2a] px-4 py-3 text-white placeholder-[#666] outline-none"
          rows={1}
        />

        {/* 전송 또는 중단 버튼 */}
        {isStreaming ? (
          <AgentStopButton onStop={onStop} />
        ) : (
          <button
            onClick={handleSubmit}
            disabled={!input.trim() && !selectedImage}
            className="rounded-xl bg-brand-primary px-4 py-3 text-white disabled:opacity-50"
          >
            <SendIcon className="h-5 w-5" />
          </button>
        )}
      </div>
    </div>
  );
};
```

### 3.10 AgentStopButton

```typescript
interface AgentStopButtonProps {
  onStop: () => void;
}

export const AgentStopButton = ({ onStop }: AgentStopButtonProps) => {
  return (
    <button
      onClick={onStop}
      className="flex items-center gap-2 rounded-xl border border-[#444] bg-[#2a2a2a] px-4 py-3 text-[#ccc] hover:bg-[#333]"
    >
      <StopCircleIcon className="h-4 w-4" />
      <span className="text-sm">중단</span>
    </button>
  );
};
```

### 3.11 AgentScrollToBottom

```typescript
interface AgentScrollToBottomProps {
  visible: boolean;
  onClick: () => void;
  unreadCount?: number;
}

export const AgentScrollToBottom = ({
  visible,
  onClick,
  unreadCount,
}: AgentScrollToBottomProps) => {
  if (!visible) return null;

  return (
    <button
      onClick={onClick}
      className="absolute bottom-4 right-4 z-10 flex h-10 w-10 items-center justify-center rounded-full bg-[#333] text-white shadow-lg hover:bg-[#444]"
    >
      <ChevronDownIcon className="h-5 w-5" />
      {unreadCount && unreadCount > 0 && (
        <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-blue-500 text-xs">
          {unreadCount}
        </span>
      )}
    </button>
  );
};
```

---

## 4. 훅 설계

### 4.1 useAgentSSE

```typescript
interface UseAgentSSEReturn {
  streamingText: string;
  isStreaming: boolean;
  error: Error | null;
  stopGeneration: () => void;
}

export const useAgentSSE = (jobId: string | null): UseAgentSSEReturn => {
  const [streamingText, setStreamingText] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!jobId) return;

    const url = `${import.meta.env.VITE_API_URL}/api/v1/chat/${jobId}/events`;
    const es = new EventSource(url, { withCredentials: true });
    eventSourceRef.current = es;
    setIsStreaming(true);
    setStreamingText('');
    setError(null);

    es.addEventListener('token', (e) => {
      const data = JSON.parse(e.data);
      setStreamingText((prev) => prev + data.content);
    });

    es.addEventListener('token_recovery', (e) => {
      const data = JSON.parse(e.data);
      setStreamingText(data.accumulated);
      if (data.completed) {
        es.close();
        setIsStreaming(false);
      }
    });

    es.addEventListener('done', () => {
      es.close();
      setIsStreaming(false);
    });

    es.onerror = (e) => {
      setError(new Error('SSE connection failed'));
      es.close();
      setIsStreaming(false);
    };

    return () => {
      es.close();
    };
  }, [jobId]);

  const stopGeneration = useCallback(() => {
    eventSourceRef.current?.close();
    setIsStreaming(false);
  }, []);

  return { streamingText, isStreaming, error, stopGeneration };
};
```

### 4.2 useScrollToBottom

```typescript
interface UseScrollToBottomReturn {
  containerRef: React.RefObject<HTMLDivElement>;
  showScrollButton: boolean;
  scrollToBottom: () => void;
  isAtBottom: boolean;
}

export const useScrollToBottom = (threshold = 100): UseScrollToBottomReturn => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [showScrollButton, setShowScrollButton] = useState(false);
  const [isAtBottom, setIsAtBottom] = useState(true);

  const checkScroll = useCallback(() => {
    if (!containerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
    const distanceFromBottom = scrollHeight - scrollTop - clientHeight;
    setShowScrollButton(distanceFromBottom > threshold);
    setIsAtBottom(distanceFromBottom <= threshold);
  }, [threshold]);

  const scrollToBottom = useCallback(() => {
    containerRef.current?.scrollTo({
      top: containerRef.current.scrollHeight,
      behavior: 'smooth',
    });
  }, []);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    container.addEventListener('scroll', checkScroll);
    return () => container.removeEventListener('scroll', checkScroll);
  }, [checkScroll]);

  return { containerRef, showScrollButton, scrollToBottom, isAtBottom };
};
```

---

## 5. API 서비스 레이어

```typescript
// api/services/agent/agent.service.ts

export class AgentService {
  static async getChatList(params?: { limit?: number; cursor?: string }) {
    const response = await api.get<ChatListResponse>('/api/v1/chat', { params });
    return response.data;
  }

  static async createChat(title?: string) {
    const response = await api.post<ChatSummary>('/api/v1/chat', { title });
    return response.data;
  }

  static async deleteChat(chatId: string) {
    await api.delete(`/api/v1/chat/${chatId}`);
  }

  static async updateChatTitle(chatId: string, title: string) {
    const response = await api.patch(`/api/v1/chat/${chatId}`, { title });
    return response.data;
  }

  static async sendMessage(chatId: string, message: string, imageUrl?: string) {
    const response = await api.post<SendMessageResponse>(
      `/api/v1/chat/${chatId}/messages`,
      { message, image_url: imageUrl }
    );
    return response.data;
  }
}
```

---

## 6. 타입 정의

```typescript
// types/AgentTypes.ts

export interface ChatSummary {
  id: string;
  title: string | null;
  preview: string | null;
  message_count: number;
  last_message_at: string | null;
  created_at: string;
}

export interface ChatListResponse {
  chats: ChatSummary[];
  next_cursor: string | null;
}

export interface SendMessageResponse {
  job_id: string;
  stream_url: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
}

export interface AgentMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  image_url?: string;
}

export interface TokenEvent {
  content: string;
  seq: number;
  node: string;
}

export interface TokenRecoveryEvent {
  stage: 'token_recovery';
  status: 'snapshot';
  accumulated: string;
  last_seq: number;
  completed: boolean;
}

export interface DoneEvent {
  job_id: string;
  stage: 'done';
  status: 'completed' | 'failed';
  result: {
    intent: string;
    answer: string;
    persistence: {
      conversation_id: string;
      user_id: string;
      user_message: string;
      assistant_message: string;
    };
  };
}
```
