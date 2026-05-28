'use client';

import { Mic, MicOff, Video, VideoOff, PhoneOff, MonitorUp, MoreVertical } from 'lucide-react';

interface ControlBarProps {
    isAudioOn: boolean;
    isVideoOn: boolean;
    onToggleAudio: () => void;
    onToggleVideo: () => void;
    onEndCall: () => void;
}

export function ControlBar({
    isAudioOn,
    isVideoOn,
    onToggleAudio,
    onToggleVideo,
    onEndCall,
}: ControlBarProps) {
    return (
        <div className="fixed bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-3 px-6 py-3 bg-slate-900/90 backdrop-blur-xl border border-white/10 rounded-full shadow-2xl z-50">
            <button
                onClick={onToggleAudio}
                className={`
                    p-3 rounded-full transition-all
                    ${isAudioOn ? 'bg-slate-800 text-white hover:bg-slate-700' : 'bg-white text-slate-900 hover:bg-slate-200'}
                `}
            >
                {isAudioOn ? <Mic className="w-5 h-5" /> : <MicOff className="w-5 h-5" />}
            </button>
            <button
                onClick={onToggleVideo}
                className={`
                    p-3 rounded-full transition-all
                    ${isVideoOn ? 'bg-slate-800 text-white hover:bg-slate-700' : 'bg-white text-slate-900 hover:bg-slate-200'}
                `}
            >
                {isVideoOn ? <Video className="w-5 h-5" /> : <VideoOff className="w-5 h-5" />}
            </button>

            <div className="w-px h-8 bg-white/10 mx-1" />

            <button className="p-3 rounded-full bg-slate-800 text-white hover:bg-slate-700 transition-all">
                <MonitorUp className="w-5 h-5" />
            </button>
            <button className="p-3 rounded-full bg-slate-800 text-white hover:bg-slate-700 transition-all">
                <MoreVertical className="w-5 h-5" />
            </button>

            <div className="w-px h-8 bg-white/10 mx-1" />

            <button
                onClick={onEndCall}
                className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-full transition-all flex items-center gap-2 font-medium shadow-lg shadow-red-500/20"
            >
                <PhoneOff className="w-5 h-5" />
                <span className="hidden sm:inline">Quitter</span>
            </button>
        </div>
    );
}
