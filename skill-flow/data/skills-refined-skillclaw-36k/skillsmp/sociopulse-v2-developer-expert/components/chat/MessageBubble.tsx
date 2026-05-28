'use client';

import { motion } from 'framer-motion';
import { Check, CheckCheck } from 'lucide-react';
import { formatBubbleTime, type Message } from './mockData';

// ===========================================
// TYPES
// ===========================================

export interface MessageBubbleProps {
    message: Message;
    isOwn: boolean;
    showAvatar?: boolean;
    senderName?: string;
}

// ===========================================
// COMPONENT
// ===========================================

export function MessageBubble({
    message,
    isOwn,
    showAvatar = false,
    senderName,
}: MessageBubbleProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ type: 'spring', stiffness: 200, damping: 20 }}
            className={`flex ${isOwn ? 'justify-end' : 'justify-start'} mb-2`}
        >
            <div
                className={`
                    relative max-w-[75%] sm:max-w-[65%] px-4 py-2.5 rounded-2xl
                    ${isOwn
                        ? 'bg-brand-600 text-white rounded-br-md'
                        : 'bg-slate-100 text-slate-800 rounded-bl-md'
                    }
                `}
            >
                {/* Sender Name (for group chats) */}
                {!isOwn && senderName && (
                    <p className="text-xs font-semibold text-brand-600 mb-1">
                        {senderName}
                    </p>
                )}

                {/* Message Content */}
                <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
                    {message.content}
                </p>

                {/* Timestamp + Read Receipt */}
                <div className={`
                    flex items-center gap-1 mt-1
                    ${isOwn ? 'justify-end' : 'justify-start'}
                `}>
                    <span className={`text-[10px] ${isOwn ? 'text-white/70' : 'text-slate-400'}`}>
                        {formatBubbleTime(message.timestamp)}
                    </span>

                    {/* Read Receipt (only for own messages) */}
                    {isOwn && (
                        message.isRead ? (
                            <CheckCheck className="w-3.5 h-3.5 text-white/70" />
                        ) : (
                            <Check className="w-3.5 h-3.5 text-white/70" />
                        )
                    )}
                </div>

                {/* Bubble Tail */}
                <div
                    className={`
                        absolute bottom-0 w-3 h-3
                        ${isOwn
                            ? 'right-[-6px] bg-brand-600'
                            : 'left-[-6px] bg-slate-100'
                        }
                    `}
                    style={{
                        clipPath: isOwn
                            ? 'polygon(0 0, 100% 0, 0 100%)'
                            : 'polygon(100% 0, 0 0, 100% 100%)',
                    }}
                />
            </div>
        </motion.div>
    );
}
