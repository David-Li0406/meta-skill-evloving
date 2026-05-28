'use client';

import { isMedical } from '@/lib/brand';

// ===========================================
// FEED FILTER TABS - Modern SaaS 2026 Style
// Clean, minimal, trendy emojis
// ===========================================

export type FeedFilter = 'all' | 'missions' | 'profiles' | 'services';

interface FeedFilterTabsProps {
    value: FeedFilter;
    onChange: (filter: FeedFilter) => void;
    showServices?: boolean;
}

// Modern SaaS 2026 tabs with trendy emojis
const TABS_SOCIAL: { value: FeedFilter; label: string; emoji: string }[] = [
    { value: 'all', label: 'Tout', emoji: '⚡' },
    { value: 'missions', label: 'Renforts', emoji: '🆘' },
    { value: 'profiles', label: 'Talents', emoji: '✦' },
    { value: 'services', label: 'SocioLive', emoji: '🎥' },
];

const TABS_MEDICAL: { value: FeedFilter; label: string; emoji: string }[] = [
    { value: 'all', label: 'Tout', emoji: '⚡' },
    { value: 'missions', label: 'Missions', emoji: '🏥' },
    { value: 'profiles', label: 'Soignants', emoji: '✦' },
];

export function FeedFilterTabs({ value, onChange, showServices = true }: FeedFilterTabsProps) {
    const baseTabs = isMedical() ? TABS_MEDICAL : TABS_SOCIAL;
    const visibleTabs = showServices
        ? baseTabs
        : baseTabs.filter(tab => tab.value !== 'services');

    return (
        <div className="flex justify-center">
            <div className="inline-flex items-center gap-0.5 p-1 rounded-2xl bg-slate-100 border border-slate-200/50">
                {visibleTabs.map((tab) => (
                    <button
                        key={tab.value}
                        onClick={() => onChange(tab.value)}
                        className={`
                            relative px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200
                            ${value === tab.value
                                ? 'bg-white text-slate-900 shadow-sm ring-1 ring-slate-900/5'
                                : 'text-slate-500 hover:text-slate-700 hover:bg-white/60'
                            }
                        `}
                    >
                        <span className="mr-1.5 opacity-90">{tab.emoji}</span>
                        <span>{tab.label}</span>
                    </button>
                ))}
            </div>
        </div>
    );
}
