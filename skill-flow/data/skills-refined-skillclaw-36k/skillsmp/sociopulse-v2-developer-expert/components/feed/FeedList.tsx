'use client';

import { useEffect, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Search } from 'lucide-react';
import { MissionCard, ServiceCard } from '@/components/wall';
import { SocialPostCard, type SocialPostCardItem } from './SocialPostCard';
import { FeedSkeleton } from './FeedSkeleton';

// ===========================================
// TYPES
// ===========================================

export interface MissionItem {
    id: string;
    authorId?: string;
    type: 'MISSION';
    title: string;
    city?: string | null;
    content?: string;
    urgencyLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    hourlyRate?: number | null;
    category?: string | null;
    createdAt?: string | Date;
    tags?: string[];
}

export interface ServiceItem {
    id: string;
    authorId?: string;
    type: 'SERVICE';
    title?: string;
    name?: string;
    city?: string | null;
    content?: string;
    serviceType?: 'WORKSHOP' | 'COACHING_VIDEO' | string | null;
    category?: string | null;
    basePrice?: number | null;
    imageUrl?: string | null;
    tags?: string[];
}

export type SocialPostItem = SocialPostCardItem;

export type FeedItem = MissionItem | ServiceItem | SocialPostItem;

export interface FeedListProps {
    items: FeedItem[];
    isLoading: boolean;
    hasMore: boolean;
    onLoadMore: () => void;
    currentUserId?: string | null;
    onSelfContact?: () => void;
}

// ===========================================
// ANIMATION
// ===========================================

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.08,
            delayChildren: 0.1,
        },
    },
};

const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
        opacity: 1,
        y: 0,
        transition: {
            type: 'spring' as const,
            stiffness: 100,
            damping: 15,
        },
    },
};

// ===========================================
// INFINITE SCROLL HOOK
// ===========================================

function useInView(
    callback: () => void,
    options?: IntersectionObserverInit
) {
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const element = ref.current;
        if (!element) return;

        const observer = new IntersectionObserver(
            (entries) => {
                if (entries[0].isIntersecting) {
                    callback();
                }
            },
            { threshold: 0.1, ...options }
        );

        observer.observe(element);

        return () => {
            observer.disconnect();
        };
    }, [callback, options]);

    return ref;
}

// ===========================================
// COMPONENT
// ===========================================

export function FeedList({
    items,
    isLoading,
    hasMore,
    onLoadMore,
    currentUserId,
    onSelfContact,
}: FeedListProps) {
    const router = useRouter();

    // Infinite scroll trigger
    const loadMoreTrigger = useInView(
        useCallback(() => {
            if (!isLoading && hasMore) {
                onLoadMore();
            }
        }, [isLoading, hasMore, onLoadMore])
    );

    // Initial loading state
    if (isLoading && items.length === 0) {
        return <FeedSkeleton count={6} />;
    }

    // Empty state
    if (!isLoading && items.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center py-20 text-center">
                <div className="w-16 h-16 rounded-full bg-slate-100 flex items-center justify-center mb-4">
                    <Search className="w-8 h-8 text-slate-400" />
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2">
                    Aucun résultat
                </h3>
                <p className="text-sm text-slate-500 max-w-sm">
                    Essayez de modifier vos filtres ou votre recherche pour trouver ce que vous cherchez.
                </p>
            </div>
        );
    }

    return (
        <>
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="columns-1 md:columns-2 xl:columns-3 gap-4 space-y-4"
            >
                {items.map((item) => (
                    <motion.div
                        key={item.id}
                        variants={itemVariants}
                        className="break-inside-avoid"
                    >
                        {item.type === 'MISSION' ? (
                            <MissionCard
                                data={item}
                                onClick={() => router.push(`/need/${item.id}`)}
                            />
                        ) : item.type === 'SERVICE' ? (
                            <ServiceCard
                                data={item}
                                currentUserId={currentUserId || undefined}
                                onSelfContact={onSelfContact}
                                onClick={() => router.push(`/offer/${item.id}`)}
                            />
                        ) : (
                            <SocialPostCard item={item} />
                        )}
                    </motion.div>
                ))}
            </motion.div>

            {/* Load More Trigger */}
            {hasMore && (
                <div ref={loadMoreTrigger} className="py-8 text-center">
                    {isLoading ? (
                        <FeedSkeleton count={3} />
                    ) : (
                        <button
                            onClick={onLoadMore}
                            className="btn-secondary"
                        >
                            Charger plus
                        </button>
                    )}
                </div>
            )}
        </>
    );
}
