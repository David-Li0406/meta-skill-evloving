import { useState, useEffect } from 'react'
import { Message } from '@hashbrown/core'

export interface Thread {
  id: string
  title: string
  messages: Message[]
}

export const useThreads = () => {
  const [threads, setThreads] = useState<Thread[]>([])
  const [activeThreadId, setActiveThreadId] = useState<string | null>(null)

  useEffect(() => {
    // Fetch threads from the server
    fetch('/api/threads')
      .then(res => res.json())
      .then(data => {
        setThreads(data)
        setActiveThreadId(data[0]?.id)
      })
  }, [])

  const createThread = () => {
    // Create a new thread on the server
    fetch('/api/threads', { method: 'POST' })
      .then(res => res.json())
      .then(newThread => {
        setThreads([...threads, newThread])
        setActiveThreadId(newThread.id)
      })
  }

  const switchThread = (threadId: string) => {
    setActiveThreadId(threadId)
  }

  return {
    threads,
    activeThread: threads.find(t => t.id === activeThreadId),
    createThread,
    switchThread,
  }
}
