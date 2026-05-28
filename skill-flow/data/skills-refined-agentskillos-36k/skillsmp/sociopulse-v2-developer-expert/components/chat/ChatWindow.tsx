'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
    ChevronLeft,
    Phone,
    Video,
    MoreVertical,
} from 'lucide-react';
import { MessageBubble } from './MessageBubble';
import { MessageInput } from './MessageInput';
import {
    MOCK_CURRENT_USER,
    MOCK_MESSAGES,
    getOtherParticipant,
    type Conversation,
    type Message,
} from './mockData';

// ===========================================
// TYPES
// ===========================================

export interface ChatWindowProps {
    conversation: Conversation;
    onBack?: () => void;
}

// ===========================================
// COMPONENT
// ===========================================

export function ChatWindow({ conversation, onBack }: ChatWindowProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [messages, setMessages] = useState<Message[]>(
        MOCK_MESSAGES[conversation.id] || []
    );

    const otherUser = getOtherParticipant(conversation, MOCK_CURRENT_USER.id);

    // Auto-scroll to bottom on new messages
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Handle sending a message
    const handleSend = async (content: string) => {
        const newMessage: Message = {
            id: `msg-${Date.now()}`,
            conversationId: conversation.id,
            senderId: MOCK_CURRENT_USER.id,
            content,
            timestamp: new Date(),
            isRead: false,
            type: 'text',
        };

        setMessages((prev) => [...prev, newMessage]);

        // Simulate "read" after 1 second
        setTimeout(() => {
            setMessages((prev) =>
                prev.map((msg) =>
                    msg.id === newMessage.id ? { ...msg, isRead: true } : msg
                )
            );
        }, 1000);
    };

    return (
        <div className="h-full flex flex-col bg-white">
            {/* Header */}
            <header className="flex-shrink-0 border-b border-slate-100 bg-white z-10">
                <div className="flex items-center gap-3 px-4 py-3">
                    {/* Back Button (Mobile) */}
                    <Link
                        href="/messages"
                        className="lg:hidden p-2 -ml-2 rounded-xl hover:bg-slate-100 transition-colors"
                        aria-label="Retour"
                    >
                        <ChevronLeft className="w-5 h-5 text-slate-600" />
                    </Link>

                    {/* Avatar */}
                    <div className="relative flex-shrink-0">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center overflow-hidden">
                            {otherUser.avatar ? (
                                <img
                                    src={otherUser.avatar}
                                    alt={otherUser.name || ''}
                                    className="w-full h-full object-cover"
                                />
                            ) : (
                                <span className="text-sm font-semibold text-brand-600">
                                    {(otherUser.name || '?').charAt(0)}
                                </span>
                            )}
                        </div>
                        {otherUser.isOnline && (
                            <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white" />
                        )}
                    </div>

                    {/* User Info */}
                    <div className="flex-1 min-w-0">
                        <h2 className="font-semibold text-slate-900 truncate">
                            {otherUser.name}
                        </h2>
                        <p className="text-xs text-slate-500">
                            {otherUser.isOnline ? 'En ligne' : 'Hors ligne'}
                        </p>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex items-center gap-1">
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="p-2.5 rounded-xl text-slate-500 hover:text-brand-600 hover:bg-brand-50 transition-colors"
                            aria-label="Appel vidéo"
                        >
                            <Video className="w-5 h-5" />
                        </motion.button>
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="p-2.5 rounded-xl text-slate-500 hover:text-brand-600 hover:bg-brand-50 transition-colors"
                            aria-label="Appel téléphonique"
                        >
                            <Phone className="w-5 h-5" />
                        </motion.button>
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="p-2.5 rounded-xl text-slate-500 hover:text-slate-700 hover:bg-slate-100 transition-colors"
                            aria-label="Plus d'options"
                        >
                            <MoreVertical className="w-5 h-5" />
                        </motion.button>
                    </div>
                </div>

                {/* Context Banner */}
                {conversation.bookingContext && (
                    <div className="px-4 py-2 bg-slate-50 border-t border-slate-100 flex items-center gap-2">
                        <div className="w-1 h-8 bg-brand-600 rounded-full" />
                        <div className="flex-1 min-w-0">
                            <p className="text-xs font-medium text-slate-500 uppercase tracking-wide">
                                Concernant
                            </p>
                            <p className="text-sm font-semibold text-slate-900 truncate">
                                {conversation.bookingContext.title} • {conversation.bookingContext.date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })}
                            </p>
                        </div>
                        <Link
                            href={`/bookings`} // In real app, link to specific booking ID
                            className="text-xs font-semibold text-brand-600 hover:underline"
                        >
                            Voir détails
                        </Link>
                    </div>
                )}
            </header>

            {/* Messages List */}
            <div className="flex-1 overflow-y-auto p-4 space-y-1 bg-slate-50/50">
                {messages.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-center">
                        <div className="w-16 h-16 rounded-full bg-slate-100 flex items-center justify-center mb-4">
                            <span className="text-2xl">👋</span>
                        </div>
                        <h3 className="text-lg font-semibold text-slate-900 mb-2">
                            Démarrez la conversation
                        </h3>
                        <p className="text-sm text-slate-500">
                            Envoyez un message à {otherUser.name}
                        </p>
                    </div>
                ) : (
                    <>
                        {messages.map((message) => (
                            <MessageBubble
                                key={message.id}
                                message={message}
                                isOwn={message.senderId === MOCK_CURRENT_USER.id}
                            />
                        ))}
                        <div ref={messagesEndRef} />
                    </>
                )}
            </div>

            {/* Input Zone */}
            <MessageInput
                onSend={handleSend}
                onAttachment={() => alert('Attachments coming soon!')}
            />
        </div>
    );
}
