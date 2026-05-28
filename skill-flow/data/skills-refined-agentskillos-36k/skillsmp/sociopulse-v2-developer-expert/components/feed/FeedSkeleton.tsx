'use client';

import { motion } from 'framer-motion';

// ===========================================
// TYPES
// ===========================================

export interface FeedSkeletonProps {
    count?: number;
}

// ===========================================
// ANIMATION VARIANTS
// ===========================================

const shimmer = {
    initial: { backgroundPosition: '-200% 0' },
    animate: {
        backgroundPosition: '200% 0',
        transition: {
            repeat: Infinity,
            duration: 1.5,
            ease: 'linear' as const,
        }
    }
};

// ===========================================
// SKELETON CARD
// ===========================================

function SkeletonCard() {
    return (
        <div className="card-surface overflow-hidden">
            {/* Hero Skeleton */}
            <motion.div
                className="h-36 bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100"
                style={{ backgroundSize: '200% 100%' }}
                variants={shimmer}
                initial="initial"
                animate="animate"
            />

            {/* Content Skeleton */}
            <div className="p-4 space-y-3">
                {/* Title */}
                <motion.div
                    className="h-5 w-3/4 rounded-lg bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100"
                    style={{ backgroundSize: '200% 100%' }}
                    variants={shimmer}
                    initial="initial"
                    animate="animate"
                />

                {/* Subtitle */}
                <motion.div
                    className="h-4 w-1/2 rounded-lg bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100"
                    style={{ backgroundSize: '200% 100%' }}
                    variants={shimmer}
                    initial="initial"
                    animate="animate"
                />

                {/* Description lines */}
                <div className="space-y-2 pt-2">
                    <motion.div
                        className="h-3 w-full rounded bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100"
                        style={{ backgroundSize: '200% 100%' }}
                        variants={shimmer}
                        initial="initial"
                        animate="animate"
                    />
                    <motion.div
                        className="h-3 w-5/6 rounded bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100"
                        style={{ backgroundSize: '200% 100%' }}
                        variants={shimmer}
                        initial="initial"
                        animate="animate"
                    />
                </div>

                {/* Tags */}
                <div className="flex gap-2 pt-2">
                    {[1, 2, 3].map((i) => (
                        <motion.div
                            key={i}
                            className="h-6 w-16 rounded-full bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100"
                            style={{ backgroundSize: '200% 100%' }}
                            variants={shimmer}
                            initial="initial"
                            animate="animate"
                        />
                    ))}
                </div>

                {/* Footer */}
                <div className="flex justify-between items-center pt-3 mt-3 border-t border-slate-100">
                    <div className="flex gap-2">
                        <motion.div
                            className="w-9 h-9 rounded-full bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100"
                            style={{ backgroundSize: '200% 100%' }}
                            variants={shimmer}
                            initial="initial"
                            animate="animate"
                        />
                        <motion.div
                            className="w-9 h-9 rounded-full bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100"
                            style={{ backgroundSize: '200% 100%' }}
                            variants={shimmer}
                            initial="initial"
                            animate="animate"
                        />
                    </div>
                    <motion.div
                        className="h-9 w-24 rounded-xl bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100"
                        style={{ backgroundSize: '200% 100%' }}
                        variants={shimmer}
                        initial="initial"
                        animate="animate"
                    />
                </div>
            </div>
        </div>
    );
}

// ===========================================
// MAIN COMPONENT
// ===========================================

export function FeedSkeleton({ count = 6 }: FeedSkeletonProps) {
    return (
        <div className="columns-1 md:columns-2 xl:columns-3 gap-4 space-y-4">
            {Array.from({ length: count }).map((_, index) => (
                <div key={index} className="break-inside-avoid">
                    <SkeletonCard />
                </div>
            ))}
        </div>
    );
}
