'use client';

import { ReactNode } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronLeft, Bell } from 'lucide-react';
import { ConversationList, MOCK_CONVERSATIONS } from '@/components/chat';

// ===========================================
// LAYOUT COMPONENT
// ===========================================

export default function MessagesLayout({ children }: { children: ReactNode }) {
    const pathname = usePathname();
    const isInConversation = pathname !== '/messages';

    return (
        <div className="h-[calc(100vh-64px)] flex flex-col bg-slate-50">
            {/* Header */}
            <header className="flex-shrink-0 sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-slate-100">
                <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-14">
                        {/* Back Button + Title */}
                        <div className="flex items-center gap-3">
                            <Link
                                href="/"
                                className="p-2 -ml-2 rounded-xl hover:bg-slate-100 transition-colors"
                                aria-label="Retour à l'accueil"
                            >
                                <ChevronLeft className="w-5 h-5 text-slate-600" />
                            </Link>
                            <h1 className="text-xl font-bold text-slate-900">
                                Messages
                            </h1>
                        </div>

                        {/* Notifications */}
                        <button
                            aria-label="Notifications"
                            className="relative p-2 rounded-xl hover:bg-slate-100 transition-colors"
                        >
                            <Bell className="w-5 h-5 text-slate-600" />
                        </button>
                    </div>
                </div>
            </header>

            {/* Main Content - Full Height */}
            <div className="flex-1 flex overflow-hidden">
                {/* Desktop: Split View */}
                <div className="hidden lg:flex w-full max-w-6xl mx-auto">
                    {/* Sidebar: Conversation List */}
                    <aside className="w-80 flex-shrink-0 border-r border-slate-100 bg-white overflow-hidden">
                        <ConversationList conversations={MOCK_CONVERSATIONS} />
                    </aside>

                    {/* Main: Chat Window */}
                    <main className="flex-1 flex flex-col min-w-0 bg-white">
                        {children}
                    </main>
                </div>

                {/* Mobile: Single View */}
                <div className="lg:hidden w-full overflow-hidden">
                    {isInConversation ? (
                        // Show Chat Window
                        <main className="h-full flex flex-col bg-white">
                            {children}
                        </main>
                    ) : (
                        // Show Conversation List
                        <div className="h-full bg-white">
                            <ConversationList conversations={MOCK_CONVERSATIONS} />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
