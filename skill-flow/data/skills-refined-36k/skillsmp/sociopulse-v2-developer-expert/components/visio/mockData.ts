export interface VisioParticipant {
    id: string;
    name: string;
    avatar?: string;
    isAudioOn: boolean;
    isVideoOn: boolean;
    isSpeaking: boolean;
    role: 'HOST' | 'GUEST';
}

export const MOCK_PARTICIPANTS: VisioParticipant[] = [
    {
        id: 'me',
        name: 'Vous',
        isAudioOn: true,
        isVideoOn: true,
        isSpeaking: false,
        role: 'HOST',
    },
    {
        id: 'guest',
        name: 'Thomas Martin',
        avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
        isAudioOn: true,
        isVideoOn: true,
        isSpeaking: true,
        role: 'GUEST',
    },
];
