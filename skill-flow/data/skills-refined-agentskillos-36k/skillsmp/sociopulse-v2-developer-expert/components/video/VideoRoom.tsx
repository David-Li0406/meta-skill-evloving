'use client';

import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    Mic,
    MicOff,
    Video,
    VideoOff,
    PhoneOff,
    MessageSquare,
    ScreenShare,
    MoreVertical,
    Maximize,
    Volume2
} from 'lucide-react';

interface VideoRoomProps {
    localStream?: MediaStream | null;
    remoteStream?: MediaStream | null;
    participantName: string;
    participantAvatar?: string;
    onLeave?: () => void;
}

export function VideoRoom({
    localStream,
    remoteStream,
    participantName,
    participantAvatar,
    onLeave
}: VideoRoomProps) {
    const [micEnabled, setMicEnabled] = useState(true);
    const [videoEnabled, setVideoEnabled] = useState(true);
    const [isFullscreen, setIsFullscreen] = useState(false);

    const localVideoRef = useRef<HTMLVideoElement>(null);
    const remoteVideoRef = useRef<HTMLVideoElement>(null);

    // Attach streams to video elements
    useEffect(() => {
        if (localVideoRef.current && localStream) {
            localVideoRef.current.srcObject = localStream;
        }
    }, [localStream]);

    useEffect(() => {
        if (remoteVideoRef.current && remoteStream) {
            remoteVideoRef.current.srcObject = remoteStream;
        }
    }, [remoteStream]);

    // Simulated remote video (for demo)
    useEffect(() => {
        async function setupLocalPreview() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: true
                });
                if (localVideoRef.current) {
                    localVideoRef.current.srcObject = stream;
                }
            } catch (error) {
                console.error('Media error:', error);
            }
        }

        if (!localStream) {
            setupLocalPreview();
        }

        return () => {
            if (localVideoRef.current?.srcObject) {
                const stream = localVideoRef.current.srcObject as MediaStream;
                stream.getTracks().forEach(track => track.stop());
            }
        };
    }, [localStream]);

    const toggleMic = () => {
        setMicEnabled(!micEnabled);
        if (localVideoRef.current?.srcObject) {
            const stream = localVideoRef.current.srcObject as MediaStream;
            stream.getAudioTracks().forEach(track => {
                track.enabled = !micEnabled;
            });
        }
    };

    const toggleVideo = () => {
        setVideoEnabled(!videoEnabled);
        if (localVideoRef.current?.srcObject) {
            const stream = localVideoRef.current.srcObject as MediaStream;
            stream.getVideoTracks().forEach(track => {
                track.enabled = !videoEnabled;
            });
        }
    };

    return (
        <div className="relative w-full h-full bg-slate-900">
            {/* Main Video (Remote Participant) */}
            <div className="absolute inset-0">
                {remoteStream ? (
                    <video
                        ref={remoteVideoRef}
                        autoPlay
                        playsInline
                        className="w-full h-full object-cover"
                    />
                ) : (
                    // Simulated remote participant
                    <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-900">
                        <div className="text-center">
                            <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center mb-4">
                                {participantAvatar ? (
                                    <img src={participantAvatar} alt={participantName} className="w-full h-full rounded-full object-cover" />
                                ) : (
                                    <span className="text-5xl font-bold text-white">
                                        {(participantName || '?').charAt(0)}
                                    </span>
                                )}
                            </div>
                            <p className="text-xl font-semibold text-white">{participantName}</p>
                            <div className="flex items-center justify-center gap-2 mt-2 text-green-400">
                                <Volume2 className="w-4 h-4" />
                                <span className="text-sm">Connecté</span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Local Video (Picture-in-Picture) */}
            <motion.div
                drag
                dragConstraints={{ left: 0, right: 0, top: 0, bottom: 0 }}
                dragElastic={0.1}
                className="absolute bottom-24 right-4 w-48 h-36 rounded-xl overflow-hidden bg-slate-800 shadow-2xl border-2 border-slate-700 cursor-move"
            >
                {videoEnabled ? (
                    <video
                        ref={localVideoRef}
                        autoPlay
                        playsInline
                        muted
                        className="w-full h-full object-cover scale-x-[-1]"
                    />
                ) : (
                    <div className="w-full h-full flex items-center justify-center bg-slate-800">
                        <VideoOff className="w-8 h-8 text-slate-500" />
                    </div>
                )}

                {/* Name badge */}
                <div className="absolute bottom-2 left-2 px-2 py-1 rounded-md bg-black/50 backdrop-blur-sm">
                    <span className="text-xs text-white font-medium">Vous</span>
                </div>

                {/* Mic indicator */}
                {!micEnabled && (
                    <div className="absolute top-2 right-2 p-1 rounded-full bg-red-500">
                        <MicOff className="w-3 h-3 text-white" />
                    </div>
                )}
            </motion.div>

            {/* Bottom Controls */}
            <div className="absolute bottom-0 left-0 right-0 p-4">
                <div className="flex items-center justify-center gap-3">
                    {/* Mic */}
                    <button
                        onClick={toggleMic}
                        className={`
              w-14 h-14 rounded-full flex items-center justify-center transition-all
              ${micEnabled
                                ? 'bg-slate-700/80 text-white hover:bg-slate-600'
                                : 'bg-red-500 text-white hover:bg-red-600'
                            }
            `}
                    >
                        {micEnabled ? <Mic className="w-6 h-6" /> : <MicOff className="w-6 h-6" />}
                    </button>

                    {/* Video */}
                    <button
                        onClick={toggleVideo}
                        className={`
              w-14 h-14 rounded-full flex items-center justify-center transition-all
              ${videoEnabled
                                ? 'bg-slate-700/80 text-white hover:bg-slate-600'
                                : 'bg-red-500 text-white hover:bg-red-600'
                            }
            `}
                    >
                        {videoEnabled ? <Video className="w-6 h-6" /> : <VideoOff className="w-6 h-6" />}
                    </button>

                    {/* Screen Share */}
                    <button className="w-14 h-14 rounded-full bg-slate-700/80 text-white hover:bg-slate-600 flex items-center justify-center transition-all">
                        <ScreenShare className="w-6 h-6" />
                    </button>

                    {/* Chat */}
                    <button className="w-14 h-14 rounded-full bg-slate-700/80 text-white hover:bg-slate-600 flex items-center justify-center transition-all">
                        <MessageSquare className="w-6 h-6" />
                    </button>

                    {/* End Call */}
                    <button
                        onClick={onLeave}
                        className="w-14 h-14 rounded-full bg-red-500 text-white hover:bg-red-600 flex items-center justify-center transition-all"
                    >
                        <PhoneOff className="w-6 h-6" />
                    </button>

                    {/* More */}
                    <button className="w-14 h-14 rounded-full bg-slate-700/80 text-white hover:bg-slate-600 flex items-center justify-center transition-all">
                        <MoreVertical className="w-6 h-6" />
                    </button>

                    {/* Fullscreen */}
                    <button
                        onClick={() => setIsFullscreen(!isFullscreen)}
                        className="w-14 h-14 rounded-full bg-slate-700/80 text-white hover:bg-slate-600 flex items-center justify-center transition-all"
                    >
                        <Maximize className="w-6 h-6" />
                    </button>
                </div>
            </div>
        </div>
    );
}
