'use client';

import { useRef, useEffect, useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ChevronLeft, ChevronRight, MapPin, Euro, Zap, Building2, Clock } from 'lucide-react';

// ===========================================
// DEMANDS CAROUSEL - Horizontal Ticker
// Compact mission cards in auto-scrolling rail
// ===========================================

interface DemandItem {
    id: string;
    title?: string;
    jobTitle?: string;
    city?: string;
    hourlyRate?: number;
    urgencyLevel?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    client?: {
        establishment?: {
            name?: string;
            logoUrl?: string;
            city?: string;
        };
    };
    createdAt?: string;
}

interface DemandsCarouselProps {
    items: DemandItem[];
}

const urgencyConfig = {
    LOW: { label: '1 sem.', color: 'bg-slate-100 text-slate-600', dot: 'bg-slate-400', urgent: false },
    MEDIUM: { label: '48h', color: 'bg-amber-100 text-amber-700', dot: 'bg-amber-500', urgent: false },
    HIGH: { label: '24h', color: 'bg-rose-100 text-rose-700', dot: 'bg-rose-500', urgent: true },
    CRITICAL: { label: 'Urgent', color: 'bg-rose-500 text-white', dot: 'bg-white', urgent: true },
};

function CompactMissionCard({ item }: { item: DemandItem }) {
    const establishment = item.client?.establishment?.name || 'Établissement';
    const city = item.city || item.client?.establishment?.city || 'France';
    const title = item.title || item.jobTitle || 'Mission de renfort';
    const hourlyRate = item.hourlyRate;
    const urgency = urgencyConfig[item.urgencyLevel || 'MEDIUM'];
    const isUrgent = urgency.urgent;

    return (
        <Link href={`/need/${item.id}`} className="block">
            <motion.div
                whileHover={{ y: -4, scale: 1.02 }}
                className="relative bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-lg transition-all duration-300 p-4 min-w-[260px] sm:min-w-[280px] max-w-[280px] h-[140px] flex flex-col snap-start"
            >
                {/* Urgency Badge */}
                <div className="absolute -top-2 right-3">
                    <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-[10px] font-bold ${urgency.color} shadow-sm`}>
                        {isUrgent && <Zap className="w-3 h-3" />}
                        <span className={`w-1.5 h-1.5 rounded-full ${urgency.dot} ${isUrgent ? 'animate-pulse' : ''}`} />
                        {urgency.label}
                    </span>
                </div>

                {/* Header */}
                <div className="flex items-center gap-2 mb-2">
                    <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center">
                        <Building2 className="w-4 h-4 text-slate-400" />
                    </div>
                    <div className="min-w-0 flex-1">
                        <p className="text-xs font-medium text-slate-500 truncate">{establishment}</p>
                    </div>
                </div>

                {/* Title */}
                <h3 className="text-sm font-bold text-slate-900 line-clamp-2 flex-1 leading-snug">
                    {title}
                </h3>

                {/* Footer */}
                <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-100">
                    <div className="flex items-center gap-1 text-xs text-slate-500">
                        <MapPin className="w-3 h-3" />
                        <span className="truncate max-w-[100px]">{city}</span>
                    </div>
                    {hourlyRate && (
                        <div className="flex items-center gap-1 text-xs font-bold text-rose-600">
                            <Euro className="w-3 h-3" />
                            <span>{hourlyRate}€/h</span>
                        </div>
                    )}
                </div>
            </motion.div>
        </Link>
    );
}

export function DemandsCarousel({ items }: DemandsCarouselProps) {
    const scrollRef = useRef<HTMLDivElement>(null);
    const [isPaused, setIsPaused] = useState(false);

    // Auto-scroll effect
    useEffect(() => {
        if (items.length <= 3 || isPaused) return;

        const interval = setInterval(() => {
            const node = scrollRef.current;
            if (!node) return;

            const maxScroll = node.scrollWidth - node.clientWidth;
            if (node.scrollLeft >= maxScroll - 10) {
                node.scrollTo({ left: 0, behavior: 'smooth' });
            } else {
                node.scrollBy({ left: 300, behavior: 'smooth' });
            }
        }, 4000);

        return () => clearInterval(interval);
    }, [items.length, isPaused]);

    const scroll = (direction: 'prev' | 'next') => {
        const node = scrollRef.current;
        if (!node) return;
        node.scrollBy({ left: direction === 'prev' ? -300 : 300, behavior: 'smooth' });
    };

    if (items.length === 0) return null;

    return (
        <section className="mb-10">
            {/* Header */}
            <div className="flex items-center justify-between gap-4 mb-4">
                <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-xl bg-rose-50 border border-rose-100 grid place-items-center">
                        <MapPin className="h-5 w-5 text-rose-500" />
                    </div>
                    <div>
                        <p className="text-[10px] uppercase tracking-[0.2em] text-rose-600 font-semibold">
                            📍 Demandes de renfort
                        </p>
                        <h2 className="text-base font-bold tracking-tight text-slate-900">
                            Établissements qui recrutent
                        </h2>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <button
                        type="button"
                        onClick={() => scroll('prev')}
                        aria-label="Défiler vers la gauche"
                        className="h-10 w-10 md:h-9 md:w-9 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 shadow-sm grid place-items-center transition-colors touch-target"
                    >
                        <ChevronLeft className="h-5 w-5 md:h-4 md:w-4 text-slate-600" />
                    </button>
                    <button
                        type="button"
                        onClick={() => scroll('next')}
                        aria-label="Défiler vers la droite"
                        className="h-10 w-10 md:h-9 md:w-9 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 shadow-sm grid place-items-center transition-colors touch-target"
                    >
                        <ChevronRight className="h-5 w-5 md:h-4 md:w-4 text-slate-600" />
                    </button>
                </div>
            </div>

            {/* Carousel Rail */}
            <div
                ref={scrollRef}
                onMouseEnter={() => setIsPaused(true)}
                onMouseLeave={() => setIsPaused(false)}
                className="flex gap-4 overflow-x-auto pb-2 scrollbar-none scroll-smooth -mx-1 px-1 snap-x snap-mandatory touch-scroll"
            >
                {items.map((item, index) => (
                    <CompactMissionCard key={item.id || index} item={item} />
                ))}
            </div>
        </section>
    );
}
