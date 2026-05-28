'use client';

import { useState, useRef, useEffect, FormEvent } from 'react';
import { useMissionChat } from '@/components/providers/SocketProvider';
import { Send, Lock, AlertTriangle, Clock } from 'lucide-react';
import { toast } from 'sonner';
import Cookies from 'js-cookie';

interface MissionChatLiveProps {
    missionId: string;
    initialMessages?: Array<{
        id: string;
        missionId: string;
        content: string;
        type: 'TEXT' | 'SYSTEM';
        createdAt: Date | string;
        sender?: {
            id: string;
            role: string;
            profile?: {
                firstName: string;
                lastName: string;
                avatarUrl?: string;
            };
            establishment?: {
                name: string;
                logoUrl?: string;
            };
        };
    }>;
    initialChatStatus?: {
        isLocked: boolean;
        closesAt?: string | null;
    };
    currentUserId?: string;
}

export function MissionChatLive({
    missionId,
    initialMessages = [],
    initialChatStatus,
    currentUserId,
}: MissionChatLiveProps) {
    const {
        messages: realtimeMessages,
        isClosing,
        closesAt,
        isLocked: realtimeLocked,
        isConnected,
        addMessage,
    } = useMissionChat(missionId);

    const [inputValue, setInputValue] = useState('');
    const [isSending, setIsSending] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Combine initial + realtime messages
    const allMessages = [
        ...initialMessages,
        ...realtimeMessages.filter(
            (rm) => !initialMessages.some((im) => im.id === rm.id)
        ),
    ];

    // Determine locked state (from initial status or realtime)
    const isLocked = realtimeLocked || initialChatStatus?.isLocked || false;
    const closureDate = closesAt || (initialChatStatus?.closesAt ? new Date(initialChatStatus.closesAt) : null);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [allMessages.length]);

    // Handle message send
    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        if (!inputValue.trim() || isLocked || isSending) return;

        setIsSending(true);

        try {
            const token = Cookies.get('accessToken');
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';

            const response = await fetch(`${apiUrl}/api/v1/mission-hub/${missionId}/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ content: inputValue }),
            });

            if (!response.ok) {
                const error = await response.json();
                if (response.status === 403) {
                    toast.error('Chat clôturé', {
                        description: error.message || 'La messagerie est en lecture seule.',
                    });
                } else {
                    throw new Error(error.message || 'Erreur lors de l\'envoi');
                }
                return;
            }

            const newMessage = await response.json();
            addMessage(newMessage);
            setInputValue('');
        } catch (error) {
            console.error('Failed to send message:', error);
            toast.error('Erreur', {
                description: 'Impossible d\'envoyer le message.',
            });
        } finally {
            setIsSending(false);
        }
    };

    // Format closure time
    const formatClosureTime = (date: Date) => {
        return date.toLocaleString('fr-FR', {
            hour: '2-digit',
            minute: '2-digit',
            day: 'numeric',
            month: 'long',
        });
    };

    // Get sender display info
    const getSenderInfo = (sender?: typeof allMessages[0]['sender']) => {
        if (!sender) return { name: 'Système', avatar: null, isSystem: true };

        if (sender.profile) {
            return {
                name: `${sender.profile.firstName} ${sender.profile.lastName}`,
                avatar: sender.profile.avatarUrl,
                isSystem: false,
            };
        }

        if (sender.establishment) {
            return {
                name: sender.establishment.name,
                avatar: sender.establishment.logoUrl,
                isSystem: false,
            };
        }

        return { name: 'Utilisateur', avatar: null, isSystem: false };
    };

    return (
        <div className="flex flex-col h-full bg-white rounded-2xl shadow-soft overflow-hidden">
            {/* Header with connection status */}
            <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
                <h3 className="font-semibold text-slate-900">Chat de mission</h3>
                <div className="flex items-center gap-2">
                    <div
                        className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-500' : 'bg-slate-300'
                            }`}
                    />
                    <span className="text-xs text-slate-500">
                        {isConnected ? 'Connecté' : 'Déconnecté'}
                    </span>
                </div>
            </div>

            {/* Closure Warning Banner */}
            {isClosing && closureDate && (
                <div className="px-4 py-3 bg-amber-50 border-b border-amber-200 flex items-center gap-3">
                    <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0" />
                    <div className="flex-1">
                        <p className="text-sm font-medium text-amber-800">
                            Mission terminée
                        </p>
                        <p className="text-xs text-amber-700">
                            La messagerie fermera automatiquement le {formatClosureTime(closureDate)}
                        </p>
                    </div>
                    <Clock className="w-4 h-4 text-amber-600" />
                </div>
            )}

            {/* Locked Banner */}
            {isLocked && (
                <div className="px-4 py-3 bg-slate-100 border-b border-slate-200 flex items-center gap-3">
                    <Lock className="w-5 h-5 text-slate-500 flex-shrink-0" />
                    <p className="text-sm text-slate-600">
                        🔒 Mission clôturée. La messagerie est désormais en lecture seule.
                    </p>
                </div>
            )}

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {allMessages.map((message) => {
                    const senderInfo = getSenderInfo(message.sender);
                    const isOwnMessage = message.sender?.id === currentUserId;
                    const isSystem = message.type === 'SYSTEM';

                    if (isSystem) {
                        return (
                            <div
                                key={message.id}
                                className="flex justify-center"
                            >
                                <div className="px-4 py-2 bg-slate-100 rounded-full text-sm text-slate-600">
                                    {message.content}
                                </div>
                            </div>
                        );
                    }

                    return (
                        <div
                            key={message.id}
                            className={`flex ${isOwnMessage ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[75%] ${isOwnMessage
                                        ? 'bg-indigo-600 text-white rounded-2xl rounded-br-sm'
                                        : 'bg-slate-100 text-slate-900 rounded-2xl rounded-bl-sm'
                                    } px-4 py-3`}
                            >
                                {!isOwnMessage && (
                                    <p className="text-xs font-medium mb-1 opacity-75">
                                        {senderInfo.name}
                                    </p>
                                )}
                                <p className="text-sm">{message.content}</p>
                                <p
                                    className={`text-xs mt-1 ${isOwnMessage ? 'text-indigo-200' : 'text-slate-500'
                                        }`}
                                >
                                    {new Date(message.createdAt).toLocaleTimeString('fr-FR', {
                                        hour: '2-digit',
                                        minute: '2-digit',
                                    })}
                                </p>
                            </div>
                        </div>
                    );
                })}
                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="p-4 border-t border-slate-100">
                <div className="flex items-center gap-3">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder={
                            isLocked
                                ? 'La messagerie est en lecture seule'
                                : 'Écrivez votre message...'
                        }
                        disabled={isLocked || isSending}
                        className={`flex-1 px-4 py-3 rounded-xl border transition-colors ${isLocked
                                ? 'bg-slate-100 text-slate-400 border-slate-200 cursor-not-allowed'
                                : 'bg-white border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:outline-none'
                            }`}
                    />
                    <button
                        type="submit"
                        disabled={isLocked || isSending || !inputValue.trim()}
                        className={`p-3 rounded-xl transition-colors ${isLocked || isSending || !inputValue.trim()
                                ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
                                : 'bg-indigo-600 text-white hover:bg-indigo-700'
                            }`}
                    >
                        {isLocked ? (
                            <Lock className="w-5 h-5" />
                        ) : (
                            <Send className="w-5 h-5" />
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
}

export default MissionChatLive;
