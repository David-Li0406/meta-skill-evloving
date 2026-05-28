'use client';

import {
    createContext,
    useContext,
    useEffect,
    useState,
    useCallback,
    useRef,
    ReactNode,
} from 'react';
import { io, Socket } from 'socket.io-client';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';

// ========================================
// TYPES
// ========================================

interface NotificationPayload {
    id: string;
    type: string;
    title: string;
    message: string;
    actionUrl?: string;
    createdAt?: string;
}

interface MissionMessagePayload {
    id: string;
    missionId: string;
    content: string;
    type: 'TEXT' | 'SYSTEM';
    createdAt: string | Date;
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
}

interface SocketContextValue {
    socket: Socket | null;
    isConnected: boolean;
    activeMissionsCount: number;
    joinMissionRoom: (missionId: string) => void;
    leaveMissionRoom: (missionId: string) => void;
    onMissionMessage: (callback: (message: MissionMessagePayload) => void) => () => void;
}

// ========================================
// CONTEXT
// ========================================

const SocketContext = createContext<SocketContextValue | null>(null);

// ========================================
// PROVIDER
// ========================================

interface SocketProviderProps {
    children: ReactNode;
}

export function SocketProvider({ children }: SocketProviderProps) {
    const [socket, setSocket] = useState<Socket | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const [activeMissionsCount, setActiveMissionsCount] = useState(0);
    const missionMessageCallbacks = useRef<Set<(message: MissionMessagePayload) => void>>(new Set());
    const router = useRouter();

    // Initialize socket connection
    useEffect(() => {
        const token = Cookies.get('token');

        // Don't connect if no token (not logged in)
        if (!token) {
            return;
        }

        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';

        const socketInstance = io(apiUrl, {
            auth: { token },
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000,
        });

        // Connection events
        socketInstance.on('connect', () => {
            console.log('Socket connected:', socketInstance.id);
            setIsConnected(true);
        });

        socketInstance.on('disconnect', (reason) => {
            console.log('Socket disconnected:', reason);
            setIsConnected(false);
        });

        socketInstance.on('connect_error', (error) => {
            console.error('Socket connection error:', error.message);
            setIsConnected(false);
        });

        socketInstance.on('connected', (data) => {
            console.log('Socket authenticated:', data);
        });

        socketInstance.on('error', (error) => {
            console.error('Socket error:', error);
        });

        // Handle notifications
        socketInstance.on('notification', (payload: NotificationPayload) => {
            console.log('Notification received:', payload);

            // Show toast with action capability
            toast(payload.title, {
                description: payload.message,
                duration: 5000,
                action: payload.actionUrl
                    ? {
                        label: 'Voir',
                        onClick: () => router.push(payload.actionUrl!),
                    }
                    : undefined,
            });
        });

        // Handle active missions count update
        socketInstance.on('activeMissionsCountUpdate', (data: { count: number }) => {
            console.log('Active missions count update:', data.count);
            setActiveMissionsCount(data.count);
        });

        // Handle mission messages
        socketInstance.on('missionMessage', (message: MissionMessagePayload) => {
            console.log('Mission message received:', message);
            missionMessageCallbacks.current.forEach((callback) => callback(message));
        });

        setSocket(socketInstance);

        // Cleanup on unmount
        return () => {
            socketInstance.disconnect();
            setSocket(null);
            setIsConnected(false);
        };
    }, [router]);

    // Join a mission room
    const joinMissionRoom = useCallback(
        (missionId: string) => {
            if (socket?.connected) {
                socket.emit('joinMissionRoom', { missionId });
                console.log('Joining mission room:', missionId);
            }
        },
        [socket]
    );

    // Leave a mission room
    const leaveMissionRoom = useCallback(
        (missionId: string) => {
            if (socket?.connected) {
                socket.emit('leaveMissionRoom', { missionId });
                console.log('Leaving mission room:', missionId);
            }
        },
        [socket]
    );

    // Subscribe to mission messages
    const onMissionMessage = useCallback(
        (callback: (message: MissionMessagePayload) => void) => {
            missionMessageCallbacks.current.add(callback);
            return () => {
                missionMessageCallbacks.current.delete(callback);
            };
        },
        []
    );

    const value: SocketContextValue = {
        socket,
        isConnected,
        activeMissionsCount,
        joinMissionRoom,
        leaveMissionRoom,
        onMissionMessage,
    };

    return (
        <SocketContext.Provider value={value}>
            {children}
        </SocketContext.Provider>
    );
}

// ========================================
// HOOK
// ========================================

export function useSocket(): SocketContextValue {
    const context = useContext(SocketContext);

    if (!context) {
        // Return a default value for SSR or when not wrapped in provider
        return {
            socket: null,
            isConnected: false,
            activeMissionsCount: 0,
            joinMissionRoom: () => { },
            leaveMissionRoom: () => { },
            onMissionMessage: () => () => { },
        };
    }

    return context;
}

// ========================================
// MISSION CHAT HOOK WITH 24H CLOSURE
// ========================================

interface MissionChatState {
    messages: MissionMessagePayload[];
    isClosing: boolean;
    closesAt: Date | null;
    isLocked: boolean;
    isConnected: boolean;
    addMessage: (message: MissionMessagePayload) => void;
    clearMessages: () => void;
}

export function useMissionChat(missionId: string | null): MissionChatState {
    const { socket, isConnected, joinMissionRoom, leaveMissionRoom, onMissionMessage } = useSocket();
    const [messages, setMessages] = useState<MissionMessagePayload[]>([]);
    const [isClosing, setIsClosing] = useState(false);
    const [closesAt, setClosesAt] = useState<Date | null>(null);
    const [isLocked, setIsLocked] = useState(false);

    // Join/leave mission room
    useEffect(() => {
        if (missionId && isConnected) {
            joinMissionRoom(missionId);

            return () => {
                leaveMissionRoom(missionId);
            };
        }
    }, [missionId, isConnected, joinMissionRoom, leaveMissionRoom]);

    // Listen for new messages
    useEffect(() => {
        if (!missionId) return;

        const unsubscribe = onMissionMessage((message) => {
            if (message.missionId === missionId) {
                setMessages((prev) => [...prev, message]);
            }
        });

        return unsubscribe;
    }, [missionId, onMissionMessage]);

    // Listen for closure events
    useEffect(() => {
        if (!socket || !missionId) return;

        const handleClosing = (data: { closesAt: string; message: string }) => {
            setIsClosing(true);
            setClosesAt(new Date(data.closesAt));
            toast.warning('Mission terminée', {
                description: data.message,
                duration: 10000,
            });
        };

        const handleLocked = (data: { message: string }) => {
            setIsLocked(true);
            setIsClosing(false);
            toast.error('Chat clôturé', {
                description: data.message,
            });
        };

        socket.on('missionClosing', handleClosing);
        socket.on('missionLocked', handleLocked);

        return () => {
            socket.off('missionClosing', handleClosing);
            socket.off('missionLocked', handleLocked);
        };
    }, [socket, missionId]);

    const addMessage = useCallback((message: MissionMessagePayload) => {
        setMessages((prev) => [...prev, message]);
    }, []);

    const clearMessages = useCallback(() => {
        setMessages([]);
    }, []);

    return {
        messages,
        addMessage,
        clearMessages,
        isClosing,
        closesAt,
        isLocked,
        isConnected,
    };
}

// Convenience hook for notifications
export function useNotifications() {
    const { activeMissionsCount } = useSocket();
    return { activeMissionsCount };
}
