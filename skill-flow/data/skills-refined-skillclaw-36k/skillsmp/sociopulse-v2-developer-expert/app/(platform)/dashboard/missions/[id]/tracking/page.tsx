'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import {
    ClipboardList,
    MessageCircle,
    FileText,
    CheckCircle2,
    PlayCircle,
    AlertCircle,
    Send,
    ArrowLeft,
    Loader2,
    Clock,
    User,
    Building2
} from 'lucide-react';
import Link from 'next/link';
import { useSocket } from '@/components/providers';

// ========================================
// TYPES
// ========================================

interface TimelineEvent {
    id: string;
    type: 'BRIEFING_READ' | 'MISSION_STARTED' | 'CHAT_MESSAGE' | 'REPORT_SUBMITTED';
    createdAt: string;
    user?: {
        profile?: {
            firstName: string;
            lastName: string;
        };
    };
}

interface Mission {
    id: string;
    title: string;
    jobTitle: string;
    status: 'ASSIGNED' | 'IN_PROGRESS' | 'COMPLETED';
    startDate: string;
    endDate: string;
    city: string;
    description: string;
    client?: {
        establishment?: {
            name: string;
            logoUrl?: string;
        };
    };
    instructions?: {
        content: string;
        checklist: Array<{ id: string; text: string; completed: boolean }>;
        isAcknowledged: boolean;
    };
}

interface ChatMessage {
    id: string;
    content: string;
    type: 'TEXT' | 'SYSTEM';
    createdAt: string | Date;
    missionId?: string;
    sender?: {
        id: string;
        role: string;
        profile?: {
            firstName: string;
            lastName: string;
            avatarUrl?: string;
        };
    };
}

// ========================================
// COMPONENTS
// ========================================

function MissionTimeline({ events }: { events: TimelineEvent[] }) {
    const getEventInfo = (type: TimelineEvent['type']) => {
        switch (type) {
            case 'BRIEFING_READ':
                return { icon: ClipboardList, label: 'Consignes validées', color: 'text-blue-600 bg-blue-100' };
            case 'MISSION_STARTED':
                return { icon: PlayCircle, label: 'Mission démarrée', color: 'text-green-600 bg-green-100' };
            case 'CHAT_MESSAGE':
                return { icon: MessageCircle, label: 'Message envoyé', color: 'text-indigo-600 bg-indigo-100' };
            case 'REPORT_SUBMITTED':
                return { icon: FileText, label: 'Rapport soumis', color: 'text-purple-600 bg-purple-100' };
            default:
                return { icon: Clock, label: 'Événement', color: 'text-slate-600 bg-slate-100' };
        }
    };

    if (events.length === 0) {
        return (
            <div className="text-center py-8 text-slate-500">
                <Clock className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-sm">Aucun événement pour le moment</p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {events.map((event, index) => {
                const info = getEventInfo(event.type);
                const Icon = info.icon;
                return (
                    <motion.div
                        key={event.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="flex items-start gap-3"
                    >
                        <div className={`p-2 rounded-lg ${info.color}`}>
                            <Icon className="w-4 h-4" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-slate-900">{info.label}</p>
                            <p className="text-xs text-slate-500">
                                {new Date(event.createdAt).toLocaleString('fr-FR', {
                                    day: 'numeric',
                                    month: 'short',
                                    hour: '2-digit',
                                    minute: '2-digit',
                                })}
                            </p>
                        </div>
                    </motion.div>
                );
            })}
        </div>
    );
}

function MissionInstructions({
    instructions,
    onAcknowledge,
    isLoading
}: {
    instructions: Mission['instructions'];
    onAcknowledge: () => void;
    isLoading: boolean;
}) {
    if (!instructions) {
        return (
            <div className="text-center py-8 text-slate-500">
                <ClipboardList className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-sm">Aucune consigne disponible</p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            <div className="prose prose-sm max-w-none">
                <p className="text-slate-700 whitespace-pre-wrap">{instructions.content}</p>
            </div>

            {instructions.checklist.length > 0 && (
                <div className="space-y-2">
                    <h4 className="text-sm font-medium text-slate-900">Checklist</h4>
                    {instructions.checklist.map((item) => (
                        <label key={item.id} className="flex items-center gap-2 text-sm">
                            <input
                                type="checkbox"
                                checked={item.completed}
                                readOnly
                                className="rounded border-slate-300"
                            />
                            <span className={item.completed ? 'line-through text-slate-400' : 'text-slate-700'}>
                                {item.text}
                            </span>
                        </label>
                    ))}
                </div>
            )}

            {!instructions.isAcknowledged && (
                <button
                    onClick={onAcknowledge}
                    disabled={isLoading}
                    className="w-full py-3 bg-gradient-to-r from-indigo-600 to-teal-500 text-white font-medium rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center gap-2"
                >
                    {isLoading ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                        <>
                            <CheckCircle2 className="w-5 h-5" />
                            Valider les consignes
                        </>
                    )}
                </button>
            )}

            {instructions.isAcknowledged && (
                <div className="flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-xl text-green-700 text-sm">
                    <CheckCircle2 className="w-5 h-5" />
                    Consignes validées
                </div>
            )}
        </div>
    );
}

function MissionChat({
    messages,
    onSendMessage,
    isLoading,
    currentUserId
}: {
    messages: ChatMessage[];
    onSendMessage: (content: string) => void;
    isLoading: boolean;
    currentUserId?: string;
}) {
    const [newMessage, setNewMessage] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (newMessage.trim()) {
            onSendMessage(newMessage.trim());
            setNewMessage('');
        }
    };

    return (
        <div className="flex flex-col h-full">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3 max-h-[400px]">
                {messages.length === 0 ? (
                    <div className="text-center py-8 text-slate-500">
                        <MessageCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
                        <p className="text-sm">Aucun message pour le moment</p>
                    </div>
                ) : (
                    messages.map((msg) => {
                        const isOwn = msg.sender?.id === currentUserId;
                        const isSystem = msg.type === 'SYSTEM';

                        if (isSystem) {
                            return (
                                <div key={msg.id} className="text-center">
                                    <span className="inline-block px-3 py-1.5 bg-slate-100 text-slate-600 text-xs rounded-full">
                                        {msg.content}
                                    </span>
                                </div>
                            );
                        }

                        return (
                            <div
                                key={msg.id}
                                className={`flex ${isOwn ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-[80%] rounded-2xl px-4 py-2 ${isOwn
                                        ? 'bg-gradient-to-r from-indigo-600 to-teal-500 text-white'
                                        : 'bg-slate-100 text-slate-900'
                                        }`}
                                >
                                    {!isOwn && msg.sender?.profile && (
                                        <p className="text-xs font-medium mb-1 opacity-75">
                                            {msg.sender.profile.firstName}
                                        </p>
                                    )}
                                    <p className="text-sm">{msg.content}</p>
                                    <p className={`text-xs mt-1 ${isOwn ? 'text-white/70' : 'text-slate-500'}`}>
                                        {new Date(msg.createdAt).toLocaleTimeString('fr-FR', {
                                            hour: '2-digit',
                                            minute: '2-digit',
                                        })}
                                    </p>
                                </div>
                            </div>
                        );
                    })
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSubmit} className="p-4 border-t border-slate-200">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        placeholder="Votre message..."
                        className="flex-1 px-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    />
                    <button
                        type="submit"
                        disabled={!newMessage.trim() || isLoading}
                        className="p-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 transition-colors"
                    >
                        {isLoading ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                        ) : (
                            <Send className="w-5 h-5" />
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
}

function MissionReportForm({
    missionStatus,
    onSubmit,
    isLoading
}: {
    missionStatus: Mission['status'];
    onSubmit: (data: { content: string; incidents?: string; hoursWorked?: number }) => void;
    isLoading: boolean;
}) {
    const [content, setContent] = useState('');
    const [incidents, setIncidents] = useState('');
    const [hoursWorked, setHoursWorked] = useState<string>('');

    const canSubmit = missionStatus === 'IN_PROGRESS';

    if (!canSubmit) {
        return (
            <div className="text-center py-8">
                <AlertCircle className="w-8 h-8 mx-auto mb-2 text-amber-500" />
                <p className="text-sm text-slate-600">
                    Le rapport ne peut être soumis qu'une fois la mission démarrée.
                </p>
            </div>
        );
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit({
            content,
            incidents: incidents || undefined,
            hoursWorked: hoursWorked ? parseFloat(hoursWorked) : undefined,
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">
                    Bilan de la mission *
                </label>
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    rows={4}
                    required
                    minLength={10}
                    placeholder="Décrivez le déroulement de la mission..."
                    className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">
                    Incidents éventuels
                </label>
                <textarea
                    value={incidents}
                    onChange={(e) => setIncidents(e.target.value)}
                    rows={2}
                    placeholder="Signalez tout incident ou difficulté rencontrée..."
                    className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-slate-700 mb-1.5">
                    Heures effectuées
                </label>
                <input
                    type="number"
                    value={hoursWorked}
                    onChange={(e) => setHoursWorked(e.target.value)}
                    step="0.5"
                    min="0.5"
                    max="24"
                    placeholder="Ex: 8"
                    className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
            </div>

            <button
                type="submit"
                disabled={!content.trim() || content.length < 10 || isLoading}
                className="w-full py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-medium rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center gap-2"
            >
                {isLoading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                    <>
                        <FileText className="w-5 h-5" />
                        Soumettre le rapport
                    </>
                )}
            </button>
        </form>
    );
}

// ========================================
// MAIN PAGE
// ========================================

export default function MissionTrackingPage() {
    const params = useParams();
    const missionId = params.id as string;
    const { joinMissionRoom, leaveMissionRoom, onMissionMessage, isConnected } = useSocket();

    const [mission, setMission] = useState<Mission | null>(null);
    const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [actionLoading, setActionLoading] = useState(false);
    const [activeTab, setActiveTab] = useState<'timeline' | 'instructions' | 'chat' | 'report'>('timeline');

    // TODO: Get from auth context
    const currentUserId = '';

    // Join mission room for real-time chat
    useEffect(() => {
        if (isConnected && missionId) {
            joinMissionRoom(missionId);
            return () => {
                leaveMissionRoom(missionId);
            };
        }
    }, [isConnected, missionId, joinMissionRoom, leaveMissionRoom]);

    // Subscribe to incoming chat messages
    useEffect(() => {
        const unsubscribe = onMissionMessage((incomingMessage) => {
            // Only add messages for this mission and avoid duplicates
            if (incomingMessage.missionId === missionId) {
                setMessages((prev) => {
                    // Check if message already exists
                    if (prev.some((m) => m.id === incomingMessage.id)) {
                        return prev;
                    }
                    return [...prev, incomingMessage];
                });
            }
        });

        return unsubscribe;
    }, [missionId, onMissionMessage]);

    useEffect(() => {
        // TODO: Fetch mission data from API
        const fetchData = async () => {
            try {
                // Mock for now
                setMission({
                    id: missionId,
                    title: 'Remplacement urgente - Aide-soignant',
                    jobTitle: 'Aide-soignant(e)',
                    status: 'ASSIGNED',
                    startDate: new Date().toISOString(),
                    endDate: new Date().toISOString(),
                    city: 'Paris',
                    description: 'Mission de renfort pour le service gériatrie.',
                    client: {
                        establishment: {
                            name: 'EHPAD Les Jardins',
                        },
                    },
                    instructions: {
                        content: 'Veuillez vous présenter à l\'accueil à 7h00. Badge fourni sur place.',
                        checklist: [
                            { id: '1', text: 'Apporter sa carte professionnelle', completed: false },
                            { id: '2', text: 'Pièce d\'identité obligatoire', completed: false },
                        ],
                        isAcknowledged: false,
                    },
                });
                setTimeline([]);
                setMessages([]);
                setIsLoading(false);
            } catch (error) {
                console.error('Error fetching mission:', error);
                setIsLoading(false);
            }
        };

        fetchData();
    }, [missionId]);

    const handleAcknowledge = async () => {
        setActionLoading(true);
        // TODO: Call API
        setTimeout(() => {
            if (mission?.instructions) {
                setMission({
                    ...mission,
                    instructions: { ...mission.instructions, isAcknowledged: true },
                });
            }
            setTimeline(prev => [...prev, {
                id: Date.now().toString(),
                type: 'BRIEFING_READ',
                createdAt: new Date().toISOString(),
            }]);
            setActionLoading(false);
        }, 1000);
    };

    const handleStartMission = async () => {
        setActionLoading(true);
        // TODO: Call API
        setTimeout(() => {
            if (mission) {
                setMission({ ...mission, status: 'IN_PROGRESS' });
            }
            setTimeline(prev => [...prev, {
                id: Date.now().toString(),
                type: 'MISSION_STARTED',
                createdAt: new Date().toISOString(),
            }]);
            setActionLoading(false);
        }, 1000);
    };

    const handleSendMessage = async (content: string) => {
        setActionLoading(true);
        // TODO: Call API
        setTimeout(() => {
            setMessages(prev => [...prev, {
                id: Date.now().toString(),
                content,
                type: 'TEXT',
                createdAt: new Date().toISOString(),
                sender: {
                    id: currentUserId,
                    role: 'TALENT',
                    profile: { firstName: 'Vous', lastName: '' },
                },
            }]);
            setActionLoading(false);
        }, 500);
    };

    const handleSubmitReport = async (data: { content: string; incidents?: string; hoursWorked?: number }) => {
        setActionLoading(true);
        // TODO: Call API
        setTimeout(() => {
            if (mission) {
                setMission({ ...mission, status: 'COMPLETED' });
            }
            setTimeline(prev => [...prev, {
                id: Date.now().toString(),
                type: 'REPORT_SUBMITTED',
                createdAt: new Date().toISOString(),
            }]);
            setActionLoading(false);
        }, 1000);
    };

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
            </div>
        );
    }

    if (!mission) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center p-4">
                <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
                <h1 className="text-xl font-semibold text-slate-900 mb-2">Mission introuvable</h1>
                <Link href="/dashboard/tracking" className="text-indigo-600 hover:underline">
                    Retour au suivi
                </Link>
            </div>
        );
    }

    const getStatusInfo = () => {
        switch (mission.status) {
            case 'IN_PROGRESS':
                return { label: 'En cours', color: 'bg-green-100 text-green-700', icon: PlayCircle };
            case 'COMPLETED':
                return { label: 'Terminée', color: 'bg-purple-100 text-purple-700', icon: CheckCircle2 };
            default:
                return { label: 'Assignée', color: 'bg-blue-100 text-blue-700', icon: Clock };
        }
    };

    const statusInfo = getStatusInfo();
    const StatusIcon = statusInfo.icon;

    const tabs = [
        { id: 'timeline' as const, label: 'Timeline', icon: Clock },
        { id: 'instructions' as const, label: 'Consignes', icon: ClipboardList },
        { id: 'chat' as const, label: 'Chat', icon: MessageCircle },
        { id: 'report' as const, label: 'Rapport', icon: FileText },
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
            {/* Header */}
            <header className="bg-white/80 backdrop-blur-sm border-b border-slate-200 sticky top-0 z-10">
                <div className="max-w-4xl mx-auto px-4 py-4">
                    <div className="flex items-center gap-3">
                        <Link
                            href="/dashboard/tracking"
                            className="p-2 -ml-2 rounded-lg hover:bg-slate-100 transition-colors"
                        >
                            <ArrowLeft className="w-5 h-5 text-slate-600" />
                        </Link>
                        <div className="flex-1 min-w-0">
                            <h1 className="text-lg font-bold text-slate-900 truncate">{mission.title}</h1>
                            <div className="flex items-center gap-2 text-sm text-slate-500">
                                <Building2 className="w-4 h-4" />
                                <span className="truncate">{mission.client?.establishment?.name}</span>
                            </div>
                        </div>
                        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${statusInfo.color}`}>
                            <StatusIcon className="w-3 h-3" />
                            {statusInfo.label}
                        </span>
                    </div>

                    {/* Start Mission Button */}
                    {mission.status === 'ASSIGNED' && mission.instructions?.isAcknowledged && (
                        <button
                            onClick={handleStartMission}
                            disabled={actionLoading}
                            className="mt-4 w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-medium rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center gap-2"
                        >
                            {actionLoading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <>
                                    <PlayCircle className="w-5 h-5" />
                                    Démarrer la mission
                                </>
                            )}
                        </button>
                    )}
                </div>
            </header>

            {/* Tabs */}
            <div className="bg-white border-b border-slate-200 sticky top-[73px] z-10">
                <div className="max-w-4xl mx-auto px-4">
                    <div className="flex gap-1 overflow-x-auto">
                        {tabs.map((tab) => {
                            const Icon = tab.icon;
                            const isActive = activeTab === tab.id;
                            return (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`flex items-center gap-1.5 px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${isActive
                                        ? 'text-indigo-600 border-indigo-600'
                                        : 'text-slate-500 border-transparent hover:text-slate-700'
                                        }`}
                                >
                                    <Icon className="w-4 h-4" />
                                    {tab.label}
                                </button>
                            );
                        })}
                    </div>
                </div>
            </div>

            {/* Content */}
            <main className="max-w-4xl mx-auto px-4 py-6">
                <motion.div
                    key={activeTab}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white rounded-2xl border border-slate-200 overflow-hidden"
                >
                    {activeTab === 'timeline' && (
                        <div className="p-6">
                            <h2 className="text-lg font-semibold text-slate-900 mb-4">Historique</h2>
                            <MissionTimeline events={timeline} />
                        </div>
                    )}

                    {activeTab === 'instructions' && (
                        <div className="p-6">
                            <h2 className="text-lg font-semibold text-slate-900 mb-4">Consignes du client</h2>
                            <MissionInstructions
                                instructions={mission.instructions}
                                onAcknowledge={handleAcknowledge}
                                isLoading={actionLoading}
                            />
                        </div>
                    )}

                    {activeTab === 'chat' && (
                        <MissionChat
                            messages={messages}
                            onSendMessage={handleSendMessage}
                            isLoading={actionLoading}
                            currentUserId={currentUserId}
                        />
                    )}

                    {activeTab === 'report' && (
                        <div className="p-6">
                            <h2 className="text-lg font-semibold text-slate-900 mb-4">Rapport de mission</h2>
                            <MissionReportForm
                                missionStatus={mission.status}
                                onSubmit={handleSubmitReport}
                                isLoading={actionLoading}
                            />
                        </div>
                    )}
                </motion.div>
            </main>
        </div>
    );
}
