'use client';

import Link from 'next/link';
import { useProgress } from '@/hooks/useProgress';

export default function ModuleFooter({ moduleSlug, nextModule, prevModule }) {
    const { isCompleted, toggleCompletion } = useProgress();
    const completed = isCompleted(moduleSlug);

    return (
        <div className="mt-12">
            {/* Completion Toggle */}
            <div className="flex justify-center mb-10">
                <button
                    onClick={() => toggleCompletion(moduleSlug)}
                    className={`flex items-center gap-3 px-8 py-4 rounded-xl font-bold text-lg transition-all duration-300 transform hover:scale-105 active:scale-95 ${completed
                            ? 'bg-green-500/20 text-green-400 border border-green-500/50 hover:bg-green-500/30'
                            : 'bg-gradient-to-r from-purple-500 to-blue-500 text-white shadow-lg sm:shadow-purple-500/20'
                        }`}
                >
                    
                    {completed ? (
                        <>
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                            Marked as Complete
                        </>
                    ) : (
                        <>
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Mark as Complete
                        </>
                    )}
                </button>
            </div>

            {/* Navigation */}
            <div className="flex flex-col sm:flex-row gap-4">
                {prevModule ? (
                    <Link
                        href={`/course/${prevModule.slug}`}
                        className="flex-1 glass rounded-xl p-6 hover:bg-slate-800/50 transition-all duration-300 group"
                    >
                        <div className="flex items-center gap-2 text-slate-400 text-sm mb-2">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                            </svg>
                            Previous Module
                        </div>
                        <div className="text-white font-semibold group-hover:text-purple-400 transition-colors">
                            {prevModule.title}
                        </div>
                    </Link>
                ) : (
                    <div className="flex-1"></div>
                )}

                {nextModule ? (
                    <Link
                        href={`/course/${nextModule.slug}`}
                        className="flex-1 glass rounded-xl p-6 hover:bg-slate-800/50 transition-all duration-300 group text-right"
                    >
                        <div className="flex items-center justify-end gap-2 text-slate-400 text-sm mb-2">
                            Next Module
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </div>
                        <div className="text-white font-semibold group-hover:text-purple-400 transition-colors">
                            {nextModule.title}
                        </div>
                    </Link>
                ) : (
                    <Link
                        href="/course"
                        className="flex-1 glass rounded-xl p-6 bg-gradient-to-r from-purple-500/20 to-blue-500/20 hover:from-purple-500/30 hover:to-blue-500/30 transition-all duration-300 group text-right"
                    >
                        <div className="flex items-center justify-end gap-2 text-slate-400 text-sm mb-2">
                            Completed! 🎉
                        </div>
                        <div className="text-white font-semibold group-hover:text-purple-400 transition-colors">
                            Back to Course Overview
                        </div>
                    </Link>
                )}
            </div>
        </div>
    );
}
