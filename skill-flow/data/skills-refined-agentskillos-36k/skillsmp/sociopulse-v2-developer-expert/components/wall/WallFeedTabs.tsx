'use client';

import { motion } from 'framer-motion';
import { AlertCircle, GraduationCap } from 'lucide-react';

// ===========================================
// WALL FEED TABS - Tab Navigation Component
// Onglet A: 🚨 SOS RENFORT (Missions)
// Onglet B: 🎓 SOCIOLIVE & ATELIERS (Services)
// ===========================================

export type FeedTab = 'renfort' | 'ateliers';

export interface WallFeedTabsProps {
    activeTab: FeedTab;
    onTabChange: (tab: FeedTab) => void;
    missionCount?: number;
    serviceCount?: number;
}

const tabConfig = {
    renfort: {
        id: 'renfort' as const,
        label: 'SOS RENFORT',
        icon: AlertCircle,
        emoji: '🚨',
        activeColors: 'bg-rose-500 text-white shadow-lg shadow-rose-500/25',
        inactiveColors: 'bg-white text-slate-600 hover:bg-rose-50 hover:text-rose-600 border border-slate-200',
        countBg: 'bg-rose-600',
    },
    ateliers: {
        id: 'ateliers' as const,
        label: 'SOCIOLIVE & ATELIERS',
        icon: GraduationCap,
        emoji: '🎓',
        activeColors: 'bg-gradient-to-r from-teal-500 to-indigo-500 text-white shadow-lg shadow-teal-500/25',
        inactiveColors: 'bg-white text-slate-600 hover:bg-teal-50 hover:text-teal-600 border border-slate-200',
        countBg: 'bg-teal-600',
    },
};

export function WallFeedTabs({ activeTab, onTabChange, missionCount, serviceCount }: WallFeedTabsProps) {
    const tabs = [
        { ...tabConfig.renfort, count: missionCount },
        { ...tabConfig.ateliers, count: serviceCount },
    ];

    return (
        <div className="flex flex-col sm:flex-row gap-3 mb-8">
            {tabs.map((tab) => {
                const isActive = activeTab === tab.id;
                const Icon = tab.icon;

                return (
                    <motion.button
                        key={tab.id}
                        type="button"
                        onClick={() => onTabChange(tab.id)}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className={`
                            relative flex-1 sm:flex-initial flex items-center justify-center gap-2
                            px-6 py-4 rounded-2xl font-bold text-sm
                            transition-all duration-300 ease-out
                            ${isActive ? tab.activeColors : tab.inactiveColors}
                        `}
                        aria-pressed={isActive}
                        aria-label={`${tab.label} - ${tab.count ?? 0} éléments`}
                    >
                        <span className="text-lg" aria-hidden="true">{tab.emoji}</span>
                        <Icon className="w-4 h-4" aria-hidden="true" />
                        <span className="tracking-wide">{tab.label}</span>

                        {/* Count Badge */}
                        {tab.count !== undefined && tab.count > 0 && (
                            <span
                                className={`
                                    ml-1 px-2 py-0.5 rounded-full text-xs font-bold
                                    ${isActive ? 'bg-white/20 text-white' : `${tab.countBg} text-white`}
                                `}
                            >
                                {tab.count}
                            </span>
                        )}

                        {/* Active Indicator */}
                        {isActive && (
                            <motion.div
                                layoutId="activeTabIndicator"
                                className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-8 h-1 rounded-full bg-current opacity-50"
                                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                            />
                        )}
                    </motion.button>
                );
            })}
        </div>
    );
}
