import { Chat } from '@hashbrownai/core'

// This is a mock in-memory database.
// In a real application, you would use a proper database like PostgreSQL, MongoDB, or Redis.
const threadStore = new Map<string, Chat.Message[]>()

export function loadThread(threadId: string): Chat.Message[] | null {
  return threadStore.get(threadId) || null
}

export function saveThread(threadId: string, messages: Chat.Message[]): void {
  threadStore.set(threadId, messages)
}
