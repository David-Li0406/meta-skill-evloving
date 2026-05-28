'use client';

import { useRef } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ChevronLeft, ChevronRight, ArrowRight } from 'lucide-react';
import { UniverseCard } from './UniverseCard';
import type { SeedItem } from '@/lib/seedData';

// ===========================================
// UNIVERSE RAIL - Netflix-Style Carousel
// ===========================================

interface UniverseRailProps {
    title: string;
    punchline: string;
    accentColor: 'rose' | 'indigo' | 'teal';
    items: SeedItem[];
    viewAllHref?: string;
}

const accentClasses = {
    rose: {
        icon: 'bg-alert-100 text-alert-600',
        link: 'text-alert-600 hover:text-alert-700',
        button: 'bg-alert-50 hover:bg-alert-100 text-alert-600',
    },
    indigo: {
        icon: 'bg-brand-100 text-brand-600',
        link: 'text-brand-600 hover:text-brand-700',
        button: 'bg-brand-50 hover:bg-brand-100 text-brand-600',
    },
    teal: {
        icon: 'bg-live-100 text-live-600',
        link: 'text-live-600 hover:text-live-700',
        button: 'bg-live-50 hover:bg-live-100 text-live-600',
    },
};

export function UniverseRail({
    title,
    punchline,
    accentColor,
    items,
    viewAllHref = '/feed'
}: UniverseRailProps) {
    const scrollRef = useRef<HTMLDivElement>(null);
    const colors = accentClasses[accentColor];

    const scroll = (direction: 'left' | 'right') => {
        if (scrollRef.current) {
            const scrollAmount = 340; // Card width + gap
            scrollRef.current.scrollBy({
                left: direction === 'left' ? -scrollAmount : scrollAmount,
                behavior: 'smooth',
            });
        }
    };

    if (items.length === 0) return null;

    return (
        <motion.section
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-50px' }}
            transition={{ duration: 0.6 }}
            className="py-8"
        >
            {/* Header */}
            <div className="flex items-start sm:items-center justify-between gap-4 mb-6 px-4 sm:px-6 lg:px-8">
                <div className="flex-1">
                    <h2 className="text-xl sm:text-2xl font-bold text-slate-900 mb-1">
                        {title}
                    </h2>
                    <p className="text-sm sm:text-base text-slate-600">
                        {punchline}
                    </p>
                </div>

                <div className="flex items-center gap-3">
                    {/* Navigation Buttons - Desktop */}
                    <div className="hidden sm:flex items-center gap-2">
                        <button
                            onClick={() => scroll('left')}
                            className={`p-2 rounded-full ${colors.button} transition-colors`}
                            aria-label="Précédent"
                        >
                            <ChevronLeft className="h-5 w-5" />
                        </button>
                        <button
                            onClick={() => scroll('right')}
                            className={`p-2 rounded-full ${colors.button} transition-colors`}
                            aria-label="Suivant"
                        >
                            <ChevronRight className="h-5 w-5" />
                        </button>
                    </div>

                    {/* View All Link */}
                    <Link
                        href={viewAllHref}
                        className={`inline-flex items-center gap-1 text-sm font-semibold ${colors.link} transition-colors`}
                    >
                        Tout voir
                        <ArrowRight className="h-4 w-4" />
                    </Link>
                </div>
            </div>

            {/* Scrollable Rail */}
            <div
                ref={scrollRef}
                className="flex gap-4 overflow-x-auto scrollbar-none snap-x snap-mandatory scroll-smooth pl-4 sm:pl-6 lg:pl-8 pr-4 sm:pr-6 lg:pr-8 pb-2"
                style={{ scrollPaddingLeft: '1rem' }}
            >
                {items.map((item, index) => (
                    <UniverseCard
                        key={`${item.data.title}-${index}`}
                        item={item}
                        accentColor={accentColor}
                    />
                ))}

                {/* View All Card */}
                <Link
                    href={viewAllHref}
                    className={`flex-shrink-0 w-[280px] sm:w-[320px] snap-center rounded-2xl border-2 border-dashed border-slate-200 hover:border-slate-300 bg-slate-50/50 flex flex-col items-center justify-center min-h-[280px] transition-colors group`}
                >
                    <div className={`w-14 h-14 rounded-full ${colors.icon} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                        <ArrowRight className="h-6 w-6" />
                    </div>
                    <span className="font-semibold text-slate-700">Voir tout</span>
                    <span className="text-sm text-slate-500 mt-1">{items.length}+ offres</span>
                </Link>
            </div>
        </motion.section>
    );
}
