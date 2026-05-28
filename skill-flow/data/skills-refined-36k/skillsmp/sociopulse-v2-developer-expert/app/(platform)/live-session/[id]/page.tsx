'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { WaitingRoom, VideoRoom, SessionTimer } from '@/components/video';
import { ToastContainer, useToasts } from '@/components/ui/Toast';

type SessionState = 'waiting' | 'connecting' | 'connected' | 'ended';

// Mock session data
const MOCK_SESSION = {
    id: 'session_123',
    expertName: 'Dr. Marie Dupont',
    expertAvatar: null,
    serviceName: 'Coaching Bien-être',
    duration: 60, // minutes
    scheduledAt: new Date(),
};

export default function LiveSessionPage() {
    const params = useParams();
    const router = useRouter();
    const sessionId = params.id as string;

    const [sessionState, setSessionState] = useState<SessionState>('waiting');
    const [sessionData, setSessionData] = useState(MOCK_SESSION);
    const [timerStarted, setTimerStarted] = useState(false);

    const { toasts, addToast, removeToast } = useToasts();

    // Load session data
    useEffect(() => {
        // In production, fetch session data from API
        console.log('Loading session:', sessionId);
    }, [sessionId]);

    // Handle expert connection (simulated)
    const handleReady = useCallback(() => {
        setSessionState('connecting');

        // Simulate connection delay
        setTimeout(() => {
            setSessionState('connected');
            setTimerStarted(true);

            addToast({
                message: `Connecté avec ${sessionData.expertName}`,
                type: 'success',
                duration: 3000,
            });
        }, 2000);
    }, [sessionData.expertName, addToast]);

    // Handle 5 minutes warning
    const handleFiveMinutesLeft = useCallback(() => {
        addToast({
            message: '⏰ Fin de séance imminente - 5 minutes restantes',
            type: 'warning',
            duration: 10000,
        });
    }, [addToast]);

    // Handle session end
    const handleTimeUp = useCallback(() => {
        addToast({
            message: 'La séance est terminée. Merci pour votre participation !',
            type: 'info',
            duration: 0, // Don't auto-dismiss
        });

        setSessionState('ended');

        // Redirect after delay
        setTimeout(() => {
            router.push('/dashboard');
        }, 5000);
    }, [addToast, router]);

    // Handle leave session
    const handleLeave = useCallback(() => {
        const confirm = window.confirm('Êtes-vous sûr de vouloir quitter la séance ?');
        if (confirm) {
            setSessionState('ended');
            router.push('/dashboard');
        }
    }, [router]);

    return (
        <div className="h-screen w-screen overflow-hidden bg-slate-900">
            {/* Timer Overlay (only when connected) */}
            {sessionState === 'connected' && timerStarted && (
                <SessionTimer
                    durationMinutes={sessionData.duration}
                    isRunning={true}
                    onFiveMinutesLeft={handleFiveMinutesLeft}
                    onTimeUp={handleTimeUp}
                />
            )}

            {/* Main Content */}
            {sessionState === 'waiting' && (
                <WaitingRoom
                    expertName={sessionData.expertName}
                    expertAvatar={sessionData.expertAvatar || undefined}
                    onReady={handleReady}
                />
            )}

            {sessionState === 'connecting' && (
                <div className="h-full flex items-center justify-center">
                    <div className="text-center">
                        <div className="w-16 h-16 mx-auto mb-4 rounded-full border-4 border-purple-500 border-t-transparent animate-spin" />
                        <p className="text-white text-lg font-medium">Connexion en cours...</p>
                        <p className="text-slate-400 text-sm mt-2">Établissement de la connexion sécurisée</p>
                    </div>
                </div>
            )}

            {sessionState === 'connected' && (
                <VideoRoom
                    participantName={sessionData.expertName}
                    participantAvatar={sessionData.expertAvatar || undefined}
                    onLeave={handleLeave}
                />
            )}

            {sessionState === 'ended' && (
                <div className="h-full flex items-center justify-center">
                    <div className="text-center max-w-md px-4">
                        <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-green-500/20 flex items-center justify-center">
                            <svg className="w-10 h-10 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                        </div>
                        <h2 className="text-2xl font-bold text-white mb-2">Séance terminée</h2>
                        <p className="text-slate-400 mb-6">
                            Merci pour votre participation ! Un résumé vous sera envoyé par email.
                        </p>
                        <button
                            onClick={() => router.push('/dashboard')}
                            className="px-6 py-3 rounded-xl bg-purple-600 text-white font-semibold hover:bg-purple-700 transition-colors"
                        >
                            Retour au tableau de bord
                        </button>
                    </div>
                </div>
            )}

            {/* Toast Notifications */}
            <ToastContainer toasts={toasts} onRemove={removeToast} />
        </div>
    );
}
