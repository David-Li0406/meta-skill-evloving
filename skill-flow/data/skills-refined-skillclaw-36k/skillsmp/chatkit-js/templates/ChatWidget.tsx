/**
 * ChatKit Widget Component Template
 *
 * A reusable chat widget component for the todo app chatbot.
 * Configures ChatKit with custom API backend and authentication.
 *
 * Requirements:
 *   npm install @openai/chatkit-react
 *
 * Environment:
 *   NEXT_PUBLIC_CHAT_API_URL=http://localhost:8000/api/chat
 *   NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key (optional)
 *
 * Usage:
 *   import { ChatWidget } from "@/components/ChatWidget";
 *   <ChatWidget />
 */

"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { useSession } from "@/lib/auth-client"; // Adjust import path

// ============================================================================
// Types
// ============================================================================

interface ChatWidgetProps {
  className?: string;
  userId?: string;
}

// ============================================================================
// Configuration
// ============================================================================

const CHAT_API_URL =
  process.env.NEXT_PUBLIC_CHAT_API_URL || "http://localhost:8000/api/chat";

const DOMAIN_KEY = process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY;

// ============================================================================
// ChatWidget Component
// ============================================================================

export function ChatWidget({ className = "", userId }: ChatWidgetProps) {
  const { data: session } = useSession();

  // Get auth token for API calls
  const getAuthToken = () => {
    // Adjust based on your auth setup
    return session?.session?.token || "";
  };

  const { control, error, isLoading } = useChatKit({
    // API Configuration
    api: {
      url: CHAT_API_URL,
      domainKey: DOMAIN_KEY,

      // Custom fetch to inject authentication
      fetch: async (input, init) => {
        const token = getAuthToken();
        const currentUserId = userId || session?.user?.id || "anonymous";

        return fetch(input, {
          ...init,
          headers: {
            ...init?.headers,
            ...(token && { Authorization: `Bearer ${token}` }),
            "Content-Type": "application/json",
            "X-User-ID": currentUserId,
          },
          credentials: "include",
        });
      },
    },

    // Theme Configuration
    theme: {
      colorScheme: "light",
      color: {
        accent: {
          primary: "#3b82f6", // Blue
          level: 2,
        },
      },
      radius: "soft",
      density: "normal",
      typography: {
        fontFamily: "Inter, system-ui, sans-serif",
      },
    },

    // Start Screen
    startScreen: {
      greeting: "Hi! I'm your task assistant. How can I help you today?",
      prompts: [
        {
          name: "View Tasks",
          prompt: "Show me my tasks",
          icon: "list",
        },
        {
          name: "Add Task",
          prompt: "I want to add a new task",
          icon: "plus",
        },
        {
          name: "Help",
          prompt: "What can you help me with?",
          icon: "question",
        },
      ],
    },

    // Header Configuration
    header: {
      enabled: true,
      title: {
        enabled: true,
        text: "Todo Assistant",
      },
    },

    // Composer Configuration
    composer: {
      placeholder: "Ask me to help manage your tasks...",
    },

    // History
    history: {
      enabled: true,
      showDelete: true,
      showRename: true,
    },
  });

  // Error State
  if (error) {
    return (
      <div className={`flex items-center justify-center ${className}`}>
        <div className="text-center text-red-500">
          <p>Failed to load chat</p>
          <p className="text-sm">{error.message}</p>
        </div>
      </div>
    );
  }

  // Loading State
  if (isLoading) {
    return (
      <div className={`flex items-center justify-center ${className}`}>
        <div className="animate-pulse text-gray-500">Loading chat...</div>
      </div>
    );
  }

  // Chat Widget
  return <ChatKit control={control} className={className} />;
}

// ============================================================================
// Floating Chat Widget
// ============================================================================

import { useState } from "react";

export function FloatingChatWidget() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-4 right-4 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-blue-600 text-2xl text-white shadow-lg transition-colors hover:bg-blue-700"
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? "✕" : "💬"}
      </button>

      {/* Chat Widget */}
      {isOpen && (
        <div className="fixed bottom-20 right-4 z-50 h-[500px] w-[380px] overflow-hidden rounded-lg border bg-white shadow-xl">
          <ChatWidget className="h-full w-full" />
        </div>
      )}
    </>
  );
}

// ============================================================================
// Default Export
// ============================================================================

export default ChatWidget;
