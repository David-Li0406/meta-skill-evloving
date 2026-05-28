'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import {
    formatMessageTime,
    getOtherParticipant,
    MOCK_CURRENT_USER,
    type Conversation,
} from './mockData';

// ===========================================
// TYPES
// ===========================================

export interface ConversationListProps {
    conversations: Conversation[];
    onSelectConversation?: (conversationId: string) => void;
}

// ===========================================
// COMPONENT
// ===========================================

export function ConversationList({
    conversations,
    onSelectConversation,
}: ConversationListProps) {
    const params = useParams();
    const activeId = params?.id as string | undefined;
    const [searchTerm, setSearchTerm] = useState('');

    const filteredConversations = conversations.filter(c => {
        const otherUser = getOtherParticipant(c, MOCK_CURRENT_USER.id);
        return otherUser.name.toLowerCase().includes(searchTerm.toLowerCase());
    });

    return (
        <div className="h-full flex flex-col">
            {/* Header with Search */}
            <div className="flex-shrink-0 p-4 border-b border-slate-100 space-y-3">
                <h2 className="text-xl font-bold text-slate-900">Messages</h2>
                <div className="relative">
                    <input
                        type="text"
                        placeholder="Rechercher une conversation..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg pl-9 pr-3 py-2 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-all outline-none"
                    />
                    <svg className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                </div>
            </div>

            {/* Conversation List */}
            <div className="flex-1 overflow-y-auto">
                {filteredConversations.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-center p-6">
                        <div className="w-16 h-16 rounded-full bg-slate-100 flex items-center justify-center mb-4">
                            <span className="text-2xl">🔍</span>
                        </div>
                        <h3 className="text-sm font-semibold text-slate-900 mb-1">
                            Aucun résultat
                        </h3>
                        <p className="text-xs text-slate-500">
                            Essayez une autre recherche
                        </p>
                    </div>
                ) : (
                    <div className="divide-y divide-slate-100">
                        {filteredConversations.map((conversation, index) => {
                            const otherUser = getOtherParticipant(conversation, MOCK_CURRENT_USER.id);
                            const isActive = activeId === conversation.id;
                            const hasUnread = conversation.unreadCount > 0;
                            const isLastMessageOwn = conversation.lastMessage?.senderId === MOCK_CURRENT_USER.id;

                            return (
                                <motion.div
                                    key={conversation.id}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.05 }}
                                >
                                    <Link
                                        href={`/messages/${conversation.id}`}
                                        onClick={() => onSelectConversation?.(conversation.id)}
                                        className={`
                                            flex items-center gap-3 p-4 transition-all relative
                                            ${isActive
                                                ? 'bg-brand-50 border-l-4 border-brand-500 pl-[12px]' // Compensate padding
                                                : 'hover:bg-slate-50 border-l-4 border-transparent'
                                            }
                                        `}
                                    >
                                        {/* Avatar */}
                                        <div className="relative flex-shrink-0">
                                            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center overflow-hidden">
                                                {otherUser.avatar ? (
                                                    <img
                                                        src={otherUser.avatar}
                                                        alt={otherUser.name}
                                                        className="w-full h-full object-cover"
                                                    />
                                                ) : (
                                                    <span className="text-lg font-semibold text-brand-600">
                                                        {(otherUser.name || '?').charAt(0)}
                                                    </span>
                                                )}
                                            </div>

                                            {/* Online Indicator */}
                                            {otherUser.isOnline && (
                                                <div className="absolute bottom-0 right-0 w-3.5 h-3.5 bg-green-500 rounded-full border-2 border-white" />
                                            )}
                                        </div>

                                        {/* Content */}
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-center justify-between gap-2">
                                                <h3 className={`
                                                    text-sm truncate
                                                    ${hasUnread ? 'font-bold text-slate-900' : 'font-medium text-slate-700'}
                                                `}>
                                                    {otherUser.name}
                                                </h3>
                                                <span className="text-xs text-slate-400 flex-shrink-0">
                                                    {conversation.lastMessage && formatMessageTime(conversation.lastMessage.timestamp)}
                                                </span>
                                            </div>

                                            <div className="flex items-center gap-2 mt-0.5">
                                                <p className={`
                                                    text-sm truncate flex-1
                                                    ${hasUnread ? 'font-medium text-slate-700' : 'text-slate-500'}
                                                `}>
                                                    {isLastMessageOwn && (
                                                        <span className="text-slate-400">Vous: </span>
                                                    )}
                                                    {conversation.lastMessage?.content}
                                                    {conversation.bookingContext && (
                                                        <span className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-600">
                                                            📅
                                                        </span>
                                                    )}
                                                </p>

                                                {/* Unread Badge */}
                                                {hasUnread && (
                                                    <span className="flex-shrink-0 w-5 h-5 bg-brand-600 text-white text-xs font-bold rounded-full flex items-center justify-center">
                                                        {conversation.unreadCount}
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    </Link>
                                </motion.div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
}
