'use client';

import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import {
    Mic,
    MicOff,
    Video,
    VideoOff,
    Settings,
    CheckCircle2,
    AlertCircle,
    Loader2
} from 'lucide-react';

interface WaitingRoomProps {
    expertName: string;
    expertAvatar?: string;
    onReady?: () => void;
}

export function WaitingRoom({ expertName, expertAvatar, onReady }: WaitingRoomProps) {
    const [micEnabled, setMicEnabled] = useState(true);
    const [videoEnabled, setVideoEnabled] = useState(true);
    const [micStatus, setMicStatus] = useState<'checking' | 'ok' | 'error'>('checking');
    const [videoStatus, setVideoStatus] = useState<'checking' | 'ok' | 'error'>('checking');
    const [isConnecting, setIsConnecting] = useState(false);
    const videoRef = useRef<HTMLVideoElement>(null);

    // Check media devices
    useEffect(() => {
        async function checkDevices() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: true
                });

                // Mic check
                const audioTracks = stream.getAudioTracks();
                setMicStatus(audioTracks.length > 0 ? 'ok' : 'error');

                // Video check
                const videoTracks = stream.getVideoTracks();
                setVideoStatus(videoTracks.length > 0 ? 'ok' : 'error');

                // Show preview
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
            } catch (error) {
                console.error('Media access error:', error);
                setMicStatus('error');
                setVideoStatus('error');
            }
        }

        checkDevices();

        return () => {
            // Cleanup stream on unmount
            if (videoRef.current?.srcObject) {
                const stream = videoRef.current.srcObject as MediaStream;
                stream.getTracks().forEach(track => track.stop());
            }
        };
    }, []);

    const handleJoin = () => {
        setIsConnecting(true);
        // Simulate connection delay
        setTimeout(() => {
            onReady?.();
        }, 2000);
    };

    const StatusIcon = ({ status }: { status: 'checking' | 'ok' | 'error' }) => {
        if (status === 'checking') return <Loader2 className="w-4 h-4 animate-spin text-slate-400" />;
        if (status === 'ok') return <CheckCircle2 className="w-4 h-4 text-green-500" />;
        return <AlertCircle className="w-4 h-4 text-red-500" />;
    };

    return (
        <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full max-w-2xl"
            >
                {/* Header */}
                <div className="text-center mb-8">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/20 text-purple-400 text-sm font-medium mb-4">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75" />
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-purple-500" />
                        </span>
                        Salle d'attente
                    </div>
                    <h1 className="text-2xl font-bold text-white mb-2">
                        Votre expert se connecte...
                    </h1>
                    <p className="text-slate-400">
                        Préparez-vous pour votre consultation avec <span className="text-white font-medium">{expertName}</span>
                    </p>
                </div>

                {/* Video Preview */}
                <div className="relative rounded-2xl overflow-hidden bg-slate-800 aspect-video mb-6">
                    {videoEnabled ? (
                        <video
                            ref={videoRef}
                            autoPlay
                            playsInline
                            muted
                            className="w-full h-full object-cover scale-x-[-1]"
                        />
                    ) : (
                        <div className="absolute inset-0 flex items-center justify-center bg-slate-800">
                            <div className="w-24 h-24 rounded-full bg-slate-700 flex items-center justify-center">
                                <VideoOff className="w-10 h-10 text-slate-500" />
                            </div>
                        </div>
                    )}

                    {/* Expert thumbnail */}
                    <div className="absolute top-4 right-4 w-20 h-20 rounded-xl bg-slate-700 border-2 border-slate-600 overflow-hidden">
                        {expertAvatar ? (
                            <img src={expertAvatar} alt={expertName} className="w-full h-full object-cover" />
                        ) : (
                            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-500 to-indigo-500">
                                <span className="text-xl font-bold text-white">
                                    {(expertName || '?').charAt(0)}
                                </span>
                            </div>
                        )}
                        <div className="absolute inset-0 flex items-center justify-center bg-black/50">
                            <Loader2 className="w-6 h-6 text-white animate-spin" />
                        </div>
                    </div>

                    {/* Controls */}
                    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-3">
                        <button
                            onClick={() => setMicEnabled(!micEnabled)}
                            className={`
                w-12 h-12 rounded-full flex items-center justify-center transition-all
                ${micEnabled
                                    ? 'bg-slate-700/80 text-white hover:bg-slate-600'
                                    : 'bg-red-500 text-white hover:bg-red-600'
                                }
              `}
                        >
                            {micEnabled ? <Mic className="w-5 h-5" /> : <MicOff className="w-5 h-5" />}
                        </button>

                        <button
                            onClick={() => setVideoEnabled(!videoEnabled)}
                            className={`
                w-12 h-12 rounded-full flex items-center justify-center transition-all
                ${videoEnabled
                                    ? 'bg-slate-700/80 text-white hover:bg-slate-600'
                                    : 'bg-red-500 text-white hover:bg-red-600'
                                }
              `}
                        >
                            {videoEnabled ? <Video className="w-5 h-5" /> : <VideoOff className="w-5 h-5" />}
                        </button>

                        <button className="w-12 h-12 rounded-full bg-slate-700/80 text-white hover:bg-slate-600 flex items-center justify-center transition-all">
                            <Settings className="w-5 h-5" />
                        </button>
                    </div>
                </div>

                {/* Device Status */}
                <div className="flex items-center justify-center gap-6 mb-8">
                    <div className="flex items-center gap-2 text-sm">
                        <StatusIcon status={micStatus} />
                        <span className={micStatus === 'ok' ? 'text-slate-300' : 'text-slate-500'}>
                            Microphone {micStatus === 'ok' ? 'OK' : micStatus === 'checking' ? '...' : 'non détecté'}
                        </span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                        <StatusIcon status={videoStatus} />
                        <span className={videoStatus === 'ok' ? 'text-slate-300' : 'text-slate-500'}>
                            Caméra {videoStatus === 'ok' ? 'OK' : videoStatus === 'checking' ? '...' : 'non détectée'}
                        </span>
                    </div>
                </div>

                {/* Join Button */}
                <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={handleJoin}
                    disabled={isConnecting}
                    className="w-full py-4 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-lg shadow-lg shadow-purple-500/30 flex items-center justify-center gap-2 disabled:opacity-70"
                >
                    {isConnecting ? (
                        <>
                            <Loader2 className="w-5 h-5 animate-spin" />
                            Connexion en cours...
                        </>
                    ) : (
                        <>
                            <Video className="w-5 h-5" />
                            Rejoindre la consultation
                        </>
                    )}
                </motion.button>

                <p className="text-center text-xs text-slate-500 mt-4">
                    En rejoignant, vous acceptez l'enregistrement de la session à des fins de qualité
                </p>
            </motion.div>
        </div>
    );
}
