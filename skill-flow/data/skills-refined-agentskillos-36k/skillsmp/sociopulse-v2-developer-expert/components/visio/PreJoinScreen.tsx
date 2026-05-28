'use client';

import { motion } from 'framer-motion';
import { Mic, MicOff, Video, VideoOff } from 'lucide-react';

interface PreJoinScreenProps {
    onJoin: () => void;
    isAudioOn: boolean;
    isVideoOn: boolean;
    onToggleAudio: () => void;
    onToggleVideo: () => void;
}

export function PreJoinScreen({
    onJoin,
    isAudioOn,
    isVideoOn,
    onToggleAudio,
    onToggleVideo,
}: PreJoinScreenProps) {
    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] gap-8 p-4">
            <h1 className="text-2xl font-bold text-white mb-2">Prêt à rejoindre ?</h1>

            {/* Camera Preview */}
            <div className="relative w-full max-w-lg aspect-video bg-slate-800 rounded-2xl overflow-hidden shadow-2xl border border-slate-700">
                {isVideoOn ? (
                    <div className="absolute inset-0 bg-slate-700 flex items-center justify-center">
                        <span className="text-slate-500 text-sm">Caméra active (Simulation)</span>
                    </div>
                ) : (
                    <div className="absolute inset-0 bg-slate-900 flex items-center justify-center">
                        <div className="w-20 h-20 rounded-full bg-slate-800 flex items-center justify-center">
                            <span className="text-2xl text-slate-500">📷</span>
                        </div>
                    </div>
                )}

                {/* Controls overlay */}
                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-3">
                    <button
                        onClick={onToggleAudio}
                        className={`
                            p-3 rounded-full transition-colors 
                            ${isAudioOn ? 'bg-slate-700 text-white hover:bg-slate-600' : 'bg-red-500 text-white hover:bg-red-600 shadow-lg shadow-red-500/20'}
                        `}
                    >
                        {isAudioOn ? <Mic className="w-5 h-5" /> : <MicOff className="w-5 h-5" />}
                    </button>
                    <button
                        onClick={onToggleVideo}
                        className={`
                            p-3 rounded-full transition-colors 
                            ${isVideoOn ? 'bg-slate-700 text-white hover:bg-slate-600' : 'bg-red-500 text-white hover:bg-red-600 shadow-lg shadow-red-500/20'}
                        `}
                    >
                        {isVideoOn ? <Video className="w-5 h-5" /> : <VideoOff className="w-5 h-5" />}
                    </button>
                </div>
            </div>

            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onJoin}
                className="px-8 py-3 bg-live-500 text-white font-semibold rounded-xl shadow-xl shadow-live-500/20 hover:bg-live-600 transition-colors"
            >
                Rejoindre la salle
            </motion.button>
        </div>
    );
}
