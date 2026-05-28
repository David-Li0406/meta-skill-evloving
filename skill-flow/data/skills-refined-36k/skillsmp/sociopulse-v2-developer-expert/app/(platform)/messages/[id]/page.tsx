'use client';

import { use } from 'react';
import { notFound } from 'next/navigation';
import { ChatWindow, MOCK_CONVERSATIONS } from '@/components/chat';

// ===========================================
// CONVERSATION PAGE
// ===========================================

interface ConversationPageProps {
    params: Promise<{ id: string }>;
}

export default function ConversationPage({ params }: ConversationPageProps) {
    const { id } = use(params);

    // Find the conversation
    const conversation = MOCK_CONVERSATIONS.find((c) => c.id === id);

    if (!conversation) {
        notFound();
    }

    return <ChatWindow conversation={conversation} />;
}
