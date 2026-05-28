'use client';

import { useProgress } from '@/hooks/useProgress';
import { modules } from '@/data/modules';

export default function CourseProgress() {
    const { getProgress, completedModules, isLoaded } = useProgress();

    // Prevent hydration mismatch
    if (!isLoaded) return (
        <div className="glass rounded-2xl p-6 mb-8 animate-pulse">
            <div className="flex items-center justify-between mb-4">
                <span className="text-slate-400">Your Progress</span>
                <span className="text-purple-400 font-semibold">...</span>
            </div>
            <div className="w-full h-3 rounded-full bg-slate-800"></div>
        </div>
    );
    

    const progress = getProgress();

    return (
        <div className="glass rounded-2xl p-6 mb-8">
            <div className="flex items-center justify-between mb-4">
                <span className="text-slate-400">Your Progress</span>
                <span className="text-purple-400 font-semibold">
                    {completedModules.length} / {modules.length} modules
                </span>
            </div>
            <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
                <div
                    className="h-full bg-gradient-to-r from-purple-500 to-blue-500 rounded-full transition-all duration-1000 ease-out"
                    style={{ width: `${progress}%` }}
                ></div>
            </div>
        </div>
    );
}
