// ===========================================
// MOCK DATA FOR MESSAGING
// ===========================================

export interface User {
    id: string;
    name: string;
    avatar?: string;
    role: 'FREELANCE' | 'CLIENT';
    isOnline: boolean;
}

export interface Message {
    id: string;
    conversationId: string;
    senderId: string;
    content: string;
    timestamp: Date;
    isRead: boolean;
    type: 'text' | 'image' | 'file';
}

// ... (User interface remains the same)

export interface BookingContext {
    id: string;
    title: string;
    date: Date;
    status: 'PENDING' | 'CONFIRMED' | 'COMPLETED' | 'CANCELLED';
}

export interface Conversation {
    id: string;
    participants: User[];
    lastMessage?: Message;
    unreadCount: number;
    updatedAt: Date;
    bookingContext?: BookingContext;
}

// ===========================================
// MOCK USERS
// ===========================================

export const MOCK_CURRENT_USER: User = {
    id: 'current-user',
    name: 'Marie Dupont',
    avatar: undefined,
    role: 'FREELANCE',
    isOnline: true,
};

export const MOCK_USERS: User[] = [
    {
        id: 'user-1',
        name: 'Thomas Martin',
        avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100',
        role: 'CLIENT',
        isOnline: true,
    },
    {
        id: 'user-2',
        name: 'Sophie Lefèvre',
        avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100',
        role: 'FREELANCE',
        isOnline: false,
    },
    {
        id: 'user-3',
        name: 'EHPAD Les Oliviers',
        avatar: undefined,
        role: 'CLIENT',
        isOnline: true,
    },
    {
        id: 'user-4',
        name: 'Pierre Bernard',
        avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100',
        role: 'FREELANCE',
        isOnline: false,
    },
    {
        id: 'user-5',
        name: 'Clinique Saint-Joseph',
        avatar: undefined,
        role: 'CLIENT',
        isOnline: true,
    },
];

// ===========================================
// MOCK CONVERSATIONS
// ===========================================

export const MOCK_CONVERSATIONS: Conversation[] = [
    {
        id: 'conv-1',
        participants: [MOCK_CURRENT_USER, MOCK_USERS[0]],
        lastMessage: {
            id: 'msg-1',
            conversationId: 'conv-1',
            senderId: 'user-1',
            content: 'Bonjour ! Je suis disponible pour la mission du weekend. Pouvez-vous me donner plus de détails ?',
            timestamp: new Date(Date.now() - 5 * 60 * 1000), // 5 min ago
            isRead: false,
            type: 'text',
        },
        unreadCount: 2,
        updatedAt: new Date(Date.now() - 5 * 60 * 1000),
        bookingContext: {
            id: 'booking-1',
            title: 'Garde de nuit',
            date: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000), // +2 days
            status: 'CONFIRMED',
        },
    },
    {
        id: 'conv-2',
        participants: [MOCK_CURRENT_USER, MOCK_USERS[1]],
        lastMessage: {
            id: 'msg-2',
            conversationId: 'conv-2',
            senderId: 'current-user',
            content: 'Merci pour votre réponse rapide !',
            timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
            isRead: true,
            type: 'text',
        },
        unreadCount: 0,
        updatedAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
        bookingContext: {
            id: 'booking-2',
            title: 'Remplacement Infirmier',
            date: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000),
            status: 'PENDING',
        },
    },
    {
        id: 'conv-3',
        participants: [MOCK_CURRENT_USER, MOCK_USERS[2]],
        lastMessage: {
            id: 'msg-3',
            conversationId: 'conv-3',
            senderId: 'user-3',
            content: 'Nous recherchons un aide-soignant pour le service de nuit. Êtes-vous intéressée ?',
            timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
            isRead: true,
            type: 'text',
        },
        unreadCount: 0,
        updatedAt: new Date(Date.now() - 24 * 60 * 60 * 1000),
    },
    // ... other conversations
    {
        id: 'conv-4',
        participants: [MOCK_CURRENT_USER, MOCK_USERS[3]],
        lastMessage: {
            id: 'msg-4',
            conversationId: 'conv-4',
            senderId: 'user-4',
            content: 'Super, à bientôt !',
            timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
            isRead: true,
            type: 'text',
        },
        unreadCount: 0,
        updatedAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    },
    {
        id: 'conv-5',
        participants: [MOCK_CURRENT_USER, MOCK_USERS[4]],
        lastMessage: {
            id: 'msg-5',
            conversationId: 'conv-5',
            senderId: 'user-5',
            content: 'Votre candidature a bien été reçue. Nous reviendrons vers vous rapidement.',
            timestamp: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 1 week ago
            isRead: false,
            type: 'text',
        },
        unreadCount: 1,
        updatedAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
    },
];

// ===========================================
// MOCK MESSAGES FOR CONV-1
// ===========================================

export const MOCK_MESSAGES: Record<string, Message[]> = {
    'conv-1': [
        {
            id: 'msg-1-1',
            conversationId: 'conv-1',
            senderId: 'current-user',
            content: 'Bonjour Thomas ! J\'ai vu que vous recherchez un éducateur pour le weekend.',
            timestamp: new Date(Date.now() - 30 * 60 * 1000),
            isRead: true,
            type: 'text',
        },
        {
            id: 'msg-1-2',
            conversationId: 'conv-1',
            senderId: 'user-1',
            content: 'Oui, exactement ! Nous avons besoin de renfort samedi et dimanche.',
            timestamp: new Date(Date.now() - 25 * 60 * 1000),
            isRead: true,
            type: 'text',
        },
        {
            id: 'msg-1-3',
            conversationId: 'conv-1',
            senderId: 'current-user',
            content: 'Je suis disponible ces deux jours. Quels sont les horaires prévus ?',
            timestamp: new Date(Date.now() - 20 * 60 * 1000),
            isRead: true,
            type: 'text',
        },
        {
            id: 'msg-1-4',
            conversationId: 'conv-1',
            senderId: 'user-1',
            content: 'Les horaires seraient de 8h à 18h. Est-ce que ça vous convient ?',
            timestamp: new Date(Date.now() - 15 * 60 * 1000),
            isRead: true,
            type: 'text',
        },
        {
            id: 'msg-1-5',
            conversationId: 'conv-1',
            senderId: 'current-user',
            content: 'Parfait, ça me convient ! Quel est le tarif horaire proposé ?',
            timestamp: new Date(Date.now() - 10 * 60 * 1000),
            isRead: true,
            type: 'text',
        },
        {
            id: 'msg-1-6',
            conversationId: 'conv-1',
            senderId: 'user-1',
            content: 'Bonjour ! Je suis disponible pour la mission du weekend. Pouvez-vous me donner plus de détails ?',
            timestamp: new Date(Date.now() - 5 * 60 * 1000),
            isRead: false,
            type: 'text',
        },
    ],
    'conv-2': [
        {
            id: 'msg-2-1',
            conversationId: 'conv-2',
            senderId: 'user-2',
            content: 'Bonjour Marie, merci pour votre message !',
            timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000),
            isRead: true,
            type: 'text',
        },
        {
            id: 'msg-2-2',
            conversationId: 'conv-2',
            senderId: 'current-user',
            content: 'Merci pour votre réponse rapide !',
            timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
            isRead: true,
            type: 'text',
        },
    ],
};

// ===========================================
// HELPER FUNCTIONS
// ===========================================

export function formatMessageTime(date: Date): string {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'À l\'instant';
    if (diffMins < 60) return `${diffMins} min`;
    if (diffHours < 24) return `${diffHours}h`;
    if (diffDays < 7) return `${diffDays}j`;
    return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
}

export function formatBubbleTime(date: Date): string {
    return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
}

export function getOtherParticipant(conversation: Conversation, currentUserId: string): User {
    return conversation.participants.find(p => p.id !== currentUserId) || conversation.participants[0];
}
