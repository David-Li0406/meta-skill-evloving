'use client';

import { motion } from 'framer-motion';
import { MicOff, User } from 'lucide-react';
import type { VisioParticipant } from './mockData';

interface VideoRoomProps {
    participants: VisioParticipant[];
    className?: string;
}

export function VideoRoom({ participants, className = '' }: VideoRoomProps) {
    // Grid logic: 1 participant = full, 2 = split, etc.
    const gridClassName = participants.length === 1
        ? 'grid-cols-1'
        : participants.length <= 4
            ? 'grid-cols-1 sm:grid-cols-2'
            : 'grid-cols-2 md:grid-cols-3';

    return (
        <div className={`grid gap-4 w-full max-w-7xl mx-auto p-4 ${gridClassName} ${className}`}>
            {participants.map((participant) => (
                <motion.div
                    layout
                    key={participant.id}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    className="relative aspect-video bg-slate-800 rounded-2xl overflow-hidden shadow-2xl border border-slate-700 group"
                >
                    {/* Video Placeholder or Stream */}
                    {participant.isVideoOn ? (
                        <div className="absolute inset-0 bg-slate-700 flex items-center justify-center">
                            {/* In real app, <video> tag here */}
                            {participant.avatar ? (
                                <img src={participant.avatar} alt={participant.name} className="w-full h-full object-cover opacity-50 blur-sm" />
                            ) : null}
                            <span className="text-slate-500 text-sm font-medium z-10">Flux Vidéo ({participant.name})</span>
                        </div>
                    ) : (
                        <div className="absolute inset-0 bg-slate-900 flex items-center justify-center">
                            <div className="w-24 h-24 rounded-full bg-slate-800 flex items-center justify-center">
                                {participant.avatar ? (
                                    <img src={participant.avatar} alt={participant.name} className="w-full h-full rounded-full object-cover" />
                                ) : (
                                    <User className="w-10 h-10 text-slate-500" />
                                )}
                            </div>
                        </div>
                    )}

                    {/* Status Indicators */}
                    <div className="absolute top-4 right-4 flex gap-2">
                        {!participant.isAudioOn && (
                            <div className="p-2 bg-red-500/90 rounded-full backdrop-blur-sm animate-in fade-in zoom-in duration-200">
                                <MicOff className="w-4 h-4 text-white" />
                            </div>
                        )}
                    </div>

                    {/* Name Tag */}
                    <div className="absolute bottom-4 left-4 max-w-[80%]">
                        <div className="px-3 py-1.5 bg-black/60 backdrop-blur-md rounded-lg flex items-center gap-2">
                            <span className="text-sm font-medium text-white truncate">
                                {participant.name} {participant.id === 'me' && '(Vous)'}
                            </span>
                            {participant.isSpeaking && (
                                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                            )}
                        </div>
                    </div>

                    {/* Speaking Border */}
                    {participant.isSpeaking && (
                        <div className="absolute inset-0 border-2 border-green-500 rounded-2xl pointer-events-none" />
                    )}
                </motion.div>
            ))}
        </div>
    );
}
