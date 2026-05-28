---
name: agent-studio-chat
description: Work on Agent Studio chat (UI + streaming) and the /api/chat route. Use for tasks like message rendering, reasoning display, editing/regenerate, Zustand chat stores, model/settings UI, and OpenRouter or Vercel AI SDK integration. 聊天功能开发/排障：流式输出、Reasoning 展示、消息编辑与重新生成、模型与参数设置。
---

# Agent Studio Chat

## Follow the data flow

- Start from `src/components/features/chat/hooks/useChatLogic.ts` (Vercel AI SDK `useChat` + `DefaultChatTransport`).
- Server route is `src/app/api/chat/route.ts` (OpenRouter provider + `streamText`).
- UI entry is `src/components/features/chat/ChatInterface.tsx` (Virtuoso list + `ChatInput`).

## Know the state layers

- Conversation persistence: `src/lib/store/useChatStore.ts`
- UI-only transient state (editing/copy): `src/lib/store/useChatUIStore.ts`
- Model + sampling + system instructions: `src/lib/store/useSettingsStore.ts` and `src/components/features/settings/SettingsPanel.tsx`

## Make safe changes

- Preserve `UIMessage.parts` when needed (reasoning parts may carry provider metadata; see `src/app/api/chat/route.ts`).
- Prefer adding new transient UI flags to `useChatUIStore` to avoid prop drilling.
- Keep feature code under `src/components/features/chat/` and reuse `src/components/ui/*` primitives.

