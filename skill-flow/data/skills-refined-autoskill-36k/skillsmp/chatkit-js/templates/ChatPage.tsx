/**
 * Chat Page Template
 *
 * A full-page chat layout with sidebar for conversation history.
 * Uses ChatKit for the main chat interface.
 *
 * Requirements:
 *   npm install @openai/chatkit-react
 *
 * Usage:
 *   // app/chat/page.tsx
 *   import ChatPage from "@/components/ChatPage";
 *   export default function Chat() { return <ChatPage />; }
 */

"use client";

import { useState, useEffect } from "react";
import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { useSession } from "@/lib/auth-client"; // Adjust import path
import { useRouter } from "next/navigation";

// ============================================================================
// Types
// ============================================================================

interface Conversation {
  id: string;
  title: string;
  updatedAt: string;
}

// ============================================================================
// Configuration
// ============================================================================

const CHAT_API_URL =
  process.env.NEXT_PUBLIC_CHAT_API_URL || "http://localhost:8000/api/chat";

const DOMAIN_KEY = process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY;

// ============================================================================
// Chat Page Component
// ============================================================================

export default function ChatPage() {
  const { data: session, isPending } = useSession();
  const router = useRouter();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentThread, setCurrentThread] = useState<string | null>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (!isPending && !session) {
      router.push("/sign-in");
    }
  }, [session, isPending, router]);

  // Load conversations
  useEffect(() => {
    async function loadConversations() {
      if (!session) return;

      try {
        const res = await fetch("/api/conversations", {
          headers: {
            Authorization: `Bearer ${session.session?.token}`,
          },
        });
        if (res.ok) {
          const data = await res.json();
          setConversations(data.conversations || []);
        }
      } catch (error) {
        console.error("Failed to load conversations:", error);
      }
    }

    loadConversations();
  }, [session]);

  // Get auth token
  const getAuthToken = () => session?.session?.token || "";
  const getUserId = () => session?.user?.id || "anonymous";

  // ChatKit configuration
  const { control, error, isLoading } = useChatKit({
    api: {
      url: CHAT_API_URL,
      domainKey: DOMAIN_KEY,

      fetch: async (input, init) => {
        const token = getAuthToken();
        const userId = getUserId();

        // Add thread_id to request body if we have a current thread
        let body = init?.body;
        if (body && currentThread) {
          try {
            const parsed = JSON.parse(body as string);
            parsed.thread_id = currentThread;
            parsed.user_id = userId;
            body = JSON.stringify(parsed);
          } catch {
            // Keep original body
          }
        }

        return fetch(input, {
          ...init,
          body,
          headers: {
            ...init?.headers,
            ...(token && { Authorization: `Bearer ${token}` }),
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
      },
    },

    theme: {
      colorScheme: "light",
      color: {
        accent: { primary: "#3b82f6", level: 2 },
      },
      radius: "soft",
      density: "normal",
    },

    startScreen: {
      greeting: session?.user?.name
        ? `Hi ${session.user.name}! How can I help you with your tasks today?`
        : "Hi! How can I help you with your tasks today?",
      prompts: [
        { name: "View Tasks", prompt: "Show me my pending tasks", icon: "list" },
        { name: "Add Task", prompt: "Help me add a new task", icon: "plus" },
        { name: "Today's Tasks", prompt: "What should I focus on today?", icon: "calendar" },
      ],
    },

    header: {
      enabled: true,
      title: { enabled: true, text: "Todo Assistant" },
      leftAction: {
        icon: sidebarOpen ? "sidebar-open-left" : "sidebar-left",
        onClick: () => setSidebarOpen(!sidebarOpen),
      },
    },

    composer: {
      placeholder: "Ask me to manage your tasks...",
    },

    history: {
      enabled: true,
      showDelete: true,
      showRename: true,
    },
  });

  // Handle new conversation
  const handleNewConversation = () => {
    setCurrentThread(null);
    // ChatKit will create a new thread automatically
  };

  // Handle selecting a conversation
  const handleSelectConversation = (threadId: string) => {
    setCurrentThread(threadId);
  };

  // Loading state
  if (isPending) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="animate-pulse text-gray-500">Loading...</div>
      </div>
    );
  }

  // Not authenticated
  if (!session) {
    return null; // Will redirect
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      {sidebarOpen && (
        <aside className="w-64 border-r bg-white">
          <div className="flex h-full flex-col">
            {/* New Chat Button */}
            <div className="border-b p-4">
              <button
                onClick={handleNewConversation}
                className="w-full rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
              >
                + New Chat
              </button>
            </div>

            {/* Conversations List */}
            <div className="flex-1 overflow-y-auto p-2">
              <h3 className="mb-2 px-2 text-xs font-semibold uppercase text-gray-500">
                Recent Chats
              </h3>
              {conversations.length === 0 ? (
                <p className="px-2 text-sm text-gray-400">No conversations yet</p>
              ) : (
                <ul className="space-y-1">
                  {conversations.map((conv) => (
                    <li key={conv.id}>
                      <button
                        onClick={() => handleSelectConversation(conv.id)}
                        className={`w-full truncate rounded-lg px-3 py-2 text-left text-sm hover:bg-gray-100 ${
                          currentThread === conv.id
                            ? "bg-blue-50 text-blue-600"
                            : "text-gray-700"
                        }`}
                      >
                        {conv.title || "Untitled conversation"}
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/* User Info */}
            <div className="border-t p-4">
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
                  <span className="text-sm font-medium text-blue-600">
                    {session.user?.name?.[0] || "U"}
                  </span>
                </div>
                <div className="flex-1 truncate">
                  <p className="text-sm font-medium">{session.user?.name}</p>
                  <p className="truncate text-xs text-gray-500">
                    {session.user?.email}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </aside>
      )}

      {/* Main Chat Area */}
      <main className="flex-1">
        {error ? (
          <div className="flex h-full items-center justify-center">
            <div className="text-center text-red-500">
              <p className="text-lg font-semibold">Failed to load chat</p>
              <p className="text-sm">{error.message}</p>
            </div>
          </div>
        ) : isLoading ? (
          <div className="flex h-full items-center justify-center">
            <div className="animate-pulse text-gray-500">Loading chat...</div>
          </div>
        ) : (
          <ChatKit control={control} className="h-full w-full" />
        )}
      </main>
    </div>
  );
}
