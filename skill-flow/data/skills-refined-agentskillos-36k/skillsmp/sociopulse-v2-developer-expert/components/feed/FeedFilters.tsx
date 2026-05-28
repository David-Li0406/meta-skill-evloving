'use client';

import { useCallback, useMemo } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion } from 'framer-motion';
import {
    Search,
    Zap,
    Dumbbell,
    Video,
    Heart,
    Palette,
    Filter,
    Stethoscope,
    Users,
} from 'lucide-react';
import { currentBrand, isMedical } from '@/lib/brand';
import { getAvailableServiceTypes } from '@/lib/jobs';

// ===========================================
// TYPES
// ===========================================

export interface FilterBadge {
    id: string;
    label: string;
    icon: typeof Zap;
    color: string;
    /** If true, only show in specific brand mode */
    brandRestriction?: 'MEDICAL' | 'SOCIAL' | null;
}

export interface FeedFiltersProps {
    searchQuery: string;
    onSearchChange: (query: string) => void;
    activeFilters: string[];
    onFilterToggle: (filterId: string) => void;
    /** Sync filters to URL search params */
    syncToUrl?: boolean;
}

// ===========================================
// CONSTANTS - Brand-Aware Filters
// ===========================================

const ALL_FILTER_BADGES: FilterBadge[] = [
    // Common filters
    { id: 'urgent', label: 'Urgent', icon: Zap, color: 'text-red-500', brandRestriction: null },

    // Medical-specific
    { id: 'soin', label: 'Soins', icon: Stethoscope, color: 'text-blue-500', brandRestriction: 'MEDICAL' },

    // Social-specific
    { id: 'sport', label: 'Sport', icon: Dumbbell, color: 'text-blue-500', brandRestriction: 'SOCIAL' },
    { id: 'bien-etre', label: 'Bien-être', icon: Heart, color: 'text-pink-500', brandRestriction: 'SOCIAL' },
    { id: 'art', label: 'Art', icon: Palette, color: 'text-orange-500', brandRestriction: 'SOCIAL' },

    // Ateliers/Visio - Only if showAteliers is true
    { id: 'visio', label: 'Visio', icon: Video, color: 'text-purple-500', brandRestriction: 'SOCIAL' },
    { id: 'educ', label: 'Éducatif', icon: Users, color: 'text-amber-500', brandRestriction: 'SOCIAL' },
];

// ===========================================
// COMPONENT
// ===========================================

export function FeedFilters({
    searchQuery,
    onSearchChange,
    activeFilters,
    onFilterToggle,
    syncToUrl = false,
}: FeedFiltersProps) {
    const router = useRouter();
    const searchParams = useSearchParams();

    // Filter badges based on current brand
    const availableFilters = useMemo(() => {
        const currentMode = currentBrand.mode;

        return ALL_FILTER_BADGES.filter(filter => {
            // If no brand restriction, always show
            if (filter.brandRestriction === null) return true;

            // Check brand restriction
            if (filter.brandRestriction === currentMode) return true;

            // Hide visio filter if ateliers are disabled
            if (filter.id === 'visio' && !currentBrand.showAteliers) return false;

            return false;
        });
    }, []);

    // Dynamic placeholder based on brand
    const searchPlaceholder = isMedical()
        ? 'Rechercher un soignant, une mission...'
        : 'Rechercher un professionnel, une mission, un atelier...';

    // Sync filter to URL when changed
    const handleFilterToggle = useCallback((filterId: string) => {
        onFilterToggle(filterId);

        if (syncToUrl) {
            const params = new URLSearchParams(searchParams.toString());
            const currentFilters = params.get('filters')?.split(',').filter(Boolean) || [];

            if (currentFilters.includes(filterId)) {
                const newFilters = currentFilters.filter(f => f !== filterId);
                if (newFilters.length > 0) {
                    params.set('filters', newFilters.join(','));
                } else {
                    params.delete('filters');
                }
            } else {
                params.set('filters', [...currentFilters, filterId].join(','));
            }

            router.replace(`?${params.toString()}`, { scroll: false });
        }
    }, [onFilterToggle, syncToUrl, searchParams, router]);

    // Sync search to URL with debounce
    const handleSearchChange = useCallback((value: string) => {
        onSearchChange(value);

        if (syncToUrl) {
            const params = new URLSearchParams(searchParams.toString());
            if (value.trim()) {
                params.set('q', value.trim());
            } else {
                params.delete('q');
            }
            router.replace(`?${params.toString()}`, { scroll: false });
        }
    }, [onSearchChange, syncToUrl, searchParams, router]);

    // Color for filter icon header
    const filterIconColor = isMedical() ? 'text-alert-400' : 'text-slate-400';

    return (
        <div className="space-y-4">
            {/* Search Bar */}
            <div className="relative max-w-2xl">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                    type="text"
                    placeholder={searchPlaceholder}
                    value={searchQuery}
                    onChange={(e) => handleSearchChange(e.target.value)}
                    className="input-premium pl-12 pr-4 w-full"
                    aria-label="Rechercher"
                />
            </div>

            {/* Filter Badges */}
            <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
                <span className={`flex-shrink-0 text-xs font-medium ${filterIconColor} mr-1`}>
                    <Filter className="w-4 h-4" />
                </span>
                {availableFilters.map((filter) => {
                    const Icon = filter.icon;
                    const isActive = activeFilters.includes(filter.id);
                    return (
                        <motion.button
                            key={filter.id}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => handleFilterToggle(filter.id)}
                            className={`
                                pill-btn flex-shrink-0 flex items-center gap-1.5
                                ${isActive ? 'pill-btn-active' : 'pill-btn-inactive'}
                            `}
                        >
                            <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : filter.color}`} />
                            {filter.label}
                        </motion.button>
                    );
                })}
            </div>
        </div>
    );
}
