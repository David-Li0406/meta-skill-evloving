'use client'

import { useEffect, useEffectEvent } from 'react'

type Props = {
  roomId: string
  theme: 'light' | 'dark'
}

// useEffectEvent separates non-reactive logic from Effects
export function ChatRoom({ roomId, theme }: Props) {
  // Extract non-reactive logic into Effect Event
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme) // Reads latest theme
  })

  useEffect(() => {
    const connection = createConnection(roomId)
    connection.on('connected', onConnected)
    connection.connect()
    return () => connection.disconnect()
  }, [roomId]) // No theme dependency needed

  return <div>Chat room: {roomId}</div>
}

function showNotification(message: string, theme: string) {
  console.log(`[${theme}] ${message}`)
}

function createConnection(roomId: string) {
  return {
    on: (event: string, callback: () => void) => {},
    connect: () => {},
    disconnect: () => {},
  }
}
