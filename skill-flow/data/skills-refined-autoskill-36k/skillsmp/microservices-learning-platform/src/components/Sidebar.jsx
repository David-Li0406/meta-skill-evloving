'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useProgress } from '@/hooks/useProgress';
import Search from '@/components/Search';

/**
 * Sidebar - Course navigation sidebar
 * @param {Object} props
 * @param {Array} props.modules - Array of module objects
 */
export default function Sidebar({ modules }) {
    const pathname = usePathname();
    const { isCompleted, getProgress, isLoaded } = useProgress();

    // Prevent hydration mismatch by only showing progress specific elements after load
    if (!isLoaded) return (
        <aside className="w-72 flex-shrink-0 hidden lg:block">
            <div className="sticky top-24 glass rounded-2xl p-4 h-[calc(100vh-120px)] animate-pulse bg-slate-800/20"></div>
        </aside>
    );

    const progress = getProgress();

    
    return (
        <aside className="w-72 flex-shrink-0 hidden lg:block">
            <div className="sticky top-24 glass rounded-2xl p-4 max-h-[calc(100vh-120px)] overflow-y-auto custom-scrollbar">
                {/* Header */}
                <div className="flex items-center gap-3 pb-4 border-b border-slate-700/50 mb-4">
                    <Link href="/" className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
                            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                            </svg>
                        </div>
                        <span className="font-bold text-white">MicroLearn</span>
                    </Link>
                </div>

                {/* Search */}
                <Search />

                {/* Navigation */}
                <nav className="space-y-1">
                    {modules.map((module, index) => {
                        const isActive = pathname === `/course/${module.slug}`;
                        const completed = isCompleted(module.slug);

                        return (
                            <Link
                                key={module.slug}
                                href={`/course/${module.slug}`}
                                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group relative ${isActive
                                    ? 'bg-purple-500/20 border border-purple-500/30'
                                    : 'hover:bg-slate-800/50'
                                    }`}
                            >
                                <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold transition-colors ${isActive
                                    ? 'bg-purple-500 text-white'
                                    : completed
                                        ? 'bg-green-500/20 text-green-400'
                                        : 'bg-slate-800 text-slate-400 group-hover:bg-slate-700'
                                    }`}>
                                    {completed ? (
                                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                        </svg>
                                    ) : (
                                        module.number.toString().padStart(2, '0')
                                    )}
                                </div>
                                <span className={`text-sm truncate flex-1 ${isActive ? 'text-white font-medium' : 'text-slate-400 group-hover:text-white'
                                    }`}>
                                    {module.title}
                                </span>
                            </Link>
                        );
                    })}
                </nav>

                {/* Progress */}
                <div className="mt-6 pt-4 border-t border-slate-700/50">
                    <div className="flex items-center justify-between text-sm mb-2">
                        <span className="text-slate-400">Progress</span>
                        <span className="text-purple-400 font-medium">{progress}%</span>
                    </div>
                    <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                        <div
                            className="h-full bg-gradient-to-r from-purple-500 to-blue-500 rounded-full transition-all duration-500 ease-out"
                            style={{ width: `${progress}%` }}
                        ></div>
                    </div>
                </div>
            </div>
        </aside>
    );
}
