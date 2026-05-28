'use client';

import type { ReactNode } from 'react';
import { useMemo, useRef, useState } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import type { LucideIcon } from 'lucide-react';
import {
    ChevronDown, Loader2, MapPin,
    Sparkles, Video, Palette, Search, Plus
} from 'lucide-react';
import { useAuth } from '@/lib/useAuth';
import { CreateActionModal, type CreateActionModalUser } from '@/components/create/CreateActionModal';
import { MissionCard } from './MissionCard';
import { ServiceCard } from './ServiceCard';
import { FeedSidebar, type SidebarData } from './FeedSidebar';
import { DemandsCarousel } from './DemandsCarousel';
import { FeaturedOffers } from './FeaturedOffers';
import { useWallFeed } from './useWallFeed';

// ===========================================
// WALL FEED CLIENT - Sociopulse "Wall Experience"
// NEW LAYOUT: Carousel + Featured + Mixed Feed
// ===========================================

export interface TalentPoolItem {
    id: string;
    name: string;
    role: string;
    avatar: string | null;
    rating: number;
}

export interface ActivityItem {
    id: string;
    text: string;
    time: string;
}

export interface FeedMeta {
    total: number;
    page: number;
    lastPage: number;
    hasNextPage: boolean;
}

interface WallFeedClientProps {
    initialData?: any[];
    initialFeed?: any[];
    initialMeta?: FeedMeta;
    initialNextCursor?: string | null;
    initialHasNextPage?: boolean;
    talentPool?: TalentPoolItem[];
    activity?: ActivityItem[];
    sidebarData?: SidebarData;
}

const isType = (item: any, type: string) => String(item?.type || '').toUpperCase() === type;

function SectionEmptyState({ icon: Icon, title, description, action }: { icon: LucideIcon; title: string; description: string; action?: ReactNode }) {
    return (
        <div className="rounded-3xl border-2 border-dashed border-slate-200 bg-white/60 backdrop-blur-md p-12 text-center">
            <div className="mx-auto mb-4 grid h-16 w-16 place-items-center rounded-2xl bg-white shadow-soft">
                <Icon className="h-8 w-8 text-slate-300" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
            <p className="mt-2 text-sm text-slate-600 max-w-sm mx-auto">{description}</p>
            {action && <div className="mt-6 flex justify-center">{action}</div>}
        </div>
    );
}

export function WallFeedClient({
    initialData,
    initialFeed,
    initialMeta,
    initialNextCursor = null,
    initialHasNextPage = false,
    talentPool = [],
    sidebarData,
}: WallFeedClientProps) {
    const resolvedInitialData = Array.isArray(initialData) ? initialData : Array.isArray(initialFeed) ? initialFeed : [];
    const resolvedHasNextPage = initialMeta?.hasNextPage ?? initialHasNextPage;

    const { user } = useAuth();
    const canPublish = Boolean(user && (user.role === 'CLIENT' || user.role === 'TALENT'));

    const { feed, isLoading, isLoadingMore, hasMore, loadMore, searchTerm, setSearchTerm } = useWallFeed({
        initialItems: resolvedInitialData,
        initialMeta,
        initialNextCursor,
        initialHasNextPage: resolvedHasNextPage,
    });

    const feedSectionRef = useRef<HTMLDivElement>(null);

    // Separate missions and services
    const missions = useMemo(() => feed.filter((item) => isType(item, 'MISSION')), [feed]);
    const services = useMemo(() => feed.filter((item) => isType(item, 'SERVICE')), [feed]);

    // Featured: first 4 services for the grid
    const featuredServices = useMemo(() => services.slice(0, 4), [services]);

    // Mixed feed: remaining items after featured (skip first 4 services, keep all missions)
    const mixedFeed = useMemo(() => {
        const remainingServices = services.slice(4);
        // Combine and sort by createdAt (newest first)
        const combined = [...missions, ...remainingServices];
        return combined.sort((a, b) => {
            const dateA = new Date(a.createdAt || 0).getTime();
            const dateB = new Date(b.createdAt || 0).getTime();
            return dateB - dateA;
        }).slice(0, 26); // Limit to 26 items
    }, [missions, services]);

    const scrollToFeed = () => {
        feedSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    return (
        <div className="relative min-h-screen bg-canvas overflow-hidden">
            {/* ========== HERO SECTION ========== */}
            <section className="relative w-full min-h-[55vh] md:min-h-[70vh] flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 overflow-hidden">
                {/* Ambient Background */}
                <div aria-hidden className="hero-mesh-gradient" />

                {/* Floating Orbs */}
                <div aria-hidden className="absolute inset-0 overflow-hidden pointer-events-none">
                    <div className="floating-orb floating-orb-1" style={{ top: '-15%', left: '10%' }} />
                    <div className="floating-orb floating-orb-2" style={{ top: '50%', right: '-10%' }} />
                    <div className="floating-orb floating-orb-3" style={{ bottom: '-10%', left: '30%' }} />
                </div>

                <div className="relative max-w-5xl mx-auto text-center z-10">
                    {/* Title */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
                        className="mb-8"
                    >
                        <h1 className="hero-title">
                            <span className="text-reveal" style={{ animationDelay: '0.1s' }}>LA PLATEFORME</span>
                            <br />
                            <span className="hero-title-gradient text-reveal" style={{ animationDelay: '0.3s' }}>
                                DU MÉDICO-SOCIAL
                            </span>
                        </h1>
                    </motion.div>

                    {/* Subtitle */}
                    <motion.h2
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.4 }}
                        className="text-lg sm:text-xl md:text-2xl lg:text-3xl font-semibold text-slate-600/90 max-w-3xl mx-auto leading-relaxed"
                    >
                        Un renfort demain.{' '}
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-live-500 to-brand-500">
                            Une Visio ou un Atelier maintenant.
                        </span>
                    </motion.h2>

                    {/* Search Bar */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.6 }}
                        className="relative mt-10 max-w-2xl mx-auto hero-search-glow"
                    >
                        <div className="relative glass rounded-full border border-white/60 shadow-soft-lg overflow-hidden">
                            <div className="relative">
                                <Search className="absolute left-6 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
                                <input
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    placeholder="Rechercher un renfort, une séance SocioLive ou un atelier..."
                                    className="w-full bg-transparent pl-14 pr-6 py-4 text-base font-medium tracking-tight text-slate-900 placeholder:text-slate-400/80 outline-none"
                                    autoComplete="off"
                                />
                            </div>
                        </div>
                    </motion.div>

                    {/* Publish CTA */}
                    {canPublish && user && (
                        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.7 }} className="mt-8">
                            <CreateActionModal
                                user={user as unknown as CreateActionModalUser}
                                trigger={
                                    <button type="button" className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-brand-600 via-brand-500 to-live-500 px-6 py-3 md:px-8 md:py-4 text-sm md:text-base font-semibold text-white shadow-soft-lg hover:shadow-xl active:scale-[0.98] transition-all duration-300 touch-target">
                                        <Plus className="h-5 w-5" />
                                        Publier une offre
                                    </button>
                                }
                            />
                        </motion.div>
                    )}
                </div>

                {/* Scroll Indicator */}
                <motion.button
                    onClick={scrollToFeed}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1 }}
                    className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-slate-400 hover:text-slate-600 transition-colors discover-btn"
                >
                    <span className="text-sm font-medium tracking-wide">Découvrir</span>
                    <ChevronDown className="w-5 h-5" />
                </motion.button>

                <div className="wave-pattern" />
            </section>

            {/* ========== MAIN CONTENT ========== */}
            <main ref={feedSectionRef} className="mx-auto max-w-[1600px] px-4 sm:px-6 lg:px-8 py-8 md:py-12 pb-safe">
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    <div className="lg:col-span-9">

                        {/* 1. DEMANDS CAROUSEL */}
                        <DemandsCarousel items={missions} />

                        {/* 2. FEATURED OFFERS (4 services) */}
                        <FeaturedOffers items={services} />

                        {/* 3. MIXED FEED - Fil d'actualité */}
                        <section>
                            <div className="flex items-center justify-between gap-4 mb-6">
                                <div className="flex items-center gap-3">
                                    <div className="h-10 w-10 rounded-xl bg-indigo-50 border border-indigo-100 grid place-items-center">
                                        <Sparkles className="h-5 w-5 text-indigo-600" />
                                    </div>
                                    <div>
                                        <p className="text-[10px] uppercase tracking-[0.2em] text-slate-500">
                                            🌍 Toutes les annonces
                                        </p>
                                        <h2 className="text-base font-bold tracking-tight text-slate-900">
                                            Fil d'actualité
                                        </h2>
                                    </div>
                                </div>
                                {mixedFeed.length > 0 && (
                                    <span className="text-sm text-slate-500 font-medium">
                                        {mixedFeed.length} publications
                                    </span>
                                )}
                            </div>

                            {isLoading && mixedFeed.length === 0 ? (
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {Array.from({ length: 6 }).map((_, index) => (
                                        <div key={index} className="rounded-2xl bg-white/60 backdrop-blur-md border border-white/60 shadow-soft animate-pulse h-[380px]" />
                                    ))}
                                </div>
                            ) : mixedFeed.length > 0 ? (
                                <AnimatePresence mode="wait">
                                    <motion.div
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        exit={{ opacity: 0 }}
                                        transition={{ duration: 0.2 }}
                                        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                                    >
                                        {mixedFeed.map((item, index) => (
                                            <motion.div
                                                key={String(item?.id ?? index)}
                                                initial={{ opacity: 0, y: 20 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                transition={{ duration: 0.3, delay: index * 0.02 }}
                                                className="h-full"
                                            >
                                                {isType(item, 'MISSION') ? (
                                                    <MissionCard data={item} />
                                                ) : (
                                                    <ServiceCard data={item} currentUserId={user?.id ?? undefined} />
                                                )}
                                            </motion.div>
                                        ))}
                                    </motion.div>
                                </AnimatePresence>
                            ) : (
                                <SectionEmptyState
                                    icon={Sparkles}
                                    title="Aucune publication"
                                    description="Affinez votre recherche ou revenez un peu plus tard."
                                    action={canPublish && user ? (
                                        <CreateActionModal user={user as unknown as CreateActionModalUser} trigger={
                                            <button type="button" className="inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r from-indigo-600 to-teal-500 px-5 py-3 text-sm font-semibold text-white shadow-soft">
                                                <Plus className="h-4 w-4" />
                                                Publier une annonce
                                            </button>
                                        } />
                                    ) : undefined}
                                />
                            )}

                            {/* Load More */}
                            {hasMore && (
                                <div className="mt-8">
                                    {isLoadingMore && (
                                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
                                            {[1, 2, 3].map((i) => (
                                                <div
                                                    key={`skeleton-${i}`}
                                                    className="rounded-2xl bg-white/60 backdrop-blur-md border border-white/60 shadow-soft animate-pulse h-[380px]"
                                                    aria-hidden="true"
                                                />
                                            ))}
                                        </div>
                                    )}

                                    <div className="flex justify-center">
                                        <button
                                            type="button"
                                            onClick={loadMore}
                                            className="btn-secondary min-w-[180px]"
                                            disabled={isLoadingMore}
                                            aria-label="Charger plus de contenus"
                                        >
                                            {isLoadingMore ? (
                                                <>
                                                    <Loader2 className="h-4 w-4 animate-spin" />
                                                    Chargement…
                                                </>
                                            ) : (
                                                'Charger plus'
                                            )}
                                        </button>
                                    </div>
                                </div>
                            )}
                        </section>
                    </div>

                    {/* SIDEBAR */}
                    <aside className="hidden lg:block lg:col-span-3">
                        <div className="sticky top-24">
                            <FeedSidebar talentPool={talentPool} initialData={sidebarData} />
                        </div>
                    </aside>
                </div>
            </main>
        </div>
    );
}
