'use client';

import { useState, useTransition } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, ChevronDown } from 'lucide-react';
import { PublicOpportunityCard, type PublicOpportunityItem } from './PublicOpportunityCard';
import { FeedFilterTabs, type FeedFilter } from './FeedFilterTabs';
import { SocialProofSidebar } from './SocialProofSidebar';
import { currentBrand } from '@/lib/brand';

// ===========================================
// PUBLIC SMART FEED - SSR + Load More Container
// 2-Column Layout: Feed Grid + Sticky Sidebar
// ===========================================

interface FeedMeta {
    page: number;
    hasNextPage: boolean;
    total?: number;
}

interface PublicSmartFeedProps {
    initialItems: PublicOpportunityItem[];
    initialMeta: FeedMeta;
    viewMode: 'establishment' | 'talent';
}

// Skeleton card for loading state
function SkeletonCard() {
    return (
        <div className="rounded-2xl border border-slate-200 bg-white/50 p-5 animate-pulse">
            <div className="flex justify-between mb-4">
                <div className="h-6 w-20 bg-slate-200 rounded-full" />
                <div className="h-6 w-16 bg-slate-200 rounded-full" />
            </div>
            <div className="h-5 w-3/4 bg-slate-200 rounded mb-2" />
            <div className="h-4 w-1/2 bg-slate-200 rounded mb-3" />
            <div className="flex gap-2">
                <div className="h-6 w-16 bg-slate-200 rounded-full" />
                <div className="h-6 w-20 bg-slate-200 rounded-full" />
            </div>
        </div>
    );
}

export function PublicSmartFeed({
    initialItems,
    initialMeta,
    viewMode
}: PublicSmartFeedProps) {
    const [items, setItems] = useState<PublicOpportunityItem[]>(initialItems);
    const [meta, setMeta] = useState<FeedMeta>(initialMeta);
    const [filter, setFilter] = useState<FeedFilter>('all');
    const [isPending, startTransition] = useTransition();

    // Filter items based on selected tab
    const filteredItems = items.filter(item => {
        if (filter === 'all') return true;
        if (filter === 'missions') return item.type === 'mission';
        if (filter === 'profiles') return item.type === 'profile';
        if (filter === 'services') return item.type === 'service';
        return true;
    });

    // Load more handler
    const handleLoadMore = () => {
        startTransition(async () => {
            try {
                const nextPage = meta.page + 1;
                const typeParam = viewMode === 'establishment' ? 'profile' : 'mission';
                const appModeParam = currentBrand.mode;

                const response = await fetch(
                    `/api/v1/wall-feed?page=${nextPage}&limit=10&type=${typeParam}&appMode=${appModeParam}`
                );

                if (!response.ok) throw new Error('Failed to load');

                const data = await response.json();

                const newItems: PublicOpportunityItem[] = (data.data || []).map((item: any) => ({
                    id: item.id,
                    type: item.type?.toLowerCase() === 'mission' ? 'mission'
                        : item.type?.toLowerCase() === 'service' ? 'service'
                            : 'profile',
                    title: item.title || item.name || 'Untitled',
                    subtitle: item.description || item.content,
                    location: item.city,
                    price: item.hourlyRate || item.basePrice,
                    imageUrl: item.imageUrl,
                    avatarUrl: item.profile?.avatarUrl || item.authorAvatar,
                    isUrgent: item.urgencyLevel === 'HIGH' || item.urgencyLevel === 'CRITICAL',
                    isAvailable: true,
                    tags: item.tags || item.requiredSkills || [],
                    category: item.category,
                    expiresAt: item.validUntil || item.startDate,
                    rating: item.profile?.averageRating,
                }));

                setItems(prev => [...prev, ...newItems]);
                setMeta({
                    page: nextPage,
                    hasNextPage: data.meta?.hasNextPage ?? false,
                    total: data.meta?.total,
                });

                // Update URL silently
                const url = new URL(window.location.href);
                url.searchParams.set('page', String(nextPage));
                window.history.replaceState({}, '', url.toString());

            } catch (error) {
                console.error('Failed to load more:', error);
            }
        });
    };

    // Empty state
    if (filteredItems.length === 0 && !isPending) {
        return (
            <section className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
                <div className="flex gap-8">
                    <div className="flex-1">
                        <FeedFilterTabs
                            value={filter}
                            onChange={setFilter}
                            showServices={currentBrand.showAteliers}
                        />
                        <div className="py-16 text-center">
                            <p className="text-slate-500 text-lg">
                                Aucun résultat pour ce filtre
                            </p>
                        </div>
                    </div>
                    <SocialProofSidebar />
                </div>
            </section>
        );
    }

    return (
        <section className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
            {/* 2-Column Layout: Feed + Sidebar */}
            <div className="flex gap-8">

                {/* Main Feed Column */}
                <div className="flex-1 min-w-0">
                    {/* SEO Section Header */}
                    <div className="mb-6">
                        <h1 className="sr-only">
                            {currentBrand.showAteliers
                                ? 'Offres de missions et ateliers médico-social - SocioPulse'
                                : 'Offres de missions soignants et renforts santé - MedicoPulse'
                            }
                        </h1>
                        <p className="text-sm text-slate-500 text-center">
                            Découvrez les dernières opportunités
                        </p>
                    </div>

                    {/* Filter Tabs */}
                    <FeedFilterTabs
                        value={filter}
                        onChange={setFilter}
                        showServices={currentBrand.showAteliers}
                    />

                    {/* Feed Grid */}
                    <motion.div
                        layout
                        className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5 sm:gap-6 mt-8"
                    >
                        <AnimatePresence mode="popLayout">
                            {filteredItems.map((item, index) => (
                                <motion.div
                                    key={item.id}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, scale: 0.95 }}
                                    transition={{ delay: index * 0.03, duration: 0.25 }}
                                    layout
                                >
                                    <PublicOpportunityCard item={item} />
                                </motion.div>
                            ))}
                        </AnimatePresence>

                        {/* Loading Skeletons */}
                        {isPending && (
                            <>
                                <SkeletonCard />
                                <SkeletonCard />
                                <SkeletonCard />
                            </>
                        )}
                    </motion.div>

                    {/* Load More Button */}
                    {meta.hasNextPage && (
                        <div className="flex justify-center mt-8">
                            <button
                                onClick={handleLoadMore}
                                disabled={isPending}
                                className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-white border border-slate-200 text-slate-700 font-medium hover:bg-slate-50 hover:border-slate-300 active:scale-[0.98] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isPending ? (
                                    <>
                                        <Loader2 className="h-4 w-4 animate-spin" />
                                        Chargement...
                                    </>
                                ) : (
                                    <>
                                        <ChevronDown className="h-4 w-4" />
                                        Voir plus
                                    </>
                                )}
                            </button>
                        </div>
                    )}

                    {/* Results count */}
                    {meta.total && (
                        <p className="text-center text-sm text-slate-500 mt-4">
                            {filteredItems.length} sur {meta.total} résultats
                        </p>
                    )}
                </div>

                {/* Sticky Sidebar - Social Proof */}
                <SocialProofSidebar />
            </div>
        </section>
    );
}
