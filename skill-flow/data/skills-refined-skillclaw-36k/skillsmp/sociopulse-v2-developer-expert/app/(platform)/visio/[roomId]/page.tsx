'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import {
    LiveKitRoom,
    VideoConference,
    RoomAudioRenderer,
    ControlBar,
} from '@livekit/components-react';
import '@livekit/components-styles';
import { Loader2, AlertCircle, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { getApiBaseWithVersion } from '@/lib/config';

const getApiBase = getApiBaseWithVersion;

const getToken = () => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('accessToken') ||
        document.cookie.split(';').find(c => c.trim().startsWith('accessToken='))?.split('=')[1];
};

interface TokenResponse {
    token: string;
    roomName: string;
    meetingUrl: string;
}

export default function VisioPage() {
    const params = useParams();
    const router = useRouter();
    const roomId = params.roomId as string;

    const [token, setToken] = useState<string | null>(null);
    const [serverUrl, setServerUrl] = useState<string>('');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchToken = async () => {
            try {
                const authToken = getToken();
                if (!authToken) {
                    setError('Vous devez \u00eatre connect\u00e9 pour acc\u00e9der \u00e0 la visio');
                    setIsLoading(false);
                    return;
                }

                const response = await fetch(`${getApiBase()}/video/join/${roomId}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${authToken}`,
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.message || 'Impossible de rejoindre la session');
                }

                const data: TokenResponse = await response.json();
                setToken(data.token);
                setServerUrl(data.meetingUrl || process.env.NEXT_PUBLIC_LIVEKIT_URL || 'wss://sociopulse.livekit.cloud');
            } catch (err: any) {
                console.error('Failed to get token:', err);
                setError(err.message || 'Erreur lors de la connexion \u00e0 la session vid\u00e9o');
            } finally {
                setIsLoading(false);
            }
        };

        if (roomId) {
            fetchToken();
        }
    }, [roomId]);

    const handleDisconnect = () => {
        router.push('/bookings');
    };

    if (isLoading) {
        return (
            <div className="min-h-screen bg-slate-900 flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <Loader2 className="h-10 w-10 text-teal-500 animate-spin" />
                    <p className="text-white text-lg">Connexion \u00e0 la session...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
                <div className="bg-slate-800 rounded-2xl p-8 max-w-md w-full text-center">
                    <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                        <AlertCircle className="h-8 w-8 text-red-400" />
                    </div>
                    <h2 className="text-xl font-semibold text-white mb-2">Impossible de rejoindre</h2>
                    <p className="text-slate-400 mb-6">{error}</p>
                    <Link
                        href="/bookings"
                        className="inline-flex items-center gap-2 text-teal-500 font-medium hover:underline"
                    >
                        <ArrowLeft className="h-4 w-4" />
                        Retour aux r\u00e9servations
                    </Link>
                </div>
            </div>
        );
    }

    if (!token || !serverUrl) {
        return (
            <div className="min-h-screen bg-slate-900 flex items-center justify-center">
                <p className="text-white">Configuration manquante</p>
            </div>
        );
    }

    return (
        <div className="h-screen bg-slate-900">
            <LiveKitRoom
                token={token}
                serverUrl={serverUrl}
                connect={true}
                video={true}
                audio={true}
                onDisconnected={handleDisconnect}
                data-lk-theme="default"
                style={{ height: '100vh' }}
            >
                <VideoConference />
                <RoomAudioRenderer />
            </LiveKitRoom>
        </div>
    );
}
