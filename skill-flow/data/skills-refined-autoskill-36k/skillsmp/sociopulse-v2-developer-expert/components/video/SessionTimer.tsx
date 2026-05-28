'use client';

import { useEffect, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface SessionTimerProps {
    durationMinutes?: number;
    onTimeUp?: () => void;
    onFiveMinutesLeft?: () => void;
    isRunning?: boolean;
}

export function SessionTimer({
    durationMinutes = 60,
    onTimeUp,
    onFiveMinutesLeft,
    isRunning = true
}: SessionTimerProps) {
    const [remainingSeconds, setRemainingSeconds] = useState(durationMinutes * 60);
    const [hasNotifiedFiveMin, setHasNotifiedFiveMin] = useState(false);

    const formatTime = useCallback((totalSeconds: number) => {
        const mins = Math.floor(totalSeconds / 60);
        const secs = totalSeconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }, []);

    useEffect(() => {
        if (!isRunning) return;

        const interval = setInterval(() => {
            setRemainingSeconds(prev => {
                if (prev <= 1) {
                    clearInterval(interval);
                    onTimeUp?.();
                    return 0;
                }

                // Notify at 5 minutes
                if (prev === 5 * 60 + 1 && !hasNotifiedFiveMin) {
                    setHasNotifiedFiveMin(true);
                    onFiveMinutesLeft?.();
                }

                return prev - 1;
            });
        }, 1000);

        return () => clearInterval(interval);
    }, [isRunning, onTimeUp, onFiveMinutesLeft, hasNotifiedFiveMin]);

    const percentage = (remainingSeconds / (durationMinutes * 60)) * 100;
    const isLow = remainingSeconds <= 5 * 60; // 5 minutes
    const isCritical = remainingSeconds <= 60; // 1 minute

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className={`
        fixed top-4 right-4 z-50 px-4 py-2 rounded-full backdrop-blur-xl shadow-lg
        flex items-center gap-3
        ${isCritical
                    ? 'bg-red-500/90 text-white'
                    : isLow
                        ? 'bg-amber-500/90 text-white'
                        : 'bg-black/70 text-white'
                }
      `}
        >
            {/* Progress Ring */}
            <div className="relative w-8 h-8">
                <svg className="w-8 h-8 -rotate-90" viewBox="0 0 32 32">
                    <circle
                        cx="16"
                        cy="16"
                        r="14"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="3"
                        className="opacity-20"
                    />
                    <circle
                        cx="16"
                        cy="16"
                        r="14"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="3"
                        strokeDasharray={`${percentage * 0.88} 88`}
                        strokeLinecap="round"
                        className="transition-all duration-1000"
                    />
                </svg>
            </div>

            {/* Time Display */}
            <span className={`
        font-mono text-lg font-bold tabular-nums
        ${isCritical ? 'animate-pulse' : ''}
      `}>
                {formatTime(remainingSeconds)}
            </span>
        </motion.div>
    );
}
