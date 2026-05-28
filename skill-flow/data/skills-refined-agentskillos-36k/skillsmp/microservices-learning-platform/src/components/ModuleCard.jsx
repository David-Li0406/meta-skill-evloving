'use client';

import Link from 'next/link';
import { useProgress } from '@/hooks/useProgress';

/**
 * ModuleCard - Course module card with glassmorphism and hover effects
 * @param {Object} props
 * @param {number} props.number - Module number
 * @param {string} props.title - Module title
 * @param {string} props.description - Module description
 * @param {string[]} props.topics - List of topics
 * @param {string} props.difficulty - 'beginner' | 'intermediate' | 'advanced'
 * @param {string} props.slug - URL slug for the module
 * @param {boolean} props.completed - Optional override for completion status
 */
export default function ModuleCard({ number, title, description, topics, difficulty, slug, completed: completedProp }) {
    const { isCompleted, isLoaded, markAsCompleted } = useProgress();

    
    // Use prop if provided, otherwise check store (once loaded)
    const completed = completedProp !== undefined ? completedProp : (isLoaded && isCompleted(slug));

    const difficultyStyles = {

        beginner: 'badge-beginner',
        intermediate: 'badge-intermediate',
        advanced: 'badge-advanced'
    };

    const difficultyLabels = {
        beginner: '🟢 Beginner',
        intermediate: '🟡 Intermediate',
        advanced: '🔴 Advanced'
    };

    return (
        <Link href={`/course/${slug}`} className="block group">
            <div className={`card h-full transition-all duration-300 ${completed ? 'border-green-500/30 bg-green-900/10' : ''}`}>
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                        <div className={`w-12 h-12 rounded-xl border flex items-center justify-center text-lg font-bold group-hover:scale-110 transition-transform duration-300 ${completed
                            ? 'bg-green-500/20 border-green-500/30 text-green-400'
                            : 'bg-gradient-to-br from-purple-500/20 to-blue-500/20 border-purple-500/30 text-purple-400'
                            }`}>
                            {completed ? (
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            ) : (
                                number.toString().padStart(2, '0')
                            )}
                        </div>
                        <span className={`badge ${difficultyStyles[difficulty]}`}>
                            {difficultyLabels[difficulty]}
                        </span>
                    </div>
                </div>

                {/* Title */}
                <h3 className="text-xl font-bold text-white mb-2 group-hover:text-purple-400 transition-colors duration-300">
                    {title}
                </h3>

                {/* Description */}
                <p className="text-slate-400 text-sm mb-4 line-clamp-2">
                    {description}
                </p>

                {/* Topics */}
                <div className="flex flex-wrap gap-2 mb-4">
                    {topics.slice(0, 4).map((topic, index) => (
                        <span
                            key={index}
                            className="text-xs px-2 py-1 rounded-md bg-slate-800/50 text-slate-400 border border-slate-700/50"
                        >
                            {topic}
                        </span>
                    ))}
                    {topics.length > 4 && (
                        <span className="text-xs px-2 py-1 rounded-md bg-purple-500/10 text-purple-400 border border-purple-500/30">
                            +{topics.length - 4} more
                        </span>
                    )}
                </div>

                {/* Quick action: mark as completed (inline, avoids extra navigation) */}
                <div className="mt-2 flex items-center justify-end">
                    <span
                        role="button"
                        aria-label="Mark module as completed"
                        onClick={(e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            markAsCompleted(slug);
                        }}
                        className="text-xs text-slate-300 hover:text-white cursor-pointer select-none"
                    >
                        {isCompleted(slug) ? 'Completed' : 'Mark Complete'}
                    </span>
                </div>

                {/* Footer */}
                <div className="flex items-center justify-between pt-4 border-t border-slate-700/50">
                    <span className="text-sm text-slate-500">{topics.length} topics</span>
                    <span className={`flex items-center gap-1 text-sm font-medium group-hover:gap-2 transition-all duration-300 ${completed ? 'text-green-400' : 'text-purple-400'
                        }`}>
                        {completed ? 'Review Module' : 'Start Learning'}
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                    </span>
                </div>
            </div>
        </Link>
    );
}
